<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="fit-content">
        <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
          <el-radio-button :label="false">展开</el-radio-button>
          <el-radio-button :label="true">折叠</el-radio-button>
        </el-radio-group>
        <el-menu default-active="2" class="el-menu-vertical-demo" :collapse="isCollapse" @open="handleOpen"
          @close="handleClose">
          <el-menu-item @click="changeRouter" index="4">

            <el-icon><icon-menu /></el-icon>
            <template #title><router-link class="router-link-active" to="/" @click="changeRouter();changeToHome()">Home</router-link> </template>
          </el-menu-item>
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span @click="changeScene(this.activeSceneId)">Scene</span>
            </template>
            <el-sub-menu v-for="item in Scene" :index="item.index" :key="item.index" @dblclick="sceneRename(item)">
              <template #title>
                <span v-if="!item.isShow" @click="changeScene(item.index)">{{ item.name }}</span>
                <el-input @blur="sceneFinishInput(item)" v-if="item.isShow" v-model="item.name"
                          placeholder="输入场景名"></el-input>
              </template>

              <el-menu-item v-for="room in item.rooms" :index="room.index" :key="room.index" @dblclick="roomRename(room)" @click="changeRoom(room.index)">
                <p v-if="!room.isShow">{{ room.name }}</p>

                <el-input @blur="roomFinishInput(room)" v-if="room.isShow" v-model="room.name"
                  placeholder="输入房间名"></el-input>
              </el-menu-item>

              <el-menu-item @click="newRoom(item)"><el-icon><plus/></el-icon>添加房间</el-menu-item>
            </el-sub-menu>
          </el-sub-menu>

          <el-menu-item @click="changeRouter();changeToSign()" index="2">
            <el-icon>
              <setting />
            </el-icon>
            <template #title><router-link class="router-link-active" to="/sign">Accounts</router-link> </template>
          </el-menu-item>
          <el-menu-item @click="changeRouter();changeToLog()" index="3">
            <el-icon>
              <message />
            </el-icon>
            <template  #title><router-link class="router-link-active" to="/log">Log</router-link> </template>
          </el-menu-item>
          <el-menu-item @click="changeRouter();changeToAbout()" index="3">
            <el-icon>
              <info-filled />
            </el-icon>
            <template  #title><router-link class="router-link-active" to="/about">About</router-link> </template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <el-page-header style="margin-top: 10px">
            <template #breadcrumb>
              <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: './page-header.html' }">
                  iHome
                </el-breadcrumb-item>
                <el-breadcrumb-item><a href="./page-header.html">{{
                    activeScene
                }}</a></el-breadcrumb-item>
                <el-breadcrumb-item>{{ activeRoom }}</el-breadcrumb-item>
              </el-breadcrumb>
            </template>
            <template #content>
              <span style="font-size:14px " >{{title}}</span>
            </template>
          </el-page-header>
        </el-header>
        <el-main>
            <div  v-if="isScene" id="mainBox">
              <el-row class="tac">
                <el-col :span="5">
                  <el-menu id="room-bar" v-if="showRoomBar" default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">
                    <el-sub-menu v-for="thing in Items.itemList" :index="thing.id" :key="thing.id" @dblclick="deviceRename(thing)">
                      <template #title>
                        <el-icon>
                          <odometer />
                        </el-icon>
                        <span v-if="!thing.isShow">{{ thing.name }}</span>
                        <el-input @blur="deviceFinishInput(thing)" v-if="thing.isShow" v-model="thing.name" placeholder="输入设备名"></el-input>
                      </template>
                      <br />
                      <el-slider v-if="thing.type==='light'" @input="updateInfo(thing)" v-model="thing.info" :step="10"/>
                      <el-switch v-if="thing.type!=='light' && thing.type !== 'sensor'" @click="updateInfo(thing)" v-model="thing.info" active-text="On" inactive-text="Off" />
                      <div v-if="thing.type === 'sensor'" class="row center">
                        <el-tooltip :content="'现在'+this.activeRoom+'的温度是'+thing.info+'°C'" placement="top" class="box-item">
                          <el-button v-model="thing.info" style="text-align: center" @click="updateInfo(thing)">点我查看更多信息</el-button>
                        </el-tooltip>
                      </div>
                      <br />
                    </el-sub-menu>
                    <el-sub-menu index="2">
                      <template #title>
                        <el-icon>
                          <plus />
                        </el-icon>
                        添加设备
                      </template>
                      <p>
                        <el-button type="primary" size="big" @click="newLight(this.activeRoomId)"><el-icon><opportunity/></el-icon>灯</el-button>
                      </p>
                      <p>
                        <el-button type="primary" size="big" @click="newSensor(this.activeRoomId)"><el-icon><cpu/></el-icon>传感器</el-button>
                      </p>
                      <p>
                        <el-button type="primary" size="big" @click="newSwitch(this.activeRoomId)"><el-icon><switch-button/></el-icon>开关</el-button>
                      </p>
                      <p>
                        <el-button type="primary" size="big" @click="newDoorLock(this.activeRoomId)"> <el-icon><lock/></el-icon>锁</el-button>
                      </p>
                    </el-sub-menu>

                  </el-menu>
                </el-col>
                <el-col
                    :span="19"
                    id="container"
                    ref="container"
                    :style="{ backgroundImage: 'url(' + showScene + ')'}" v-if="hasScene">
                  <draw-box
                      v-for="thing in AllItems.itemList"
                      :x="thing.x"
                      :y="thing.y"
                      :key="thing.id+timer"
                      :id="thing.id"
                      :who="thing.who">
                  </draw-box>
                </el-col>
                <el-col id="container" ref="container" v-if="!hasScene">
                  <el-card shadow="always" class="show">
                    <el-empty :image-size="250" description="还没有场景呢，快去创建吧！ " />
                  </el-card>
                </el-col>
              </el-row>
            </div>
          <router-view v-else></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import drawBox from "./components/draw.vue";
