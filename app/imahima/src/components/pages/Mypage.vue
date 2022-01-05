<template>
    <div class="container mypage_container">
        <Header />
        <div class="m-3">
            <div class="mypage_content">
                <div class="mypage_content_dummy_body">
                    <div class="mypage_logout" @click="logout">
                        <div class="mypage_logout_icon" />
                        <div class="mypage_logout_word">ログアウト</div>
                    </div>
                </div>
                <div>
                    <div class="mypage_icon"></div>
                    <div class="mypage_username">{{userName}}</div>
                    <div class="mypage_id d-inline-flex">
                        <div class="mypage_id_weight"></div>
                        <div class="mypage_id">ID:{{userId}}</div>
                        <div class="mypage_id_copy btn_imahima" @click="copyId"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="m-3">
            <div class="mypage_title">ステータス設定</div>
            <div class="mypage_content">
                <div class="d-inline-flex mt-2 mypage_inline">
                    <div class="display">
                        <div class="mypage_inline_icon hima"></div>
                        <div class="mypage_inline_word">ヒマでしかない</div>
                    </div>
                    <Switch v-model:value="statusHima" :switchId="'switch1'" />
                </div>
                <div class="d-inline-flex mt-2 mypage_inline">
                    <div class="display">
                        <div class="mypage_inline_icon maybe"></div>
                        <div class="mypage_inline_word">予定ではヒマ</div>
                    </div>
                    <Switch v-model:value="statusMaybe" :switchId="'switch2'"/>
                </div>
                <div class="d-inline-flex mt-2 mypage_inline">
                    <div class="display">
                        <div class="mypage_inline_icon busy"></div>
                        <div class="mypage_inline_word">ヒマじゃない</div>
                    </div>
                    <Switch v-model:value="statusBusy" :switchId="'switch3'"/>
                </div>
            </div>
        </div>

        <div class="m-3">
            <div class="mypage_title">通知設定</div>
            <div class="mypage_content">
                <div class="d-inline-flex mt-2 mypage_inline">
                    <div class="display">
                        <div class="mypage_inline_word">カテゴリにこだわらない</div>
                    </div>
                    <Switch v-model:value="isAllCategorySelected" :switchId="'switchNotice'" />
                </div>
                <div class="mt-2">
                    <div class="mypage_content_title d-flex">カテゴリ選択</div>
                    <div class="mypage_category_area">
                        <div v-for="(items, bulkIndex) in groupedCategorys" :key="bulkIndex" class="mypage_button_area_bulk">
                            <div v-for="(item, index) in items" :key="index" class="mypage_button_area">
                                <input type="checkbox" v-model="item.selected" :id="bulkIndex + '_' + index">
                                <label class="btn_category btn_imahima" :for="bulkIndex + '_' + index">{{item.name}}</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="m-3">
            <div class="mypage_title">通知日時</div>
            <div class="mypage_content">
                <div class="mt-2">
                    <div class="mypage_content_title d-flex">通知可能時間</div>
                    <div class="d-inline-flex mt-2 mypage_inline_noticable">
                        <VueTimepicker input-class="time" format="HH:mm" v-model="noticableTimeStart" :minute-interval="10" hide-clear-button></VueTimepicker>
                        <div class="hyphen">~</div>
                        <VueTimepicker input-class="time" format="HH:mm" v-model="noticableTimeEnd" :minute-interval="10" hide-clear-button></VueTimepicker>                        
                    </div>
                </div>
                <div class="mt-2">
                    <div class="mypage_content_title d-flex">通知可能曜日</div>
                    <div class="mypage_week_area">
                        <div v-for="(item, index) in week" :key="index" class="mypage_week_button_area">
                            <input type="checkbox" v-model="item.selected" :id="index">
                            <label class="btn_week btn_imahima" :for="index">{{item.name}}</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="m-3 mypage_blank" />
        
    </div>
</template>

