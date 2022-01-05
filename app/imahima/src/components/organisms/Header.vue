<template>
    <div class="header d-flex">
        <div class="header_info">
            <div class="header_info_icon">?</div>
            <div class="header_info_word">ご案内</div>
        </div>
        <svg class="header_house_logo" @click="goHouse"/>
        <div class="header_mypage"  @click="goMyPage" />
    </div>
</template>

<style  lang="scss">
.header{
    height:70px;
    width:100%;

    justify-content: space-around;
    align-items: center;
    background: linear-gradient(rgba(255,255,255,1),rgb(200 200 200));

    .header_info{
        height: 50px;
        width: 50px;
        .header_info_icon{
            font-size: 28px;
            font-weight: bold;
            transform: translateY(-5px);
        }
        .header_info_word{
            font-size: 11px;
            font-weight: bold;
            transform: translateY(-10px);
        }
    }

    .header_house_logo{
        background-image: url("../../assets/img/logo.svg");
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
        height: 50px;
        width: 50px;
    }
    .header_mypage{
        height: 50px;
        width: 50px;
        background-color: #c9e8aa;
        border-radius: 25px;
    }
}
</style>

<script>
export default {
    name: "Header",
    data: () => ({
            credentials: {},
            valid:true,
            loading:false,
            isError: false,
        }
    ),
    methods: {
        goHouse() {
            this.$router.push('House');
        },
        goMyPage() {
            this.$router.push('MyPage');
        }
    }
}
</script>


