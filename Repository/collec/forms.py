from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()