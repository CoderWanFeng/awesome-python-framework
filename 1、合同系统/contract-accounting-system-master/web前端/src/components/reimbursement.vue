<template>
  <div>
    <el-card>

      <div>
        <!--  折叠板-->
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>报销管理</el-breadcrumb-item>
          <el-breadcrumb-item>新增报销</el-breadcrumb-item>
        </el-breadcrumb>
        <el-collapse accordion>
          <el-collapse-item style="text-align: center">
            <template slot="title" style="text-align: center">
              <p style="flex: 1 0 90%;order: -1;text-align: right;margin-right: 20px;color: rgba(22,131,215,0.97);">
                新增-展开</p>
            </template>
            <!--            标签页-->
            <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
              <!--项目报销标签页-->
              <el-tab-pane label="出差报销" name="first">
                <el-form label-width="80px" :model="ruleForm" :rules="rules" ref="ruleForm">
                  <el-form-item label="出差项目" prop="project_name">
                    <el-col :span="11">
                      <el-select @click.native="getusername()" v-model="ruleForm.project_name" clearable placeholder="选择项目"
                                 filterable
                                 style="width: 100%;">
                        <el-option v-for="item in userlist.results" :value="item.id"
                                   :label="item.project_name"></el-option>
                      </el-select>
                    </el-col>
                  </el-form-item>
                  <el-form-item prop="start_addr" label="出发地点">
                    <el-col :span="5">
                      <el-input v-model="ruleForm.start_addr" style="width: 100%"></el-input>

                    </el-col>
                    <el-col :span="6">
                      <el-form-item prop="end_addr" label="目的地点">
                        <el-input v-model="ruleForm.end_addr">
                        </el-input>
                      </el-form-item>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="出差时间" required label-width="80px">
                    <el-col :span="5">
                      <el-form-item prop="start_date">
                        <el-date-picker type="date" placeholder="开始日期" v-model="ruleForm.start_date"
                                        style="width: 100%;"
                                        format="yyyy年MM月dd月" value-format="yyyy-MM-dd"
                        ></el-date-picker>
                      </el-form-item>
                    </el-col>
                    <el-col :span="1">
                      <span style="font-size: 16px">-</span>
                    </el-col>
                    <el-col :span="5">
                      <el-form-item prop="end_date">
                        <el-date-picker type="date" placeholder="结束日期" v-model="ruleForm.end_date" style="width: 100%;"
                                        format="yyyy年MM月dd月" value-format="yyyy-MM-dd"></el-date-picker>
                      </el-form-item>
                    </el-col>
                  </el-form-item>
                  <el-form-item prop="sumDate" label="总天数">
                    <el-col :span="5">
                      <el-input-number @change="handleChange" :min="1" :max="30" v-model="ruleForm.sumDate"
                                       style="width: 100%"></el-input-number>

                    </el-col>
                    <el-col :span="6">
                      <el-form-item prop="sumButie" label="总补贴">
                        <el-input v-model="ruleForm.sumButie" type="number">
                        </el-input>
                      </el-form-item>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="交通方式" prop="Type_traffic">
                    <el-col :span="3 ">
                      <el-select @click.native="getjtfs()" v-model="ruleForm.Type_traffic" placeholder="选择交通方式"
                                 style="width: 100%">
                        <el-option v-for="item in jtfslist" :value="item.id" :label="item.project_name"></el-option>
                      </el-select>
                    </el-col>
                    <el-col :span="4">
                      <el-form-item label="交通费" prop="money_traffic">
                        <el-input v-model="ruleForm.money_traffic" type="number"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="4">
                      <el-form-item label="住宿费" prop="zhushu">
                        <el-input v-model="ruleForm.zhushu" type="number"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="项目说明" prop="explain">
                    <el-col :span="11">

                      <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="ruleForm.explain"
                                style="width: 100%">
                      </el-input>
                    </el-col>
                  </el-form-item>

                  <el-col>
                    <el-form-item>
                      <el-button type="primary" @click="submitForm()">提交报销</el-button>
                      <el-button @click="reset('ruleForm')">重置</el-button>
                    </el-form-item>
                  </el-col>
                </el-form>
              </el-tab-pane>
              <!--其他报销标签页-->
              <el-tab-pane label="其他报销" name="second">
                <el-form label-width="80px" :model="fbxForm" :rules="qtrules" ref="fbxForm">
                  <el-form-item label="出差项目" prop="project_name">
                    <el-col :span="11">
                      <el-select @click.native="getusername()" clearable v-model="fbxForm.project_name" placeholder="选择项目"
                                 filterable
                                 style="width: 100%;">
                        <el-option v-for="item in userlist.results" :value="item.id"
                                   :label="item.project_name"></el-option>
                      </el-select>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="报销金额" prop="money">
                    <el-col :span="11">
                      <el-input placeholder="请输入金额" v-model="fbxForm.money" style="width: 100%" type="number">
                      </el-input>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="发生日期">
                    <el-col :span="11">
                      <el-form-item prop="date">
                        <el-date-picker type="date" placeholder="报销日期" v-model="fbxForm.date"
                                        style="width: 100%;"
                                        format="yyyy年MM月dd月" value-format="yyyy-MM-dd"
                        ></el-date-picker>
                      </el-form-item>
                    </el-col>
                  </el-form-item>
                  <el-form-item label="报销内容" prop="cause">
                    <el-col :span="11">

                      <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="fbxForm.cause"
                                style="width: 100%">
                      </el-input>
                    </el-col>
                  </el-form-item>

                  <el-col>
                    <el-form-item>
                      <el-button type="primary" @click="fbxtjForm()">提交报销</el-button>
                      <el-button @click="reset('fbxForm')">重置</el-button>
                    </el-form-item>
                  </el-col>
                </el-form>

              </el-tab-pane>

            </el-tabs>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-card>

    <!--报销列表区-->
    <el-card style="margin-top: 20px">
      <div style="width: 100%">
        <div style="float: left;">
          <p style=" font-weight:bold;color: deepskyblue">
            出差报销</p>
        </div>
        <div style="margin-right: 20px;float: right">
          <p style=" font-weight:bold;color: deepskyblue;display:inline-block;">当前页总计:</p>
            <p style="font-weight: bold;color: red;display:inline-block;">¥{{zj}}</p>

        </div>
      </div>

      <el-table :data="projectlist" border style="margin-top: 20px;"
                :header-cell-style="{'text-align':'center'}"
                :cell-style="{'text-align':'center'}">

        <el-table-column prop="pj_name" label="出差项目"></el-table-column>
        <el-table-column prop="explain" label="出差说明"></el-table-column>
        <el-table-column label="金额详细">
          <template slot-scope="scope">
          住宿费:¥{{scope.row.zhushu}} 交通费:¥{{scope.row.money_traffic}} 总补贴:¥{{scope.row.sumButie}}
          </template>
        </el-table-column>
        <el-table-column prop="account_date" label="报销时间"></el-table-column>
        <el-table-column label="报销金额">
          <template slot-scope="scope">
            ¥{{scope.row.money_traffic + scope.row.sumButie + scope.row.zhushu}}
          </template>
        </el-table-column>
        <el-table-column prop="user" label="报销人"></el-table-column>


        <el-table-column label="编辑">
          <template slot-scope="scope">
            <!--修改按钮-->
            <el-tooltip class="item" effect="dark" content="修改按钮" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="ctdk(scope.row)"></el-button>
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
          :page-sizes="[5, 10, 50, 100]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="restdata.count">
        </el-pagination>
      </div>
    </el-card>
    <!--其他报销列表区-->
    <el-card style="margin-top: 20px">
      <div style="width: 100%">
        <div style="float: left;">
          <p style=" font-weight:bold;color: #00bfff">
            其他报销</p>
        </div>
        <div style="margin-right: 20px;float: right">
          <p style=" font-weight:bold;color: #00bfff;display:inline-block;">当前页总计:</p>
          <p style="font-weight: bold;color: red;display:inline-block;">¥{{qtzj}}</p>

        </div>
      </div>
      <el-table :data="qtlist" border style="margin-top: 20px;"
                :header-cell-style="{'text-align':'center'}"
                :cell-style="{'text-align':'center'}">
        <el-table-column prop="pj_name" label="出差项目"></el-table-column>
        <el-table-column prop="cause" label="出差说明"></el-table-column>
        <el-table-column prop="date" label="发生日期"></el-table-column>
        <el-table-column label="报销金额" prop="money"></el-table-column>
        <el-table-column prop="user" label="报销人"></el-table-column>
        <el-table-column label="编辑">
          <template slot-scope="scope">
            <!--修改按钮-->
            <el-tooltip class="item" effect="dark" content="修改按钮" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="qtctdk(scope.row)"></el-button>
            </el-tooltip>
            <!--删除按钮-->
            <el-tooltip class="item" effect="dark" content="删除按钮" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="qtshanchu(scope.row.id)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!--分页区域-->
      <div class="block">
        <el-pagination
          @size-change="qthandleSizeChange"
          @current-change="qthandleCurrentChange"
          :current-page="qtInfo.page"
          :page-sizes="[5, 10, 50, 100]"
          :page-size="qtInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="qtdata.count">
        </el-pagination>
      </div>
    </el-card>
    <!--            抽屉弹框区-->
      <el-drawer :visible.sync="drawer"
               title="报销单"
               @close="ctgb('ctForm')"
    >
      <el-form label-width="80px" :model="ctForm" :rules="rules" ref="ctForm">
        <el-form-item label="出差项目" prop="project_name">
          <el-col :span="22">
            <el-select @click.native="getusername()" v-model="ctForm.project_name" clearable placeholder="选择项目" filterable
                       style="width: 100%;">
              <el-option v-for="item in userlist.results" :value="item.id" :label="item.project_name"></el-option>
            </el-select>
          </el-col>
        </el-form-item>
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
        <el-form-item label="出差时间" required label-width="80px">
          <el-col :span="11">
            <el-form-item prop="start_date">
              <el-date-picker type="date" placeholder="开始日期" v-model="ctForm.start_date" style="width: 100%;"
                              format="yyyy年MM月dd月" value-format="yyyy-MM-dd"></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="1">
            <span style="font-size: 16px">-</span>
          </el-col>
          <el-col :span="10">
            <el-form-item prop="end_date">
              <el-date-picker type="date" placeholder="结束日期" v-model="ctForm.end_date" style="width: 100%;"
                              format="yyyy年MM月dd月" value-format="yyyy-MM-dd"></el-date-picker>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item prop="sumDate" label="总天数">
          <el-col :span="11">
            <el-input-number @change="handleChange" :min="1" :max="30" v-model="ctForm.sumDate"
                             style="width: 100%"></el-input-number>

          </el-col>
          <el-col :span="11">
            <el-form-item prop="sumButie" label="总补贴">
              <el-input v-model="ctForm.sumButie" type="number">
              </el-input>
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item label="交通方式" prop="Type_traffic">
          <el-col :span="22 ">
            <el-select @click.native="getjtfs()" v-model="ctForm.Type_traffic" placeholder="选择交通方式" filterable
                       style="width: 100%">
              <el-option v-for="item in jtfslist" :value="item.id" :label="item.project_name"></el-option>
            </el-select>
          </el-col>
        </el-form-item>
        <el-col :span="11">
          <el-form-item prop="money_traffic" label="交通费">
            <el-input v-model="ctForm.money_traffic"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="zhushu" label="住宿费">
            <el-input v-model="ctForm.zhushu"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="22">
          <el-form-item prop="explain" label="项目说明">
            <el-input type="textarea" :rows="2" placeholder="请输入内容"
                      style="width: 100%" v-model="ctForm.explain"></el-input>
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
      <el-col>
        <el-form-item>
          <el-button type="primary" @click="cttjForm()">提交报销</el-button>
          <el-button @click="reset('ctForm')">重置</el-button>
        </el-form-item>
      </el-col>
      </el-form>
    </el-drawer>
    <!--            其他抽屉弹框区-->
    <el-drawer :visible.sync="qtdrawer"
               title="报销单"
               @close="ctgb('qtctForm')"
    >
      <el-form label-width="80px" :model="qtctForm" :rules="qtrules" ref="qtctForm">
        <el-form-item label="出差项目" prop="project_name">
          <el-col :span="22">
            <el-select @click.native="getusername()" v-model="qtctForm.project_name" clearable placeholder="选择项目" filterable
                       style="width: 100%;">
              <el-option v-for="item in userlist.results" :value="item.id" :label="item.project_name"></el-option>
            </el-select>
          </el-col>
        </el-form-item>
        <el-form-item prop="money" label="报销金额">
          <el-col :span="22">
            <el-input placeholder="请输入内容" style="width: 100%" v-model="qtctForm.money"></el-input>
          </el-col>
        </el-form-item>
        <el-col :span="22">
          <el-form-item prop="cause" label="项目说明">
            <el-input type="textarea" :rows="2" placeholder="请输入内容"
                      style="width: 100%" v-model="qtctForm.cause"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="22">
          <el-form-item prop="date" label="发生日期">
            <el-date-picker type="date" placeholder="发生日期" v-model="qtctForm.date" style="width: 100%;"
                            format="yyyy年MM月dd月" value-format="yyyy-MM-dd"></el-date-picker>
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
        <el-col>
          <el-form-item>
            <el-button type="primary" @click="qttjForm()">提交报销</el-button>
            <el-button @click="reset('qtctForm')">重置</el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-drawer>
  </div>


