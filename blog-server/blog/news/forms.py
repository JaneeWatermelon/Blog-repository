from django import forms
from django.forms import ModelForm


class LeaveCommentForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'comment_input',
        'placeholder': 'Введите комментарий',
        'maxlength': '1000',
        'rows': '1',
    }), required=True)
