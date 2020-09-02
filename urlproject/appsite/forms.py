from django import forms

class NameForm(forms.Form):
    your_name= forms.CharField (label='Your name', max_length = 100)
    numbers = forms.IntegerField(label='number')
    url = forms.URLField(label='url')

class RegistrationForm(forms.Form):
    user_name = forms.CharField(label = 'User name', max_length = 100)
    email_id = forms.EmailField(label ='Email ID')
    password = forms.CharField(widget = forms.PasswordInput)
    password_retype = forms.CharField(widget = forms.PasswordInput)

class UrlForm(forms.Form):
    url = forms.URLField()
