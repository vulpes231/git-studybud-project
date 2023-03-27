from django.urls import path

from .views import main, room, about, contact, createRoom, updateRoom, deleteRoom, deleteMessage, userProfile, updateUser

urlpatterns = [
    path('', main, name="main"),
    path('create-room/', createRoom, name="create-room"),
    path('update-room/<str:pk>', updateRoom, name="update-room"),
    path('delete-room/<str:pk>', deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', deleteMessage, name="delete-message"),
    path('update-user/', updateUser, name="update-user"),
    path('room/<str:pk>', room, name="room"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('profile/<str:pk>', userProfile, name="profile"),
]