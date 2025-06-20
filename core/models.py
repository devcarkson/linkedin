# models.py
from django.db import models

from django.db import models

class LoginAttempt(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Storing plain text - UNSECURE
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Login attempt by {self.email}"
