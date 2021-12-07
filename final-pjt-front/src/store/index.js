import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    accessToken: '',
    movies: [],
    allMovies: [],
    moviesTitle: [],
    searchNow: false,
    userName: '',
    loading: false,
  },
  getters: {
    isLogin: function (state) {
      return !!state.accessToken
    },
    getUserId: function (state) {
      return JSON.parse(atob(state.accessToken.split('.')[1])).user_id
    },
  },
  mutations: {
    SET_TOKEN (state, newAccessToken) {
      state.accessToken = newAccessToken
    },
    GET_MOVIES (state, moviesData) {
      state.movies = moviesData
    },
    DELETE_TOKEN (state) {
      state.accessToken = ''
      localStorage.removeItem('accessToken')
    },
    SEARCH_MOVIES (state, allData) {
      state.allMovies = allData
      for (let temp of state.allMovies) {
          state.moviesTitle.push(temp.title)
        }
    },
    SET_USERNAME (state, username) {
      state.userName = username
    }
  },
  actions: {
    // 로그인한 User의 username 을 state에 유지
    setUserName ({ commit }, userId) {
      // axios
      axios({
        method: 'get',
        url: `http://localhost:8000/accounts/${userId}/profile/`,
        headers: {
            Authorization: `Bearer ${this.state.accessToken}`
        },
      })
        .then(response => {
          commit('SET_USERNAME', response.data.username)
        })
        .catch(error => {
          alert(error)
        })
    },
    getToken ({commit, dispatch}, {username, password}) {
      axios({
        method: 'post',
        url: 'http://localhost:8000/api/token/',
        data: {
          username,
          password,
        }
      })
        .then(response => {
          localStorage.setItem('accessToken', response.data.access)
          commit('SET_TOKEN', response.data.access)
          router.push({ name: 'Home' })
          dispatch('setUserName', this.getters.getUserId)
        })
        .catch(error => {
          error
          alert('ID와 PASSWORD를 확인해주세요')
        })
    },
    deleteToken ({commit}) {
      commit('DELETE_TOKEN')
    },
    getMovies ({commit, state}) {
      state.loading = true
      // 영화 데이터 요청
      axios({
        method: 'get',
        url: 'http://localhost:8000/movies',
      })
        // mutations 호출
        .then(response => {
          commit('GET_MOVIES', response.data)
          console.log(response)
          state.loading = false
        })
        .catch(error => {
          console.log(error)
        })
    },
    getSearchMovies ({commit, state}) {
      state.loading = true
      // 전체 영화 데이터 가져오기
      axios({
          method: 'get',
          url: 'http://localhost:8000/movies/getmovie/',
      })
        .then(response => {
          commit('SEARCH_MOVIES', response.data)
          state.loading = false
        })
        .catch(error => {
          console.log(error)
        })
    },
  },
  modules: {
  }
})
