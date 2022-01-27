from django.apps import AppConfig

VERBOSE_APP_NAME = 'Журнал'


class TasksConfig(AppConfig):
    name = 'journal'
    verbose_name = VERBOSE_APP_NAME
