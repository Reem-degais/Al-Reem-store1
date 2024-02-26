from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
         'placeholder': "Enter your name",
         'class': 'form-control'
     }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
         'placeholder': "Enter your last name",
         'class': 'form-control'
     }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
         'placeholder': "Enter your email",
         'class': 'form-control'
     }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
         'placeholder': "Enter your phone number",
         'class': 'form-control'
     }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
         'placeholder': "Enter Password",
         'class': 'form-control'
     }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
         'placeholder': "Repeat Password",
         'class': 'form-control'
     }))
     
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    # to check if passwords are match or not
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise forms.ValidationError(
                "Password does not match!"
            )