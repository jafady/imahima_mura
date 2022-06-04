from django.shortcuts import render
from rest_framework import generics, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
import json
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponse
from django.db.models import F, Q, DateTimeField, ExpressionWrapper

from ..models import Event,EventMembers
from ..serializers import EventSerializer,EventMembersSerializer

# イベントの設定
class EventCreate(generics.ListCreateAPIView):
    """ イベント 作成 """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, )

class EventList(APIView):
    """ イベント 一覧 """
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, houseId):

        target_day = datetime.date.today()

        infos = Event.objects\
                .select_related('EventMembers')\
                .filter(Q(houseId=houseId), (Q(startDate__gte=target_day) | Q(startDate__isnull=True)))\
                .order_by('startDate', 'startTime', 'endTime')\
                .values('id', 'houseId', 'eventName', 'recruitmentNumbersLower', 'recruitmentNumbersUpper',
                    'location', 'locationUrl', 'startDate', 'startTime', 'endTime', 'tyouseiUrl', 'categoryId', 'detail'
                    )

        for info in infos:
            userIds = EventMembers.objects\
                .filter(eventId=info.get('id'))\
                .values_list('userId', flat=True)
            info['userIds'] = [data for data in userIds]

        res_json = json.dumps(list(infos), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

class EventInfo(APIView):
    """ イベント 1件取得 """
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, eventId):
        infos = Event.objects\
                .select_related('EventMembers')\
                .filter(id=eventId)\
                .values('id', 'houseId', 'eventName', 'recruitmentNumbersLower', 'recruitmentNumbersUpper',
                    'location', 'locationUrl', 'startDate', 'startTime', 'endTime', 'tyouseiUrl', 'categoryId', 'detail'
                    )

        for info in infos:
            userIds = EventMembers.objects\
                .filter(eventId=info.get('id'))\
                .values_list('userId', flat=True)
            info['userIds'] = [data for data in userIds]

        res_json = json.dumps(list(infos), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

class EventUpdate(generics.UpdateAPIView):
    """ イベント 更新 """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, )

class EventDelete(generics.DestroyAPIView):
    """ イベント 削除 """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, )

class EventJoin(generics.CreateAPIView):
    """ イベント 参加 """
    queryset = EventMembers.objects.all()
    serializer_class = EventMembersSerializer
    permission_classes = (permissions.AllowAny, )

class EventLeave(APIView):
    """ イベント 退出 """
    permission_classes = (permissions.IsAuthenticated, )
    def delete(self, request, eventId, userId):
        EventMembers.objects.filter(eventId=eventId, userId=userId).delete()
        return HttpResponse(status=200)