"""customer_needs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# import products views
from product_for_order.views import (
    main_view,
    pdfmaker,
)

urlpatterns = [
    path("", main_view, name="main_page"),
    path("api/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("products_for_order/", include("product_for_order.urls")),
    path("users/", include("user.urls")),
    path("accounts/", include("allauth.urls")),
    path("products/", include("product.urls")),
    path("debts/", include("debts.urls")),
    path("journal/", include("workday_finance_management.urls")),
]


handler404 = "product_for_order.views.error_404"
