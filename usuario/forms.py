from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class registroForm(UserCreationForm):
    username = forms.IntegerField(label = "CFN")
    password1 = forms.CharField(label = "ECN",widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Confirma ECN",widget = forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','password1','password2']
        help_texts = {k: "" for k in fields}
        
class loginForm(AuthenticationForm):
    username = forms.IntegerField(label = "CFN")
    password = forms.CharField(label = "ECN")