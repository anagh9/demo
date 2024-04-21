from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from .models import User, IncomeExpense


@login_required
def index(request):
    all_income = IncomeExpense.objects.filter(user=request.user).all()

    return render(request, 'app/index.html', {'all_income': all_income })


@login_required
def add_expense(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        user = request.user
        amount = data['amount']
        description = data['description']
        date = data['date']
        category = data['category']
        type = data['type']

        income_expense = IncomeExpense(
            user=user, amount=amount, description=description, date=date, category=category, type=type)

        income_expense.save()

        messages.success(request, 'Expense added successfully !! ')
        return redirect('app:index')
    return render(request, 'app/add.html')


@login_required
def edit_expense(request, expense_id):
    expense = IncomeExpense.objects.get(id=expense_id)
    if request.method == 'POST':
        data = request.POST
        expense.amount = data['amount']
        expense.description = data['description']
        expense.date = data['date']
        expense.category = data['category']
        expense.type = data['type']

        expense.save()

        messages.success(request, 'Expense updated successfully !! ')
        return redirect('app:index')
    return render(request, 'app/edit.html', {'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = IncomeExpense.objects.get(id=expense_id)
    if request.user != expense.user:
        messages.error(
            request, 'You are not authorized to delete this expense !! ')
        return redirect('app:index')
    expense.delete()
    messages.success(request, 'Expense deleted successfully !! ')
    return redirect('app:index')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(
                request, 'User not found or password is incorrect !! ')
            return render(request, 'app/login.html')
        auth_login(request, user)
        return redirect('app:index')
    return render(request, 'app/login.html')


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'app/login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'app/register.html')

        user = User(name=name, email=email)
        user.set_password(password)
        user.save()
        auth_login(request, user)
        return redirect('app:index')
    return render(request, 'app/register.html')
