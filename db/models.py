import sys
from main import User
try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


# Sample User model
class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    location = models.TextField()
    chat_id = models.PositiveBigIntegerField()
    def __str__(self):
        return self
