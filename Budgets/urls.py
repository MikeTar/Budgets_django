from django.urls import path

from .views import BudgetView, PPO_View

app_name = "budgets"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('budgets/', BudgetView.as_view()),
    path('ppo/', PPO_View.as_view()),
]