import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import "./assets/scss/common.scss";

import Axios, {AxiosRequestConfig} from 'axios'
import Push from 'push.js'
import VueTimepicker from 'vue3-timepicker'
import 'vue3-timepicker/dist/VueTimepicker.css'
import Datepicker from 'vue3-datepicker';
import 'vue3-datepicker/dist/vue3-datepicker.css'

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
app.component('VueTimepicker', VueTimepicker);
app.component('Datepicker', Datepicker);
app.mount('#app');
