<template>
    <div class="container login_container">
        <div class="login_logo">
        </div>
        <div class="card login_card_base">
            <div class="card-body">
                <form class="mb-3">
                    <div class="mb-3 text-start">
                        <input class="form-control" placeholder="ID" id="username" v-model="credentials.username">
                    </div>
                    <div class="mb-3 text-start">
                        <input type="password" class="form-control" placeholder="パスワード" id="password" v-model="credentials.password">
                    </div>
                    <button type="button" class="btn btn_primary btn_login" @click="login">ログイン</button>
                </form>
                <span class="d-flex mb-3">
                    <div class="login_dash_box login_dash_box_left"></div>
                    <div class="login_dash_box_or">OR</div>
                    <div class="login_dash_box login_dash_box_right"></div>
                </span>
                <span class="d-flex mb-1 login_firstvisiter">
                    <div class="login_firstvisiter_text">
                        はじめましての方は
                    </div>
                    <button type="button" class="btn btn_primary btn_firstvisitor" @click="firstvisitor">こちらへ</button>
                </span>
            </div>
        </div>
        <div class="alert alert-warning alert-dismissible fade" v-bind:class="{show: isError}" role="alert">
            ユーザー名かパスワードが間違っています
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
</template>

<style  lang="scss">
.login_container {
    height: 100%;
    max-width: 100% !important;
    padding: unset !important;
    background-position: center;
    background-size: cover;
    background-image: url("../../assets/img/login/woodenDoor.jpg");
    background-color: rgba(230, 255, 230, 0.2);
    background-blend-mode: soft-light;

    .login_logo{
        background-image: url("../../assets/img/logo.svg");
        background-repeat: no-repeat;
        background-position: center;
        width: 90%;
        max-width: 600px;
        height: 43%;
        margin: 0 auto;
    }
    .login_card_base{
        width: 90%;
        max-width: 600px;
        margin: 0 auto;
        background-color: rgba(58, 190, 39, 0.3);
        border-radius: 8px;
        border: 0;

        .login_dash_box{
            width: 40%;
            height: 1px;
            background-color: var(--text-color-black);
            align-self: center;
        }
        .login_dash_box_left{
            margin-right: 5%;
        }
        .login_dash_box_right{
            margin-left: 5%;
        }
        .login_dash_box_or{
            width: 10%;
            color: var(--text-color-black)
        }

        .btn_login {
            width: 200px;
            height: 50px;
        }

        .login_firstvisiter{
            align-items: center;
            justify-content: center;
            color: var(--text-color-white);
        }

        .btn_firstvisitor {
            width: 102px;
            height: 22px;
            font-size: 12px!important;
            background-size: 10px;
            margin-left: 5%;
        }
    }
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'

interface credentials {username:string,password:string}
export type DataType = {
    credentials: credentials,
    valid:boolean,
    loading:boolean,
    isError: boolean,
}

export default defineComponent({
    name: "Login",
    data(): DataType {
        return {
            credentials: {username:"",password:""},
            valid:true,
            loading:false,
            isError: false,
        }
    },
    mounted : function(){
        if(localStorage.getItem("token")){
            let next:any = this.$route.query.redirect;
            if(!this.$route.query.redirect){
                next = "House"
            }
            this.$router.push(next);
        }
        let userId = localStorage.getItem("userId");
        if(userId){
            this.credentials.username = userId;
        }
    },
    methods: {
        login() {
            this.loading = true;
            const userId = this.credentials.username;
            this.$http.post("auth/", this.credentials).then(response => {
                this.$store.dispatch("auth", {
                    userId: userId,
                    userToken: response.data.token
                });
                localStorage.setItem("userId", userId);
                localStorage.setItem("token", response.data.token);
                let next:any = this.$route.query.redirect;
                if(!this.$route.query.redirect){
                    next = "House"
                }
                this.$router.push(next);
            }).catch(e => {
                    this.loading = false;
                    this.isError = true;
            });
        },
        firstvisitor() {
            this.$router.push("FirstVisitor");
        }
    }
})
</script>


