<template>
    <div class="header d-flex">
        <div class="header_info">
            <div class="header_info_icon">?</div>
            <div class="header_info_word">ご案内</div>
        </div>
        <svg class="header_house_logo" @click="goHouse"/>
        <div class="header_mypage" :class="statusCss" @click="goMyPage">
            <img :src="myIcon" class="icon_image" />
        </div>
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
        border-radius: 50%;

        .icon_image{
            width: 90%;
            margin-top: 5%;
            background-color: white;
            border-radius: 50%;
        }
    }
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'

export type DataType = {
    myIcon: string | ArrayBuffer | null,
}

export default defineComponent({
    name: "Header",
    data(): DataType {
        return{
            myIcon: require("../../assets/img/default_icon.png")
        }
    },
    computed: {
        statusCss(): string{
            return "icon_bg_" + this.$store.state.userStatus
        }
    },
    mounted : function():void{
        if(this.$store.state.userIcon){
            this.myIcon = this.$store.state.userIcon;
        }else{
            this.$store.dispatch("getUserInfo").then(()=>{
                this.myIcon = this.$store.state.userIcon;
            });
        }
    },
    methods: {
        goHouse() {
            this.$router.push('House');
        },
        goMyPage() {
            this.$router.push('MyPage');
        }
    }
})
</script>


