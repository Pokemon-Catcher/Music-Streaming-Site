from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField('Аватар',upload_to='avatars', blank=True,default='avatars/noimage.svg')

class Listening(models.Model):
    date = models.DateField('Дата прослушивания',default=datetime.now) 
    user = models.ForeignKey(User,on_delete=models.SET_DEFAULT,default=None,null=True)
    time = models.FloatField('Длительность',default=0)

class View(models.Model):
    date = models.DateField('Дата прослушивания',default=datetime.now) 
    user = models.ForeignKey(User,on_delete=models.SET_DEFAULT,default=None,null=True)

class Content(models.Model):
    tags = models.ManyToManyField('Tag',default=None, blank=True)
    likes = models.ManyToManyField('Like',default=None, blank=True)
    views = models.ManyToManyField('View',default=None,blank=True)
    def likes_count(self):
        likes=self.likes.filter(active=True)
        return likes.count()
    def views_count(self):
        return self.views.count()
    def addView(self,user):
        self.views.add(View.objects.create(user=user))
        self.save()
        return self
    def get_tags(self):
        a=[i.tag for i in self.tags.all()]
        return ', '.join(a)
    def is_liked(self,user):
        return self.likes.filter(user=user,active=True).count()>0

class Artist(Content):
    name = models.CharField('Имя', max_length=64)
    description = models.TextField('Описание', blank=True)
    photo = models.ImageField('Фото',upload_to='artists_pics', blank=True,default='artists_pics/noimage.svg')
    def __str__(self):
        return self.name

class RoleType(models.Model):
    title = models.CharField('Роль', max_length=64, default="Автор", primary_key=True)
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
    active=models.BooleanField('Активен',default=False)
    date=models.DateField('Дата',default=datetime.now)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def switch(self):
        self.active=not self.active
        self.save()
        return self

class Song(Content):
    title = models.CharField('Название', max_length=64)
    role = models.ManyToManyField(Role, blank=True,default=None)
    cover = models.ImageField('Обложка',upload_to='song_covers', blank=True)
    audio = models.FileField('Аудиофайл',upload_to='audio')
    release_date = models.DateField('Дата выпуска',blank=True)
    upload_date = models.DateField('Дата загрузки',default=datetime.now)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE,null=True,default=None)
    listenings = models.ManyToManyField('Listening',blank=True,default=None)

    def __str__(self):
        return self.title
    def authors(self):
        a=self.role.filter(type__title='Author')[:3]
        if a.count()==0:
            a=self.role.all()[:3]
        return a
    def listenings_count(self):
        return self.listenings.count()        
    def addListening(self,user):
        self.listenings.add(Listening.objects.create(user=user))
        self.save()
        return self
        
class Album(Content):
    title = models.CharField('Название', max_length=64)
    release_date = models.DateField('Дата выпуска')
    cover = models.ImageField('Обложка',upload_to='albums_covers', blank=True)
    songs = models.ManyToManyField(Song, blank=True)
    authors = models.ManyToManyField(Artist,blank=True,default=None)
    def __str__(self):
        return self.title

class Playlist(Content):
    title = models.CharField('Название', max_length=64)
    songs = models.ManyToManyField(Song, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField('Дата создания',default=datetime.now)
    def __str__(self):
        return self.title
