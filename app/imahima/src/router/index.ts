import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

//component
// import Login from '@/components/pages/Login.vue'
// import FirstVisitor from '@/components/pages/FirstVisitor.vue'

import House from '@/components/pages/House.vue'
// import Mypage from '@/components/pages/Mypage.vue'

// store
import Store from '@/store/index'

import Axios, {AxiosRequestConfig} from 'axios'
Axios.defaults.baseURL = process.env.VUE_APP_API_ENDPOINT_PROTOCOL +"://"+process.env.VUE_APP_API_ENDPOINT_HOST+"/";
Axios.interceptors.request.use((config: AxiosRequestConfig) => {
    if(config.headers && localStorage.getItem('token')){
        config.headers.Authorization = "Token " + localStorage.getItem('token')
    }
    return config
});

declare module 'vue-router' {
  interface RouteMeta {
    beforeAuth?: boolean
    title?: string
  }
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: '',
    component: House,
    meta: { title:'イマヒマ村 ホーム' }
  },
  {
    path: '/login',
    name: 'Login',
    // component: Login,
    component: () => import('@/components/pages/Login.vue'),
    meta: { beforeAuth: true, title:'イマヒマ村 ログイン' }
  },
  {
    path: '/FirstVisitor',
    name: 'FirstVisitor',
    // component: FirstVisitor,
    component: () => import('@/components/pages/FirstVisitor.vue'),
    meta: { beforeAuth: true, title:'イマヒマ村へようこそ' }
  },
  {
    path: '/House',
    name: 'House',
    component: House,
    meta: { title:'イマヒマ村 ホーム' }
  },
  {
    path: '/MyPage',
    name: 'MyPage',
    // component: Mypage,
    component: () => import('@/components/pages/Mypage.vue'),
    meta: { title:'イマヒマ村 マイページ' }
  },
]

const DEFAULT_TITLE = 'イマヒマ村'
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {

  if (to.matched.some(record => !record.meta.beforeAuth)) {
    if(localStorage.getItem('token')){
      // tokenの生存確認用に適当なところにリクエストを送っている
      Axios.get("/api/statuses/").then((response:any) => {
        Store.dispatch("auth", {
          userId: localStorage.getItem('userId'),
          userToken: localStorage.getItem('token')
        });
        // websocket疎通確認&接続
        Store.dispatch("connectWebsocket",false);
        next();
      }).catch(()=>{
        Store.dispatch("clear");
        localStorage.setItem("token", "");
        next({ path: '/login', query: { redirect: to.fullPath, inviteToken: to.query.inviteToken } });
      })
    } else {
      next({ path: '/login', query: { redirect: to.fullPath, inviteToken: to.query.inviteToken } });
    }
  } else {
    // websocket疎通確認&接続
    if(localStorage.getItem("token")){
      Store.dispatch("connectWebsocket",false);
    }
    next();
  }
});
router.afterEach((to) => {
  document.title = to.meta.title || DEFAULT_TITLE
})

export default router
