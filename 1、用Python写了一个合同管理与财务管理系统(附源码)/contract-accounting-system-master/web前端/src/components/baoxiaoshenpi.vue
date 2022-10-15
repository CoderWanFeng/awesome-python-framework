<template>
<div>
  <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
  <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item>财务管理</el-breadcrumb-item>
    <el-breadcrumb-item>报销审批</el-breadcrumb-item>
  </el-breadcrumb>
  <!--卡片视图区-->
  <el-card>
    <div>
      <el-col :span="6">
        <el-select @click.native="getusername()" v-model="xmspForm.name" clearable placeholder="选择报销人" filterable
                   style="width: 100%;" @change="xmsp" >
          <el-option v-for="item in userlist" :value="item.id" :label="item.name"></el-option>
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-button @click="toggleSelection(baoxiaolist)">全选</el-button>
        <el-button @click="toggleSelection()" :disabled="multipleSelection.length === 0">取消选择</el-button>
        <el-button @click="tjbx()" :disabled="multipleSelection.length === 0" type="primary">报销</el-button>
      </el-col>
<!--导出-->
      <el-button @click="bxzhdk" :disabled="multipleSelection.length === 0" type="primary">
        项目报销整合
      </el-button>
    </div>

    <!--报销列表区-->
    <el-table :data="baoxiaolist"
              :header-cell-style="{'text-align':'center'}"
              :cell-style="{'text-align':'center'}"
              ref="multipleTable"
              tooltip-effect="light"
              show-summary
              :summary-method="getSummaries"
              @row-click="ctdk"
              style="width: 100%; margin-top: 60px;"
              @selection-change="handleSelectionChange"
              border fit highlight-current-row >
      <el-table-column type="selection" width="55" :disable="isdisable">
      </el-table-column>
      <el-table-column label="序号"  width="55"
        type="index">
      </el-table-column>
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
<!--    出差报销抽屉-->
    <el-drawer :visible.sync="drawer"
               title="出差报销"
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
        <el-form-item prop="start_addr" label="出发地点">
            <el-input v-model="ctForm.start_addr" :disabled="true"></el-input>
        </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item prop="end_addr" label="目的地点">
              <el-input v-model="ctForm.end_addr" :disabled="true">
              </el-input>
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
    <el-drawer :visible.sync="qtdrawer" size="40%"
               title="其他报销"
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
  </el-card>
  <el-card style="margin-top: 20px;">
    <div>
      <el-col :span="6">
        <el-select @click.native="getusername()" v-model="xmyspForm.name" clearable placeholder="选择报销人" filterable
                   style="width: 100%;" @change="yxmsp" >
          <el-option v-for="item in yuserlist" :value="item.id" :label="item.name"></el-option>
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-button @click="ytoggleSelection(ybaoxiaolist)">全选</el-button>
        <el-button @click="ytoggleSelection()" :disabled="ymultipleSelection.length === 0">取消选择</el-button>
        <el-button @click="ytjbx()" :disabled="ymultipleSelection.length === 0" type="primary">撤销</el-button>
      </el-col>
    </div>

    <!--列表区-->
    <el-table :data="ybaoxiaolist"
              :header-cell-style="{'text-align':'center'}"
              :cell-style="{'text-align':'center'}"
              ref="ymultipleTable"
              tooltip-effect="light"
              @row-click="yctdk"
              style="width: 100%;margin-top: 60px;" @selection-change="yhandleSelectionChange" stripe border fit highlight-current-row >
      <el-table-column type="selection" width="55" :disable="isdisable">
      </el-table-column>
      <el-table-column label="序号"  width="55"
        type="index">
      </el-table-column>
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
        @size-change="yhandleSizeChange"
        @current-change="yhandleCurrentChange"
        :current-page="yqueryInfo.page"
        :page-sizes="[10, 50, 100, 200]"
        :page-size="yqueryInfo.size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="yrestdata.count">
      </el-pagination>
    </div>
    <!--    项目报销抽屉-->
    <el-drawer :visible.sync="ydrawer" size="40%"
               title="项目报销"
               @close="yctgb('yctForm')"
    >
      <el-form label-width="80px" :model="yctForm" ref="yctForm">
        <el-col :span="22">
          <el-form-item prop="pj_name" label="报销项目">
            <el-input v-model="yctForm.pj_name" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="start_date" label="出发时间">
            <el-input v-model="yctForm.start_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="end_date" label="返回时间">
            <el-input v-model="yctForm.end_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="sumDate" label="总天数">
            <el-input v-model="yctForm.sumDate" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="sumButie" label="总补贴">
            <el-input v-model="yctForm.sumButie" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="jtfs" label="交通方式">
            <el-input v-model="yctForm.jtfs" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="money_traffic" label="交通费">
            <el-input v-model="yctForm.money_traffic" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="zhushu" label="住宿费">
            <el-input v-model="yctForm.zhushu" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="finish_flag" label="状态">
            <template>
              <el-tag :type="yctForm.finish_flag ? 'success' : 'danger'" style="width: 100%">
                {{level[yctForm.finish_flag]}}
              </el-tag>
            </template>
          </el-form-item>
        </el-col>
        <el-col :span="22">
          <el-form-item prop="explain" label="事由说明">
            <el-input type="textarea" :rows="2" placeholder="请输入内容"
                      style="width: 100%" v-model="yctForm.explain" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="user" label="报销人">
            <el-input v-model="yctForm.user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="account_date" label="报销时间">
            <el-input v-model="yctForm.account_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approve_user" label="审批人">
            <el-input v-model="yctForm.approve_user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approve_time" label="审批时间">
            <el-input v-model="yctForm.approvetime" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
      </el-form>
    </el-drawer>
    <!--    其他项目报销抽屉-->
    <el-drawer :visible.sync="yqtdrawer"
               title="其他报销"
               size="40%"
               @close="yctgb('yqtctForm')"
    >
      <el-form label-width="80px" :model="yqtctForm" ref="yqtctForm">
        <el-col :span="22">
          <el-form-item prop="pj_name" label="报销项目">
            <el-input v-model="yqtctForm.pj_name" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="money" label="报销金额">
            <el-input v-model="yqtctForm.money" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="date" label="发生日期">
            <el-input v-model="yqtctForm.date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="finish_flag" label="状态">
            <template>
              <el-tag :type="yqtctForm.finish_flag ? 'success' : 'danger'" style="width: 100%">
                {{level[yqtctForm.finish_flag]}}
              </el-tag>
            </template>
          </el-form-item>
        </el-col>
        <el-col :span="22">
          <el-form-item prop="pj_name" label="事由说明">
            <el-input type="textarea" :rows="2" placeholder="请输入内容"
                      style="width: 100%" v-model="yqtctForm.cause" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="user" label="报销人">
            <el-input v-model="yqtctForm.user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="account_date" label="报销时间">
            <el-input v-model="yqtctForm.account_date" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approve_user" label="审批人">
            <el-input v-model="yqtctForm.approve_user" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="approvetime" label="审批时间">
            <el-input v-model="yqtctForm.approvetime" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
      </el-form>
    </el-drawer>
  </el-card>

  <el-dialog
  title="报销整合"
  @close="closeBxzh"
  :visible.sync="bxVisible"
  width="80%"
