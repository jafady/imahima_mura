import { createStore } from 'vuex'
import Axios, {AxiosRequestConfig} from 'axios'
Axios.defaults.baseURL = process.env.VUE_APP_API_ENDPOINT_PROTOCOL +"://"+process.env.VUE_APP_API_ENDPOINT_HOST+"/";
Axios.interceptors.request.use((config: AxiosRequestConfig) => {
    if(config.headers && localStorage.getItem('token')){
        config.headers.Authorization = "Token " + localStorage.getItem('token')
    }
    return config
});

export default createStore({
  state: {
    userId: "",
    userToken: "",
    userName: "",
    userIcon: null,
  },
  mutations: {
    loginUser(state, user) {
      state.userId = user.userId;
      state.userToken = user.userToken;
    },
    userInfo(state, userInfo) {
      state.userName = userInfo.userName;
      state.userIcon = userInfo.userIcon;
    }
  },
  actions: {
    auth(context, user) {
      context.commit('loginUser', user);
    },
    async getUserInfo(context) {
      const userId = context.state.userId;
      await Axios.get("/api/user_info/" + userId + "/").then((response:any) => {
          const userInfo = {
            userName: response.data.username,
            userIcon: response.data.userSetting[0]
          }
          context.commit('userInfo', userInfo);
      })
    }
    
  },
  modules: {
  }
})
