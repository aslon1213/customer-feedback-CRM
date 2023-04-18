from django.shortcuts import redirect, render

# iumpoirt messages
from django.contrib import messages
from .models import Product
from django.views.generic import ListView
from .forms import ProductCreationForm

# import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


@staff_member_required(login_url="login")
def create_product(request):
    form = ProductCreationForm()
    if request.method == "POST":
        form = ProductCreationForm(request.POST)
        # access the form data
        selling_price_wholesale = form.data["selling_price_whosale"]
        # if selling_price_wholesale == "":
        # update_price
        obj = form.save()
        if selling_price_wholesale == "":
            obj.update_wholesale_price()
            obj.save()
        messages.success(request, "Product created successfully")
        return redirect("product-list")
    context = {"form": form, "title": "Create Product"}
    return render(request, "product/create_product.html", context)


@staff_member_required(login_url="login")
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductCreationForm(instance=product)
    if request.method == "POST":
        form = ProductCreationForm(request.POST, instance=product)
        if form.is_valid():
            obj = form.save()
            selling_price_wholesale = form.data["selling_price_whosale"]
            if selling_price_wholesale == "":
                obj.update_wholesale_price()
                obj.save()
            messages.success(request, "Product updated successfully")
            return redirect("product-list")
    context = {
        "form": form,
        "product_id": pk,
    }
    return render(request, "product/edit_product.html", context)


@staff_member_required(login_url="login")
def delete_product(request, pk):
    object = Product.objects.get(id=pk)
    if request.method == "POST":
        object.delete()
        messages.success(request, "Product deleted successfully")
        return redirect("product-list")
    context = {"object": object}
    return render(request, "product/delete_product.html", context)


class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    queryset = Product.objects.all()
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context


def product_info(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        "product": product,
        "path": request.get_full_path(),
    }
    return render(request, "product/product_info_page.html", context)


def product_list(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "product/product_list.html", context)


# name = models.CharField(max_length=120)
#     bar_code = models.CharField(max_length=120, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)

#     #manufacturer info
#     manufacturer = models.CharField(max_length=120, blank=True, null=True)
#     manufactured_date = models.DateField(blank=True, null=True)
#     expiry_date = models.DateField(blank=True, null=True)
#     manufactured_place = models.CharField(max_length=120, blank=True, null=True)

#     #availability info
#     in_stock = models.BooleanField(default=False)
#     number_in_stock = models.IntegerField(default=0)

#     #price info
#     coming_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     selling_price_whosale = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     selling_price_retail = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


def auto_make_products(request):
    for i in range(50):
        product = Product.objects.create(
            name=f"Product {i}",
            description=f"Product {i} description",
            bar_code=f"Barcode {i}",
            manufacturer=f"Manufacturer {i}",
            manufactured_date="2021-01-01",
            expiry_date="2024-01-01",
            manufactured_place=f"Manufactured place {i}",
            in_stock=True,
            number_in_stock=100,
            coming_price=100,
            selling_price_whosale=110,
            selling_price_retail=130,
        )
        product.save()
    return redirect("product-list")
