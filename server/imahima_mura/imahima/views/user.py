from django.shortcuts import render
from ..models import User,UserSetting,UserSelectCategory,HouseMate,Event,EventMembers
from ..serializers import UserSerializer,UserNameSerializer,UserSettingSerializer,UserSelectCategorySerializer,UserPasswordSerializer
from rest_framework import generics, permissions, status
from .mixin import MultipleFieldLookupMixin

from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.db import connection
from rest_framework.decorators import api_view, permission_classes


from django.db.models import F, Q, Case, When, Value, CharField, DateTimeField, ExpressionWrapper
import datetime
import random, string
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
                .values('id','username', 'userSetting__discordId',
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
        info_with_ongame = setOngameAtUsers(users = infos,target_datetime=invited_datetime)
        
        for info in info_with_ongame:
            if info['nowStatus'] == 'ヒマ':
                info['nowStatus'] = '予定ではヒマ'
            if info['nowStatus'] == 'ゲーム中':
                info['nowStatus'] = 'ヒマじゃない'
                
        res_json = json.dumps(list(info_with_ongame), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")


class UserBaseInfo(APIView):
    """ ユーザ基本情報取得用 """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, userId):
        info = User.objects.get_base_info(target_day=datetime.datetime.now())\
                .filter(id=userId)\
                .values('id','username',
                    'userSetting__icon',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )

        info_with_ongame = setOngameAtUsers(users = info,target_datetime = datetime.datetime.now())
        
        res_json = json.dumps(list(info_with_ongame), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")
        
class UserPasswordRetrieveUpdate(APIView):
    """ ユーザパスワード更新用 """
    permission_classes = (permissions.AllowAny, )
    def put(self, request, userId):
        # パスワード生成
        n = 8
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        password = ''.join(randlst)
        print("パスワードリセット")

        # パスワード更新
        user = User.objects.get(id=userId)
        user.set_password(password)
        user.save()

        res_json = json.dumps(password, cls=DjangoJSONEncoder)
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
        info = User.objects.get_base_info(target_day=datetime.datetime.now())\
                .filter(housemate__houseId=houseId,housemate__isApproved=True)\
                .values('id','username',
                    'userSetting__icon',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )
        
        
        info_with_ongame = setOngameAtUsers(users = info,target_datetime = datetime.datetime.now())
                
        res_json = json.dumps(list(info_with_ongame), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

# 対象日時のまだ終わっていないイベント一覧
def getEvent(target_datetime = datetime.datetime.now()):
    target_day = target_datetime.date()
    infos = Event.objects\
                .select_related('EventMembers')\
                .filter(
                    Q(startDate__gte=target_day), Q(startDate__lt=target_day + datetime.timedelta(days=1)), 
                    Q(endTime__gte = target_datetime.time()) )\
                .annotate(startDateAtJp = ExpressionWrapper(F('startDate') + datetime.timedelta(hours=9),
                    output_field=DateTimeField()
                ))\
                .order_by('startDate', 'startTime', 'endTime')\
                .values('id', 'houseId', 'eventName', 'recruitmentNumbersLower', 'recruitmentNumbersUpper',
                    'location', 'locationUrl', 'startDateAtJp', 'startTime', 'endTime', 'tyouseiUrl', 'categoryId', 'detail'
                    )

    for info in infos:
        userIds = EventMembers.objects\
            .filter(eventId=info.get('id'))\
            .values_list('userId', flat=True)
        info['userIds'] = [data for data in userIds]
    
    return infos

# ユーザ一覧にゲーム中かどうかの情報を足す
def setOngameAtUsers(users,target_datetime = datetime.datetime.now()):
    events = getEvent(target_datetime=target_datetime)
    for user in users:
        for event in events:
            # イベント参加予定か確認
            if user['id'] not in event['userIds']:
                continue
            # 現時点がイベント中であれば、ステータスをゲーム中に変更する
            if event['startTime'] < target_datetime.time() and  target_datetime.time() < event['endTime']:
                user['nowStatus'] = 'ゲーム中'
            
            # ヒマ時間から差し引く
            time0 = datetime.time(0, 0, 0, 0)
            if user['todayEndTime'] != time0 and user['todayEndTime'] < event['startTime']:
                continue
            if event['endTime'] !=time0 and event['endTime'] < user['todayStartTime']:
                continue
            if user['todayStartTime'] < event['startTime']:
                # 対象時点より後ろを採用する
                if event['startTime'] < target_datetime.time() and \
                    (user['todayEndTime'] == time0 or
                    (user['todayEndTime'] != time0 and event['endTime'] < user['todayEndTime'])):
                    user['todayStartTime'] = event['endTime']
                else:
                    user['todayEndTime'] = event['startTime']

            elif user['todayEndTime'] == time0 or \
                    (user['todayEndTime'] != time0 and event['endTime'] < user['todayEndTime']):
                user['todayStartTime'] = event['endTime']

    return users
