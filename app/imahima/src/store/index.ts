import { createStore } from 'vuex'
import Axios, {AxiosRequestConfig} from 'axios'
Axios.defaults.baseURL = process.env.VUE_APP_API_ENDPOINT_PROTOCOL +"://"+process.env.VUE_APP_API_ENDPOINT_HOST+"/";
Axios.interceptors.request.use((config: AxiosRequestConfig) => {
    if(config.headers && localStorage.getItem('token')){
        config.headers.Authorization = "Token " + localStorage.getItem('token')
    }
    return config
});
import CONST from '../components/const'
import utils from '@/mixins/utils'
import {houseMates} from '@/mixins/interface'

export interface LatestNotice {
  houseId: string,
  latestNoticeTimeOM: Date,
  latestNoticeHouseMatesNumOM: number
}

export interface State {
  userId: string,
  userToken: string,
  userName: string,
  userIcon: string,
  userStatus: string,
  houseId: string,
  houseMates: houseMates,
  websocket: WebSocket | null,
  noticeIntervalMinOM: number,
  latestNoticeData: {[key:string]:LatestNotice},

  latestNoticeTimeOM: Date,
  latestNoticeHouseMatesNumOM: number
}

export default createStore<State>({
  state: {
    userId: "",
    userToken: "",
    userName: "",
    userIcon: require("../assets/img/default_icon.png"),
    userStatus: "hima",
    houseId: "",
    houseMates: {},
    websocket: null,
    noticeIntervalMinOM: 1,
    latestNoticeData: {},

    latestNoticeTimeOM: new Date(),
    latestNoticeHouseMatesNumOM: 0,
  },
  mutations: {
    clear(state) {
      state.userId = "";
      state.userToken = "";
      state.userName = "";
      state.userIcon = require("../assets/img/default_icon.png");
      state.userStatus = "hima";
    },
    loginUser(state, user) {
      state.userId = user.userId;
      state.userToken = user.userToken;
    },
    userInfo(state, userInfo) {
      state.userName = userInfo.userName;
      state.userStatus = userInfo.userStatus;
      if(userInfo.userIcon){
        state.userIcon = userInfo.userIcon;
      }
    },
    setUserIcon(state, userIcon){
      if(userIcon){
        state.userIcon = userIcon;
      }
    },
    setStatus(state, userStatus){
      state.userStatus = userStatus;
    },
    setHouseId(state, houseId){
      state.houseId = houseId;
    },
    setHouseMates(state, houseMates){
      state.houseMates = houseMates;
    },
    setOneHouseMate(state, data){
      state.houseMates[data.id] = {
        id: data.id,
        name: data.name,
        icon: data.icon,
        noticableStartTime: data.noticableStartTime,
        noticableEndTime: data.noticableEndTime,
        nowStatus: data.nowStatus,
        statusValidDateTime: data.statusValidDateTime,
      }
    },
    setWebsocket(state, websocket){
      state.websocket = websocket;
    },
    setNoticeIntervalMinOM(state, noticeIntervalMinOM){
      state.noticeIntervalMinOM = noticeIntervalMinOM;
    },
    setlatestNoticeData(state, latestNoticeData){
      state.latestNoticeData[latestNoticeData.houseId] = {
        houseId: latestNoticeData.houseId,
        latestNoticeTimeOM: latestNoticeData.latestNoticeTimeOM,
        latestNoticeHouseMatesNumOM: latestNoticeData.latestNoticeHouseMatesNumOM
      }
    },

    setLatestNoticeTimeOM(state, latestNoticeTimeOM){
      state.latestNoticeTimeOM = latestNoticeTimeOM;
    },
    setLatestNoticeHouseMatesNumOM(state, latestNoticeHouseMatesNumOM){
      state.latestNoticeHouseMatesNumOM = latestNoticeHouseMatesNumOM;
    },
    
  },
  actions: {
    clear(context) {
      context.commit('clear');
    },
    auth(context, user) {
      context.commit('loginUser', user);
    },
    async getUserInfo(context, userId) {
      userId = userId || context.state.userId;
      await Axios.get("/api/user_base_info/" + userId + "/").then((response:any) => {
        const { getStatusByName } = utils();
        const res = response.data[0];
        const userIcon = res.userSetting__icon? CONST.BASE64.header + res.userSetting__icon: null;
        const userInfo = {
          userName: res.username,
          userIcon: userIcon,
          userStatus: getStatusByName(res.nowStatus)
        }
        context.commit('userInfo', userInfo);

        // ユーザ一覧中の情報も更新する
        const data = {
          id: res.id,
          name: res.username,
          icon: userIcon,
          noticableStartTime: res.todayStartTime,
          noticableEndTime: res.todayEndTime,
          nowStatus: getStatusByName(res.nowStatus),
          statusValidDateTime: res.userSetting__statusValidDateTime
        }
        context.commit('setOneHouseMate', data);
      })
    },
    setUserIcon(context, icon){
      const userIcon = icon? CONST.BASE64.header + icon: null;
      context.commit('setUserIcon', userIcon);
    },
    setStatus(context, userStatus) {
      context.commit('setStatus', userStatus);
    },
    setHouseId(context, houseId){
      context.commit('setHouseId', houseId);
    },
    async getHouseUsers(context) {
      // 家のIDを基に住民情報取得
      // アイコンの呼び出しなどで仕様するため、共通変数に入れる
      await Axios.get("/api/users/" + context.state.houseId + "/").then((response:any) => {
        const { getStatusByName } = utils();
        const data:any = {};
        const res = response.data
        for (const key in res) {
          const userIcon = res[key].userSetting__icon? CONST.BASE64.header + res[key].userSetting__icon: null;
          data[res[key].id] = {
            id: res[key].id,
            name: res[key].username,
            icon: userIcon,
            noticableStartTime: res[key].todayStartTime,
            noticableEndTime: res[key].todayEndTime,
            nowStatus: getStatusByName(res[key].nowStatus),
            statusValidDateTime: res[key].userSetting__statusValidDateTime,
          }
        }
        context.commit('setHouseMates', data);
      });
    },
    setWebsocket(context, websocket){
      context.commit('setWebsocket', websocket);
    },
    connectWebsocket(context){
      if(context.state.websocket != null) {
        return;
      }
      const token = localStorage.getItem("token");
      const socket = new WebSocket(
          "ws://"
          + process.env.VUE_APP_API_ENDPOINT_HOST
          + "/ws/imahima/"
          + "?token="
          + token
      );
      socket.onmessage = (e)=>{
          const data = JSON.parse(e.data);
          if(data.type == "someOneChangeStatus"){
            context.dispatch("someOneChangeStatus", data);
          }
      }
      socket.onclose = (e) => {
          console.error("Chat socket closed unexpectedly");
          // this.connectWebSocket();
      }

      context.commit('setWebsocket', socket);
    },
    setDefaultOnmessage(context){
      const socket = context.state.websocket;
      if(!socket)return;
      socket.onmessage = (e)=>{
        const data = JSON.parse(e.data);
        if(data.type == "someOneChangeStatus"){
          context.dispatch("someOneChangeStatus", data);
        }
      }
      context.commit('setWebsocket', socket);
    },

    // 通知制御
    async someOneChangeStatus(context, data:any):Promise<void>{
      // 誰かがステータス更新した。
      // ステータス情報をカウントして通知出すかを判断する

      const res = await context.dispatch("checkCanNoticeOnlineMembers",data);
      // 通知の開発用に一時的にコメントアウト
      // if (!res){
      //     return
      // }

      // 人数チェック & 人数増加チェック(規定時間ごとの確認のため)
      // houseIdを基に問い合わせ。人数チェックする
      const houseId = data.houseId;
      let himaCount = 0;
      await Axios.get("/api/users/" + houseId + "/").then((response:any) => {
        const { getStatusByName } = utils();
        const res = response.data
        for (const key in res) {
          if (getStatusByName(res[key].nowStatus) == "hima") {
            himaCount += 1;
          }
        }
      });

      if(himaCount < 2 || context.state.latestNoticeData[houseId].latestNoticeHouseMatesNumOM >= himaCount) {
          return;
      }

      context.dispatch("noticeOnlineMembers",{
        houseId:houseId,
        count:himaCount
      });
    },
    checkCanNoticeOnlineMembers(context, data:any):boolean{
      // 誰かの更新の際に全員分取り直しているので、自分含めて最新を持っているはず。
      // 人数チェック(人数を通知に使うのでこれは別口で。)
      // 増えた時だけ通知
      if(data.status != "hima"){
          return false;
      }
      // 自分のステータスチェック(予定ではヒマとヒマに送る)
      const myStatus = context.state.houseMates[context.state.userId].nowStatus;
      if(myStatus != "hima" && myStatus != "maybe"){
          return false;
      }

      // 指定のhouseIdがあるかチェック なければinitデータを作る
      const houseId = data.houseId;
      if(context.state.latestNoticeData[houseId] == undefined){
        // init
        context.commit('setlatestNoticeData', {
          houseId: houseId,
          latestNoticeTimeOM: new Date(),
          latestNoticeHouseMatesNumOM: 0
        });
      }

      // 前回の通知から規定時間以上立っていたら送る
      const latestNoticeTimeOM:Date = new Date(context.state.latestNoticeData[houseId].latestNoticeTimeOM.getTime());
      latestNoticeTimeOM.setMinutes( latestNoticeTimeOM.getMinutes() + context.state.noticeIntervalMinOM);
      if(latestNoticeTimeOM > new Date()){
          return false;
      }

      return true;
    },
    async noticeOnlineMembers(context:any, data:{houseId:string, count:number}):Promise<void>{
      // 2人以上になったよの通知
      // 通知しつつ次の通知のインターバルを設定する。

      // 通知許可チェック
      const { checkNoticePermission } = utils();
      const permission = await checkNoticePermission();
      if(!permission) return;

      // 人数と通知時間の記録(その家のものに)
      context.commit('setlatestNoticeData', {
        houseId: data.houseId,
        latestNoticeTimeOM: new Date(),
        latestNoticeHouseMatesNumOM: data.count
      });

      const img = require('@/assets/img/notification/app_icon.png');
      const text = data.count + "人ヒマな人がいます。";
      const options = {
          tag: 'noticeOnlineMembers',
          icon: img,
          body: text,
          actions: [
              {action: 'enterRoom', title: "入る"}
              ],
          data: {
              baseUrl: process.env.BASE_URL,
              url: "/?#/House",
          }
      }
      navigator.serviceWorker.ready.then((registration) => {
          registration.showNotification("ヒマですか？", options);
      });
      
      // インターバルよりも少し多く待つ
      setTimeout(() =>{context.dispatch("someOneChangeStatus",{houseId: data.houseId, status:"hima"})}, context.state.noticeIntervalMinOM * 60 * 1000 + 1000);
    },
    
  },
  modules: {
  }
})
