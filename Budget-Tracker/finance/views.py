from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Income, Expense, Budget, EMI, Category
from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
from datetime import date
from django.db.models import Sum, Q, F, DecimalField, ExpressionWrapper
from .forms import Budget
from .models import BudgetCategory

 
User = get_user_model()
 
def home(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    balance = total_income - total_expense
    income_progress = (total_income / 10000) * 100  
    expense_progress = (total_expense / 10000) * 100  

    # Pass values to the template
    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'income_progress': income_progress,
        'expense_progress': expense_progress,
    }

    return render(request, 'home.html', context)


# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('home')
        messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')


# Register view
def register_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        else:
            user = User.objects.create_user(email=email, password=password, name=name, phone=phone)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('home')
    return render(request, 'register.html')
# Budget settings
def budget_setting_view(request):
    if request.method == 'POST':
        form = BudgetSettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgets')
    else:
        form = BudgetSettingForm()
    categories = Category.objects.filter(user=request.user)
    return render(request, 'budget_setting.html', {'form': form, 'categories': categories})
# Budget report
def budget_report(request):
    categories = BudgetCategory.objects.all()
    return render(request, 'budget/report.html', {'categories': categories})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# Expenses
@login_required
def expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses.html', context={'expenses': expenses})


@login_required
def expense_add(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        description = request.POST.get('description', '')     
        expense_date = request.POST.get('date', date.today()) 
        if not category_id:
            messages.error(request, "Please select a category.")
            return redirect('expense_add')
        try:
            category = Category.objects.get(id=category_id, user=request.user, category_type='Expense')
        except Category.DoesNotExist:
            messages.error(request, "Please select a valid expense category.")
            return redirect('expense_add')
        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description,
            date=expense_date
        )
        messages.success(request, "Expense added successfully!")
        return redirect('expenses')
    categories = Category.objects.filter(user=request.user, category_type='Expense')
    return render(request, 'expense_add.html', {'categories': categories})



@login_required
def expense_update(request, id):
    expense = get_object_or_404(Expense, user=request.user, id=id)
    if request.method == "POST":
        expense.amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        expense.description = request.POST.get('description')
        expense.date = request.POST.get('date')
        expense.category = get_object_or_404(Category, id=category_id, user=request.user, category_type='Expense')
        expense.save()
        messages.success(request, "Expense updated successfully.")
        return redirect('expenses')
    categories = Category.objects.filter(user=request.user, category_type='Expense')
    return render(request, 'expense_update.html', {'expense': expense, 'categories': categories})


@login_required
def expense_delete(request, id):
    expense = get_object_or_404(Expense, user=request.user, id=id)
    expense.delete()
    messages.success(request, "Expense deleted successfully.")
    return redirect('expenses')


# Incomes
@login_required
def incomes(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'incomes.html', {'incomes': incomes})


@login_required
def income_add(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')  # Default to empty string if not provided
        income_date = request.POST.get('date', date.today())  # Default to today if not provided
        if not category_id:
            messages.error(request, "Please select a category.")
            return redirect('income_add')
        try:
            category = Category.objects.get(id=category_id, user=request.user, category_type='Income')
        except Category.DoesNotExist:
            messages.error(request, "Please select a valid income category.")
            return redirect('income_add')
        Income.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description,
            date=income_date
        )
        messages.success(request, "Income added successfully!")
        return redirect('incomes')
    categories = Category.objects.filter(user=request.user, category_type='Income')
    return render(request, 'income_add.html', {'categories': categories})



@login_required
def income_update(request, id):
    income = get_object_or_404(Income, user=request.user, id=id)
    if request.method == "POST":
        income.amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        income.description = request.POST.get('description')
        income.date = request.POST.get('date')
        income.category = get_object_or_404(Category, id=category_id, user=request.user, category_type='Income')
        income.save()
        messages.success(request, "Income updated successfully.")
        return redirect('incomes')
    categories = Category.objects.filter(user=request.user, category_type='Income')
    return render(request, 'income_update.html', {'income': income, 'categories': categories})


@login_required
def income_delete(request, id):
    income = get_object_or_404(Income, user=request.user, id=id)
    income.delete()
    messages.success(request, "Income deleted successfully.")
    return redirect('incomes')


# Budgets
@login_required
def budgets_view(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'budgets_view.html', {'budgets': budgets})


@login_required
def budget_add_view(request):
    if request.method == "POST":
        category_id = request.POST.get('category')
        amount_limit = request.POST.get('amount_limit')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        category = get_object_or_404(Category, id=category_id, user=request.user)
        Budget.objects.create(user=request.user, category=category, amount_limit=amount_limit, start_date=start_date, end_date=end_date)
        messages.success(request, "Budget added successfully.")
        return redirect('budgets')
    categories = Category.objects.filter(user=request.user)
    return render(request, 'budget_add_view.html', {'categories': categories})


