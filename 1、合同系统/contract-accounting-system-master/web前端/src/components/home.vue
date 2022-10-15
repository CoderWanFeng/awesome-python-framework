<template>
  <el-container class="home-tou">
    <el-header style="height: 80px">
      <div >
         <img  style="margin-left: 20px;width: 60px; height: 60px" src="../assets/logo.png" >
        <span style="font-size:20px" > 水 滴&nbsp;合 同 账&nbsp;务&nbsp;系&nbsp;统</span>
      </div>
      <!--<span v-text="a" id="a"></span>-->
      <!--<el-avatar v-text="a" icon="el-icon-user-solid" ></el-avatar>-->
      <!--<el-button type="info" @click="out">退出</el-button>-->
      <el-dropdown :hide-on-click="false">
  <span class="el-dropdown-link">
    <i class="el-icon-s-custom el-icon--left"></i><span v-text="a" id="a">   </span>
  </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="opengeren()">个人中心</el-dropdown-item>
          <el-dropdown-item @click.native="out">退出登录</el-dropdown-item>
        </el-dropdown-menu>

      </el-dropdown>
    </el-header>

    <el-container>
      <el-aside :width="iscollapse ?  '64px' :'200px'">
        <div class="zhedie" @click="zd"><i :class="iscollapse ? 'el-icon-s-fold' : 'el-icon-s-unfold'"></i></div>
        <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          background-color="#535a5c"
          text-color="#fff"
          active-text-color="#409eff"
          :unique-opened="true"
          :collapse="iscollapse"
          :collapse-transition="false"
          :router="true"
          @select="handleSelect"
          :default-active="this.$router.history.current.path"
        >
          <!--default-active="$route.path" 所在页面子菜单导航高亮-->
          <!-- 一级菜单 -->
          <el-submenu :index="item.id +''" v-for="item in menulist" :key="item.id">
            <template slot="title">
              <i :class="menuicos[item.id]"></i>
              <span>{{item.authName}}</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item :index="'/' +subItem.path" v-for="subItem in item.children" :key="subItem.id"
            >
              <template slot="title">
                <!-- 图标 -->
                <i :class="menuicos[subItem.id]"></i>
                <span>{{subItem.authName}}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <!--路由占位符-->
        <router-view v-if="isRouterAlive"></router-view>
        <!--个人中心-->
        <el-dialog
          title="个人中心"
          :visible.sync="gerenVisible"
          width="50%" @close="closeDialog('ruleForm')"
          :data="userlist"
        >
          <!--内容主题区域-->
          <el-form :model="ruleForm" :rules="ruleFormRules" ref="ruleForm" label-width="70px" style="text-align: left;">
            <el-form-item label="账 号" prop="username" >
              <el-input v-model="ruleForm.username" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="密 码" prop="password">
              <el-input v-model="ruleForm.password"></el-input>
            </el-form-item>
            <el-form-item label="姓 名" prop="name">
              <el-input v-model="ruleForm.name" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="角 色">
              <el-select v-model="ruleForm.user_type" placeholder="请选择" :disabled="true">
                <el-option label="普通用户" value=1></el-option>
                <el-option label="管理员" value=2></el-option>
                <!--            <el-option v-for="item in usertype_optons" :key="item.value" :label="item.label"></el-option>-->
              </el-select>
              <el-select  v-model="ruleForm.department_id" placeholder="选择部门"
                         :disabled="true">
                <el-option v-for="item in deptlist" :value="item.id" :label="item.dept_name"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <!--底部区域-->
          <span slot="footer" class="dialog-footer">
    <el-button @click="gerenVisible = false">取 消</el-button>
    <el-button type="primary" @click="gerenuser()">确 定</el-button>
  </span>
        </el-dialog>

      </el-main>
    </el-container>
  </el-container>

</template>

