from django import forms
from .models import Posts,Comment

class PostModelForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={"rows":2}))
    class Meta:
        model=Posts
        fields=("content","image")

class CommentModelForm(forms.ModelForm):
    body=forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"yorum ekleyin..."}))
    class Meta:
        model=Comment
        fields=("body",)