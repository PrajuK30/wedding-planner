from django import forms
from .models import CustomUser

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'mobile', 'location', 'pincode', 'age', 'gender', 'role']
