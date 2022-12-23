from django.db import models

# import user model
from django.contrib.auth.models import AbstractUser

# import permission model
from uuid import uuid4

# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField("auth.Group", related_name="Defaultuser")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="Deaultuser"
    )

    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    # id and created time
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    # if is staff = True then they are a manager
    # if is staff = False then they are a customer

    class Meta:
        permissions = [
            ("can_view_orders_made_by_customer", "Can view orders made by customer"),
            ("can_add_orders", "Can add orders"),
            ("can_edit_order_made_by_customer", "Can edit order made by customer"),
            ("can_delete_order_made_by_customer", "Can delete order made by customer"),
            ("has_access_to_all_orders", "Can access all orders"),
            ("can_edit_all_orders", "Can edit orders"),
            ("can_delete_all_orders", "Can delete orders"),
        ]
        app_label = "user"

    def __str__(self):
        return self.username

    pass


# class has_access_to_all_orders(Permission):
#     pass
