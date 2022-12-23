from uuid import UUID
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from .models import Product
from django.views.generic import ListView


# import forms
from .forms import CustomPostCreationForm


class ProductListView(ListView):
    model = Product
    template_name = "to_do.html"
    queryset = Product.objects.all()
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context["products"] = products
        context["num_products"] = products.count()
        messages.success(self.request, "Product list has been updated.")
        return context


def create_product_order(request):
    form = CustomPostCreationForm()
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
            else:
                print("User is authenticated - not staff")
                product = Product.objects.create(
                    name=request.POST.get("name"),
                    description=request.POST.get("description"),
                    person_ordered_id=request.user.id,
                    is_customer=True,
                )
                product.save()

        else:
            print("User is not authenticated")
            product = Product.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                person_ordered_id=None,
                is_customer=True,
            )
            product.save()

    context = {
        "form": form,
        "type": "Create",
    }
    return render(request, "product/create_order.html", context)


def edit_product_order(request, pk):
    product = Product.objects.get(pk=pk)
    form = CustomPostCreationForm(instance=product)
    if request.method == "POST":
        form = CustomPostCreationForm(request.POST, instance=product)
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
