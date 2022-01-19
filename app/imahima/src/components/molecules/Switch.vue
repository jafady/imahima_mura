<template>
    <div class="switchArea">
        <input type="checkbox" v-bind:id="switchId" v-model="valueComputed">
        <label v-bind:for="switchId"><span></span></label>
        <label v-bind:for="switchId" id="swImg"></label>
    </div>
</template>

<style  lang="scss">
/* === ボタンを表示するエリア ============================== */
.switchArea {
    position       : relative;              /* 親要素が基点       */
    width          : 90px;                  /* ボタンの横幅       */
    background     : var(--inactive-bg-color);   /*  デフォルト背景色   */
    border-radius  : 23px;
}

/* === チェックボックス ==================================== */
.switchArea input[type="checkbox"] {
    display        : none;            /* チェックボックス非表示 */
}

/* === チェックボックスのラベル（標準） ==================== */
.switchArea label {
    display        : block;               /* ボックス要素に変更 */
    box-sizing     : border-box;          /* 枠線を含んだサイズ */
    height         : 45px;                /* ボタンの高さ       */
    border-radius  : 23px;                /* 角丸               */
}

/* === チェックボックスのラベル（ONのとき） ================ */
.switchArea input[type="checkbox"]:checked +label {
    background-color: var(--main-bg-color);
}

/* === 丸部分のSTYLE（標準） =============================== */
.switchArea #swImg {
    position       : absolute;            /* 親要素からの相対位置*/
    width          : 38px;                /* 丸の横幅           */
    height         : 38px;                /* 丸の高さ           */
    background     : rgba(255,255,255,1);             /* カーソルタブの背景 */
    top            : 4px;                 /* 親要素からの位置   */
    left           : 4px;                 /* 親要素からの位置   */
    border-radius  : 19px;                /* 角丸               */
    transition     : .2s;                 /* 滑らか変化         */
}

/* === 丸部分のSTYLE（ONのとき） =========================== */
.switchArea input[type="checkbox"]:checked ~ #swImg {
    transform      : translateX(44px);    /* 丸も右へ移動       */
}
</style>

<script>
import { toRefs, computed } from 'vue'
export default {
    name: "Switch",
    props: {
      value: Boolean,
      switchId: String
    },
    emits: ['update:value'],
    setup(props, { emit }) {
        const { value,switchId } = toRefs(props)
        const valueComputed = computed({
            get: () => value.value,
            set: (value) => {
                emit('update:value', value)
            },
        })

        return {
            valueComputed,
        }
    }
}
</script>


