from django.urls import path
from .views import (
    create_lending,
    create_lending_history,
)

urlpatterns = [
    path("", create_lending, name="create_lending"),
    path("lend/", create_lending, name="create_lending"),
    # path("create_lending_history/", create_lending_history, name="create_lending_history"),
]
