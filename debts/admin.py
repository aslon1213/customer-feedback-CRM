from django.contrib import admin

# Register your models here.
from .models import Debt, MoneyChain, DebtTaker

admin.site.register(Debt)
admin.site.register(MoneyChain)
admin.site.register(DebtTaker)
