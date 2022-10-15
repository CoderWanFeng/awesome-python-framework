<template>
  <div>
    <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>信息管理</el-breadcrumb-item>
      <el-breadcrumb-item>单位信息</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <div style="margin-bottom: 10px;text-align: left">
        <el-button type="primary" @click="dialogVisible = true"> 新增单位实体</el-button>
      </div>
      <!--    显示单位信息表-->
      <el-table :data="entitylist" stripe border>
        <el-table-column label="单位名称" prop="entity_name" fixed></el-table-column>
        <el-table-column label="地址" prop="entity_addr"></el-table-column>
        <el-table-column label="电话" prop="phone"></el-table-column>
        <el-table-column label="开户银行" prop="bank_addr"></el-table-column>
        <el-table-column label="银行帐号" prop="bank_number"></el-table-column>
        <el-table-column label="税号" prop="shuiHao"></el-table-column>
        <el-table-column label="备注" prop="explain"></el-table-column>
        <el-table-column label="编辑" fixed="right" width="120px">
          <template slot-scope="scope">
            <!--修改按钮-->
            <el-tooltip class="item" effect="dark" content="修改按钮" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="openeditEntity(scope.row)"></el-button>
            </el-tooltip>
            <!--删除按钮-->
            <el-tooltip class="item" effect="dark" content="删除按钮" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini"
                         @click="deleteEntity(scope.row.id)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!--分页-->
      <div class="block">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.page"
          :page-sizes="[10,50]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="restdata.count">
        </el-pagination>
      </div>
    </el-card>


    <!--    新增单位实例弹框-->
    <el-dialog title="添加单位" :visible.sync="dialogVisible" width="50%">
      <el-form :model="addEntityForm" :rules="entityFormRules" ref="addEntityForm" style="text-align: left;"
               label-width="80px">
        <el-form-item label="单位名称" prop="entity_name">
          <el-input v-model="addEntityForm.entity_name" placeholder="请输入单位或公司名称"></el-input>
        </el-form-item>
        <el-form-item label="单位地址" prop="entity_addr">
          <el-input v-model="addEntityForm.entity_addr"></el-input>
        </el-form-item>
        <el-form-item label="单位电话" prop="phone">
          <el-input v-model="addEntityForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="开户银行" prop="bank_addr">
          <el-input v-model="addEntityForm.bank_addr"></el-input>
        </el-form-item>
        <el-form-item label="银行帐号" prop="bank_number">
          <el-input v-model="addEntityForm.bank_number"></el-input>
        </el-form-item>
        <el-form-item label="信用税号" prop="shuiHao">
          <el-input v-model="addEntityForm.shuiHao"></el-input>
        </el-form-item>
        <el-form-item label="备注信息" prop="explain">
          <el-input type="textarea" v-model="addEntityForm.explain"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addEntity">确 定</el-button>
  </span>
    </el-dialog>
    <!--    编辑单位信息-->
    <el-dialog title="编辑单位信息" :visible.sync="editdialogVisible" width="50%" @close="closeDialog('editEntityForm')">
      <el-form :model="editEntityForm" :rules="entityFormRules" ref="editEntityForm" style="text-align: left;"
               label-width="80px">
        <el-form-item label="单位名称" prop="entity_name">
          <el-input v-model="editEntityForm.entity_name" placeholder="请输入单位或公司名称"></el-input>
        </el-form-item>
        <el-form-item label="单位地址" prop="entity_addr">
          <el-input v-model="editEntityForm.entity_addr"></el-input>
        </el-form-item>
        <el-form-item label="单位电话" prop="phone">
          <el-input v-model="editEntityForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="开户银行" prop="bank_addr">
          <el-input v-model="editEntityForm.bank_addr"></el-input>
        </el-form-item>
        <el-form-item label="银行帐号" prop="bank_number">
          <el-input v-model="editEntityForm.bank_number"></el-input>
        </el-form-item>
        <el-form-item label="信用税号" prop="shuiHao">
          <el-input v-model="editEntityForm.shuiHao"></el-input>
        </el-form-item>
        <el-form-item label="备注信息" prop="explain">
          <el-input type="textarea" v-model="editEntityForm.explain"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="editdialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="editEntity">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    name: 'entityInfo',

    data () {
      return {
        entitylist: [],
        dialogVisible: false,
        editdialogVisible: false,
        addEntityForm: {
          entity_name: '',
          entity_addr: '',
          phone: '',
          bank_addr: '',
          bank_number: '',
          shuiHao: '',
          explain: '',
        },
        editEntityForm: {},
        restdata: {},
        queryInfo: {
          query: '',
          page: 1,
          size: 10,
        },
        entityFormRules: {
          entity_name: [
            {
              required: true,
              message: '请输单位名称',
              trigger: 'blur'
            },
          ],
        },

      }
    },
    created () {
      this.getEntitylist()
    },
    methods: {
      //获取显示数据
      getEntitylist () {
        this.$http.get('entity/', { params: this.queryInfo }).then(res => {
          this.restdata = res.data
          this.entitylist = res.data.results
        }).catch((error) => {
          this.$message.error(error)
        })
      },
      handleSizeChange (newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.queryInfo.size = newSize
        this.getEntitylist()
      },
      // // // 监听页码改变
      handleCurrentChange (newPage) {
        // console.log(`当前页: ${newPage}`)
        this.queryInfo.page = newPage
        this.getEntitylist()
      },
      // 新增单位
      addEntity () {
        this.$refs.addEntityForm.validate(
          async valid => {
            if (!valid) return this.$message.error('请输入单位名称才能提交')
            const loading = this.$loading({
              lock: true,
              text: '正在提交',
              spinner: 'el-icon-loading',
              background: 'rgba(0, 0, 0, 0.7)'
            })
            try {
              const { status: res } = await this.$http.post('entity/', this.addEntityForm)
              if (res == 201) this.$message.success('添加成功！')
              this.dialogVisible = false
              loading.close()
              // this.getEntitylist()
            } catch (e) {
              this.dialogVisible = false
              loading.close()
              this.$message.error('操作失败！' + e.toString())
            }
          }
        )
      },
      //编辑单位信息
      openeditEntity (row) {
        this.editdialogVisible = true
        this.editEntityForm = row
      },
      editEntity () {
        this.$refs.editEntityForm.validate(
          async valid => {
            if (!valid) return this.$message.error('请输入单位名称才能提交')
            try {
              const { status: res } = await this.$http.put(`entity/${this.editEntityForm.id}/`, this.editEntityForm)
              if (res == 200) {
                this.$message.success('修改成功！')
                // this.getEntitylist()
                this.editdialogVisible = false
              }
            } catch (e) {
              this.editdialogVisible = false
              this.$message.error('操作失败！' + e.toString())
            }
          }
        )
      },
      //删除单位
      async deleteEntity (id) {
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
          const { status: res } = await this.$http.delete(`entity/${id}/`)
          if (res == 204) {
            this.$message.success('删除成功！')
            this.getEntitylist();
          }
        } catch (err) {
          this.$message.error('删除失败！' + err.toString())
        }
      },
      //关闭Dialog清空数据
      closeDialog (formName) {
        this.$refs[formName].resetFields()
        this.getEntitylist();
      },
    }
  }
</script>

<style scoped>

</style>
