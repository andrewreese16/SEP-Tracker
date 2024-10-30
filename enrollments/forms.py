# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer  # Import the Customer model

# User registration form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Form for the Customer model
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'sep_start_date']

        # You can customize the widgets here if needed
        widgets = {
            'sep_start_date': forms.SelectDateWidget(),
        }
