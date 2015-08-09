from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"username",
        error_messages={'required': 'please input your username'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"username",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"password",
        error_messages={'required': u'please input password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"password",
            }
        ),
    )
    imagecode = forms.CharField(
        required=True,
        label=u"imagecode",
        error_messages={'required': u'please input image code'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"image code",
            }
        ),                   
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"username or password is wrong")
        else:
            cleaned_data = super(LoginForm, self).clean()