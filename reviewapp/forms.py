from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Review
from .models import Product

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        initial='user',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default role to 'user' if not already set
        if not self.initial.get('role'):
            self.initial['role'] = 'user'

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']