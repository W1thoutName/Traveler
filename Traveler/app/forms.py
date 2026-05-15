"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment, Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    
    city = forms.CharField(label='Из какого вы города?', min_length=2, max_length=100)
    
    email = forms.EmailField(label='Ваш e-mail', min_length=7, required=False)
    
    rating = forms.ChoiceField(label='Оцените наш сайт о путешествиях',
        choices=[('1', '1 — Ужасно'),
                 ('2', '2 — Плохо'),
                 ('3', '3 — Средне'),
                 ('4', '4 — Хорошо'),
                 ('5', '5 — Отлично')],
        widget=forms.RadioSelect, initial=4)
    
    travel_frequency = forms.ChoiceField(label='Как часто вы путешествуете?',
        choices=[('rarely', 'Редко (раз в несколько лет)'),
                 ('sometimes', 'Иногда (раз в год)'),
                 ('often', 'Часто (2-3 раза в год)'),
                 ('always', 'Постоянно путешествую')],
        widget=forms.Select, initial='sometimes')
    
    favorite_destinations = forms.MultipleChoiceField(label='Любимые направления',
        choices=[('europe', 'Европа'),
                 ('asia', 'Азия'),
                 ('africa', 'Африка'),
                 ('america', 'Северная Америка'),
                 ('australia', 'Австралия и Океания')],
        widget=forms.CheckboxSelectMultiple, required=False)
    
    budget = forms.IntegerField(label='Бюджет на путешествие (тыс. руб.)',
        min_value=10, max_value=5000, required=False)
    
    notice = forms.BooleanField(label='Получать рассылку о горящих турах?',
        required=False)
    
    message = forms.CharField(label='Ваши пожелания и предложения',
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 70}), required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"} # метка к полю формы text
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'Напишите ваш комментарий здесь...',
                'class': 'comment-field'
            })
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        labels = {
            'title': 'Заголовок статьи',
            'description': 'Краткое содержание',
            'content': 'Полное содержание',
            'image': 'Изображение для статьи'
        }