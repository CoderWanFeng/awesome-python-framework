<template>
  <div>
    <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>财务管理</el-breadcrumb-item>
      <el-breadcrumb-item>综合查询</el-breadcrumb-item>
    </el-breadcrumb>
    <!--卡片视图区-->
    <el-card>
      <!--搜索与添加区域-->
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input placeholder="可查询项目名称、出差事由" v-model="queryInfo.query" clearable>
            <el-button slot="append" icon="el-icon-search" @click="getbaoxiaolist" clearable></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-date-picker
            v-model="timeRange"
            type="daterange"
            range-separator="-"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            @change="filterTime()"
            style="width: 100%">
          </el-date-picker>
        </el-col>
        <el-col :span="6">
          <el-select @click.native="getxmname()" v-model="xmbxForm.project_name" clearable placeholder="选择项目" filterable
                     style="width: 100%;" @change="xmbx">
            <el-option v-for="item in userlist.results" :value="item.id" :label="item.project_name"></el-option>
          </el-select>
        </el-col>
        <el-col :span="2">
          <el-button style="width: 100%;height: 40px" type="success" round @click="ybx">已报销</el-button>
        </el-col>
        <el-col :span="2">
          <el-button style="width: 100%;height: 40px" type="danger" round @click="wbx">未报销</el-button>
        </el-col>
        <el-col :span="2">
          <el-button style="width: 100%;height: 40px" type="primary" round @click="cz">重置</el-button>
        </el-col>
        <el-col :span="8">
          <el-select @click.native="getusername()" v-model="xmspForm.name" clearable placeholder="选择报销人" filterable
                     style="width: 100%; margin-top: 20px;" @change="yh">
            <el-option v-for="item in userlist.results" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-col>
      </el-row>

      <!--用户列表区-->
      <el-table :data="baoxiaolist" border style="margin-top: 20px;"
                :header-cell-style="{'text-align':'center'}"
                :cell-style="{'text-align':'center'}"
                show-summary
                :summary-method="getSummaries"
                @row-click="ctdk">
        <el-table-column prop="type" label="报销类型">
          <template slot-scope="scope">
            <p v-if="scope.row.type==='a'" style="color: #00bfff"> {{leixin[scope.row.type]}}</p>
            <p v-if="scope.row.type==='b'" style="color: #73e073"> {{leixin[scope.row.type]}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="user" label="报销人"></el-table-column>
        <el-table-column prop="pj_name" label="项目名称"></el-table-column>
        <el-table-column prop="cause" label="报销事由说明"></el-table-column>
        <el-table-column prop="account_date" label="报销时间"></el-table-column>
        <el-table-column prop="money" label="报销金额">
          <template slot-scope="scope">
            ¥{{scope.row.money}}
          </template>
        </el-table-column>
        <el-table-column prop="finish_flag" label="报销状态">
          <template slot-scope="scope">
            <el-tag :type="scope.row.finish_flag ? 'success' : 'danger'">
              {{level[scope.row.finish_flag]}}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <!--分页区域-->
      <div class="block">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.page"
          :page-sizes="[10, 50, 100, 200]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="restdata.count">
        </el-pagination>
      </div>
    </el-card>
    <!--    项目报销抽屉-->
    <el-drawer :visible.sync="drawer"
               title="项目报销"
               size="40%"
               @close="ctgb('ctForm')"
    >
      <el-form label-width="80px" :model="ctForm" ref="ctForm">
        <el-col :span="22">
          <el-form-item prop="pj_name" label="报销项目">
            <el-input v-model="ctForm.pj_name" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="start_date" label="出发时间">
            <el-input v-model="ctForm.start_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="end_date" label="返回时间">
            <el-input v-model="ctForm.end_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="sumDate" label="总天数">
            <el-input v-model="ctForm.sumDate" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="sumButie" label="总补贴">
            <el-input v-model="ctForm.sumButie" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="jtfs" label="交通方式">
            <el-input v-model="ctForm.jtfs" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="money_traffic" label="交通费">
            <el-input v-model="ctForm.money_traffic" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="zhushu" label="住宿费">
            <el-input v-model="ctForm.zhushu" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="finish_flag" label="状态">
            <template>
              <el-tag :type="ctForm.finish_flag ? 'success' : 'danger'" style="width: 100%">
                {{level[ctForm.finish_flag]}}
              </el-tag>
            </template>
          </el-form-item>
        </el-col>
        <el-col :span="22">
          <el-form-item prop="explain" label="事由说明">
            <el-input type="textarea" :rows="2" placeholder="请输入内容"
                      style="width: 100%" v-model="ctForm.explain" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="user" label="报销人">
            <el-input v-model="ctForm.user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="account_date" label="报销时间">
            <el-input v-model="ctForm.account_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approve_user" label="审批人">
            <el-input v-model="ctForm.approve_user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approvetime" label="审批时间">
            <el-input v-model="ctForm.approvetime" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
      </el-form>
    </el-drawer>
    <!--    其他项目报销抽屉-->
    <el-drawer :visible.sync="qtdrawer"
               title="其他报销"
               size="40%"
               @close="ctgb('qtctForm')"
    >
      <el-form label-width="80px" :model="qtctForm" ref="qtctForm">
        <el-col :span="22">
          <el-form-item prop="pj_name" label="报销项目">
            <el-input v-model="qtctForm.pj_name" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="money" label="报销金额">
            <el-input v-model="qtctForm.money" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="date" label="发生日期">
            <el-input v-model="qtctForm.date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="finish_flag" label="状态">
            <template>
              <el-tag :type="qtctForm.finish_flag ? 'success' : 'danger'" style="width: 100%">
                {{level[qtctForm.finish_flag]}}
              </el-tag>
            </template>
          </el-form-item>
        </el-col>
        <el-col :span="22">
          <el-form-item prop="pj_name" label="事由说明">
            <el-input type="textarea" :rows="2" placeholder="请输入内容"
                      style="width: 100%" v-model="qtctForm.cause" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="user" label="报销人">
            <el-input v-model="qtctForm.user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="account_date" label="报销时间">
            <el-input v-model="qtctForm.account_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approve_user" label="审批人">
            <el-input v-model="qtctForm.approve_user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approvetime" label="审批时间">
            <el-input v-model="qtctForm.approvetime" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
      </el-form>
    </el-drawer>
  </div>
</template>

<script>
  export default {
    name: 'baoxiachaxun',
    data() {
      return {
        timeRange: '',
        form: {
          name: '',
          type: [],
        },
        // 获取用户列表的参数对象
        queryInfo: {
          query: '',
          page: 1,
          size: 50,
        },
        xmbxForm: {
          project_name: '',
        },
        projectlist: [],
        ctForm: {
          start_date: '',
          end_date: '',
          money_traffic: '',
          zhushu: '',
          sumButie: 50,
          sumDate: 1,
          explain: '',
          project_name: '',
          Type_traffic: '',
          pj_name: '',
          id: '',
          account_date: '',
          jtfs: '',
          approve_user: '',
          approvetime: '',
        },
        qtctForm: {
          money: '',
          cause: '',
          date: '',
          project_name: '',
          pj_name: '',
          project_id: '',
          account_date: '',
        },
        drawer: false,
        qtdrawer: false,
        baoxiaolist: [],
        ctlist: [],
        deptlist: '',
        userlist: '',
        restdata: '',
        xmspForm: {
          name: '',
          id: '',
        },
        level: {
          0: '未报销',
          1: '已报销'
        },
        leixin: {
          a: '项目报销',
          b: '其他报销'
        },
      }
    },
    created() {
      this.getbaoxiaolist()
    },
    methods: {
      async getbaoxiaolist() {
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
        // console.log(this.baoxiaolist)
      },
      // 监听pagesize改变事件
      handleSizeChange(newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.queryInfo.size = newSize
        this.getbaoxiaolist()
      },
      // // 监听页码改变
      handleCurrentChange(newPage) {
        // console.log(`当前页: ${newPage}`)
        this.queryInfo.page = newPage
        this.getbaoxiaolist()
      },
// 获取项目信息
      getxmname() {
        let _this = this
        this.$http.get('projects/')
          .then(res => {
            _this.userlist = res.data
            // console.log(res)

          }).catch((error) => {
          console.log(error)
        })
      },
      // 获取报销人信息
      getusername() {
        let _this = this
        this.$http.get('users/')
          .then(res => {
            _this.userlist = res.data
            _this.yuserlist = res.data
            // console.log(res)

          }).catch((error) => {
          console.log(error)
        })
      },
      //点击行数据打开抽屉
      async ctdk(row) {
        // let thisRowData = this;
        // thisRowData = row;
        //如果是项目出差
        if (row.type === 'a') {
          this.drawer = true
          // console.log(row.tableid)
          const {data: res} = await this.$http.get(`/Account_projects/${row.tableid}/`)
          this.ctForm = res
          console.log(this.ctForm)
        }
        //如果是其它出差
        if (row.type === 'b') {
          this.qtdrawer = true
          console.log(row.tableid)
          const {data: res} = await this.$http.get(`/Account_normals/${row.tableid}/`)
          this.qtctForm = res
          console.log(this.qtctForm)
        }
      },
      //关闭ct清空数据
      ctgb(formName) {
        this.$refs[formName].resetFields()
        this.getbaoxiaolist()
      },
      async filterTime() {
        if (this.timeRange === null) {
          this.getbaoxiaolist()
          return
        }
        // console.log(this.timeRange)
        let timelte = {"timelte": this.timeRange[1]}
        let timegte = {"timegte": this.timeRange[0]}
        let obj = {...this.queryInfo, ...timelte, ...timegte}
        const {data: res} = await this.$http.get('/Account_views', {
          params: obj
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      },
      async yh(row) {
        this.queryInfo.expense_name = this.xmspForm.name
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      },
      getSummaries(param) {
        const { columns, data } = param;
        const sums = [];
        columns.forEach((column, index) => {
          if (index === 0) {
            sums[index] = '合计';
            return;
          }
          const values = data.map(item => Number(item[column.property]));
          if (column.property === 'money' ) {
            sums[index] = values.reduce((prev, curr) => {
              const value = Number(curr);
              if (!isNaN(value)) {
                return prev + curr;
              } else {
                return prev;
              }
            }, 0);
            sums[index]+= ' 元';
          }
        });
        return sums
      },

      async wbx() {
        this.queryInfo.finish_flag = 0
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      },
      async ybx() {
        this.queryInfo.finish_flag = 1
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      },
      async cz() {
        this.queryInfo.finish_flag = ''
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      },
      async xmbx(row) {
        this.queryInfo.project_name = this.xmbxForm.project_name
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      }
    },

  }

</script>

<style scoped>

</style>
