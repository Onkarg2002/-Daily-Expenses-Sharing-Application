from rest_framework import serializers
from .models import User, Expense, ExpenseParticipant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number']

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = ['user', 'amount_owed']

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'description', 'total_amount', 'split_method', 'created_by', 'participants']
