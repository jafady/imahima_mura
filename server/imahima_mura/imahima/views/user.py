from django.shortcuts import render
from ..models import User,UserSetting,UserSelectCategory,HouseMate
from ..serializers import UserSerializer,UserSettingSerializer,UserSelectCategorySerializer
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

# ログアウト
class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# ユーザ操作
# class UserList(generics.ListAPIView):
#     """ ユーザ一覧 """
#     queryset = User.objects.all().order_by('id')
#     serializer_class = UserSerializer
#     permission_classes = (permissions.IsAuthenticated,)


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

class UserBaseInfo(APIView):
    """ ユーザ基本情報取得用 """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, userId):
        info = User.objects\
                .select_related('UserSetting').select_related('UserSetting__statusId__StatusMaster')\
                .prefetch_related('UserSelectCategory').select_related('UserSelectCategory__categoryId__CategoryMaster')\
                .filter(id=userId)\
                .values('id','username',
                    'userSetting__icon',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    )
                

        res_json = json.dumps(list(info), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

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

        # 曜日から取り出すカラムを特定する
        weekday = datetime.date.today().weekday()
        weekday_name = calendar.day_name[weekday][0:3]
        todayStart = 'userSetting__noticable'+weekday_name+'TimeStart'
        todayEnd = 'userSetting__noticable'+weekday_name+'TimeEnd'

        
        # ヒマなときに、イベント中かどうかでゲーム中かの判定を行うが、今はイベントがないのでこのまま
        info = User.objects\
                .filter(housemate__houseId=houseId).filter(housemate__isApproved=True)\
                .select_related('UserSetting').select_related('UserSetting__statusId__StatusMaster')\
                .annotate(todayStartTime = F(todayStart)).annotate(todayEndTime = F(todayEnd))\
                .annotate(nowStatus = Case(
                    When(Q(userSetting__statusValidDateTime__lt = datetime.datetime.now(), todayStartTime__lt = datetime.datetime.now().time(), todayEndTime__gte = datetime.datetime.now().time()), 
                        then=Value('予定ではヒマ')),
                    When(Q(userSetting__statusValidDateTime__lt = datetime.datetime.now(), todayStartTime__gte = datetime.datetime.now().time()), 
                        then=Value('ヒマじゃない')),
                    When(Q(userSetting__statusValidDateTime__lt = datetime.datetime.now(), todayEndTime__lt = datetime.datetime.now().time()), 
                        then=Value('ヒマじゃない')),
                    When(Q(userSetting__statusValidDateTime__gte = datetime.datetime.now(), userSetting__statusId__statusName = 'ヒマじゃない'), 
                        then=Value('ヒマじゃない')),
                    When(Q(userSetting__statusValidDateTime__gte = datetime.datetime.now(), userSetting__statusId__statusName = 'ヒマ'), 
                        then=Value('ヒマ')),
                    default=Value('ヒマ'),
                    output_field=CharField()
                    )
                )\
                .values('id','username',
                    'userSetting__icon',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )
                
        res_json = json.dumps(list(info), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

