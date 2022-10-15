<template>
  <div>
    <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>合同管理</el-breadcrumb-item>
      <el-breadcrumb-item>项目合同</el-breadcrumb-item>
    </el-breadcrumb>
    <!--    头部查询与新增合同-->
    <el-card>
      <!--搜索与添加区域-->
      <el-row :gutter="20">
        <el-col :span="9">
          <el-input placeholder="可查询合同名称、备注等关键字" v-model="queryInfo.query" clearable>
            <el-button slot="append" icon="el-icon-search" @click="getxmList"></el-button>
          </el-input>
        </el-col>
        <el-col :span="2  ">
          <el-button type="primary" @click="dialogVisible = true" icon="el-icon-circle-plus-outline">
            添加合同
          </el-button>
        </el-col>
      </el-row>

    </el-card>
    <!--    综合查询区-可收缩-->
    <el-card :body-style="{ padding: '0px' }">
      <!--头部综合查询区-->
      <el-collapse-transition>
        <div v-show="show3" style="padding: 20px">
          <el-row :gutter="20">
            <el-col :span="4">
              <el-date-picker
                v-model="searchyear"
                value-format="yyyy-MM-dd"
                type="year"
                placeholder="合同签订年份" @change="xmchange">
              </el-date-picker>
            </el-col>
            <el-col :span="6">
              <el-select @click.native="getxm()" v-model="project_name" clearable placeholder="选择项目" filterable
                         style="width: 100%;" @change="xmchange">
                <el-option v-for="item in projectlist.results" :value="item.id" :label="item.project_name"></el-option>
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select v-model="htType" placeholder="选择合同类型" clearable  @change="xmchange">
                <el-option value=1 label="收款合同"></el-option>
                <el-option value=2 label="付款合同"></el-option>
              </el-select>
            </el-col>
          </el-row>
        </div>
      </el-collapse-transition>
      <!--      点击条-->
      <div class="header"
           ref="refheader"
           @mouseover="mouseOver"
           @mouseleave="mouseLeave"
           @click="show3 = !show3;isActive=!isActive">
        <transition name="el-fade-in-linear">
          <div v-show="textShow" v-text="isActive?'展开查询项':'收缩查询项'"></div>
        </transition>
        <transition name="el-fade-in-linear">
          <i style="font-size:large;" :class="isActive?'el-icon-caret-bottom':'el-icon-caret-top'"></i>
        </transition>


      </div>
    </el-card>
    <!--    合同列表区-->
    <el-card>
      <!--用户列表区-->
      <el-table :data="xmlist" border style="margin-top: 20px;"
                :header-cell-style="{'text-align':'center'}"
                :cell-style="{'text-align':'center'}"
                @row-click="ctdk"
      >
        <el-table-column width="140px" prop="contract_type" label="合同类型">
          <template slot-scope="scope">
            <el-tag :type="scope.row.contract_type===2 ? 'success' : 'danger'">
              {{level[scope.row.contract_type]}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="contract_name" label="合同名称"></el-table-column>
        <el-table-column prop="project_name" label="项目名称"></el-table-column>
        <el-table-column prop="Date_start" label="签订日期"></el-table-column>
        <el-table-column prop="Date_end" label="到期日期"></el-table-column>
        <el-table-column prop="amount" label="合同金额"></el-table-column>
        <el-table-column prop="zj_percent" label="资金计划">
          <template slot-scope="scope">
            <el-progress :percentage="scope.row.zj_percent" :color="customColorMethod"></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="fp_percent" label="发票计划">
          <template slot-scope="scope">
            <el-progress :percentage="scope.row.fp_percent" :color="customColorMethod"></el-progress>
          </template>
        </el-table-column>

      </el-table>
      <!--      分页区域-->
      <div class="block">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.page"
          :page-sizes="[5,10,50]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="restdata.count">
        </el-pagination>
      </div>
    </el-card>
    <!--添加合同对话框-->
    <el-dialog
      title="添加合同"
      :visible.sync="dialogVisible"
      width="50%" @close="closeDialog('xmForm')"
    >
      <!--内容主题区域-->
      <el-form :model="xmForm" :rules="xmFormRules" ref="xmForm" label-width="80px" style="text-align: left;">
        <el-form-item label="合同类型" prop="contract_type">
          <el-select v-model="xmForm.contract_type" clearable placeholder="请选择" style="width: 100%">
            <el-option label="收款合同" value=1></el-option>
            <el-option label="付款合同" value=2></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称" prop="project">
          <el-select @click.native="getxmname()" v-model="xmForm.project" clearable placeholder="选择项目" filterable
                     style="width: 100%;">
            <el-option v-for="item in xmmclist" :value="item.id" :label="item.project_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="合同名称" prop="contract_name">
          <el-input v-model="xmForm.contract_name"></el-input>
        </el-form-item>
        <el-form-item label="合同金额" prop="amount">
          <el-input v-model="xmForm.amount"></el-input>
        </el-form-item>
        <el-form-item label="合同本方" prop="body">
          <el-select @click.native="gethtname()" v-model="xmForm.body" clearable placeholder="选择合同本方" filterable
                     style="width: 100%;">
            <el-option v-for="item in htdxlist" :value="item.id" :label="item.entity_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="合同对方" prop="target">
          <el-select @click.native="gethtname()" v-model="xmForm.target" clearable placeholder="选择合同对方" filterable
                     style="width: 100%;">
            <el-option v-for="item in htdxlist" :value="item.id" :label="item.entity_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="签订日期" prop="Date_start">
          <el-date-picker
            v-model="xmForm.Date_start"
            type="date"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            placeholder="选择日期"
            style="width: 100%">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="到期日期" prop="Date_end">
          <el-date-picker
            v-model="xmForm.Date_end"
            type="date"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            placeholder="选择日期"
            style="width: 100%">
          </el-date-picker>
        </el-form-item>

        <el-form-item label="税金成本" prop="taxes">
          <el-input v-model="xmForm.taxes"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="explain">
          <el-input type="textarea" :rows="2" placeholder="请输入内容"
                    style="width: 100%" v-model="xmForm.explain"></el-input>
        </el-form-item>
      </el-form>
      <!--底部区域-->
      <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="adduser">确 定</el-button>
  </span>
    </el-dialog>
    <el-drawer :visible.sync="drawer"
               title="项目合同"
               @close="ctgb('xmctForm')"
               size="50%"
    >
      <el-form label-width="80px" :model="xmctForm" ref="xmctForm">
        <el-form-item label="合同类型" prop="contract_type" style="margin-right: 30px;margin-left: 30px;">
          <el-select v-model="xmctForm.contract_type" clearable placeholder="请选择" style="width: 100%;" filterable>
            <!--            <el-option v-for="(value,key,index) in this.level" :value="key" :label="value"></el-option>-->
            <el-option label="收款合同" value=1></el-option>
            <el-option label="付款合同" value=2></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称" prop="project" style="margin-right: 30px;margin-left: 30px;">
          <el-select @click.native="getxmname()" v-model="xmctForm.project" clearable placeholder="选择项目" filterable
                     style="width: 100%;">
            <el-option v-for="item in xmmclist" :value="item.id" :label="item.project_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="合同名称" prop="contract_name" style="margin-right: 30px;margin-left: 30px;">
          <el-input v-model="xmctForm.contract_name"></el-input>
        </el-form-item>
        <el-form-item label="合同金额" prop="amount" style="margin-right: 30px;margin-left: 30px;">
          <el-input v-model="xmctForm.amount"></el-input>
        </el-form-item>
        <el-form-item label="合同本方" prop="body" style="margin-right: 30px;margin-left: 30px;">
          <el-select @click.native="gethtname()" v-model="xmctForm.body" clearable placeholder="选择合同本方" filterable
                     style="width: 100%;">
            <el-option v-for="item in htdxlist" :value="item.id" :label="item.entity_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="合同对方" prop="target" style="margin-right: 30px;margin-left: 30px;">
          <el-select @click.native="gethtname()" v-model="xmctForm.target" clearable placeholder="选择合同对方" filterable
                     style="width: 100%;">
            <el-option v-for="item in htdxlist" :value="item.id" :label="item.entity_name"></el-option>
          </el-select>
        </el-form-item>
        <el-row style="margin-right: 30px;margin-left: 30px;">
          <el-col :span="11">
            <el-form-item label="签订日期" prop="Date_start">
              <el-date-picker
                v-model="xmctForm.Date_start"
                type="date"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                style="width: 100%">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="到期日期" prop="Date_end">
              <el-date-picker
                v-model="xmctForm.Date_end"
                type="date"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                style="width: 100%">
              </el-date-picker>
            </el-form-item>
          </el-col>

        </el-row>


        <el-form-item label="税金成本" prop="taxes" style="margin-right: 30px;margin-left: 30px;">
          <el-input v-model="xmctForm.taxes"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="explain" style="margin-right: 30px;margin-left: 30px;">
          <el-input type="textarea" :rows="2" placeholder="请输入内容"
                    style="width: 100%" v-model="xmctForm.explain"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="xiugai">提交</el-button>
      <el-button type="danger" @click="shanchu">删 除</el-button>
      <!--      表单下部区-->
      <div>
        <!--        发票计划区-->
        <el-divider style="margin-top: 20px;margin-bottom: 20px;"></el-divider>

        <el-row type="flex" align="middle" style="margin-left: 20px;">
          <el-col :span="3" style="text-align: left">
            <el-button size="small" type="success" @click="fpVisible=true">发票计划</el-button>
          </el-col>
          <el-col :span="3" style="text-align: right;"><label style="font-size: small">发票进度：</label></el-col>
          <el-col :span="16">
            <el-progress :percentage="fppercent" :color="customColorMethod"></el-progress>
          </el-col>
        </el-row>
        <!--        发票计划-->
        <el-table :data="fplist" border style="margin-top: 20px;"
                  size="mini"
                  :header-cell-style="{'text-align':'center'}"
                  :cell-style="{'text-align':'center'}"
        >
          <el-table-column prop="finish_type" label="完成情况">
            <template slot-scope="scope">
              <el-tag :type="(scope.row.finish_type)?'success':'info'">
                {{scope.row.finish_type?'已完成':'未完成'}}
              </el-tag>
              <el-tooltip class="item" effect="dark" content="状态切换" placement="right" :enterable="false">
                <el-popconfirm title="你确定要更改状态吗？" @onConfirm="changeContractPlanFinishType(scope.row)">
                  <el-switch
                    style="margin-left: 8px"
                    v-model="scope.row.finish_type"
                    :active-value="1"
                    :inactive-value="0"
                    slot="reference"
                    @change="contartplan_finish_type_change(scope.row)"
                  >
                  </el-switch>
                </el-popconfirm>

              </el-tooltip>
              <!--              <el-switch v-model="scope.row.finish_type"></el-switch>-->
            </template>
          </el-table-column>
          <el-table-column label="计划日期">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{ scope.row.date_plan }}</span>
            </template>
          </el-table-column>
          <el-table-column label="百分比">
            <template slot-scope="scope">
              <p>{{scope.row.money_plan/xmctForm.amount*100}}%</p>
            </template>
          </el-table-column>
          <el-table-column prop="money_plan" label="金额"></el-table-column>

          <el-table-column label="删除 ">
            <template slot-scope="scope">
              <el-popconfirm title="你确定要删除吗？" @onConfirm="delete_contract_plan(scope.row.id)">
                <el-button slot="reference" type="danger" size="mini">删除</el-button>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <!--        资金计划区-->
        <el-divider style="margin-top: 20px;margin-bottom: 20px;"></el-divider>

        <el-row type="flex" align="middle" style="margin-left: 20px;">
          <el-col :span="3" style="text-align: left">
            <el-button size="small" type="success" @click="zjVisible=true">资金计划</el-button>
          </el-col>
          <el-col :span="3" style="text-align: right;"><label style="font-size: small">资金进度：</label></el-col>
          <el-col :span="16">
            <el-progress :percentage="zjpercent" :color="customColorMethod"></el-progress>
          </el-col>
        </el-row>
        <!--        资金计划-->
        <el-table :data="zjlist" border style="margin-top: 20px;"
                  size="mini"
                  :header-cell-style="{'text-align':'center'}"
                  :cell-style="{'text-align':'center'}"
        >
          <el-table-column prop="finish_type" label="完成情况">
            <template slot-scope="scope">
              <el-tag :type="(scope.row.finish_type)?'success':'info'">
                {{scope.row.finish_type?'已完成':'未完成'}}
              </el-tag>
              <el-tooltip class="item" effect="dark" content="状态切换" placement="right" :enterable="false">
                <el-popconfirm title="你确定要更改状态吗？" @onConfirm="changeContractPlanFinishType(scope.row)">
                  <el-switch
                    style="margin-left: 8px"
                    v-model="scope.row.finish_type"
                    :active-value="1"
                    :inactive-value="0"
                    slot="reference"
                    @change="contartplan_finish_type_change(scope.row)"
                  >
                  </el-switch>
                </el-popconfirm>

              </el-tooltip>
              <!--              <el-switch v-model="scope.row.finish_type"></el-switch>-->
            </template>
          </el-table-column>
          <el-table-column label="计划日期">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{ scope.row.date_plan }}</span>
            </template>
          </el-table-column>
          <el-table-column label="百分比">
            <template slot-scope="scope">
              <p>{{scope.row.money_plan/xmctForm.amount*100}}%</p>
            </template>
          </el-table-column>
          <el-table-column prop="money_plan" label="金额"></el-table-column>

          <el-table-column label="删除 ">
            <template slot-scope="scope">
              <el-popconfirm title="你确定要删除吗？" @onConfirm="delete_contract_plan(scope.row.id)">
                <el-button slot="reference" type="danger" size="mini">删除</el-button>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <!--        附件区-->
        <el-divider style="margin-top: 20px;margin-bottom: 20px;"></el-divider>
        <el-upload
          :headers="headers"
          action="/api/attachments/"
          :on-preview="handlePreview"
          :on-error="onError"
          :on-success="onSuccess"
          :before-upload="onBeforeUpload"
          :data="htfj"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          :on-exceed="handleExceed"
          multiple

          :file-list="fileList"
          style="float: left;margin-left: 20px;text-align: left">
          <el-button size="small" type="success">上传附件</el-button>

          <div slot="tip" class="el-upload__tip">上传合同文件及其他必要文件</div>

        </el-upload>


      </div>

    </el-drawer>

    <el-dialog
      title="新增发票计划"
      :visible.sync="fpVisible"
      width="40%"
      @close="fpgb('fpForm')"
    >
      <el-row>
        <el-col>
          <span style="float: left;color: darkgray;margin-bottom: 20px;"><i class="el-icon-warning-outline"></i>：输入发票金额或者占总金额的百分比，点击生成即可。<span
            style="color: blue">合同金额：¥{{xmctForm.amount}}元</span></span>
        </el-col>

      </el-row>

      <el-form :model="fpForm" ref="fpForm" style="text-align: center;">
        <el-row>
          <el-col :span="8">
            <el-form-item label="计划日期:" prop="Date" style="vertical-align: middle;">
              <el-date-picker
                v-model="fpForm.Date"
                type="date"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                style="width: 60%"
                size="small">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="5" style="text-align: left">
            <el-form-item prop="money">
              <el-input :disabled="sw" v-model="fpForm.money" size="small"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="1">
            <div style="height: 40.5px;vertical-align: middle;display:table-cell;padding-left: 5px;">
              <el-switch
                v-model="sw"
                active-color="#13ce66"
                inactive-color="#ff4949">
              </el-switch>
            </div>

          </el-col>
          <el-col :span="4">
            <el-form-item prop="jd">
              <el-input :disabled="!sw" v-model="fpForm.jd" style="width: 60px" size="small"></el-input>
              <span>%</span>
            </el-form-item>
          </el-col>

          <el-col :span="3">
            <div style="height: 40.5px;vertical-align: middle;display:table-cell;">
              <el-button type="success" @click="scjh" size="small" style="vertical-align: middle;"> 生成</el-button>
            </div>

          </el-col>
        </el-row>
      </el-form>
      <span style="font-size: 18px;">计划内容：合同金额：<el-tag style="font-size: 18px;">{{jd}}%</el-tag> ，金额：<el-tag
        style="font-size: 18px;">{{je}}元</el-tag>，计划日期：{{rq}}</span>
      <span slot="footer" class="dialog-footer">
    <el-button @click="fpVisible = false">取 消</el-button>
    <el-button type="primary" @click="fpjh">提 交</el-button>
  </span>
    </el-dialog>
    <!--    资金计划-->
    <el-dialog
      title="新增资金计划"
      :visible.sync="zjVisible"
      width="40%"
      @close="zjgb('zjForm')"
    >
      <el-row>
        <el-col>
          <span style="float: left;color: darkgray;margin-bottom: 20px;"><i class="el-icon-warning-outline"></i>：输入资金金额或者占总金额的百分比，点击生成即可。<span
            style="color: blue">合同金额：¥{{xmctForm.amount}}元</span></span>
        </el-col>

      </el-row>

      <el-form :model="zjForm" ref="zjForm" style="text-align: center;">
        <el-row>
          <el-col :span="8">
            <el-form-item label="计划日期:" prop="Date" style="vertical-align: middle;">
              <el-date-picker
                v-model="zjForm.Date"
                type="date"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                style="width: 60%"
                size="small">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="5" style="text-align: left">
            <el-form-item prop="money">
              <el-input :disabled="sw" v-model="zjForm.money" size="small"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="1">
            <div style="height: 40.5px;vertical-align: middle;display:table-cell;padding-left: 5px;">
              <el-switch
                v-model="sw"
                active-color="#13ce66"
                inactive-color="#ff4949">
              </el-switch>
            </div>

          </el-col>
          <el-col :span="4">
            <el-form-item prop="jd1">
              <el-input :disabled="!sw" v-model="zjForm.jd1" style="width: 60px" size="small"></el-input>
              <span>%</span>
            </el-form-item>
          </el-col>

          <el-col :span="3">
            <div style="height: 40.5px;vertical-align: middle;display:table-cell;">
              <el-button type="success" @click="scfp" size="small" style="vertical-align: middle;"> 生成</el-button>
            </div>

          </el-col>
        </el-row>
      </el-form>
      <span style="font-size: 18px;">计划内容：合同金额：<el-tag style="font-size: 18px;">{{jd1}}%</el-tag> ，金额：<el-tag
        style="font-size: 18px;">{{je1}}元</el-tag>，计划日期：{{rq1}}</span>
      <span slot="footer" class="dialog-footer">
    <el-button @click="zjVisible = false">取 消</el-button>
    <el-button type="primary" @click="zjjh">提 交</el-button>
  </span>
    </el-dialog>
  </div>

