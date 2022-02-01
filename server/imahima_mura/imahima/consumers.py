import json
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
import datetime
import pytz

from channels.db import database_sync_to_async

from .models import House,HouseMate,User
# websocketのリクエスト受信
class ImahimaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('websocket接続--------------------------')
        print(self.scope["user"])
        self.user = self.scope["user"]
        # 参加している家IDを一覧取得し、全部に入る
        houseIds = await self.get_houses()
        for houseId in houseIds:
            room_group_name = self.get_room_group_name(houseId)
            print(room_group_name)
            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        houseIds = await self.get_houses()
        for houseId in houseIds:
            room_group_name = self.get_room_group_name(houseId)
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        msg_type = data_json['type']
        room_group_name = self.get_room_group_name(data_json['houseId'])
        # 接続の追加
        if msg_type == 'addConnect':
            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )

        if msg_type == 'talk':
            message = data_json['message']
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'talk.receive',
                    'message': message,
                    'userId': self.user.id,
                    'userName': self.user.username,
                    'date': datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y/%m/%d"),
                    'time': datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%H:%M"),
                }
            )
        if msg_type == 'requestTalks':
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'talk.requestdata',
                    'userId': self.user.id,
                }
            )
        
        if msg_type == 'sendTalks':
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'talk.senddata',
                    'target': data_json['target'],
                    'talks': data_json['talks'],
                }
            )
        
        if msg_type == 'noticeChangeStatus':
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'status.notice',
                    'userId': self.user.id,
                    'status': data_json['status'],
                }
            )
        

    # Receive message from room group
    async def talk_receive(self, event):
        await self.send(text_data=json.dumps({
            'type': 'talk',
            'message': event['message'],
            'userId': event['userId'],
            'userName': event['userName'],
            'date': event['date'],
            'time': event['time'],
        }))
    
    # 雑談のログをリクエスト
    async def talk_requestdata(self, event):
        await self.send(text_data=json.dumps({
            'type': 'requestTalks',
            'userId': event['userId'],
        }))
    
    # 雑談のログを受領する
    async def talk_senddata(self, event):
        if self.user.id == event['target']:
            await self.send(text_data=json.dumps({
                'type': 'receiveTalks',
                'talks': event['talks'],
            }))
    
    # ステータス変更を受領する
    async def status_notice(self, event):
        if self.user.id != event['userId']:
            await self.send(text_data=json.dumps({
                'type': 'someOneChangeStatus',
                'userId': event['userId'],            
                'status': event['status'],
            }))
    

    # 共通処理
    def get_room_group_name(self,houseId):
        return 'socket_%s' % houseId

    # DB操作
    # 参加している家一覧取得
    @database_sync_to_async
    def get_houses(self):
        result = House.objects.prefetch_related('HouseMate').filter(housemate__userId=self.scope["user"].id,housemate__isApproved=True).values('id', 'houseName')
        houseId = [str(data['id']) for data in result]
        return houseId