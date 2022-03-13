<template>
    <div class="header d-flex">
        <div class="header_info">
            <div class="header_info_icon" @click="displaySideMenu"></div>
        </div>
        <svg class="header_house_logo" @click="goHouse"/>
        <div class="header_mypage" :class="statusCss" @click="goMyPage">
            <img :src="myIcon" class="icon_image" />
        </div>
    </div>
    <SideMenuModal ref="sideMenuModal" />
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
            background-image: url("../../assets/img/hamburger_menu.svg");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            height: 25px;
            width: 30px;
            margin: 0 auto;
            margin-top: 13px;
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
import SideMenuModal from '@/components/organisms/SideMenuModal.vue'
export type DataType = {
}

export default defineComponent({
    name: "Header",
    components: {
        SideMenuModal,
    },
    data(): DataType {
        return{
        }
    },
    computed: {
        refs():any {
            return this.$refs;
        },
        statusCss(): string{
            return "icon_bg_" + this.$store.state.userStatus
        },
        myIcon(): string | ArrayBuffer | null{
            if(!this.$store.state.userIcon || this.$store.state.userIcon == require("@/assets/img/default_icon.png")){
                this.$store.dispatch("getUserInfo")
            }
            return this.$store.state.userIcon;
        },

    },
    methods: {
        displaySideMenu(e:Event):void {
            e.stopPropagation();
            this.refs.sideMenuModal.openModal();
        },
        goHouse():void {
            this.$router.push('House');
        },
        goMyPage(e:Event):void {
            e.stopPropagation();
            this.$router.push('MyPage');
        }
    }
})
</script>


