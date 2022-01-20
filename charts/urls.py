from django.urls import path

from . import views
from .forms import ChartForm

urlpatterns = [
    path('return_count_adr/', views.return_count_adr, name='return_count_adr'),
    path('return_adr_reu/', views.return_adr_reu, name='return_adr_reu'),

]

# Add URLConf to create, update, and delete tasks
urlpatterns += [
    path('', views.ChartListView.as_view(), name='chart-list'),
    path('create/', views.ChartCreate.as_view(form_class=ChartForm), name='chart_create'),
    path('<int:pk>', views.ChartDetailView.as_view(), name='chart-detail'),
    path('<int:pk>/update/', views.ChartUpdate.as_view(form_class=ChartForm), name='chart_update'),
    path('<int:pk>/delete/', views.ChartDelete.as_view(), name='chart_delete'),
]
