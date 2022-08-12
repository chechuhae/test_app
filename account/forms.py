from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'ivanovivan'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': '12345678'})


class CreationUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        help_texts = {
            'username': None,
        }


class CreationProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'town', 'profile_pic')
