from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image','created_date', 'published_date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['published_date'].required = True
        self.fields['published_date'].required = True

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author']
        widgets = {
            'author': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 155, 'rows': 3})
        }

        labels = {
            'text': 'Comentar:',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['author'].initial = user