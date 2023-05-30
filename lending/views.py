from django.shortcuts import render, redirect


# models
from .models import LendingProduct, LendingHistory, Borrower

# forms
from .forms import CreateLendingProductForm, CreateLending, CreateBorrower


def dashboard(request):
    lendingProducts = LendingProduct.objects.all()
    context = {
        "lendingProducts": lendingProducts,
    }
    return render(request, "lending/dashboard.html")


def create_lending(request):
    form = CreateLending()
    if request.method == "POST":
        form = CreateLending(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_lending")

    return render(request, "lending/create_lending.html")


def create_LendingProduct(request):
    return render(request, "lending/create_LendingProduct.html")


def show_products(request):
    return render(request, "lending/show_products.html")


def show_lending_history(request):
    return render(request, "lending/show_lending_history.html")


def show_borrowers(request):
    return render(request, "lending/show_borrowers.html")


def show_borrower_details(request):
    return render(request, "lending/show_borrower_details.html")
