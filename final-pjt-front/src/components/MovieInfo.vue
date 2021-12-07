<template>
  <b-container class="text-start my-5" v-if="movie" style="position: relative; top: 50px;">
    <b-row id="movieInfo1">
      <!-- 포스터 -->

      <b-col>
        <img id="poster-img" :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`" alt="sample-img">
      </b-col>
      
      <b-col class="d-flex flex-column justify-content-between align-items-center">
        <!-- 기본정보 -->
        <!-- 제목 -->
        <b-row align-h="start" class="mb-5 align-self-start">
          <h1 class="fw-bold text-white">{{ movie.title }}</h1>
        </b-row>
        <!-- 세부정보 -->
        <b-row class="mb-5 align-self-start">
          <div class="text-start fs-4 text-white">
            <p>
              <span class="text-success">기본정보 </span>
              <span class="fs-5">
                <span>{{ releaseDate }} ・ </span>
                <span>{{ genreStr }} ・ </span>
                <span>{{ movie.country }}</span>
              </span>
            </p>
            <p>
              <span class="text-success">감독</span> <span class="fs-5">{{ movie.director }}</span>
            </p>
            <p>
              <span class="text-success">출연진</span> <span class="fs-5">{{ movie.actors }}</span>
            </p>
            <p class="mt-5">
              <span><i class="fas fa-star text-warning"></i> {{ movie.vote_average }} </span>
              <span>({{ movie.vote_count }}명 참여)</span>
            </p>
          </div>
        </b-row>
        <!-- Button -->
        <div class="align-self-start">
          <div class="d-flex align-items-center">

            <div @click="addToMyList" class="me-5 fs-5" style="cursor: pointer">
              <p class="text-success" v-show="likeState"><i class="fas fa-check"> </i> 보고싶어요</p>
              <p class="text-light" v-show="!likeState"><i class="fas fa-plus"> </i> 보고싶어요</p>
            </div>

            <div>
            <p class="link-light fs-5" @click="moveToReview" style="cursor: pointer"><i class="fas fa-pen"></i> 리뷰 쓰기</p>
            </div>
            
          </div>
        </div>
      </b-col>
    </b-row>

    <hr class="my-5">
    <!-- 기본정보 2 -->
    <b-row id="movieInfo2" class="my-5 d-flex justify-content-between">
      <!-- 줄거리 -->
      <b-col class="text-start text-white">
        <h2>줄거리</h2>
        <p class="fs-5">{{ movie.overview }}</p>
      </b-col>
      <b-col id="col-video" class="align-self-center">
        <b-embed
          id="video"
          class="align-self-center"
          type="iframe"
          aspect="16by9"
          :src="`https://www.youtube.com/embed/${movie.video_key}?rel=0`"
          allowfullscreen
        ></b-embed>
      </b-col>
    </b-row>
    <hr>
  </b-container>
</template>

<script>
import axios from 'axios'
import { mapGetters } from 'vuex'

export default {
  name: 'MovieInfo',
  props: {
    movieId: {
      type: String,
    }
  },
  data () {
    return {
      movie: null,
      releaseDate: null,
      genreList: [],
      genreStr: '',
      likeState: null,
    }
  },
  methods: {
    moveToReview: function () {
      if (this.isLogin) {
        const movieId = this.movieId
        this.$router.push({ name: 'CreateReview', params: {movieId, reviewId: 0} })
      } else {
        // 로그인되어있지 않은 경우
        alert('리뷰작성을 위해 로그인해주세요')
        this.$router.push({ name: 'Login' })
      }
    },
    addToMyList: function () {
      this.likeState = !this.likeState
      if (this.isLogin) {
        const accessToken = localStorage.getItem('accessToken')
        // const movieId = this.movieId
        // axios 요청
        axios({
          method: 'post',
          url: `http://localhost:8000/movies/${this.movieId}/movie_like/`,
          headers: {
          Authorization: `Bearer ${accessToken}`
          }, 
        })
          .then(response => {
            console.log(response)
          })
          .catch(error => {
            alert(error)
          })
      } else {
        // 로그인되어있지 않은 경우
        alert('로그인해주세요.')
        this.$router.push({ name: 'Login' })
      }
    }
  },
  computed: {
  ...mapGetters([
    'isLogin',
    'getUserId'
  ])
  },
  created () {
    axios({
      method: 'get',
      url: `http://localhost:8000/movies/genre`,
    })
      .then(response => {
        this.genreList = response.data
      })

    // axios
    axios({
        method: 'get',
        url: `http://localhost:8000/movies/${this.movieId}`,
    })
      .then(response => {
        this.movie = response.data
        this.releaseDate = this.movie.release_date.substr(0, 10)

        // 장르를 문자열로
        for (const genre_id of this.movie.genres) {
          for (const genreObj of this.genreList) {
            if (genre_id === genreObj.id) {
              this.genreStr += genreObj.name + '/'
            }
          }
        }

        if (this.isLogin && this.movie.like_users.includes(this.getUserId)) {
          this.likeState = true
        } else {
          this.likeState = false
        }
      })
      .catch(error => {
        console.log(error)
      })

  }
}
</script>

<style scoped>
#movieInfo1 {
  display: flex;
}

#movieInfo2 {
   display: flex;
}

img {
  width: 400px;
  object-fit: cover;
}

#video {
  position: relative;
  /* left: 180px; */
  left: 0;
  width: 100%;
  height: 300px;
  object-fit:cover;
  border-radius: 15px;
}

#poster-img {
  max-width:100%;
  max-height:100%;
  border-radius: 4px;
  object-fit:cover;
}
</style>