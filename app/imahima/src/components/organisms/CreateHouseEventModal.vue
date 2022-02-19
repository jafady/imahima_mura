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
                                <input type="text" v-model="eventName" class="eventName_input" placeholder="タイトル">
                            </div>
                            <div class="mb-3">
                                <div class="content_title">概要</div>
                                <div class="CHEM_content">
                                    <div class="m-1 CHEM_inline recruitment_area">
                                        <div class="CHEM_icon recruitment_icon"></div>
                                        <div class="content_subtitle">目標人数</div>
                                        <input type="number" v-model="recruitmentNumbersLower" class="text_input" >
                                        <div class="suffix">人</div>
                                        <div class="middle">～</div>
                                        <input type="number" v-model="recruitmentNumbersUpper" class="text_input" >
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
                                        <datepicker class="vue-datepicker-box" v-model="startDate" />
                                    </div>
                                    <div class="m-1 mt-3 CHEM_inline time_area">
                                        <div class="time_area_weight"></div>
                                        <div class="content_subtitle"></div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="startTime" :key="refreshStartTime" :minute-interval="10" hide-clear-button></VueTimepicker>
                                        <div class="middle">～</div>
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="endTime" :key="refreshEndTime" :minute-interval="10" hide-clear-button></VueTimepicker>
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
                                    <textarea class="detail_input" v-model="detail"/>
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
            height: 55px;
            margin: 0 auto;
            text-align-last: center;
            .btn_create_event{
                width: 80%;
                height: 55px;
                font-size: 18px;
                font-weight: bold;
                background-position-x: 80%;

                .create_event_icon{
                    position: absolute;
                    left: 23%;
                    width: 46px;
                    height: 55px;
                    background-image: url("../../assets/img/house/create_event.svg");
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
}

export default defineComponent({
    name: "CreateHouseEventModal",
    components: {
        Icon,
    },
    setup(): Record<string, any>{
        const { sortTime,cutSeconds, sendWebsocket } = utils()
        return{
            sortTime,
            cutSeconds,
            sendWebsocket
        }
    },
    data(): DataType {
        return{
            eventName: "",
            recruitmentNumbersLower: 0,
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
    },
    methods: {
        openModal():void{
            // データ初期化
            this.getCategoryList()
            
            // モーダル開く
            const target = document.getElementById('create_event_modal');
            if(!target) return;
            const myModal = new Modal(target);
            if(!myModal) return;
            myModal.show();
        },
        // initData():void{
        //     this.houseName = "";
        //     this.discordUrl = "";
        //     this.friendId = "";
        //     this.friendName = "";
        //     this.alreadyRegistered = false;
        // },
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
        createEvent(){
            console.log("createEvent");
        },
        
        saveHouseInfo(data:any):void{
            this.$http.put("/api/house_info/" + this.houseId + "/",data)
            .then(async ()=>{
                // 家の名前のためだけではあるけれど。。
                this.$emit("changeHouseInfo")
            });
        }
    }
})



</script>


