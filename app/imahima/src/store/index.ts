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

export default createStore({
  state: {
    userId: "",
    userToken: "",
    userName: "",
    userIcon: null,
    userStatus: "hima",
  },
  mutations: {
    clear(state) {
      state.userId = "";
      state.userToken = "";
      state.userName = "";
      state.userIcon = null;
      state.userStatus = "hima";
    },
    loginUser(state, user) {
      state.userId = user.userId;
      state.userToken = user.userToken;
    },
    userInfo(state, userInfo) {
      state.userName = userInfo.userName;
      state.userIcon = userInfo.userIcon;
      state.userStatus = userInfo.userStatus;
    },
    setStatus(state, userStatus){
      state.userStatus = userStatus;
    }
    
  },
  actions: {
    clear(context) {
      context.commit('clear');
    },
    auth(context, user) {
      context.commit('loginUser', user);
    },
    async getUserInfo(context) {
      const userId = context.state.userId;
      await Axios.get("/api/user_base_info/" + userId + "/").then((response:any) => {
        const { getStatusByName } = utils();
        const userIcon = response.data[0].userSetting__icon? CONST.BASE64.header + response.data[0].userSetting__icon: null;
        const userInfo = {
          userName: response.data[0].username,
          userIcon: userIcon,
          userStatus: getStatusByName(response.data[0].userSetting__statusId__statusName)
        }
        context.commit('userInfo', userInfo);
      })
    },
    setStatus(context, userStatus) {
      context.commit('setStatus', userStatus);
    },
    
  },
  modules: {
  }
})
