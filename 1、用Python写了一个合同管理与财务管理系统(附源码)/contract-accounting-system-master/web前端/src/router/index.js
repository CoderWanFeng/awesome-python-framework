import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'
import web2020 from '../components/web2020'
import home from '../components/home'
import welcome from  '../components/welcome'
import yonghuxinxi from  '../components/yonghuxinxi'
import  department from  '../components/department'
import  entityInfo from  '../components/entityInfo'
import  Project from  '../components/Project'
import  reimbursement from  '../components/reimbursement'
import  baoxiaochaxun from  '../components/baoxiaochaxun'
import  baoxiaoshenpi from  '../components/baoxiaoshenpi'
import  zonghechaxun from  '../components/zonghechaxun'
import  xiangmuhetong from  '../components/xiangmuhetong'
import  caigouhetong from  '../components/caigouhetong'
import  register from  '../components/register'

// import  contian from '../components/contian'

Vue.use(VueRouter)

const routes = [
  {
    path: '/', redirect: '/login'
  },
  {
    path: '/register',
    name:'register',
    component:register
  },
  // {
  //   path: 'yonghuxinxi',
  //   name: 'yonghuxinxi',
  //   meta: {
  //     roles: ['admin']
  //   },
  //   component: () => import('../components/yonghuxinxi.vue')
  // },
  {
    path: '/login',
    name: 'web2020',
    component: web2020
  },
  {
    path: '/home',
    name: 'home',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    component: home,
    // 页面路由
    redirect :'/welcome',children:[
      {path:'/welcome',component:welcome},
      {path:'/department',component:department},
      {path:'/yonghuxinxi',component:yonghuxinxi},
      {path:'/entityInfo',component:entityInfo},
      {path:'/Project',component:Project},
      {path:'/reimbursement',component:reimbursement},
      {path:'/baoxiaochaxun',component:baoxiaochaxun},
      {path:'/baoxiaoshenpi',component:baoxiaoshenpi},
      {path:'/zonghechaxun',component:zonghechaxun},
      {path:'/xiangmuhetong',component:xiangmuhetong},
      {path:'/caigouhetong',component:caigouhetong},
    ]
  },
  // {
  //   path: '/contian',
  //   name: 'contian',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  //   component: contian,
  //   // 页面路由
  //   redirect :'/welcome',children:[
  //     {path:'/yonghuxinxi',component:yonghuxinxi}
  //   ]
  // }
]


const router = new VueRouter({

  mode: 'history',
  base: process.env.BASE_URL,
  routes,
})
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

// 路由守卫
  router.beforeEach((to, from, next) => {
  if (to.path === '/login'){ return next()}
  if(to.path === '/register') { return next()}
  const tokenStr=window.sessionStorage.getItem('token')

  if (!tokenStr) return next('/login')
  next()
})
export default router
