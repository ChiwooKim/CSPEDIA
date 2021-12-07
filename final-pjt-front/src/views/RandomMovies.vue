<template>
  <b-container>
    <div id="head">
      <h1 class="text-center my-5">
        <span class="text-danger">랜</span>
        <span class="text-primary">덤 </span>
        <span class="text-warning">영</span>
        <span class="text-success">화</span>
        
        <span class="text-light"> 뽑기</span>
      </h1>
    </div>

    <!-- button -->
    <b-btn v-if="!loading" class="btn-danger random-button fs-3" @click="[pickRandom(), addPopcorn()]" style="position: relative; top: 100px; width: 300px; height: 100px">Pick</b-btn>

    <div style="position: relative; top: 120px">
      <b-spinner v-if="loading" variant="success" label="Spinning"  ></b-spinner>
    </div>

    <!-- 로딩 화면 -->
    <b-container style="position: relative; top: 200px">
      <b-row cols="3" id="loading">
      </b-row>
    </b-container>
 
    <b-container id="body" v-show="!loading">
      <b-row cols=5>
        <b-col
          v-for="movie in randomMovies"
          :key="movie.id"
        >
        
          <!-- modal 창 -->
          <b-modal
            :id="`${movie.id}`"
            title="상세보기"
            size="xl"
            scrollable
            body-bg-variant="dark"
            hide-header
            hide-footer
          > 
            <MovieDetail
              :movieId="String(movie.id)"
            />
          </b-modal>
          
          <div class="card" :id="`movie-${movie.id}`">
            <div class="card-inner">
              <!-- 카드 앞면 -->
              <div v-if="!movieLoading" class="card-front d-flex justify-content-center align-items-center">
                <span style="font-size: 80px; color: white;">
                  <i class="far fa-hand-point-up"></i>
                </span>        
              </div>
              
              <!-- 카드 뒷면 (영화 포스터) -->
              <div class="card-back" v-b-modal="`${movie.id}`">
                <img :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`" class="card-img-top" alt="movie-poster">
                <div class="card-body my-2" style="background-color: #141414; border-radius: 10px">
                  <p class="card-text text-center text-light">{{ movie.title }}</p>
                </div>
              </div>
              
            </div>
          </div>    
        </b-col>
      </b-row>
    </b-container> 
  </b-container>
</template>

<script>
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

import MovieDetail from '@/components/MovieDetail'
import axios from 'axios'
import _ from 'lodash'
import { mapGetters } from 'vuex'
import { mapState } from 'vuex'

export default {
  name: 'RandomMovies',
  data: function () {
    return {
      userMovies: [],
      randomMovies: new Set(),
      movieLoading: false,
    }
  },
  components: {
    MovieDetail
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
    async addPopcorn () {
      console.log('팝콘함수 실행')
      const row = document.querySelector("#loading")
      const btn = document.querySelector(".random-button")
      btn.innerText = "영화를 뽑는중입니다..."

      while (this.movieLoading) {
        const col = document.createElement("b-col")
        const img = document.createElement("img")
        img.src = "/img/popcorn.9c7c2663.png"
        col.appendChild(img)
        row.appendChild(col)
        await sleep(1000)
      }

      while (row.hasChildNodes()) {
        row.removeChild(row.firstChild)
      }
      
      btn.innerText  = "다시 뽑기"

    },
    async pickRandom () {
        this.movieLoading = true

        // 기존 randomMovies 배열 초기화
        this.randomMovies = new Set()
        while (this.randomMovies.size < 5) {
          const allMovies = this.$store.state.allMovies
          const pickedMovie = _.sample(allMovies)
          const userMovieIds = this.userMovies.map(movie => {
            return movie.id
          })
          if (userMovieIds.includes(pickedMovie.id)) {
            continue
          }
          this.randomMovies.add(pickedMovie)
        }

        const randomMovieIds = []
        for (const movie of this.randomMovies) {
          randomMovieIds.push(movie.id)
        }
        
        await sleep(3000)
        
        for (const movieId of randomMovieIds) {
          // 각 card에 toggle 기능 부여
          const card = document.querySelector(`#movie-${movieId}`)
          card.addEventListener("mouseenter", () => {
            card.classList.toggle("flipped")
          })
          card.addEventListener("mouseleave", () => {
            card.classList.toggle("flipped")
          })
        }
        this.movieLoading = false
    }
  },


  created: async function() {
    setTimeout(() => {
      this.$store.state.loading = false
    }, 1500)

    // Login 한 User 가 리뷰를 작성한 모든 영화 객체 가져오기 && userMovies 에 삽입
    // 1. User의 모든 리뷰 가져오기
    this.$store.state.loading = true
    axios({
      method: 'get',
      url: `http://localhost:8000/community/${this.getUserId}/user_reviews_all/`,
    })
      .then(response => {
        const userReviews = response.data
        // 2. 받아온 모든 리뷰를 순회, movie_id에 접근
        for (const review of userReviews) {
          const movieId = review.movie
          // axios - user가 리뷰를 작성한 영화 정보 요청
          axios({
            method: 'get',
            url: `http://localhost:8000/movies/${movieId}/`,
          })
            .then(response => {
              // 각각의 영화 객체를 userMovies에 삽입
              this.userMovies.push(response.data)
              
            })
        }     
      })
  }
}
</script>

<style scoped>
.card {
  background-color: #141414;
  position: relative;
  top: 200px;
  cursor: pointer;
  width: 200px;
  height: 285px;
  margin: 0 auto;
  perspective: 500px;
}

.b-modal {
  background-color: #141414;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}

.card.flipped .card-inner {

  transform: rotateY(180deg);
}

img {
  width:100%;
  height:100%;
  object-fit:cover;
  border-radius: 10px;
}

.card-back,
.card-front {
  position: absolute;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  backface-visibility: hidden;
  background-color: #142f25;
  border-radius: 10px;
}



.card-back {
  transform: rotateY(180deg);
}
</style>