<template>
  <div>
    <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>信息管理</el-breadcrumb-item>
      <el-breadcrumb-item>项目信息</el-breadcrumb-item>
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
            添加项目
          </el-button>
        </el-col>
      </el-row>
      <!--项目列表区-->
      <el-table :data="userlist" border style="margin-top: 20px;">
        <el-table-column prop="project_name" label="项目名称"></el-table-column>
        <el-table-column prop="customer_name" label="客户对象"></el-table-column>
        <el-table-column prop="owner_name" label="主体公司"></el-table-column>
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
          :page-sizes="[20,50]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="restdata.count">
        </el-pagination>
      </div>
    </el-card>
    <!--添加用户的对话框-->
    <el-dialog
      title="添加项目"
      :visible.sync="dialogVisible"
      width="50%" @close="closeDialog('addform')"
    >
      <!--内容主题区域-->
      <el-form :model="addform" :rules="addformRules" ref="addform" label-width="100px" style="text-align: left;">
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="addform.project_name"></el-input>
        </el-form-item>
        <el-form-item label="客户对象" prop="customer_id">
          <el-select @click.native="getEntitys('customer')" v-model="addform.customer_id" placeholder="选择客户">
            <el-option v-for="item in entityList.results" :value="item.id" :label="item.entity_name"></el-option>
            <el-pagination
              small
              layout="prev, pager, next"
              @current-change="entityCurrentChange($event,'customer')"
              :page-size="entityqueryInfo.size"
              :current-page="entityqueryInfo.page"
              :total="entityList.count">
            </el-pagination>
          </el-select>
          <!--            <el-option v-for="item in usertype_optons" :key="item.value" :label="item.label"></el-option>-->
        </el-form-item>
        <el-form-item label="主体公司" prop="owner_id">
          <el-select @click.native="getEntitys('owner')" v-model="addform.owner_id" placeholder="选择主体公司">
            <el-option v-for="item in ownerentityList.results" :value="item.id" :label="item.entity_name"></el-option>
            <el-pagination
              small
              layout="prev, pager, next"
              @current-change="entityCurrentChange($event,'owner')"
              :page-size="entityqueryInfo.size"
              :current-page="entityqueryInfo.page"
              :total="ownerentityList.count">
            </el-pagination>
          </el-select>
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
      title="修改项目"
      :visible.sync="xiugaiVisible"
      width="50%" @close="closeDialog('xiugaiForm')"
    >
      <!--内容主题区域-->
      <el-form :model="xiugaiForm" :rules="addformRules" ref="xiugaiForm" label-width="100px"
               style="text-align: left;">
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="xiugaiForm.project_name"></el-input>
        </el-form-item>
        <el-form-item label="客户对象">
          <el-select @click.native="getEntitys('customer')" v-model="xiugaiForm.customer_id" placeholder="选择客户">
            <el-option v-for="item in entityList.results" :value="item.id" :label="item.entity_name"></el-option>
            <el-pagination
              small
              layout="prev, pager, next"
              @current-change="entityCurrentChange($event,'customer')"
              :page-size="entityqueryInfo.size"
              :current-page="entityqueryInfo.page"
              :total="entityList.count">
            </el-pagination>
          </el-select>
        </el-form-item>
        <el-form-item label="主体公司">
          <el-select @click.native="getEntitys('owner')" v-model="xiugaiForm.owner_id" placeholder="选择主体公司">
            <el-option v-for="item in ownerentityList.results" :value="item.id" :label="item.entity_name"></el-option>
            <el-pagination
              small
              layout="prev, pager, next"
              @current-change="entityCurrentChange($event,'owner')"
              :page-size="entityqueryInfo.size"
              :current-page="entityqueryInfo.page"
              :total="ownerentityList.count">
            </el-pagination>
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
    name: 'Project',
    data () {
      return {
        entityList: {},
        ownerentityList: {},
        restdata: {},
        // 获取公司列表的参数对象
        entityqueryInfo: {
          query: '',
          page: 1,
          size: 10,
        },
        // 获取项目列表的参数对象
        queryInfo: {
          query: '',
          page: 1,
          size: 20,
        },
        userlist: [],
        // 控制添加用户对话框的隐藏
        dialogVisible: false,
        // 添加用户的表单数据
        addform: {
          owner_name: '',
          customer_name: '',
          project_name: '',
          owner_id: null,
          customer_id: null,
        },
        // 添加表单的验证规则对象
        addformRules: {
          project_name: [
            {
              required: true,
              message: '请输入项目名',
              trigger: 'blur'
            },
          ],
          owner_id:[
            {
              required: true,
              message: '请选择客户对象',
              trigger: 'blur'
            }
            ],
          customer_id:[
            {
              required: true,
              message: '请选择主体公司',
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
    created () {
      this.getUserList()
    },
    methods: {
      async getUserList () {
        const { data: res } = await this.$http.get('/projects', {
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
      handleSizeChange (newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.queryInfo.size = newSize
        this.getUserList()
      },
      // // 监听页码改变
      handleCurrentChange (newPage) {
        // console.log(`当前页: ${newPage}`)
        this.queryInfo.page = newPage
        this.getUserList()
      },
          // // 监听页码改变
      entityCurrentChange (newPage,type) {
        console.log(`当前页: ${newPage}`+'type为'+type)
        this.entityqueryInfo.page = newPage
        this.getEntitys(type)
      },
      // 监听pagesize改变事件
      entitySizeChange (newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.entityqueryInfo.size = newSize
        this.getEntitys()
      },
      // // 监听开关状态
      // async userstatechange (userinfo) {
      //   // var putdata = JSON.parse(JSON.stringify(userinfo))
      //   // delete putdata.id
      //   // delete putdata.url
      //   // console.log(putdata)
      //   // console.log(userinfo)
      //   const { data: res } = await
      //     this.$http.put(`users/${userinfo.id}/`, userinfo)
      // },
      //获取下拉框中内容
      getEntitys (type) {
        let _this = this
        this.$http.get('entity/', { params: this.entityqueryInfo })
          .then(res => {
            //请求返回的数据
            //赋值
            if(type=='customer'){
               _this.entityList = res.data
            }
            if(type=='owner'){
              _this.ownerentityList = res.data
            }
            // _this.entityList = res.data
            // console.log(res.data)
          }).catch((error) => {
          console.log(error)
        })
      },
      //关闭Dialog清空数据
      closeDialog (formName) {
        this.$refs[formName].resetFields()
      },
      //点击按钮添加新用户
      adduser () {
        this.$refs.addform.validate(
          async valid => {
            if (!valid) return
            //添加用户请求
            try {
              const { status: res } = await this.$http.post('/projects/', this.addform)
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
      openXiugai (row) {
        this.xiugaiVisible = true
        this.xiugaiForm = row
        // this.xiugaiForm.user_type = this.xiugaiForm.user_type.toString()

        //给下拉框赋值
        this.ownerentityList={'results':[{'id':row.owner_id,'entity_name':row.owner_name}]}
        this.entityList={'results':[{'id':row.customer_id,'entity_name':row.customer_name}]}
        // this.xiugaiForm.user_type=this.xiugaiForm.user_type.toString()
        //  console.log(row)
      },
      async xiugai (row) {
        const { data: ras } = await this.$http.get('/projects/${row.id}/')
        this.xiugaiVisible = true
      },
      //提交修改内容
      async xiugaiuser () {
        this.$refs.xiugaiForm.validate(
          async valid => {
            if (!valid) return
            // console.log(this.xiugaiForm.id)
            console.log(this.xiugaiForm)
            //修改用户请求
            try {
              const res = await this.$http.put(`/projects/${this.xiugaiForm.id}/`, this.xiugaiForm)
              console.log(res)
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
      async shanchu (id) {
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
          const { status: res } = await this.$http.delete(`/projects/${id}/`)
          if (res == 204) {
            this.$message.success('删除成功！')
            this.getUserList()
          }
        } catch (err) {
          this.$message.error('删除失败！' + err.toString())
        }
      },
    }
  }
</script>

<style lang="less" scoped>
  .item {
    margin: 4px;
  }
</style>
