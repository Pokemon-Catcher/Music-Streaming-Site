from django import forms
from django.contrib.auth.models import User

class UploadForm(forms.Form):
    title = forms.CharField(label="Название", max_length=64,widget=forms.TextInput(attrs={"class":"form-control"}))
    artist=forms.CharField(label="Исполнитель", max_length=64, required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    audio=forms.FileField(label="Аудио",widget=forms.FileInput(attrs={"accept":"audio/*","class":"form-control-file"}),)
    cover=forms.ImageField(label="Обложка",required=False,widget=forms.FileInput(attrs={"accept":"image/*","class":"form-control-file"}))
    release_date=forms.DateField(label="Дата выпуска",required=False,widget=forms.DateInput(attrs={"type":"date", "class":"form-control" }))
    tags=forms.RegexField(label="Теги",regex=r'((^\w+$))|(^(\w+,)+\w+$)',required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
