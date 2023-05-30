from django.urls import path
from .views import (
    create_debt,
    list_debts,
    transaction_minus,
    transaction_plus,
    delete_debt,
    get_debt_history,
    debt_taker_page,
)


urlpatterns = [
    path("", list_debts, name="list-debts"),
    path("all/", list_debts, name="list-debts"),
    path("debt/<str:pk>", get_debt_history, name="debt-history"),
    path("create/", create_debt, name="create-debt"),
    path("transaction/plus/<str:pk>", transaction_plus, name="transaction-plus"),
    path("transaction/minus/<str:pk>", transaction_minus, name="transaction-minus"),
    path("delete/<str:pk>", delete_debt, name="delete-debt"),
    # debtaker
    path("debtaker/<str:pk>/", debt_taker_page, name="debt-taker-page"),
]
