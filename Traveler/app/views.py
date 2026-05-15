"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm

from .forms import AnketaForm, CommentForm, BlogForm
from .models import Blog, Comment

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'страница контактов',
            'year':datetime.now().year,
        }
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Мы – команда увлеченных путешественников. Наша миссия – вдохновлять вас на новые открытия!',
            'year':datetime.now().year,
        }
    )

def links(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )


def registration(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')
    else:
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    rating = {'1': '1 — Ужасно', '2': '2 — Плохо', '3': '3 — Средне',
              '4': '4 — Хорошо', '5': '5 — Отлично'}
    travel_frequency = {'rarely': 'Редко (раз в несколько лет)',
                        'sometimes': 'Иногда (раз в год)',
                        'often': 'Часто (2-3 раза в год)',
                        'always': 'Постоянно путешествую'}
    destinations = {'europe': 'Европа', 'asia': 'Азия', 'africa': 'Африка',
                    'america': 'Северная Америка', 'australia': 'Австралия и Океания'}
    
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['email'] = form.cleaned_data['email']
            data['rating'] = rating[form.cleaned_data['rating']]
            data['travel_frequency'] = travel_frequency[form.cleaned_data['travel_frequency']]

            fav = form.cleaned_data['favorite_destinations']
            if fav:
                data['favorite_destinations'] = ', '.join([destinations[d] for d in fav])
            else:
                data['favorite_destinations'] = 'Не указано'
            
            data['budget'] = form.cleaned_data['budget']
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()
    
    return render(
        request,
        'app/anketa.html',
        {
            "title": "Обратная связь",
            'form': form,
            'year': datetime.now().year,
            'data': data
        }
    )


def blog(request):
    assert isinstance(request, HttpRequest)

    posts = Blog.objects.all()

    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог о путешествиях',
            'posts': posts,
            'year': datetime.now().year,
        }
    )
def blogpost(request, parametr):
    assert isinstance(request, HttpRequest)

    post = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.date = datetime.now()
            comment.post = post
            comment.save()
            return redirect('blogpost', parametr=post.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'title': post.title,
            "post": post,
            "year": datetime.now().year,
            "comments": comments,
            "form": form,
        }
    )


def newpost(request):
    """Страница добавления новой статьи блога (только для администратора)"""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'title': 'Добавить статью',
            'form': form,
            'year': datetime.now().year,
        }
    )

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео о путешествиях',
            'year': datetime.now().year,
        }
    )