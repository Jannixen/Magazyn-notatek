from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [path('', views.storage_page), path("storage", views.storage_page), path("noteform", views.add_note_page),
               path('note/<int:note_id>/', views.note_page), path("accounts/", include("django.contrib.auth.urls")),
               path('register', views.register, name="register"),
               path('note/<int:note_id>/share/', views.share_note_page),
               ]
