from django.shortcuts import render

# import listview from django
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# import Product model from another app
from product.models import Product

# Create your views here.
from .models import User

# Create your views here.
class CustomerListView(ListView):
    # model = User
    template_name = "users_list.html"
    # queryset = User.objects.all()
    # context_object_name = "users"

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customers"] = User.objects.all()
        return context


def create_user_automation(request):
    for i in range(50):
        user = User.objects.create(
            username=f"user{i}",
            email=f"user{i}@gmail.com",
            first_name=f"User {i}",
            last_name=f"User {i}",
            password="pbkdf2_sha256$390000$MuAXKlt3dInrNXAy56hCz7$fW2ImyHQEQIidz4+iqserTQJOyLbWmH5qbw1DLwtGHk=",
            is_staff=False,
        )
        user.save()
        user = User.objects.create(
            username=f"manager{i}",
            email=f"manager{i}@gmail.com",
            first_name=f"Manager {i}",
            last_name=f"Manager {i}",
            password="pbkdf2_sha256$390000$MuAXKlt3dInrNXAy56hCz7$fW2ImyHQEQIidz4+iqserTQJOyLbWmH5qbw1DLwtGHk=",
            is_staff=True,
        )
        user.save()

    return redirect("main_page")


@login_required(login_url="account_login")
def customer_profile(request, pk):

    customer = User.objects.get(id=pk)
    if customer.is_staff:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(person_ordered_id=pk)
    context = {
        "customer": customer,
        "products": products,
    }
    return render(request, "user/customer_profile.html", context)


# class Create
