import code

from django.db import models


class LegalBasis(models.Model):
    document_legal = models.URLField()
    article = models.TextField()
    paragraph = models.CharField(max_length=8, blank=True, null=True)
    alinea = models.CharField(max_length=8, blank=True, null=True)
    point = models.CharField(max_length=8, blank=True, null=True)
    phrase = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self) -> str:
        return self.document_legal


class Stage(models.Model):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.code


class Type(models.Model):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.code


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Initiative(models.Model):
    id = models.BigIntegerField(primary_key=True)
    better_regulation_requirement = models.ManyToManyField(
        "categories.BetterRegulationRequirement"
    )
    committee = models.ForeignKey(
        "committees.Committee", on_delete=models.CASCADE, null=True, blank=True
    )
    created_date = models.DateTimeField()
    dg = models.CharField(max_length=10)
    dossier_summary = models.TextField(blank=True, null=True)
    expert_group = models.ForeignKey(
        "committees.ExpertGroup", on_delete=models.CASCADE, null=True, blank=True
    )
    foreseen_act_type = models.ForeignKey(
        Type, on_delete=models.CASCADE, null=True, blank=True
    )
    initiative_category = models.ManyToManyField("categories.Category")
    initiative_status = models.ForeignKey(
        Status, on_delete=models.CASCADE, null=True, blank=True
    )
    is_evaluation = models.BooleanField(null=True, blank=True)
    is_grouped_cfe = models.BooleanField(null=True, blank=True)
    is_major = models.BooleanField(null=True, blank=True)
    legal_basis = models.ManyToManyField(LegalBasis, blank=True)
    modified_date = models.DateTimeField()
    reference = models.CharField(max_length=100)
    unit = models.ForeignKey(
        "committees.Unit", on_delete=models.CASCADE, null=True, blank=True
    )
    order_date = models.DateTimeField()
    policy_areas = models.ManyToManyField("policy_areas.PolicyArea")
    publications = models.ManyToManyField(
        "publication_documents.Publication", blank=True
    )
    published_date = models.DateTimeField()
    receiving_feedback_status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="initiative_feedback_status",
    )
    short_title = models.CharField(max_length=500)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    topics = models.ManyToManyField("topics.Topic")

    def __str__(self) -> str:
        return self.reference
