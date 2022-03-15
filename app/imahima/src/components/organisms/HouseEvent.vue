<template>
    <div class="container house_event_container">
        <!-- 検索 -->
        <div class="search_event">
            <div class="event_header">
                <div class="event_header_icon search_icon"></div>
                <div class="event_header_word">検索</div>
            </div>
            <div class="search_content">
                <div class="search_title d-flex">開始日</div>
                <div class="d-inline-flex search_inline">
                    <datepicker class="vue-datepicker-box" v-model="searchStartDate" :clearable="true"/>
                    <VueTimepicker input-class="time" format="HH:mm" v-model="searchStartTime" :key="refreshSearchStartTime" :minute-interval="10"></VueTimepicker>
                    <div class="word">以降</div>
                </div>
            </div>
        </div>
        <!-- 誘い -->
        <div class="insession_event mt-4">
            <div class="event_header">
                <div class="event_header_icon insession_icon"></div>
                <div class="event_header_word">誘い</div>
            </div>
            <div class="insession_content">
                <div class="noevent" v-if="searchedEventList.length < 1">
                    <div>誘いはありません</div>
                    <div>ヒマつぶしに誘ってみましょう</div>
                    <div class="noevent_icon"></div>
                </div>
                <div v-for="(event) in searchedEventList" v-bind:key="event.id" class="event_content">
                    <div class="members">
                        <div v-for="userId in event.userIds" v-bind:key="userId" class="icon_area">
                            <div><Icon :userId="userId" :hideStatus="true"/></div>
                        </div>
                    </div>
                    <div class="info">
                        <div class="title_area"><div class="title">{{event.eventName}}</div></div>
                        <div class="recruitment_area event_info_inline">
                            <div class="event_info_icon recruitment_icon"></div>
                            <div class="number">{{event.recruitmentNumbersLower}}</div>
                            <div class="suffix">人</div>
                            <div class="middle">～</div>
                            <div class="number">{{event.recruitmentNumbersUpper}}</div>
                            <div class="suffix" v-if="event.recruitmentNumbersUpper">人</div>
                        </div>
                        <div class="location_area event_info_inline">
                            <div class="event_info_icon location_icon"></div>
                            <div class="location">{{event.location}}</div>
                        </div>
                        <div class="time_area event_info_inline">
                            <div class="event_info_icon time_icon"></div>
                            <div class="time_info">
                                <div class="day">{{event.displayDay}}</div>
                                <div class="time">{{event.displayTime}}</div>
                            </div>
                            
                        </div>
                    </div> 
                    <button type="button" class="btn btn_imahima btn_detail_event content_center_inline" @click="openDetail($event, event.id)" >
                        <div class="detail_event_word">詳しく</div>
                    </button>
                </div>
            </div>
        </div>
        <UpdateHouseEventModal ref="updateHouseEventModal" />
    </div>
</template>

