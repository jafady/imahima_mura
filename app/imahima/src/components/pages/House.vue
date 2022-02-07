<template>
    <div class="container house_container" v-on:click="checkStatus">
        <Header />
        <!-- 家タイトル -->
        <div class="mt-2 house_title content_center">
            <div class="weight"></div>
            <div class="house_name">{{houseName}}</div>
            <div class="house_setting">
                <div class="setting_icon"></div>
                <div class="setting_word">家の設定</div>
            </div>
        </div>
        <!-- メニュータブ -->
        <div class="mt-3 house_tab">
            <div class="friend" :class={friend_active:isFriendMode} @click="houseMode = 'friend'">
                <div class="friend_icon"></div>
                <div class="friend_word">友達に会う</div>
            </div>
            <div class="room" :class={room_active:isRoomMode} @click="houseMode = 'room'">
                <div class="room_word">部屋を探す</div>
                <div class="room_icon"></div>
            </div>
        </div>
        <!-- 選択メニューによって切り替える予定 -->
        <!-- TODO: 友達に会うは、ヒマじゃない人には見せない。 -->
        <div v-if="isFriendMode" class="mt-4">
            <HouseFriend :talks="talks" ref="houseFriend"/>
        </div>
        <div v-else-if="isRoomMode" class="mt-4">
            <HouseRoom />
        </div>
        <div class="m-3 blank_content" />
        <StatusSettingModal ref="statusSettingModal" @noticeChangeStatus="noticeChangeStatus" />
    </div>
</template>