>
    <el-table :data="bxlist"
              :header-cell-style="{'text-align':'center'}"
              :cell-style="{'text-align':'center'}"
              tooltip-effect="light"
              id="dayin"
              style="width: 100%; " border fit highlight-current-row >
      <el-table-column label="序号"  width="55" type="index">
      </el-table-column>
      <el-table-column label="人员" prop="user"></el-table-column>
      <el-table-column label="出差日期" prop="start_date"></el-table-column>
      <el-table-column label="地点">
        <el-table-column label="起点" prop="start_addr"></el-table-column>
        <el-table-column label="终点" prop="end_addr"></el-table-column>
      </el-table-column>
      <el-table-column label="交通费">
        <el-table-column label="交通方式" prop="jtfs"></el-table-column>
        <el-table-column label="交通费" prop="money_traffic"></el-table-column>
      </el-table-column>
      <el-table-column label="出差天数" prop="sumDate"></el-table-column>
      <el-table-column label="住宿费" prop="zhushu"></el-table-column>
      <el-table-column label="补贴" prop="sumButie"></el-table-column>
      <el-table-column label="出差项目" prop="pj_name"></el-table-column>
    </el-table>
    <el-button v-print="'#dayin'">打印</el-button>
    &nbsp;
    <el-button  @click="outTab" style="margin-left: 80px;margin-top: 30px;">导出</el-button>

