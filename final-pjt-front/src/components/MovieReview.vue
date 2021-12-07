<template>
  <div>
    <b-container style="position: relative; top: 50px">
      <h3 class="mb-5 text-start text-white">리뷰</h3>
      <b-row cols="2">
        <div
          v-for="review in reviews"
          :key="review.id"
          class="d-flex justify-content-center"
        >
          <MovieReviewItem
            :review="review"
          />
        </div>
      </b-row>
      <b-spinner v-if="loading" variant="success" label="Spinning"></b-spinner>
      <p v-if="reviews.length === 0" style="text-align: center;color: darkgreen; mt-3; font-weight: bold">표시할 리뷰가 없습니다.</p>
      <p v-if="none && reviews.length !== 0" style="text-align: center;color: darkgreen; mt-3; font-weight: bold">표시할 리뷰가 없습니다.</p>
    </b-container>
    
  </div>
</template>

<script>

import { mapState } from 'vuex'
import axios from 'axios'
import MovieReviewItem from '@/components/MovieReviewItem'
export default {
  name: 'MovieReview',
  props: {
    movieId: {
      type: String,
    }
  },
  components: {
    MovieReviewItem
  },
  computed: {
    ...mapState([
      'loading',
    ])
  },
  data: function () {
    return {
      reviews: [],
      pageNum: 2,
      none: false,
    }
  },
  created () {
    // window 에서 scroll event 발생 시 handleScroll method 실행시킴
    window.addEventListener('scroll', this.handleScroll);
    // axios
    axios({
      method: 'get',
      url: `http://localhost:8000/community/${this.movieId}/?page=1`,
    })
      .then(response => {
        this.reviews = response.data
      })
      .catch(error => {
        console.log(error)
      })
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
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
            url: `http://localhost:8000/community/${this.movieId}/?page=${this.pageNum}`,
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
  }
}
</script>

<style>

</style>