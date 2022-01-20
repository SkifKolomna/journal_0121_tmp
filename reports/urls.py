from django.urls import path

from . import views

urlpatterns = [
    path('export_report_reu/', views.export_report_reu, name='export_report_reu'),
    path('export_report_reu_all/', views.export_report_reu_all, name='export_report_reu_all'),
    path('export_report_tools/', views.export_report_tools, name='export_report_tools'),
    path('export_report_tools_all/', views.export_report_tools_all, name='export_report_tools_all'),
    path('export_report_ac/', views.export_report_ac, name='export_report_ac'),
    path('export_report_month/', views.export_report_month, name='export_report_month'),
    path('export_report_month_tek/', views.export_report_month_tek, name='export_report_month_tek'),
    path('export_report_all/', views.export_report_all, name='export_report_all'),
    path('edit_lift/', views.edit_lift, name='edit_lift'),
]