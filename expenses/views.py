
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import csv
from django.views import View
from io import StringIO
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Expense, ExpenseParticipant
from .serializers import UserSerializer, ExpenseSerializer, ExpenseParticipantSerializer
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        split_method = data.get('split_method')
        total_amount = float(data.get('total_amount'))
        participants_data = data.get('participants', [])

        if not isinstance(participants_data, list):
            return Response({"error": "Participants data should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            created_by = User.objects.get(id=data.get('created_by'))
        except User.DoesNotExist:
            return Response({"error": "Creator user does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if split_method == 'percentage':
            total_percentage = sum([p.get('percentage', 0) for p in participants_data])
            if total_percentage != 100:
                return Response({"error": "Percentages must add up to 100%"}, status=status.HTTP_400_BAD_REQUEST)

        expense = Expense.objects.create(
            description=data.get('description'),
            total_amount=total_amount,
            split_method=split_method,
            created_by=created_by
        )

        for participant_data in participants_data:
            user_id = participant_data.get('user')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": f"Participant user with id {user_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            if split_method == 'equal':
                amount_owed = total_amount / len(participants_data)
            elif split_method == 'exact':
                amount_owed = participant_data.get('amount')
            elif split_method == 'percentage':
                amount_owed = (total_amount * participant_data.get('percentage')) / 100

            ExpenseParticipant.objects.create(
                user=user,
                expense=expense,
                amount_owed=amount_owed
            )

        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def overall_expenses(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def individual_expenses(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        expenses = Expense.objects.filter(expenseparticipant__user=user).distinct()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download_balance_sheet(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        expenses = Expense.objects.filter(expenseparticipant__user=user).distinct()

        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Expense ID', 'Description', 'Total Amount', 'Split Method', 'Amount Owed'])

        for expense in expenses:
            participants = ExpenseParticipant.objects.filter(expense=expense)
            amount_owed = 0
            for participant in participants:
                if participant.user == user:
                    amount_owed = participant.amount_owed

            csv_writer.writerow([
                expense.id,
                expense.description,
                expense.total_amount,
                expense.split_method,
                amount_owed
            ])

        csv_file.seek(0)
        response = HttpResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="balance_sheet_user_{user.id}.csv"'

        return response

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'user_list.html', {'users': users})

class ExpenseListView(View):
    def get(self, request):
        expenses = Expense.objects.all()
        return render(request, 'expense_list.html', {'expenses': expenses})


class AddExpenseView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'add_expense.html', {'users': users})

    def post(self, request):
        description = request.POST.get('description')
        total_amount = float(request.POST.get('total_amount'))
        split_method = request.POST.get('split_method')
        created_by_id = request.POST.get('created_by')

        try:
            created_by = User.objects.get(id=created_by_id)
        except User.DoesNotExist:
            return render(request, 'add_expense.html', {'error': 'Creator user does not exist.', 'users': User.objects.all()})

       
        expense = Expense.objects.create(
            description=description,
            total_amount=total_amount,
            split_method=split_method,
            created_by=created_by
        )

       
        amount_owed = total_amount
        ExpenseParticipant.objects.create(
            user=created_by,
            expense=expense,
            amount_owed=amount_owed
        )

        return redirect('expense_list')
    
class UserRegistrationView(View):
    def get(self, request):
        return render(request, 'user_registration.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'user_registration.html', {'error': 'Email is already in use.'})

        User.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        return redirect('home')


class BalanceSheetView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        expenses = Expense.objects.filter(expenseparticipant__user=user).distinct()
        return render(request, 'balance_sheet.html', {'user': user, 'expenses': expenses})
