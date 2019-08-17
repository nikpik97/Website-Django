from django.urls import path
from about_me import views

urlpatterns = [
    path('', views.about_me, name='about_me'),
]