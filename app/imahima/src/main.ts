import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"

import Axios from 'axios';

const app = createApp(App).use(store).use(router)
app.config.globalProperties.$http = Axios;
app.mount('#app')
