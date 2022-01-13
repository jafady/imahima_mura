<template>
    <div class="container IUM_container">
        <button @click="modalOpen = true">
            Open full screen modal! (With teleport!)
        </button>
        <teleport to="body">
            <div v-if="modalOpen" class="modal">
                <div>
                    I'm a teleported modal! 
                    (My parent is "body")
                <button @click="modalOpen = false">
                    Close
                </button>
                </div>
            </div>
        </teleport>
    </div>
</template>

<style  lang="scss">
.modal {
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  background-color: rgba(0,0,0,.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: white;
  width: 300px;
  height: 300px;
  padding: 5px;
}
</style>

<script lang="ts">

export type DataType = {
    modalOpen: boolean
}

export default {
    name: "IconUploadModal",
    components: {
    },
    data(): DataType {
        return{
            modalOpen: false,
        }
    },
    // created: function():void{
    // },
    // mounted : function():void{
    // },
    // watch: {
    // },
    // methods: {
    // }
}



</script>


