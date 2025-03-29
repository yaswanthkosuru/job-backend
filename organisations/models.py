from django.db import models


# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
