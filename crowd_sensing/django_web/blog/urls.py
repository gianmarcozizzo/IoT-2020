from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('storage/', views.storage, name='blog-storage'),
]
