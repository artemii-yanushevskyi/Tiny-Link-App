from django import forms

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(LoginForm, self).__init__(*args, **kwargs)

    attrs_password = {
        "type": "password",
        "class": "form-control",
        "placeholder": "********",
    }
    attrs_username = {
        "class": "form-control",
        "placeholder": "Enter Username",
        "style": "margin-bottom:20px;",
    }

    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs=attrs_username))
    password = forms.CharField(label='Password', max_length=100, widget=forms.TextInput(attrs=attrs_password))
