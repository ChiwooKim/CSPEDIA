<template>
  <div class="d-flex">
    <div class="container">

      <input 
      type="text" 
      class="form-control me-2" 
      autocomplete="off" 
      aria-label="Search"
      aria-autocomplete="list"
      :value="state"
      @input="filterMovies"
      @keyup.enter="changeList"
      >

      <div class="searchlist" v-if="state" >
        <b-list-group
          v-for="filtermovie in filtermovies" 
          :key="filtermovie"
          @click="goDetail(filtermovie)" >
          <b-list-group-item button>{{ filtermovie }}</b-list-group-item>
        </b-list-group>
      </div>
    </div>
    <button class="btn btn-outline-success" @click="changeList">Search</button>
  </div>
</template>

<script>
import { mapState } from 'vuex'


export default {
  name: 'TheSearchBar',

  data() {
    return {
      state: '',
      filtermovies: [],
    }
  },
  computed: {
    ...mapState([
      'allMovies',
      'moviesTitle',
      'loading'
    ])
  },
  methods: {
    filterMovies(word) {
      this.state = word.target.value
      this.filtermovies = this.moviesTitle.filter( state => {
        return state.startsWith(this.state)
      })
     
    },
    goDetail(name) {
      for (let i of this.allMovies) {
        if (i.title === name) {
          return this.$router.push( {name: 'MovieDetail', params: { movieId: i.id }})
        }
      }
    },
    changeList () {
      if (this.state == false) {
        alert('검색어를 입력하세요.')
      } else {
        this.$emit('change-list', this.filtermovies)
        this.state = ''
        this.filtermovies = []
      }
    },
  },
  created() {
    if (this.allMovies == false) {
      this.$store.dispatch('getSearchMovies')
    }
  },
}

</script>

<style scoped>
input {
  position: relative;
  width: 20rem;
  background: none;
  outline: none;
  border: 1px solid rgba(25, 135, 84);
  line-height: 50px;
  height: 50px;
  box-shadow: 0px 0px 12px rgba(25, 135, 84, 0.18);
  border-radius: 4px;
  font-size: 20px;
  font-weight: bold;
  text-align: left;
}
.searchlist {
  text-align: left;
  width: 20rem;
  height: 200px;
  position: absolute;
  background: none;
  outline: none;
  border-radius: 4px;
  font-size: 19px;
  font-weight: bold;
  overflow-y: auto;
}


</style>