import { ArrowRight } from "@element-plus/icons-vue";
import { ref } from "vue";
import {
  Menu as IconMenu,
  Location,
  Setting,
  Plus,
  Cpu,
  Opportunity,
  Lock,
  SwitchButton,
  Odometer,
  Message,
  InfoFilled
} from "@element-plus/icons-vue";

import axios from "axios";
import qs from "qs";
import { ElMessage } from "element-plus";
import router from "@/router";

const isCollapse = ref(false);
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};

const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};

export default {
  name: "HelloWorld",
  data() {
    return {
      title: "",
      isCollapse,
      ArrowRight,
      activeRoom: "",
      activeScene: "",
      activeRoomId: "",
      activeSceneId: "",
      hasScene: false,
      isScene: false,
      Scene: [],
      showScene: "",
      Items: {},
      AllItems: {},
      showRoomBar: false,
      timer:''
    };
  },
  created() {
    if (!sessionStorage.getItem("userState")) {
      ElMessage.error("你还未登录，将跳转到登录页面");
      router.replace({path: '/sign'})
      return;
    }
    this.title = "Home";
    // 这里首先需要先获取所有Scene的房间信息
    let scenes;
    axios.post('/api/scene/getall', qs.stringify({}))
        .then(response => {
          scenes = response.data;
          for (let i in scenes) {
            this.hasScene = true;
            this.activeSceneId = scenes[0]['scene_id'];
            let roomArr = [];
            let rooms = scenes[i]['rooms'];
            for (let j in rooms) {
              roomArr.push(
                  {
                    name: rooms[j]['room_name'],
                    index: scenes[i]['scene_id'] + "-" + rooms[j]['room_id'],
                    isShow: false
                  }
              )
            }
            this.Scene.push(
                {
                  name: scenes[i]['scene_name'],
                  index: scenes[i]['scene_id'],
                  rooms: roomArr,
                  isShow: false
                }
            )
          }
        })
        .catch(e => {
          console.log(e);
        })
  },
  methods: {
    handleClose,
    handleOpen,
    // for APP.vue
    changeScene(id) {

      if (!sessionStorage.getItem("userState")) {
        ElMessage.error("你还未登录，将跳转到登录页面");
        router.replace({path: '/sign'})
      }

      this.title = "ScenePage";
      this.showRoomBar = false;
      this.isScene = true;
      // 用传进来的scene id获取指定scene的图片url和name
      let sceneId = id;

      axios.post('/api/scene/getname', qs.stringify({'scene_id': id}))
          .then(response => {

            let scene = response.data;

            this.activeScene = "Scene" + id;
            this.showScene = "http://121.4.99.100:8080/pics/" + scene['scene_id'] + ".jpg"
          })
          .catch(e => {
            console.log(e);
          })

      //这里根据传进来的sceneID，向后端请求当前场景所有Items，用于渲染图片上的图标
      this.AllItems = {itemList: []};
      axios.post('/api/room/getall', qs.stringify({'scene_id': sceneId}))
          .then(response1 => {
            let rooms = response1.data;
            console.log("rooms", rooms);
            for (let i in rooms) {
              axios.post('/api/device/getall',
                  qs.stringify({'room_id': rooms[i]['room_id'],})
              ).then(response2 => {
                let devices = response2.data;
                for (let j in devices) {

                  // 判断显示图片类型
                  let choice;
                  if (devices[j]['device_type'] === 'light') {
                    if (devices[j]['device_info'] == 0) {
                      choice = 'light0';
                    } else if (devices[j]['device_info'] <= 30) {
                      choice = 'light1';
                    } else if (devices[j]['device_info'] <= 60) {
                      choice = 'light2';
                    } else {
                      choice = 'light3';
                    }
                  } else if (devices[j]['device_type'] === 'sensor') {
                    choice = 'sensor';
                  } else if (devices[j]['device_type'] === 'door_lock') {
                    if (devices[j]['device_info'] == 1) {
                      choice = 'door_lock1';
                    } else {
                      choice = 'door_lock0';
                    }
                  } else if (devices[j]['device_type'] === 'switch') {
                    if (devices[j]['device_info'] == 1) {
                      choice = 'switch1';
                    } else {
                      choice = 'switch0';
                    }
                  }

                  this.AllItems.itemList.push(
                      {
                        id: sceneId + "-" + rooms[i]['room_id'] + "-" + devices[j]['device_id'],
                        name: devices[j]['device_name'],
                        info: devices[j]['device_info'],
                        x: devices[j]['x'],
                        y: devices[j]['y'],
                        who: choice
                      }
                  )
                }
                console.log("aaa", this.AllItems.itemList);
              }).catch(e => {
                console.log(e);
              })
            }

          })
          .catch(e => {
            console.log(e);
          })
    },
    changeRouter() {
      // 不用管
      this.showRoomBar = false;
      this.isScene = false;
    },
    newRoom(f) {
      axios.post(
          '/api/room/create',
          qs.stringify({
            'room_name': '房间',
            'scene_id': f.index
          })
      ).then(
          response => {
            this.activeRoom = response.data['room_name'];
            f.rooms.push({
              name: response.data['room_name'],
              index: f.index + "-" + response.data['room_id'],
              isShow: false
            })
          }
      ).catch(error => {
        alert(error);
      })
    },
    roomRename(r) {
      //不用管
      r.isShow = true;
    },
    sceneRename(s) {
      s.isShow = true;
    },
    deviceRename(d) {
      d.isShow = true;
    },
    deviceFinishInput(d) {
      let idArr = String(d.id).split('-');
      axios.post('/api/device/changename',
          qs.stringify({'device_id': idArr.slice(-1)[0], 'device_name': d.name}))
          .then(response => {
            if (response.data['state'] === 0) {
              ElMessage.success('设备名修改成功')
            }
          })
          .catch(e => {
            console.log(e);
          })
      d.isShow = false;
    },
    sceneFinishInput(s) {
      axios.post(
          '/api/scene/update',
          qs.stringify({'scene_id': s.index, 'scene_name': s.name})
      ).then(
          response => {
            if (response.data['state'] === 0) {
              ElMessage.success('场景名修改成功')
            }
          }
      ).catch(error => {
        console.log(error);
      })
      s.isShow = false;
    },
    roomFinishInput(r) {
      let idArr = String(r.index).split('-');
      axios.post(
          '/api/room/update',
          qs.stringify({'room_id': idArr.slice(-1)[0], 'room_name': r.name})
      ).then(
          response => {
            if (response.data['state'] === 0) {
              ElMessage.success('房间名修改成功')
            }
          }
      ).catch(error => {
        console.log(error);
      })
      r.isShow = false;
    },
    changeRoom(id) {
      // 用传进来的room id获取当前room的名字和itemList
      let idArr = String(id).split('-');
      let roomId = idArr.slice(-1)[0];
      this.showRoomBar = true;

      axios.post('/api/room/getname', qs.stringify({'room_id': roomId}))
          .then(response => {
            this.activeRoom = response.data['room_name'];
          });

      this.activeRoomId = id;
      this.Items = {itemList: []};
      axios.post('/api/device/getall',
          qs.stringify(
              {
                'room_id': roomId,
              }
          ))
          .then(response => {
            this.Items['nowId'] = 0;
            let devices = response.data;
            for (let i in devices) {
              let choice;
              if (devices[i]['device_type'] === 'light') {
                console.log("changeRoom", devices[i]['device_info']);
                if (devices[i]['device_info'] == 0) {
                  choice = 'light0';
                } else if (devices[i]['device_info'] <= 30) {
                  choice = 'light1';
                } else if (devices[i]['device_info'] <= 60) {
                  choice = 'light2';
                } else {
                  choice = 'light3';
                }
              } else if (devices[i]['device_type'] === 'sensor') {
                choice = 'sensor';
              } else if (devices[i]['device_type'] === 'door_lock') {
                if (devices[i]['device_info'] == 1) {
                  choice = 'door_lock1';
                } else {
                  choice = 'door_lock0';
                }
              } else if (devices[i]['device_type'] === 'switch') {
                if (devices[i]['device_info'] == 1) {
                  choice = 'switch1';
                } else {
                  choice = 'switch0';
                }
              }

              this.Items['itemList'].push(
                  {
                    id: id + "-" + devices[i]['device_id'],
                    name: devices[i]['device_name'],
                    info: devices[i]['device_info'], // 需要！
                    type: devices[i]['device_type'],
                    x: devices[i]['x'],
                    y: devices[i]['y'],
                    who: choice
                  }
              )
            }
          })
          .catch(e => {
            console.log(e);
          })
    },
    changeToHome() {
      // 不用管
      this.activeScene = "Home";
      this.activeRoom = "Welcome";
      this.title = "HomePage";
    },
    changeToSign() {
      // 不用管
      this.title = "SignPage";
      this.activeScene = "Accounts";
      this.activeRoom = "sign & log";
    },
    changeToLog() {
      this.title = "InfoPage"
      this.activeScene = "Log";
      this.activeRoom = "table";
    },
    changeToAbout() {
      this.title = "AboutPage"
      this.activeScene = "About";
      this.activeRoom = "me";
    },
    // for Scene
    newLight(roomId) {
      // 向后端添加一个新的light，并返回这个item的基本信息
      let idArr = String(roomId).split('-');
      let id = idArr.slice(-1)[0];
      axios.post('/api/device/install',
          qs.stringify(
              {
                'device_name': '灯',
                'device_type': 'light',
                'room_id': id
              }
          ))
          .then(response => {
            console.log("install", response.data);
            this.Items.itemList.push(
                {
                  id: roomId + "-" + response.data['device_id'],
                  name: response.data['device_name'],
                  info: response.data['device_info'],
                  type: response.data['device_type'],
                  x: response.data['x'],
                  y: response.data['y'],
                  who: 'light0',
                  isShow: false
                }
            );
            this.AllItems.itemList.push({
              id: roomId + "-" + response.data['device_id'],
              name: response.data['device_name'],
              info: response.data['device_info'],
              type: response.data['device_type'],
              x: response.data['x'],
              y: response.data['y'],
              who: 'light0',
              isShow: false
            })
          }).catch(e => {
        console.log(e);
      })
    },
    newSensor(roomId) {
      // 向后端添加一个新的sensor，并返回这个item的基本信息
      let idArr = String(roomId).split('-');
      let id = idArr.slice(-1)[0];
      axios.post('/api/device/install',
          qs.stringify(
              {
                'device_name': '传感器',
                'device_type': 'sensor',
                'room_id': id
              }
          )).then(response => {
        this.Items.itemList.push(
            {
              id: roomId + "-" + response.data['device_id'],
              name: response.data['device_name'],
              info: response.data['device_info'],
              type: response.data['device_type'],
              x: response.data['x'],
              y: response.data['y'],
              who: 'sensor',
              isShow: false
            }
        );
        this.AllItems.itemList.push({
          id: roomId + "-" + response.data['device_id'],
          name: response.data['device_name'],
          info: response.data['device_info'],
          type: response.data['device_type'],
          x: response.data['x'],
          y: response.data['y'],
          who: 'sensor',
          isShow: false
        })
      }).catch(e => {
        console.log(e);
      })
    },
    newSwitch(roomId) {
      // 向后端添加一个新的switch，并返回这个item的基本信息
      let idArr = String(roomId).split('-');
      let id = idArr.slice(-1)[0];
      axios.post('/api/device/install',
          qs.stringify(
              {
                'device_name': '开关',
                'device_type': 'switch',
                'room_id': id
              }
          )).then(response => {
        this.Items.itemList.push(
            {
              id: roomId + "-" + response.data['device_id'],
              name: response.data['device_name'],
              info: response.data['device_info'],
              type: response.data['device_type'],
              x: response.data['x'],
              y: response.data['y'],
              who: 'switch1',
              isShow: false
            }
        );
        this.AllItems.itemList.push({
          id: roomId + "-" + response.data['device_id'],
          name: response.data['device_name'],
          info: response.data['device_info'],
          type: response.data['device_type'],
          x: response.data['x'],
          y: response.data['y'],
          who: 'switch1',
          isShow: false
        })
      }).catch(e => {
        console.log(e);
      })
    },
    newDoorLock(roomId) {
      let idArr = String(roomId).split('-');
      let id = idArr.slice(-1)[0];
      axios.post('/api/device/install',
          qs.stringify(
              {
                'device_name': '锁',
                'device_type': 'door_lock',
                'room_id': id
              }
          )).then(response => {
        this.Items.itemList.push(
            {
              id: roomId + "-" + response.data['device_id'],
              name: response.data['device_name'],
              info: response.data['device_info'],
              type: response.data['device_type'],
              x: response.data['x'],
              y: response.data['y'],
              who: 'door_lock1',
              isShow: false
            }
        );
        this.AllItems.itemList.push({
          id: roomId + "-" + response.data['device_id'],
          name: response.data['device_name'],
          info: response.data['device_info'],
          type: response.data['device_type'],
          x: response.data['x'],
          y: response.data['y'],
          who: 'door_lock1',
          isShow: false
        })
      }).catch(e => {
        console.log(e);
      })
    },
    updateInfo(device) {
      let idArr = String(device.id).split('-');
      let deviceId = idArr.slice(-1)[0];

      if (device.type !== 'sensor') {
        axios.post('/api/device/update', qs.stringify({'device_id': deviceId, 'device_info': Number(device.info)}))
            .then(response => {
              if (response.data['state'] === 0) {
                for (let i in this.AllItems.itemList) {
                  if (this.AllItems.itemList[i].id === device.id) {
                    let info = Number(device.info);
                    if (info === 0) {
                      this.AllItems.itemList[i].who = String(device.type) + '0';
                    } else if (info <= 30) {
                      this.AllItems.itemList[i].who = String(device.type) + '1';
                    } else if (info <= 60) {
                      this.AllItems.itemList[i].who = String(device.type) + '2';
                    } else {
                      this.AllItems.itemList[i].who = String(device.type) + '3';
                    }
                    this.timer = new Date().getTime();

                    let sceneId = idArr.slice(0)[0];
                    let roomId = idArr.slice(1)[0];
                    let sceneName = '';
                    let roomName = '';

                    axios.post('/api/scene/getname', qs.stringify({'scene_id': sceneId}))
                        .then(res => {
                          sceneName = res.data['scene_name'];
                          axios.post('/api/room/getname', qs.stringify({'room_id': roomId}))
                              .then(res => {
                                roomName = res.data['room_name'];
                                axios.post('/api/scene/log', qs.stringify(
                                    {
                                      'scene_name': sceneName,
                                      'room_name': roomName,
                                      'device_name': device.name,
                                      'log': new Date().toLocaleDateString() + ", "
                                          + new Date().toLocaleTimeString()
                                          + ", 设备值修改为 " + Number(device.info)
                                    }
                                ))
                              })
                        })
                    break;
                  }
                }
              }
            }).catch(e => {
          console.log(e);
        })
      }
    }
  },
  components: {
    drawBox,
    IconMenu,
    Location,
    Setting,
    Plus,
    Cpu, // sensor
    SwitchButton, // switch
    Lock, // door lock
    Opportunity, // light
    Odometer,
    Message,
    InfoFilled
  },
};
</script>


<style>
#container {
  position: relative;
  background-size: auto, 80%;
  background-repeat: no-repeat;
  height:800px;
}
a{
  text-decoration: none;
}
.test {
  position: absolute;
  left: 100px;
  top: 100px;
}
#room-bar{
  height: 80vh;
}
#app {
  font-family: Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.router-link-active {
  text-decoration: none;
  color: black;
}

nav {
  padding: 30px;
}

.show{
  margin-top: 5vh;
  text-align: left;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  height: 90vh;
}

.tooltip-base-box .row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.tooltip-base-box .center {
  justify-content: center;
}
</style>
