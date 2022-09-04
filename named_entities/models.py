from django.db import models


class NamedEntity(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    entity_type = models.CharField(max_length=100, null=True, blank=True)
    salience = models.DecimalField(max_digits=3, decimal_places=2)


class NamedEntityMetaData(models.Model):
    named_entity = models.ForeignKey(NamedEntity, on_delete=models.CASCADE)
    key = models.CharField(max_length=500)
    value = models.TextField(null=True, blank=True)


class NamedEntityMentions(models.Model):
    named_entity = models.ForeignKey(NamedEntity, on_delete=models.CASCADE)
    key = models.CharField(max_length=500)
    value = models.TextField(null=True, blank=True)
