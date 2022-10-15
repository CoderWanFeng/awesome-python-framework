<template>
  <div id="login_c">
    <div class="login_box">
      <div class="avatar_box">
        <img src="../assets/logo.png" alt="">
      </div>

      <div style="margin-top: 80px;">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
          <el-row>
            <p class="a">水 滴&nbsp;合 同 账&nbsp;务&nbsp;系&nbsp;统</p>
          </el-row>
          <el-row type="flex" justify="center">
            <el-form-item prop="username" style="width: 70%">
              <el-input prefix-icon="el-icon-user"  v-model="ruleForm.username" placeholder="用户名"
                        v-on:keyup.enter.native="submit"></el-input>
            </el-form-item>
          </el-row>

          <el-row type="flex" justify="center">
            <el-form-item prop="password" style="width: 70%">
              <el-input prefix-icon="el-icon-lock" placeholder="请输入密码" v-model="ruleForm.password" show-password
                        v-on:keyup.enter.native="submit"></el-input>
            </el-form-item>
          </el-row>


          <el-row class="btns">
            <el-button type="primary" @click="submit">点击登录</el-button>
            <el-button type="info" @click="reset" style="margin-left: 20%">点击重置</el-button>
          </el-row>
        </el-form>
      </div>


    </div>
  </div>
</template>

<script>

  export default {
    name: 'web2020',
    data () {
      return {
        ruleForm: {
          username: '',
          password: ''

        },

        rules: {
          username: [
            {
              required: true,
              message: '请输入用户名',
              trigger: 'blur'
            },
          ],
          password: [
            {
              required: true,
              message: '请输入密码',
              trigger: 'blur'
            },
            {
              min: 6,
              max: 15,
              message: '长度在 6 到 15 个字符',
              trigger: 'blur'
            }
          ],
        },
      }
    },
    created(){
      this.chickRegister()
    },
    methods: {
      reset () {
        this.$refs.ruleForm.resetFields()
      },

      submit () {

        this.$refs.ruleForm.validate(
          async valid => {
            if (!valid) return this.$message.error('请输入用户名密码')
            const loading = this.$loading({
              lock: true,
              text: '正在登录',
              spinner: 'el-icon-loading',
              background: 'rgba(0, 0, 0, 0.7)'
            })
            try {
              const { data: res } = await this.$http.post('/login', this.ruleForm)
              // console.log(res);
              if (res) loading.close()
              if (res.meta.status !== 200) {
                return this.$message({
                  showClose: true,
                  message: (res.meta.msg),
                  type: 'error'
                })
              }
              this.$message.success('登录成功')
              window.sessionStorage.setItem('token', res.data.token)
              window.sessionStorage.setItem('name', res.data.name)
              window.sessionStorage.setItem('id', res.data.id)
              this.$router.push('/home')
            } catch (err) {
              loading.close()
              this.$message.error('连接服务器失败')
            }
          })
      },
      async chickRegister(){
         const {data:res} = await this.$http.get('/zhuche')

        if(res.data['license'] !==""&& res.message=="registered"){
          return
        }else {
          this.$router.push('/register')
        }
      },
    }
  }
</script>

<style lang="less" scoped>

  #login_c {
    background-color: #00445B;
    background-size: 100% 100%;
    height: 100%;
  }

  .login_box {
    width: 500px;
    height: 400px;
    border-radius: 4px;
    position: absolute;
    left: 50%;
    top: 50%;
    text-align: center;
    transform: translate(-50%, -50%);
    background-color: #ada89b;

    .avatar_box {
      height: 130px;
      width: 130px;
      border: 1px solid #eee;
      border-radius: 50%;
      padding: 10px;
      box-shadow: 0 0 10px #ddd;
      position: absolute;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: #fff;

      img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: #eee;
      }
    }
  }

  .a {
    font-size: 28px;
    color: white;
  }

  .btns {
    display: flex;
    margin-left: 26%;
  }
</style>
