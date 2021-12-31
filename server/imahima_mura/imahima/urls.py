from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('users/', UserList.as_view()),
    path('create_user/', UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),

    path('create_house/', HouseCreate.as_view()),
    path('create_housemate/', HouseMateCreate.as_view()),
    path('get_myinvitation/<userId>/', HouseMateInvitation.as_view()),
    path('accept_invitation/<pk>/', AcceptInvitation.as_view()),
]