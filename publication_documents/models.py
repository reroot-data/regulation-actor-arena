from django.db import models


class Link(models.Model):
    link = models.URLField()


class AttachmentType(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Attachment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    reference = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    filename = models.CharField(max_length=200)
    document_id = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    is_original = models.BooleanField()
    date = models.DateTimeField()
    language = models.CharField(max_length=5)
    size = models.BigIntegerField()
    pages = models.IntegerField()

    type = models.ForeignKey(AttachmentType, on_delete=models.CASCADE)
    work_type = models.ForeignKey("initiatives.Type", on_delete=models.CASCADE)

    category = models.ForeignKey("categories.Category", on_delete=models.CASCADE)
    index = models.CharField(max_length=100)
    work_group = models.ForeignKey("committees.WorkGroup", on_delete=models.CASCADE)

    take_the_original = models.BooleanField()
    published = models.BooleanField()
    ers_file_name = models.CharField(max_length=100)


class Publication(models.Model):
    id = models.BigIntegerField(primary_key=True)
    type = models.ForeignKey("initiatives.Type", on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    group_id = models.IntegerField()
    modified_date = models.DateTimeField()
    attachment = models.ForeignKey(
        Attachment, on_delete=models.CASCADE, null=True, blank=True
    )
    end_date = models.DateTimeField()
    stage = models.ForeignKey("initiatives.Stage", on_delete=models.CASCADE)
    decide_send_date = models.DateTimeField()
    published_date = models.DateTimeField()
    receiving_feedback_status = models.ForeignKey(
        "initiatives.Status",
        on_delete=models.CASCADE,
        related_name="receiving_feedback",
    )
    planned_start_date = models.DateTimeField(null=True, blank=True)
    translation_date = models.DateTimeField(null=True, blank=True)
    adoption_date = models.DateTimeField()
    is_current = models.BooleanField()
    target_groups = models.ManyToManyField("committees.TargetGroup")
    consultation_objective = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField()
    total_feedback = models.IntegerField()
    planned_end_date = models.DateTimeField(blank=True, null=True)
    planned_period = models.CharField(max_length=100)
    front_end_stage = models.ForeignKey(
        "initiatives.Stage",
        on_delete=models.CASCADE,
        related_name="publication_front_end",
    )
    useful_links = models.ManyToManyField(Link)
    feedback_period = models.IntegerField()
    author_name = models.CharField(max_length=100)
    author_surname = models.CharField(max_length=100)
    author_mail = models.CharField(max_length=100)
    author_phone_number = models.CharField(max_length=100)
    initiative_status = models.ForeignKey(
        "initiatives.Status", on_delete=models.CASCADE
    )
    survey_contact_mail = models.CharField(max_length=100, blank=True, null=True)
    is_complete = models.BooleanField()

    def __str__(self) -> str:
        return self.reference
