from django.apps import AppConfig


class SentimentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sentiments"

    def ready(self) -> None:
        from . import signals
