<template>
  <div>
    <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>信息管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户信息</el-breadcrumb-item>
    </el-breadcrumb>
    <!--卡片视图区-->
    <el-card>
      <!--搜索与添加区域-->
      <el-row :gutter="20">
        <el-col :span="9">
          <el-input placeholder="请输入内容" v-model="queryInfo.query">
            <el-button slot="append" icon="el-icon-search" @click="getUserList"></el-button>
          </el-input>
        </el-col>
        <el-col :span="2  ">
          <el-button type="primary" @click="dialogVisible = true">
            添加用户
          </el-button>
        </el-col>
      </el-row>
      <!--用户列表区-->
      <el-table :data="userlist" border style="margin-top: 20px;">
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="username" label="账号"></el-table-column>
        <el-table-column prop="dept_name" label="部门"></el-table-column>
        <el-table-column label="角色">
          <template slot-scope="scope">
            {{level[scope.row.user_type]}}
          </template>
        </el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <el-tooltip class="item" effect="dark" content="激活/禁用" placement="right" :enterable="false">
              <el-switch
                v-model="scope.row.status"
                @change="userstatechange(scope.row)"
              >
              </el-switch>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="编辑" width="180px">
          <template slot-scope="scope">
            <!--修改按钮-->
            <el-tooltip class="item" effect="dark" content="修改按钮" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="openXiugai(scope.row)"></el-button>
            </el-tooltip>
            <!--删除按钮-->
            <el-tooltip class="item" effect="dark" content="删除按钮" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="shanchu(scope.row.id)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!--分页区域-->
      <div class="block">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.page"
          :page-sizes="[10,20,50]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="restdata.count">
        </el-pagination>
      </div>
    </el-card>
    <!--添加用户的对话框-->
    <el-dialog
      title="添加用户"
      :visible.sync="dialogVisible"
      width="50%" @close="closeDialog('addform')"
    >
      <!--内容主题区域-->
      <el-form :model="addform" :rules="addformRules" ref="addform" label-width="70px" style="text-align: left;">
        <el-form-item label="账 号" prop="username" >
          <el-input v-model="addform.username"placeholder="请输入电话号码"></el-input>
        </el-form-item>
        <el-form-item label="密 码" prop="password">
          <el-input v-model="addform.password"></el-input>
        </el-form-item>
        <el-form-item label="姓 名" prop="name">
          <el-input v-model="addform.name"></el-input>
        </el-form-item>
        <el-form-item label="角 色">
          <el-select v-model="addform.user_type" placeholder="请选择">
            <el-option label="普通用户" value=1></el-option>
            <el-option label="管理员" value=2></el-option>
            <!--            <el-option v-for="item in usertype_optons" :key="item.value" :label="item.label"></el-option>-->
          </el-select>
          <el-select @click.native="getDeptOptions()" v-model="addform.department_id" placeholder="选择部门">
            <el-option v-for="item in deptlist" :value="item.id" :label="item.dept_name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="状 态">

          <el-switch v-model="addform.status" active-color="#13ce66" active-text="生效"></el-switch>
        </el-form-item>

      </el-form>
      <!--底部区域-->
      <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="adduser">确 定</el-button>
  </span>
    </el-dialog>
    <!--修改对话框-->
    <el-dialog
      title="修改用户"
      :visible.sync="xiugaiVisible"
      width="50%" @close="closeDialog('xiugaiForm')"
    >
      <!--内容主题区域-->
      <el-form :model="xiugaiForm" :rules="addformRules" ref="xiugaiForm" label-width="70px"
               style="text-align: left;">
        <el-form-item label="账 号" prop="username">
          <el-input v-model="xiugaiForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密 码" prop="password">
          <el-input v-model="xiugaiForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="姓 名" prop="name">
          <el-input v-model="xiugaiForm.name"></el-input>
        </el-form-item>
        <el-form-item label="角 色">
          <el-select v-model="xiugaiForm.user_type" placeholder="请选择">
            <el-option label="普通用户" value=1></el-option>
            <el-option label="管理员" value=2></el-option>
            <!--            <el-option v-for="item in usertype_optons" :key="item.value" :label="item.label"></el-option>-->
          </el-select>
          <el-select @click.native="getDeptOptions()" v-model="xiugaiForm.department_id" placeholder="选择部门">
            <el-option v-for="item in deptlist" :value="item.id" :label="item.dept_name"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <!--底部区域-->
      <span slot="footer" class="dialog-footer">
    <el-button @click="xiugaiVisible = false">取 消</el-button>
    <el-button type="primary" @click="xiugaiuser">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    name: 'yonghuxinxi',

    data() {

      return {
        deptlist: '',
        restdata: {},
        // 获取用户列表的参数对象
        queryInfo: {
          query: '',
          page: 1,
          size: 10,
        },
        userlist: [],
        // 控制添加用户对话框的隐藏
        dialogVisible: false,
        // 添加用户的表单数据
        addform: {
          username: '',
          password: '',
          name: '',
          user_type: '1',
          department_id: null,
          status: true,
        },
        // 添加表单的验证规则对象
        addformRules: {
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
        // 修改用户对话框的显示与隐藏
        xiugaiVisible: false,
        xiugaiForm: {},
      }
    },
    created() {
      this.getUserList()
    },

    methods: {

      async getUserList() {
          const {data: res} = await this.$http.get('/users', {
            params: this.queryInfo
          }).catch((error) => {
            this.$message.error(error)
          })
        this.restdata = res
        this.userlist = res.results
        // if (res.meta.status !== 200) {
        //   return this.$message.error('获取用户列表失败！')
        // }
        // this.userlist= res.data.users
        // this.total = res.data.total
        // console.log(res)
      },
      // 监听pagesize改变事件
      handleSizeChange(newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.queryInfo.size = newSize
        this.getUserList()
      },
      // // 监听页码改变
      handleCurrentChange(newPage) {
        // console.log(`当前页: ${newPage}`)
        this.queryInfo.page = newPage
        this.getUserList()
      },
      // 监听开关状态
      async userstatechange(userinfo) {
        // var putdata = JSON.parse(JSON.stringify(userinfo))
        // delete putdata.id
        // delete putdata.url
        // console.log(putdata)
        // console.log(userinfo)
        const {data: res} = await this.$http.put(`users/${userinfo.id}/`, userinfo).catch((err) => {
          this.$message.error(err)
        })
      },
      //获取部门下拉框中内容
      getDeptOptions() {
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
      closeDialog(formName) {
        this.$refs[formName].resetFields()
        this.getUserList()
      },
      //点击按钮添加新用户
      adduser() {
        this.$refs.addform.validate(
          async valid => {
            if (!valid) return
            //添加用户请求
            try {
              const {status: res} = await this.$http.post('/users/', this.addform)
              if (res == 201) {
                this.$message.success('添加成功！')
                this.dialogVisible = false
                this.getUserList()
              }

            } catch (err) {
              this.$message.error('添加失败！' + err.toString())
            }

          }
        )
      },

      // 打开修改用户的对话框
      openXiugai(row) {
        this.xiugaiVisible = true
        this.xiugaiForm = row
        this.xiugaiForm.user_type = this.xiugaiForm.user_type.toString()
        this.getDeptOptions()
        // this.xiugaiForm.user_type=this.xiugaiForm.user_type.toString()
        // console.log(row)
      },
      async xiugai(row) {
        const {data: ras} = await this.$http.get('/users/${row.id}/')
        this.xiugaiVisible = true

      },
      //提交修改内容
      async xiugaiuser() {
        this.$refs.xiugaiForm.validate(
          async valid => {
            if (!valid) return
            // console.log(this.xiugaiForm.id)
            // console.log(this.xiugaiForm)
            //修改用户请求
            try {
                const res = await this.$http.put(`/users/${this.xiugaiForm.id}/`, this.xiugaiForm)
              // console.log(res)
              if (res.status == 200) {
                this.$message.success('修改成功！')
                this.xiugaiVisible = false
                this.getUserList()
              }
            } catch (err) {
              this.$message.error('修改失败！' + err.toString())
            }

          }
        )
      },
      async shanchu(id) {
        // console.log(id)
        //  询问用户是否删除
        const confirmResult = await this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).catch(err => err)
        //如果用户确认删除，返回confirm
        // 如果用户取消删除，返回cancel
        // console.log(confirmResult)
        if (confirmResult !== 'confirm') {
          return this.$message.info('已取消删除')
        }
        try {
        const {status: res} = await this.$http.delete(`/users/${id}/`)
        if (res == 204) {
          this.$message.success('删除成功！')
          this.getUserList()
        }
      } catch(err) {
        this.$message.error('删除失败！' + err.toString())
      }
    }
  },

  }
</script>

<style lang="less" scoped>
  .item {
    margin: 4px;
  }
</style>
