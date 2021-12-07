<template>
    <div class="review-list">
      <b-modal
      :id="`${review.id}`"
      size="xl"
      scrollable
      centered
      hide-footer
      header-bg-variant="white"
      body-bg-variant="white"
    >
      <template #modal-title>
        {{reviewer}} 님의 리뷰
      </template>
      <!-- 리뷰 내용 -->
      <template>
        <div v-if="isLogin">
            <div class="d-flex justify-content-between align-items-center">
              <h2 class="fw-bold" style="margin: 0px;">{{ review.title }}</h2>
              <div class="me-2">
                <i class="far fa-star fw-bold" style="font-size: 20px;"> {{ review.rank }}</i>
              </div>
            </div>
   
          <p style="font-size: 30px;">{{ review.content }}</p>

        </div>
        <div v-else>
          <p>리뷰를 보려면 로그인해야합니다.</p>
        </div>
      </template>

      <!-- 좋아요, 댓글 개수 표시 -->

      <template>
        <div class="d-flex justify-content-between">
          <div class="d-flex align-items-center">
            <div
              @click="clickLike(review.id)"
            >
              <b-link class="link-success" v-show="likeState"><i class="far fa-heart fw-bold" style="font-size: 20px;"> {{ likeCount }}</i></b-link>
              <b-link class="link-secondary" v-show="!likeState"><i class="fas fa-heart fw-bold" style="font-size: 20px;"> {{ likeCount }}</i></b-link>
            </div>

            <div>
              <i class="fas fa-comment fw-bold mx-3" style="font-size: 20px;"> {{ comments.length }}</i>
            </div>
          </div>
          <div class="d-flex justify-content-end" v-if="getUserId">
            <b-btn
              variant="success"
              class="mx-3"
              v-if="getUserId === review.user"
              @click="updateReview"
              size="md"
            >수정
            </b-btn>
            <b-btn
              variant="danger"
              v-if="getUserId === review.user"
              @click="deleteReview"
              size="md"
            >
              삭제
            </b-btn>
          </div>
        </div>
        <hr> 
      </template>

      <!-- 댓글 목록 -->
      <template v-if="comments.length !== 0">
        <div v-if="getUserId">
        <p style="font-size: 30px;">댓글</p>
        <p
          v-if="!isLogin"
        >
          댓글을 보려면 로그인해야합니다.
        </p>
        <ul>
          <li
            v-for="comment in comments"
            :key="comment.id"
          >
          <span style="font-size: 20px;">
             {{ comment.content }}  
          </span>
          <b-link
            class="mx-2 link-danger text-decoration-none"
            @click="deleteComment(comment.id)"
            v-if="getUserId === comment.user"
          >삭제
          </b-link>
          </li>
        </ul>
        </div>
      <hr>
      </template>

      <template>
        <p style="font-size: 20px;">댓글 작성</p>
        <form> 
          <b-form-textarea
          v-if="isLogin"
          id="textarea"
          v-model="content"
          placeholder="내용을 입력해주세요"
          rows="3"
          max-rows="6"
          ></b-form-textarea>
          <b-form-textarea
          v-else
          id="textarea"
          v-model="content"
          placeholder="댓글 작성을 위해 로그인해주세요"
          rows="3"
          max-rows="6"
          disabled
          ></b-form-textarea>
          <div class="d-flex justify-content-end mt-2">
            <b-button size="md" variant="success" @click="addComment">
            작성
            </b-button>
          </div>
        </form>
      </template>
    </b-modal>    

      <!-- 영화에 대한 전체 reviews 목록 -->
        <div class="card text-white mb-5 text-start" style="background-color: #141414 ;height: 14rem; width: 36rem; max-width: 36rem; border: #142f25 solid 2px">
          <!-- card header -->
          <div class="card-header d-flex justify-content-between">
            <div>
              <i class="far fa-user fw-bold"> {{ this.reviewer }}</i>
            </div>
            <div>
              <i class="far fa-star fw-bold"> {{ review.rank }}</i>
            </div>
          </div>
          <!-- card body -->
          <div
            class="card-body"
            v-b-modal="`${review.id}`"
            @click="getComments(review.id)"
          >
            <h5 class="card-title">{{ review.title }}</h5>
            <p class="card-text">{{ review.content }}</p>
          </div>
          <!-- card footer -->
          <div class="card-footer">
          <i class="far fa-heart fw-bold"> {{ likeCount }}</i>
          </div>
        </div>
      </div>
    
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
export default {
  name: 'MovieReviewItem',
  data: function() {
    return {
      comments: [],
      content: '',
      likeCount: this.review.like_users.length,
      likeState: null,
      reviewer: null,
    }
  },
  props: {
    review: {
      type: Object,
    }
  },
  computed: {
    ...mapGetters([
      'isLogin',
      'getUserId'
    ]),
  },
  methods: {
    getReviewer (userId) {
      axios({
      method: 'get',
      url: `http://localhost:8000/accounts/${userId}/profile/`,
      })
      .then(response => {
        this.reviewer = response.data.username
      })
      .catch(error => {
        alert(error)
      })
    },
    deleteReview () {
      // axios
      axios({
        method: 'delete',
        url: `http://localhost:8000/community/${this.review.id}/reviews/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.accessToken}`
        },
      })
      .then(response => {
        console.log(response)
        alert('리뷰가 삭제되었습니다.')
        // 새로고침
        this.$router.go()
      })
      .catch(error => {
        error
        alert('권한이 없습니다.')
      })
    },
    updateReview () {
      // 수정 요청
      this.$router.push( { name: 'CreateReview', params: { movieId: this.review.movie, reviewId: this.review.id }} )
    },
    clickLike (reviewId) {
      if (this.isLogin) {
        this.likeState = !this.likeState
        console.log(this.likeState)
        // axios 요청
        axios({
          method: 'post',
          url: `http://localhost:8000/community/${reviewId}/review_like/`,
          headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`
          },
        })
          .then(response => {
            if (response.data.liked) {
              // 먼저 likeCount --
              this.likeCount += 1
            } else {
              this.likeCount -= 1
            }
          })
          .catch(error => {
            error
          })

      } else {
        // 로그인하지 않은 상태에서 좋아요를 누를 경우 알림창이 뜨도록 한다.
        alert('로그인 해주세요')
      }
    },
    deleteComment(commentId) {
      axios({
        method: 'delete',
        url: `http://localhost:8000/community/${commentId}/comments/delete/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.accessToken}`
        },
      })
        .then(response => {
          response
          this.getComments(this.review.id)
        })
        .catch(error => {
          error
          alert('본인 댓글만 삭제할 수 있습니다.')
        })
    },
    getComments(reviewId) {
      if (this.isLogin) {
        axios({
          method: 'get',
          url: `http://localhost:8000/community/${reviewId}/comments/`,
          headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`
          },
        })
          .then(response => {
            console.log(response.data)
            this.comments = response.data
          })
          .catch(error => {
            error
            alert('리뷰를 보려면 로그인해주세요')
          })
      }
    },
    addComment() {
      axios({
        method: 'post',
        url: `http://localhost:8000/community/${this.review.id}/comments/`,
        data: {
          content: this.content
        },
        headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`
        },
      })
        .then(response => {
          alert('댓글이 작성되었습니다.')
          response
          this.getComments(this.review.id)
          this.content = ''
        })
        .catch(error => {
          if (error.response.status === 400) {
            alert('내용을 입력해주세요')
          } else {
            alert('댓글 작성을 위해 로그인해주세요')
          }
        })
    }
  },
  created () {
    // 로그인 되었을 때만 좋아요 상태값을 가져온다.
    if (this.isLogin) {
      if (this.review.like_users.includes(this.getUserId)) {
        this.likeState = true
      } else {
        this.likeState = false
      }
    }
    this.getReviewer(this.review.user)
  }
}
</script>

<style>
* {
  font-family: 'Do Hyeon', sans-serif;
}
.card-text {
   overflow: hidden;
   text-overflow: ellipsis;
   white-space: nowrap
}
.close {
  background-color: #dc3545;
  width: 30px;
  height: 30px;
  font-size: 30px;
  border-radius: 4px;
  color: white;
  padding: 0;
  margin: 0;
  border: 2px;
  text-align: center;
  
}
.modal-title {
  font-size: 40px;
}
</style>