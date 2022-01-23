<template>
    <div class="container house_container">
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
        <div v-if="isFriendMode" class="mt-4">
            <HouseFriend />
        </div>
        <div v-else-if="isRoomMode" class="mt-4">
            <HouseRoom />
        </div>
        <div class="m-3 blank_content" />
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
            width: calc(50vw + 7%);
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
            width: calc(50vw + 7%);
            height: inherit;
            border-radius: 0px 32px 32px 0px;
            clip-path: polygon(0% 100%, 35% 0%, 100% 0%, 100% 100%);
            box-sizing: border-box;
            align-items: center;
            display: flex;
            padding: 5px;
            position: absolute;
            left: calc(50vw - 12%);
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
import Header from '../organisms/Header.vue'
import HouseFriend from '@/components/organisms/HouseFriend.vue'
import HouseRoom from '@/components/organisms/HouseRoom.vue'

interface house {id:string,name:string}
interface houseList {[key:string]:house}
export type DataType = {
    houseId: string,
    houseName: string,
    houseMode: string,
    houseList: houseList,
}

export default defineComponent({
    name: "House",
    components: {
        Header,
        HouseFriend,
        HouseRoom,
    },
    data(): DataType {
        return {
            houseId: "",
            houseName: "カメハウスa",
            houseMode: "friend",
            houseList: {"":{id:"",name:""}},
        }
    },
    computed: {
        isFriendMode():boolean {
            return this.houseMode == "friend";
        },
        isRoomMode():boolean {
            return this.houseMode == "room";
        },

    },
    mounted : function(){
        // 家一覧取得
        this.$http.get("/api/myhouses/" + this.$store.state.userId + "/").then((response)=>{
            this.setHouseList(response.data);
            this.setHouseInfo();
            this.getHouseInfo();
        });
    },
    methods: {
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
            }
        },
        async getHouseInfo():Promise<void>{
            if(this.$store.state.houseId){
                this.$store.dispatch("getHouseUsers");
            }
        },
    }
})
</script>


