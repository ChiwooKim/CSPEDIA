<template>
  <div>
    <h2 class="text-white">Latest Movie</h2>
    <br>
    <swiper class="swiper" :options="swiperOption" @click-slide="clickSlide">
      <swiper-slide
        v-for="movie in movies"
        :key="movie.id"
        :style="{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        width: '300px',
        height: '400px',
        textAlign: 'center',
        fontWeight: 'bold',
        backgroundPosition: 'center',
        backgroundSize: 'cover',
        backgroundImage: 'url(' + 'https://image.tmdb.org/t/p/original' + movie.poster_path + ')'
        }"
      >
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination">
      </div>
    </swiper>
  </div>
</template>

<script>
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/css/swiper.css";
import axios from 'axios'

export default {
  name: 'LatestMovie',
  props: {
    movies: {
      type: Array,
    }
  },
  components: {
    Swiper,
    SwiperSlide,
  },
  methods: {
    clickSlide (index) {
      const movieId = String(this.movies[index].id)
      // axios
      axios({
        method: 'get',
        url: `http://localhost:8000/movies/${movieId}`,
      })
        .then(response => {
          console.log(response)
          this.$router.push( {name: 'MovieDetail', params: {movieId}})
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
    data() {
      return {
        swiperOption: {
          effect: 'coverflow',
          grabCursor: true,
          loop: false,
          centeredSlides: true,
          slidesPerView: 4,
          coverflowEffect: {
            rotate: 25,
            stretch: -20,
            depth: 100,
            modifier: 1,
            slideShadows : true
          },
          pagination: {
            el: '.swiper-pagination'
          }
        }
      }
    } 
  }
</script>

<style lang="scss" scoped>
  .swiper {
    height: 100%;
    width: 100%;
  }
</style>