"""journal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView

app_name = 'journal'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('tasks.urls')),
    path('api/v1/base-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth_token/', include('djoser.urls.authtoken')),
]

# Используйте include() чтобы добавлять URL из каталога приложения
urlpatterns += [
    # path('', include('commons.urls', namespace="commons")),
    path('commons/', include('commons.urls')),
    # path('tasks/', include('tasks.urls')),
    path('tasks/', include('tasks.urls', namespace='tasks_task')),
    # path('tasks/', include('tasks.urls')),
    path('charts/', include('charts.urls')),
    path('reports/', include('reports.urls')),
    # path('messages_tasks/', include('messages_tasks.urls')),
]

# Добавьте URL соотношения, чтобы перенаправить запросы с корневового URL, на URL приложения
urlpatterns += [
    path('', RedirectView.as_view(url='/tasks/', permanent=True)),
]

# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# добаленно вручную
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('select2/', include('django_select2.urls')),

]
