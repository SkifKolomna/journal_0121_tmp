from django.apps import AppConfig

VERBOSE_APP_NAME = 'Комментарии'


class CommonsConfig(AppConfig):
    name = 'commons'
    verbose_name = VERBOSE_APP_NAME
