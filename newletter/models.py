from django.db import models

class Newsletter(models.Model):
    name = models.CharField(max_length=100)
    email = models.JSONField(unique=True)

    def __str__(self):
        return self.name