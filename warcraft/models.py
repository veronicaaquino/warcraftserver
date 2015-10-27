from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    picture = models.ImageField(upload_to='images', blank=True)
    wins = models.PositiveIntegerField(default = 0)
    loss = models.PositiveIntegerField(default = 0)
    
    def __unicode__(self):
        return self.user.username
    
