import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/element.js'
import './assets/css/global.css'
import axios from 'axios'
import qs from 'qs'
Vue.prototype.$qs = qs;
import Print from 'vue-print-nb'
Vue.use(Print)

//配置请求
axios.defaults.baseURL = '/api'
axios.interceptors.request.use(config => {
  config.headers.Authorization = window.sessionStorage.getItem('token')
  return config
})



axios.interceptors.response.use(response => {
  return response
}, error => {
  if (error.response) {
    switch (error.response.status) {

      case 403:
        if (error.response.data.detail === '用户认证失败！') {
          localStorage.removeItem('token')
          router.replace({ path: '/login' })
          return Promise.reject('用户验证失败，账号可能异地登录！');
        }
        if(error.response.data.detail === 'You do not have permission to perform this action.'){
          return Promise.reject('你无权进行此操作！')
        }
      case 500:
        return Promise.reject('服务器检测出操作错误，联系管理员！');
      case 550:
        return Promise.reject('存在关联数据，不能删除');
    }

  }
})
Vue.prototype.$http = axios
Vue.config.productionTip = false
// const service =axios.create(
//   {
//     baseURL:process.env.BASE_URL,
//     timeout:5000
//   })
//   service.interceptors.request.use(
//     config=>{
//       app.$vux.loading.show({
//         text:'数据加载中.....'
//       });
//       config.method==='get'
//       ? config.data = qs.stringfy({...config.data})
//         :config.params = {...config.params}
//         config.headers.Authorization=window.sessionStorage.getItem('token')
//       return config
//     },error => {
//       app.$vux.toast.show({
//         type:'warn',
//         text:error
//       })
//     }
//   )
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

// const role = 'user'
// // 在进入一个页面前会触发 router.beforeEach 事件
// router.beforeEach((to, from, next) => {
//   if (to.meta.roles.includes(role)) {
//     next()
//   } else {
//     next({path: '/404'})
//   }
// })
