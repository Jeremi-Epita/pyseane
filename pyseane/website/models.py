from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # add any additional fields you need
    pass

class Pyseane_User(models.Model):
    username = models.CharField(max_length=80)
    mdp = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    
