from django.db import models

# Create your models here.


class User(models.Model):
    lastname = models.CharField(max_length=60, null=True)
    lastname = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        User,  on_delete=models.CASCADE, related_name='posts', null=False)
