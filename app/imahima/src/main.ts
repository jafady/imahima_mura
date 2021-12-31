import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import "./assets/scss/common.scss";

import Axios, {AxiosRequestConfig} from 'axios'
import Push from 'push.js'

const app = createApp(App).use(store).use(router);
Axios.defaults.baseURL = process.env.VUE_APP_API_ENDPOINT_PROTOCOL +"://"+process.env.VUE_APP_API_ENDPOINT_HOST+"/";
Axios.interceptors.request.use((config: AxiosRequestConfig) => {
    if(config.headers && localStorage.getItem('token')){
        config.headers.Authorization = "Token " + localStorage.getItem('token')
    }
    return config
});

app.config.globalProperties.$http = Axios;
app.config.globalProperties.$push = Push;
app.mount('#app');
