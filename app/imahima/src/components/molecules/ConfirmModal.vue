<template>
    <div class="container confirm_container">
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="confirm_modal" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content confirm_modal">
                        <div class="modal-body confirm_body">
                            <div>{{msg}}</div>
                        </div>
                        <div class="confirm_footer">
                            <button type="button" class="btn btn_primary_normal confirm_btn" data-bs-dismiss="modal" @click="confirmOK">はい</button>
                            <button type="button" class="btn btn_cancel confirm_btn" data-bs-dismiss="modal" @click="confirmCancel">キャンセル</button>
                        </div>
                    </div>
                </div>
            </div>
        </teleport>
    </div>
</template>

<style lang="scss">
.confirm_modal{
    width: 80%!important;
    background-position: center!important;
    margin: 0 auto!important;
    border: none!important;
}
.modal-content{
    overflow: unset!important;
}
.confirm_body{
    padding-bottom: 0!important;
    background-color: var(--content-bg-color);
    overflow: unset!important;
    text-align: center;
    min-height: 60px;
    .confirm_content{
        background-color: rgba(246,246,246,1);
        padding: 10px;
        border-radius: var(--content-border-radius);
        .confirm_inline{
            align-items: center;
            justify-content: space-between;
            width: 100%;

            
        }
        
    }
}
.confirm_footer{
    display: flex;
    align-content: center;
    justify-content: space-evenly;
    align-items: center;
    height: 60px;
    background-color: var(--content-bg-color);

    .confirm_btn{
        width: 100px;
    }
}


</style>

<script lang="ts">
import { defineComponent } from 'vue'
import utils from '@/mixins/utils'
import { Modal } from 'bootstrap'

export type DataType = {
    msg: string,
}

export default defineComponent({
    name: "ConfirmModal",
    components: {
        
    },
    // setup(): Record<string, any>{
    //     const { sortTime,cutSeconds, sendWebsocket,getDisplayTime } = utils()
    //     return{
    //         sortTime,
    //         cutSeconds,
    //         sendWebsocket,
    //         getDisplayTime
    //     }
    // },
    data(): DataType {
        return{
            msg: ""
        }
    },
    // computed: {
        
    // },
    methods: {
        openModal(msg:string):void{
            this.msg = msg;
            // モーダル開く
            const target = document.getElementById('confirm_modal');
            if(!target) return;
            const myModal = new Modal(target);
            if(!myModal) return;
            myModal.show();
        },
        closeModal():void{
            const target = document.getElementById('confirm_modal');
            if(!target) return;
            const myModal = Modal.getInstance(target);
            if(!myModal) return;
            myModal.hide();
        },
        confirmOK():void{
            this.$emit("ok");
        },
        confirmCancel():void{
            this.$emit("cancel");
        },
        // async initData():Promise<void>{
            
        // },
    }
})



</script>


