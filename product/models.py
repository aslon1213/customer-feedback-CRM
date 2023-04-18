from django.db import models
from uuid import uuid4

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=120)
    bar_code = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # manufacturer info
    manufacturer = models.CharField(max_length=120, blank=True, null=True)
    manufactured_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    manufactured_place = models.CharField(max_length=120, blank=True, null=True)

    # availability info
    in_stock = models.BooleanField(default=False)
    number_in_stock = models.IntegerField(default=0)

    # price info
    coming_price = models.FloatField(blank=True, null=True)
    selling_price_whosale = models.FloatField(blank=True, null=True)
    selling_price_retail = models.FloatField(blank=True, null=True)

    # id and created time
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def update_wholesale_price(self):
        if self.coming_price != None:
            self.selling_price_whosale = self.coming_price * 1.1
        else:
            self.selling_price_whosale = 0

    def get_absolute_url(self):
        return f"/products/{self.id}"

    def __str__(self):
        return self.name
