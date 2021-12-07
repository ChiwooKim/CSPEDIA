import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import MovieDetail from '../components/MovieDetail.vue'
import CreateReview from '../components/CreateReview'
import Profile from '../views/Profile'
import RandomMovies from '../views/RandomMovies'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/detail/:movieId',
    name: 'MovieDetail',
    component: MovieDetail,
    props: true,
  },
  {
    path: '/review/:movieId/:reviewId',
    name: 'CreateReview',
    component: CreateReview,
    props: true,
  },
  {
    path: '/profile/:userId',
    name: 'Profile',
    component: Profile,
    props: true,
  },
  {
    path: '/RandomMovies/',
    name: 'RandomMovies',
    component: RandomMovies,
  }
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
