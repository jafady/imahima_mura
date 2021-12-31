import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

//component
import Login from '@/components/pages/Login.vue'
import FirstVisitor from '@/components/pages/FirstVisitor.vue'

import House from '@/components/pages/House.vue'

import PushTest from '@/components/pages/PushTest.vue'

// store
import Store from '@/store/index'

declare module 'vue-router' {
  interface RouteMeta {
    beforeAuth?: boolean
    title?: string
  }
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { beforeAuth: true, title:'イマヒマ村 ログイン' }
  },
  {
    path: '/FirstVisitor',
    name: 'FirstVisitor',
    component: FirstVisitor,
    meta: { beforeAuth: true, title:'イマヒマ村へようこそ' }
  },
  {
    path: '/House',
    name: 'House',
    component: House,
    meta: { title:'イマヒマ村 居間' }
  },
  {
    path: '/pushtest',
    name: 'PushTest',
    component: PushTest,
    meta: { beforeAuth: true }
  },
]

const DEFAULT_TITLE = 'イマヒマ村'
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => !record.meta.beforeAuth) && !Store.state.userToken) {
    // localStorage.setItem('userId', '');
    // localStorage.setItem('token', '');
    if(localStorage.getItem('token')){
      // todo tokenの生存確認しなきゃ。。
      Store.dispatch("auth", {
          userId: localStorage.getItem('userId'),
          userToken: localStorage.getItem('token')
      });
      next();
    } else {
      next({ path: '/login', query: { redirect: to.fullPath } });
    }
  } else {
    next();
  }
});
router.afterEach((to, from) => {
  document.title = to.meta.title || DEFAULT_TITLE
})

export default router
