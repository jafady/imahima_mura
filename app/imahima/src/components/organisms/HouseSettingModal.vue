<template>
    <div class="container HSM_container">
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="house_setting_modal" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content HSM_modal">
                        <div class="HSM_header">
                            <div class="title">
                                <div class="title_icon"></div>
                                <div class="title_word">家の設定</div>
                            </div>
                            <div class="turn_back btn_imahima" data-bs-dismiss="modal"></div>
                        </div>
                        <div class="modal-body HSM_body">
                            <div class="mb-3">
                                <div class="content_title">設定</div>
                                <div class="HSM_content">
                                    <div class="m-1">
                                        <div class="content_subtitle d-flex">名前</div>
                                        <input type="text" v-model="houseName" class="text_input" placeholder="家の名前" @change="changeHouseName">
                                    </div>
                                    <div class="m-1 mt-3">
                                        <div class="content_subtitle d-flex">discordサーバURL</div>
                                        <input type="text" v-model="discordUrl" class="text_input" placeholder="https://discord.gg/" @change="changeDiscordUrl">
                                    </div>
                                    <div class="m-1 mt-3">
                                        <div class="content_subtitle d-flex">discord通知Webhook</div>
                                        <input type="text" v-model="discordNoticeUrl" class="text_input" placeholder="https://discordapp.com/api/webhooks/" @change="changeDiscordNoticeUrl">
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="content_title">友達を招待する</div>
                                <div class="HSM_content">
                                    <div class="mb-4">
                                        <div class="m-1">
                                            <button type="button" class="btn_primary_normal invite_btn" @click="createInviteUrl">招待用URLの発行</button>
                                        </div>
                                        <div v-if = "inviteUrl" class="m-1 mt-3">
                                            <div class="content_subtitle d-flex">このURLを招待したい人へ送ってください</div>
                                            <div class="mb-3 text-start d-flex">
                                                <input class="text_input inviteUrl_text" id="inviteUrl" v-model="inviteUrl" readonly>
                                                <div class="HSM_flex_dummy_body">
                                                    <button type="button" class="HSM_copy_url" id="copyUrl" @click="copyUrl"></button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="m-1">
                                        <div class="content_subtitle d-flex">IDで招待</div>
                                        <input type="text" v-model="friendId" class="text_input" placeholder="ID" @input="changeFriendId">
                                    </div>
                                    <div v-if = "friendName" class="m-1 mt-3">
                                        <div class="content_subtitle d-flex">招待したい友達はこの人ですか？</div>
                                        <input type="text" v-model="friendName" class="text_input" placeholder="" readonly>

                                        <div v-if="!alreadyRegistered">
                                            <button type="button" class="mt-3 mb-2 btn_primary_normal invite_btn" @click="inviteFriend">招待する</button>
                                        </div>
                                        <div v-else-if="registered">
                                            <div class="mt-3 mb-2">招待しました!</div>
                                        </div>
                                        <div v-else>
                                            <div class="mt-3 mb-2">すでに招待されているようです</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="content_title">友達</div>
                                <div class="HSM_content">
                                    <div v-for="(value) in houseMates" v-bind:key="value.id" class="friend">
                                        <div class="icon_area"><Icon :userId="value.id" /></div>
                                        <div>{{value.name}}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <Alert :css="alertCss" :alertMsg="alertMsg" :displayTime="alertDisplayTime" ref="alert" />
        </teleport>
    </div>
    
</template>

