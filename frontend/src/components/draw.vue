<template>
  <div class="d-box" id="moveBox" @mousedown="moveTo" :style="{top: x+'px',left:y+'px'}">
    <img :src="path" alt="" />
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";
import light0 from '@/assets/light0.png';
import light1 from '@/assets/light1.png';
import light2 from '@/assets/light2.png';
import light3 from '@/assets/light3.png';
import sensor from '@/assets/sensor.png';
import switch0 from '@/assets/switch0.png';
import switch1 from '@/assets/switch1.png';
import lock0 from '@/assets/lock0.png';
import lock1 from '@/assets/lock1.png';

export default {
  name: "drawBox",
  data() {
    return {
      path: '',
      which: this.who,
      location: {
        top: this.x,
        left: this.y,
      },
    };
  },
  watch: {
    which(n, o) {
      this.which = n;
      this.update();
      console.log(o);
    }
  },
  methods: {
    moveTo(e) {
      e.preventDefault();
      const t = true;
      if (t) {
        let icon = e.currentTarget;
        const x = e.clientX - icon.offsetLeft;
        const y = e.clientY - icon.offsetTop;
        const maxWidth = document.getElementById("moveBox").offsetParent.clientWidth;
        const maxHeight = document.getElementById("moveBox").offsetParent.clientHeight;
        document.onmousemove = (event) => {
          let left = event.clientX - x;
          let top = event.clientY - y;
          if (left < 0) left = 0;
          else if (left > maxWidth) left = maxWidth;
          if (top < 0) top = 0;
          else if (top > maxHeight) top = maxHeight;

          icon.style.left = left + "px";
          icon.style.top = top + "px";

          document.onmouseup = (event) => {
            console.log("draw", this.who);
            icon.style.cursor = "default";
            document.onmousemove = null;
            document.onmouseup = null;
            this.location.left =
                this.location.top = event.clientX - x;

            // return icon location here
            let idArr = String(this.id).split('-');
            let device_id = idArr.slice(-1)[0];
            axios.post('/api/device/pos', qs.stringify(
                {
                  'device_id': device_id,
                  'x': event.clientY - y,
                  'y': event.clientX - x
                }
            )).then(response => {
              console.log(response.data)
            }).catch(e => {
              console.log(e)
            })
          };
        };
      }
    },
    update() {
      if (this.isLight0) {
        this.path = light0;
      } else if (this.isLight1) {
        this.path = light1;
      } else if (this.isLight2) {
        this.path = light2;
      } else if (this.isLight3) {
        this.path = light3;
      } else if (this.isSensor) {
        this.path = sensor;
      } else if (this.isSwitch0) {
        this.path = switch0;
      } else if (this.isSwitch1) {
        this.path = switch1;
      } else if (this.isLock0) {
        this.path = lock0;
      } else if (this.isLock1) {
        this.path = lock1;
      }
    },
  },
  computed: {
    isLight0() {
      return this.which === 'light0';
    },
    isLight1() {
      return this.which === 'light1';
    },
    isLight2() {
      return this.which === 'light2';
    },
    isLight3() {
      return this.which === 'light3';
    },
    isSensor() {
      return this.which === 'sensor';
    },
    isSwitch0() {
      return this.which === 'switch0';
    },
    isSwitch1() {
      return this.which === 'switch1';
    },
    isLock0() {
      return this.which === 'door_lock0';
    },
    isLock1() {
      return this.which === 'door_lock1';
    }
  },
  props: {
    id: String,
    who: String,
    x: Number,
    y: Number,
  },
  components: {
  },
  created() {
    this.update();
  },
};

</script>
<style scoped>
.d-box {
  position: absolute;
  width: 40px;
  height: 40px;
}
.d-box img {
  width: 100%;
  height: 100%;
}
</style> 