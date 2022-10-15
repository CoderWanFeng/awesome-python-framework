//module.exports = {
  //lintOnSave: false
//}
module.exports = {
  lintOnSave:false,
  devServer: {
    //跨域请求代理
    proxy: {
      '/api': {
        //target: 'http://192.168.231.128:9000/api', //对应自己的接口
        target: 'http://127.0.0.1:9000/api', //对应自己的接口
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          '^/api': '/'
        }
      }
    }
  }
}
