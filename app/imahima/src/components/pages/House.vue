<template>
    <div class="container house_container" v-on:click="checkStatus">
        <Header />
        <!-- 家タイトル -->
        <div class="mt-2 house_title content_center">
            <div class="weight"></div>
            <select class="house_name" v-model="selectedHouseId" @change="changeHouse">
                <option v-for="value in houseList" v-bind:key="value.id" v-bind:value="value.id">
                    {{ value.name }}
                </option>
            </select>
            <div class="house_setting" @click="openHouseSetting">
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
            <div class="event" :class={event_active:isEventMode} @click="houseMode = 'event'">
                <div class="event_word">誘いを探す</div>
                <div class="event_icon"></div>
            </div>
        </div>
        <!-- 選択メニューによって切り替える予定 -->
        <!-- TODO: 友達に会うは、ヒマじゃない人には見せない。 -->
        <div v-if="isFriendMode" class="mt-4">
            <HouseFriend :talks="talks" ref="houseFriend"/>
        </div>
        <div v-else-if="isEventMode" class="mt-4">
            <HouseEvent ref="houseEvent" />
        </div>
        <div class="mt-4 create_event">
            <button type="button" class="btn btn_primary btn_create_event content_center_inline" @click="openCreateEvent">
                <div class="create_event_icon"></div>
                <div class="create_event_word">誘う</div>
                <div class="create_event_icon_dummy"></div>
            </button>
        </div>
        <div class="mt-3 blank_content" />
        <StatusSettingModal ref="statusSettingModal" @noticeChangeStatus="noticeChangeStatus" />
        <HouseSettingModal ref="houseSettingModal" @changeHouseInfo="changeHouseInfo"/>
        <CreateHouseEventModal ref="createHouseEventModal" />
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
            border: none;
            text-align: center;
            max-width: 65%;
            background-size: 16px 16px;
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
        .event{
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
            .event_icon{
                width: 30px;
                height: 55px;
            }
            .event_word{
                font-size: 22px;
                font-weight: bold;
                color: var(--text-color-gray2);
            }
        }
        .event_active{
            background-color: var(--main-bg-color);
            .event_icon{
                background-image: url("../../assets/img/house/think_girl.svg");
                background-repeat: no-repeat;
            }
            .event_word{
                color: var(--text-color-white);
            }
        }
    }
    .create_event{
        width: 90%;
        height: 55px;
        margin: 0 auto;
        .btn_create_event{
            width: 80%;
            height: 55px;
            font-size: 18px;
            font-weight: bold;
            background-position-x: 88%;

            .create_event_icon{
                position: relative;
                left: 3%;
                width: 46px;
                height: 55px;
                background-image: url("../../assets/img/house/create_event.svg");
            }
            .create_event_icon_dummy{
                width: 46px;
                height: 55px;
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
import HouseEvent from '@/components/organisms/HouseEvent.vue'
import StatusSettingModal from '@/components/organisms/StatusSettingModal.vue'
import HouseSettingModal from '@/components/organisms/HouseSettingModal.vue'
import CreateHouseEventModal from '@/components/organisms/CreateHouseEventModal.vue'

import {houseList, houseMate, talk} from '@/mixins/interface'

export type DataType = {
    selectedHouseId: string,
    houseMode: string,
    houseList: houseList,
    talks: talk[],
    latestNoticeTimeOM: Date,
    latestNoticeHouseMatesNumOM: number,
}

export default defineComponent({
    name: "House",
    components: {
        Header,
        HouseFriend,
        HouseEvent,
        StatusSettingModal,
        HouseSettingModal,
        CreateHouseEventModal,
    },
    setup(): Record<string, any>{
        const { sendWebsocket, queryToString } = utils()
        return{
            sendWebsocket,
            queryToString,
        }
    },
    data(): DataType {
        return {
            selectedHouseId: "",
            houseMode: "friend",
            houseList: {"":{id:"",name:""}},
            talks:[],
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
        isEventMode():boolean {
            return this.houseMode == "event";
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
        openHouseSetting():void{
            this.refs.houseSettingModal.openModal();
        },
        openCreateEvent(e:Event):void{
            e.stopPropagation();
            this.refs.createHouseEventModal.openModal();
        },

        changeHouse(value:any):void{
            // 再読み込み用にlocalstorageへの保存
            this.$store.dispatch("setHouseId", this.selectedHouseId);
            // 雑談のリセット
            this.talks.splice(0);
            // ユーザの入れ替え
            this.getHouseInfo();
            // 雑談の入れ替え
            this.requestTalks();
            // イベントの入れ替え
            this.refs.houseEvent.getEventList();
        },
        getHouseList():void{
            this.$http.get("/api/myhouses/" + this.$store.state.userId + "/").then((response)=>{
                this.setHouseList(response.data);
            });
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
            // storeにあるということは選んでいるので使う
            if(!this.$store.state.houseId){
                // 選択されたものがなければlistから取得する(任意のもので良いのでobjectで良い)
                let selectedHouseId = localStorage.getItem("houseId") || Object.entries(this.houseList)[0][1].id;

                // パラメータがあるならパラメータを使う
                const paramHouseId:string | undefined = this.queryToString(this.$route.query.houseId);
                if(paramHouseId && this.houseList[paramHouseId]){
                    // パラメータは一回使用したら消す
                    const url = new URL(window.location.href);
                    history.replaceState('', '', url.href.replace(/\?.*$/,""));

                    selectedHouseId = paramHouseId;
                }

                this.$store.dispatch("setHouseId", selectedHouseId);
                this.selectedHouseId = selectedHouseId;
            }else{
                this.selectedHouseId = this.$store.state.houseId;
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
        changeHouseInfo():void{
            this.getHouseList()
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
            // houseIdが選択中のものでなければ無関係なので何もしない
            if(data.houseId != this.selectedHouseId){
                return;
            }
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
            if(data.type == "someOneChangeEvent"){
                // 画面更新
                this.refs.houseEvent.getEventList();
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


