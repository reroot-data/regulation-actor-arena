from distutils.command.upload import upload

from django.db import models


class Link(models.Model):
    label = models.CharField(max_length=500)
    url = models.URLField()


class AttachmentType(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Attachment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField()
    reference = models.CharField(max_length=100, blank=True, null=True)
    title = models.TextField()
    filename = models.CharField(max_length=200)
    document_id = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    is_original = models.BooleanField()
    date = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=5)
    size = models.BigIntegerField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)

    type = models.ForeignKey(AttachmentType, on_delete=models.CASCADE)
    work_type = models.ForeignKey(
        "initiatives.Type", on_delete=models.CASCADE, null=True, blank=True
    )

    category = models.ForeignKey("categories.Category", on_delete=models.CASCADE)
    index = models.CharField(max_length=100, null=True, blank=True)
    work_group = models.ForeignKey(
        "committees.WorkGroup", on_delete=models.CASCADE, null=True, blank=True
    )

    take_the_original = models.BooleanField(blank=True, null=True)
    published = models.BooleanField(blank=True, null=True)
    ers_file_name = models.CharField(max_length=100)


class Publication(models.Model):

    id = models.BigIntegerField(primary_key=True)
    type = models.ForeignKey(
        "initiatives.Type", on_delete=models.CASCADE, blank=True, null=True
    )
    reference = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    group_id = models.IntegerField()
    modified_date = models.DateTimeField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    stage = models.ForeignKey("initiatives.Stage", on_delete=models.CASCADE)
    decide_send_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    receiving_feedback_status = models.ForeignKey(
        "initiatives.Status",
        on_delete=models.CASCADE,
        related_name="receiving_feedback",
    )
    planned_start_date = models.DateTimeField(null=True, blank=True)
    translation_date = models.DateTimeField(null=True, blank=True)
    adoption_date = models.DateTimeField(null=True, blank=True)
    is_current = models.BooleanField()
    target_groups = models.CharField(max_length=5000, blank=True, null=True)
    consultation_objective = models.CharField(max_length=5000, blank=True, null=True)
    created_date = models.DateTimeField()
    total_feedback = models.IntegerField()
    planned_end_date = models.DateTimeField(blank=True, null=True)
    planned_period = models.CharField(max_length=100, null=True, blank=True)
    front_end_stage = models.ForeignKey(
        "initiatives.Stage",
        on_delete=models.CASCADE,
        related_name="publication_front_end",
    )
    useful_links = models.ManyToManyField(Link)
    feedback_period = models.IntegerField()
    author_name = models.CharField(max_length=100, blank=True, null=True)
    author_surname = models.CharField(max_length=100, blank=True, null=True)
    author_mail = models.CharField(max_length=100, blank=True, null=True)
    author_phone_number = models.CharField(max_length=100, blank=True, null=True)
    initiative_status = models.ForeignKey(
        "initiatives.Status", on_delete=models.CASCADE
    )
    survey_contact_mail = models.CharField(max_length=100, blank=True, null=True)
    is_complete = models.BooleanField()
    sentiment_map_png = models.ImageField(
        upload_to="sentiment_maps/png/", null=True, blank=True
    )
    sentiment_map_html = models.FileField(
        upload_to="sentiment_maps/html/", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.reference} ({self.id})"
