from django.shortcuts import render
from ..models import User,UserSetting,UserSelectCategory,HouseMate
from ..serializers import UserSerializer,UserNameSerializer,UserSettingSerializer,UserSelectCategorySerializer
from rest_framework import generics, permissions, status
from .mixin import MultipleFieldLookupMixin

from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.db import connection
from rest_framework.decorators import api_view, permission_classes


from django.db.models import F, Q, Case, When, Value, CharField
import datetime
import calendar
import pytz 
local_tz = jst = pytz.timezone('Asia/Tokyo')#TODO取り扱い

import logging
logger = logging.getLogger(__name__)
streamhandler = logging.StreamHandler()
logger.addHandler(streamhandler)
logger.setLevel(logging.WARN)
logger.warn('warntest')




# ログアウト
class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserCreate(generics.CreateAPIView):
    """ ユーザ作成 """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )


class UserInfo(APIView):
    """ 一連のユーザ情報取得 """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, userId):
        info = User.objects\
                .select_related('UserSetting').select_related('UserSetting__statusId__StatusMaster')\
                .prefetch_related('UserSelectCategory').select_related('UserSelectCategory__categoryId__CategoryMaster')\
                .filter(id=userId)\
                .values('id','username',
                    'userSetting__icon','userSetting__isAllCategorySelected',
                    'userSetting__noticableMonTimeStart','userSetting__noticableMonTimeEnd','userSetting__noticableTueTimeStart','userSetting__noticableTueTimeEnd',
                    'userSetting__noticableWedTimeStart','userSetting__noticableWedTimeEnd','userSetting__noticableThuTimeStart','userSetting__noticableThuTimeEnd',
                    'userSetting__noticableFriTimeStart','userSetting__noticableFriTimeEnd','userSetting__noticableSatTimeStart','userSetting__noticableSatTimeEnd',
                    'userSetting__noticableSunTimeStart','userSetting__noticableSunTimeEnd',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'userselectcategory__categoryId','userselectcategory__categoryId__categoryName',
                    )
                

        res_json = json.dumps(list(info), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

class UsersFuture(APIView):
    """ 未来時点のユーザ一覧取得 """
    """ 未来時点なのでステータスの読み替えを行う """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, houseId, dateTime):
        invited_datetime = datetime.datetime.strptime(f'{dateTime}','%Y-%m-%dT%H:%M:%S').replace(tzinfo=local_tz).astimezone(local_tz)

        infos = User.objects.get_base_info(target_day=invited_datetime)\
                .filter(housemate__houseId=houseId,housemate__isApproved=True)\
                .values('id','username',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )
        
        for info in infos:
            if info['nowStatus'] == 'ヒマ':
                info['nowStatus'] = '予定ではヒマ'
            if info['nowStatus'] == 'ゲーム中':
                info['nowStatus'] = 'ヒマじゃない'
                
        res_json = json.dumps(list(infos), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")


class UserBaseInfo(APIView):
    """ ユーザ基本情報取得用 """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, userId):
        info = User.objects.get_base_info()\
                .filter(id=userId)\
                .values('id','username',
                    'userSetting__icon',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )
        
        
        res_json = json.dumps(list(info), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")
        

class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """ ユーザ設定更新用 """
    queryset = User.objects.all()
    serializer_class = UserNameSerializer
    permission_classes = (permissions.AllowAny, )

class UserSettingRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """ ユーザ設定更新用 """
    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer
    lookup_field = 'userId'
    permission_classes = (permissions.IsAuthenticated, )

class UserSelectCategoryCreate(generics.CreateAPIView):
    """ ユーザが通知設定したカテゴリのcreate """
    queryset = UserSelectCategory.objects.all()
    serializer_class = UserSelectCategorySerializer
    permission_classes = (permissions.IsAuthenticated, )

class UserSelectCategoryDelete(MultipleFieldLookupMixin,generics.DestroyAPIView):
    """ ユーザが通知設定したカテゴリのdelete """
    queryset = UserSelectCategory.objects.all()
    serializer_class = UserSelectCategorySerializer
    lookup_fields = ('userId','categoryId')
    permission_classes = (permissions.IsAuthenticated, )

class UserList(APIView):
    """ ユーザ一覧 基本情報 """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, houseId):
        # 返す値：userid,username,icon,ステータス,今日のヒマ時間        
        info = User.objects.get_base_info()\
                .filter(housemate__houseId=houseId,housemate__isApproved=True)\
                .values('id','username',
                    'userSetting__icon',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )
                
        res_json = json.dumps(list(info), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")


