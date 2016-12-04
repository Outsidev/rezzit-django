from django import forms
from .models import Post,Comment,User,UserProfile

class CommentForm(forms.ModelForm):  
    class Meta:
        model = Comment
        fields = ('text',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()