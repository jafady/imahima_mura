<template>
    <div class="container SSM_container">
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="status_setting" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-body SSM_body">
                            <div v-if="!isToHimaView">
                                <div>こんにちは。</div>
                                <div>今日のご予定はいかがでしょうか？</div>
                            </div>
                            <div v-else>
                                <div>ヒマな人のための画面を出そうとしています。</div>
                                <div>いつまでヒマですか？</div>
                            </div>
                            <div class="SSM_content">
                                <div class="d-inline-flex mt-2 SSM_inline">
                                    <div class="display">
                                        <div class="SSM_inline_icon hima"></div>
                                        <div class="SSM_inline_word">ヒマでしかない</div>
                                    </div>
                                    <Switch v-model:value="statusHima" :switchId="'switch1'" @change="changeStatus(STATUS.hima, statusHima)"/>
                                </div>
                                <div class="d-inline-flex mt-2 SSM_inline">
                                    <div class="display">
                                        <div class="SSM_inline_icon busy"></div>
                                        <div class="SSM_inline_word">ヒマじゃない</div>
                                    </div>
                                    <Switch v-model:value="statusBusy" :switchId="'switch2'" @change="changeStatus(STATUS.busy, statusBusy)"/>
                                </div>

                                <div class="mt-2">
                                    <div class="SSM_content_title d-flex">いつまでのステータスか</div>
                                    <div class="d-inline-flex SSM_inline_statusValidDateTime">
                                        <datepicker class="vue-datepicker-box" v-model="statusValidDate" />
                                        <VueTimepicker input-class="time" format="HH:mm" v-model="statusValidTime" :key="refreshStatusTime" :minute-interval="10" hide-clear-button></VueTimepicker>
                                    </div>
                                </div>
                            </div>
                            
                        </div>
                        <div class="SSM_footer">
                            <button type="button" class="btn btn_primary_normal IUM_btn" data-bs-dismiss="modal" @click="saveStatus">確定</button>
                        </div>
                    </div>
                </div>
            </div>
        </teleport>
    </div>
</template>

<style lang="scss">
.status_setting{
    height: 350px;
    width: 150px;
    background-position: center;
    margin: 0 auto;
    border: none;
}
.modal-content{
    overflow: unset!important;
}
.SSM_body{
    font-family: var(--font-family);
    padding-bottom: 0!important;
    background-color: var(--content-bg-color);
    overflow: unset!important;
    .SSM_content{
        background-color: rgba(246,246,246,1);
        padding: 10px;
        border-radius: var(--content-border-radius);
        .SSM_inline{
            align-items: center;
            justify-content: space-between;
            width: 100%;

            .display{
                display: inline-flex;
                align-items: center;
                
                .SSM_inline_icon{
                    width: 40px;
                    height: 40px;
                    border-radius: 20px;
                    margin-right: 5px;
                }
                .ongame{
                    background-color: var(--status-color-ongame);
                }
                .hima{
                    background-color: var(--status-color-hima);
                }
                .maybe{
                    background-color: var(--status-color-maybe);
                }
                .busy{
                    background-color: var(--status-color-busy);
                }
            }
        }
        .SSM_inline_statusValidDateTime{
            align-items: center;
            width: 100%;
            .vue-datepicker-box{
                width: 120px;
                height: 40px;
                border: none;
                border-radius: 8px;
                font-family: var(--font-family);
                text-align: center;
            }

            .time{
                width: 70px;
                height: 40px;
                border: none;
                border-radius: 8px;
                margin-left: 20px;
                font-family: var(--font-family);
                text-align: center;
            }
            
        }
    }
}
.SSM_footer{
    display: flex;
    align-content: center;
    justify-content: space-evenly;
    align-items: center;
    height: 60px;
    background-color: var(--content-bg-color);
}

.vue__time-picker{
    width:fit-content !important;
}

</style>

<script lang="ts">
import { defineComponent } from 'vue'
import CONST from '@/mixins/const'
import Switch from '@/components/molecules/Switch.vue'
import { Modal } from 'bootstrap'

export type DataType = {
    statusHima: boolean,
    statusBusy: boolean,
    statusValidDateTime: Date | null,
    refreshStatusTime: number,

    isToHimaView: boolean,
}

