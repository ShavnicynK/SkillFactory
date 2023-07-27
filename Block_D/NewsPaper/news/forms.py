from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'name',
            'author',
            'categorys',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        name = cleaned_data.get('name')
        if name == content:
            raise ValidationError(
                'Текст материала должен отличаться от названия'
            )
        return cleaned_data