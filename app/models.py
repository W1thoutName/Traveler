from django.contrib import admin
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Полное описание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата публикации")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
#blank=True	Разрешено пустое значение в формах
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

    def __str__(self): #как булдет отображать в адмике объект коментария
        return self.title

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return f"Комментарий от {self.author.username}: {self.text[:50]}"

    class Meta:
        db_table = "Comments"
        ordering = ["-date"]
        verbose_name = "комментарий"
        #В админке будет написано "комментарий".
        verbose_name_plural = "комментарии"
admin.site.register(Blog)