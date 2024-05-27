from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from users.models import FacultyProfile, StudentProfile

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address ending with @iiit-bh.ac.in.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@iiit-bh.ac.in') or not email.startswith('b') or not email[1:7].isdigit():
            raise forms.ValidationError("Student email must start with 'b', followed by 6 digits, and end with '@iiit-bh.ac.in'")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.startswith('b') or not username[1:].isdigit() or len(username) != 7:
            raise forms.ValidationError("Username must start with 'b' followed by 6 digits.")
        return username

class FacultyRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address ending with @iiit-bh.ac.in.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        local_part = email.split('@')[0]
        if any(char.isdigit() for char in local_part):
            raise forms.ValidationError("Faculty email must not contain digits in the local part.")
        return email

class StudentAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.startswith('b') or not username[1:].isdigit() or len(username) != 7:
            raise forms.ValidationError("Username will start with 'b' followed by 6 digits.")
        return username

class FacultyAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if username.startswith('b') and username[1:7].isdigit():
            raise forms.ValidationError("Students are not allowed to log in from the faculty login page.")
        return username


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['user','email','fullname', 'address', 'profile_image', 'branch', 'year','mobile_no']

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['user','email','fullname', 'address', 'profile_image', 'short_intro', 'mobile_no']


 # forms.py
from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['subject', 'message']

