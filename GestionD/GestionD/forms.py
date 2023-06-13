from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=True)
    password =forms.ChoiceField(required=False)
    
