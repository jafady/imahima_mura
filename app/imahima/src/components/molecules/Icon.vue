<template>
    <div class="iconArea">
        <div class="icon_base" :class="statusCss">
            <img :src="icon" class="icon_image" />
        </div>
    </div>
</template>

<style  lang="scss">
.iconArea {
    position: relative;              /*   親要素が基点     */
    width: 100%;                  
    height: 100%;
    .icon_base {
        width: 100%;                  
        height: 100%;
        border-radius: 50%;
        .icon_image {
            width: 90%;                  
            height: 90%;
            margin-top: 5%;
            background-color: white;
            border-radius: 50%;
        }
    }
}


</style>

<script>
import { defineComponent } from 'vue'
export default defineComponent({
    name: "Icon",
    props: {
      userId: String
    },
    computed: {
        icon(){
            return this.$store.state.houseMates[this.userId].icon || require("@/assets/img/default_icon.png");
        },
        statusCss(){
            return "icon_bg_" + this.$store.state.houseMates[this.userId].nowStatus;
        },
    },
})
</script>