</template>

<script>
  import ElCollapseTransition from 'element-ui/lib/transitions/collapse-transition'

  export default {
    name: 'xiangmuhetong',
    components: { ElCollapseTransition },
    data () {
      return {
        searchyear: null,
        htType:null,
        project_name: '',
        projectlist: '',
        show3: false,
        sw: true,
        headers: {
          Authorization: window.sessionStorage.getItem('token')
        },

        queryInfo: {
          query: '',
          htType:'',
          page: 1,
          size: 10,
        },
        fppercent: 0,
        zjpercent: 0,
        fileList: [],
        dialogVisible: false,
        fpVisible: false,
        zjVisible: false,
        xmlist: [],
        fplist: [],
        zjlist: [],
        xmmclist: [],
        htdxlist: [],
        restdata: '',
        xmctForm: {},
        fpForm: {},
        zjForm: {},
        jd: 0,
        je: 0,
        rq: null,
        jd1: 0,
        je1: 0,
        rq1: null,
        htfj: { hetong: '' },
        drawer: false,
        level: {
          1: '收款合同',
          2: '付款合同'
        },
        xmForm: {
          contract_type: '',
          contract_name: '',
          project: '',
          amount: '',
          body: '',
          target: '',
          Date_start: '',
          Date_end: '',
          attchments: '',
          taxes: '',
          explain: '',
        },
        xmFormRules: {
          contract_type: [
            {
              required: true,
              message: '请选择合同类型',
              trigger: 'blur'
            }],
          contract_name: [
            {
              required: true,
              message: '请输入合同名称',
              trigger: 'blur'
            }],
          project: [
            {
              required: true,
              message: '请选择项目',
              trigger: 'blur'
            }],
          amount: [
            {
              required: true,
              message: '请输入合同金额',
              trigger: 'blur'
            }],
          body: [
            {
              required: true,
              message: '请选择合同本方',
              trigger: 'blur'
            }],
          target: [
            {
              required: true,
              message: '请选择合同对方',
              trigger: 'blur'
            }],
          Date_start: [
            {
              required: true,
              message: '请选择合同签订日期',
              trigger: 'blur'
            }],
          Date_end: [
            {
              required: true,
              message: '请选择合同到期日期',
              trigger: 'blur'
            }],
        },
        progress_status_zj: 'warning',
        progress_status_fp: 'warning',
        active: '',
        isActive: true,
        headerText: '展开查询项',
        textShow: false,
      }

    },
    created () {
      this.getxmList()
    },
    methods: {
      //获取项目列表
      async getxmList () {
        const { data: res } = await this.$http.get('/Contract_infos', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.xmlist = res.results

      },
      closeDialog (formName) {
        this.$refs[formName].resetFields()
        this.getxmList()
      },
      // 获取项目信息
      getxmname () {
        let _this = this
        this.$http.get('projectsall/')
          .then(res => {
            _this.xmmclist = res.data
          }).catch((error) => {
          console.log(error)
        })
      },
      // 获取合同对象信息
      gethtname () {
        let _this = this
        this.$http.get('entityall/')
          .then(res => {
            _this.htdxlist = res.data
          }).catch((error) => {
          console.log(error)
        })
      },
      //点击按钮添加新合同
      adduser () {
        function clone (myObj) {
          if (typeof (myObj) != 'object') {
            return myObj
          }
          if (myObj == null) {
            return myObj
          }
          if (myObj instanceof Array) {
            var myNewObj = new Array()
          } else {
            var myNewObj = new Object()
          }
          for (var i in myObj) {
            myNewObj[i] = clone(myObj[i])
          }
          return myNewObj
        }

        this.$refs.xmForm.validate(
          async valid => {
            if (!valid) return
            //添加用户请求
            try {
              var dataform = null
              if (this.xmForm.taxes === '') {
                dataform = clone(this.xmForm)
                delete dataform.taxes
                console.log(dataform)
              } else {
                console.log(dataform)
                dataform = clone(this.xmForm)
              }
              const { status: res } = await this.$http.post('/Contract_infos/', dataform)
              if (res === 201) {
                this.$message.success('添加成功！')
                this.dialogVisible = false
                this.getxmList()
              }

            } catch (err) {
              this.$message.error('添加失败！' + err.toString())
            }

          }
        )
      },
      // 监听pagesize改变事件
      handleSizeChange (newSize) {
        // console.log(`每页 ${newSize} 条`)
        this.queryInfo.size = newSize
        this.getxmList()
      },
      // // 监听页码改变
      handleCurrentChange (newPage) {
        // console.log(`当前页: ${newPage}`)
        this.queryInfo.page = newPage
        this.getxmList()
      },
      //点击行数据打开抽屉
      async ctdk (row) {
        // let thisRowData = this;
        // thisRowData = row;
        //如果是项目出差
        this.gethtname()
        this.getxmname()
        this.drawer = true
        // 下载合同数据
        const { data: res } = await this.$http.get(`/Contract_infos/${row.id}/`)
        this.xmctForm = res
        this.xmctForm.contract_type = this.xmctForm.contract_type.toString()
        //给合同附体清空数组
        this.fileList = []
        if (this.xmctForm.attchments != null) {
          //取表单获取附件内容值并按照upload的显示要求赋值
          for (var item in this.xmctForm.attchments) {
            this.fileList.push({
              id: this.xmctForm.attchments[item].id,
              name: this.xmctForm.attchments[item].filename,//显示文件名
              url: this.xmctForm.attchments[item].file,//下载地址
              hetong: this.xmctForm.attchments[item].hetong
            })
          }
        }
        console.log(res)
        //更新发票计划数据
        this.getfplist(this.xmctForm.id, 0)
        //更新资金计划数据
        this.getfplist(this.xmctForm.id, 1)

      },
      //关闭ct清空数据
      ctgb (formName) {
        this.$refs[formName].resetFields()
        this.getxmList()
      },
      //提交修改内容
      async xiugai () {
        this.$refs.xmctForm.validate(
          async valid => {
            if (!valid) return
            //修改用户请求
            try {
              const res = await this.$http.put(`/Contract_infos/${this.xmctForm.id}/`, this.xmctForm)
              console.log(res)
              if (res.status === 200) {
                this.$message.success('修改成功！')
                this.drawer = false
                this.getxmList()
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
        const confirmResult = await this.$confirm('此操作将永久删除该合同, 是否继续?', '提示', {
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
          const { status: res } = await this.$http.delete(`/Contract_infos/${this.xmctForm.id}/`)
          if (res === 204) {
            this.$message.success('删除成功！')
            this.drawer = false
            this.getxmList()
          }
        } catch (err) {
          this.$message.error('删除失败！' + err.toString())
        }
      },
      handleRemove (file, fileList) {
        console.log('执行了浏览器删除')
      },
      handlePreview (file) {
        console.log('点击打开文件')
        window.open(file.url)
      },
      handleExceed (files, fileList) {
        this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
      },
      beforeRemove (file, fileList) {
        this.$confirm(`确定移除 ${file.name}？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.fjcl(file, fileList)

          // return result
          // this.$http.delete(`/attachments/${file.id}/`).then(
          //   function (response) {
          //     if (response.status === 204) {
          //       console.log('123')
          //       this.$message.success('删除成功！')
          //       return true
          //     }
          //   }
          // ).catch(function (error) {
          //   this.$message.error('删除失败！' + error.toString())
          //   return false
          // })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
        return false

      },
      async fjcl (file, fileList) {
        try {
          const { status: res } = await this.$http.delete(`/attachments/${file.id}/`)
          if (res === 204) {
            this.$message.success('删除成功！')
            //找到被删除那个文件的数组位置
            const deleteIndex = fileList.filter(item => {
              return item.name === file.name
            })
            // // 再删除，`splice(开始下标， 删除元素数量)`可以删除，且会修改原数组
            fileList.splice(deleteIndex, 1)
          }
        } catch (err) {
          this.$message.error('删除失败！' + err.toString())
        }
      },
      onBeforeUpload (file) {
        this.htfj.hetong = this.xmctForm.id
        return true
      },
      onError (err, file, fileList) {
        this.$message.error(err)
      },
      onSuccess (reponse, file, fileList) {
        this.$message.success('上传成功')
        //刚上传的文件在fileList中的格式不对，需要重要整理
        const Index = fileList.indexOf(file)
        fileList[Index].id = file.response.id
        fileList[Index].url = file.response.file

      },
      scjh () {
        console.log(this.fpForm)
        //百分数可用
        if (this.sw) {
          this.je = this.xmctForm.amount * 0.01 * this.fpForm.jd
          this.jd = Math.floor(this.fpForm.jd*100)/100 //不四舍五入 ，向下取整
          this.rq = this.fpForm.Date
          // this.fpForm.money = this.je
        } else {//金额可用
          this.je = this.fpForm.money
          this.jd = this.fpForm.money / this.xmctForm.amount * 100
          this.rq = this.fpForm.Date
          // this.fpForm.jd = this.jd
        }

      },
      //关闭fp清空数据
      fpgb (formName) {
        this.$refs[formName].resetFields()
        this.je = null
        this.jd = null
        this.rq = null
      },
      isMoney (arg) {//22,111,22.11   判断是否是金额
        arg = arg.toString()
        var argChar = '0123456789.,'
        var beginArg = arg.substring(0, 1)
        if (beginArg === '.' || beginArg === ',') {
          return false
        }
        for (var i = 0; i < arg.length; i++) {
          if (argChar.indexOf(arg.substring(i, i + 1)) === -1) return false
          return true
        }
      },
      //获取计划数据
      async getfplist (contract_id, contract_type) {
        //先清空
        // this.fplist=null;
        // this.zjlist=null;
        //定义查询参数
        var paramsInfo = {
          contractinfo: contract_id,
          contract_type: contract_type
        }
        const { data: res } = await this.$http.get(`/Contract_plans/`, {
          params: paramsInfo
        }).catch((err) => {
          this.$message.error(err)
        })
        console.log('先看list')
        console.log(res)
        //如果请求的是发票计划
        if (contract_type === 0) {
          this.fplist = res
          //统计完成情况的百分比
          this.fppercent = 0
          for (var row in this.fplist) {
            if (this.fplist[row].finish_type === 1) {

              this.fppercent +=  Math.floor((this.fplist[row].money_plan / this.xmctForm.amount * 100)*100)/100
            }
          }
          console.log('看一下fplist')
          console.log(this.fplist)
        }
        //如果请求的是资金计划
        if (contract_type === 1) {
          this.zjlist = res
          this.zjpercent = 0
          for (var row in this.zjlist) {
            if (this.zjlist[row].finish_type === 1) {
              this.zjpercent += Math.floor((this.zjlist[row].money_plan / this.xmctForm.amount * 100)*100)/100
            }
          }
        }
      },
      async fpjh () {
        var je = parseFloat(this.je)
        if (!this.isMoney(je)) {//如果金额不是一个合法数字
          this.$message.error('没有生成正确的金额！')
          return
        }
        if (!this.rq) {
          this.$message.error('没有生成日期！')
          return
        }
        var fromdata1 = {
          contractinfo: this.xmctForm.id,
          date_plan: this.rq,
          money_plan: this.je,
          contract_type: 0,
          finish_type: 0,
        }

        try {
          const { status: res } = await this.$http.post('/Contract_plans/', fromdata1)
          if (res === 201) {
            this.$message.success('添加成功！')
            this.fpVisible = false
            this.getfplist(this.xmctForm.id, 0)
          }

        } catch (err) {
          this.$message.error('添加失败！' + err.toString())
        }
      },
      //关闭fp清空数据
      zjgb (formName) {
        this.$refs[formName].resetFields()
        this.je1 = null
        this.jd1 = null
        this.rq1 = null
      },
      scfp () {
        console.log(this.zjForm)
        //百分数可用
        if (this.sw) {
          this.je1 = this.xmctForm.amount * 0.01 * this.zjForm.jd1
          this.jd1 = this.zjForm.jd1
          this.rq1 = this.zjForm.Date
          // this.fpForm.money = this.je
        } else {//金额可用
          this.je1 = this.zjForm.money
          this.jd1 = this.zjForm.money / this.xmctForm.amount * 100
          this.rq1 = this.zjForm.Date
          // this.fpForm.jd = this.jd
        }

      },
      async zjjh () {
        var je1 = parseFloat(this.je1)
        if (!this.isMoney(je1)) {//如果金额不是一个合法数字
          this.$message.error('没有生成正确的金额！')
          return
        }
        if (!this.rq1) {
          this.$message.error('没有生成日期！')
          return
        }
        var fromdata2 = {
          contractinfo: this.xmctForm.id,
          date_plan: this.rq1,
          money_plan: this.je1,
          contract_type: 1,
          finish_type: 0,
        }

        try {
          const { status: res } = await this.$http.post('/Contract_plans/', fromdata2)
          if (res === 201) {
            this.$message.success('添加成功！')
            this.zjVisible = false
            this.getfplist(this.xmctForm.id, 1)
          }

        } catch (err) {
          this.$message.error('添加失败！' + err.toString())
        }
      },
      format (percentage) {
        if (percentage === 100) {
          this.$ref.el - progress - fp
          this.progress_status_fp = 'success'
        }
        return percentage === 100 ? '完成' : `${percentage}%`
      },
      customColorMethod (percentage) {
        if (percentage < 30) {
          return '#909399'
        } else if (percentage < 70) {
          return '#409eff'
        } else if (percentage >= 100) {
          return '#67c23a'
        }
      },

      async delete_contract_plan (id) {
        try {
          const { status: res } = await this.$http.delete(`/Contract_plans/${id}/`)
          if (res === 204) {
            this.$message.success('删除成功！')
            this.getfplist(this.xmctForm.id, 0)
            this.getfplist(this.xmctForm.id, 1)
          }
        } catch (err) {
          this.$message.error('删除失败！' + err.toString())
        }
      },
      //保持switch点击前的状态
      contartplan_finish_type_change (row) {
        console.log('点击后的状态是' + row.finish_type)
        let flag = row.finish_type //保存点击之后v-modeld的值(true，false)
        row.finish_type = row.finish_type === 1 ? 0 : 1//保持switch点击前的状态
        console.log('现在的状态是' + row.finish_type)
      },
      //真正修改合同计划的状态
      async changeContractPlanFinishType (row) {
        try {
          const { status: res } = await this.$http.patch(`/Contract_plans/${row.id}/`, { finish_type: ((row.finish_type === 1) ? 0 : 1) })
          if (res === 200) {
            this.getfplist(this.xmctForm.id, row.contract_type)
            this.$message.success('操作成功！')
          }
        } catch (err) {
          this.$message.error('操作失败！' + err.toString())
        }
      },
      //选择项目后查询
      async xmchange (type) {
        this.queryInfo.project = this.project_name
        this.queryInfo.contract_type = this.htType
        this.queryInfo.searchyear = this.searchyear
        const { data: res } = await this.$http.get('/Contract_infos/', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.xmlist = res.results
      },
      // 获取项目信息
      getxm () {
        let _this = this
        this.$http.get('projects/')
          .then(res => {
            _this.projectlist = res.data
            // console.log(res)

          }).catch((error) => {
          console.log(error)
        })
      },
      // 移入
      mouseOver () {
        // this.active = "background-color:black";
        // 操作dom 获取p标签改变其样式
        this.textShow = true
        var acps = this.$refs.refheader
        acps.style.color = '#409EFF'
        acps.style.background = '#F2F6FC'
      },
      // 移出
      mouseLeave () {
        // 操作dom 获取p标签改变其样式
        this.textShow = false
        var acps = this.$refs.refheader
        acps.style.color = ''
        acps.style.background = ''
      },
    },

  }
</script>

<style lang="less">
  .header {
    /*background-color: lightcoral;*/
    height: 40px;
    font-size: smaller;
    cursor: pointer;
    color: darkgray;
    /*text-align: center;*/
    /*flex 布局*/
    display: flex;
    /*实现垂直居中*/
    align-items: center;
    /*实现水平居中*/
    justify-content: center;

    text-align: justify;
  }

  .el-drawer.rtl {
    overflow: scroll;
  }
</style>
