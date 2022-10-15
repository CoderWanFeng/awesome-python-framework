<template>
  <div>
    <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>信息管理</el-breadcrumb-item>
      <el-breadcrumb-item>部门信息</el-breadcrumb-item>
    </el-breadcrumb>
    <div style="margin-bottom: 10px;text-align: left">
      <el-button type="primary" @click="tianjiaVisible = true"> 新增部门</el-button>
    </div>

    <el-table :data="deptlist">
      <el-table-column label="部门名称" prop="dept_name"></el-table-column>
      <el-table-column label="部门经理" prop="dept_manager_name"></el-table-column>
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
    <!--添加部门-->
    <el-dialog title="添加部门" :visible.sync="tianjiaVisible" width="50%" @close="closeDialog('tianjiaForm')">
      <el-form :model="tianjiaForm" :rules="tianjiaFormRules" ref="tianjiaForm" style="text-align: left;"
               label-width="80px">
        <el-form-item label="部门名称" prop="dept_name">
          <el-input v-model="tianjiaForm.dept_name" placeholder="请输入部门名称"></el-input>
        </el-form-item>
        <el-form-item label="部门经理" prop="dept_manager_id">
          <el-select @click.native="getUsers()" v-model="tianjiaForm.dept_manager_id" placeholder="选择用户">
            <el-option v-for="item in userlist" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="tianjiaVisible = false">取 消</el-button>
    <el-button type="primary" @click="tianjia">确 定</el-button>
  </span>
    </el-dialog>

    <!--修改对话框-->
    <el-dialog title="修改部门" :visible.sync="xiugaiVisible" width="50%" @close="closeDialog('xiugaiForm')">
      <el-form :model="xiugaiForm" :rules="tianjiaFormRules" ref="xiugaiForm" style="text-align: left;"
               label-width="80px">
        <el-form-item label="部门名称" prop="dept_name">
          <el-input v-model="xiugaiForm.dept_name" placeholder="请输入部门名称"></el-input>
        </el-form-item>
        <el-form-item label="部门经理" prop="dept_manager_id">
           <el-select  v-model="xiugaiForm.dept_manager_id" placeholder="选择用户">
            <el-option v-for="item in userlist" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="xiugaiVisible = false">取 消</el-button>
    <el-button type="primary" @click="xiugaiuser">确 定</el-button>
  </span>
    </el-dialog>
  </div>

</template>

<script>
  export default {
    name: 'department',
    created() {
      this.getDeptList()
    },
    data() {
      return {
        deptlist: [],
        userlist:[],
        tianjiaVisible: false,
        tianjiaForm: {
          dept_name:'',
          dept_manager_id:null
        },
        tianjiaFormRules:{
          dept_name:[
            {
              required: true,
              message: '请输部门名称',
              trigger: 'blur'
            }
          ]
        },
        // 修改部门对话框的显示与隐藏
        xiugaiVisible: false,
        xiugaiForm: {},
      }
    },
    methods: {
      getDeptList() {
        this.$http.get('dept/').then(res => {
          // console.log(res.data)
          this.deptlist = res.data
        }).catch((error) => {
          this.$message.error(error)
        })
      },
      //新增部门
      tianjia() {
        this.$refs.tianjiaForm.validate(
          async valid => {
            if (!valid) return this.$message.error('请输入部门名称才能提交')
            const loading = this.$loading({
              lock: true,
              text: '正在提交',
              spinner: 'el-icon-loading',
              background: 'rgba(0, 0, 0, 0.7)'
            })
            try {
              const {status: res} = await this.$http.post('dept/', this.tianjiaForm)
              if (res == 201) this.$message.success('添加成功！')
              this.tianjiaVisible = false
              loading.close()
              this.getDeptList()
            } catch (e) {
              this.tianjiaVisible = false
              loading.close()
              this.$message.error('操作失败！' + e.toString())
            }
          }
        )
      },
      closeDialog (formName) {
        this.$refs[formName].resetFields()
        this.getDeptList();
      },
      // 打开修改用户的对话框
      openXiugai(row) {
        this.xiugaiVisible = true
        this.xiugaiForm = row
        this.getUsers()
        // this.xiugaiForm.user_type=this.xiugaiForm.user_type.toString()
        // console.log(row)
      },
      async xiugai(row) {
        const {data: ras} = await this.$http.get('/dept/${row.id}/')
        this.xiugaiVisible = true

      },
      getUsers(){
        this.$http.get('/users').then(res =>{
          this.userlist = res.data.results
          console.log(this.userlist)
        }
        ).catch((error) => {
          this.$message.error(error)
        })
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

              const res = await this.$http.put(`/dept/${this.xiugaiForm.id}/`, this.xiugaiForm)
              console.log(res)
              if (res.status == 200) {
                this.$message.success('修改成功！')
                this.xiugaiVisible = false
                this.getDeptList()
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
          const {status: res} = await this.$http.delete(`/dept/${id}/`)
          if (res == 204) {
            this.$message.success('删除成功！')
            this.getDeptList()
          }
        } catch(err) {
          this.$message.error('删除失败！' + err.toString())
        }
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
