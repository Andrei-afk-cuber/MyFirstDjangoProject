from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Vacancy(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открыта"),
        ("closed", "Закрытая")
    ]

    text = models.CharField(max_length=2000)
    slug = models.SlugField(max_length=50)
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.slug