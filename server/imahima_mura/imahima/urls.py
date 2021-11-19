from django.urls import path

from . import views
from .views import *

urlpatterns = [
    # path('', views.index, name='index'),

    path('users/', UserList.as_view()),
    path('create-users/', UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),
]