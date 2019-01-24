from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField('Created Date', default=timezone.now)
    title = models.CharField('Title', max_length=200)
    content = models.TextField('Content')
    slug = models.SlugField('Slug')

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)


class Pad(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    locate = models.CharField(max_length=70)
    date = models.DateTimeField()

    def __str__(self):
        return '{} update from {}'.format(self.name, self.date)