import json
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
import datetime
import asyncio
import pytz
from django.db.models import Q

from channels.db import database_sync_to_async

from .models import House,HouseMate,User,UserSetting,UserSelectCategory
from push_notifications.models import WebPushDevice
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
        
        if msg_type == 'joinHouse':
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'join.house',
                    'houseId': data_json['houseId'],
                }
            )

        if msg_type == 'talk':
            message = data_json['message']
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'talk.receive',
                    'houseId': data_json['houseId'],
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
                    'houseId': data_json['houseId'],
                    'userId': self.user.id,
                }
            )
        
        if msg_type == 'sendTalks':
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'talk.senddata',
                    'houseId': data_json['houseId'],
                    'target': data_json['target'],
                    'talks': data_json['talks'],
                }
            )
        
        if msg_type == 'noticeChangeStatus':
            # ステータス変更の画面側通知
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'status.notice',
                    'houseId': data_json['houseId'],
                    'userId': self.user.id,
                    'status': data_json['status'],
                }
            )

            # ステータス変更の通知
            await self.send_inclease_members_notice({
                    'houseId': data_json['houseId'],
                    'userId': self.user.id,
                    'status': data_json['status'],
                })
        
        if msg_type == 'noticeChangeEvent':
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'event.notice',
                    'houseId': data_json['houseId'],
                    'userId': self.user.id,
                }
            )
        
        if msg_type == 'createEvent':
            await self.send_event_create_notice({
                    'houseId': data_json['houseId'],
                    'userId': self.user.id,
                    'userName': self.user.username,
                    'eventId': data_json['eventId'],
                    'eventName': data_json['eventName'],
                    'categoryId': data_json['categoryId'],
                    'targetUserIds': data_json['targetUserIds'],
                })
        
        if msg_type == 'sendManualNotice':
            await self.send_manual_notice({
                    'houseId': data_json['houseId'],
                    'userId': self.user.id,
                    'userName': self.user.username,
                    'eventId': data_json['eventId'],
                    'eventName': data_json['eventName'],
                    'targetUserIds': data_json['targetUserIds'],
                    'msg': data_json['msg'],
                })
        
    # Receive message from room group
    # 誰かが家に参加した
    async def join_house(self, event):
        await self.send(text_data=json.dumps({
            'type': 'someOneJoinHouse',
            'houseId': event['houseId'],
        }))

    # 雑談を受け取る
    async def talk_receive(self, event):
        await self.send(text_data=json.dumps({
            'type': 'talk',
            'houseId': event['houseId'],
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
            'houseId': event['houseId'],
            'userId': event['userId'],
        }))
    
    # 雑談のログを受領する
    async def talk_senddata(self, event):
        if self.user.id == event['target']:
            await self.send(text_data=json.dumps({
                'type': 'receiveTalks',
                'houseId': event['houseId'],
                'talks': event['talks'],
            }))
    
    # ステータス変更を受領する
    async def status_notice(self, event):
        if self.user.id != event['userId']:
            await self.send(text_data=json.dumps({
                'type': 'someOneChangeStatus',
                'houseId': event['houseId'],
                'userId': event['userId'],            
                'status': event['status'],
            }))
    
    # イベント作成&変更を受領する
    async def event_notice(self, event):
        await self.send(text_data=json.dumps({
            'type': 'someOneChangeEvent',
            'houseId': event['houseId'],
        }))
    
    
    # 通知処理
    # websocketの送信側で処理を行う

    # ステータス変更に伴うヒマ人数増加の通知
    async def send_inclease_members_notice(self, event):
        print('ヒマ人数増加通知送信')
        noticeIntervalMin = 60
        sendNoticeCount = 0

        # 増えたときだけ通知
        if event['status'] != 'hima':
            print('増えてないから終了')
            return
        
        # 通知対象の取得
        # 同じ家かつ、現時点のステータスが予定ではヒマとヒマが対象
        targetUsers = await self.get_member_notice_target(event['houseId'])

        # ヒマ人数のカウント(2人以下なら誰にも送らないので終了)
        himaUsers = [user for user in targetUsers if user['nowStatus'] == 'ヒマ']
        himaCount = len(himaUsers)
        if himaCount < 2:
            print('2人以下なので終了')
            return

        for targetUser in targetUsers:
            # 自分には送らない
            if targetUser['id'] == self.user.id:
                print('event_create 自分なので送らない ' + targetUser['id'])
                continue
            
            # 時間と人数チェック
            # 前回記録時から日付が変わっていたら人数カウントリセット
            lastMemberNoticeNumber = targetUser['housemate__lastMemberNoticeNumber']
            if targetUser['housemate__lastMemberNoticeTime'].day != datetime.datetime.now().day:
                print('日付変わった userid:' + targetUser['id'] + ' houseId:'+ event['houseId'])
                lastMemberNoticeNumber = 0
            
            sendFlg = False
            # 最後送信時の人数から増えていたら送ってOK(かつ2人以上)
            if lastMemberNoticeNumber < himaCount:
                sendFlg = True
            
            # 前回の通知から規定時間以上経っていたら送ってOK
            lastMemberNoticeTime = targetUser['housemate__lastMemberNoticeTime'] + datetime.timedelta(minutes = noticeIntervalMin)
            lastMemberNoticeTime = datetime.datetime.today().replace(year=lastMemberNoticeTime.year, month=lastMemberNoticeTime.month, day=lastMemberNoticeTime.day,
                                                                            hour=lastMemberNoticeTime.hour, minute=lastMemberNoticeTime.minute, second=lastMemberNoticeTime.second)
            print('lastMemberNoticeTime ' + lastMemberNoticeTime.strftime('%Y/%m/%d %H:%M:%S'))
            print('now ' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            if lastMemberNoticeTime < datetime.datetime.now():
                sendFlg = True

            # 通知送信
            if sendFlg:
                # 通知送信
                print('通知送る')
                await self.send_WebPushDevice(targetUser['id'],
                    json.dumps({
                        'type': 'incleaseMembersNotice',
                        'houseId': event['houseId'],
                        'count': himaCount,
                    })
                )
                print('通知送った')
                # 最終送信日時と人数を記録する
                await self.update_member_notice(event['houseId'],targetUser['id'],himaCount)
                sendNoticeCount += 1

        
        # 規定時間経過後にもう一回発火する(誰かひとりにでも送ったら次を仕込む)
        if sendNoticeCount < 1:
            print('送ってないのでここで終わり houseId:'+ event['houseId'])
            return
        print('一定時間後に試す')
        await asyncio.sleep(noticeIntervalMin*60)
        print('次の通知確認')
        self.send_inclease_members_notice(event)


    # イベント作成に伴う通知
    async def send_event_create_notice(self, event):
        print('イベント作成通知送信')

        for targetUserId in event['targetUserIds']:
            # 自分には送らない
            if targetUserId == self.user.id:
                print('event_create 自分なので送らない ' + targetUserId)
                continue
                
            # カテゴリが通知許可されていないならはじく
            if not await self.check_category(userId=targetUserId, categoryId=event['categoryId']):
                print('event_create カテゴリ許可されていないので送らない ' + targetUserId)
                continue
        
            # 時間がそろっているうちに何秒待つかもここで計算する
            noticable_time = await self.get_noticable_time(userId=targetUserId)
            print('noticable_time')
            print(noticable_time)
            if noticable_time is None:
                print('event_create noticable_time is Noneので送らない ' + targetUserId)
                continue
            # 通知秒
            notice_second = 0
            if noticable_time == 0:
                notice_second = 0
            else:
                diff_time = noticable_time - datetime.datetime.now()
                notice_second = diff_time.seconds
            
            await self.send_WebPushDevice(targetUserId,
                json.dumps({
                    'type': 'receiveCreateEvent',
                    'houseId': event['houseId'],
                    'eventId': event['eventId'],
                    'eventName': event['eventName'],
                    'userId': targetUserId,
                    'noticeSecond': notice_second,
                })
            )
            print('イベント作成通知送った '+targetUserId)

    # 手動メッセージを送信する
    async def send_manual_notice(self, event):
        print('手動メッセージ送信')

        # ターゲットユーザ分だけ通知処理を行う。待機時間の計算はそれぞれなので個別
        for targetUserId in event['targetUserIds']:
            # 時間がそろっているうちに何秒待つかもここで計算する
            noticable_time = await self.get_noticable_time(userId=targetUserId)
            print('noticable_time')
            print(noticable_time)
            if noticable_time is None:
                continue
            # 通知秒
            notice_second = 0
            if noticable_time == 0:
                notice_second = 0
            else:
                diff_time = noticable_time - datetime.datetime.now()
                notice_second = diff_time.seconds
            print(notice_second)

            # notice_second=0
            await self.send_WebPushDevice(targetUserId,
                json.dumps({
                    'type': 'receiveManualMessage',
                    'houseId': event['houseId'],
                    'eventId': event['eventId'],
                    'eventName': event['eventName'],
                    'userName': event['userName'],
                    'noticeSecond': notice_second,
                    'msg': event['msg'],
                })
            )
            print('手動メッセージ送った '+targetUserId)
    

    # 共通処理

    # websocketの部屋名取得
    def get_room_group_name(self,houseId):
        return 'socket_%s' % houseId

    # DB操作
    # 参加している家一覧取得
    @database_sync_to_async
    def get_houses(self):
        result = House.objects.prefetch_related('HouseMate').filter(housemate__userId=self.scope["user"].id,housemate__isApproved=True).values('id', 'houseName')
        houseId = [str(data['id']) for data in result]
        return houseId
    
    # ヒマ人数増加通知の対象取得
    @database_sync_to_async
    def get_member_notice_target(self, houseId):
        print('取得開始' + houseId)
        user_base_info = User.objects.get_base_info(target_day=datetime.datetime.now())\
                .prefetch_related('HouseMate')\
                .filter(housemate__houseId=houseId,housemate__isApproved=True)\
                .filter(Q(nowStatus='ヒマ')|Q(nowStatus='予定ではヒマ'))\
                .values('id','username','nowStatus','housemate__lastMemberNoticeTime','housemate__lastMemberNoticeNumber')
        users = [data for data in user_base_info]
        return users
    
    # ヒマ人数増加通知の記録
    @database_sync_to_async
    def update_member_notice(self, houseId,userId,count):
        print('記録' + houseId)
        targetHousemate = HouseMate.objects.get(houseId=houseId, userId=userId, isApproved=True)
        targetHousemate.lastMemberNoticeTime = datetime.datetime.now()
        targetHousemate.lastMemberNoticeNumber = count

        targetHousemate.save()
        return True

    # カテゴリの通知許可を確認
    @database_sync_to_async
    def check_category(self,userId,categoryId):
        user_setting = UserSetting.objects\
                        .filter(userId=userId)\
                        .values('isAllCategorySelected')
        isAllCategorySelected = [data['isAllCategorySelected'] for data in user_setting][0]

        if isAllCategorySelected == True:
            return True
        
        user_category = UserSelectCategory.objects\
                        .filter(userId=userId, categoryId=categoryId)\
                        .values('categoryId')
        
        if len(user_category) > 0:
            return True

        return False
    
    # 通知する時間取得
    # ステータス関係なく送るとき、指定時間まで待つのが必要
    # ヒマ/予定ではヒマの期間内⇒送る
    # ヒマ/予定ではヒマの期間外⇒ヒマのスタート時間か20:00の早い方
    @database_sync_to_async
    def get_noticable_time(self,userId):
        # ヒマ/予定ではヒマの期間取得
        user_base_info = User.objects.get_base_info(target_day=datetime.datetime.now())\
                .filter(id=userId)\
                .values('id','username',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )
        
        nextday = datetime.datetime.now() + datetime.timedelta(days = 1)
        user_base_info_next_day = User.objects.get_base_info(target_day = nextday)\
                .filter(id=userId)\
                .values('id','username',
                    'userSetting__statusValidDateTime','userSetting__statusId__statusName',
                    'todayStartTime','todayEndTime','nowStatus'
                    )
        # print('データ取得')

        userSetting__statusValidDateTime = [data['userSetting__statusValidDateTime'] for data in user_base_info][0]
        userSetting__statusId__statusName = [str(data['userSetting__statusId__statusName']) for data in user_base_info][0]
        todayStartTime = [data['todayStartTime'] for data in user_base_info][0]
        todayEndTime = [data['todayEndTime'] for data in user_base_info][0]

        nextDayStartTime = [data['todayStartTime'] for data in user_base_info_next_day][0]

        now = datetime.datetime.now()
        userSetting__statusValidDateTime = datetime.datetime.today().replace(year=userSetting__statusValidDateTime.year, month=userSetting__statusValidDateTime.month, day=userSetting__statusValidDateTime.day,
                                                                            hour=userSetting__statusValidDateTime.hour, minute=userSetting__statusValidDateTime.minute, second=userSetting__statusValidDateTime.second)
        todayStartTime = datetime.datetime.today().replace(hour=todayStartTime.hour, minute=todayStartTime.minute, second=todayStartTime.second)
        todayEndTime = datetime.datetime.today().replace(hour=todayEndTime.hour, minute=todayEndTime.minute, second=todayEndTime.second)
        nextDayStartTime = datetime.datetime.today().replace(hour=nextDayStartTime.hour, minute=nextDayStartTime.minute, second=nextDayStartTime.second) + datetime.timedelta(days = 1)

        noticeTime = datetime.datetime.strptime('20:00', '%H:%M')
        noticeTime = datetime.datetime.today().replace(hour=noticeTime.hour, minute=noticeTime.minute, second=0)
        noticeTime_nextDay = datetime.datetime.today().replace(hour=noticeTime.hour, minute=noticeTime.minute, second=0) + datetime.timedelta(days = 1)

        # print('データ取得完了')
        # 期間内とは
        # userSetting__statusValidDateTimeがヒマであれば、今送って大丈夫。
        # userSetting__statusValidDateTimeの範囲内で、ヒマじゃないというなら通知なしでは
        #   ヒマ明け後の直近のヒマ時間という考えもあるが、キリがなくなりそうなので止めとく。
        if userSetting__statusValidDateTime > now:
            print('ヒマ意思表示期間内')
            if userSetting__statusId__statusName == "ヒマ":
                return 0
            else:
                return None
        else:
            print('ヒマ意思表示期間外')
            if todayStartTime < now:
                print('todayStartTime < now')
                if now < todayEndTime:
                    print('now < todayEndTime')
                    return 0
                if now < noticeTime:
                    print('now < 20:00')
                    return noticeTime
                else:
                    print('now > 20:00')
                    # 翌日のstarttimeと"20:00"の早い方
                    if nextDayStartTime < noticeTime_nextDay:
                        print('nextDayStartTime < 20:00')
                        return nextDayStartTime
                    else:
                        print('nextDayStartTime > 20:00')
                        return noticeTime_nextDay

            else:
                print('todayStartTime > now')
                if todayStartTime < noticeTime:
                    print('now < todayStartTime < 20:00')
                    return todayStartTime
                elif noticeTime < now:
                    print('20:00 < now < todayStartTime')
                    return 0
                else:
                    print('now < 20:00 < todayStartTime')
                    return noticeTime
    
    
    # Webpushの情報を取得しつつ送信
    @database_sync_to_async
    def send_WebPushDevice(self,targetUserId,data):
        device = WebPushDevice.objects.filter(user_id=targetUserId)
        try:
            device.send_message(data)
        except:
            print('不正な宛先があるので最新の一つだけ送る')
            device = WebPushDevice.objects.filter(user_id=targetUserId).order_by('-id').first()
            device.send_message(data)
        return True