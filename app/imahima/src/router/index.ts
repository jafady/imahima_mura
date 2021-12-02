import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

//component
import Login from '@/components/pages/Login.vue'
import Welcome from '@/components/pages/Welcome.vue'
import PushTest from '@/components/pages/PushTest.vue'

// store
import Store from '@/store/index'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { beforeAuth: true }
  },
  {
    path: '/',
    name: 'Welcome',
    component: Welcome
  },
  {
    path: '/pushtest',
    name: 'PushTest',
    component: PushTest,
    meta: { beforeAuth: true }
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => !record.meta.beforeAuth) && !Store.state.userToken) {
    next({ path: '/login', query: { redirect: to.fullPath } });
  } else {
    next();
  }
});

export default router
