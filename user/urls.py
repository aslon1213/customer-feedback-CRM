from django.urls import path
from .views import (
    CustomerListView,
)

urlpatterns = [path("", CustomerListView.as_view(), name="user-list")]
