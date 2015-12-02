from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from simple_email_confirmation import SimpleEmailConfirmationUserMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out

# Create your models here.

'''class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    picture = models.ImageField(upload_to="images")
    REQUIRED_FIELDS = ('user', 'email',)
    
    def __unicode__(self):
        return self.user.usernam'''

class LoggedUser(models.Model):
    user = models.ForeignKey('User')
    web = models.BooleanField(default=False)
    internal = models.BooleanField(default=False)

    def __unicode__(self):
        return self

    def login_user(sender, request, user, **kwargs):
        try:
            e = LoggedUser.objects.get(user=user)
            if user.login_web is True and e.web is False:
                e.web=user.login_web
                e.save()
            
            elif user.login_internal is True and e.internal is False:
                e.internal=user.login_internal
                e.save()
       
        except LoggedUser.DoesNotExist:
            LoggedUser(user=user, web=user.login_web, internal=user.login_internal).save()

    def logout_user(sender, request, user, **kwargs):
        try:
            e = LoggedUser.objects.get(user=user)
            if user.login_web is False and user.login_internal is True:
                e.web=user.login_web
                e.save()
            elif user.login_internal is False and user.login_web is True:
                e.internal=user.login_internal
                e.save()
            else :
                e.delete()
        except LoggedUser.DoesNotExist:
            pass

    user_logged_in.connect(login_user)
    user_logged_out.connect(logout_user)



class CustomUserManager(BaseUserManager):

    def create_user(self, userName, password=None, **extra_fields):
        userName = userName
        user = self.model(userName=userName, is_staff=False, is_active=True, is_superuser=False, is_admin = False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userName, password, **extra_fields):
        userName = userName
        user = self.model(userName=userName, is_staff=False, is_active=True, is_superuser=True, is_admin = True)
        user.set_password(password)
        user.save(using=self._db)
        return user
        


        
class User(SimpleEmailConfirmationUserMixin, AbstractBaseUser):
        posts = models.IntegerField(default=0)
        wins = models.PositiveIntegerField(default = 0)
        losses = models.PositiveIntegerField(default = 0)
        rating = models.FloatField(default = 1000)
        ranking = models.PositiveIntegerField(default = 1)
        userName = models.CharField(max_length=31, unique = True)
        picture =models.ImageField(upload_to="images")
        firstName = models.CharField(max_length=31)
        lastName = models.CharField(max_length=31)
        email = models.EmailField('email address')
        is_active = models.BooleanField(default = False)
        is_admin = models.BooleanField(default = False)
        is_online = models.BooleanField(default = False)
        login_internal = models.BooleanField(default = False)
        login_web = models.BooleanField(default = False)
        USERNAME_FIELD = 'userName'
        REQUIRED_FIELDS = []
        emailEvery= models.IntegerField(default = 0)
        has_messages = models.BooleanField(default = False)
        
        objects = CustomUserManager()

        def __unicode__(self):
            return self.userName
        
        @property
        def is_superuser(self):
            return self.is_admin

        @property
        def is_staff(self):
            return self.is_admin

        def has_perm(self, perm, obj=None):
            return self.is_admin

        def has_module_perms(self, app_label):
            return self.is_admin
        
        def get_short_name(self):
            return self.userName
            
        def get_email(self):
            return self.email
        
        def get_wins(self):
            return self.wins

        def get_losses(self):
            return self.losses

        def get_rating(self):
            return self.rating
            
        def beats(self, losingPlayer, players):
          if players == 2:
              k = 10 #The K value is an arbitrary value we choose based on how much we want
          if players > 2:
              k = 10*(players/2)
              #a player's score to increase/decrease after a match
              Ea = 1 / (1 + 10** ((self.rating - losingPlayer.rating) / 400))
              Eb = 1 / (1 + 10** ((losingPlayer.rating - self.rating) / 400))
              self.wins = self.wins + 1
              self.rating = math.trunc(self.rating + k * (1 - Ea))
              self.save()
              losingPlayer.losses = losingPlayer.losses + 1
              losingPlayer.rating = math.trunc(losingPlayer.rating + k * (0 - Eb))
              losingPlayer.save()

        def get_ranking(self):
            return self.ranking


