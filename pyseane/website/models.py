from django.db import models
class Pyseane_User(models.Model):
    username = models.CharField(max_length=80)
    mdp = models.CharField(max_length=80)
    email = models.CharField(max_length=80)