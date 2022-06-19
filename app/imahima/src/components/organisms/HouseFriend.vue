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
                <div v-for="(value) in houseMateListHima" v-bind:key="value.id">
                    <div v-if = "isHouseMateDisplay(value.nowStatus)" class="housemate">
                        <div class="icon_area"><Icon :userId="value.id" /></div>
                        <div>{{value.name}}</div>
                        <div>~{{cutSeconds(value.noticableEndTime)}}</div>
                    </div>
                </div>
                
                <div v-for="(value) in houseMateListMaybe" v-bind:key="value.id">
                    <div v-if = "isHouseMateDisplay(value.nowStatus)" class="housemate">
                        <div class="icon_area"><Icon :userId="value.id" /></div>
                        <div>{{value.name}}</div>
                        <div>{{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}</div>
                    </div>
                </div>
                <div v-for="(value) in houseMateListOngame" v-bind:key="value.id">
                    <div v-if = "isHouseMateDisplay(value.nowStatus)" class="housemate">
                        <div class="icon_area"><Icon :userId="value.id" /></div>
                        <div>{{value.name}}</div>
                        <div>{{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}</div>
                    </div>
                </div>
                <div v-for="(value) in houseMateListBusy" v-bind:key="value.id">
                    <div v-if = "isHouseMateDisplay(value.nowStatus)" class="housemate">
                        <div class="icon_area"><Icon :userId="value.id" /></div>
                        <div>{{value.name}}</div>
                        <div v-if="isDisplayTime(value.noticableStartTime,value.noticableEndTime)">
                            {{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}
                        </div>
                        <div v-else>ヒマなし</div>
                    </div>
                </div>
            </div>
        </div>
        <!-- 今の気分 -->
        <div class="mt-4 feeling">
            <div class="feeling_header" @click="changeFeelingDisplay">
                <div class="feeling_icon"></div>
                <div class="feeling_word">今の気分</div>
            </div>
            <div v-if="feelingDisplay" class="feeling_content pt-3 pb-3">
                <div v-for="(value) in feelings" v-bind:key="value.gameId">
                    <div class="game mb-3">
                        <div class="gameName_area">{{value.gameName}}</div>
                        <div class="user_area">
                            <div v-for="(val) in value.userIds" v-bind:key="val.id">
                                <div class="icon_area"><Icon :userId="val" :hideStatus="true"/></div>
                            </div>
                        </div>
                        <Switch v-model:value="value.choice" :switchId="value.gameId" @change="changeGameChoice(value)"/>
                    </div>
                    <div class="detail m-3 pb-3" v-if="value.detailTypes.length > 0">
                        <div class="detail_arrow"></div>
                        <div v-for="(val) in value.detailTypes" v-bind:key="val.gameId">
                            <div class="detail_content mb-2">
                                <div class="left">{{val.leftName}}</div>
                                <div class="center"><vue-slider v-model="val.choice" :min="0" :max="2" :interval="1" :adsorb="true" :process="false" :tooltip="'none'" @change="changeGameDetailChoice" @mousedown="changeStartGameDetailChoice(val)" @drag-start="changeStartGameDetailChoice(val)"></vue-slider></div>
                                <div class="right">{{val.rightName}}</div>
                            </div>
                            <div class="detail_content mb-4">
                                <div class="detail_user">
                                    <div v-for="(userChoice) in val.userIds" v-bind:key="userChoice.userId">
                                        <div v-if="userChoice.choice == 0" class="icon_area">
                                            <Icon :userId="userChoice.userId" :hideStatus="true"/>
                                        </div>
                                    </div>
                                </div>
                                <div class="detail_user">
                                    <div v-for="(userChoice) in val.userIds" v-bind:key="userChoice.userId">
                                        <div v-if="userChoice.choice == 1" class="icon_area">
                                            <Icon :userId="userChoice.userId" :hideStatus="true"/>
                                        </div>
                                    </div>
                                </div>
                                <div class="detail_user">
                                    <div v-for="(userChoice) in val.userIds" v-bind:key="userChoice.userId">
                                        <div v-if="userChoice.choice == 2" class="icon_area">
                                            <Icon :userId="userChoice.userId" :hideStatus="true"/>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="feeling_content_close" @click="changeFeelingDisplay">
                <div class= "handle"></div>
            </div>
        </div>
        <!-- 雑談 -->
        <div class="mt-4 talk">
            <div class="talk_header">
                <div class="talk_word">雑談</div>
                <div class="talk_icon"></div>
            </div>
            <div class="talk_content">
                <div class="talk_field" id="talk_field">
                    <div v-for="(value,index) in talks" v-bind:key="index">
                        <div v-if="checkDisplayDate(index)" class="mt-2 mb-2 date_field">{{value.date}}</div>
                        <div v-if="value.userId != this.$store.state.userId" class="one_field">
                            <div class="icon_area"><Icon :userId="value.userId" /></div>
                            <div class="msg_field">
                                <div class="info_field">
                                    <div class="name">{{value.userName}}</div>
                                    <div class="time">{{value.time}}</div>
                                </div>
                                <div class="message">{{value.message}}</div>
                            </div>
                        </div>
                        <div v-else class="one_field my_talk">
                            <div class="msg_field">
                                <div class="info_field">
                                    <div class="time">{{value.time}}</div>
                                    <div class="name">{{value.userName}}</div>
                                    
                                </div>
                                <div class="message">{{value.message}}</div>
                            </div>
                            <div class="icon_area"><Icon :userId="value.userId" /></div>
                        </div>
                    </div>
                    <div class="mt-3 blank_content" />
                </div>
                <input type="text" v-model="inputText" v-on:keyup.enter="sendTalk" class="talk_input" placeholder="話す">
            </div>
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
            overflow-x: auto;
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
    .feeling{
        width: 90%;
        margin: 0 auto;
        .feeling_header{
            height: 40px;
            background-color: var(--main-bg-color);
            clip-path: polygon(0% 100%, 0% 90%, 20% 90%, 35% 0%, 65% 0%, 
80% 90%,100% 90%,100% 100%);
            display: flex;
            align-items: center;
            justify-content: center;

            .feeling_word{
                color: var(--text-color-white);
                font-size: 18px;
                font-weight: bold;
            }
            .feeling_icon{
                position: absolute;
                background-position-y: center;
                left: calc(45% - 50px);
                width: 30px;
                height: 30px;
                background-image: url("../../assets/img/house/friend/feeling.svg");
                background-repeat: no-repeat;
                background-size: contain;
            }
            
        }
        .feeling_content{
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
            top: -1px;
            position: relative;
            .game{
                display: flex;
                justify-content: space-evenly;
                align-items: center;
                align-content: center;
                font-size: 15px;
                font-weight: bold;

                .gameName_area{
                    width: 120px;
                    text-align: left;
                }

                .user_area{
                    display: flex;
                    align-items: center;
                    height: 35px;
                    width: 30%;
                    background: white;
                    border-radius: var(--content-border-radius);
                    padding-left: 10px;
                    padding-right: 10px;
                    overflow: auto;
                    
                    .icon_area{
                        width: 25px;
                        height: 25px;
                        margin: 2px;
                    }
                }
            }

            .detail{
                background: rgba(246,246,246,1);
                border-radius: var(--content-border-radius);
                .detail_arrow{
                    background: rgba(246,246,246,1);
                    width: 50px;
                    height: 15px;
                    position: relative;
                    top: -14px;
                    left: 10px;
                    clip-path: polygon(0% 100%, 50% 0%, 100% 100%);
                }
                .detail_content{
                    display: flex;
                    justify-content: space-evenly;
                    align-content: center;
                    font-size: 13px;
                    font-weight: bold;
                    .left{
                        text-align: right;
                        width: 30%;
                        margin-right: 15px;
                    }
                    .right{
                        text-align: left;
                        width: 30%;
                        margin-left: 15px;
                    }
                    .center{
                        width: 30%;
                    }
                    .vue-slider-dot-handle{
                        background: var(--main-bg-color);
                    }
                    .detail_user{
                        display: flex;
                        min-height: 35px;
                        width: 30%;
                        background: white;
                        border-radius: var(--content-border-radius);
                        flex-wrap: wrap;
                        .icon_area{
                            width: 25px;
                            height: 25px;
                            margin: 2px;
                        }
                    }
                }
            }
        }
        .feeling_content_close{
            background-color: var(--main-bg-color);
            border-radius: 0px 0px 8px 8px;
            top: -1px;
            position: relative;
            height: 10px;
            display: flex;
            align-items: center;
            .handle{
                background-color: var(--content-bg-color);
                width: 25px;
                height: 3px;
                border-radius: 3px;
                margin: 0 auto;
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
            height: 260px;
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
            top: -1px;
            position: relative;
            .talk_field{
                width: 100%;
                height: calc(100% - 50px);
                overflow-y: auto;
                .date_field{
                    background-color: var(--main-bg-color);
                    border-radius: 10px;
                    width: 130px;
                    margin: 0 auto;
                    text-align: center;
                    color: var(--text-color-white);
                    font-size: 14px;
                }
                .one_field{
                    display: flex;
                    padding: 5px;
                    margin-bottom: 10px;
                    .icon_area{
                        height:40px;
                        width:40px;
                    }
                    .msg_field{
                        width: calc(75% - 35px);
                        padding-left: 10px;
                        .info_field{
                            display: flex;
                            justify-content: space-between;
                            font-size: 10px;
                        }
                        .message{
                            background-color: var(--inactive-bg-color2);
                            border-radius: 10px;
                            padding-left: 10px;
                            text-align: left;
                            font-size: 13px;
                            overflow-wrap: anywhere;
                            padding: 3px 10px;
                        }
                    }
                }
                .my_talk{
                    justify-content: flex-end;
                    .icon_area{
                        margin-left: 10px;
                    }
                }
                
            }
            .talk_input{
                width: 100%;
                height: 50px;
                border: none;
                padding-left: 10px;
                border-radius: 0 0 8px 8px;
            }
        }
    }

}
</style>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import utils from '@/mixins/utils'
import Icon from '@/components/molecules/Icon.vue'
import Switch from '@/components/molecules/Switch.vue'
import {houseMates, houseMate, talk} from '@/mixins/interface'

interface userChoices {userId:string, choice:number }
interface detailType {gameDetailTypeId:string, gameDetailTypeName:string, gameId:string, leftName:string, rightName:string, choice:number, userIds: userChoices[] }
interface feeling {gameId:string, gameName:string, choice:boolean, userIds: string[], detailTypes:detailType[]}
export type DataType = {
    friendMode: string,
    feelingDisplay: boolean,
    feelings: feeling[],
    changingDetail: detailType | null,
    inputText: string,
}

export default defineComponent({
    name: "HouseFriend",
    components: {
        Icon,
        Switch,
    },
    setup(): Record<string, any>{
        const { sortTime,cutSeconds, sendWebsocket } = utils()
        return{
            sortTime,
            cutSeconds,
            sendWebsocket
        }
    },
    props: {
      talks: Array as PropType<talk[]>,
    },
    data(): DataType {
        return {
            friendMode: "hima",
            feelingDisplay: false,
            feelings: [],
            changingDetail:null,
            inputText: "",
        }
    },
    computed: {
        isHimaMode():boolean {
            return this.friendMode == "hima";
        },
        isMaybeMode():boolean {
            return this.friendMode == "maybe";
        },
        houseMateListHima():houseMate[] {
            return this.getHouseMateList("hima");
        },
        houseMateListMaybe():houseMate[] {
            return this.getHouseMateList("maybe");
        },
        houseMateListBusy():houseMate[] {
            return this.getHouseMateList("busy");
        },
        houseMateListOngame():houseMate[] {
            return this.getHouseMateList("ongame");
        },


    },
    mounted: function():void{
        this.getFeelings();
    },
    methods: {
        initial(){
            this.getFeelings();
        },
        isHouseMateDisplay(nowStatus:string):boolean {
            if(nowStatus == "hima"){
                return this.isHimaMode;
            }else{
                return this.isMaybeMode;
            }
        },
        sendTalk():void{
            if(!this.inputText){
                return
            }
            this.sendWebsocket(JSON.stringify({
                "type": "talk",
                "houseId": this.$store.state.houseId,
                "message": this.inputText
            }));
            this.inputText = "";
            this.talkScrollEnd();
        },
        checkDisplayDate(index:number):boolean{
            if(!this.talks){
                return false;
            }

            if(index == 0){
                return true;
            }

            const currentData:talk = this.talks[index];
            const lastData:talk = this.talks[index-1];
            if(currentData.date != lastData.date){
                return true;
            }
            return false;
        },
        changeFeelingDisplay(){
            this.feelingDisplay = !this.feelingDisplay;
        },
        async getFeelings():Promise<void> {
            if(!this.$store.state.houseId){
                return
            }
            const feelings = await this.$http.get("/api/feelings/" + this.$store.state.houseId + "/");
            const receiveData = feelings.data
            const data:feeling[] = [];
            for (const key in receiveData) {
                const gameVal = receiveData[key];
                const detailTypes:detailType[] = [];
                for (const detailKey in gameVal.gameDetails) {
                    const detailVal = gameVal.gameDetails[detailKey];
                    const myDetail = detailVal.gameDetailUsers.find((user:userChoices) => user.userId == this.$store.state.userId);
                    let myDetailChoice = 1;
                    if(myDetail){
                        myDetailChoice = myDetail.choice;
                    }
                    detailTypes.push({
                        gameDetailTypeId: detailVal.id,
                        gameDetailTypeName: detailVal.gameDetailTypeName,
                        gameId: gameVal.id,
                        leftName: detailVal.leftName,
                        rightName: detailVal.rightName,
                        choice: myDetailChoice,
                        userIds: detailVal.gameDetailUsers
                    });
                }
                const choice = gameVal.gameUsers.findIndex((user:string) => user == this.$store.state.userId) > -1;
                data.push({
                    gameId: gameVal.id,
                    gameName: gameVal.gameName,
                    choice: choice,
                    userIds: gameVal.gameUsers,
                    detailTypes: detailTypes
                });
            }
            this.feelings = data;
        },
        changeGameChoice(val:feeling){
            if(val.choice){
                // ONにしたとき
                const saveData:Record<string, unknown> = {
                    "houseId": this.$store.state.houseId,
                    "userId": this.$store.state.userId,
                    "gameId": val.gameId,
                    "gameDetailTypeId": null,
                    "choice": 1,
                };
                this.saveFeeling(saveData);

                // 詳細をdefault値で登録
                for(const key in val.detailTypes){
                    const saveData:Record<string, unknown> = {
                        "houseId": this.$store.state.houseId,
                        "userId": this.$store.state.userId,
                        "gameId": val.gameId,
                        "gameDetailTypeId": val.detailTypes[key].gameDetailTypeId,
                        "choice": 1,
                    };
                    this.saveFeeling(saveData);
                }
            }else{
                // OFFにしたとき
                // 詳細含めて削除
                this.deleteFeeling(val.gameId);
            }
        },
        changeStartGameDetailChoice(val:detailType){
            // changeイベントが値変更前になってしまうので、変更対象のデータを保持する
            this.changingDetail = val;
        },
        changeGameDetailChoice(val:number){
            if(!this.changingDetail){
                return
            }
            const saveData:Record<string, unknown> = {
                "houseId": this.$store.state.houseId,
                "userId": this.$store.state.userId,
                "gameId": this.changingDetail.gameId,
                "gameDetailTypeId": this.changingDetail.gameDetailTypeId,
                "choice": val,
            };
            this.saveFeeling(saveData);
        },
        saveFeeling(data:any):void{
            this.$http.post("/api/upsert_feelings/", data)
            .then((response)=>{
                // イベント変更の共有
                this.sendChangeFeeling();
            });
        },
        deleteFeeling(gameId:string):void{
            if(!gameId){
                return
            }
            this.$http.delete("/api/delete_feelings/" + this.$store.state.houseId + "/" + this.$store.state.userId + "/"
                + gameId + "/")
            .then((response)=>{
                // イベント変更の共有
                this.sendChangeFeeling();
            });
        },
        sendChangeFeeling():void{
            // 画面更新
            this.sendWebsocket(JSON.stringify({
                "type": "noticeChangeFeeling",
                "houseId": this.$store.state.houseId
            }));
            this.getFeelings();
        },
        talkScrollEnd():void{
            const target = document.getElementById("talk_field");
            if(!target) return;
            target.scrollTop = target.scrollHeight;
        },
        getHouseMateList(status:string):houseMate[]{
            // 計算量を減らすためにfilterで母数を減らす
            // ソート順 ステータス＞ヒマ終了時間＞ヒマ開始時間
            const houseMates:houseMates = this.$store.state.houseMates;
            const houseMateList:houseMate[] = Object.values(houseMates).filter((houseMate:houseMate)=>houseMate.nowStatus == status)
            .sort((a:houseMate, b:houseMate)=>{
                // 時間
                const end = this.sortTime(a.noticableEndTime, b.noticableEndTime);
                if(end == 0){
                    return this.sortTime(a.noticableStartTime, b.noticableStartTime);
                }else{
                    return end;
                }
            });
            return houseMateList;
        },
        isDisplayTime(startTime:string,endTime:string):boolean{
            if(this.cutSeconds(startTime) == '00:00' && this.cutSeconds(endTime)=='24:00'){
                return false
            }else{
                return true
            }
        },
    }
})
</script>


