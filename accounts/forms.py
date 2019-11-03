from django import forms
from django.contrib.auth.models import User
from .models import Profile


class AccountCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cleaned_data['password2']


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'profile_picture')
