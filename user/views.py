from django.shortcuts import render

# import listview from django
from django.views.generic import ListView

# Create your views here.
from .models import User

# Create your views here.
class CustomerListView(ListView):
    # model = User
    template_name = "users_list.html"
    # queryset = User.objects.all()
    # context_object_name = "users"

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customers"] = User.objects.all()
        return context


# class Create
