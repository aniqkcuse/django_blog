from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class":"form-control"})

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label="Passoword confirmation", widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["email", "password", "is_active", "is_admin"]

class UserAuntheticateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class":"form-control"})

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = CustomUser
        fields = ["email"]