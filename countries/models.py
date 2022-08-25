from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.label
