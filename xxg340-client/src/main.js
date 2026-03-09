import { 
  createApp,
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onActivated,
  onDeactivated,
  onErrorCaptured,
  onRenderTracked,
  onRenderTriggered,
  watch,
  watchEffect,
  reactive,
  ref,
  computed,
  nextTick
} from 'vue';

import App from './App.vue'
import ElementPlus from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'

import * as Icons from '@element-plus/icons-vue'
import router from '@/routers/index'
import pinia from '@/stores/index'
import * as echarts from "echarts";
window.echarts = echarts
import  "@/assets/js/echarts/china.js"

// element css
import 'element-plus/dist/index.css'
// reset style sheet
import '@/styles/reset.scss'
// CSS common style sheet
import '@/styles/common.scss'
// element dark(内置暗黑模式)
import 'element-plus/theme-chalk/dark/css-vars.css'
// custom element css
import '@/styles/element.scss'
// public css
import '@/styles/public.scss'
import '@/style.css'

const app = createApp(App)
// 注册element Icons组件
Object.keys(Icons).forEach(key => {
  app.component(key, Icons[key])
})

// 自定义全局组件
import UploadImg from "@/components/UploadImg/index.vue";
import UploadManyImg from "@/components/UploadManyImg/index.vue";
import UploadFile from "@/components/UploadFile/index.vue";
import WangEditor from "@/components/WangEditor/index.vue";
app.component('UploadImg', UploadImg)
app.component('UploadManyImg', UploadManyImg)
app.component('UploadFile', UploadFile)
app.component('WangEditor', WangEditor)


// 将所有生命周期钩子函数和响应式 API 挂载到 window 上
window.onBeforeMount = onBeforeMount;
window.onMounted = onMounted;
window.onBeforeUpdate = onBeforeUpdate;
window.onUpdated = onUpdated;
window.onBeforeUnmount = onBeforeUnmount;
window.onUnmounted = onUnmounted;
window.onActivated = onActivated;
window.onDeactivated = onDeactivated;
window.onErrorCaptured = onErrorCaptured;
window.onRenderTracked = onRenderTracked;
window.onRenderTriggered = onRenderTriggered;
window.ElMessage = ElMessage
window.ElMessageBox = ElMessageBox

// 响应式 API
window.watch = watch;
window.watchEffect = watchEffect;
window.reactive = reactive;
window.ref = ref;
window.computed = computed;
window.nextTick = nextTick;

app.use(router).use(pinia).use(ElementPlus).mount('#app')

export default app;