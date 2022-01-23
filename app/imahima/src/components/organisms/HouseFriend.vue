<template>
    <div class="container house_friend_container">
        <!-- 住民一覧 -->
        <div class="friend_list">
            <div class="friend_header">
                <div class="hima" :class={hima_active:isHimaMode} @click="friendMode = 'hima'">
                    <div class="hima_icon"></div>
                    <div class="hima_word">今ヒマ</div>
                </div>
                <div class="maybe" :class={maybe_active:isMaybeMode} @click="friendMode = 'maybe'">
                    <div class="maybe_word">どうせヒマ</div>
                    <div class="maybe_icon"></div>
                </div>
            </div>
            <div class="friend_content">
            <!-- 住民一覧を出す -->
                <div v-for="(value) in houseMateList" v-bind:key="value.id">
                    <div v-if = "isHouseMateDisplay(value.nowStatus)" class="housemate">
                        <div class="icon_area"><Icon :userId="value.id" /></div>
                        <div>{{value.name}}</div>
                        <div>{{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}</div>
                    </div>
                </div>
            </div>
        </div>
        <!-- 雑談 -->
        <div class="mt-4 talk">
            <div class="talk_header">

                <div class="talk_word">雑談</div>
                <div class="talk_icon"></div>
            </div>
            <div class="talk_content"></div>
        </div>
        <!-- 部屋を作るボタン -->
        <div class="mt-4 make_house">
            <button type="button" class="btn btn_primary btn_make_room content_center_inline" @click="makeRoom">
                <div class="make_room_icon"></div>
                <div class="make_room_word">部屋を作る</div>
            </button>
        </div>
    </div>
</template>

<style lang="scss">
.house_friend_container {
    min-height: 100%;
    max-width: 100% !important;
    padding: unset !important;

    .friend_list{
        width: 90%;
        margin: 0 auto;
        .friend_header{
            height: 40px;
            .hima{
                background-color: var(--inactive-bg-color2);
                width: calc(50vw - 3%);
                height: inherit;
                border-radius: 8px 0px 0px 0px;
                clip-path: polygon(0% 100%, 0% 0%, 70% 0%, 100% 100%);
                box-sizing: border-box;
                align-items: center;
                display: flex;
                padding-top: 5px;
                position: absolute;
                border-bottom: 5px solid var(--main-bg-color);
                .hima_icon{
                    width: 55px;
                    height: 40px;
                }
                .hima_word{
                    padding-right: 30px;
                    font-size: 18px;
                    font-weight: bold;
                    color: var(--text-color-gray2);
                }
            }
            .hima_active{
                background-color: var(--main-bg-color);
                .hima_icon{
                    background-image: url("../../assets/img/house/friend/cat.svg");
                    background-repeat: no-repeat;
                }
                .hima_word{
                    color: var(--text-color-white);
                }
            }

            .maybe{
                background-color: var(--inactive-bg-color2);
                width: calc(50vw - 3%);
                height: inherit;
                border-radius: 0px 8px 0px 0px;
                clip-path: polygon(0% 100%, 30% 0%, 100% 0%, 100% 100%);
                box-sizing: border-box;
                align-items: center;
                display: flex;
                padding-top: 5px;
                position: absolute;
                left: calc(50vw - 2%);
                justify-content: flex-end;
                border-bottom: 5px solid var(--main-bg-color);
                .maybe_icon{
                    width: 45px;
                    height: 40px;
                    margin-right: 10px;
                }
                .maybe_word{
                    font-size: 18px;
                    font-weight: bold;
                    color: var(--text-color-gray2);
                    position: absolute;
                    right: 45px;
                }
            }
            .maybe_active{
                background-color: var(--main-bg-color);
                .maybe_icon{
                    background-image: url("../../assets/img/house/friend/read_boy.svg");
                    background-repeat: no-repeat;
                }
                .maybe_word{
                    color: var(--text-color-white);
                }
            }
        }
        .friend_content{
            height: 115px;
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
            padding: 5px;
            display: flex;
            overflow-x: scroll;
            .housemate{
                width: 80px;
                margin-right: 10px;
                font-size: 13px;
                font-weight: bold;
                .icon_area{
                    height:60px;
                    width:60px;
                    margin: 0 auto;
                }
            }   
        }
    }


    .talk{
        width: 90%;
        margin: 0 auto;
        .talk_header{
            height: 40px;
            background-color: var(--main-bg-color);
            clip-path: polygon(0% 100%, 0% 90%, 20% 90%, 35% 0%, 65% 0%, 
80% 90%,100% 90%,100% 100%);
            display: flex;
            align-items: center;
            justify-content: center;

            .talk_word{
                color: var(--text-color-white);
                font-size: 18px;
                font-weight: bold;
            }
            .talk_icon{
                position: absolute;
                width: 115px;
                height: 40px;
                background-image: url("../../assets/img/house/friend/talk.svg");
                background-repeat: no-repeat;
            }
            
        }
        .talk_content{
            height: 20vh;
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
        }
    }

    .make_house{
        width: 90%;
        height: 55px;
        margin: 0 auto;
        .btn_make_room{
            width: 80%;
            height: 55px;
            font-size: 18px;
            font-weight: bold;
            background-position-x: 80%;

            .make_room_icon{
                position: absolute;
                left: 23%;
                width: 46px;
                height: 55px;
                background-image: url("../../assets/img/house/make_room.svg");
            }
        }
    }

}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import utils from '@/mixins/utils'
import Icon from '@/components/molecules/Icon.vue'

interface houseMate {
    id: string,
    name: string,
    icon: string,
    noticableStartTime: string,
    noticableEndTime: string,
    nowStatus: string,
    }
interface houseMates {[key:string]:houseMate}
export type DataType = {
    friendMode: string,
}

export default defineComponent({
    name: "HouseFriend",
    components: {
        Icon,
    },
    setup(): Record<string, any>{
        const { cutSeconds } = utils()
        return{
            cutSeconds
        }
    },
    data(): DataType {
        return {
            friendMode: "hima",
        }
    },
    computed: {
        isHimaMode():boolean {
            return this.friendMode == "hima";
        },
        isMaybeMode():boolean {
            return this.friendMode == "maybe";
        },
        houseMateList():houseMates {
            return this.$store.state.houseMates;
        }

    },
    // mounted : function(){
    // },
    methods: {
        isHouseMateDisplay(nowStatus:string):boolean {
            if(nowStatus == "hima" || nowStatus == "ongame"){
                return this.isHimaMode;
            }else{
                return this.isMaybeMode;
            }
        },
        // cutSeconds(fullTime:string):string{
        //     return fullTime.substring(0,5);
        // }
    }
})
</script>


