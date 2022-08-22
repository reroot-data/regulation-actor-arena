from django.db import models


class WorkGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)


class ExpertGroup(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name


class TargetGroup(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=25, unique=True)


class Committee(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name
