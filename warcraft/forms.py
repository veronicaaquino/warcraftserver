from django import forms
from django.contrib.auth.models import User
from warcraft.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(max_length=75, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
  
    class Meta:
        model = UserProfile
        fields = ('picture',)
        
class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(max_length=75, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')