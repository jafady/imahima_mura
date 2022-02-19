<template>
    <div class="container house_event_container">
        <!-- 部屋検索 -->
        <div class="search_event">
            <div class="event_header">
                <div class="event_header_icon search_icon"></div>
                <div class="event_header_word">検索</div>
            </div>
            <div class="search_content"></div>
        </div>
        <!-- 開催中の部屋 -->
        <div class="insession_event mt-4">
            <div class="event_header">
                <div class="event_header_icon insession_icon"></div>
                <div class="event_header_word">誘い</div>
            </div>
            <div class="insession_content"></div>
        </div>
        <!-- 部屋を作るボタン -->
        <!--
        <div class="mt-4 make_house">
            <button type="button" class="btn btn_primary btn_make_event content_center_inline" @click="makeEvent">
                <div class="make_event_icon"></div>
                <div class="make_event_word">部屋を作る</div>
            </button>
        </div>
        -->
    </div>
</template>

<style lang="scss">
.house_event_container {
    min-height: 100%;
    max-width: 100% !important;
    padding: unset !important;

    .event_header{
        height: 40px;
        background-color: var(--main-bg-color);
        border-radius: 8px 0px 0px 0px;
        clip-path: polygon(0% 100%, 0% 0%, 45% 0%, 60% 90%, 100% 90%, 100% 100%);
        box-sizing: border-box;
        align-items: center;
        display: flex;
        padding: 5px;
        .event_header_icon{
            width: 42px;
            height: 40px;
            background-repeat: no-repeat;
        }
        .search_icon{
            background-image: url("../../assets/img/house/event/fly_cupid.svg");
        }
        .insession_icon{
            background-image: url("../../assets/img/house/event/sit_cupid.svg");
        }
        .event_header_word{
            padding-right: 30px;
            font-size: 18px;
            font-weight: bold;
            color: var(--text-color-white);
        }

    }

    .search_event{
        width: 90%;
        margin: 0 auto;
        // .search_header{
        //     height: 40px;
        //     background-color: var(--main-bg-color);
        //     border-radius: 8px 0px 0px 0px;
        //     clip-path: polygon(0% 100%, 0% 0%, 40% 0%, 50% 90%, 100% 90%, 100% 100%);
        //     box-sizing: border-box;
        //     align-items: center;
        //     display: flex;
        //     padding: 5px;
        //     .search_icon{
        //         width: 42px;
        //         height: 40px;
        //         background-image: url("../../assets/img/house/event/fly_cupid.svg");
        //         background-repeat: no-repeat;
        //     }
        //     .search_word{
        //         padding-right: 30px;
        //         font-size: 18px;
        //         font-weight: bold;
        //         color: var(--text-color-white);
        //     }

        // }
        .search_content{
            height: 95px;
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
        }
    }
    .insession_event{
        width: 90%;
        margin: 0 auto;
        
        .insession_content{
            height: 216px;
            background-color: var(--content-bg-color);
            border-radius: 0px 0px 8px 8px;
        }
    }

}
</style>

<script lang="ts">
import { defineComponent } from 'vue'

export type DataType = {
    friendMode: string,
}

export default defineComponent({
    name: "HouseEvent",
    components: {
    },
    data(): DataType {
        return {
            friendMode: "hima",
        }
    },
    computed: {
        isHimaMode():boolean {
            return this.friendMode == "hima";
        },
        isMaybeMode():boolean {
            return this.friendMode == "maybe";
        },

    },
    // mounted : function(){
    // },
    methods: {
    }
})
</script>


