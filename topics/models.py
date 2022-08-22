from django.db import models


class Topic(models.Model):
    code = models.CharField(max_length=10)
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.code
