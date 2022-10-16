<template>
  <div>
    <!--&lt;!&ndash;面包屑导航区&ndash;&gt;-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>合同管理</el-breadcrumb-item>
      <el-breadcrumb-item>综合查询</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <!--头部综合查询区-->
      <el-row gutter="20">
        <el-col :span="8">
          <el-input placeholder="可查询合同名称、备注等关键字" v-model="queryInfo.query" clearable>
            <el-button slot="append" icon="el-icon-search" clearable></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-date-picker
            v-model="searchyear"
            type="year"
            placeholder="合同签订年份">
          </el-date-picker>
        </el-col>
        <el-col :span="6">
          <el-select @click.native="getxmname()" v-model="project_name" clearable placeholder="选择项目" filterable
                     style="width: 100%;" @change="xmchange">
            <el-option v-for="item in projectlist.results" :value="item.id" :label="item.project_name"></el-option>
          </el-select>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: 'caigouhetong',
    data () {
      return {
        // 获取用户列表的参数对象
        queryInfo: {
          query: '',
          page: 1,
          size: 50,
        },
        project_name: '',
        projectlist: '',
      }
    },
    created () {
    },
    methods: {
      // 获取项目信息
      getxmname () {
        let _this = this
        this.$http.get('projects/')
          .then(res => {
            _this.projectlist = res.data
            // console.log(res)

          }).catch((error) => {
          console.log(error)
        })
      },
      //选择项目后查询
      async xmchange (row) {
        this.queryInfo.project_name = project_name
        const { data: res } = await this.$http.get('/Contract_infos/', {
          params: this.queryInfo
        }).catch((error) => {
          this.$message.error(error)
        })
        this.restdata = res
        this.baoxiaolist = res.results
      }
    }
  }
</script>

<style scoped>

</style>
