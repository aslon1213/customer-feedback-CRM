from django.urls import path
from .views import (
    main_view,
    new_journal,
    view_journal,
    new_operation,
    delete_operation,
    edit_operation,
    close_current,
)

urlpatterns = [
    path("", main_view, name="journal_main"),
    path("new", new_journal, name="new_journal"),
    path("view", view_journal, name="view_journal"),
    path("operations/new", new_operation, name="new_operation"),
    path("operations/delete", delete_operation, name="delete_operation"),
    path("operations/update", edit_operation, name="edit_operation"),
    path("close_current", close_current, name="close_current"),
]