<style lang="scss">
.house_event_container {
    min-height: 100%;
    max-width: 100% !important;
    padding: unset !important;

    .event_header{
        height: 40px;
        background-color: var(--main-bg-color);
        border-radius: 8px 0px 0px 0px;
        clip-path: polygon(0% 100%, 0% 0%, 45% 0%, 60% 90%, 100% 90%, 100% 100%);
        box-sizing: border-box;
        align-items: center;
        display: flex;
        padding: 5px;
        .event_header_icon{
            width: 42px;
            height: 40px;
            background-repeat: no-repeat;
        }
        .search_icon{
            background-image: url("../../assets/img/house/event/fly_cupid.svg");
        }
        .insession_icon{
            background-image: url("../../assets/img/house/event/sit_cupid.svg");
        }
        .event_header_word{
            padding-right: 30px;
            font-size: 18px;
            font-weight: bold;
            color: var(--text-color-white);
        }

    }

    .search_event{
        width: 90%;
        margin: 0 auto;
        .search_content{
            height: 95px;
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
            padding: 15px;
            .search_title{
                text-align: left;
                align-items: center;
                font-size: 14px;
                font-weight: 500;
            }
            .search_inline{
                align-items: center;
                width: 100%;
                .vue-datepicker-box{
                    width: 120px;
                    height: 40px;
                    border: none;
                    border-radius: 8px;
                    font-family: "游ゴシック";
                    margin-right: 15px;
                    text-align: center;
                }

                .time{
                    width: 80px;
                    height: 40px;
                    border: none;
                    border-radius: 8px;
                    font-family: "游ゴシック";
                    text-align: center;
                }

                .word{
                    margin-left: 10px;
                }
            }
        }
    }
    .insession_event{
        width: 90%;
        margin: 0 auto;
        
        .insession_content{
            min-height: 245px;
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
            padding: 15px;
            display: flex;
            overflow-x: auto;

            .noevent{
                width: 100%;
                height: 100%;
                .noevent_icon{
                    background-image: url("../../assets/img/house/event/look_at_me.svg");
                    background-repeat: no-repeat;
                    background-position: center;
                    background-size: contain;
                    height: 100px;
                    margin-top: 30px;
                }
            }


            .event_content{
                width: 106px;
                margin-right: 10px;

                .members{
                    height: 35px;
                    background-color: var(--inactive-bg-color2);
                    border-radius: 8px;
                    display: flex;
                    overflow-x: auto;
                    .icon_area{
                        width: 25px;
                        height: 25px;
                        margin: 2px;
                    }
                }
                .info{
                    width: inherit;
                    background-color: var(--inactive-bg-color2);
                    border-radius: 8px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                    padding: 5px;
                    .event_info_inline{
                        display: flex;
                        align-items: center;
                        font-size: 10px;
                        margin-top: 5px;
                        .event_info_icon{
                            width: 10px;
                            height: 15px;
                            margin-right: 10px;
                            background-repeat: no-repeat;
                            background-size: contain;
                            background-position: center;
                        }
                        .suffix{
                            margin-left: 5px;
                        }
                        .middle{
                            margin: 0 5px;
                        }
                    }
                    .title_area{
                        overflow: auto;
                        font-size: 13px;
                        font-weight: bold;
                        height: 40px;
                    }
                    .recruitment_area{
                        .recruitment_icon{
                            background-image: url("../../assets/img/house/event/boy.svg");
                        }
                    }
                    .location_area{
                        .location_icon{
                            background-image: url("../../assets/img/house/event/pin.svg");
                        }
                        .location{
                            overflow-x: auto;
                        }
                    }
                    .time_area{
                        height: 30px;
                        .time_icon{
                            background-image: url("../../assets/img/house/event/hourglass.svg");
                        }
                        .time_info{
                            text-align: left;
                        }
                    }
                }
                .btn_detail_event{
                    height: 25px;
                    width: 100%;
                    border-color: var(--main-bg-color);
                    border-width: medium;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    background-color: var(--inactive-bg-color2);
                    .detail_event_word{
                        color: var(--main-bg-color);
                        font-size: 13px;
                        font-weight: bolder;
                    }
                }
            }
        }
    }

}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import Icon from '@/components/molecules/Icon.vue'
import utils from '@/mixins/utils'
import { event } from '@/mixins/interface'
import UpdateHouseEventModal from '@/components/organisms/UpdateHouseEventModal.vue'

export type DataType = {
    eventList: event[],
    searchStartDateTime: Date | null,
    refreshSearchStartTime: number,
}