<style lang="scss">
.HSM_modal{
    font-family: var(--font-family);
    max-height: 90%!important;
    border: none!important;
    background-color: revert!important;
    overflow: unset!important;
    .HSM_header{
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
                left: calc(45% - 55px);
                width: 35px;
                height: 35px;
                background-image: url("../../assets/img/house/wrench.svg");
                background-repeat: no-repeat;
                background-size: contain;
                opacity: 30%;
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

    .HSM_body{
        padding-bottom: 0!important;
        background-color: var(--content-bg-color);

        .content_title{
            text-align: left;
            align-items: center;
            font-size: 21px;
        }

        .HSM_content{
            background-color: rgba(246,246,246,1);
            padding: 10px;
            border-radius: var(--content-border-radius);

            .content_subtitle{
                font-size: 15px;
            }
            .text_input{
                border: none;
                border-radius: 8px;
                padding-left: 10px;
                width: 100%;
                height: 40px;
                font-size: 18px;
            }

            .inviteUrl_text{
                padding-right: 15%;
            }

            .HSM_flex_dummy_body {
                width: 85%;
                height: 20px;
                position: absolute;
                align-self: center;
                text-align: end;
                padding-right: 5px;
                pointer-events: none;
                .HSM_copy_url {
                    background-image: url("../../assets/img/login/copy.svg");
                    background-color: rgba(0,0,0,0);
                    background-repeat: no-repeat;
                    width: 30px;
                    height: 20px;
                    border: none;
                    pointer-events: all;
                }
                .HSM_copy_url:active {
                    transform: var(--btn-active-trans);
                }
            }

            .invite_btn{
                border: none;
                width: 100%;
                height: 40px;
            }

            .friend{
                display: flex;
                align-items: center;
                justify-content: flex-start;
                align-content: center;
                margin-bottom: 10px;
                .icon_area{
                    height: 50px;
                    width: 50px;
                    margin-right: 20px;
                }
            }
            
        }

    }
    
}

</style>

<script lang="ts">
import { defineComponent } from 'vue'
import {houseMates} from '@/mixins/interface'
import { Modal } from 'bootstrap'
import CONST from '@/mixins/const'
import Icon from '@/components/molecules/Icon.vue'
import Alert from '@/components/molecules/Alert.vue'

export type DataType = {
    houseName: string,
    discordUrl: string,
    discordNoticeUrl: string,
    inviteUrl: string,
    friendId: string,
    friendName: string,
    alreadyRegistered: boolean,
    registered: boolean,

    alertCss: string,
    alertMsg: string,
    alertDisplayTime: number,
}

export default defineComponent({
    name: "HouseSettingModal",
    components: {
        Icon,
        Alert,
    },
    data(): DataType {
        return{
            houseName: "",
            discordUrl: "",
            discordNoticeUrl: "",
            inviteUrl: "",
            friendId: "",
            friendName: "",
            alreadyRegistered: false,
            registered: false,

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
        houseMates():houseMates {
            return this.$store.state.houseMates;
        },
    },
    methods: {
        openModal():void{
            // データ初期化
            this.initData();
            // データ読み込み
            this.getHouseInfo();
            
            // モーダル開く
            const target = document.getElementById('house_setting_modal');
            if(!target) return;
            const myModal = new Modal(target);
            if(!myModal) return;
            myModal.show();
        },
        initData():void{
            this.houseName = "";
            this.discordUrl = "";
            this.discordNoticeUrl = "";
            this.friendId = "";
            this.friendName = "";
            this.alreadyRegistered = false;
        },
        async getHouseInfo():Promise<void>{
            const houseInfo = await this.$http.get("/api/house_info/"+ this.houseId +"/");
            this.houseName = houseInfo.data.houseName;
            this.discordUrl = houseInfo.data.discordUrl;
            this.discordNoticeUrl = houseInfo.data.discordNoticeUrl;
        },
        changeHouseName():void{
            const saveData = {
                houseName: this.houseName
            };
            this.saveHouseInfo(saveData);
        },
        changeDiscordUrl():void{
            const saveData = {
                discordUrl: this.discordUrl
            };
            this.saveHouseInfo(saveData);
        },
        changeDiscordNoticeUrl():void{
            const saveData = {
                discordNoticeUrl: this.discordNoticeUrl
            };
            this.saveHouseInfo(saveData);
        },
        async createInviteUrl():Promise<void>{
            const sendData = {
                "houseId": this.houseId
            }
            const inviteId = await this.$http.post("/api/create_invitetoken/",sendData);
            this.inviteUrl = CONST.baseUrl + "MyPage" + "?inviteToken=" + inviteId.data.id;
        },
        copyUrl():void{
            const inviteUrl:HTMLInputElement = document.getElementById("inviteUrl") as HTMLInputElement;
            inviteUrl.select();
            document.execCommand("copy");

            this.alertCss = "alert-success";
            this.alertMsg = "コピーしました";
            this.alertDisplayTime = 5000;
            this.refs.alert.open();
        },
        async changeFriendId():Promise<void>{
            try{
                // ユーザの存在確認
                const userinfo:any = await this.$http.get("api/user_info/" + this.friendId + "/");
                if(userinfo.e || !userinfo.data[0]){
                    this.friendName = "";
                    return;
                }
                this.friendName = userinfo.data[0].username;

                // 招待済みか確認
                const housemates:any = await this.$http.get("api/check_housemate/" + this.houseId + "/" + this.friendId + "/");
                if(housemates.data[0]){
                    this.alreadyRegistered = true;
                }else{
                    this.alreadyRegistered = false;
                }
            } catch(e) {
                this.friendName = "";
            }

        },
        inviteFriend():void{
            // 招待する
            const saveData = {
                houseId: this.houseId,
                userId: this.friendId,
            };
            this.$http.post("api/create_housemate/", saveData)
            .then(()=>{
                this.registered = true;
                this.alreadyRegistered = true;
            });
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


