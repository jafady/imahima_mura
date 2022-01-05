from django.shortcuts import render
from ..models import StatusMaster,CategoryMaster
from rest_framework import generics, permissions

from ..serializers import StatusMasterSerializer,CategoryMasterSerializer

# ステータスマスタ操作
class StatusMasterList(generics.ListAPIView):
    """ View to list all StatusMasters"""
    queryset = StatusMaster.objects.all().order_by('id')
    serializer_class = StatusMasterSerializer
    permission_classes = (permissions.IsAuthenticated,)


class StatusMasterCreate(generics.CreateAPIView):
    """ View to create a new StatusMaster. Only accepts POST requests """
    queryset = StatusMaster.objects.all()
    serializer_class = StatusMasterSerializer
    permission_classes = (permissions.IsAuthenticated, )


class StatusMasterRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """ Retrieve a StatusMaster or update StatusMaster information.
    Accepts GET and PUT requests and the record id must be provided in the request """
    queryset = StatusMaster.objects.all()
    serializer_class = StatusMasterSerializer
    permission_classes = (permissions.IsAuthenticated, )



# カテゴリマスタ操作
class CategoryMasterList(generics.ListAPIView):
    """ View to list all CategoryMasters"""
    queryset = CategoryMaster.objects.all().order_by('id')
    serializer_class = CategoryMasterSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CategoryMasterCreate(generics.CreateAPIView):
    """ View to create a new CategoryMaster. Only accepts POST requests """
    queryset = CategoryMaster.objects.all()
    serializer_class = CategoryMasterSerializer
    permission_classes = (permissions.IsAuthenticated, )


class CategoryMasterRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """ Retrieve a CategoryMaster or update CategoryMaster information.
    Accepts GET and PUT requests and the record id must be provided in the request """
    queryset = CategoryMaster.objects.all()
    serializer_class = CategoryMasterSerializer
    permission_classes = (permissions.IsAuthenticated, )