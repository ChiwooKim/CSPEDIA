<template>
  <b-container class="my-5">
    <!-- 영화 상세 정보 -->
    <div>
      <MovieInfo
        :movieId="movieId"
      />
    </div>

    <!-- 영화 리뷰 목록 -->
    <div>
      <MovieReview
        :movieId="movieId"
      />
    </div> 

  </b-container>
</template>

<script>
import MovieInfo from '@/components/MovieInfo'
import MovieReview from '@/components/MovieReview'

export default {
  name: 'MovieDetail',
  components: {
    MovieInfo,
    MovieReview,
  },
  props: {
    movieId: {
      type: String,
    }
  },
}

</script>

<style>

</style>