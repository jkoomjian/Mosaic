from django import forms

class LoginForm(forms.Form):
    #using widget_tweaks
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30, required=False, widget=forms.PasswordInput())
    submitType = forms.CharField(max_length=30)
    # the not so smart way:
    #password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'span3', 'placeholder': 'Password Again'}))