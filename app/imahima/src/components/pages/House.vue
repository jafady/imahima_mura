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


