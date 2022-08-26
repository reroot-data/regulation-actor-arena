from committees.models import UserType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from google.api_core.exceptions import InvalidArgument
from google.cloud import translate_v3 as translate
from google.oauth2 import service_account
from google_trans_new import google_translator
from publication_documents.models import Publication
from sentiments.models import Sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .models import Feedback


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

    # SCOPES = [
    #     "https://www.googleapis.com/auth/cloud-translation",
    # ]
    # creds = service_account.Credentials.from_service_account_file(
    #     "credentials.json", scopes=SCOPES
    # )
    # TRANSLATE = translate.TranslationServiceClient(credentials=creds)
    # detect_language = TRANSLATE.detect_language(
    #     parent="projects/have-your-ai", content=instance.feedback
    # )

    # if detect_language == "en":
    #     # do not run when text is already in english
    #     # just take over original text
    #     instance.feedback_en = instance.feedback
    #     return

    return
    translator = google_translator()
    translate_text = translator.translate(instance.feedback, lang_tgt="en")
    instance.feedback_en = translate_text

    # try:

    # chunk_size = 1000
    # text = instance.feedback
    # response = TRANSLATE.translate_text(
    #     request={
    #         "parent": "projects/have-your-ai",
    #         "target_language_code": "en",
    #         "contents": [
    #             text[i : i + chunk_size] for i in range(0, len(text), chunk_size)
    #         ],
    #     }
    # )
    # instance.feedback_en = "".join(
    #     [i.translated_text for i in response.translations]
    # )
    # except InvalidArgument as e:
    #     return
    return


@receiver(post_save, sender=Feedback)
def feedback_add_sentiment(sender, instance, *args, **kwargs):

    if not instance.feedback_en:
        return

    if instance.user_type:
        if not instance.user_type.include_in_sentiment_analysis:
            return

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(instance.feedback_en)

    if sentiment_dict:
        sentiment, created = Sentiment.objects.update_or_create(
            feedback=instance,
            defaults={
                "positive": sentiment_dict["pos"],
                "neutral": sentiment_dict["neu"],
                "negative": sentiment_dict["neg"],
                "compound": sentiment_dict["compound"],
            },
        )

        # Update publication sentiment plot
        instance.publication_object.save()
