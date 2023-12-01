<template>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">homepage</el-breadcrumb-item>
      <el-breadcrumb-item>promotion management</el-breadcrumb-item>
      <el-breadcrumb-item>promotion list</el-breadcrumb-item>
      <el-breadcrumb-item>promotion detail</el-breadcrumb-item>
    </el-breadcrumb>
</template>
  
<script>
  import { ArrowRight } from '@element-plus/icons-vue'
  export default {
    name: 'breadVue',
    data() {
      return {
        ArrowRight
      }
    },
    methods: {},
    props: {},
    components: {}
  }
</script>