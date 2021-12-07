<template>
  <div>
    <div v-if="this.$store.state.searchNow">
      <div v-for="searchmovie in searchmovies" :key="searchmovie.id">
        <br><br>
        <div class="container d-flex justify-content-center " >
          <div class="card mb-3" style="width: 780px;" @click="goDetail( searchmovie.id )">
            <div class="row g-0">
              <div class="col-md-3 my-auto mx-auto">
                <img :src="`https://image.tmdb.org/t/p/original${searchmovie.poster_path}`" class="img-thumbnail rounded-start" alt="sample-img">
              </div>
              <div class="col-md-8 my-auto mx-auto">
                <b-spinner v-if="loading" variant="success" label="Spinning"></b-spinner>
                <div class="card-body mt-2" >
                  <h5 class="card-title">{{ searchmovie.title }}</h5>
                  <p class="card-text">감독</p>
                  <p class="card-text">{{ searchmovie.director }}</p>
                  <p class="card-text">배우</p>
                  <p class="card-text">{{ searchmovie.actors }}</p>
                  <p class="card-text">줄거리</p>
                  <p class="card-text">{{ searchmovie.overview }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <LatestMovie class="my-5"
        :movies="movies.latest_movies"
      />
      <b-spinner v-if="loading" variant="success" label="Spinning"></b-spinner>
      <hr>
      <PopularMovie class="my-5"
        :movies="movies.popularity_movies"
      />
      <b-spinner v-if="loading" variant="success" label="Spinning"></b-spinner>
      <hr>
      <TopRatedMovie class="my-5"
        :movies="movies.vote_movies"
      />
      <b-spinner v-if="loading" variant="success" label="Spinning"></b-spinner>
      <hr>
      <div class="container">
        <div ></div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import PopularMovie from '@/components/PopularMovie'
import TopRatedMovie from '@/components/TopRatedMovie'
import LatestMovie from '@/components/LatestMovie'
import _ from 'lodash'

export default {
  name: 'Home',
  components: {
    PopularMovie,
    TopRatedMovie,
    LatestMovie,
  },
  props: {
    searchmovies: {
      type: Array,
    }
  },
  data() {
    return {
      recommend: [],
    }
  },
  computed: {
    ...mapState(['movies', 'allMovies', 'loading'])
  },
  created() {
    // 영화 가져오기
    this.$store.dispatch('getMovies')
  },
  methods: {
    recommendMovies() {
      this.recommend = _.sampleSize(this.allMovies, 5)
    },
    goDetail(id) {
      for (let i of this.allMovies) {
        if (i.id === id) {
          return this.$router.push( {name: 'MovieDetail', params: { movieId: i.id }})
        }
      }
    },
  },
}
</script>

<style scoped>

div p {
  width: 500px;
  white-space: nowrap;
  text-align: left;
  overflow: hidden; 
  text-overflow: ellipsis;
}
.container .card {
  background: #141414;
  color: white;
  border: 2px solid rgba(25, 135, 84, 0.5);
  box-shadow: 0px 0px 12px rgba(25, 135, 84, 0.18);
}
</style>