</template>

<script>
  export default {
    name: 'reimbursement',
    data () {
      return {
        activeName: 'first',
        num: 1,
        projectlist: [],
        restdata: {},
        qtdata:{},
        userlist: '',
        jtfslist: '',
        qtlist:[],
        zj:0,
        qtzj:0,
        drawer: false,
        qtdrawer: false,
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
          id:'',
          account_date:'',
        },
        qtctForm:{
          money:'',
          cause:'',
          date:'',
          project_name: '',
          pj_name:'',
          project_id:'',
          account_date:'',
        },
        qtrules:{
          money: [
            {
              required: true,
              message: '请输入报销金额',
              trigger: 'blur'
            },
            ],
          cause: [
            {
              required: true,
              message: '请输入项目说明',
              trigger: 'blur'
            },
          ],
          date: [
            {
              required: true,
              message: '请输入发生日期',
              trigger: 'blur'
            },
          ],
        },
        queryInfo: {
          query: '',
          page: 1,
          size: 50,
          expense_name: '',
          finish_flag: '',
        },
        qtInfo: {
          query: '',
          page: 1,
          size: 50,
          expense_name: '',
          finish_flag: '',
        },
        fbxForm:{
          money:'',
          cause:'',
          date:'',
          project_name: '',
          project_id:'',
        },
        ruleForm: {
          start_date: '',
          end_date: '',
          start_addr: '',
          end_addr: '',
          money_traffic: '',
          zhushu: '',
          sumButie: 50,
          sumDate: 1,
          explain: '',
          project_name: null,
          Type_traffic: null,

        },
        rules: {
          zhushu: [
            {
              required: true,
              message: '请输入住宿金额',
              trigger: 'blur'
            },
          ],
          start_addr: [
            {
              required: true,
              message: '请输入出发地点',
              trigger: 'blur'
            },
          ],
          end_addr: [
            {
              required: true,
              message: '请输入目的地点',
              trigger: 'blur'
            },
          ],
          start_date: [
            {
              type: 'string',
              required: true,
              message: '请选择日期',
              trigger: 'change'
            }
          ],
          end_date: [
            {
              type: 'string',
              required: true,
              message: '请选择日期',
              trigger: 'change'
            }
          ],
          money_traffic: [
            {
              required: true,
              message: '请填写交通费',
              trigger: 'blur'
            }
          ],
          sumButie: [
            {
              required: true,
              message: '请填写总补贴',
              trigger: 'change'
            }
          ],
          sumDate: [
            {
              required: true,
              message: '请选择总天数',
              trigger: 'change'
            }
          ],
          explain: [
            {
              required: true,
              message: '请填写项目说明',
              trigger: 'blur'
            }
          ],
          project_name: [
            {
              required: true,
              message: '请选择项目名称',
              trigger: 'change'
            }
          ],
          Type_traffic: [
            {
              required: true,
              message: '请选择交通方式',
              trigger: 'change'
            }
          ],
        },

      }
    },
    created () {
      this.getprojectlist()
      this.getqtlist()
    },

    methods: {
      //关闭ct清空数据
      ctgb (formName) {
        this.$refs[formName].resetFields()
        this.getprojectlist()
        this.getqtlist()
      },
      // 获取报销信息
      async getprojectlist () {
        this.queryInfo.expense_name = window.sessionStorage.getItem('id')
        this.queryInfo.finish_flag = 0
        // console.log(this.queryInfo)
        const { data: res } = await this.$http.get('Account_projects/', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.projectlist = res.results
        this.zj = 0
        for (let item in res.results) {
          this.zj += res.results[item].zhushu + res.results[item].money_traffic + res.results[item].sumButie;
        }
      },
      // 获取其他报销信息
      async getqtlist () {
        this.qtInfo.expense_name = window.sessionStorage.getItem('id')
        this.qtInfo.finish_flag = 0
        // console.log(this.queryInfo)
        const { data: res } = await this.$http.get('Account_normals/', {
          params: this.qtInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.qtdata = res
        this.qtlist = res.results
        this.qtzj = 0
        for (let item in res.results) {
          this.qtzj += +res.results[item].money;
        }
        // console.log(res)
      },
      // 监听pagesize改变事件
      handleSizeChange (newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.queryInfo.size = newSize
        this.getprojectlist()
      },
      // // 监听页码改变
      handleCurrentChange (newPage) {
        // console.log(`当前页: ${newPage}`)
        this.queryInfo.page = newPage
        this.getprojectlist()
      },
      // 监听pagesize改变事件
      qthandleSizeChange (newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.qtInfo.size = newSize
        this.getqtlist()
      },
      // // 监听页码改变
      qthandleCurrentChange (newPage) {
        // console.log(`当前页: ${newPage}`)
        this.qtInfo.page = newPage
        this.getqtlist()
      },
      // 页面选择器
      handleClick (tab, event) {
        // console.log(tab, event);
      },
      // 计数器
      handleChange (value) {
        // console.log(value);
        this.ruleForm.sumButie = value * 50
        this.ctForm.sumButie = value * 50
      },
      // 重置按钮
      reset (formName) {
        this.$refs[formName].resetFields()
      },
      // 获取交通方式
      getjtfs () {
        let _this = this
        this.$http.get('traffictypes/')
          .then(res => {
            _this.jtfslist = res.data
            // console.log(res)
          }).catch((error) => {
          console.log(error)
        })
      },
      // 获取项目信息
      getusername () {
        let _this = this
        this.$http.get('projects/')
          .then(res => {
            _this.userlist = res.data
            // console.log(res)

          }).catch((error) => {
          console.log(error)
        })
      },
      // 提交报销单
      submitForm () {
        this.$refs.ruleForm.validate(
          async valid => {
            if (!valid) return
            //提交请求
            try {
              const { status: res } = await this.$http.post('Account_projects/', this.ruleForm)
              if (res === 201) {
                this.$message.success('提交成功！')
              }

            } catch (err) {
              this.$message.error('提交失败！' + err.toString())
            }
            this.getprojectlist()
          }
        )
      },
      // 打开抽屉获取数据
      ctdk (row) {
        this.drawer = true
        //console.log(row)
        this.ctForm = row
        this.getjtfs()
        this.getusername()
        // console.log(this.projectlist)
        // const abc = await this.$http.get('Account_projects/${row.id}/')
        // console.log(abc)
      },
      async shanchu (id) {
        // console.log(id)
        //  询问用户是否删除
        const confirmResult = await this.$confirm('此操作将永久删除该报销, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).catch(err => err)
        if (confirmResult !== 'confirm') {
          return this.$message.info('已取消删除')
        }
        try {
          const { status: res } = await this.$http.delete(`/Account_projects/${id}/`)
          if (res === 204) {
            this.$message.success('删除成功！')
            this.getprojectlist()
          }
        } catch (err) {
          this.$message.error('删除失败！' + err.toString())
        }
      },
      // 抽屉提交数据
      cttjForm(){
        this.$refs.ctForm.validate(
          async valid => {
            if (!valid) return
            //提交请求
            try {
              const { status: res } = await this.$http.put(`/Account_projects/${this.ctForm.id}/`, this.ctForm)
              if (res === 200) {
                this.$message.success('提交成功！')
              }

            } catch (err) {
              this.$message.error('提交失败！' + err.toString())
            }
            this.drawer = false
            this.getprojectlist()
          }
        )
      },
      // 其他报销提交
      fbxtjForm(){
        this.$refs.fbxForm.validate(
          async valid => {
            if (!valid) return
            //提交请求
            try {
              const { status: res } = await this.$http.post('Account_normals/', this.fbxForm)
              if (res === 201) {
                this.$message.success('提交成功！')
              }

            } catch (err) {
              this.$message.error('提交失败！' + err.toString())
            }
            this.getqtlist()
          }
        )
      },
      // 打开其他抽屉获取数据
      qtctdk (row) {
        this.qtdrawer = true
        //console.log(row)
        this.qtctForm = row
        this.getusername()
        // console.log(this.projectlist)
        // const abc = await this.$http.get('Account_projects/${row.id}/')
        // console.log(abc)
      },
      async qtshanchu (id) {
        // console.log(id)
        //  询问用户是否删除
        const confirmResult = await this.$confirm('此操作将永久删除该报销, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).catch(err => err)
        if (confirmResult !== 'confirm') {
          return this.$message.info('已取消删除')
        }
        try {
          const { status: res } = await this.$http.delete(`/Account_normals/${id}/`)
          if (res === 204) {
            this.$message.success('删除成功！')
            this.getqtlist()
          }
        } catch (err) {
          this.$message.error('删除失败！' + err.toString())
        }
      },
      // 其他抽屉提交数据
      qttjForm(){
        this.$refs.qtctForm.validate(
          async valid => {
            if (!valid) return
            //提交请求
            try {
              const { status: res } = await this.$http.put(`/Account_normals/${this.qtctForm.id}/`, this.qtctForm)
              if (res === 200) {
                this.$message.success('提交成功！')
              }

            } catch (err) {
              this.$message.error('提交失败！' + err.toString())
            }
            this.qtdrawer = false
            this.getqtlist()
          }
        )
      },
    }
  }

</script>

<style scoped>

</style>
