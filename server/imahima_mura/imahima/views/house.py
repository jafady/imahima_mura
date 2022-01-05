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


class HouseMateCreate(generics.CreateAPIView):
    """ ユーザ招待 """
    queryset = HouseMate.objects.all()
    serializer_class = HouseMateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HouseMateInvitation(APIView):
    """ 招待確認 """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, userId):
        # fields = ('id', 'houseId', 'userId', 'isApproved', 'house')
        invitation = HouseMate.objects.select_related('House').filter(userId=userId,isApproved=False).values('id', 'houseId', 'userId', 'houseId__houseName')

        res_json = json.dumps(list(invitation), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")


class AcceptInvitation(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk):
        invitation = HouseMate.objects.get(id=pk)
        if invitation:
            invitation.isApproved = True
            invitation.save()
        
        resdata = HouseMate.objects.filter(id=pk)
        res_json = json.dumps(list(resdata.values()), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")