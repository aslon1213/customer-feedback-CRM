from uuid import UUID
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import jinja2
import pdfkit
import time

# import HTTPRESPONSE
from django.http import HttpResponse

# staff member required decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

# Create your views here.
from .models import ProductForOrder
from django.views.generic import ListView


# import forms
from .forms import CustomProductCreationForm, CustomProductCreationManagerForm


class ProductListView(ListView):
    model = ProductForOrder
    template_name = "product_for_order/orders_list.html"
    queryset = ProductForOrder.objects.all()
    context_object_name = "products"

    def get_queryset(self):
        return ProductForOrder.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.get_full_path())
        products = ProductForOrder.objects.all()
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                products = ProductForOrder.objects.all()
            else:
                products = ProductForOrder.objects.filter(
                    person_ordered_id=self.request.user.id
                )
            context["products"] = products

        context["num_products"] = products.count()
        return context


def auto_make_products(request):
    for i in range(100):
        product = ProductForOrder.objects.create(
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
                product = ProductForOrder.objects.create(
                    name=request.POST.get("name"),
                    description=request.POST.get("description"),
                    person_ordered_id=request.user.id,
                    is_customer=False,
                )
                product.save()
                messages.success(request, f"Order has been succesfully added")
            else:
                print("User is authenticated - not staff")
                product = ProductForOrder.objects.create(
                    name=request.POST.get("name"),
                    description=request.POST.get("description"),
                    person_ordered_id=request.user.id,
                    is_customer=True,
                )
                product.save()
                messages.success(request, f"Order has been succesfully added")

        else:
            print("User is not authenticated")
            product = ProductForOrder.objects.create(
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
    return render(request, "product_for_order/create_order.html", context)


@login_required(login_url="account_login")
def edit_product_order(request, pk):
    product = ProductForOrder.objects.get(pk=pk)
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
    return render(request, "product_for_order/create_order.html", context)


@login_required(login_url="login")
def delete_product_order(request, pk):
    products = ProductForOrder.objects.filter(person_ordered_id=pk)
    if request.user.is_staff:
        products = ProductForOrder.objects.all()
    if request.method == "POST":
        pks = request.POST.getlist("delete[]")
        # print(Product.objects.filter(id__in=pks))
        # for p in pks:
        #     print(Product.objects.get(pk=UUID(p)))
        products = ProductForOrder.objects.filter(id__in=pks)

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
    return render(request, "product_for_order/delete_orders.html", context)


@staff_member_required(login_url="main_page")
def change_status(request):
    products = ProductForOrder.objects.all()

    if request.method == "POST":
        print(request.POST)
        pks = request.POST.getlist("change")
        print(pks)
        products = ProductForOrder.objects.filter(id__in=pks)
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
    return render(request, "product_for_order/change_status.html", context)


def error_404(request, exception):
    return render(request, "404/404.html", {})


def main_view(request):
    return render(request, "main.html")


import django


def pdfmaker(request):
    # check for user authentication
    if not request.user.is_authenticated:
        return redirect("account_login")
    # check for user access
    products = []
    print(request.user.is_staff)
    if request.user.is_staff:
        products = ProductForOrder.objects.all()
    else:
        ProductForOrder.objects.filter(person_ordered_id=request.user.id)
    context = {
        "products": products,
    }

    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("/templates/order_to_pdf.html")

    html = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    options = {"enable-local-file-access": True}
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type="application/pdf")
    date = time.strftime("%d-%m-%Y")
    response["Content-Disposition"] = "attachment; filename=" + ".pdf"
    return django.http.response.HttpResponse(
        pdf, content_type="application/pdf", response=response
    )
