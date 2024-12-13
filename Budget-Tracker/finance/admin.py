from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm
from .models import Category, Income, Expense, EMI, Budget, Alert, Report

# Retrieve the custom User model
User = get_user_model()

# Custom UserAdmin for the User model
class UserAdmin(BaseUserAdmin):
    # Forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # Fields to display in the admin interface
    list_display = ["name", "email", "phone", "is_admin"]
    list_filter = ["is_admin"]

    # Fields shown when viewing/editing a user
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal Info", {"fields": ["name", "phone"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    # Fields shown when creating a new user
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "phone", "password1", "password2"],
            },
        ),
    ]

    # Configuration for searching, ordering, and filters
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

# Register the custom User model and its admin
admin.site.register(User, UserAdmin)

# Unregister the default Group model since we're not using Django's default permissions
admin.site.unregister(Group)

# Register additional models in the admin
admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(EMI)
admin.site.register(Budget)
admin.site.register(Alert)
admin.site.register(Report)
