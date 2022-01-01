<template>
    <div class="container mypage_container">
        <div>
            <button class="btn btn-primary" @click="logout">ログアウト</button>
        </div>
    </div>
</template>

<style  lang="scss">
.mypage_container {
    height: 100%;
    max-width: 100% !important;
    padding: unset !important;
    background-position: center;
    background-size: cover;
    background-image: url("../../assets/img/login/woodenDoor.jpg");
    background-color: rgba(230, 255, 230, 0.2);
    background-blend-mode: soft-light;

    
}
</style>

<script>
export default {
    name: "MyPage",
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
        logout() {
            localStorage.setItem('token', '');
            this.$router.push('Login');
        }
    }
}
</script>


