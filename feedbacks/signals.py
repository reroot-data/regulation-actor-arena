import re
from email.policy import default

from committees.models import UserType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from google.api_core.exceptions import InvalidArgument
from google.cloud import language_v1
from google.cloud import translate_v3 as translate
from google.oauth2 import service_account
from google_trans_new import google_translator
from named_entities.models import NamedEntity, NamedEntityMentions, NamedEntityMetaData
from nltk.stem import WordNetLemmatizer
from publication_documents.models import Publication
from sentiments.models import Sentiment
from spellchecker import SpellChecker
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


@receiver(pre_save, sender=Feedback)
def feedback_spell_check(sender, instance, *args, **kwargs):
    spell = SpellChecker()
    list_words = re.findall("[a-zA-Z]}", instance.feedback_en)
    misspelled = spell.unknown(list_words)
    for word in misspelled:
        instance.feedback_en.replace(word, spell.correction(word))


@receiver(pre_save, sender=Feedback)
def feedback_trim_whitespaces(sender, instance, *args, **kwargs):
    instance.feedback_en = re.sub(" +", " ", instance.feedback_en)


@receiver(pre_save, sender=Feedback)
def feedback_lemmatization(sender, instance, *args, **kwargs):
    lemmatizer = WordNetLemmatizer()
    text_list = re.findall("[a-zA-Z]}", instance.feedback_en)
    lemmatized = [lemmatizer.lemmatize(word) for word in text_list]
    instance.feedback_lemmatized = " ".join(lemmatized)


@receiver(post_save, sender=Feedback)
def feedback_add_named_entity(sender, instance, *args, **kwargs):

    client = language_v1.LanguageServiceClient()

    # settings
    type_ = language_v1.Document.Type.PLAIN_TEXT
    encoding_type = language_v1.EncodingType.UTF8
    language = "en"

    # content
    document = {
        "content": instance.feedback_lemmatized,
        "type_": type_,
        "language": language,
    }
    response = client.analyze_entities(
        request={"document": document, "encoding_type": encoding_type}
    )

    for entity in response.entities:
        entity = NamedEntity.objects.update_or_create(
            name=entity.name,
            defaults={
                "entity_type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            },
        )
        for metadata_name, metadata_value in entity.metadata.items():
            NamedEntityMetaData.objects.update_or_create(
                named_entity=instance,
                key=metadata_name,
                defaults={"value": metadata_value},
            )

        for mention in entity.mentions:
            NamedEntityMentions.objects.update_or_create(
                named_entity=instance,
                key=mention.text.content,
                defaults={"value": language_v1.EntityMention.Type(mention.type_).name},
            )
        instance.named_entities.add(entity)


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
