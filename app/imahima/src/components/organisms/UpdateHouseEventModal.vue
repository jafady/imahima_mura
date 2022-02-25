<template>
    <div class="container UHEM_container">
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="update_event_modal" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content UHEM_modal">
                        <div class="UHEM_header">
                            <div class="delete_event btn_imahima" v-if="mode=='in'" @click="deleteEvent"></div>
                            <div class="title">
                                <div class="title_word">誘いの詳細</div>
                            </div>
                            <div class="turn_back btn_imahima" data-bs-dismiss="modal"></div>
                        </div>
                        <div class="modal-body UHEM_body">
                            <div class="mb-3 d-flex">
                                <input type="text" v-model="eventName" class="eventName_input" :class="errorTitle" placeholder="タイトル" @change="changeEventName">
                            </div>
                            <div class="mb-3">
                                <div class="content_title">概要</div>
                                <div class="UHEM_content">
                                    <div class="m-1 UHEM_inline recruitment_area">
                                        <div class="UHEM_icon recruitment_icon"></div>
                                        <div class="content_subtitle">目標人数</div>
                                        <input type="number" v-model="recruitmentNumbersLower" class="text_input" :class="errorRecruitmentNumbersLower" min="1" step="1" @change="changeRecruitmentNumbersLower">
                                        <div class="suffix">人</div>
                                        <div class="middle">～</div>
                                        <input type="number" v-model="recruitmentNumbersUpper" class="text_input" min="1" step="1" @change="changeRecruitmentNumbersUpper">
                                        <div class="suffix">人</div>
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline location_area">
                                        <div class="UHEM_icon location_icon"></div>
                                        <div class="content_subtitle">場所</div>
                                        <input type="text" v-model="location" class="text_input" @change="changeLocation">
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline date_area">
                                        <div class="UHEM_icon time_icon"></div>
                                        <div class="content_subtitle">開催日時</div>
                                        <datepicker class="vue-datepicker-box" v-model="startDate" :lower-limit="lowerLimitDate" :clearable="true" @input="changeStartDate"/>
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline time_area">
                                        <div class="time_area_weight"></div>
                                        <div class="content_subtitle"></div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="startTime" :key="refreshStartTime" :minute-interval="10" hide-clear-button @change="changeTime('start')"></VueTimepicker>
                                        <div class="middle">～</div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="endTime" :key="refreshEndTime" :minute-interval="10" hide-clear-button @change="changeTime('end')"></VueTimepicker>
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline category_area">
                                        <div class="UHEM_icon category_icon"></div>
                                        <div class="content_subtitle">カテゴリ</div>
                                        <select class="category_select" v-model="selectedCategoryId" @change="changeSelectedCategoryId">
                                            <option v-for="value in categoryList" v-bind:key="value.id" v-bind:value="value.id">
                                                {{ value.name }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="content_title">詳細</div>
                                <div class="UHEM_content">
                                    <textarea class="detail_input" :class="errorDetail" v-model="detail" @change="changeDetail"/>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="content_title">参加予定の人</div>
                                <div class="UHEM_content">
                                    <div class="members_area d-flex">
                                        <div v-for="userId in userIds" v-bind:key="userId" class="member_area">
                                            <div class="icon_area"><Icon :userId="userId" :hideStatus="true"/></div>
                                            <div class="name_area">{{ getUserName(userId) }}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-3" v-if="mode=='in'">
                                <div class="content_title">開催する時の状況</div>
                                <div class="UHEM_content">
                                    <div class="m-1">
                                        <div class="content_subtitle">予定ではヒマ</div>
                                        <div class="housemate_area">
                                            <div v-for="(value) in houseMateListMaybe" v-bind:key="value.id">
                                                <div class="housemate">
                                                    <div class="icon_area"><Icon :userId="value.id" :hideStatus="true"/></div>
                                                    <div>{{value.name}}</div>
                                                    <div>{{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="m-1 mt-3">
                                        <div class="content_subtitle">ヒマじゃない</div>
                                        <div class="housemate_area">
                                            <div v-for="(value) in houseMateListBusy" v-bind:key="value.id">
                                                <div class="housemate">
                                                    <div class="icon_area"><Icon :userId="value.id" :hideStatus="true"/></div>
                                                    <div>{{value.name}}</div>
                                                    <div>{{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                            </div>


                            <div class="m-4 join_event" v-if="mode=='out'">
                                <button type="button" class="btn btn_primary btn_join_event content_center_inline" @click="joinEvent">
                                    <div class="join_event_icon"></div>
                                    <div class="join_event_word">誘われる</div>
                                    <div class="join_event_icon_dummy"></div>
                                </button>
                            </div>

                            <div class="m-4 leave_event" v-if="mode=='in'">
                                <button type="button" class="btn btn_primary btn_leave_event content_center_inline" @click="leaveEvent">
                                    <div class="leave_event_icon_dummy"></div>
                                    <div class="leave_event_word">抜ける</div>
                                    <div class="leave_event_icon"></div>
                                </button>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </div>
        </teleport>
    </div>
</template>

<style lang="scss">
.UHEM_modal{
    max-height: 90%!important;
    border: none!important;
    background-color: revert!important;
    overflow: unset!important;
    .UHEM_header{
        height: 40px;

        .title{
            height: 40px;
            background-color: var(--main-bg-color);
            clip-path: polygon(0% 100%, 0% 80%, 20% 80%, 35% 0%, 65% 0%, 
    80% 80%,100% 80%,100% 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            .title_word{
                color: var(--text-color-white);
                font-size: 18px;
                font-weight: bold;
            }
        }

        .delete_event{
            position: absolute;
            left: 5%;
            top: -5%;
            width: 45px;
            height: 45px;
            background-image: url("../../assets/img/house/event/delete_event.svg");
            background-repeat: no-repeat;
            background-position-y: 55%;
            background-position-x: 55%;
            background-size: 25px;
            background-color: var(--error-color);
            border-radius: 50%;
        }
        
        .turn_back{
            position: absolute;
            left: 82%;
            top: -5%;
            width: 45px;
            height: 45px;
            background-image: url("../../assets/img/turn_back.svg");
            background-repeat: no-repeat;
            background-position-y: 55%;
            background-position-x: 55%;
            background-size: 25px;
            background-color: var(--main-bg-color);
            border-radius: 50%;
        }
        
    }

    .UHEM_body{
        padding-bottom: 0!important;
        background-color: var(--content-bg-color);

        .content_title{
            text-align: left;
            align-items: center;
            font-size: 21px;
        }
        .eventName_input{
            border: none;
            border-radius: 8px;
            padding-left: 10px;
            width: 80%;
            height: 40px;
            font-size: 18px;
            text-align: center;
            margin: 0 auto;
        }

        .UHEM_content{
            background-color: rgba(246,246,246,1);
            padding: 10px;
            border-radius: var(--content-border-radius);

            .UHEM_inline{
                display: flex;
                align-items: center;
                .UHEM_icon{
                    width: 16px;
                    height: 25px;
                    margin-right: 10px;
                    background-repeat: no-repeat;
                    background-size: contain;
                    background-position: center;
                }
                .content_subtitle{
                    font-size: 15px;
                    margin-right: 20px;
                    width: 60px;
                }
                .text_input{
                    border: none;
                    border-radius: 8px;
                    padding-left: 10px;
                    height: 40px;
                    font-size: 16px;
                }
                .suffix{
                    margin-left: 5px;
                }
                .middle{
                    margin: 0 10px;
                }
            }

            .recruitment_area{
                .recruitment_icon{
                    background-image: url("../../assets/img/house/event/boy.svg");
                }
                .text_input{
                    width: 40px;
                }
            }
            .location_area{
                .location_icon{
                    background-image: url("../../assets/img/house/event/pin.svg");
                }
                .text_input{
                    width: 165px;
                }
            }
            .date_area{
                .time_icon{
                    background-image: url("../../assets/img/house/event/hourglass.svg");
                }
                .vue-datepicker-box{
                    width: 120px;
                    height: 40px;
                    border: none;
                    border-radius: 8px;
                    font-family: "游ゴシック";
                    padding: 7px;
                }
            }
            .time_area{
                .time_area_weight{
                    width: 16px;
                    margin-right: 10px;
                }
                .time{
                    width: 75px;
                    height: 40px;
                    border: none;
                    border-radius: 8px;
                    font-family: "游ゴシック";
                }
            }
            .category_area{
                .category_icon{
                    background-image: url("../../assets/img/house/event/books.svg");
                }
                .category_select{
                    width: 165px;
                    height: 40px;
                    border-radius: 8px;
                    border: none;
                    background-color: white;
                    background-position-x: 99%;
                    padding: 7px;
                    appearance: none;
                }
            }

            .detail_input{
                width: 100%;
                height: 250px;
                min-height: 100px;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }

            .members_area{
                overflow-x: auto;
                text-align: center;
                .member_area{
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

            .housemate_area{
                display: flex;
                overflow-x: auto;
                text-align: center;
                min-height: 100px;
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

        .join_event{
            width: 90%;
            margin: 0 auto;
            text-align-last: center;
            .btn_join_event{
                width: 80%;
                height: 55px;
                font-size: 18px;
                font-weight: bold;
                background-position-x: 88%;

                .join_event_icon{
                    position: relative;
                    left: 3%;
                    width: 46px;
                    height: 55px;
                    background-image: url("../../assets/img/house/create_event.svg");
                }
                .join_event_icon_dummy{
                    width: 46px;
                    height: 55px;
                }
            }
            .err_msg{
                margin: 10px;
                color: var(--error-color);
            }
        }

        .leave_event{
            width: 90%;
            margin: 0 auto;
            text-align-last: center;
            .btn_leave_event{
                width: 80%;
                height: 55px;
                font-size: 18px;
                font-weight: bold;
                background-position-x: 15%;
                background-image: url("../../assets/img/triangle_left.svg");
                

                .leave_event_icon{
                    position: relative;
                    right: 3%;
                    width: 46px;
                    height: 55px;
                    background-image: url("../../assets/img/house/event/leave_event.svg");
                    background-repeat: no-repeat;
                    background-position-y: center;
                }
                .leave_event_icon_dummy{
                    width: 46px;
                    height: 55px;
                }
            }
        }

    }
    
}
.vue__time-picker{
    width:fit-content !important;
}

</style>

<script lang="ts">
import { defineComponent } from 'vue'
import { houseMates, houseMate } from '@/mixins/interface'
import utils from '@/mixins/utils'
import { Modal } from 'bootstrap'
import Icon from '@/components/molecules/Icon.vue'

interface category {id:string,name:string}

export type DataType = {
    eventId: string,
    eventName: string,
    recruitmentNumbersLower: number,
    recruitmentNumbersUpper: number|null,
    location: string,
    startDate: Date | null,
    startTime: string | null,
    endTime: string | null,
    refreshStartTime: number,
    refreshEndTime: number,
    selectedCategoryId: string,
    categoryList: category[],

    detail: string,

    userIds: string[],

    lowerLimitDate: Date
}

export default defineComponent({
    name: "UpdateHouseEventModal",
    components: {
        Icon,
    },
    setup(): Record<string, any>{
        const { sortTime,cutSeconds, sendWebsocket,getDisplayTime } = utils()
        return{
            sortTime,
            cutSeconds,
            sendWebsocket,
            getDisplayTime
        }
    },
    data(): DataType {
        return{
            eventId: "",
            eventName: "",
            recruitmentNumbersLower: 1,
            recruitmentNumbersUpper: null,
            location: "discord",
            startDate: new Date(),
            startTime: null,
            endTime: null,
            refreshStartTime: 1,
            refreshEndTime: 1,
            selectedCategoryId: "",
            categoryList:[],

            detail: "",

            userIds: [],

            lowerLimitDate: new Date(),
        }
    },
    computed: {
        houseId():string {
            return this.$store.state.houseId;
        },
        mode():string{
            if(this.userIds.includes(this.$store.state.userId)){
                return "in"
            }else{
                return "out"
            }
        },

        houseMates():houseMates {
            return this.$store.state.houseMates;
        },
        houseMateListMaybe():houseMate[] {
            return this.getHouseMateList("maybe");
        },
        houseMateListBusy():houseMate[] {
            return this.getHouseMateList("busy");
        },

        errorTitle():string{
            if(this.eventName){
                return "";
            }else{
                return "error_border"
            }
        },
        errorRecruitmentNumbersLower():string{
            if(this.recruitmentNumbersLower){
                return "";
            }else{
                return "error_border"
            }
        },
        errorDetail():string{
            if(this.detail){
                return "";
            }else{
                return "error_border"
            }
        },
    },
    watch: {
        startDate: function(oldVal,newVal):void {
            this.startDate?.setHours(0);
            this.startDate?.setMinutes(0);
            this.startDate?.setSeconds(0);
            this.startDate?.setMilliseconds(0);
            const saveData:Record<string, unknown> = {};
            saveData["startDate"] = this.startDate;
            this.saveUpdateEvent(saveData);
        }
    },
    methods: {
        openModal(eventId:string):void{
            if(!eventId){
                return;
            }
            this.eventId = eventId;
            // データ初期化
            this.getCategoryList();
            this.initData();
            
            // モーダル開く
            const target = document.getElementById('update_event_modal');
            if(!target) return;
            const myModal = new Modal(target);
            if(!myModal) return;
            myModal.show();
        },
        closeModal():void{
            const target = document.getElementById('update_event_modal');
            if(!target) return;
            const myModal = Modal.getInstance(target);
            if(!myModal) return;
            myModal.hide();
        },
        async initData():Promise<void>{
            const eventRes = await this.$http.get("/api/event_info/" + this.eventId + "/");
            const targetData = eventRes.data[0];

            this.eventName = targetData.eventName;
            this.recruitmentNumbersLower = targetData.recruitmentNumbersLower;
            this.recruitmentNumbersUpper = targetData.recruitmentNumbersUpper;
            this.location = targetData.location;

            this.startDate = targetData.startDateAtJp? new Date(targetData.startDateAtJp):null;
            this.startTime = targetData.startTime;
            this.endTime = targetData.endTime;
            this.selectedCategoryId = targetData.categoryId;
            this.detail = targetData.detail;
            this.userIds = targetData.userIds;

            this.refreshStartTime *= -1;
            this.refreshEndTime *= -1;
        },
        
        async getCategoryList():Promise<void>{
            const categoryRes = await this.$http.get("/api/categorys/");
            const data = [];
            for (const key in categoryRes.data) {
                if(categoryRes.data[key].categoryName == "その他"){
                    this.selectedCategoryId = categoryRes.data[key].id;
                }
                data.push({
                    id: categoryRes.data[key].id,
                    name: categoryRes.data[key].categoryName,
                });
            }
            this.categoryList=data;
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
        getUserName(userId:string):string{
            return this.$store.state.houseMates[userId].name;
        },

        // 変更
        changeEventName():void{
            if(!this.eventName){
                return
            }
            const saveData:Record<string, unknown> = {};
            saveData["eventName"] = this.eventName;
            this.saveUpdateEvent(saveData);
        },
        changeLocation():void{
            const saveData:Record<string, unknown> = {};
            saveData["location"] = this.location;
            this.saveUpdateEvent(saveData);
        },
        changeStartDate():void{
            this.startDate?.setHours(0);
            this.startDate?.setMinutes(0);
            this.startDate?.setSeconds(0);
            this.startDate?.setMilliseconds(0);
            const saveData:Record<string, unknown> = {};
            saveData["startDate"] = this.startDate;
            this.saveUpdateEvent(saveData);
        },
        changeSelectedCategoryId():void{
            const saveData:Record<string, unknown> = {};
            saveData["categoryId"] = this.selectedCategoryId;
            this.saveUpdateEvent(saveData);
        },
        changeDetail():void{
            if(!this.detail){
                return
            }
            const saveData:Record<string, unknown> = {};
            saveData["detail"] = this.detail;
            this.saveUpdateEvent(saveData);
        },
        changeRecruitmentNumbersLower():void{
            // 最小値チェック
            if(this.recruitmentNumbersLower < 1){
                this.recruitmentNumbersLower = 1;
            }
            // 整数チェック
            this.recruitmentNumbersLower = Math.round(this.recruitmentNumbersLower);

            // 大きさチェック
            if(this.recruitmentNumbersUpper && this.recruitmentNumbersLower > this.recruitmentNumbersUpper){
                this.recruitmentNumbersUpper = this.recruitmentNumbersLower;
            }

            const saveData:Record<string, unknown> = {};
            saveData["recruitmentNumbersLower"] = this.recruitmentNumbersLower;
            saveData["recruitmentNumbersUpper"] = this.recruitmentNumbersUpper;
            this.saveUpdateEvent(saveData);
        },
        changeRecruitmentNumbersUpper():void{
            if(!this.recruitmentNumbersUpper){
                return
            }
            // 最小値チェック
            if(this.recruitmentNumbersUpper < 1){
                this.recruitmentNumbersUpper = 1;
            }
            // 整数チェック
            this.recruitmentNumbersUpper = Math.round(this.recruitmentNumbersUpper);

            // 大きさチェック
            if(this.recruitmentNumbersLower > this.recruitmentNumbersUpper){
                this.recruitmentNumbersLower = this.recruitmentNumbersUpper;
            }

            const saveData:Record<string, unknown> = {};
            saveData["recruitmentNumbersLower"] = this.recruitmentNumbersLower;
            saveData["recruitmentNumbersUpper"] = this.recruitmentNumbersUpper;
            this.saveUpdateEvent(saveData);
        },
        changeTime(mode:string):void{
            // チェック対象かどうかの確認
            if(this.checkEditing(this.startTime) || this.checkEditing(this.endTime)){
                return;
            }

            // データの整合性調整
            const editedStartTime = this.getDisplayTime(this.startTime);
            let editedEndTime = this.getDisplayTime(this.endTime);
            if (editedStartTime > editedEndTime){
                if(mode == "start"){
                    this.endTime = editedStartTime;
                    this.refreshEndTime *= -1;
                }else{
                    this.startTime = editedEndTime;
                    this.refreshStartTime *= -1;
                }
            }

            const saveData:Record<string, unknown> = {};
            saveData["startTime"] = this.startTime;
            saveData["endTime"] = this.endTime;
            this.saveUpdateEvent(saveData);
        },
        checkEditing(data:any):boolean{
            const blankHour = data?.HH == "";
            const blankMin = data?.mm == "";
            // 片方だけがブランクの場合は編集中と判断する
            const edited = blankHour == blankMin;
            return !edited;
        },


        deleteEvent():void{
            this.$http.delete("/api/delete_event/" + this.eventId + "/")
            .then((response)=>{
                // イベント情報再取得
                this.sendUpdateEvent();
                this.closeModal();
            });
        },
        joinEvent():void{
            const data = {
                eventId: this.eventId,
                userId: this.$store.state.userId
            }
            this.$http.post("/api/join_event/", data)
            .then((response)=>{
                // イベント情報再取得
                this.initData();
                this.sendUpdateEvent();
            });
        },
        leaveEvent():void{
            this.$http.delete("/api/leave_event/" + this.eventId + "/" + this.$store.state.userId + "/")
            .then((response)=>{
                // イベント情報再取得
                this.initData();
                this.sendUpdateEvent();
            });
        },

        
        saveUpdateEvent(data:any):void{
            this.$http.put("/api/update_event/" + this.eventId + "/", data)
            .then((response)=>{
                // イベント変更の共有
                this.sendUpdateEvent();
            });
        },

        sendUpdateEvent():void{
            // 画面更新
            this.sendWebsocket(JSON.stringify({
                "type": "noticeChangeEvent",
                "houseId": this.$store.state.houseId
            }));
        }
    }
})



</script>


