from django import forms
from .models import CustomUser, BlogPost
from django.core.exceptions import ValidationError
import re

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            'user_type', 'first_name', 'last_name', 'username', 'email',
            'profile_picture', 'password', 'confirm_password',
            'address_line1', 'city', 'state', 'pincode'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-control'  
            if self.errors.get(field_name):
                css_class += ' is-invalid'
            field.required = True 
            field.widget.attrs['required'] = 'required'  
            field.widget.attrs['class'] = css_class

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith(('.com', '.org', '.net')):
            raise ValidationError("Email domain must be .com, .org, or .net")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        if not re.match(r'^\w+$', username):
            raise ValidationError("Username can only contain letters, numbers and underscores")
        return username

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode.isdigit() or len(pincode) != 6:
            raise ValidationError("Pincode must be a 6-digit number")
        return pincode

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                if field_name != 'is_draft':
                    field.widget.attrs['class'] = 'form-control'
                else:
                    field.widget.attrs['class'] = 'form-check-input'
