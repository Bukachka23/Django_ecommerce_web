from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product


# Define a new form that inherits from UserCreationForm.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Define some metadata for the form.
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # Override the save method of the form.
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user