from django.apps import AppConfig


class InheritingClassAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inheriting_class_app'
