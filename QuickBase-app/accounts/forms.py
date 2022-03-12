from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import APIKey

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email","name", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class modifyAccount():
    class Meta:
        model = APIKey
        fields = ("username","email","password3","password1", "password2","APIKey","APISecret")

    def save(self, commit=True):
        APIKey = super(modifyAccount, self).save(commit=False)
        if commit:
            APIKey.save()
        return APIKey

class validation():
    class Meta:
        fields = ("code")
