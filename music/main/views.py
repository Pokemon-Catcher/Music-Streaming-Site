from django.shortcuts import render, redirect
from django.db.models import Prefetch
from . import models
from . import forms
import random
from datetime import datetime
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
import re
from django.contrib.auth import authenticate, login, logout, forms as auth_forms
from django.contrib.auth.models import User

def index(request):
    songs=models.Song.objects.all()
    new_songs=models.Song.objects.order_by('release_date')[:10]
    random_songs=models.Song.objects.filter(id__in=random.sample(set(models.Song.objects.all().values_list('id',flat=True)),k=min(10,models.Song.objects.count())))
    recommend_songs=models.Song.objects.all()[:10]
    best_songs=models.Song.objects.all()[:10]
    return render(request,'main/index.html',{'new_songs':new_songs,'random_songs':random_songs,'best_songs':best_songs,'recommend_songs':recommend_songs})

def upload(request):
    if request.method == 'POST':
        form=forms.UploadForm(request.POST,request.FILES)
        try:
            if(form.is_valid()):
                authorType=models.RoleType.objects.get_or_create(title='Author')[0]
                role=models.Role.objects.filter(artist__name=form.cleaned_data["artist"],type=authorType)[:1]
                if(not role):
                    artist=models.Artist.objects.get_or_create(name=form.cleaned_data["artist"])[0]
                    role=models.Role.objects.create(artist=artist,type=authorType)
                tags=form.cleaned_data["tags"].split(",")
                for tag in tags:
                    tagObj=models.Tag.objects.get_or_create(tag=tag)[0]
                print(form.cleaned_data)
                song=models.Song.objects.create(title=form.cleaned_data["title"],
                                release_date=form.cleaned_data["release_date"],
                                cover=form.files["cover"],
                                audio=form.files["audio"],
                                )
                song.role.set(role)
                song.tags.set(tags)
                song.save()
                print('ok')
                return render(request, 'main/message.html',{'title':"Успешно","message":"Загрузка удалась"})
            else:
                return render(request, 'main/message.html',{'title':"Ошибка","message":"Загрузка не удалась: "+form.errors.as_text()})
        except Exception as e:
            return render(request, 'main/message.html',{'title':"Ошибка","message":"Загрузка не удалась: "+repr(e)})
    else: 
        form=forms.UploadForm()
        return render(request, 'main/upload.html', {'form':form})

def search(request):
    queries=re.split(r',|\s',request.GET['query'])
    artist_query=[]
    song_query=[]
    for q in queries:
        artist_query=(artist_query or Q(name__icontains=q)) & Q(name__icontains=q)
        song_query=(song_query or Q(title__icontains=q)|Q(tags=q)|Q(role__artist__name__icontains=q)) & (Q(title__icontains=q)|Q(tags=q)|Q(role__artist__name__icontains=q))
    print(song_query)
    artists=models.Artist.objects.filter(artist_query)
    songs=models.Song.objects.filter(song_query)
    """ albums=models.Album.objects.filter(song_query)
    playlists=models.Playlist.objects.filter(song_query) """
    return render(request, 'main/search.html',{'songs':songs,'artists':artists})

def song(request,id):
    song=models.Song.objects.get(id=id)
    return render(request, 'main/song.html',{'song':song})

def log_in(request):
    if request.method == 'POST':
        form=auth_forms.AuthenticationForm(data=request.POST)
        if(form.is_valid()):
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                result=login(request, user)
                return redirect("/")
            else:
                return render(request, 'main/login.html',{'form':form,"errors":["Неправильный логин или пароль"]})
        return render(request, 'main/login.html',{'form':form,"errors":form.non_field_errors()})
    else:
        if not request.user.is_authenticated:
            form=auth_forms.AuthenticationForm()
            return render(request, 'main/login.html',{'form':form})
        else:
             return redirect("/")

def profile(request):
    return redirect("/")

def log_out(request):
    logout(request)
    return redirect("/")

def register(request):
    if request.method == 'POST':
        form=auth_forms.UserCreationForm(request.POST)
        if(form.is_valid()):
            user=form.save()
            login(request,user)
            return redirect("/")
        return render(request, 'main/register.html',{'form':form, "errors":form.errors})
    else:
        if not request.user.is_authenticated:
            form=auth_forms.UserCreationForm()
            return render(request, 'main/register.html',{'form':form})
        else:
            return redirect("/")