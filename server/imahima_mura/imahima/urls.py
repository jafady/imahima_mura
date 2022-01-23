from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('logout/', Logout.as_view()),

    path('users/<houseId>/', UserList.as_view()),
    path('create_user/', UserCreate.as_view()),
    path('user_info/<userId>/', UserInfo.as_view()),
    path('user_base_info/<userId>/', UserBaseInfo.as_view()),
    path('user_setting/<userId>/', UserSettingRetrieveUpdate.as_view()),
    path('user_select_category/', UserSelectCategoryCreate.as_view()),
    path('user_select_category/delete/<userId>/<categoryId>/', UserSelectCategoryDelete.as_view()),


    path('create_house/', HouseCreate.as_view()),
    path('create_housemate/', HouseMateCreate.as_view()),
    path('get_myinvitation/<userId>/', HouseMateInvitation.as_view()),
    path('accept_invitation/<pk>/', AcceptInvitation.as_view()),
    path('myhouses/<userId>/', MyHouses.as_view()),

    path('create_status/', StatusMasterCreate.as_view()),
    path('statuses/', StatusMasterList.as_view()),
    path('create_category/', CategoryMasterCreate.as_view()),
    path('categorys/', CategoryMasterList.as_view()),
]