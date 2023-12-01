<template>
    <div class="in">
        <el-card shadow="always" class="log" style="margin-top:15vh">
          <h1 v-if="hasLogIn && !isModify">个人信息</h1>
          <br/>
          <el-table v-if="hasLogIn && !isModify" :data="tableData" stripe style="width: 100%">
            <el-table-column prop="name" label="账号名" width="180" />
            <el-table-column prop="phone" label="电话号码" width="180" />
            <el-table-column prop="desc" label="个人简介" width="180" />
            <el-table-column prop="address" label="地址" />
          </el-table>
          <br />
          <el-button v-if="hasLogIn && !isModify" @click="toModify">修改密码</el-button>

<!--          修改密码-->
          <div v-if="isModify">
            <h1 >修改密码</h1>
            <el-row  style="margin-top:3vh">
              <el-col :span="6">账号</el-col>
              <el-col :span="12"><el-input v-model="accounts" placeholder="请输入账户名" clearable /></el-col>
            </el-row>
            <el-row  style="margin-top:3vh">
              <el-col :span="6">新密码</el-col>
              <el-col :span="12"><el-input
                  v-model="password"
                  type="password"
                  placeholder="请输入密码"
                  show-password
              />
              </el-col>
            </el-row >
            <el-row  style="margin-top:3vh">
              <el-col :span="6">确认密码</el-col>
              <el-col :span="12"><el-input
                  v-model="doubleConfirm"
                  type="password"
                  placeholder="请再次确认密码"
                  show-password
              />
              </el-col>
            </el-row >

            <el-row style="margin-top:3vh;margin-bottom: 3vh;">
              <el-col>
                <el-button type="primary" @click="modify">提交修改</el-button>
              </el-col>
            </el-row>
          </div>

<!--          注册、登录-->
          <div v-if="!hasLogIn">
            <h1 v-if="isLogIn">登录</h1>
            <h1 v-if="!isLogIn">注册</h1>
            <el-row  style="margin-top:3vh">
              <el-col :span="6">账号</el-col>
              <el-col :span="12">
                <el-input v-model="accounts" placeholder="请输入账户名" clearable />
              </el-col>
            </el-row>
            <el-row v-if="!isLogIn" style="margin-top:3vh">
              <el-col :span="6">电话</el-col>
              <el-col :span="12"><el-input v-model="phoneNumber" placeholder="请输入电话号码" clearable /></el-col>
            </el-row>
            <el-row  style="margin-top:3vh">
              <el-col :span="6">密码</el-col>
              <el-col :span="12"><el-input
                  v-model="password"
                  type="password"
                  placeholder="请输入密码"
                  show-password
              />
              </el-col>
            </el-row >
            <el-row style="margin-top:3vh;margin-bottom: 3vh;">
              <el-col :span="6">
              </el-col>
              <el-col v-if="isLogIn" :span="6">
                <el-button type="primary" @click="log">登录</el-button>
              </el-col>
              <el-col v-if="isLogIn" :span="6">
                <el-button type="success" @click="toReg">没有账号？先注册</el-button>
              </el-col>
              <el-col v-if="!isLogIn" :span="6">
                <el-button type="primary" @click="toLog">已有账号？去登录</el-button>
              </el-col>
              <el-col v-if="!isLogIn" :span="6">
                <el-button type="success" @click="reg">注册</el-button>
              </el-col>
            </el-row>
          </div>
          <el-dialog
              v-model="dialogVisible"
              title=""
              width="30%"
              :before-close="handleClose"
          >
            <span>{{state}}</span>
            <div>
              <el-button type="primary" @click="toHome" style="margin-top:30px">
                进入控制台
              </el-button>
              <el-button type="primary" @click="toAbout" style="margin-top:30px">
                看一眼 About
              </el-button>
            </div>
          </el-dialog>
        </el-card>
    </div>
</template>