export default defineComponent({
    name: "HouseEvent",
    components: {
        Icon,
        UpdateHouseEventModal,
    },
    setup(): Record<string, any>{
        const { time2Date } = utils()
        return{
            time2Date,
        }
    },
    data(): DataType {
        return {
            eventList: [],
            searchStartDateTime: null,
            refreshSearchStartTime: 1,
        }
    },
    computed: {
        refs():any {
            return this.$refs;
        },
        searchStartDate:{
            get: function ():Date | null {
                if(!this.searchStartDateTime){
                    return null;
                }
                const val:Date = new Date(this.searchStartDateTime.getTime());
                val.setHours(0);
                val.setMinutes(0);
                val.setSeconds(0);
                return val;
            },
            set: function (newVal:Date):void {
                if(!newVal){
                    this.searchStartDateTime = null;
                    return;
                }
                const val:Date = new Date(newVal.getTime());
                let HH = 0;
                let mm = 0;
                if(this.searchStartTime){
                    HH = parseInt(this.searchStartTime.substring(0,2)) || 0;
                    mm = parseInt(this.searchStartTime.substring(3,5)) || 0;
                    val.setHours(HH);
                    val.setMinutes(mm);
                }
                this.searchStartDateTime = val;
            },
        },
        searchStartTime:{
            get: function ():string | null {
                if(!this.searchStartDateTime){
                    return null;
                }
                return this.searchStartDateTime.getHours().toString().padStart(2,'0') + ":" + this.searchStartDateTime.getMinutes().toString().padStart(2,'0');
            },
            set: function (newVal:string):void {
                if(this.searchStartDate){
                    const val:Date = new Date(this.searchStartDate.getTime());
                    const HH:number = parseInt(newVal.substring(0,2)) || 0;
                    const mm:number = parseInt(newVal.substring(3,5)) || 0;
                    val.setHours(HH);
                    val.setMinutes(mm);
                    this.searchStartDateTime = val;
                }
            },
        },
        // Dateの問題でevent[]をevent[]に入れることができないのでいったんanyで
        searchedEventList():any[] {
            if(!this.searchStartDateTime){
                return this.eventList;
            }
            const searchedEventList:any[] = Object.values(this.eventList).filter((event:any)=>{
                    const targetDay = new Date(event.startDate);
                    const HH = parseInt(event.startTime.substring(0,2)) || 0;
                    const mm = parseInt(event.startTime.substring(3,5)) || 0;
                    targetDay.setHours(HH);
                    targetDay.setMinutes(mm);
                    targetDay.setSeconds(0);
                    if(!this.searchStartDateTime){
                        return true;
                    }
                    if(targetDay.getTime() > this.searchStartDateTime.getTime()){
                        return true;
                    }
                    return false;
                });

            return searchedEventList;
        },
    },
    mounted : function(){
        this.getEventList();
    },
    methods: {
        async getEventList():Promise<void>{
            const eventsRes = await this.$http.get("/api/events/" + this.$store.state.houseId + "/");
            this.setEventList(eventsRes.data);
        },
        setEventList(data:any):void{
            const tempData:event[] = [];
            for (const key in data) {
                const targetData = data[key];
                if(!this.checkEndTime(targetData.startDate, targetData.endTime)){
                    continue;
                }

                tempData.push({
                    id: targetData.id,
                    eventName: targetData.eventName,
                    recruitmentNumbersLower: targetData.recruitmentNumbersLower,
                    recruitmentNumbersUpper: targetData.recruitmentNumbersUpper,
                    location: targetData.location,
                    startDate: targetData.startDate,
                    startTime: targetData.startTime,
                    endTime: targetData.endTime,
                    displayDay: this.setDisplayDay(targetData.startDate),
                    displayTime: this.setDisplayTime(targetData.startDate, targetData.startTime, targetData.endTime),
                    categoryId: targetData.categoryId,
                    detail: targetData.detail,
                    userIds: targetData.userIds
                });
            }
            this.eventList = tempData;
        },
        checkEndTime(startDay:Date, endTime:string):boolean{
            // 終了時間が過ぎているものはイベント自体出さない
            const targetDay = new Date(startDay);
            const now = new Date();
            if(targetDay.getFullYear() == now.getFullYear() 
                && targetDay.getMonth() == now.getMonth() 
                && targetDay.getDate() == now.getDate()){
                    // 今日
                    const endDateTime = this.time2Date(endTime);

                    // 開始時間が過ぎていたら 20分経過のように、経過時間を表示
                    if(endDateTime.getTime() < now.getTime()){
                        return false;
                    }
            }
            return true;
        },
        setDisplayDay(day:Date):string{
            if(!day){
                return "";
            }
            let res = "";
            const targetDay = new Date(day);
            const today = new Date();
            const week = [ "日", "月", "火", "水", "木", "金", "土" ][targetDay.getDay()];
            // 今日であれば出さない
            if(targetDay.getFullYear() == today.getFullYear() 
                && targetDay.getMonth() == today.getMonth() 
                && targetDay.getDate() == today.getDate()){
                    res = "";
                    return res;
            }
            // 過去でも出さない
            if(today.getTime() > targetDay.getTime()){
                res = "";
                return res;
            }

            // 今週であれば今週と表示
            // 来週頭よりも近ければ今週
            const nextWeekDay = new Date();
            let diff = 0;
            // 日曜なら+1
            // 月から土(1~6)なら次の月曜まで
            if(today.getDay() == 0){
                diff = 1;
            }else{
                diff = 7 - today.getDay() + 1;
            }
            nextWeekDay.setDate(nextWeekDay.getDate() + diff);
            nextWeekDay.setHours(0);
            nextWeekDay.setMinutes(0);
            nextWeekDay.setSeconds(0);

            if(targetDay.getTime() < nextWeekDay.getTime()){
                res = "今週(" + week + ")";
            }else{
                 // そのほかは、曜日付きで表示
                res = (targetDay.getMonth() +1) + "/" + targetDay.getDate() + "(" + week + ")";
            }

            return res;
        },
        setDisplayTime(startDay:Date, startTime:string, endTime:string):string{
            let res = "";
            const targetDay = new Date(startDay);
            const now = new Date();
            if(targetDay.getFullYear() == now.getFullYear() 
                && targetDay.getMonth() == now.getMonth() 
                && targetDay.getDate() == now.getDate()){
                    // 今日
                    const startDateTime = this.time2Date(startTime);

                    // 開始時間が過ぎていたら 20分経過のように、経過時間を表示
                    if(startDateTime.getTime() < now.getTime()){
                        const diffHour = now.getHours() - startDateTime.getHours();
                        const diffMin = now.getMinutes() - startDateTime.getMinutes();
                        const diff = diffHour * 60 + diffMin;

                        res = diff + "分経過";
                        return res;
                    }
            }

            res = startTime.substring(0,5) + " ～ " + endTime.substring(0,5);

            // 両方とも00:00の場合は未設定と解釈して時間出さない
            if(startTime == "00:00:00" && endTime == "00:00:00" ){
                res = "";
            }

            return res
        },
        openDetail(e:Event, eventId:string):void{
            e.stopPropagation();
            this.refs.updateHouseEventModal.openModal(eventId);
        },
        async openEventModalFromUrl(eventId:string):Promise<void>{
            await this.getEventList();
            this.refs.updateHouseEventModal.openModal(eventId);
        }
    }
})
</script>


