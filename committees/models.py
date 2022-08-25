from django.db import models


class UserType(models.Model):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=200)


class WorkGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)


class ExpertGroup(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=25, unique=True)


class Committee(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name
