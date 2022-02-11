<template>
    <teleport to="body">
        <div v-if="show" class="alert imahima_alert alert-dismissible" :class="css" role="alert">
            {{alertMsg}}
            <button type="button" class="btn-close" @click="close"></button>
        </div>
    </teleport>
</template>

<style  lang="scss">
.imahima_alert {
    position: fixed!important;
    bottom: 0;
    width: 100%;
    text-align: center;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'

export type DataType = {
    show:boolean,
}
export default defineComponent({
    name: "Alert",
    data(): DataType {
        return{
            show: false,
        }
    },
    props: {
        css: String,
        alertMsg: String,
        displayTime: Number,
    },
    methods: {
        open():void{
            this.show = true;
            if(this.displayTime){
                setTimeout(this.close, this.displayTime);
            }
        },
        close():void{
            this.show = false;
        },
    },
})
</script>


