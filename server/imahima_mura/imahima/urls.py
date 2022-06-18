from django.urls import path
from push_notifications.api.rest_framework import WebPushDeviceViewSet

from .views import *

urlpatterns = [
    path('logout/', Logout.as_view()),

    path('users/<houseId>/', UserList.as_view()),
    path('create_user/', UserCreate.as_view()),
    path('user_info/<userId>/', UserInfo.as_view()),
    path('user_base_info/<userId>/', UserBaseInfo.as_view()),
    path('users_future/<houseId>/<dateTime>/', UsersFuture.as_view()),


    path('update_user/<pk>/', UserRetrieveUpdate.as_view()),
    path('user_setting/<userId>/', UserSettingRetrieveUpdate.as_view()),
    path('user_select_category/', UserSelectCategoryCreate.as_view()),
    path('user_select_category/delete/<userId>/<categoryId>/', UserSelectCategoryDelete.as_view()),
    path('user_password_update/<pk>/', UserPasswordRetrieveUpdate.as_view()),


    path('create_house/', HouseCreate.as_view()),
    path('create_housemate/', HouseMateCreate.as_view()),
    path('get_myinvitation/<userId>/', HouseMateInvitation.as_view()),
    path('accept_invitation/<pk>/', AcceptInvitation.as_view()),
    path('myhouses/<userId>/', MyHouses.as_view()),
    path('house_info/<pk>/', HouseInfo.as_view()),
    path('check_housemate/<houseId>/<userId>/', CheckHouseMate.as_view()),

    path('create_invitetoken/', InviteHouseTokenCreate.as_view()),
    path('use_invitetoken/<userId>/<inviteToken>', InviteHouseTokenUse.as_view()),

    path('create_event/', EventCreate.as_view()),
    path('event_info/<eventId>/', EventInfo.as_view()),
    path('update_event/<pk>/', EventUpdate.as_view()),
    path('delete_event/<pk>/', EventDelete.as_view()),
    path('join_event/', EventJoin.as_view()),
    path('leave_event/<eventId>/<userId>/', EventLeave.as_view()),
    path('events/<houseId>/', EventList.as_view()),

    path('feelings/<houseId>/', HouseMateFeelingList.as_view()),
    path('upsert_feelings/', HouseMateFeelingCreate.as_view()),
    path('delete_feelings/<houseId>/<userId>/<gameId>/', HouseMateFeelingDestroy.as_view()),

    path('create_status/', StatusMasterCreate.as_view()),
    path('statuses/', StatusMasterList.as_view()),
    path('create_category/', CategoryMasterCreate.as_view()),
    path('categorys/', CategoryMasterList.as_view()),

    path('games/', GameList.as_view()),
    path('create_game/', GameCreate.as_view()),
    path('update_game/<pk>/', GameRetrieveUpdate.as_view()),
    path('delete_game/<pk>/', GameDestroy.as_view()),

    path('game_details/', GameDetailTypeList.as_view()),
    path('create_game_detail/', GameDetailTypeCreate.as_view()),
    path('update_game_detail/<pk>/', GameDetailTypeRetrieveUpdate.as_view()),
    path('delete_game_detail/<pk>/', GameDetailTypeDestroy.as_view()),

    path('regist_webpush/', WebPushDeviceViewSet.as_view({'post': 'create'}))
]