@login_required
def budget_update_view(request, id):
    budget = get_object_or_404(Budget, user=request.user, id=id)
    if request.method == "POST":
        budget.amount_limit = request.POST.get('amount_limit')
        category_id = request.POST.get('category')
        budget.start_date = request.POST.get('start_date')
        budget.end_date = request.POST.get('end_date')
        budget.category = get_object_or_404(Category, id=category_id, user=request.user)
        budget.save()
        messages.success(request, "Budget updated successfully.")
        return redirect('budgets')
    categories = Category.objects.filter(user=request.user)
    return render(request, 'budget_update_view.html', {'budget': budget, 'categories': categories})


@login_required
def budget_delete_view(request, id):
    budget = get_object_or_404(Budget, user=request.user, id=id)
    budget.delete()
    messages.success(request, "Budget deleted successfully.")
    return redirect('budgets')


# EMIs
@login_required
def emi_view(request):
    emis = EMI.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'emi_view.html', {'emis': emis})


@login_required
def emi_add_view(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        frequency = request.POST.get('frequency')
        description = request.POST.get('description')
        next_payment_date = request.POST.get('next_payment_date')
        EMI.objects.create(user=request.user, amount=amount, start_date=start_date, end_date=end_date, frequency=frequency, description=description, next_payment_date=next_payment_date)
        messages.success(request, "EMI added successfully.")
        return redirect('emi_view')
    return render(request, 'emi_add_view.html')


@login_required
def emi_update_view(request, id):
    emi = get_object_or_404(EMI, user=request.user, id=id)
    if request.method == "POST":
        emi.amount = request.POST.get('amount')
        emi.start_date = request.POST.get('start_date')
        emi.end_date = request.POST.get('end_date')
        emi.frequency = request.POST.get('frequency')
        emi.description = request.POST.get('description')
        emi.next_payment_date = request.POST.get('next_payment_date')
        emi.save()
        messages.success(request, "EMI updated successfully.")
        return redirect('emi_view')
    return render(request, 'emi_update_view.html', {'emi': emi})


@login_required
def emi_delete_view(request, id):
    emi = get_object_or_404(EMI, user=request.user, id=id)
    emi.delete()
    messages.success(request, "EMI deleted successfully.")
    return redirect('emi_view')



@login_required
def category_view(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, 'category_view.html', {'categories': categories})


@login_required
def category_add_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category_type = request.POST.get('category_type')  
        Category.objects.create(user=request.user, name=name, category_type=category_type)
        messages.success(request, "Category added successfully.")
        return redirect('category_view')
    return render(request, 'category_add_view.html')

@login_required
def category_update_view(request, id):
    category = get_object_or_404(Category, user=request.user, id=id)
    if request.method == "POST":
        category.name = request.POST.get('name')
        category.category_type = request.POST.get('category_type')
        category.save()
        messages.success(request, "Category updated successfully.")
        return redirect('category_view')
    return render(request, 'category_update_view.html', {'category': category})


@login_required
def category_delete_view(request, id):
    category = get_object_or_404(Category, user=request.user, id=id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('category_view')



@login_required
def dashboard_view(request):
    # Total income (Coalesce ensures a fallback to 0)
    total_income = Income.objects.filter(user=request.user).aggregate(
        total=ExpressionWrapper(
            Coalesce(Sum('amount'), 0),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )['total']

    # Total expenses (Coalesce ensures a fallback to 0)
    total_expenses = Expense.objects.filter(user=request.user).aggregate(
        total=ExpressionWrapper(
            Coalesce(Sum('amount'), 0),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )['total']

    # Calculate the balance
    balance = total_income - total_expenses

    # Budget summary: Calculate `spent` by summing expenses linked by the same category
    budget_summary = Budget.objects.filter(user=request.user).annotate(
        spent=ExpressionWrapper(
            Coalesce(
                Sum(
                    'category__expenses__amount',
                    filter=Q(category__expenses__date__range=[F('start_date'), F('end_date')])
                ),
                0
            ),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

@login_required
def budget_setting_view(request):
    if request.method == "POST":
        budget_limit = request.POST.get('budget-limit')
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id, user=request.user)
        Budget.objects.create(user=request.user, category=category, amount_limit=budget_limit)
        messages.success(request, "Budget setting added successfully.")
        return redirect('budgets')
    categories = Category.objects.filter(user=request.user)
    return render(request, 'budget_setting.html', {'categories': categories}
# budget report

def budget_report(request):
    categories = BudgetCategory.objects.all()
    return render(request, 'budget/report.html', {'categories': categories})
    # EMI summary
    emi_summary = EMI.objects.filter(user=request.user)

    # Recent expenses and incomes
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:4]
    recent_incomes = Income.objects.filter(user=request.user).order_by('-date')[:4]

    # Data for charts or statistics
    chart_data = {
        'total_income': total_income,
        'total_expenses': total_expenses,
    }

    return render(request, 'dashboard_view.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,  # Pass the balance to the template
        'budget_summary': budget_summary,
        'emi_summary': emi_summary,
        'recent_expenses': recent_expenses,
        'recent_incomes': recent_incomes,
        'chart_data': chart_data,
    })
