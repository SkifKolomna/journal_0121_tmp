from django.apps import AppConfig

VERBOSE_APP_NAME = 'Заявки'


class TasksConfig(AppConfig):
    name = 'tasks'
    verbose_name = VERBOSE_APP_NAME
