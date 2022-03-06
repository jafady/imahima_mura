<template>
    <div class="container mypage_container">
        <Header />
        <div class="m-3">
            <div class="mypage_content">
                <div class="mypage_content_dummy_body">
                    <div class="mypage_logout" @click="logout">
                        <div class="mypage_logout_icon" />
                        <div class="mypage_logout_word">ログアウト</div>
                    </div>
                </div>
                <div>
                    <IconUploadModal />
                    <input type="text" v-model="userName" class="mypage_username" placeholder="名前" @change="changeUserName">
                    <div class="mypage_id d-inline-flex">
                        <div class="mypage_id_weight"></div>
                        <div class="mypage_id">ID:{{userId}}</div>
                        <div class="mypage_id_copy btn_imahima" @click="copyId"></div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="invitations.length > 0" class="m-3">
            <div class="mypage_title">招待を受ける</div>
            <div class="mypage_content">
                <div v-for="(item, index) in invitations" :key="index" class="mt-2 d-inline-flex mypage_inline invite_house_area">
                    <label class="invited_housename">{{item.houseName}}</label>
                    <button class="btn_primary_normal btn_approve_invite" @click="approveHouse(item)">この家に入る</button>
                </div>
            </div>
        </div>
        <div class="m-3">
            <div class="mypage_title">ステータス設定</div>
            <div class="mypage_content">
                <div class="d-inline-flex mt-2 mypage_inline">
                    <div class="display">
                        <div class="mypage_inline_icon hima"></div>
                        <div class="mypage_inline_word">ヒマでしかない</div>
                    </div>
                    <Switch v-model:value="statusHima" :switchId="'switch1'" @change="changeStatus(status.hima, statusHima)"/>
                </div>
                <div class="d-inline-flex mt-2 mypage_inline">
                    <div class="display">
                        <div class="mypage_inline_icon busy"></div>
                        <div class="mypage_inline_word">ヒマじゃない</div>
                    </div>
                    <Switch v-model:value="statusBusy" :switchId="'switch2'" @change="changeStatus(status.busy, statusBusy)"/>
                </div>

                <div class="mt-2">
                    <div class="mypage_content_title d-flex">いつまでのステータスか</div>
                    <div class="d-inline-flex mypage_inline_statusValidDateTime">
                        <datepicker class="vue-datepicker-box" v-model="statusValidDate" />
                        <VueTimepicker input-class="time" format="HH:mm" v-model="statusValidTime" :key="refreshStatusTime" :minute-interval="10" hide-clear-button></VueTimepicker>
                    </div>
                </div>
            </div>
        </div>

        <div class="m-3">
            <div class="mypage_title">通知設定</div>
            <div class="mypage_content">
                <div class="d-inline-flex mt-2 mypage_inline">
                    <div class="display">
                        <div class="mypage_inline_word">カテゴリにこだわらない</div>
                    </div>
                    <Switch v-model:value="isAllCategorySelected" :switchId="'switchNotice'" @change="changeIsAllCategorySelected(isAllCategorySelected)"/>
                </div>
                <div class="mt-2">
                    <div class="mypage_content_title d-flex">カテゴリ選択</div>
                    <div class="mypage_category_area">
                        <div v-for="(items, bulkIndex) in groupedCategorys" :key="bulkIndex" class="mypage_button_area_bulk">
                            <div v-for="(item, index) in items" :key="index" class="mypage_button_area" @change="changeCategorySelect(item)">
                                <input type="checkbox" v-model="item.selected" :id="bulkIndex + '_' + index">
                                <label class="btn_category btn_imahima" :for="bulkIndex + '_' + index">{{item.name}}</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="m-3">
            <div class="mypage_title">ヒマ予定時間</div>
            <div class="mypage_content">
                <div class="mt-2">
                    <div class="mypage_week_induction">お誘いしやすくするため、ヒマかもしれない時間を教えてください</div>
                    <div class="mypage_week_area">
                        <div v-for="(item, index) in week" :key="index" class="mypage_week_button_area">
                            <input type="checkbox" v-model="item.selected" :id="index" disabled="disabled">
                            <label class="btn_week" :for="index">{{item.name}}</label>
                            <div class="d-inline-flex mypage_inline_noticable">
                                <VueTimepicker input-class="time" format="HH:mm" v-model="item.startTime" :key="refresh" :minute-interval="10" @change="changeWeekTime(item)"></VueTimepicker>
                                <div class="hyphen">~</div>
                                <VueTimepicker input-class="time" format="HH:mm" v-model="item.endTime" :key="refresh" :minute-interval="10" @change="changeWeekTime(item)"></VueTimepicker>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-3 blank_content" />
        <Alert :css="alertCss" :alertMsg="alertMsg" :displayTime="alertDisplayTime" ref="alert" />
    </div>