</el-dialog>
</div>

</template>

<script>

  export default {
    name: 'baoxiaoshenpi',
    data() {
      return {
        // 获取用户列表的参数对象
        queryInfo: {
          query: '',
          page: 1,
          size: 50,
        },
        yqueryInfo: {
          query: '',
          page: 1,
          size: 50,
        },
        xmspForm: {
          name: '',
          id: '',
        },
        xmyspForm: {
          name: '',
          id: '',
        },
        baoxiaolist: [],
        bxlist: [],
        ybaoxiaolist: [],
        restdata: '',
        yrestdata: '',
        userlist: '',
        yuserlist: '',
        bxForm:{},
        bxVisible: false,
        multipleSelection: [],
        ymultipleSelection: [],
        bxmultipleSelection: [],
        isdisable: false,
        level: {
          0: '未报销',
          1: '已报销'
        },
        leixin: {
          a: '项目报销',
          b: '其他报销'
        },
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
        yctForm: {
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
          approve_user: '',
          approvetime: '',
        },
        yqtctForm: {
          money: '',
          cause: '',
          date: '',
          project_name: '',
          pj_name: '',
          project_id: '',
          account_date: '',
          approve_user: '',
          approvetime: '',
        },
        drawer: false,
        qtdrawer: false,
        ydrawer: false,
        yqtdrawer: false,
      }
    },
    created() {
      this.getbaoxiaolist()
      this.ygetbaoxiaolist()
    },
    // 导出
    // json_fields: {
    //   "头部-": "name",    //常规字段
    //   "头部-": "phone.mobile", //支持嵌套属性
    //   "头部-": {
    //     field: "phone.landline",
    //     //自定义回调函数
    //     callback: value => {
    //       return `损坏区域代码 - ${value}`;
    //     }
    //   }
    // },
    // json_data: [
    //
    // ],
    // json_meta: [
    //   [
    //     {
    //       " key ": " charset ",
    //       " value ": " utf- 8 "
    //     }
    //   ]
    // ],

    methods: {
      async getbaoxiaolist() {
        this.queryInfo.finish_flag = 0
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
        // console.log(this.baoxiaolist)
      },
      closeBxzh(){
        this.bxlist.length = 0;
      },
      bxgb (formName) {
        this.$refs[formName].resetFields()
        this.getbaoxiaolist()
      },
      async ygetbaoxiaolist() {
        this.yqueryInfo.finish_flag = 1
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.yqueryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.yrestdata = res
        this.ybaoxiaolist = res.results
        // console.log(this.baoxiaolist)
      },
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        //val 为选中数据的集合
        this.multipleSelection = val;
      },
      ytoggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.ymultipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.ymultipleTable.clearSelection();
        }
      },
      yhandleSelectionChange(val) {
        //val 为选中数据的集合
        this.ymultipleSelection = val;
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
      yhandleSizeChange(newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.yqueryInfo.size = newSize
        this.ygetbaoxiaolist()
      },
      // // 监听页码改变
      yhandleCurrentChange(newPage) {
        // console.log(`当前页: ${newPage}`)
        this.yqueryInfo.page = newPage
        this.ygetbaoxiaolist()
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
          // console.log(this.ctForm)
        }
        //如果是其它出差
        if (row.type === 'b') {
          this.qtdrawer = true
          // console.log(row.tableid)
          const {data: res} = await this.$http.get(`/Account_normals/${row.tableid}/`)
          this.qtctForm = res
          // console.log(this.qtctForm)
        }
      },
      //点击行数据打开抽屉
      async yctdk(row) {
        // let thisRowData = this;
        // thisRowData = row;
        //如果是项目出差
        if (row.type === 'a') {
          this.ydrawer = true
          // console.log(row.tableid)
          const {data: res} = await this.$http.get(`/Account_projects/${row.tableid}/`)
          this.yctForm = res
          // console.log(this.yctForm)
        }
        //如果是其它出差
        if (row.type === 'b') {
          this.yqtdrawer = true
          // console.log(row.tableid)
          const {data: res} = await this.$http.get(`/Account_normals/${row.tableid}/`)
          this.yqtctForm = res
          // console.log(this.yqtctForm)
        }
      },
      //关闭ct清空数据
      ctgb(formName) {
        this.$refs[formName].resetFields()
        this.getbaoxiaolist()
      },
      yctgb(formName) {
        this.$refs[formName].resetFields()
        this.ygetbaoxiaolist()
      },
      // 获取报销人信息
      getusername() {
        let _this = this
        this.$http.get('usersall/')
          .then(res => {
            _this.userlist = res.data
            _this.yuserlist = res.data
            // console.log(res)

          }).catch((error) => {
          console.log(error)
        })
      },
      async xmsp() {
        this.queryInfo.expense_name = this.xmspForm.name
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      },
      async yxmsp() {
        this.yqueryInfo.expense_name = this.xmyspForm.name
        const {data: res} = await this.$http.get('/Account_views', {
          params: this.yqueryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.yrestdata = res
        this.ybaoxiaolist = res.results
      },
      async tjbx() {
        const confirmResult = await this.$confirm('此操作将提交该报销, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).catch(err => err)
        if (confirmResult !== 'confirm') {
          return this.$message.info('已取消报销')
        }
        var arr = this.multipleSelection;
        let a = [];
        let b = [];
        for (let item in arr) {
          if (arr[item].type === 'a') {
            var obj = {'pk': null, 'finish_flag': 1}
            obj.pk = arr[item].tableid
            a.push(obj)
            // a.push(finish_flag===1)
          }
          if (arr[item].type === 'b') {
            var bbj = {'pk': null, 'finish_flag': 1}
            bbj.pk = arr[item].tableid
            b.push(bbj)
          }
        }

        if (a.length !== 0) {
          try {
            var res = await this.$http.patch(`/Account_projects/`, a)
            if (res.status === 200) {
              this.$message.success('成功审批出差报销' + res.data.results.length + "条报销记录")
            }
          } catch (err) {
            this.$message.error('提交出差报销失败！' + err.toString())
          }
          // console.log(res)
          this.$refs.multipleTable.clearSelection();
          this.ygetbaoxiaolist()
          this.getbaoxiaolist()
        }
        if (b.length !== 0) {
          try {
            var bres = await this.$http.patch(`/Account_normals/`, b)
            if (bres.status === 200) {
              this.$message.success('成功审批其他项目报销' + bres.data.results.length + "条报销记录")
            }
          } catch (err) {
            this.$message.error('提交其他项目报销失败！' + err.toString())
          }
          // console.log(bres)
          this.$refs.multipleTable.clearSelection();
          this.ygetbaoxiaolist()
          this.getbaoxiaolist()
        }
      },
      async ytjbx() {
        const confirmResult = await this.$confirm('此操作将撤销该报销, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).catch(err => err)
        if (confirmResult !== 'confirm') {
          return this.$message.info('已取消撤销')
        }
        var yarr = this.ymultipleSelection;
        let ya = [];
        let yb = [];
        for (let item in yarr) {
          if (yarr[item].type === 'a') {
            var yobj = {'pk': null, 'finish_flag': 0}
            yobj.pk = yarr[item].tableid
            ya.push(yobj)
            // a.push(finish_flag===1)
          }
          if (yarr[item].type === 'b') {
            var ybbj = {'pk': null, 'finish_flag': 0}
            ybbj.pk = yarr[item].tableid
            yb.push(ybbj)
          }
        }
        // console.log(a)
        // console.log(b)
        // console.log(bbj)
        // console.log(obj)
        if (ya.length !== 0) {
          try {
            var res = await this.$http.patch(`/Account_projects/`, ya)
            if (res.status === 200) {
              this.$message.success('成功撤销项目报销'+ res.data.results.length+"条报销记录")
            }
          } catch (err) {
            this.$message.error('提交项目报销失败！' + err.toString())
          }
          // console.log(res)
          this.$refs.ymultipleTable.clearSelection();
          this.ygetbaoxiaolist()
          this.getbaoxiaolist()
        }
        if (yb.length !== 0) {
          try {
            var ybres = await this.$http.patch(`/Account_normals/`, yb)
            if (ybres.status === 200) {
              this.$message.success('成功撤销其他项目报销'+ ybres.data.results.length+"条报销记录")
            }
          } catch (err) {
            this.$message.error('撤销其他项目报销失败！' + err.toString())
          }
          // console.log(ybres)
          this.$refs.ymultipleTable.clearSelection();
          this.ygetbaoxiaolist()
          this.getbaoxiaolist()
        }
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
      async bxzhdk(){
        this.bxVisible = true
        var bxarr = this.multipleSelection;
        //判断选择的是否包含非项目报销
        for(let item in bxarr){
         if(bxarr[item].type == 'b') {
           this.$message.error("只能对项目报销条目进行整合！")
           this.bxVisible = false
           return
         }
        }
        for (let item in bxarr) {
          // console.log(bxarr[item].tableid)
          const {data: res} = await this.$http.get(`/Account_projects/${bxarr[item].tableid}/`)
          this.bxlist.push(res)
        }

      },
       outTab() {
      require.ensure([], () => {
        const { export_json_to_excel } = require('../excel/Export2Excel') //注意这个Export2Excel路径
        const tHeader = [ '报销人员', '出差日期', '出发地', '目的地', '交通方式', '交通费','出差天数','住宿费','出差补贴','出差项目','备注说明'] // 上面设置Excel的表格第一行的标题
        const filterVal = ['user', 'start_date', 'start_addr', 'end_addr', 'jtfs', 'money_traffic', 'sumDate','zhushu','sumButie','pj_name','explain'] // 上面的index、nickName、name是tableData里对象的属性key值
        const list = this.bxlist //把要导出的数据tableData存到list
        const data = this.formatJson(filterVal, list)
        export_json_to_excel(tHeader, data, '报销整合表格') //最后一个是表名字
      })
    },
    //格式转换,不需要改动
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    },
      async exportExcel() {
        // 创建工作簿
        const wb = new this.ExcelJS.Workbook();
        // 添加工作表,也就是我们Excel的页签
        const ws1 = wb.addWorksheet("第一页");
        // 添加表格的标题
        ws1.addRow(['报销单']);
        // 添加表格的表头信息和样式
        ws1.addRow(['人员', '出差日期', '地点', '交通费', '出差天数', '住宿费', '补贴', '出差项目']).font = {
          bold: true,
          color: {
            argb: '909399'
          }
        };
        ws1.addRow(['','', '起点', '终点']).font = {
          bold: true,
          color: {
            argb: '909399'
          }
        };
        ws1.addRow(['', '','',  '交通方式', '交通费']).font = {
          bold: true,
          color: {
            argb: '909399'
          }
        };
        // 依照表格合并单元格
        ws1.mergeCells('A1:F1');
        ws1.mergeCells('B2:F2');
        ws1.mergeCells('C3:F3');
        ws1.mergeCells('A2:A4');
        ws1.mergeCells('B3:B4');
        // 设置表格标题的样式
        ws1.getRow(1).alignment = {
          vertical: 'middle',
          horizontal: 'center'
        }
        // 插入表格数据
        this.tableData.forEach((item) => {
          let {
            date,
            name,
            province,
            city,
            address,
            zip
          } = item;
          ws1.addRow([date, name, province, city, address, zip]).font = {
            bold: true,
            color: {
              argb: '606266'
            }
          };
        });
        // 写入 buffer
        const buf = await wb.xlsx.writeBuffer();
        // 导出Excel,并且命名为"导出的表格.xlsx"
        saveAs(new Blob([buf]), "导出的表格.xlsx");
      }
        // let ya = [];
        // let yb = [];
        // for (let item in yarr) {
        //   if (yarr[item].type === 'a') {
        //     var yobj = {'pk': null, 'finish_flag': 0}
        //     yobj.pk = yarr[item].tableid
        //     ya.push(yobj)
        //     // a.push(finish_flag===1)
        //   }
        //   if (yarr[item].type === 'b') {
        //     var ybbj = {'pk': null, 'finish_flag': 0}
        //     ybbj.pk = yarr[item].tableid
        //     yb.push(ybbj)
        //   }
        // this.bxlist = this.multipleSelection
      }
  }
</script>

<style scoped>
</style>
