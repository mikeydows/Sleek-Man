from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.username