<style lang="scss">
.house_container {
    min-height: 100%;
    max-width: 100% !important;
    padding: unset !important;
    background-position: top;
    background-size: auto;
    background-image: url("../../assets/img/house/flooring.png");
    background-color: rgba(0, 0, 0, 0.4);
    background-blend-mode: hard-light;

    .house_title {
        width: 90%;
        height: 40px;
        background-color: white;
        margin: 0 auto;
        border: 3px solid;
        border-radius: 11px;
        border-color: var(--main-bg-color);

        .weight {
            width:40px;
        }
        .house_name {
            font-size: 22px;
            font-weight: bold;
            color: var(--main-bg-color);
        }

        .house_setting {
            text-align: -webkit-center;
            .setting_icon {
                width:20px;
                height:20px;
                background-size: contain;
                background-image: url("../../assets/img/house/wrench.svg");
                background-repeat: no-repeat;
            }
            .setting_word {
                height: 11px;
                font-size: 10px;
                font-weight: bold;
            }
        }
    }

    .house_tab{
        width: 90%;
        height: 65px;
        margin: 0 auto;
        border-radius: 36px;

        .friend{
            background-color: var(--inactive-bg-color2);
            width: calc(50vw + 5%);
            height: inherit;
            border-radius: 32px 0px 0px 32px;
            clip-path: polygon(0% 100%, 0% 0%, 100% 0%, 65% 100%);
            box-sizing: border-box;
            align-items: center;
            display: flex;
            padding: 5px;
            position: absolute;
            .friend_icon{
                width: 40px;
                height: 55px;
            }
            .friend_word{
                padding-right: 30px;
                font-size: 22px;
                font-weight: bold;
                color: var(--text-color-gray2);
            }
        }
        .friend_active{
            background-color: var(--main-bg-color);
            .friend_icon{
                background-image: url("../../assets/img/house/walk_boy.svg");
                background-repeat: no-repeat;
            }
            .friend_word{
                color: var(--text-color-white);
            }
        }
        .room{
            background-color: var(--inactive-bg-color2);
            width: calc(50vw + 5%);
            height: inherit;
            border-radius: 0px 32px 32px 0px;
            clip-path: polygon(0% 100%, 35% 0%, 100% 0%, 100% 100%);
            box-sizing: border-box;
            align-items: center;
            display: flex;
            padding: 5px;
            position: absolute;
            left: calc(50vw - 10%);
            justify-content: flex-end;
            .room_icon{
                width: 30px;
                height: 55px;
            }
            .room_word{
                font-size: 22px;
                font-weight: bold;
                color: var(--text-color-gray2);
            }
        }
        .room_active{
            background-color: var(--main-bg-color);
            .room_icon{
                background-image: url("../../assets/img/house/think_girl.svg");
                background-repeat: no-repeat;
            }
            .room_word{
                color: var(--text-color-white);
            }
        }
    }
    
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import utils from '@/mixins/utils'
import Header from '@/components/organisms/Header.vue'
import HouseFriend from '@/components/organisms/HouseFriend.vue'
import HouseRoom from '@/components/organisms/HouseRoom.vue'
import StatusSettingModal from '@/components/organisms/StatusSettingModal.vue'

import {houseList, houseMate, talk} from '@/mixins/interface'

export type DataType = {
    houseId: string,
    houseName: string,
    houseMode: string,
    houseList: houseList,
    talks: talk[],
    noticeIntervalMinOM: number,
    latestNoticeTimeOM: Date,
    latestNoticeHouseMatesNumOM: number,
}

export default defineComponent({
    name: "House",
    components: {
        Header,
        HouseFriend,
        HouseRoom,
        StatusSettingModal,
    },
    setup(): Record<string, any>{
        const { sendWebsocket, checkNoticePermission } = utils()
        return{
            sendWebsocket,
            checkNoticePermission
        }
    },
    data(): DataType {
        return {
            houseId: "",
            houseName: "",
            houseMode: "friend",
            houseList: {"":{id:"",name:""}},
            talks:[],
            noticeIntervalMinOM: 1,
            latestNoticeTimeOM: new Date(),
            latestNoticeHouseMatesNumOM: 0,
        }
    },
    computed: {
        refs():any {
            return this.$refs;
        },
        isFriendMode():boolean {
            return this.houseMode == "friend";
        },
        isRoomMode():boolean {
            return this.houseMode == "room";
        },
        noticeIntervalMSecOM():number {
            return this.noticeIntervalMinOM * 60 * 1000; 
        },
        

    },
    mounted : function(){
        // 家一覧取得
        this.$http.get("/api/myhouses/" + this.$store.state.userId + "/").then((response)=>{
            this.setHouseList(response.data);
            this.setHouseInfo();
            this.getHouseInfo();
            this.setWebSocketAction();
            this.requestTalks();
        });
    },
    methods: {
        checkStatus():void{
            // ステータスを確認し、意思表示有効期間が過ぎていたら、ステータスを教えてもらう。
            if(new Date(this.$store.state.houseMates[this.$store.state.userId].statusValidDateTime) < new Date()){
                this.refs.statusSettingModal.openModal();
            }
        },
        setHouseList(houses:any[]):void{
            const data:houseList = {};
            for (const key in houses) {
                data[houses[key].id] = {
                    id: houses[key].id,
                    name: houses[key].houseName,
                }
            }
            this.houseList = data;
        },
        setHouseInfo():void{
            if(!this.$store.state.houseId){
                // 選択されたものがなければlistから取得する
                // 任意のもので良いのでobjectで良い
                const selectedHouseId = localStorage.getItem("houseId") || Object.entries(this.houseList)[0][1].id;
                this.$store.dispatch("setHouseId", selectedHouseId);
                this.houseName = this.houseList[selectedHouseId].name;
            }else{
                this.houseName = this.houseList[this.$store.state.houseId].name;
            }
        },
        async getHouseInfo():Promise<void>{
            if(this.$store.state.houseId){
                await this.$store.dispatch("getHouseUsers");
            }
        },
        async talkScrollEnd() {
            await (this.isFriendMode == true)
            this.refs.houseFriend.talkScrollEnd();
        },

        setWebSocketAction():void{
            const socket = this.$store.state.websocket;
            if(!socket)return;
            socket.onmessage = (e)=>{
                const data = JSON.parse(e.data);
                this.webSocketOnmessage(data);
            }
            this.$store.dispatch("setWebsocket", socket);
        },
        webSocketOnmessage(data:any):void{
            // websocketからのコマンドを捌く
            if(data.type == "talk"){
                this.addTalk(data);
            }
            if(data.type == "requestTalks"){
                this.sendTalks(data);
            }
            if(data.type == "receiveTalks"){
                this.receiveTalks(data);
            }
            if(data.type == "someOneChangeStatus"){
                // 画面更新
                this.$store.dispatch("getHouseUsers");
            }
        },
        addTalk(data:any):void{
            this.talks.push({
                message: data.message,
                userId: data.userId,
                userName: data.userName,
                date: data.date,
                time: data.time,
            });
            this.talkScrollEnd();
        },
        requestTalks():void{
            // 描画直後に一番情報持っている人に情報をもらう
            this.sendWebsocket(JSON.stringify({
                "type": "requestTalks",
                "houseId": this.$store.state.houseId
            }));
        },
        sendTalks(data:any):void{
            // 自分の持っているデータを送ってあげる
            // 会話ログが負担になったら長さで消すかも
            this.sendWebsocket(JSON.stringify({
                "type": "sendTalks",
                "houseId": this.$store.state.houseId,
                "target": data.userId,
                "talks": this.talks
            }));
        },
        receiveTalks(data:any):void{
            // 自分の持っている情報よりも大きければ採用。
            if(this.talks.length < data.talks.length ){
                this.talks = data.talks;
                this.talkScrollEnd();
            }
        },
        noticeChangeStatus():void{
            // ステータス変更の周知
            console.log("noticeChangeStatus");
            this.sendWebsocket(JSON.stringify({
                "type": "noticeChangeStatus",
                "houseId": this.$store.state.houseId,
                "status": this.$store.state.userStatus
            }));
        },
    }
})
</script>


