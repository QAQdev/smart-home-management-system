<template>
  <div>
    <el-card shadow="always" class="show">
      <el-table :data="tableData" stripe height="600" style="width: 100%">
        <el-table-column prop="scene" label="场景" width="180" />
        <el-table-column prop="room" label="房间" width="180" />
        <el-table-column prop="device" label="设备" width="180" />
        <el-table-column prop="log" label="日志信息" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";
import router from "@/router";
import axios from "axios";
import qs from 'qs';

export default {
  name: "logVue",
  data() {
    return {
      tableData: []
    };
  },
  props: {},
  components: {},
  created() {
    if (!sessionStorage.getItem("userState")) {
      ElMessage.error("你还未登录，将跳转到登录页面");
      router.replace({path: '/sign'})
      return;
    }

    axios.post('/api/scene/getlog', qs.stringify({}))
        .then(res => {
          let logs = res.data;
          console.log(logs);
          for (let i in logs) {
            this.tableData.push(
                {
                  'scene': logs[i]['scene_name'],
                  'room': logs[i]['room_name'],
                  'device': logs[i]['device_name'],
                  'log': logs[i]['log']
                }
            )
          }
        })
  }
}
</script>

<style scoped>
.show {
  margin-top: 4vh;
  text-align: left;
}
</style>