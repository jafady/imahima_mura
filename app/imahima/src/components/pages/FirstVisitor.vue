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
                            <input class="form-control" placeholder="名前" id="username" v-model="credentials.username">
                        </div>
                        <div class="mb-3 text-start d-flex">
                            <input type="password" class="form-control" placeholder="パスワード" id="password" v-model="credentials.password">
                            <div class="fv_flex_dummy_body">
                                <button type="button" class="fv_close_eye" id="changePwdDisplay" @click="changePwdDisplay"></button>
                            </div>
                        </div>
                        <button type="submit" class="btn btn_primary btn_create_user" @click="createUser">ID発行</button>
                    </form>
                </div>
                <div class="fv_display_id">
                    <div class="mb-3 text-start d-flex">
                        <input class="form-control" placeholder="ID" id="userId" v-model="credentials.userId" readonly="readonly">
                        <div class="fv_flex_dummy_body">
                            <button type="button" class="fv_copy_id" id="copyId" @click="copyId"></button>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div>友達にこのIDをコピーして教えてあげてください。</div>
                    </div>
                </div>
                <div class="fv_start">
                    <form class="mb-3">
                        <div class="mb-3 text-start">
                            <input class="form-control" placeholder="家の名前" id="housename" v-model="credentials.housename" readonly="readonly">
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
        background-color: rgba(230,238,232,1);
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
                .fv_close_eye {
                    background-image: url("../../assets/img/login/closeEye.svg");
                    background-color: rgba(0,0,0,0);
                    background-repeat: no-repeat;
                    width: 30px;
                    height: 20px;
                    border: none;
                }
                .fv_open_eye {
                    background-image: url("../../assets/img/login/openEye.svg");
                    background-color: rgba(0,0,0,0);
                    background-repeat: no-repeat;
                    width: 30px;
                    height: 20px;
                    border: none;
                }
                .fv_copy_id {
                    background-image: url("../../assets/img/login/copy.svg");
                    background-color: rgba(0,0,0,0);
                    background-repeat: no-repeat;
                    width: 30px;
                    height: 20px;
                    border: none;
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
            credentials: {},
            valid:true,
            loading:false,
            isError: false,
        }
    ),
    // mounted : function(){
    // },
    methods: {
        changePwdDisplay(e) {
            let inputPwd = document.getElementById("password");
            let pwdEye = document.getElementById("changePwdDisplay");
            if( inputPwd.type === 'password' ) {
                inputPwd.type = 'text';
                pwdEye.className = "fv_open_eye";
            } else {
                inputPwd.type = 'password';
                pwdEye.className = "fv_close_eye";
            }
        },
        createUser() {
            console.log("ユーザ作成")
        },
        copyId() {
            console.log("IDコピー")
        },
        approveHouse() {
            console.log("家承認")
        }
    }
}
</script>


