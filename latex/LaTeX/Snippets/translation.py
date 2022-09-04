from django.db.models.signals import pre_save
from django.dispatch import receiver
from feedbacks.models import Feedback
from google.api_core.exceptions import InvalidArgument
from google.cloud import translate_v3 as translate
from google.oauth2 import service_account


@receiver(pre_save, sender=Feedback)
def Feedback_add_translation(sender, instance, **kwargs):
    if not instance.feedback:
        # only run when there is text
        return

    saved_instance = Feedback.objects.filter(id=instance.id).first()
    if saved_instance:
        if saved_instance.feedback == instance.feedback:
            # do not run when text is left unchanged
            return

    SCOPES = [
        "https://www.googleapis.com/auth/cloud-translation",
    ]
    creds = service_account.Credentials.from_service_account_file(
        "credentials.json", scopes=SCOPES
    )
    TRANSLATE = translate.TranslationServiceClient(credentials=creds)
    detect_language = TRANSLATE.detect_language(
        parent="projects/have-your-ai", content=instance.feedback
    )

    if detect_language == "en":
        # do not run when text is already in english
        # just take over original text
        instance.feedback_en = instance.feedback
        return

    try:
        chunk_size = 1000
        text = instance.feedback
        response = TRANSLATE.translate_text(
            request={
                "parent": "projects/have-your-ai",
                "target_language_code": "en",
                "contents": [
                    text[i : i + chunk_size] for i in range(0, len(text), chunk_size)
                ],
            }
        )
        instance.feedback_en = "".join(
            [i.translated_text for i in response.translations]
        )
    except InvalidArgument as e:
        return
    return
