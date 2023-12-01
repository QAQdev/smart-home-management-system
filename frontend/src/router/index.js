import { createRouter, createWebHashHistory } from 'vue-router'
import sign from '@/pages/sign'
import home from '@/pages/home'
import about from '@/pages/about'
import log from "@/pages/log.vue";

const routes = [
  {
    path: '/sign',
    name: 'sign',
    component: sign
  },
  {
    path: '/',
    name: 'home',
    component: home
  },
  {
    path: '/about',
    name: 'about',
    component: about
  },
  {
    path: '/log',
    name: 'log',
    component: log
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
