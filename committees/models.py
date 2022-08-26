from django.db import models


class UserType(models.Model):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=200)
    include_in_sentiment_analysis = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.code


class WorkGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class ExpertGroup(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name