export default defineComponent({
    name: "StatusSettingModal",
    components: {
        Switch,
    },
    setup(): Record<string, any>{
        const { STATUS } = CONST
        return{
            STATUS
        }
    },
    data(): DataType {
        return{
            statusHima: true,
            statusBusy: false,
            statusValidDateTime: null,
            refreshStatusTime: 1,

            isToHimaView: false,
        }
    },
    computed: {
        statusValidDate:{
            get: function ():Date | null {
                if(!this.statusValidDateTime){
                    return null;
                }
                const val:Date = new Date(this.statusValidDateTime.getTime());
                val.setHours(0);
                val.setMinutes(0);
                val.setSeconds(0);
                return val;
            },
            set: function (newVal:Date):void {
                const val:Date = new Date(newVal.getTime());
                let HH = 0;
                let mm = 0;
                if(this.statusValidTime){
                    HH = parseInt(this.statusValidTime.substring(0,2)) || 0;
                    mm = parseInt(this.statusValidTime.substring(3,5)) || 0;
                    val.setHours(HH);
                    val.setMinutes(mm);
                }
                this.statusValidDateTime = val;
            },
        },
        statusValidTime:{
            get: function ():string | null {
                if(!this.statusValidDateTime){
                    return null;
                }
                return this.statusValidDateTime.getHours().toString().padStart(2,'0') + ":" + this.statusValidDateTime.getMinutes().toString().padStart(2,'0');
            },
            set: function (newVal:string):void {
                if(this.statusValidDate){
                    const val:Date = new Date(this.statusValidDate.getTime());
                    const HH:number = parseInt(newVal.substring(0,2)) || 0;
                    const mm:number = parseInt(newVal.substring(3,5)) || 0;
                    val.setHours(HH);
                    val.setMinutes(mm);
                    this.statusValidDateTime = val;
                }
            },
        },
    },
    methods: {
        openModal(isToHimaView:boolean):void{
            this.isToHimaView = isToHimaView;
            // データ読み込み
            const userData = this.$store.state.houseMates[this.$store.state.userId];
            // 予定ではヒマなときに出すので基本ヒマで
            this.setStatusFlg(userData.nowStatus);
            // 今日 + noticableEndTimeの日時で。
            let val:Date = new Date();
            const noticableEndTime: string = userData.noticableEndTime;
            val.setHours(parseInt(noticableEndTime.substring(0,2)) || 0);
            val.setMinutes(parseInt(noticableEndTime.substring(3,5)) || 0);

            // noticableEndTimeが今の時間よりも前であれば今の時間を入れる
            if(val < new Date()){
                val = new Date();
            }
            val.setSeconds(0);
            this.statusValidDateTime = val;
            this.refreshStatusTime *= -1;

            // モーダル開く
            const target = document.getElementById('status_setting');
            if(!target) return;
            const myModal = new Modal(target);
            if(!myModal) return;
            myModal.show();
        },
        setStatusFlg(statusName:string):void{
            this.statusHima = false;
            this.statusBusy = false;
            if (statusName == CONST.STATUS.hima){
                this.statusHima = true;
            }else if(statusName == CONST.STATUS.busy){
                this.statusBusy = true;
            }else{
                this.statusHima = true;
            }
        },
        async changeStatus(statusName:string, val:boolean):Promise<void>{
            if(val){
                this.statusHima = false;
                this.statusBusy = false;
            }
            if (statusName == CONST.STATUS.hima){
                this.statusHima = val;
            }else if(statusName == CONST.STATUS.busy){
                this.statusBusy = val;
            }
            if(!this.statusHima && !this.statusBusy){
                this.statusHima = true;
            }
            
        },
        async saveStatus():Promise<void>{
            const statusRes = await this.$http.get("/api/statuses/")
            const saveData = {statusId:null, statusValidDateTime: this.statusValidDateTime};
            if (this.statusHima){
                saveData["statusId"] = statusRes.data.find((status:any) => status.statusName == CONST.STATUS.hima).id;
            }else if(this.statusBusy){
                saveData["statusId"] = statusRes.data.find((status:any) => status.statusName == CONST.STATUS.busy).id;
            }

            this.saveUserSetting(saveData);
        },
        saveUserSetting(data:any):void{
            this.$http.put("/api/user_setting/" + this.$store.state.userId + "/",data)
            .then(async ()=>{
                await this.$store.dispatch("getUserInfo");
                this.$emit("noticeChangeStatus")
                if(this.isToHimaView){
                    this.$emit("changeStatusToHimaView")
                }
            });
        }
    }
})



</script>