<script>

  export default {

    name: 'web2020',
    data () {
      return {
        isRouterAlive: true,
        a: window.sessionStorage.getItem('name'),
        menulist: [
          {
            'id': 1,
            'authName': '合同管理',
            'path': '/hetong',
            'children': [
              {
                'id': 101,
                'authName': '项目合同',
                'path': 'xiangmuhetong',
                'children': []
              },
              // {
              //   'id': 102,
              //   'authName': '综合查询',
              //   'path': 'caigouhetong',
              //   'children': []
              // }
            ]
          },
          {
            'id': 2,
            'authName': '报销管理',
            'path': '/hetong',
            'children': [
              {
                'id': 201,
                'authName': '新增报销',
                'path': 'reimbursement',
                'children': []
              },
              {
                'id': 202,
                'authName': '报销查询',
                'path': 'baoxiaochaxun',
                'children': []
              }
            ]
          },
          {
            'id': 3,
            'authName': '信息管理',
            'path': '/hetong',
            'children': [
              {
                'id': 301,
                'authName': '用户信息',
                'path': 'yonghuxinxi',
                'children': []
              },
              {
                'id': 302,
                'authName': '部门信息',
                'path': 'department',
                'children': []
              },
              {
                'id': 303,
                'authName': '单位信息',
                'path': 'entityInfo',
                'children': []
              },
              {
                'id': 304,
                'authName': '项目信息',
                'path': 'Project',
                'children': []
              }
            ]
          },
          {
            'id': 4,
            'authName': '财务管理',
            'path': '2',
            'children': [
              {
                'id': 401,
                'authName': '报销审批',
                'path': 'baoxiaoshenpi',
                'children': []
              },
              {
                'id': 402,
                'authName': '综合查询',
                'path': 'zonghechaxun',
                'children': []
              },
            ]
          },
        ],
        menuicos: {
          '1': 'el-icon-notebook-2',
          '101': 'el-icon-notebook-2',
          '102': 'el-icon-notebook-2',
          '103': 'el-icon-notebook-2',
          '2': 'el-icon-notebook-1',
          '201': 'el-icon-notebook-1',
          '202': 'el-icon-notebook-1',
          '3': 'el-icon-s-custom',
          '301': 'el-icon-s-custom',
          '302': 'el-icon-s-custom',
          '303': 'el-icon-s-custom',
          '304': 'el-icon-s-custom',
          '4': 'el-icon-notebook-1',
          '401': 'el-icon-notebook-1',
          '402': 'el-icon-notebook-1',
        },
        deptlist: '',
        userlist: [],
        restdata: {},
        ruleForm: {
          username: '',
          password: '',
          name: '',
          user_type: '1',
          department_id: null,
          status: true,
        },
        ruleFormRules: {
          name: [
            {
              required: true,
              message: '请输入用户名',
              trigger: 'blur'
            },
            {
              min: 1,
              max: 15,
              message: '用户名长度为1-15个字',
              trigger: 'blur'
            }
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
              message: '密码长度为6-15个字',
              trigger: 'blur'
            }
          ],
          username: [
            {
              required: true,
              message: '请输入账号',
              trigger: 'blur'
            },
            {
              min: 3,
              max: 15,
              message: '账号长度为3-15个字',
              trigger: 'blur'
            }
          ],
        },
        level: {
          1: '普通用户',
          2: '管理员'
        },
        created () {
          this.getUserList()
        },
        iscollapse: false,
        gerenVisible: false,
      }
    },
    methods: {
      // created() {
      //   this.getUserList()
      // },
      async getUserList () {
        const { data: res } = await this.$http.get('/users', {
          params: this.queryInfo
        })
        this.restdata = res
        this.userlist = res.results
      },
      // 退出登录
      out () {
        window.sessionStorage.clear()
        this.$router.push('/login')
      },
      // 列表折叠
      zd () {
        this.iscollapse = !this.iscollapse
      },
      //获取部门下拉框中内容
      getDeptOptions () {
        let _this = this

        this.$http.get('dept/')
          .then(res => {
            //请求返回的数据
            //赋值
            _this.deptlist = res.data
          }).catch((error) => {
          console.log(error)
        })
      },
      //关闭Dialog清空数据
      closeDialog (formName) {
        this.$refs[formName].resetFields()
      },
      // 个人中心
      async opengeren () {
        this.gerenVisible = true
        const { data: res } = await this.$http.post('/getUserInfo', { token: window.sessionStorage.getItem('token') })
        console.log(res)
        this.ruleForm = res.data
        this.ruleForm.user_type = this.ruleForm.user_type.toString()
        this.getDeptOptions()
        // this.xiugaiForm.user_type=this.xiugaiForm.user_type.toString()
        // console.log(row)
      },
      async geren (row) {
        const { data: ras } = await this.$http.get('/users/${row.id}/')
        this.gerenVisible = true

      },
      //提交修改内容
      async gerenuser () {
        this.$refs.ruleForm.validate(
          async valid => {
            if (!valid) return
            // console.log(this.xiugaiForm.id)
            // console.log(this.xiugaiForm)
            //修改用户请求
            try {
              // const res = await this.$http.put(`/users/${this.ruleForm.id}/`, this.ruleForm)
              const res = await this.$http.patch(`/users/${this.ruleForm.id}/`, {password:this.ruleForm.password})
              // console.log(res)
              if (res.status == 200) {
                this.$message.success('修改成功！')
                this.gerenVisible = false
                // this.getUserList()
              }
            } catch (err) {
              this.$message.error('修改失败！' + err.toString())
            }

          }
        )
      },
      handleSelect (index) {

        if (index === this.$route.path) {
          // console.log(index+"abc")
          // console.log(this.$route.path+"vvvv")
          this.reload()
          // let num = Math.floor(Math.random() * 1000 + 1)
          // this.$router.replace(`${index}?${num}`)
        }
      },
      reload () {
        this.isRouterAlive = false
        this.$nextTick(function () {
          this.isRouterAlive = true
        })
      }
    }
  }

</script>

<style lang="less" scoped>
  .home-tou {
    height: 100%;
  }

  .el-header, .el-footer {
    background-color: rgba(48, 54, 67, 0.93);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-left: 0;
    color: white;
    font-size: 20px;


    > div {
      display: flex;
      align-items: center;
    }
  }

  //退出
  .el-dropdown-link {
    cursor: pointer;
    color: #ffffff;
  }

  .el-icon-arrow-down {
    font-size: 16px;
  }

  //
  .el-aside {
    background-color: #535a5c;
    color: #333;

    .el-menu {
      border-right: none;

      .el-submenu {
        text-align: left;
      }
    }
  }

  .el-main {
    background-color: #E9EEF3;
  }

  .zhedie {
    background-color: #f6f6f6;
    color: #303643;
    font-size: 16px;
    line-height: 24px;
    text-align: center;
    letter-spacing: 0.2em;
    cursor: pointer;
  }


</style>
