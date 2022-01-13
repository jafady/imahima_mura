from django.shortcuts import render
from ..models import User,UserSetting,UserSelectCategory
from ..serializers import UserSerializer,UserInfoSerializer,UserSettingSerializer,UserSelectCategorySerializer
from rest_framework import generics, permissions
from .mixin import MultipleFieldLookupMixin

from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

# ユーザ操作
class UserList(generics.ListAPIView):
    """ ユーザ一覧 """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


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

class UserInfoRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """ ユーザ基本情報取得用 """
    queryset = User.objects.all()
    # queryset = User.objects.select_related('UserSetting').values('id','username',
    #                 'usersetting'
    #                 )
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated, )

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
