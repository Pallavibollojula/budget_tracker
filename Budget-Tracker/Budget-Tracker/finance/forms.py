from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User, Category, Income, Expense ,EMI,Budget,Report
 

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "email", "phone"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["name", "email", "password", "phone", "is_active", "is_admin"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_type']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'description', 'category', 'date']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'is_fixed']

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True,
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': True,
        })
    )

class RegisterForm(UserCreationForm):
    """Form for user registration that inherits from UserCreationForm."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["name", "email", "phone", "password1", "password2"]




class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "amount", "date", "description", "is_fixed"]


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["amount_limit", "start_date", "end_date", "category"]


class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ["amount", "start_date", "end_date", "next_payment_date", "description", "frequency"]