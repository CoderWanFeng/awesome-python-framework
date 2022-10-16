<template>

  <div class="login_c">

    <div class="div1">
      <el-row style="margin-bottom: 20px">
         <span style="font-size: 20px;margin-right: 20px">合同系统注册页</span>
        <el-tag  :type="registered?'success':'danger'">{{registered?'已注册':'未注册'}}</el-tag>
      </el-row>


      <el-card style="height: 100%">
        <el-form :model="registerForm" label-width="80px" :rules="rule" ref="registerForm">
          <el-row style="margin-top: 5px">
            <el-form-item label="HOSTID:" prop="hostid">
              <el-input v-model="registerForm.hostid" readonly></el-input>
            </el-form-item>
          </el-row>
          <el-row style="margin-top: 5px">
            <el-form-item label="LICENSE:" prop="license">
              <el-input v-model="registerForm.license" placeholder="输入您的license"></el-input>
            </el-form-item>
          </el-row>
          <el-row style="margin-top: 5px">
            <el-button type="primary" @click="submit">点击注册</el-button>
          </el-row >
           <el-row type="flex" style="margin-top: 40px;font-size: small">
          <el-col>
            <i class="el-icon-info">请将您的HOSTID发送至供应商，获取LICENSE进行系统软件注册。</i>
          </el-col>

        </el-row>
        </el-form>


      </el-card>
    </div>

  </div>
</template>

<script>
  export default {
    name: 'register',
    data () {
      return {
        registerForm: {
          hostid: '',
          license: ''
        },
        registered:false,
       rule:{
          license:[{required:true,message:'请输入LICENSE',trigger: 'blur'}],
       }

      }

    },
    created(){
      this.getinfo();
    },
    methods: {
      submit(){

        this.$refs.registerForm.validate(
          async valid =>{
            if (!valid) return this.$message.error('请输入LICENSE')
            try{
              const {data:res} = await this.$http.post('/zhuche',this.registerForm)
               switch (res.code) {
                case 200:
                  if(res.message =="ok"){
                     this.$router.push('/login')
                    return this.$message.success("注册成功！")
                  }
                  break
                case 400:
                  return this.$message.error(res.message)
              }
            }catch (e) {
               return this.$message.error(e.toString())
            }
          }
        )
      },
      async getinfo(){
        const {data:res} = await this.$http.get('/zhuche')
        this.registerForm.hostid = res.data['hostid']
        if(res.data['license'] !==""&& res.message=="registered"){
          this.registerForm.license = res.data['license']
          this.registered = true
        }
      },
    }
  }
</script>

<style lang="less" scoped>
  .login_c {
    background-color: #ada89b;
    background-size: 100% 100%;
    height: 100%;
  }

  .div1 {
    width: 600px;
    height: 400px;
    /*border-radius: 5px;*/
    position: absolute;
    left: 50%;
    top: 50%;
    text-align: center;
    transform: translate(-50%, -50%);
    /*border:1px solid #535a5c;*/
    /*background-color: #3138ad;*/
    /*outline: 2px solid #303643;*/
    /*padding: 10px;*/
  }
</style>
