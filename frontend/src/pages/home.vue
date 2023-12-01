<template>
    <div>
      <el-card shadow="always" class="card">  
       <img src="@/assets/cat.png" alt="">
       <div><h1>Hello, Mr.Cheng</h1>
       <h4>Welcome to iHome, use it to control your households!</h4></div>
      </el-card>
      <el-card shadow="always" class="show">
        <el-card v-for="scene in Scene" :body-style="{ padding: '0px',width:'320px'}" class="show-card" :key="scene.name" shadow="hover">
          <h3>{{scene.name}}</h3>
          <img :src="scene.src" alt="">
          <el-card shadow="hover"><h4>欢迎来到{{scene.name}}！</h4>
          </el-card>
        </el-card>

        <el-upload
            class="upload-demo"
            drag
            action="/api/scene/upload"
            multiple="false"
            accept=".jpg,.png,.jpeg"
            :http-request="uploadRequest"
            :before-upload="beforeUpload"
        >
          <el-icon size="50"><upload-filled /></el-icon>
          <div class="el-upload__text">
            拖拽文件至此或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              jpg/png 文件大小不能超过 4MB
            </div>
          </template>
        </el-upload>
      </el-card >
    </div>
  </template>
    
<script>
  import router from '@/router';
  import axios from "axios";
  import qs from 'qs';
  import { ElMessage } from "element-plus";
  import {UploadFilled} from "@element-plus/icons-vue";

  export default {
    name: "homeVue",
    data() {
      return {
        Scene: []
      };
    },
    props: {},
    components: {
      UploadFilled
    },
    created() {
      if (!sessionStorage.getItem("userState")) {
        ElMessage.error("你还未登录，将跳转到登录页面");
        router.replace({path: '/sign'})
      }
      // 在这里向后端申请Scene的内容，包括name和url
      axios.post('/api/scene/getall', qs.stringify({}))
          .then(response => {
            let scenes = response.data;
            console.log(scenes);
            for (let i in scenes) {
              this.Scene.push(
                  {
                    name: scenes[i]['scene_name'],
                    src: "http://121.4.99.100:8080/pics/" + scenes[i]['scene_id'] + ".jpg"
                  }
              )
            }
          })
          .catch(e => {
            console.log(e);
          })
    },
    methods: {
      beforeUpload(file) {
        const isJPEG = file.name.split(".")[1] === "jpeg";
        const isJPG = file.name.split(".")[1] === "jpg";
        const isPNG = file.name.split(".")[1] === "png";
        const isWEBP = file.name.split(".")[1] === "webp";
        const isGIF = file.name.split(".")[1] === "gif";
        console.log(file.size);
        const isLt500K = file.size / 1024 / 1024 < 4;
        if (!isJPG && !isJPEG && !isPNG && !isWEBP && !isGIF) {
          ElMessage.error("上传图片只能是 JPEG/JPG/PNG 格式");
        }
        if (!isLt500K) {
          ElMessage.error("单张图片大小不能超过 4MB");
        }
        return (isJPEG || isJPG || isPNG || isWEBP || isGIF) && isLt500K;
      },
      uploadRequest(options) {
        let file = options.file;
        console.log(file);
        let scene_id;
        axios.post('/api/scene/create', qs.stringify({'scene_name': '新场景'}
        )).then(response => {
          scene_id = response.data['scene_id'];
          const reader = new FileReader();
          1110920
          reader.onloadend = function () {
            axios.post('/api/scene/upload', qs.stringify(
                {
                  'name': scene_id,
                  'code': reader.result
                }
            )).then(response => {
              if (response.data['state'] == 0) {
                ElMessage.success("图片上传成功");
                this.Scene.push({
                  name: response.data['scene_name'],
                  index: response.data['scene_id'],
                  src: "http://121.4.99.100:8080/pics/" + scene_id + '.jpg',
                })
              } else {
                ElMessage.success("图片上传失败");
              }
            })
          }
          reader.readAsDataURL(file);
        }).catch(e => {
          ElMessage.error("上传图片创建场景时出现错误");
          console.log(e);
        })
      },
    },
  };
</script>

<style scoped>
.card{
  height: 200px;
  text-align: left;
}
.card img{
  height: 160px;
  width:auto;
  display: inline-block;
  vertical-align: middle;
  margin-right: 6vw;
}
.card div{
  display: inline-block;
}
.card div h4{
  margin-top: 40px;
  color:grey;
}
.show{
  margin-top: 5vh;
  text-align: left;
}
.show-card{
  display:inline-block;
  width:320px;
  margin:30px;
 
}
.show-card img{
  width: 320px;
  height:230px;
}
.show-card h3{
  text-align: left;
  padding-left:20px;
}
.show-card h4{
  color:grey;
  text-align: left;
}
.add{
  height:150px !important;
  width: 150px !important;
  margin-top:123px !important;
  margin-left:85px !important;
  margin-right: 85px !important;
  margin-bottom: 123px !important;
}
.show-card-add{
  width: 320px;
  height: 396px;
  display:inline-block;
  margin:30px;
}
  </style>