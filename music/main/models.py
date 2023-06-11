from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    
# Create your models here.
class Artist(models.Model):
    name = models.CharField('Имя', max_length=64)
    description = models.TextField('Описание', blank=True)
    photo = models.ImageField('Фото',upload_to='artists_pics', blank=True)
    def __str__(self):
        return self.name

class RoleType(models.Model):
    title = models.CharField('Роль', max_length=64, primary_key=True)
    def __str__(self):
        return self.title

class Role(models.Model):
    type = models.ForeignKey(RoleType,on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.artist)+'/'+str(self.type)

class Tag(models.Model):
    tag = models.CharField('Тег',max_length=64, primary_key=True)

class Like(models.Model):
    active=models.BooleanField('Активен',default=True)
    date=models.DateField('Дата')
    user=models.ForeignKey(User,on_delete=models.CASCADE)\

class Song(models.Model):
    title = models.CharField('Название', max_length=64)
    role = models.ManyToManyField(Role, blank=True)
    cover = models.ImageField('Обложка',upload_to='song_covers', blank=True)
    audio = models.FileField('Аудиофайл',upload_to='audio')
    release_date = models.DateField('Дата выпуска',blank=True)
    upload_date = models.DateField('Дата загрузки',default=datetime.now)
    tags = models.ManyToManyField(Tag,default=None, blank=True)
    likes = models.ManyToManyField(Like,default=None, blank=True)

    def __str__(self):
        return self.title
    def likes_count(self):
        return self.likes.count()
    def get_tags(self):
        a=[i.tag for i in self.tags.all()]
        return ', '.join(a)
    def authors(self):
        a=[i.artist.name for i in self.role.filter(type__title='Author')[:3]]
        if len(a)==0:
            a=[i.artist.name for i in self.role.all()[:3]]
        return ', '.join(a)

class Album(models.Model):
    title = models.CharField('Название', max_length=64)
    release_date = models.DateField('Дата выпуска')
    cover = models.ImageField('Обложка',upload_to='albums_covers', blank=True)
    songs = models.ManyToManyField(Song, blank=True)
    tags = models.ManyToManyField(Tag,default=None, blank=True)
    likes = models.ManyToManyField(Like,default=None, blank=True)
    def __str__(self):
        return self.title

class Playlist(models.Model):
    title = models.CharField('Название', max_length=64)
    songs = models.ManyToManyField(Song, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField('Дата создания',default=datetime.now)
    tags = models.ManyToManyField(Tag,default=None, blank=True)
    likes = models.ManyToManyField(Like,default=None, blank=True)
    def __str__(self):
        return self.title

