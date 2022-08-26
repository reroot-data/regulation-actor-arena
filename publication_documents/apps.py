from django.apps import AppConfig


class PublicationDocumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "publication_documents"

    def ready(self) -> None:
        from . import signals
