from django.contrib import admin

# Register your models here.


from .models import Journal, Operation

admin.site.register(Journal)
admin.site.register(Operation)
