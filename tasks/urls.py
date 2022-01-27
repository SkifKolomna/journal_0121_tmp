from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import remove_comment, TaskCreateView, CommentCreateView, TaskApiView, CommentDetailView, TaskDetailView, \
    TaskApiDetailView
from .views import edit_comment
from .views import add_comment
# from .views import (AddCommentView, UpdateCommentView, DeleteCommentView)
from . import views
# from .forms import TaskForm, StatusForm
from .forms import TaskForm

app_name = 'tasks'
verbose_name = '123'


urlpatterns = [
    path('journal/', views.index, name='index'),

    path('return_count_tel/', views.return_count_tel, name='return_count_tel'),
    path('return_tool/', views.return_tool, name='return_tool'),
    path('return_last_id/', views.return_last_id, name='return_last_id'),
    path('return_deadline/', views.return_deadline, name='return_deadline'),

    # path('', csrf_exempt(views.sort_list), name='form'),
    # url(r'^tasks/$', views.TaskListView.as_view(), name='tasks-list'),
    # url(r'^tasks/(?P<pk>\d+)$', views.TaskDetailView.as_view(), name='task-detail'),
    # path('search/', views.search, name='search'),
]

router = SimpleRouter()
router.register('api', views.TaskView)
urlpatterns += router.urls
urlpatterns += [
    path('task/create/', TaskCreateView.as_view(), name='api_task_create'),
    path('task/view/', TaskApiView.as_view(), name='api_task_view'),
    path('comment/create/', CommentCreateView.as_view(), name='api_comment_create'),
    path('comment/detail/<int:pk>/', CommentDetailView.as_view(), name='api_comment_detail'),
    path('task/detail/<int:pk>/', TaskApiDetailView.as_view(), name='api_task_detail'),
]

# Add URLConf to create, update, and delete tasks
urlpatterns += [
    path('', views.TaskListView.as_view(), name='tasks-list'),
    path('<int:pk>/view/', views.TaskDetailView.as_view(), name='task-detail'),
    path('create/', views.TaskCreate.as_view(), name='task_create'),
    # path('add_status/<int:pk>', views.StatusCreate.as_view(form_class=StatusForm), name='add_status'),
    path('<int:pk>/update/', views.TaskUpdate.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDelete.as_view(), name='task_delete'),

    path('<int:pk>/print_alarm_task/', views.print_alarm_task, name='print_alarm_task'),

    # path('select2/', include('django_select2.urls', namespace='django_select2')),
    # path('api-auth/', include('rest_framework.urls')),
    # path('api/v1/', include('tasks.urls')),
]
urlpatterns += [
    path('comment/add/', add_comment, name="add_comment"),
    path('comment/<int:pk>/edit/', edit_comment, name="edit_comment"),
    path('comment/remove/', remove_comment, name="remove_comment"),
    path('edit_comment_first/', views.clone_first_comment_all, name='edit_comment_first'),
]