</template>
<style lang="scss">
.mypage_container {
    min-height: 100%;
    max-width: 100% !important;
    padding: unset !important;

    .mypage_title{
        text-align: left;
        align-items: center;
        font-size: 21px;
    }

    .mypage_content{
        background-color: rgba(246,246,246,1);
        padding: 10px;
        border-radius: var(--content-border-radius);

        .mypage_content_dummy_body{
            width: calc(100% - 40px);
            position: absolute;
            align-self: center;
            padding-right: 10px;
            pointer-events: none;
            display: flex;
            justify-content: flex-end;

            .mypage_logout{
                pointer-events: all;
                height:50px;
                width:50px;
                .mypage_logout_icon{
                    background-image: url("../../assets/img/mypage/logout.svg");
                    width: 50px;
                    height: 35px;
                    background-repeat: no-repeat;
                    background-position: center;
                }
                .mypage_logout_word{
                    width:100%;
                    font-size:10px
                }
            }
        }
        .mypage_username{
            font-size: 35px;
            width: 100%;
            text-align: center;
            border: none;
            border-radius: 8px;
            background: none;
        }
        .mypage_id{
            font-size: 21px;
            align-items: center;
        }
        .mypage_id_copy{
            background-image: url("../../assets/img/mypage/copy.svg");
            width: 40px;
            height: 40px;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 28px 28px;
            background-color: white;
            border-radius: 24px;
            margin-left: 15px;
            box-shadow: 3px 7px 2px rgb(0 0 0 / 10%);
        }
        .mypage_id_weight{
            width: 40px;
            height: 40px;
            margin-right: 15px;
        }
        

        .mypage_inline{
            align-items: center;
            justify-content: space-between;
            width: 100%;

            .display{
                display: inline-flex;
                align-items: center;
                
                .mypage_inline_icon{
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
        .invite_house_area{
            height: 50px;
            .invited_housename{
                max-width: calc(100% - 150px);
                overflow: auto;
                text-align: left;
            }
            .btn_approve_invite{
                border: none;
                width: 130px;
                height: 35px;
            }
        }
        .mypage_inline_statusValidDateTime{
            align-items: center;
            width: 100%;
            .vue-datepicker-box{
                width: 120px;
                height: 40px;
                border: none;
                border-radius: 8px;
                font-family: "游ゴシック";
                margin-right: 20px;
                text-align: center;
            }

            .time{
                width: 70px;
                height: 40px;
                border: none;
                border-radius: 8px;
                font-family: "游ゴシック";
                text-align: center;
            }
            
        }
        .mypage_category_area{
            display: flex;
            overflow-x: auto;
            white-space: nowrap;
            .mypage_button_area_bulk{
                width: 125px;
                height: 130px;
                white-space: normal;
                margin-right: 10px;
                .mypage_button_area{
                    width: 125px;
                    height: 45px;
                    margin-top: 10px;

                    .btn_category{
                        background-color: var(--inactive-bg-color);
                        border-radius: 23px;
                        color: var(--text-color-gray);
                        font-size: 18px;
                        box-shadow: var(--box-shadow);
                        width: 125px;
                        height: 45px;
                        white-space: pre;
                        overflow-x: scroll;
                        overflow-y: hidden;
                        padding: 10px 6px;
                        -ms-overflow-style: none;
                    }
                    .btn_category::-webkit-scrollbar {
                        display:none;
                    }
                    input[type="checkbox"] {
                        display : none;            /* チェックボックス非表示 */
                    }
                    input[type="checkbox"]:checked +label {
                        background-color: var(--main-bg-color);
                        color: var(--text-color-white);
                        box-shadow:none;
                    }
                }
            }
        }

        .mypage_week_induction{
            text-align: left;
        }

        .mypage_week_area{
            white-space: nowrap;

            .mypage_week_button_area{
                display: flex;
                width: 100%;
                height: 60px;
                align-items: center;
                margin-top: 10px;
                margin-right: 10px;

                .btn_week{
                    background-color: var(--inactive-bg-color);
                    border-radius: 23px;
                    color: var(--text-color-gray);
                    font-size: 20px;
                    width: 45px;
                    height: 45px;
                    padding: 8px;
                    margin-right: 10px;
                }
                input[type="checkbox"] {
                    display : none;            /* チェックボックス非表示 */
                }
                input[type="checkbox"]:checked +label {
                    background-color: var(--main-bg-color);
                    color: var(--text-color-white);
                    box-shadow:none;
                }

                .mypage_inline_noticable{
                    align-items: center;
                    width: calc(100% - 60px);

                    .time{
                        width: 80px;
                        height: 40px;
                        border: none;
                        border-radius: 8px;
                        font-family: "游ゴシック";
                        text-align: left;
                    }
                    .hyphen{
                        width: 30px;
                    }
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

import CONST, { STATUS } from '@/mixins/const'
import Header from '@/components/organisms/Header.vue'
import Switch from '@/components/molecules/Switch.vue'
import Alert from '@/components/molecules/Alert.vue'
import IconUploadModal from '@/components/organisms/IconUploadModal.vue'

import utils from '@/mixins/utils'
interface category {id:string,name:string,selected:boolean}
interface weekContent {id:string,name:string,selected:boolean,startTime:any,endTime:any}
interface invitation {id:string,houseName:string}

export type DataType = {
    userId: string,
    userName: string,

    invitations: invitation[],

    statusHima: boolean,
    statusBusy: boolean,
    statusValidDateTime: Date | null,
    refreshStatusTime: number,

    isAllCategorySelected: boolean,
    categorys:category[],

    refresh: number,
    week:weekContent[],

    alertCss: string,
    alertMsg: string,
    alertDisplayTime: number,

}

export default defineComponent({
    name: "MyPage",
    components: {
        Header,
        Switch,
        Alert,
        IconUploadModal,
    },
    setup(): Record<string, any>{
        const { dateTimeToString } = utils()
        return{
            dateTimeToString
        }
    },
    data(): DataType {
        return{
            userId: "",
            userName: "",

            invitations:[],

            statusHima: true,
            statusBusy: false,
            statusValidDateTime: null,
            refreshStatusTime: 1,
            
            isAllCategorySelected: true,
            categorys:[
                {id:"", name:"ボードゲーム",selected:true},
            ],
            
            refresh:1,
            week:[
                {name:"月",id:"",selected:true,startTime:"time",endTime:"time"},
                {name:"火",id:"",selected:true,startTime:"time",endTime:"time"},
                {name:"水",id:"",selected:true,startTime:"time",endTime:"time"},
                {name:"木",id:"",selected:true,startTime:"time",endTime:"time"},
                {name:"金",id:"",selected:true,startTime:"time",endTime:"time"},
                {name:"土",id:"",selected:true,startTime:"time",endTime:"time"},
                {name:"日",id:"",selected:true,startTime:"time",endTime:"time"},
            ],

            alertCss: "alert-success",
            alertMsg: "",
            alertDisplayTime: 2000,
        }
    },
    computed: {
        refs():any {
            return this.$refs;
        },
        groupedCategorys():category[][]{
            const base = this.categorys.length
            const splitCnt = 2       // 何個ずつに分割するか
            const groupedCategorys = []
            for (let i=0; i<Math.ceil(base/splitCnt); i++) {
                let multipleCnt = i * splitCnt  // splitCnt
                // (i * splitCnt)番目から(i * splitCnt + splitCnt)番目まで取得
                let result = this.categorys.slice(multipleCnt, multipleCnt + splitCnt) 
                groupedCategorys.push(result)
            }
            return groupedCategorys
        },
        status():STATUS{
            return CONST.STATUS;
        },
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
                this.changeStatusValidTime();
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
                    this.changeStatusValidTime();
                }
            },
        },

    },
    created: function():void{
        this.$store.dispatch("getUserInfo").then(()=>{
            this.getUserFromStore();
        });

        this.getUserInfo();
    },
    methods: {
        getUserFromStore():void{
            this.userId = this.$store.state.userId;
            this.userName = this.$store.state.userName;
        },
        async getUserInfo():Promise<void>{
            const categoryRes = await this.$http.get("/api/categorys/");
            const userInfoRes = await this.$http.get("/api/user_info/" + this.$store.state.userId + "/");
            const myInvitationRes = await this.$http.get("/api/get_myinvitation/" + this.$store.state.userId + "/");

            const firstData = userInfoRes.data[0];
            // status
            this.setStatusFlg(firstData.userSetting__statusId__statusName);
            this.setStatusTime(firstData.userSetting__statusValidDateTime);
            
            // categorys
            this.isAllCategorySelected = firstData.userSetting__isAllCategorySelected;
            this.setCategorys(categoryRes.data,userInfoRes.data);

            // week
            this.setNoticeData(firstData);

            // invite
            this.setInvitation(myInvitationRes.data);

        },
        setStatusFlg(statusName:string):void{
            this.statusHima = false;
            this.statusBusy = false;
            if (statusName == CONST.STATUS.hima){
                this.statusHima = true;
            }else if(statusName == CONST.STATUS.busy){
                this.statusBusy = true;
            }
        },
        setStatusTime(statusValidDateTime:string):void{
            this.statusValidDateTime = new Date(statusValidDateTime);
            this.refreshStatusTime *= -1;
        },
        setCategorys(categorys:any[],userInfos:any[]){
            const data = [];
            for (const key in categorys) {
                const isSelected = userInfos.find((userInfo:any) => userInfo.userselectcategory__categoryId == categorys[key].id)?true:false;
                data.push({
                    id: categorys[key].id,
                    name: categorys[key].categoryName,
                    selected: isSelected
                });
            }
            this.categorys=data;
        },
        setNoticeData(data:any):void{
            this.week = [
                {name:"月", id:"Mon", selected: data.userSetting__noticableMonTimeStart!=data.userSetting__noticableMonTimeEnd, startTime: data.userSetting__noticableMonTimeStart, endTime: data.userSetting__noticableMonTimeEnd},
                {name:"火", id:"Tue", selected: data.userSetting__noticableTueTimeStart!=data.userSetting__noticableTueTimeEnd, startTime: data.userSetting__noticableTueTimeStart, endTime: data.userSetting__noticableTueTimeEnd},
                {name:"水", id:"Wed", selected: data.userSetting__noticableWedTimeStart!=data.userSetting__noticableWedTimeEnd, startTime: data.userSetting__noticableWedTimeStart, endTime: data.userSetting__noticableWedTimeEnd},
                {name:"木", id:"Thu", selected: data.userSetting__noticableThuTimeStart!=data.userSetting__noticableThuTimeEnd, startTime: data.userSetting__noticableThuTimeStart, endTime: data.userSetting__noticableThuTimeEnd},
                {name:"金", id:"Fri", selected: data.userSetting__noticableFriTimeStart!=data.userSetting__noticableFriTimeEnd, startTime: data.userSetting__noticableFriTimeStart, endTime: data.userSetting__noticableFriTimeEnd},
                {name:"土", id:"Sat", selected: data.userSetting__noticableSatTimeStart!=data.userSetting__noticableSatTimeEnd, startTime: data.userSetting__noticableSatTimeStart, endTime: data.userSetting__noticableSatTimeEnd},
                {name:"日", id:"Sun", selected: data.userSetting__noticableSunTimeStart!=data.userSetting__noticableSunTimeEnd, startTime: data.userSetting__noticableSunTimeStart, endTime: data.userSetting__noticableSunTimeEnd},
            ]
            this.refresh *= -1;
        },
        setInvitation(data:any[]):void{
            // 招待確認
            const tempData = [];
            for (const key in data) {
                tempData.push({
                    id: data[key].id,
                    houseName: data[key].houseId__houseName
                });
            }
            this.invitations = tempData;
        },
        logout():void{
            this.$http.get("/api/logout/").then(()=>{
                this.$store.dispatch("clear");
                localStorage.setItem("token", "");
                this.$router.push("Login");
            });
        },
        copyId():void{
            navigator.clipboard.writeText(this.userId).then(() => {
                this.alertCss = "alert-success";
                this.alertMsg = "コピーしました";
                this.alertDisplayTime = 2000;
                this.refs.alert.open();
            });
        },
        approveHouse(item:invitation):void{
            this.$http.put("/api/accept_invitation/" + item.id + "/")
            .then(()=>{
                // 承認した。
                // 招待の更新
                this.updateInvitations();

                // 入ったよのメッセージ
                this.alertCss = "alert-success";
                this.alertMsg = item.houseName + "に入りました";
                this.alertDisplayTime = 5000;
                this.refs.alert.open();
            });
        },
        async updateInvitations():Promise<void>{
            const myInvitationRes = await this.$http.get("/api/get_myinvitation/" + this.$store.state.userId + "/");
            this.setInvitation(myInvitationRes.data);
        },

        changeUserName():void{
            if(!this.userName){
                return;
            }
            const saveData = {
                username: this.userName
            };
            this.saveUserName(saveData);
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

            // trueになっている物で保存
            const statusRes = await this.$http.get("/api/statuses/")
            const saveData = {statusId:null};
            if (this.statusHima){
                saveData["statusId"] = statusRes.data.find((status:any) => status.statusName == CONST.STATUS.hima).id;
                this.$store.dispatch("setStatus", "hima");
            }else if(this.statusBusy){
                saveData["statusId"] = statusRes.data.find((status:any) => status.statusName == CONST.STATUS.busy).id;
                this.$store.dispatch("setStatus", "busy");
            }
            this.saveUserSetting(saveData);
            
        },
        changeStatusValidTime():void{
            const saveData = {
                statusValidDateTime: this.statusValidDateTime
            };
            this.saveUserSetting(saveData);
        },
        changeIsAllCategorySelected(val:any):void{
            const saveData = {
                isAllCategorySelected: val
            };
            this.saveUserSetting(saveData);
        },
        changeCategorySelect(val:any):void{
            if(val.selected){
                // create
                const saveData = {
                    userId: this.$store.state.userId,
                    categoryId: val.id,
                };
                this.$http.post("/api/user_select_category/", saveData);
            }else{
                // 削除
                this.$http.delete("/api/user_select_category/delete/"+ this.$store.state.userId +"/"+ val.id +"/" );
            }

        },
        changeWeekTime(val:weekContent):void{
            // 保存対象かどうかの確認
            if(val.startTime == "time" || val.endTime == "time"){
                return;
            }
            if(this.checkEditing(val.startTime) || this.checkEditing(val.endTime)){
                return;
            }

            // データの整合性調整
            const saveStartTime = this.getDisplayTime(val.startTime);
            let saveEndTime = this.getDisplayTime(val.endTime);
            if (saveStartTime > saveEndTime){
                val.endTime = saveStartTime;
                saveEndTime = this.getDisplayTime(val.endTime);
                this.refresh *= -1;
            }
            val.selected = val.endTime != val.startTime;

            // 保存
            const saveData:Record<string, unknown> = {};
            saveData["noticable"+val.id+"TimeStart"] = saveStartTime;
            saveData["noticable"+val.id+"TimeEnd"] = saveEndTime;
            this.saveUserSetting(saveData);
        },
        checkEditing(data:any):boolean{
            const blankHour = data?.HH == "";
            const blankMin = data?.mm == "";
            // 片方だけがブランクの場合は編集中と判断する
            const edited = blankHour == blankMin;
            return !edited;
        },
        getDisplayTime(data:any):string{
            if(!data){
                return "00:00"
            }
            if(!data.HH || !data.mm){
                return data;
            }
            return data.HH + ":" + data.mm;
        },
        saveUserName(data:any):void{
            this.$http.put("/api/update_user/" + this.$store.state.userId + "/",data).then(()=>{
                this.$store.dispatch("getUserInfo");
            });
        },
        saveUserSetting(data:any):void{
            this.$http.put("/api/user_setting/" + this.$store.state.userId + "/",data).then(()=>{
                this.$store.dispatch("getUserInfo");
            });
        }
    }
})



</script>


