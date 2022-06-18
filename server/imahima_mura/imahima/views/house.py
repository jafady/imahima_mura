from django.shortcuts import render
from rest_framework import generics, permissions, status

from rest_framework.views import APIView
from rest_framework.response import Response
import json, datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponse
from django.db.models import F

from ..models import House,HouseMate,InviteHouseToken,User,Game,GameDetailType,HouseMateFeeling
from ..serializers import HouseSerializer,HouseMateSerializer,InviteHouseTokenSerializer,GameSerializer,GameDetailTypeSerializer,HouseMateFeelingSerializer

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

class InviteHouseTokenCreate(generics.CreateAPIView):
    """ 招待用URLトークン発行 """
    queryset = InviteHouseToken.objects.all()
    serializer_class = InviteHouseTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

class InviteHouseTokenUse(APIView):
    """ 招待用URLトークンの使用 """
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, userId, inviteToken):
        # 期限切れトークン削除
        InviteHouseToken.objects.filter(validDateTime__lte=datetime.datetime.now()).delete()

        # 対象トークン取得
        inviteToken = InviteHouseToken.objects \
                        .filter(id=inviteToken, validDateTime__gte=datetime.datetime.now())\
                        .values('id','houseId','validDateTime')

        # 何も取れなかったら空白で返す
        if len(list(inviteToken)) < 1:
            res_json = json.dumps({'msg':'有効期限切れの可能性があります'}, cls=DjangoJSONEncoder)
            return HttpResponse(res_json, content_type="application/json")

        houseId = [str(data['houseId']) for data in inviteToken][0]

        # 対象ユーザが招待済みであれば何もしない
        housemate = HouseMate.objects.select_related('House').filter(houseId=houseId, userId=userId).values('id', 'houseId', 'userId', 'isApproved')
        if len(list(housemate)) > 0:
            res_json = json.dumps({'msg':'招待済みです'}, cls=DjangoJSONEncoder)
            return HttpResponse(res_json, content_type="application/json")
        
        # 招待手続き
        house = House.objects.get(id=houseId)
        user = User.objects.get(id=userId)
        invitation = HouseMate.objects.create_housemate(request.user,houseId=house,userId=user)

        res_invitaiton = HouseMate.objects.filter(id=invitation.id).values('id','houseId','userId')
        res_json = json.dumps(list(res_invitaiton)[0], cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")


# ゲームマスタ操作
class GameList(generics.ListAPIView):
    """ View to list all Game"""
    queryset = Game.objects.all().order_by('id')
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GameCreate(generics.CreateAPIView):
    """ View to create a new Game. Only accepts POST requests """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated, )


class GameRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """ Retrieve a Game or update Game information.
    Accepts GET and PUT requests and the record id must be provided in the request """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated, )

class GameDestroy(generics.DestroyAPIView):
    """ Destroy a GameDetailType information. """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated, )

# ゲーム詳細マスタ操作
class GameDetailTypeList(generics.ListAPIView):
    """ View to list all GameDetailType"""
    queryset = GameDetailType.objects.all().order_by('id')
    serializer_class = GameDetailTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GameDetailTypeCreate(generics.CreateAPIView):
    """ View to create a new GameDetailType. Only accepts POST requests """
    queryset = GameDetailType.objects.all()
    serializer_class = GameDetailTypeSerializer
    permission_classes = (permissions.IsAuthenticated, )


class GameDetailTypeRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """ Retrieve a GameDetailType or update GameDetailType information.
    Accepts GET and PUT requests and the record id must be provided in the request """
    queryset = GameDetailType.objects.all()
    serializer_class = GameDetailTypeSerializer
    permission_classes = (permissions.IsAuthenticated, )

class GameDetailTypeDestroy(generics.DestroyAPIView):
    """ Destroy a GameDetailType information. """
    queryset = GameDetailType.objects.all()
    serializer_class = GameDetailTypeSerializer
    permission_classes = (permissions.IsAuthenticated, )

# 今の気分
class HouseMateFeelingList(APIView):
    """ 今の気分のリスト返却 """
    serializer_class = HouseMateFeelingSerializer
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, houseId):
        games = Game.objects.filter(houseId = houseId).order_by('sortNo')\
                .values('id','gameName')
        
        for game in games:
            gameUsers = User.objects.get_base_info(target_day=datetime.datetime.now())\
                .prefetch_related('HouseMateFeeling')\
                .filter(housematefeeling__houseId = houseId,housematefeeling__gameId = game['id'],housematefeeling__gameDetailTypeId__isnull=True, housematefeeling__choice=1)\
                .filter(nowStatus='ヒマ')\
                .values('id')
            game['gameUsers'] = [data['id'] for data in gameUsers]

            gameDetails = GameDetailType.objects.filter(houseId = houseId,gameId = game['id']).order_by('sortNo')\
                .values('id','gameDetailTypeName','leftName','rightName')
            for gameDetail in gameDetails:
                gameDetailUsers = User.objects.get_base_info(target_day=datetime.datetime.now())\
                            .prefetch_related('HouseMateFeeling')\
                            .filter(housematefeeling__houseId = houseId,housematefeeling__gameId = game['id'],\
                                housematefeeling__gameDetailTypeId = gameDetail['id'])\
                            .filter(nowStatus='ヒマ')\
                            .annotate(userId=F('id'))\
                            .annotate(choice=F('housematefeeling__choice'))\
                            .values('userId','choice')
                gameDetail['gameDetailUsers'] = [data for data in gameDetailUsers]

            game['gameDetails'] = [data for data in gameDetails]


        res_json = json.dumps(list(games), cls=DjangoJSONEncoder)
        return HttpResponse(res_json, content_type="application/json")

class HouseMateFeelingCreate(generics.CreateAPIView):
    """ View to create a new HouseMateFeeling. Only accepts POST requests """
    queryset = HouseMateFeeling.objects.all()
    serializer_class = HouseMateFeelingSerializer
    permission_classes = (permissions.IsAuthenticated, )

class HouseMateFeelingDestroy(APIView):
    """ Destroy a HouseMateFeeling information. """
    serializer_class = HouseMateFeelingSerializer
    lookup_fields = ('houseId','userId','gameId')
    permission_classes = (permissions.IsAuthenticated, )
    def delete(self, request, houseId, userId, gameId):
        feelings = HouseMateFeeling.objects.filter(houseId = houseId, userId = userId, gameId = gameId)
        feelings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
