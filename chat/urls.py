from django.urls import path
from . import views

urlpatterns = [
    path('api/send/', views.chat_message, name='chat_message'),
]