<style  lang="scss">
.mypage_container {
    min-height: 100%;
    max-width: 100% !important;
    padding: unset !important;

    .mypage_title{
        text-align: left;
        align-items: center;
    }

    .mypage_content{
        background-color: rgba(246,246,246,1);
        padding: 5px;
        border-radius: var(--content-border-radius);

        .mypage_content_dummy_body{
            width: calc(100% - 40px);
            position: absolute;
            align-self: center;
            padding-right: 10px;
            pointer-events: none;
            display: flex;
            justify-content: flex-end;

            .mypage_logout{
                pointer-events: all;
                height:50px;
                width:50px;
                .mypage_logout_icon{
                    background-image: url("../../assets/img/mypage/logout.svg");
                    width: 50px;
                    height: 35px;
                    background-repeat: no-repeat;
                    background-position: center;
                }
                .mypage_logout_word{
                    width:100%;
                    font-size:10px
                }
            }
        }
        .mypage_icon{
            height: 100px;
            width: 100px;
            background-color: #c9e8aa;
            border-radius: 50px;
            background-position: center;
            margin: 0 auto;
        }
        .mypage_username{
            font-size: 35px;
        }
        .mypage_id{
            font-size: 21px;
            align-items: center;
        }
        .mypage_id_copy{
            background-image: url("../../assets/img/mypage/copy.svg");
            width: 40px;
            height: 40px;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 28px 28px;
            background-color: white;
            border-radius: 24px;
            margin-left: 15px;
            box-shadow: 3px 7px 2px rgb(0 0 0 / 10%);
        }
        .mypage_id_weight{
            width: 40px;
            height: 40px;
            margin-right: 15px;
        }

        .mypage_inline{
            align-items: center;
            justify-content: space-between;
            width: 100%;

            .display{
                display: inline-flex;
                align-items: center;
                
                .mypage_inline_icon{
                    width: 40px;
                    height: 40px;
                    border-radius: 20px;
                    margin-right: 5px;
                }
                .hima{
                    background-color: var(--status-color-hima);
                }
                .maybe{
                    background-color: var(--status-color-maybe);
                }
                .busy{
                    background-color: var(--status-color-busy);
                }
            }
        }
        .mypage_category_area{
            display: flex;
            overflow-x: auto;
            white-space: nowrap;
            .mypage_button_area_bulk{
                width: 125px;
                height: 130px;
                white-space: normal;
                margin-right: 10px;
                .mypage_button_area{
                    width: 125px;
                    height: 45px;
                    margin-top: 10px;

                    .btn_category{
                        background-color: var(--inactive-bg-color);
                        border-radius: 23px;
                        color: var(--text-color-gray);
                        font-size: 18px;
                        box-shadow: var(--box-shadow);
                        width: 125px;
                        height: 45px;
                        white-space: pre;
                        overflow-x: scroll;
                        overflow-y: hidden;
                        padding: 10px 6px;
                        -ms-overflow-style: none;
                    }
                    .btn_category::-webkit-scrollbar {
                        display:none;
                    }
                    input[type="checkbox"] {
                        display : none;            /* チェックボックス非表示 */
                    }
                    input[type="checkbox"]:checked +label {
                        background-color: var(--main-bg-color);
                        color: var(--text-color-white);
                        box-shadow:none;
                    }
                }
            }
        }

        .mypage_inline_noticable{
            width: 100%;
            align-items: center;

            .time{
                width: 125px;
                height: 40px;
                border: none;
                border-radius: 8px;
            }
            .hyphen{
                width: 30px;
            }
        }

        .mypage_week_area{
            display: flex;
            overflow-x: auto;
            white-space: nowrap;

            .mypage_week_button_area{
                width: 45px;
                height: 60px;
                margin-top: 10px;
                margin-right: 10px;

                .btn_week{
                    background-color: var(--inactive-bg-color);
                    border-radius: 23px;
                    color: var(--text-color-gray);
                    font-size: 20px;
                    box-shadow: var(--box-shadow);
                    width: 45px;
                    height: 45px;
                    padding: 8px;
                }
                input[type="checkbox"] {
                    display : none;            /* チェックボックス非表示 */
                }
                input[type="checkbox"]:checked +label {
                    background-color: var(--main-bg-color);
                    color: var(--text-color-white);
                    box-shadow:none;
                }
            }
        }
    }
    .mypage_blank{
        height: 10px;
    }
}
</style>

<script>
import VueTimepicker from 'vue3-timepicker'
import 'vue3-timepicker/dist/VueTimepicker.css'

import Header from '../organisms/Header.vue'
import Switch from '../molecules/Switch.vue'
export default {
    name: "MyPage",
    components: {
        VueTimepicker,
        Header,
        Switch,
    },
    data: () => ({
            userId: "efcjpo",
            userName: "田中 浩一",

            statusHima: true,
            statusMaybe: false,
            statusBusy: true,
            
            isAllCategorySelected: false,
            categorys:[
                {name:"ボードゲーム",selected:true},
                {name:"ボルダリング",selected:true},
                {name:"TRPG",selected:false},
                {name:"スカイダイビング",selected:false},
                {name:"雑談",selected:false},
                {name:"ダイビング",selected:false},
                {name:"山登り",selected:false},
            ],
            
            noticableTimeStart:"19:00",
            noticableTimeEnd:"23:00",
            week:[
                {name:"月",selected:true},
                {name:"火",selected:false},
                {name:"水",selected:true},
                {name:"木",selected:true},
                {name:"金",selected:true},
                {name:"土",selected:true},
                {name:"日",selected:true},
            ],

            valid:true,
            loading:false,
            isError: false,
        }
    ),
    // mounted : function(){
    // },
    computed: {
        groupedCategorys(){
            const base = this.categorys.length
            const splitCnt = 2       // 何個ずつに分割するか
            const groupedCategorys = []
            for (let i=0; i<Math.ceil(base/splitCnt); i++) {
                let multipleCnt = i * splitCnt  // splitCnt
                // (i * splitCnt)番目から(i * splitCnt + splitCnt)番目まで取得
                let result = this.categorys.slice(multipleCnt, multipleCnt + splitCnt) 
                groupedCategorys.push(result)
            }
            return groupedCategorys
        },
    },
    methods: {
        logout() {
            localStorage.setItem('token', '');
            this.$router.push('Login');
        },
        copyId() {
            navigator.clipboard.writeText(this.userId).then(e => {
                alert('コピーしました');
            });
        },
    }
}
</script>


