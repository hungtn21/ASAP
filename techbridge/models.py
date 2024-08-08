from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_language = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
