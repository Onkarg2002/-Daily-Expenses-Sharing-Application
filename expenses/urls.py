from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AddExpenseView, HomeView, UserListView, ExpenseListView, UserRegistrationView, BalanceSheetView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', AddExpenseView.as_view(), name='add_expense'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('balance_sheet/<int:pk>/', BalanceSheetView.as_view(), name='balance_sheet_view'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
