from django import forms
from .models import Account_holders

class UserForm(forms.ModelForm):
    class Meta:
        model = Account_holders
        fields = ['username','name', 'gender', 'email', 'mobile', 'dob', 'address','password']