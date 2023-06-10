from django.shortcuts import render
from django.db.models import Prefetch
from . import models
from . import forms
import random
from datetime import datetime

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