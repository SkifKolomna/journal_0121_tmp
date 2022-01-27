# from commons.views import (
#     add_comment, edit_comment, remove_comment
# )
from django.urls import path

# from .forms import TaskForm, StatusForm
VERBOSE_APP_NAME = 'Образовательные ресурсы'
app_name = 'commons'
verbose_name = VERBOSE_APP_NAME
# Add URLConf to create, update, and delete tasks
urlpatterns = [
    # path('comment/add/', add_comment, name="add_comment"),
    # path('comment/<int:pk>/edit/', edit_comment, name="edit_comment"),
    # path('comment/remove/', remove_comment, name="remove_comment"),
]
