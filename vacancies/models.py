from django.db import models

class Vacancy(models.Model):
    text = models.CharField(max_length=2000)

class User(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()