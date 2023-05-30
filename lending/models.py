import uuid
from django.db import models
from product.models import Product

# Create your models here.


# class LendingProduct(models.Model):
#     product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
#     price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
#     price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
#     price_per_year = models.DecimalField(max_digits=10, decimal_places=2)

#     ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product.name} - {self.product.category}"

#     def set_up_prices(self):
#         p = Product.objects.get(ID=self.product.ID)
#         self.price_per_day = p.selling_price_retail * 2 / 60
#         self.price_per_month = p.selling_price_retail * 3 / 60
#         self.price_per_year = p.selling_price_retail / 2


# class LendingHistory(models.Model):
#     product = models.ManyToManyField("LendingProduct", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     number_of_lendings = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.product.product.name} - {self.created_at}"


# class Borrower(models.Model):
#     LendingHistory = models.ManyToManyField("LendingHistory", on_delete=models.CASCADE)
#     ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
#     surname = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)
#     address = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=100)
#     passport_number = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.name} {self.surname}"
