import { createStore } from 'vuex'
import Axios, {AxiosRequestConfig} from 'axios'
Axios.defaults.baseURL = process.env.VUE_APP_API_ENDPOINT_PROTOCOL +"://"+process.env.VUE_APP_API_ENDPOINT_HOST+"/";
Axios.interceptors.request.use((config: AxiosRequestConfig) => {
    if(config.headers && localStorage.getItem('token')){
        config.headers.Authorization = "Token " + localStorage.getItem('token')
    }
    return config
});
import CONST from '@/mixins/const'
import utils from '@/mixins/utils'
import {houseMates} from '@/mixins/interface'


export interface State {
  userId: string,
  userToken: string,
  userName: string,
  userIcon: string,
  userStatus: string,
  houseId: string,
  houseMates: houseMates,
  websocket: WebSocket | null,
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
  },
  mutations: {
    clear(state) {
      state.userId = "";
      state.userToken = "";
      state.userName = "";
      state.userIcon = require("../assets/img/default_icon.png");
      state.userStatus = "hima";
      state.houseId = "";
      state.houseMates = {};
    },
    disconnectWebsocket(state){
      state.websocket = null;
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
    
  },
  actions: {
    clear(context) {
      context.commit('clear');
      context.dispatch('disconnectWebsocket');
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

        const todayEndTime = res.todayEndTime == "00:00:00"?"24:00:00":res.todayEndTime;

        // ユーザ一覧中の情報も更新する
        const data = {
          id: res.id,
          name: res.username,
          icon: userIcon,
          noticableStartTime: res.todayStartTime,
          noticableEndTime: todayEndTime,
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
      localStorage.setItem("houseId", houseId);
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
          const todayEndTime = res[key].todayEndTime == "00:00:00"?"24:00:00":res[key].todayEndTime;
          data[res[key].id] = {
            id: res[key].id,
            name: res[key].username,
            icon: userIcon,
            noticableStartTime: res[key].todayStartTime,
            noticableEndTime: todayEndTime,
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
      navigator.serviceWorker.ready.then( registration => {
        registration.active?.postMessage({
          type: "connectWebsocket",
          token: localStorage.getItem("token"),
          userId: context.state.userId
        });
      });

      if(context.state.websocket != null) {
        return;
      }
      const token = localStorage.getItem("token");
      const socket = new WebSocket(
          process.env.VUE_APP_WEBSOCKET_ENDPOINT_PROTOCOL
          +"://"
          + process.env.VUE_APP_API_ENDPOINT_HOST
          + "/ws/imahima/"
          + "?token="
          + token
      );
      socket.onmessage = (e)=>{
          const data = JSON.parse(e.data);
      }
      socket.onclose = (e) => {
          console.error("Chat socket closed unexpectedly");
          context.dispatch("connectWebSocket");
      }

      context.commit('setWebsocket', socket);
    },
    disconnectWebsocket(context){
      navigator.serviceWorker.ready.then( registration => {
        registration.active?.postMessage({
          type: "disconnectWebsocket",
        });
      });
      if(context.state.websocket == null) {
        return;
      }
      context.state.websocket.close();
      context.commit('disconnectWebsocket');

    },
  },
  modules: {
  }
})
