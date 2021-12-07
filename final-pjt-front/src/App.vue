<template>
<div id=app>
  <div>
   <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top align-items-center">
     <div class="d-flex" style="margin-left: 10px; margin-right: auto;">
      <span>
        <router-link @click.native="changeState" :to="{ name: 'Home' }"><img style="height: 40px; weight: 10px" src="./assets/cs_pedia.png" alt="logo-img"></router-link>
      </span>
      <span class="navbar-nav">
        <router-link @click.native="changeState" :to="{ name: 'Home' }" class="nav-link active">Home</router-link>
      </span>
      <span class="navbar-nav" v-if="isLogin">
        <router-link :to="{ name: 'RandomMovies' }" class="nav-link active">영화뽑기</router-link>
      </span>
     </div>

      <TheSearchBar @change-list="changeList" style="margin-left: auto; margin-right: auto;"/>

      <div style="margin-left: auto; margin-right: 20px;">
        <span class="navbar-nav" v-if="isLogin">
          <router-link :to="{ name: 'Profile', params: { userId: getUserId } }" class="nav-link active " >Profile</router-link>
          <button @click="logout" class="nav-link active bg-dark border-0 p-0" >Logout</button> 
        </span>
        <span class="navbar-nav" v-else>
          <router-link :to="{name: 'Login'}" class="nav-link active">Login</router-link>
        </span>
      </div>
    </nav>           

    <div class="main container">
      <router-view :searchmovies="searchmovies"/>
    </div>
  </div>
</div>
</template>

<script>
import { mapGetters } from 'vuex'
import TheSearchBar from '@/components/TheSearchBar'
import { mapState } from 'vuex'
import Login from '@/views/Login'

export default {
  name: 'App',
  components: {
    TheSearchBar,
  },
  views:{
    Login
  },

  data() {
    return {
      searchmovies: [],
    }
  },
  methods: {
    changeState () {
      this.$store.state.searchNow = false
    },
    logout () {
      this.$store.dispatch('deleteToken')
      localStorage.removeItem('accessToken')

      // 현재 경로가 Home이면 로그아웃 시 새로고침
      if (this.$route.name === 'Home') {
        this.$router.go()
      } else {
        // 그 외의 경로일 경우 Home으로 이동하게 한다.
        this.$router.push({ name: 'Home' })
      }
    },
    changeList(moviedata) {
      event.preventDefault()
      let temp = []
      for (let i of moviedata) {
        for (let j of this.allMovies) {
          if (i === j.title) {
            temp.push(j)
          }
        }
      }
      this.searchmovies = temp
      this.$store.state.searchNow = true
      let nowLink = document.location.href.split("/")
      if (nowLink[3] !== "") {
        this.$router.push({ name: 'Home'})
      }
    

    },
  },
  computed: {
    ...mapGetters([
      'isLogin',
      'getUserId',
    ]),
    ...mapState([
      'allMovies',
    ])
  },
  created () {
    const accessToken = localStorage.getItem('accessToken') || ''
    this.$store.commit('SET_TOKEN', accessToken)
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-family: 'Do Hyeon', sans-serif;
}
#nav {
  padding: 30px;
  background-color: #141414;
}
.main {
  text-align: center;
  background-color: #141414;
}
img {
  width: 200px;
  height: 80;
}
footer {
  width: 100%;
  height: 50px;
}
</style>
