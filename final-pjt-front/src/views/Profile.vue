<template>
  <b-container id="main" class="text-white text-start my-5">
    <!-- Header -->
    <b-row class="my-4">
      <h1 class="fw-bold">{{ username }} 님의 프로필</h1>
    </b-row>
    
    <!-- 기본 정보 -->
    <b-row class="my-4">
      <h3 class="my-4">기본 정보</h3>
      <b-col>
      <div class="card mb-3" style="max-width: 600px; background-color: #141414;">
        <div class="row g-0">
          <div class="col-md-4">
            <img src="@/assets/profile_img.jpg" class="img-fluid rounded-start" alt="..." >
          </div>
          <div class="col-md-8">
            <div class="card-body" style="padding: 0; margin-left: 50px; margin-top: 5px;">
              <h2 class="card-title text-white">UserName</h2>
              <p class="card-text text-white"><small class="text-muted" style="font-size: 30px;">{{ username }}</small></p>
              <h2 class="card-title text-white m">E-mail</h2>
              <p class="card-text text-white"><small class="text-muted" style="font-size: 30px;">{{ email || '없음' }}</small></p>
            </div>
          </div>
        </div>
      </div>
      </b-col>
    </b-row>
    <hr>

      <!-- wish list -->
      <h3 class="my-4">보고싶은 작품</h3>
        <div class="mb-3">
          <b-row cols="5">
          <span
            v-for="movie in like_movies"
            :key="movie.id"
          >
              <b-col class="d-flex flex-column mb-4">
                <img
                  class="mb-1"
                  :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`"
                  @click="moveToDetail(movie.id)"
                  
                >
                <a href="#" @click="moveToDetail(movie.id)" class="link-light text-decoration-none" style="font-size: 20px; text-align: center;">{{ movie.title }}</a>
              </b-col>
            
          </span>
          </b-row>
          
        </div>
      <hr>
      <!-- 작성한 리뷰 -->
      <h3 class="my-4">작성한 리뷰</h3>
      <div>
        <b-row cols="2">
          <div
            v-for="review in reviews"
            :key="review.id"
          >
            <MovieReviewItem
              :review="review"
            />
          </div>
        </b-row>
        <b-spinner class="offset-6" v-if="loading" variant="success" label="Spinning"></b-spinner>
        <h1 v-if="reviews.length === 0" style="text-align: center;color: darkgreen; font-weight: bold;" class="my-5">표시할 리뷰가 없습니다.</h1>
        <h5 v-if="none && reviews.length !== 0" style="text-align: center;color: darkgreen; font-weight: bold" class="mt-3">더 이상 표시할 리뷰가 없습니다.</h5>
      </div>
  </b-container>


</template>

<script>
import { mapState } from 'vuex'
import MovieReviewItem from '@/components/MovieReviewItem'
import axios from 'axios'
import { mapGetters } from 'vuex'
export default {
  name: 'Profile',
  data: function() {
    return {
      username: '',
      email: '',
      like_movies: '',
      reviews: [],
      comments: '',
      pageNum: 2,
      none: false,
    }
  },
  components: {
    MovieReviewItem
  },
  computed: {
    ...mapGetters([
      'getUserId'
    ]),
    ...mapState([
      'loading'
    ])
  },
  methods: {
     getComments(reviewId) {
      axios({
        method: 'get',
        url: `http://localhost:8000/community/${reviewId}/comments/`,
        headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`
        },
      })
        .then(response => {
          this.comments = response.data
        })
        .catch(error => {
          error
        })
    },
    moveToDetail (movieId) {
      this.$router.push( {name: 'MovieDetail', params: {movieId}})
    },
    handleScroll (event) {
      event
      const { scrollHeight, scrollTop, clientHeight } = document.documentElement

      if (scrollHeight - Math.round(scrollTop) === clientHeight) {
        if (!this.none) {
          // 로딩중...
          this.$store.state.loading = true
          // axios
          axios({
            method: 'get',
            url: `http://localhost:8000/community/${this.getUserId}/user_reviews/?page=${this.pageNum}`,
          })
            .then(response => {
              if (response.data) {
                const new_reviews = response.data
                
                new_reviews.forEach((review) => {
                  this.reviews.push(review)
                })
                this.pageNum += 1
              } else {
                this.none = true
              }
              this.$store.state.loading = false
            })
            .catch(error => {
              alert(error)
            })      
        } 
      }
    }
  },
  created () {
    window.addEventListener('scroll', this.handleScroll);
    // profile 정보 요청
    const accessToken = localStorage.getItem('accessToken')
    axios({
      method: 'get',
      url: `http://localhost:8000/accounts/${this.getUserId}/profile/`,
      headers: {
          Authorization: `Bearer ${accessToken}`
      },
    })
      .then(response => {
        this.username = response.data.username
        this.email = response.data.email
        this.like_movies = response.data.like_movies
      })

    // user의 리뷰 1page만 요청
    axios({
      method: 'get',
      url: `http://localhost:8000/community/${this.getUserId}/user_reviews/?page=1`,
    })
      .then(response => {
        this.reviews = response.data
      })
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll);
  },
  
}
</script>

<style scoped>
img {
  width: auto; height: auto;
  max-width: 235px;
  max-height: 285px;
  border-radius: 4px;
}
#main {
  padding: 0px;
}
</style>