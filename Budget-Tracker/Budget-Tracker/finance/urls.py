 
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),  # Home page
   path("dashboard/", views.dashboard_view, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("expenses/", views.expenses, name="expenses"),
    path("expenses/add/", views.expense_add, name="expense_add"),
    path("expenses/<int:id>/update/", views.expense_update, name="expense_update"),
    path("expenses/<int:id>/delete/", views.expense_delete, name="expense_delete"),
    path("incomes/", views.incomes, name="incomes"),
    path("incomes/add/", views.income_add, name="income_add"),
    path("incomes/<int:id>/update/", views.income_update, name="income_update"),
    path("incomes/<int:id>/delete/", views.income_delete, name="income_delete"),
    path("budgets/", views.budgets_view, name="budgets"),
    path("budgets/add/", views.budget_add_view, name="budget_add"),
    path("budgets/<int:id>/update/", views.budget_update_view, name="budget_update"),
    path("budgets/<int:id>/delete/", views.budget_delete_view, name="budget_delete"),
    path("emis/", views.emi_view, name="emi_view"),
    path("emis/add/", views.emi_add_view, name="emi_add"),
    path("emis/<int:id>/update/", views.emi_update_view, name="emi_update"),
    path("emis/<int:id>/delete/", views.emi_delete_view, name="emi_delete"),
    path("categories/", views.category_view, name="category_view"),  
    path("categories/add/", views.category_add_view, name="category_add"),
    path("categories/<int:id>/update/", views.category_update_view, name="category_update"),
    path("categories/<int:id>/delete/", views.category_delete_view, name="category_delete"),
]

# from django.conf.urls.static import static

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 