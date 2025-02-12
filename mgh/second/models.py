from django.db import models

# Create your models here.


class First(models.Model):
    name=models.CharField(max_length=50)