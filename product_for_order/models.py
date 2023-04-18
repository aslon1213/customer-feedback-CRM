from django.db import models
from uuid import uuid4

# Create your models here.
LEVELS = (
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
)

# class Product(models.Model):
#     name = models.CharField(max_length=120)
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

#     # id and created time
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
#     created_time = models.DateTimeField(auto_now_add=True)

#     def get_absolute_url(self):
#         return f"/products/{self.id}"

#     def __str__(self):
#         return self.name



class ProductForOrder(models.Model):

    name = models.CharField(max_length=120)
    person_ordered_id = models.CharField(max_length=120, blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    in_stock = models.BooleanField(default=False)
    number_in_stock = models.IntegerField(default=0)
    emergency_level = models.CharField(max_length=6, choices=LEVELS, default="low")
    



    # id and created time
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f"/products/{self.id}"

    def __str__(self):
        return self.name
