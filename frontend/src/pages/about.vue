<template>
    <div>
      <el-card shadow="always" class="show">
        <div style="justify-content: center; display: flex">
          <img style="width: 100%;" src="@/assets/bs.jpg"/>
        </div>
        <p>本项目是 2021-2022 秋冬学期《B/S 体系软件设计》的课程项目，旨在设计一个智能家居管理系统。用户在登录之后可以修改个人信息和创建场景、房间，添加设备、控制设备以及查看设备信息，设备包括灯、门锁、传感器和开关。网站界面对用户友好，样式适配手机移动端，可以在手机浏览器和微信等应用内置的浏览器中友好显示，同时也需要提供必要的软件项目文档，使自己了解并掌握一套 web 应用开发技术和开发的总体流程。</p>
      </el-card>
    </div>
  </template>

<script>
  export default {
    name: "aboutVue",
    data() {
      return {
      };
    },
    props: {},
    components: {
      //   ArrowRight
    },
  };
</script>

<style scoped>
    .show{
      margin-top: 5vh;
      text-align: left;
    }
</style>