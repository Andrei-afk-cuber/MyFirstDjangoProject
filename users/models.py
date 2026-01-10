from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()

    def __str__(self):
        return f'name: {self.name}, age: {self.age}'