from django.shortcuts import render
from rest_framework import generics, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponse

from ..models import House,HouseMate
from ..serializers import HouseSerializer,HouseMateSerializer

# 家全体の設定
class HouseCreate(generics.CreateAPIView):
    """ 家作成 """
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = (permissions.IsAuthenticated, )

class HouseInfo(generics.RetrieveUpdateAPIView):
    """ 家の設定 """
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = (permissions.IsAuthenticated, )


class HouseMateCreate(generics.CreateAPIView):
    """ ユーザ招待 """
    queryset = HouseMate.objects.all()
    serializer_class = HouseMateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HouseMateInvitation(APIView):
    """ 自分の招待確認 """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, userId):
        invitation = HouseMate.objects.select_related('House').filter(userId=userId,isApproved=False).values('id', 'houseId', 'userId', 'houseId__houseName')

        res_json = json.dumps(list(invitation), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")


class AcceptInvitation(APIView):
    """ 招待承認 """
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, pk):
        invitation = HouseMate.objects.get(id=pk)
        if invitation:
            invitation.isApproved = True
            invitation.save()
        
        resdata = HouseMate.objects.filter(id=pk)
        res_json = json.dumps(list(resdata.values()), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

class MyHouses(APIView):
    """ 所属する家一覧 """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, userId):
        houses = House.objects.prefetch_related('HouseMate').filter(housemate__userId=userId,housemate__isApproved=True).values('id', 'houseName')
        res_json = json.dumps(list(houses), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")


class CheckHouseMate(APIView):
    """ 招待有無関係なく、登録されているか確認 """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, houseId, userId):
        invitation = HouseMate.objects.select_related('House').filter(houseId=houseId, userId=userId).values('id', 'houseId', 'userId', 'isApproved')

        res_json = json.dumps(list(invitation), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")