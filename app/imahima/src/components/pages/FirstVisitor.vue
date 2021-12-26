<template>
    <div class="container fv_container">
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
                    <button type="login" class="btn btn_primary btn_login" @click="login">ログイン</button>
                </form>
            </div>
        </div>
        <div class="alert alert-warning alert-dismissible fade" v-bind:class="{show: isError}" role="alert">
            ユーザー名かパスワードが間違っています
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
</template>

<style  lang="scss">
.fv_container {
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
        height: 42%;
        margin: 0 auto;
        background-color: rgba(58, 190, 39, 0.3);
        border-radius: 8px;
        border: 0;
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
        createUser() {
            console.log("ユーザ作成")
        }
    }
}
</script>


