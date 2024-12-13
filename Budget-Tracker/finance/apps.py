from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'
def ready(self):
        # Import and initialize budget-related functionality
        from .budget import initialize_budget_settings
        initialize_budget_settings()