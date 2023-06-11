from django.urls import path, path
from . import views

urlpatterns = [
    path('', views.index),
    path('upload', views.upload, name="upload"),
    path('search', views.search, name="search"),
    path('song/<int:id>', views.song, name="song"),
    path('login',views.log_in,name="login"),
    path('profile',views.profile,name="profile"),
    path('register',views.register,name="register"),
    path('logout',views.log_out,name="logout"),
]
