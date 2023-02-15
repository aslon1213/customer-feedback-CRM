from uuid import UUID
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# staff member required decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

# Create your views here.
from .models import Product
from django.views.generic import ListView


# import forms
from .forms import CustomProductCreationForm, CustomProductCreationManagerForm


class ProductListView(ListView):
    model = Product
    template_name = "product/orders_list.html"
    queryset = Product.objects.all()
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.get_full_path())
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                products = Product.objects.all()
            else:
                products = Product.objects.filter(
                    person_ordered_id=self.request.user.id
                )
            context["products"] = products

        context["num_products"] = products.count()
        return context


def auto_make_products(request):
    for i in range(100):
        product = Product.objects.create(
            name=f"Product {i}",
            description=f"Product {i} description",
        )
        product.save()
    return redirect("product-list")


def create_product_order(request):
    form = CustomProductCreationForm()
    print(request.method)
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.is_staff:
                print("User is authenticated - staff")
                product = Product.objects.create(
                    name=request.POST.get("name"),
                    description=request.POST.get("description"),
                    person_ordered_id=request.user.id,
                    is_customer=False,
                )
                product.save()
                messages.success(request, f"Order has been succesfully added")
            else:
                print("User is authenticated - not staff")
                product = Product.objects.create(
                    name=request.POST.get("name"),
                    description=request.POST.get("description"),
                    person_ordered_id=request.user.id,
                    is_customer=True,
                )
                product.save()
                messages.success(request, f"Order has been succesfully added")

        else:
            print("User is not authenticated")
            product = Product.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                person_ordered_id=None,
                is_customer=True,
            )
            product.save()
            messages.success(request, f"Order has been succesfully added")

    context = {
        "form": form,
        "type": "Create",
    }
    return render(request, "product/create_order.html", context)


@login_required(login_url="account_login")
def edit_product_order(request, pk):
    product = Product.objects.get(pk=pk)
    form = CustomProductCreationForm(instance=product)
    if request.user.is_staff:
        form = CustomProductCreationManagerForm(instance=product)
    if request.method == "POST":
        if request.user.is_staff:
            form = CustomProductCreationManagerForm(request.POST, instance=product)
        else:
            form = CustomProductCreationForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product-list")
    context = {
        "form": form,
        "type": "Edit",
    }
    return render(request, "product/create_order.html", context)


@login_required(login_url="login")
def delete_product_order(request, pk):
    products = Product.objects.filter(person_ordered_id=pk)
    if request.user.is_staff:
        products = Product.objects.all()
    if request.method == "POST":
        pks = request.POST.getlist("delete[]")
        # print(Product.objects.filter(id__in=pks))
        # for p in pks:
        #     print(Product.objects.get(pk=UUID(p)))
        products = Product.objects.filter(id__in=pks)

        for product in products:
            print("Product " + product.name + " has been deleted from database.")
            if product.person_ordered_id == request.user.id or request.user.is_staff:
                product.delete()
                messages.success(
                    request,
                    "Product " + product.name + " has been deleted from database.",
                )
            else:
                messages.error(request, "You are not authorized to delete this order.")
        # for product in products:
        #     print(product.id)
        # if request.method == "POST":
        #     pks = request.POST["delete[]"]
        #     for p in pks:
        #         print(type(p))
        #         product = Product.objects.get(pk=UUID(p))
        #         print(product)
        #         if product.person_ordered_id == request.user.id or request.user.is_staff:
        #             product.delete()
        #         else:
        #             messages.error(request, "You are not authorized to delete this order.")

        return redirect("product-list")
    context = {
        "products": products,
        "type": "Delete",
    }
    return render(request, "product/delete_orders.html", context)


@staff_member_required(login_url="main_page")
def change_status(request):
    products = Product.objects.all()

    if request.method == "POST":
        print(request.POST)
        pks = request.POST.getlist("change")
        print(pks)
        products = Product.objects.filter(id__in=pks)
        for product in products:
            product.in_stock = True
            product.number_in_stock += 1
            product.save()
            messages.success(
                request, f"Product {product.name} has been succesfully edited"
            )
        return redirect("product-list")
    context = {
        "products": products,
    }
    return render(request, "product/change_status.html", context)


def error_404(request, exception):
    return render(request, "404/404.html", {})


def main_view(request):
    return render(request, "main.html")
