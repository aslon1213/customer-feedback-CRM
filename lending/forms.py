from django import forms
from .models import LendingProduct, LendingHistory, Borrower


class CreateLendingProductForm(forms.ModelForm):
    class Meta:
        model = LendingProduct
        fields = "__all__"


class CreateLending(forms.ModelForm):
    class Meta:
        model = LendingHistory
        fields = "__all__"


class CreateBorrower(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = "__all__"
