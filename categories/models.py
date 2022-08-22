from django.db import models


class BetterRegulationRequirement(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name
