from django import forms
from django.contrib.auth.models import User
from .models import UserInfo
from . import models

class UploadForm(forms.Form):
    title = forms.CharField(label="Название", max_length=64,widget=forms.TextInput(attrs={"class":"form-control"}))
    artist=forms.CharField(label="Исполнитель", max_length=64, required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    audio=forms.FileField(label="Аудио",widget=forms.FileInput(attrs={"accept":"audio/*","class":"form-control-file"}),)
    cover=forms.ImageField(label="Обложка",required=False,widget=forms.FileInput(attrs={"accept":"image/*","class":"form-control-file"}))
    release_date=forms.DateField(label="Дата выпуска",required=False,widget=forms.DateInput(attrs={"type":"date", "class":"form-control" }))
    tags=forms.RegexField(label="Теги",regex=r'((^\w+$))|(^(\w+,)+\w+$)',required=False,widget=forms.TextInput(attrs={"class":"form-control"}))

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ["avatar"]

class PlaylistForm(forms.Form):
    playlist = forms.ModelChoiceField(None,empty_label=None,widget=forms.Select(attrs={'"id"="playlist"'}))
    song = forms.Field(required=True)
    def __init__(self, user, *args, **kwargs):
        self.fields['playlist'].queryset = models.Playlist.objects.filter(owner=user)
        super(PlaylistForm, self).__init__(*args, **kwargs)