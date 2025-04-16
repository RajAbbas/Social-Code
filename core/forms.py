from django import forms
from .models import CustomUser as User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Post,Comment,Reply

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if password and password2 and password!=password2:
            raise ValidationError("password do not match")
        
        return cleaned_data
    
    def save(self, commit = True):
        user =  super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit :
            user.save()
        return user,
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','image','topic']

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Comment','class':'form-control'}))

    class Meta:
        model = Comment
        fields=["text"]

class ReplyForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={"placeholder":'Reply','class':'form-control'}))
    class Meta:
        model=Reply
        fields=['content']
    
    