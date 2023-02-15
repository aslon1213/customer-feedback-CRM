from django.urls import path
from .views import (
    CustomerListView,
    create_user_automation,
    customer_profile,
)

urlpatterns = [
    path("", CustomerListView.as_view(), name="user-list"),
    path("customer_profile/<str:pk>/", customer_profile, name="customer-profile"),
    #
    # automation
    path("create_automation/", create_user_automation, name="create-automation"),
]
