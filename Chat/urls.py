from django.urls import path
from . import views
urlpatterns = [
    path('', views.index ),
    path('room/<slug:slug>/', views.room_detail, name='room_detail')
]