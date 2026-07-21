from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """Sign-up form with role selection"""
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('consultant', 'Consultant'),
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        label='your role',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Login form"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )