from django.db.models.signals import post_save
from django.dispatch import receiver
from feedbacks.models import Feedback
from google.cloud import language_v1

from named_entities.models import NamedEntity, NamedEntityMentions, NamedEntityMetaData


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
