import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import VueDragResize from 'vue-drag-resize'

createApp(App)
    .use(router)
    .use(VueDragResize)
    .use(ElementPlus)
    .mount('#app')