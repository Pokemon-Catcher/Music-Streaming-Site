from django.contrib import admin
from . import models
# Register your models here
admin.site.register(models.Role)
admin.site.register(models.RoleType)
admin.site.register(models.Album)
admin.site.register(models.Song)
admin.site.register(models.Playlist)
admin.site.register(models.Artist)
admin.site.register(models.Tag)
admin.site.register(models.Like)