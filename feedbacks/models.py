from django.db import models


class FeedbackAttachment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    size = models.BigIntegerField()
    documentId = models.CharField(max_length=1000)
    ers_file_name = models.CharField(max_length=1000)
    pages = models.IntegerField(null=True, blank=True)
    pdf_size = models.BigIntegerField()
    is_rendered = models.BooleanField()
    is_externalized_in_hrs = models.BooleanField()


class Feedback(models.Model):
    id = models.BigIntegerField(primary_key=True)
    language = models.CharField(max_length=10)
    country = models.ForeignKey(
        "countries.Country", on_delete=models.CASCADE, null=True, blank=True
    )
    organization = models.CharField(max_length=500, null=True, blank=True)
    surname = models.CharField(max_length=500, blank=True, null=True)
    status = models.ForeignKey("initiatives.Status", on_delete=models.CASCADE)
    feedback = models.CharField(max_length=10000, null=True, blank=True)
    feedback_en = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=500, null=True, blank=True)
    attachments = models.ManyToManyField(FeedbackAttachment, blank=True)
    date_feedback = models.DateTimeField()
    publication = models.CharField(max_length=100)
    publication_object = models.ForeignKey(
        "publication_documents.Publication", on_delete=models.CASCADE
    )
    user_type = models.ForeignKey(
        "committees.UserType", on_delete=models.CASCADE, null=True, blank=True
    )
    company_size = models.CharField(max_length=500, null=True, blank=True)
    tr_number = models.CharField(max_length=100, null=True, blank=True)
    is_my_feedback = models.BooleanField()
    reference_initiative = models.CharField(max_length=200)
    history_event_occurs = models.BooleanField()
    publication_id = models.BigIntegerField()
    publication_status = models.CharField(max_length=100)
