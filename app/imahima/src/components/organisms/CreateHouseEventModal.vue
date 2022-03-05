<template>
    <div class="container CHEM_container">
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="create_event_modal" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content CHEM_modal">
                        <div class="CHEM_header">
                            <div class="title">
                                <div class="title_icon"></div>
                                <div class="title_word">誘う</div>
                            </div>
                            <div class="turn_back btn_imahima" data-bs-dismiss="modal"></div>
                        </div>
                        <div class="modal-body CHEM_body">
                            <div class="mb-3 d-flex">
                                <input type="text" v-model="eventName" class="eventName_input" :class="errorTitle" placeholder="タイトル">
                            </div>
                            <div class="mb-3">
                                <div class="content_title">概要</div>
                                <div class="CHEM_content">
                                    <div class="m-1 CHEM_inline recruitment_area">
                                        <div class="CHEM_icon recruitment_icon"></div>
                                        <div class="content_subtitle">目標人数</div>
                                        <input type="number" v-model="recruitmentNumbersLower" class="text_input" :class="errorRecruitmentNumbersLower" min="1" step="1" @change="changeRecruitmentNumbersLower">
                                        <div class="suffix">人</div>
                                        <div class="middle">～</div>
                                        <input type="number" v-model="recruitmentNumbersUpper" class="text_input" min="1" step="1" @change="changeRecruitmentNumbersUpper">
                                        <div class="suffix">人</div>
                                    </div>
                                    <div class="m-1 mt-3 CHEM_inline location_area">
                                        <div class="CHEM_icon location_icon"></div>
                                        <div class="content_subtitle">場所</div>
                                        <input type="text" v-model="location" class="text_input" >
                                    </div>
                                    <div class="m-1 mt-3 CHEM_inline date_area">
                                        <div class="CHEM_icon time_icon"></div>
                                        <div class="content_subtitle">開催日時</div>
                                        <datepicker class="vue-datepicker-box" v-model="startDate" :lower-limit="lowerLimitDate" :clearable="true"/>
                                    </div>
                                    <div class="m-1 mt-3 CHEM_inline time_area">
                                        <div class="time_area_weight"></div>
                                        <div class="content_subtitle"></div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="startTime" :key="refreshStartTime" :minute-interval="10" hide-clear-button @change="changeTime('start')"></VueTimepicker>
                                        <div class="middle">～</div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="endTime" :key="refreshEndTime" :minute-interval="10" hide-clear-button @change="changeTime('end')"></VueTimepicker>
                                    </div>
                                    <div class="m-1 mt-3 CHEM_inline category_area">
                                        <div class="CHEM_icon category_icon"></div>
                                        <div class="content_subtitle">カテゴリ</div>
                                        <select class="category_select" v-model="selectedCategoryId" >
                                            <option v-for="value in categoryList" v-bind:key="value.id" v-bind:value="value.id">
                                                {{ value.name }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="content_title">詳細</div>
                                <div class="CHEM_content">
                                    <textarea class="detail_input" :class="errorDetail" v-model="detail"/>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="content_title">開催する時の状況</div>
                                <div class="CHEM_content">
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
                            <div class="m-4 create_event">
                                <button type="button" class="btn btn_primary btn_create_event content_center_inline" @click="createEvent">
                                    <div class="create_event_icon"></div>
                                    <div class="create_event_word">この内容で誘う</div>
                                    <div class="create_event_icon_dummy"></div>
                                </button>
                                <div v-if="error" class="err_msg">赤枠の必須項目を入力してください</div>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </div>
        </teleport>
    </div>
</template>

<style lang="scss">
.CHEM_modal{
    max-height: 90%!important;
    border: none!important;
    background-color: revert!important;
    overflow: unset!important;
    .CHEM_header{
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
            .title_icon{
                position: absolute;
                background-position-y: center;
                left: calc(45% - 40px);
                width: 40px;
                height: 40px;
                background-image: url("../../assets/img/house/create_event.svg");
                background-repeat: no-repeat;
                background-size: contain;
                opacity: 80%;
            }
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

    .CHEM_body{
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

        .CHEM_content{
            background-color: rgba(246,246,246,1);
            padding: 10px;
            border-radius: var(--content-border-radius);

            .CHEM_inline{
                display: flex;
                align-items: center;
                .CHEM_icon{
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

        .create_event{
            width: 90%;
            margin: 0 auto;
            text-align-last: center;
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
            .err_msg{
                margin: 10px;
                color: var(--error-color);
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

    error: boolean,
    lowerLimitDate: Date
}

export default defineComponent({
    name: "CreateHouseEventModal",
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

            error: false,

            lowerLimitDate: new Date(),
        }
    },
    computed: {
        houseId():string {
            return this.$store.state.houseId;
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
            if(this.eventName || !this.error){
                return "";
            }else{
                return "error_border"
            }
        },
        errorRecruitmentNumbersLower():string{
            if(this.recruitmentNumbersLower || !this.error){
                return "";
            }else{
                return "error_border"
            }
        },
        errorDetail():string{
            if(this.detail || !this.error){
                return "";
            }else{
                return "error_border"
            }
        },
    },
    methods: {
        openModal():void{
            // データ初期化
            this.initData();
            this.getCategoryList();
            
            // モーダル開く
            const target = document.getElementById('create_event_modal');
            if(!target) return;
            const myModal = new Modal(target);
            if(!myModal) return;
            myModal.show();
        },
        closeModal():void{
            const target = document.getElementById('create_event_modal');
            if(!target) return;
            const myModal = Modal.getInstance(target);
            if(!myModal) return;
            myModal.hide();
        },
        initData():void{
            this.eventName = "";
            this.recruitmentNumbersLower = 1;
            this.recruitmentNumbersUpper = null;
            this.location = "discord";

            const now = new Date();
            
            this.startDate = new Date();
            this.startDate.setHours(0);
            this.startDate.setMinutes(0);
            this.startDate.setSeconds(0);
            this.startDate.setMilliseconds(0);
            this.startTime = now.getHours().toString().padStart(2,'0') + ":" + now.getMinutes().toString().padStart(2,'0');
            this.endTime = (now.getHours()+1).toString().padStart(2,'0') + ":" + now.getMinutes().toString().padStart(2,'0');
            this.detail = "";
            this.error = false;

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
        },
        checkEditing(data:any):boolean{
            const blankHour = data?.HH == "";
            const blankMin = data?.mm == "";
            // 片方だけがブランクの場合は編集中と判断する
            const edited = blankHour == blankMin;
            return !edited;
        },

        
        createEvent():void{
            if(!this.validate()){
                return
            }
            const saveData = {
                houseId : this.$store.state.houseId,
                eventName: this.eventName,
                recruitmentNumbersLower: this.recruitmentNumbersLower,
                recruitmentNumbersUpper: this.recruitmentNumbersUpper,
                location: this.location,
                startDate: this.startDate,
                startTime: this.getDisplayTime(this.startTime),
                endTime: this.getDisplayTime(this.endTime),
                categoryId: this.selectedCategoryId,
                detail: this.detail
            }
            this.saveCreateEvent(saveData);
            this.initData();
            this.closeModal();
        },
        validate():boolean{
            this.error = false;
            let result = true;
            if(!this.eventName){
                result = false;
            }
            if(!this.recruitmentNumbersLower || this.recruitmentNumbersLower < 1){
                result = false;
            }
            if(!this.detail){
                result = false;
            }

            if(!result){
                this.error = true;
            }

            // データトリミング
            this.startDate?.setHours(0);
            this.startDate?.setMinutes(0);
            this.startDate?.setSeconds(0);
            this.startDate?.setMilliseconds(0);

            return result;
        },

        saveCreateEvent(data:any):void{
            this.$http.post("/api/create_event/", data)
            .then((response)=>{
                // イベント作成の通知
                this.sendCreateEvent(response.data);
            });
        },
        sendCreateEvent(data:any):void{
            // 画面更新用と通知用で分けてもいいかもしれない

            // 画面更新
            this.sendWebsocket(JSON.stringify({
                "type": "noticeChangeEvent",
                "houseId": this.$store.state.houseId
            }));

            // 時間ごとの人表示の実装までは固定で。
            const targetUserIds = ["6b2acdfa","ec69970d"];

            // 通知用
            this.sendWebsocket(JSON.stringify({
                "type": "createEvent",
                "houseId": this.$store.state.houseId,
                "eventId": data.id,
                "eventName": data.eventName,
                "categoryId": data.categoryId,
                "targetUserIds": targetUserIds,
            }));
        }
    }
})



</script>


