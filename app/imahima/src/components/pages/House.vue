<template>
    <div class="container house_container">
        <Header />
        <div>
            <button class="btn btn-primary" @click="logout">ログアウト</button>
        </div>
    </div>
</template>

<style  lang="scss">
.house_container {
    min-height: 100%;
    max-width: 100% !important;
    padding: unset !important;
    background-position: top;
    background-size: auto;
    background-image: url("../../assets/img/house/flooring.png");
    background-color: rgba(0, 0, 0, 0.4);
    background-blend-mode: hard-light;

    .header{
        height:70px;
        width:100%;

        justify-content: space-around;
        align-items: center;
        background: linear-gradient(rgba(255,255,255,1),rgb(200 200 200));

        .info{
            height: 50px;
            width: 50px;
            .info_mark{
                font-size: 28px;
                font-weight: bold;
                transform: translateY(-5px);
            }
            .info_word{
                font-size: 11px;
                font-weight: bold;
                transform: translateY(-10px);
            }
        }

        .house_logo{
            background-image: url("../../assets/img/logo.svg");
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
            height: 50px;
            width: 50px;
        }
        .mypage{
            height: 50px;
            width: 50px;
            background-color: #c9e8aa;
            border-radius: 25px;
        }
    }
    
    
}
</style>

<script>
import Header from '../organisms/Header.vue'

export default {
    name: "House",
    components: {
        Header,
    },
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


