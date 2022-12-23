from django.db import models
from uuid import uuid4

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=120)
    person_ordered_id = models.CharField(max_length=120, blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    in_stock = models.BooleanField(default=False)
    number_in_stock = models.IntegerField(default=0)

    # id and created time
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f"/products/{self.id}"

    def __str__(self):
        return self.name