<script>
    import { ref } from 'vue'
    import router from '@/router';
    import axios from "axios";
    import qs from "qs";
    import {ElMessage} from "element-plus";
  export default {
    name: "signVue",
    data() {
      return {
        accounts: "",
        phoneNumber: "",
        password: "",
        doubleConfirm: "",
        input: ref(''),
        dialogVisible: false,
        isLogIn: true,
        isModify: false,
        hasLogIn: sessionStorage.getItem('userState'),
        state: "",
        tableData: []
      };
    },
    methods: {
      log() {

        if (this.accounts === '') {
          ElMessage.error('请输入用户名');
        } else if (this.password === '') {
          ElMessage.error('请输入密码');
        } else {
          // 将accounts和password传入后端,传回是否正确
          axios.post('/api/accounts/signin', qs.stringify({'user': this.accounts, 'password': this.password}))
              .then(response => {
                if (response.data['state'] === 0) {
                  this.dialogVisible = true;
                  this.state = "登录成功，欢迎来到家居管理系统";
                  sessionStorage.setItem("userState", true);
                  sessionStorage.setItem("name", this.accounts);
                  sessionStorage.setItem("phone", response.data['phone']);
                  this.hasLogIn = true;
                } else if (response.data['state'] === 3) {
                  ElMessage.error("用户名不存在");
                } else {
                  ElMessage.error("密码错误");
                }
              })
              .catch(e => {
                console.log(e);
              })
        }
      },
      reg() {
        if (this.phoneNumber.length === 0) {
          ElMessage.error('请填写手机号');
        } else if (!(/^1[3456789]\d{9}$/.test(this.phoneNumber))) {
          ElMessage.error('手机号格式错误');
        } else if (this.password.length === 0) {
          ElMessage.error('请填写密码');
        } else if (this.password.length < 8) {
          ElMessage.error('密码少于 8 位');
        } else {
          axios.post('/api/accounts/signup', qs.stringify(
              {
                'user': this.accounts,
                'phone': this.phoneNumber,
                'password': this.password
              }
          )).then(response => {
            if (response.data['state'] === 2) {
              ElMessage.error('该用户名已经存在');
            } else if (response.data['state'] === 4) {
              ElMessage.error('该电话号码已经被注册');
            } else {
              ElMessage.success('注册成功');
              this.dialogVisible = true;
              this.state = "注册成功，欢迎来到家居管理系统";
              sessionStorage.setItem("userState", true);
              sessionStorage.setItem("name", this.accounts);
              sessionStorage.setItem("phone", this.phoneNumber);
              this.hasLogIn = true;
            }
          })
        }
      },
      modify() {
        if (sessionStorage.getItem('name') !== this.accounts) {
          ElMessage.error('用户名并非当前登录用户')
        } else if (this.password.length === 0) {
          ElMessage.error('请填写密码');
        } else if (this.password.length < 8) {
          ElMessage.error('新密码少于 8 位');
        } else if (this.doubleConfirm !== this.password) {
          ElMessage.error('两次输入密码不一致')
        } else {
          axios.post('/api/accounts/modify', qs.stringify(
              {
                'password': this.password
              }
          )).then(response => {
            if (response.data['state'] === 5) {
              ElMessage.error('新旧密码相同，请重新输入');
            } else if (response.data['state'] === 0) {
              ElMessage.success('修改密码成功，请重新登录');
              this.isLogIn = true;
              this.hasLogIn = false;
              this.isModify = false;
              sessionStorage.clear();
            }
          })
        }
      },
      toReg() {
        this.isModify = false;
        this.isLogIn = false;
      },
      toLog() {
        this.isModify = false;
        this.isLogIn = true;
      },
      toModify() {
        this.isModify = true;
      },
      toHome() {
        //不用管
        this.dialogVisible = false;
        router.replace({path: '/'})
      },
      toAbout() {
        //不用管
        this.dialogVisible = false;
        router.replace({path: '/about'})
      },
    },
    created() {
      this.tableData.push(
          {
            'name': sessionStorage.getItem('name'),
            'phone': sessionStorage.getItem('phone'),
            'desc': '不积跬步，无以至千里；不积小流，无以成江海。',
            'address': '老和山职业技术学院 32 舍'
          }
      );
    }
  };
</script>

<style scoped>
    .in{
      position: relative;
    }
    .log{
      margin: auto;
      max-width: 800px;
    }
</style>