<template>
  <div class="container text-light text-start">
    <h1 class="my-5">리뷰 작성</h1>
    <b-form @submit="createReview" class="text-success">
      <div class="mb-5">
        <h4>제목</h4>
        <b-form-input v-model="title" placeholder="리뷰 제목을 작성해주세요" style="height: 50px;" ></b-form-input>
      </div>
      <div class="mb-5">
        <h4>내용</h4>
        <b-form-textarea
          id="textarea"
          v-model="content"
          placeholder="리뷰 내용을 작성해주세요"
          rows="3"
          max-rows="6"
          style="height: 200px;"
        ></b-form-textarea>
      </div>
      <div class="mb-5">
        <h4>평점</h4>
        <div class="d-flex">
          <b-form-rating v-model="rank" stars="10" class="text-warning" style="margin-right: auto;"></b-form-rating>
          <button class="btn btn-outline-success justfy-content-end" type="submit">작성</button>
          <!-- <p class="mt-2">{{ rank || 0 }} 점</p> -->
        </div>
      </div>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'CreateReview',
  props: {
    movieId: {
      type: String,
    },
    reviewId: {
      type: Number,
    }
  },
  data() {
    return {
      rank: null,
      content: '',
      title: '',
    }
  },
  methods: {
    createReview (event) {
      event.preventDefault()

      // data 가져오기
      const title = this.title
      const content = this.content
      const rank = Number(this.rank)
      const accessToken = localStorage.getItem('accessToken')

      // 만약 평점을 0점으로 준 경우
      if (rank === 0) {
        alert('평점은 1점 이상이어야 합니다.')
      } else {
        // create or update 판단
        if (this.reviewId) {
              // axios
              axios({
                method: 'put',
                url: `http://localhost:8000/community/${this.reviewId}/reviews/`,
                data: {
                  title,
                  content,
                  rank,
                },
                headers: {
                  Authorization: `Bearer ${accessToken}`
                },
              })
              .then(response => {
                console.log(response)
                alert('리뷰가 수정되었습니다.')
                this.$router.go(-1)
                // this.$router.push( { name: 'MovieDetail', params: { movieId: this.movieId } } )
              })
              .catch(error => {
                error
                alert('내용을 모두 작성해주세요')
              })
        } else {
            // axios
            axios({
              method: 'post',
              url: `http://localhost:8000/community/${this.movieId}/create/`,
              data: [{
                title,
                content,
                rank,
              }],
              headers: {
                Authorization: `Bearer ${accessToken}`
              },
            })
              .then(response => {
                console.log(response)
                alert('리뷰가 작성되었습니다.')
                this.$router.push( { name: 'MovieDetail', params: { movieId: this.movieId } } )
              })
              .catch(error => {
                error
                alert('내용을 모두 작성해주세요')
              })
        }
      }
    }
  },
  created () {
    if (this.reviewId) {
      // 기존 내용 불러오기
      axios({
        method: 'get',
        url: `http://localhost:8000/community/${this.reviewId}/reviews/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.accessToken}`
        },
      })
      .then(response => {
        console.log(response)
        // 폼 안에 기존 내용 넣어주기
        this.rank = response.data.rank
        this.content = response.data.content
        this.title = response.data.title
      })
      .catch(error => {
        alert(error)
      })
    }
  }
}
</script>

<style scoped>
.text-warning {
  width: 50%; 
  height: 50px;
}


</style>