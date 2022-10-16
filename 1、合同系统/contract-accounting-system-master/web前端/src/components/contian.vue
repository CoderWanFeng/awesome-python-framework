<template>
  <div>
    <!--面包屑导航区-->

    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item v-text="one"></el-breadcrumb-item>
      <el-breadcrumb-item>eeee</el-breadcrumb-item>
    </el-breadcrumb>

    <router-view></router-view>
  </div>

</template>

<script>
  export default {
    name: "contian",
    data() {
      return {
        // one : this.$parent.ruleForm.username,
        one: "2222",
        two: this.$parent.subItem.id,
      }
    }
  }
</script>

<style scoped>

</style>
