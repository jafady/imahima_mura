from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('users/', UserList.as_view()),
    path('create_users/', UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),
]