<template>
    <div class="container SMM_container">
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="side_menu_modal" aria-hidden="true">
                <div class="modal-dialog modal-dialog-scrollable">
                    <div class="modal-content SMM_modal">
                        <div class="SMM_header">
                            <svg class="header_house_logo" />
                        </div>
                        <div class="SMM_border"></div>
                        <div class="modal-body SMM_body">
                            <div class="SMM_inline mb-1" @click="goHouse">
                                <svg class="side_menu_icon link_house_logo" />
                                <div class="link_word">家に帰る</div>
                            </div>
                            <div class="SMM_inline mb-1" @click="goMyPage">
                                <div class="side_menu_icon"><Icon :userId="userId" :hideStatus="true"/></div>
                                <div class="link_word">マイページ</div>
                            </div>
                            <div class="SMM_inline mb-1" @click="goDevelop">
                                <svg class="side_menu_icon link_develop_logo" />
                                <div class="link_word">開拓</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </teleport>
    </div>
</template>

<style lang="scss">
.modal.fade .modal-dialog {
    transition: transform .3s ease-out;
    transform: translate(-50px,0px) !important;
}
.modal.show .modal-dialog {
    transform: none !important;
}
.modal-dialog{
    margin: unset!important;
}
.SMM_modal{
    max-height: 90%!important;
    width: 200px!important;
    border: none!important;
    border-radius: 0 8px 8px 0!important;
    background-color: var(--inactive-bg-color2)!important;
    overflow: unset!important;
    
    .SMM_header{
        height: 55px;
        margin: 10px auto;
        .header_house_logo{
            background-image: url("../../assets/img/logo.svg");
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
            height: 50px;
            width: 50px;
        }
    }
    .SMM_border{
        border-bottom: rgba(112,112,112,1);
        border-bottom-style: solid;
        border-bottom-width: 0.5px;
    }

    .SMM_body{
        padding-bottom: 0!important;
        padding: unset!important;
        .SMM_inline{
            display: flex;
            align-items: center;
            justify-content: flex-start;
            width: 100%;
            height: 50px;
            
            
            .link_word{
                margin-left: 15px;
            }
            .side_menu_icon{
                height: 30px;
                width: 30px;
                margin-left: 20px;
            }
            .link_house_logo{
                background-image: url("../../assets/img/logo.svg");
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
            .link_develop_logo{
                background-image: url("../../assets/img/wrench.svg");
                background-repeat: no-repeat;
                background-position: center;
            }
        }
        .SMM_inline:hover{
            background-color: var(--content-bg-color);
        }
    }
    
}

</style>

<script lang="ts">
import { defineComponent } from 'vue'
import { Modal } from 'bootstrap'
import Icon from '@/components/molecules/Icon.vue'

export type DataType = {

}

export default defineComponent({
    name: "SideMenuModal",
    components: {
        Icon,
    },
    data(): DataType {
        return{
            
        }
    },
    computed: {
        userId():string {
            return this.$store.state.userId;
        },
    },
    methods: {
        openModal():void{
            const target = document.getElementById('side_menu_modal');
            if(!target) return;
            const myModal = new Modal(target);
            if(!myModal) return;
            myModal.show();
        },
        closeModal():void{
            const target = document.getElementById('side_menu_modal');
            if(!target) return;
            const myModal = Modal.getInstance(target);
            if(!myModal) return;
            myModal.hide();
        },
        goHouse():void {
            this.closeModal();
            this.$router.push('House');
        },
        goMyPage():void {
            this.closeModal();
            this.$router.push('MyPage');
        },
        goDevelop():void {
            this.closeModal();
            window.open('https://github.com/jafady/imahima_mura/issues', '_blank');
        },
    }
})



</script>


