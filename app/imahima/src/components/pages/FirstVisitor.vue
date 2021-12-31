<template>
    <div class="container fv_container">
        <div class="fv_card_header">
            <div class="fv_logo" />
            <div class="fv_title">新規登録</div>           
        </div>
        <div class="card fv_card_base">
            <div class="card-body fv_card_body">
                <div class="fv_create_user">
                    <div class="mt-3 mb-3">
                        <div>はじめまして。イマヒマ村へようこそ</div>
                        <div>この村はヒマなときに顔見知りでなんとなく集まって、</div>
                        <div>ヒマな人で遊ぶ場です。</div>
                    </div>
                    <div class="mb-3">
                        <div>さて、あなたは友達に誘われて</div>
                        <div>この村にやってきたはずです。</div>
                        <div>お名前を教えてください。</div>
                        <div>友達が家に招待できるようにIDを発行しましょう。</div>
                    </div>
                    <form class="mb-3">
                        <div class="mb-3 text-start">
                            <input class="form-control" placeholder="名前" id="username" v-model="user.username">
                        </div>
                        <div class="mb-3 text-start d-flex">
                            <input type="password" class="form-control" placeholder="パスワード" id="password" v-model="user.password">
                            <div class="fv_flex_dummy_body">
                                <button type="button" class="fv_close_eye" id="changePwdDisplay" @click="changePwdDisplay"></button>
                            </div>
                        </div>
                        <button type="submit" class="btn btn_primary btn_create_user" @click="createUser">ID発行</button>
                    </form>
                </div>
                <div v-if="userId" class="fv_display_id">
                    <div class="mb-3 text-start d-flex">
                        <input class="form-control" placeholder="ID" id="userId" v-model="userId" readonly="readonly">
                        <div class="fv_flex_dummy_body">
                            <button type="button" class="fv_copy_id" id="copyId" @click="copyId"></button>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div>友達にこのIDをコピーして教えてあげてください。</div>
                    </div>
                </div>
                <div v-if="houseName" class="fv_start">
                    <form class="mb-3">
                        <div class="mb-3 text-start">
                            <input class="form-control" placeholder="家の名前" id="houseName" v-model="houseName" readonly="readonly">
                        </div>
                        <button type="submit" class="btn btn_primary btn_approve_house" @click="approveHouse">承諾してスタート</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<style  lang="scss">
.fv_container {
    max-width: 100% !important;
    min-height: 100%;
    padding: unset !important;
    background-position: center;
    background-size: cover;
    background-image: url("../../assets/img/login/woodenDoor.jpg");
    background-color: rgba(230, 255, 230, 0.2);
    background-blend-mode: soft-light;
    background-attachment: fixed;

    .fv_card_header {
        width: 90%;
        max-width: 600px;
        display: inline-flex;
        align-items: flex-end;
        margin-top: 5%;
        z-index: 1;

        .fv_logo {
            background-image: url("../../assets/img/logo.svg");
            background-repeat: no-repeat;
            background-position: center;
            width: 100px;
            height: 100px;
            z-index: inherit;
        }

        .fv_title {
            background-color: var(--main-bg-color);
            border-radius: 40px;
            color: var(--text-color-white);
            font-size: 18px;
            width: calc(100% - 200px);
            z-index: inherit;
        }
    }


    .fv_card_base {
        width: 90%;
        max-width: 600px;
        margin: 0 auto;
        background-color: var(--content-bg-color);
        border-radius: 8px;
        border: 0;
        transform: translateY(-20px);

        .fv_card_body {
            font-size: 15px;
            .fv_flex_dummy_body {
                width: 90%;
                height: 20px;
                position: absolute;
                align-self: center;
                text-align: end;
                padding-right: 5px;
                pointer-events: none;
                .fv_close_eye {
                    background-image: url("../../assets/img/login/closeEye.svg");
                    background-color: rgba(0,0,0,0);
                    background-repeat: no-repeat;
                    width: 30px;
                    height: 20px;
                    border: none;
                    pointer-events: all;
                }
                .fv_open_eye {
                    background-image: url("../../assets/img/login/openEye.svg");
                    background-color: rgba(0,0,0,0);
                    background-repeat: no-repeat;
                    width: 30px;
                    height: 20px;
                    border: none;
                    pointer-events: all;
                }
                .fv_copy_id {
                    background-image: url("../../assets/img/login/copy.svg");
                    background-color: rgba(0,0,0,0);
                    background-repeat: no-repeat;
                    width: 30px;
                    height: 20px;
                    border: none;
                    pointer-events: all;
                }
                .fv_copy_id:active {
                    transform: var(--btn-active-trans);
                }
            }
            
            .btn_create_user {
                width: 50%;
                height: 48px;
            }
            .btn_approve_house {
                width: 100%;
                height: 48px;
            }
        }
    }

    
}
</style>

<script>
export default {
    name: "FirstVisitor",
    data: () => ({
            user: {
                username:"",
                password:""
            },
            userId:"",
            inviteId:"",
            houseName:"",
            valid:true,
            loading:false,
            isError: false,
        }
    ),
    methods: {
        changePwdDisplay(e) {
            const inputPwd = document.getElementById("password");
            const pwdEye = document.getElementById("changePwdDisplay");
            if( inputPwd.type === 'password' ) {
                inputPwd.type = 'text';
                pwdEye.className = "fv_open_eye";
            } else {
                inputPwd.type = 'password';
                pwdEye.className = "fv_close_eye";
            }
        },
        createUser() {
            console.log("ユーザ作成");
            const that = this;
            this.$http.post("api/create_user/", this.user).then(response => {
                console.log("ユーザ作成成功");
                that.userId =  response.data.id;
                that.login();
                that.gettingInvitation();
            }).catch(e => {
                this.loading = false;
                this.isError = true;
            });
        },
        copyId() {
            const id = document.getElementById("userId");
            id.select();
            document.execCommand("copy");
        },
        login(){
            const data = {
                "username":this.userId,
                "password":this.user.password
            }
            const that = this;
            this.$http.post("auth/", data).then(response => {
                this.$store.dispatch("auth", {
                    userId: that.userId,
                    userToken: response.data.token
                });
                localStorage.setItem("userId", that.userId);
                localStorage.setItem("token", response.data.token);
                this.$router.push(this.$route.query.redirect);
            }).catch(e => {
                    this.loading = false;
                    this.isError = true;
            });

        },
        gettingInvitation() {
            const that = this;
            const getInvitation = () =>{
                // 招待問い合わせ
                console.log("招待問い合わせ");
                this.$http.get("api/get_myinvitation/" + this.userId +"/").then(response => {
                    console.log("招待取得成功");
                    that.inviteId = response.data[0].id;
                    that.houseName = response.data[0].houseId__houseName;
                }).catch(e => {
                    this.loading = false;
                    this.isError = true;
                });
            };
            const intervalId = setInterval(
                ()=>{
                    getInvitation();
                    if(that.houseName){
                        clearInterval(intervalId);
                    }
                }, 5000
            )
        },
        approveHouse() {
            if(!this.inviteId){
                return;
            }
            this.$http.put("api/accept_invitation/" + this.inviteId + "/").then(response => {
                console.log("家承認成功");
                this.$router.push("House");
            }).catch(e => {
                this.loading = false;
                this.isError = true;
            });
        }
    }
}
</script>


