<template>
    <div class="container UHEM_container">
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="update_event_modal" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content UHEM_modal">
                        <div class="UHEM_header">
                            <div class="delete_event btn_imahima" v-if="mode=='in'" @click="confirmDelete"></div>
                            <div class="title">
                                <div class="title_word">誘いの詳細</div>
                            </div>
                            <div class="turn_back btn_imahima" data-bs-dismiss="modal"></div>
                        </div>
                        <div class="modal-body UHEM_body">
                            <div class="mb-3 d-flex">
                                <input type="text" v-model="eventName" class="eventName_input" :class="errorTitle" placeholder="タイトル" @change="changeEventName" :disabled="disabled">
                            </div>
                            <div class="mb-3">
                                <div class="content_title">概要</div>
                                <div class="UHEM_content">
                                    <div class="m-1 UHEM_inline recruitment_area">
                                        <div class="UHEM_icon recruitment_icon"></div>
                                        <div class="content_subtitle">目標人数</div>
                                        <input type="number" v-model="recruitmentNumbersLower" class="text_input" :class="errorRecruitmentNumbersLower" min="1" step="1" @change="changeRecruitmentNumbersLower" :disabled="disabled">
                                        <div class="suffix">人</div>
                                        <div class="middle">～</div>
                                        <input type="number" v-model="recruitmentNumbersUpper" class="text_input" min="1" step="1" @change="changeRecruitmentNumbersUpper" :disabled="disabled">
                                        <div class="suffix">人</div>
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline location_area">
                                        <div class="UHEM_icon location_icon"></div>
                                        <div class="content_subtitle">場所</div>
                                        <input type="text" v-model="location" class="text_input" @change="changeLocation" :disabled="disabled">
                                        <div class="UHEM_icon location_url_icon btn_imahima" @click="enterLink"></div>
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline location_url_area">
                                        <div class="location_url_area_weight"></div>
                                        <div class="content_subtitle"></div>
                                        <input type="text" v-model="locationUrl" class="text_input" placeholder="https://discord.gg/" @change="changeLocationUrl" :disabled="disabled">
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline date_area">
                                        <div class="UHEM_icon time_icon"></div>
                                        <div class="content_subtitle">開催日時</div>
                                        <datepicker class="vue-datepicker-box" v-model="startDate" :lower-limit="lowerLimitDate" :clearable="!disabled" @input="changeStartDate" :disabled="disabled"/>
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline time_area">
                                        <div class="time_area_weight"></div>
                                        <div class="content_subtitle"></div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="startTime" :key="refreshStartTime" :minute-interval="10" @change="changeTime('start')" :disabled="disabled"></VueTimepicker>
                                        <div class="middle">～</div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="endTime" :key="refreshEndTime" :minute-interval="10" @change="changeTime('end')" :disabled="disabled"></VueTimepicker>
                                    </div>
                                    <div v-if="needTyousei" class="m-1 mt-3 UHEM_inline tyousei_area">
                                        <div class="UHEM_icon tyousei_icon"></div>
                                        <div class="content_subtitle">日程調整</div>
                                            <div v-if="tyouseiUrl" class="tyousei_btn_area">
                                                <button type="button" class="btn btn_primary_normal btn_make_tyousei content_center_inline" @click="enterTyouseiLink">
                                                    <div class="write_tyousei_icon_dummy"></div>
                                                    <div>予定を書き込む</div>
                                                    <div class="write_tyousei_icon"></div>
                                                </button>
                                            </div>
                                            <div v-else class="tyousei_btn_area">
                                                <button type="button" class="btn btn_primary_normal btn_make_tyousei content_center_inline" @click="enterTyouseiLink">
                                                    <div class="make_tyousei_icon_dummy"></div>
                                                    <div>調整さんを作る</div>
                                                    <div class="make_tyousei_icon"></div>
                                                </button>
                                            </div>
                                    </div>
                                    <div v-if="needTyousei" class="m-1 mt-3 UHEM_inline tyousei_area">
                                        <div class="tyousei_area_weight"></div>
                                        <div class="content_subtitle"></div>
                                        <input type="text" v-model="tyouseiUrl" class="text_input" placeholder="https://chouseisan.com/" @change="changeTyouseiUrl" :disabled="disabled">
                                    </div>
                                    <div v-if="canRegistCalendar" class="m-1 mt-3 UHEM_inline regist_calendar_area">
                                        <div class="UHEM_icon regist_calendar_icon"></div>
                                        <div class="content_subtitle">予定</div>
                                        <button type="button" class="btn btn_primary_normal btn_regist_calendar content_center_inline" @click="registCalendar" :disabled="disabled">
                                            <div class="regist_calendar_btn_icon"></div>
                                            <div>自分のカレンダーに登録</div>
                                            <div class="regist_calendar_btn_icon_dummy"></div>
                                        </button>
                                    </div>
                                    <div class="m-1 mt-3 UHEM_inline category_area">
                                        <div class="UHEM_icon category_icon"></div>
                                        <div class="content_subtitle">カテゴリ</div>
                                        <select class="category_select" v-model="selectedCategoryId" @change="changeSelectedCategoryId" :disabled="disabled">
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
                                    <textarea class="detail_input" :class="errorDetail" v-model="detail" @change="changeDetail" :disabled="disabled"/>
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
                                    <div class="m-1" v-if="houseMatesFuture.length > 0">
                                        <div class="content_subtitle">予定ではヒマ</div>
                                        <div class="housemate_area">
                                            <div v-for="(value) in houseMateListMaybe" v-bind:key="value.id">
                                                <div class="housemate btn_imahima" :class="selectedHousemateCss(value.id)" @click="changeSelectedHousemate(value.id)">
                                                    <div class="icon_area"><Icon :userId="value.id" :hideStatus="true"/></div>
                                                    <div class="mt-2">{{value.name}}</div>
                                                    <div>{{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="m-1 mt-3" v-if="houseMatesFuture.length > 0">
                                        <div class="content_subtitle">ヒマじゃない</div>
                                        <div class="housemate_area">
                                            <div v-for="(value) in houseMateListBusy" v-bind:key="value.id">
                                                <div class="housemate btn_imahima" :class="selectedHousemateCss(value.id)" @click="changeSelectedHousemate(value.id)">
                                                    <div class="icon_area"><Icon :userId="value.id" :hideStatus="true"/></div>
                                                    <div class="mt-2">{{value.name}}</div>
                                                    <div v-if="isDisplayTime(value.noticableStartTime,value.noticableEndTime)">
                                                        {{cutSeconds(value.noticableStartTime)}}~{{cutSeconds(value.noticableEndTime)}}
                                                    </div>
                                                    <div v-else>ヒマなし</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="m-1" v-if="houseMatesFuture.length < 1">
                                        <div class="content_subtitle">友達リスト</div>
                                        <div class="housemate_area">
                                            <div v-for="(value) in houseMates" v-bind:key="value.id">
                                                <div class="housemate btn_imahima" :class="selectedHousemateCss(value.id)" @click="changeSelectedHousemate(value.id)">
                                                    <div class="icon_area"><Icon :userId="value.id" :hideStatus="true"/></div>
                                                    <div class="mt-2">{{value.name}}</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mt-4 m-1" v-if="selectedHousemate.length > 0">
                                        <div class="content_subtitle">なんて話しかけますか？</div>
                                        <div class="manual_msg_area">
                                            <textarea class="manual_msg" :class="errorManualMsg" v-model="manualMsg" placeholder="あそぼ"/>
                                        </div>
                                    </div>
                                    <div class="m-4 send_notice">
                                        <button type="button" class="btn btn_primary_normal btn_send_notice content_center_inline" @click="sendManualNotice">
                                            <div class="send_notice_icon_dummy"></div>
                                            <div class="leave_event_word">追加通知</div>
                                            <div class="send_notice_icon"></div>
                                        </button>
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
            <ConfirmModal ref="confirmModal" @ok="deleteEvent"/>
            <Alert :css="alertCss" :alertMsg="alertMsg" :displayTime="alertDisplayTime" ref="alert" />
        </teleport>
    </div>
</template>

<style lang="scss">
.UHEM_modal{
    font-family: var(--font-family);
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
                    width: 45%;
                }
                .location_url_icon{
                    width: 26px;
                    height: 30px;
                    margin-left: 10px;
                    background-image: url("../../assets/img/house/event/enter_url.svg");
                }
            }
            .location_url_area{
                .location_url_area_weight{
                    width: 16px;
                    margin-right: 10px;
                }
                .text_input{
                    width: 65%;
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
                    font-family: var(--font-family);
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
                    font-family: var(--font-family);
                }
            }
            .tyousei_area{
                .tyousei_icon{
                    background-image: url("../../assets/img/house/event/calendar.svg");
                    width: 20px;
                }
                .content_subtitle{
                    margin-right: 14px;
                }
                .tyousei_url_icon{
                    width: 26px;
                    height: 30px;
                    margin-left: 10px;
                    background-image: url("../../assets/img/house/event/enter_url.svg");
                }
                .tyousei_btn_area{
                    display:contents;
                    .btn_make_tyousei{
                        width: 65%;
                        height: 35px;
                        font-size: 15px;
                        font-weight: bold;                    

                        .write_tyousei_icon{
                            position: relative;
                            right: 3%;
                            width: 30px;
                            height: 30px;
                            background-image: url("../../assets/img/house/event/write_tyousei.svg");
                            background-repeat: no-repeat;
                            background-position-y: center;
                            background-size: contain;
                        }
                        .write_tyousei_icon_dummy{
                            width: 30px;
                            height: 30px;
                        }

                        .make_tyousei_icon{
                            position: relative;
                            right: 3%;
                            width: 30px;
                            height: 30px;
                            background-image: url("../../assets/img/house/event/make_tyousei.svg");
                            background-repeat: no-repeat;
                            background-position-y: center;
                            background-size: contain;
                        }
                        .make_tyousei_icon_dummy{
                            width: 30px;
                            height: 30px;
                        }
                    }
                }


                .tyousei_area_weight{
                    width: 16px;
                    margin-right: 10px;
                }
                .text_input{
                    width: 65%;
                }
            }
            .regist_calendar_area{
                .regist_calendar_icon{
                    background-image: url("../../assets/img/house/event/calendar.svg");
                    width: 20px;
                }
                .content_subtitle{
                    margin-right: 16px;
                }
                
                .btn_regist_calendar{
                    width: 65%;
                    height: 35px;
                    font-size: 13px;
                    font-weight: bold;                    

                    .regist_calendar_btn_icon{
                        position: relative;
                        left: 3%;
                        width: 20px;
                        height: 15px;
                        background-image: url("../../assets/img/house/event/regist_calendar.svg");
                        background-repeat: no-repeat;
                        background-position-y: center;
                        background-size: contain;
                    }
                    .regist_calendar_btn_icon_dummy{
                        width: 5px;
                        height: 15px;
                    }
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
                    padding-left: 7px;
                }
                .category_select:disabled{
                    opacity: 0.5;
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
                min-height: 120px;
                margin-top: 5px;
                .housemate{
                    width: 80px;
                    margin-right: 10px;
                    font-size: 10px;
                    font-weight: bold;
                    border-radius: 4px;
                    padding-top: 5px;
                    padding-bottom: 10px;
                    .icon_area{
                        height:60px;
                        width:60px;
                        margin: 0 auto;
                    }
                }
                .noSelectedHousemate{
                    border: solid;
                    border-color: var(--no-selected-area);
                    border-width: 1px;
                }
                .selectedHousemate{
                    background-color: var(--selected-area);
                    border: none;
                }
            }

            .manual_msg_area{
                display: flex;
                justify-content: center;
                .manual_msg{
                    width: 100%;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                }
            }

            .send_notice{
                width: 90%;
                margin: 0 auto;
                text-align: center;
                .btn_send_notice{
                    width: 70%;
                    height: 55px;
                    font-size: 18px;
                    font-weight: bold;                    

                    .send_notice_icon{
                        position: relative;
                        right: 3%;
                        width: 30px;
                        height: 30px;
                        background-image: url("../../assets/img/house/event/send_notice.svg");
                        background-repeat: no-repeat;
                        background-position-y: center;
                        background-size: contain;
                    }
                    .send_notice_icon_dummy{
                        width: 30px;
                        height: 30px;
                    }
                }
            }
        }

        .join_event{
            width: 90%;
            margin: 0 auto;
            text-align: center;
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
            text-align: center;
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
import ConfirmModal from '@/components/molecules/ConfirmModal.vue'
import Alert from '@/components/molecules/Alert.vue'

interface category {id:string,name:string}

export type DataType = {
    eventId: string,
    eventName: string,
    recruitmentNumbersLower: number,
    recruitmentNumbersUpper: number|null,
    location: string,
    locationUrl: string,
    startDate: Date | null,
    startTime: string | null,
    endTime: string | null,
    refreshStartTime: number,
    refreshEndTime: number,
    makeTyouseiUrl: string,
    tyouseiUrl: string,
    selectedCategoryId: string,
    categoryList: category[],

    detail: string,

    houseMatesFuture:houseMate[],
    userIds: string[],

    selectedHousemate: string[],
    manualMsg: string,
    isErrorManualMsg: boolean,

    lowerLimitDate: Date,

    alertCss: string,
    alertMsg: string,
    alertDisplayTime: number,
}

export default defineComponent({
    name: "UpdateHouseEventModal",
    components: {
        Icon,
        ConfirmModal,
        Alert
    },
    setup(): Record<string, any>{
        const { sortTime,cutSeconds, sendWebsocket,getDisplayTime,dateTimeToUrlString,getStatusByName } = utils()
        return{
            sortTime,
            cutSeconds,
            sendWebsocket,
            getDisplayTime,
            dateTimeToUrlString,
            getStatusByName
        }
    },
    data(): DataType {
        return{
            eventId: "",
            eventName: "",
            recruitmentNumbersLower: 1,
            recruitmentNumbersUpper: null,
            location: "discord",
            locationUrl: "",
            startDate: new Date(),
            startTime: null,
            endTime: null,
            refreshStartTime: 1,
            refreshEndTime: 1,
            makeTyouseiUrl: "https://chouseisan.com/",
            tyouseiUrl: "",
            selectedCategoryId: "",
            categoryList:[],

            detail: "",

            houseMatesFuture: [],
            userIds: [],

            selectedHousemate: [],
            manualMsg: "",
            isErrorManualMsg: false,

            lowerLimitDate: new Date(),
            alertCss: "alert-success",
            alertMsg: "",
            alertDisplayTime: 2000,
        }
    },
    computed: {
        refs():any {
            return this.$refs;
        },
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
        disabled():boolean{
            if(this.mode == "out"){
                return true;
            }
            return false;
        },
        needTyousei():boolean{
            if(this.mode == "out"){
                return false;
            }
            if(!this.startDate || !this.startTime || !this.endTime){
                return true;
            }
            return false;
        },
        canRegistCalendar():boolean{
            if(this.mode == "out"){
                return false;
            }
            if(!this.startDate || !this.startTime || !this.endTime){
                return false;
            }
            return true;
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
        errorManualMsg():string{
            if(this.manualMsg || !this.isErrorManualMsg){
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
            this.getHouseMateFuture();
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
            this.getHouseMateFuture();
            
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
            this.locationUrl = targetData.locationUrl;

            this.startDate = targetData.startDate? new Date(targetData.startDate):null;
            this.startTime = targetData.startTime;
            this.endTime = targetData.endTime;
            this.tyouseiUrl = targetData.tyouseiUrl;
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
        async getHouseMateFuture():Promise<void>{
            // 開催日時を選んだ時点のユーザ一覧を取得する
            if(!this.startDate || !this.startTime){
                this.houseMatesFuture = [];
                return;
            }
            const targetDay = this.startDate;
            const HH = parseInt(this.startTime.substring(0,2)) || 0;
            const mm = parseInt(this.startTime.substring(3,5)) || 0;
            targetDay.setHours(HH);
            targetDay.setMinutes(mm);
            targetDay.setSeconds(0);
            const searchDateTime = this.dateTimeToUrlString(targetDay);
            const houseMatesFutureRes = await this.$http.get("/api/users_future/" + this.$store.state.houseId + "/" + searchDateTime + "/");
            const data:houseMate[] = [];
            const res = houseMatesFutureRes.data;
            for (const key in res) {
                const todayEndTime = res[key].todayEndTime == "00:00:00"?"24:00:00":res[key].todayEndTime;
                data.push({
                    id: res[key].id,
                    name: res[key].username,
                    icon: "",
                    noticableStartTime: res[key].todayStartTime,
                    noticableEndTime: todayEndTime,
                    nowStatus: this.getStatusByName(res[key].nowStatus),
                    statusValidDateTime: res[key].userSetting__statusValidDateTime,
                })
            }
            this.houseMatesFuture=data;
        },
        getHouseMateList(status:string):houseMate[]{
            // 計算量を減らすためにfilterで母数を減らす
            // ソート順 ステータス＞ヒマ終了時間＞ヒマ開始時間
            const houseMateList:any[] = this.houseMatesFuture.filter((houseMate:any)=>houseMate.nowStatus == status)
            .sort((a:any, b:any)=>{
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
        
        // 表示用計算
        selectedHousemateCss(userId:string):string{
            if(this.selectedHousemate.includes(userId)){
                return "selectedHousemate";
            }else{
                return "noSelectedHousemate"
            }
        },
        changeSelectedHousemate(userId:string):void{
            if(this.selectedHousemate.includes(userId)){
                this.selectedHousemate = this.selectedHousemate.filter((selectedUserId:string)=> selectedUserId != userId);
            }else{
                this.selectedHousemate.push(userId);
            }
        },

        getUserName(userId:string):string{
            return this.$store.state.houseMates[userId].name;
        },
        isDisplayTime(startTime:string,endTime:string):boolean{
            if(this.cutSeconds(startTime) == '00:00' && this.cutSeconds(endTime)=='24:00'){
                return false
            }else{
                return true
            }
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
        changeLocationUrl():void{
            const saveData:Record<string, unknown> = {};
            saveData["locationUrl"] = this.locationUrl;
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
            this.getHouseMateFuture();
        },
        changeTyouseiUrl():void{
            const saveData:Record<string, unknown> = {};
            saveData["tyouseiUrl"] = this.tyouseiUrl;
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
            this.getHouseMateFuture();
        },
        checkEditing(data:any):boolean{
            const blankHour = data?.HH == "";
            const blankMin = data?.mm == "";
            // 片方だけがブランクの場合は編集中と判断する
            const edited = blankHour == blankMin;
            return !edited;
        },

        enterLink():void{
            if(!this.locationUrl){
                return;
            }
            window.open(this.locationUrl, '_blank');
        },
        enterTyouseiLink():void{
            if(!this.tyouseiUrl){
                window.open(this.makeTyouseiUrl, '_blank');
            }else{
                window.open(this.tyouseiUrl, '_blank');
            }
        },
        registCalendar():void{
            // カレンダー登録のため、ical形式で予定出力する
            if(!this.startDate || !this.startTime || !this.endTime){
                return;
            }
            const startDate = ""+this.startDate.getFullYear()+("00"+(this.startDate.getMonth()+1)).slice(-2)+("00"+this.startDate.getDate()).slice(-2);
            const startTime = this.startTime.replace(":","")+"00";
            const endTime = this.endTime.replace(":","")+"00";
            const outputDetail = this.detail.split("\n").join("\\n");

            let contents = ["BEGIN:VCALENDAR"
                            ,"VERSION:2.0"
                            ,"PRODID:-//jafady//imahima//JP"
                            ,"BEGIN:VEVENT"
                            ,"DTSTART;TZID=Asia/Tokyo:"+startDate+"T"+startTime
                            ,"DTEND;TZID=Asia/Tokyo:"+startDate+"T"+endTime
                            ,"SUMMARY:" + this.eventName || " "
                            ,"LOCATION:" + this.location || " "
                            ,"URL:" + this.locationUrl || " "
                            ,"DESCRIPTION:" + outputDetail || " "
                            ,"END:VEVENT"
                            ,"END:VCALENDAR"
                            ]
            
            const content = contents.join("\r\n")
            const blob = new Blob([content],{type:"text/calendar"});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'imahimaSchedule.ics';
            link.click();
        },
        confirmDelete():void{
            this.refs.confirmModal.openModal("本当に消しますか？");
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
        },

        sendManualNotice():void{
            if(this.selectedHousemate.length < 1){
                return;
            }
            if(!this.manualMsg){
                this.isErrorManualMsg = true;
            }
            this.sendWebsocket(JSON.stringify({
                "type": "sendManualNotice",
                "houseId": this.$store.state.houseId,
                "eventId": this.eventId,
                "eventName": this.eventName,
                "targetUserIds": this.selectedHousemate,
                "msg": this.manualMsg,
            }));
            // 通知送ったよのメッセージを出す
            this.alertCss = "alert-success";
            this.alertMsg = "追加通知を送りました。";
            this.alertDisplayTime = 5000;
            this.refs.alert.open();
        }
    }
})



</script>


