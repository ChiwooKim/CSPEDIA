<template>
<div>
  <input type="radio" name="r" id="radio1" checked style="display: none">
  <input type="radio" name="r" id="radio2" style="display: none">
  <div id="main">
    <!-- 로그인 -->
    <div id="form1">
      <form @submit="login" autocomplete="off">
        <h1 id="heading">Login</h1>
          <br>
          <input
          type="text"
          placeholder="Username"
          v-model="username">
          <input
          type="password"
          placeholder="password"
          v-model="password">
          <input type="submit" value="Login" name="sbmit">
          <div id="lblsup"><label for="radio2">Sign Up</label></div>
      </form>
    </div>

    <!-- 회원가입 -->
    <div id="form2">
      <form @submit="signup" autocomplete="off">
        <h1 id="heading">Sign Up</h1>
        <br>
        <input
          type="text"
          required
          maxlength="50"
          v-model="username"
          placeholder="Username"
        >
 
        <input
          type="email"
          required
          maxlength="100"
          v-model="email"
          placeholder="E-mail"
        >
        <input
          type="password"
          required
          v-model="password"
          placeholder="Password"
        >
        <input
          id="check"
          type="password"
          required
          v-model="passwordConfirmation"
          placeholder="Password Confirmation"
        >
    
        <input type="submit" value="Sign Up" name="submit1" style="postion: relative;">
        <div id="lblsup2"><label for="radio1" style="postion: relative;">Login</label></div>
      </form>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data: function () {
    return {
      username: '',
      password: '',
      passwordConfirmation: '',
      email: '',
    }
  },
  methods: {
    login: function (event) {
      event.preventDefault()
      const payload = {
        username: this.username,
        password: this.password,
      }
      this.$store.dispatch('getToken', payload)
      // this.$store.dispatch('setUserName', payload.username)
    },
    signup: function (event) {
      event.preventDefault()

      const signupData = {
        username: this.username,
        password: this.password,
        password_confirmation: this.passwordConfirmation,
        email: this.email,
      }
      
      axios({
        method: 'post',
        url: 'http://localhost:8000/accounts/signup/',
        data: signupData,
      })
        .then(response => {
          const username = response.data.username
          alert(`${username}님, 회원가입이 완료되었습니다.`) 
        })
        .catch(error => {
          alert('잘못된 양식입니다.')
          console.log(error)
        })
      this.username=''
      this.email=''
      this.password=''
      this.passwordConfirmation=''
    },
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap');
* {
  padding: 0px;
  margin: 0px;
  box-sizing: border-box;
  font-family: 'Do Hyeon', sans-serif;
}
#main {
  position: absolute;
  width: 400px;
  height: 350px;
  box-shadow: 0px 0px 30px rgba(25, 135, 84, 60);
  top: calc(50% - 175px);
  left: calc(50% - 200px);
  border-radius: 20px;
  background-color: white;
  overflow: hidden;
  transition: 0.6s cubic-bezier(.78, -0.2, .42, 1.45);
}
#heading {
  position: absolute;
  width: 100%;
  text-align: center;
  line-height: 80px;
  color: black;
  text-shadow: 2px 2px 6px rgba(25, 135, 84, 0.35);
}
input {
  position: relative;
  background: none;
  outline: none;
  border: 1px solid rgba(25, 135, 84, 0.5);
  line-height: 50px;
  height: 50px;
  box-shadow: 0px 0px 12px rgba(25, 135, 84, 0.18);
  width: 80%;
  border-radius: 25px;
  font-size: 19px;
  font-weight: bold;
  text-align: center;
}
input[type=text] {
  top: 70px;
}
input[type=password] {
  top: 90px;
}
input[type=submit] {
  top: 110px;
  box-shadow: 0px 0px 10px rgba(25, 135, 84, 0.23);
  background-image: linear-gradient(rgba(25, 135, 84, 0.46), rgba(25, 135, 84, 0.19));
  color: black;
  cursor: pointer;
}
#form2 input[type=text] {
  top: 70px;
}
#form2 input[type=email] {
  top: 90px;
}
#form2 input[type=password] {
  top: 110px;
}
#form2 #check {
  top: 130px;
}
#form2 input[type=submit] {
  top: 150px;
  box-shadow: 0px 0px 10px rgba(25, 135, 84, 0.23);
  background-image: linear-gradient(rgba(25, 135, 84, 0.46), rgba(25, 135, 84, 0.19));
  color: black;
  cursor: pointer;
}
#lblsup {
  position: relative;
  width: 100%;
  text-align: center;
  top: 120px;
  font-size: 22px;
  font-weight: bolder;
}
#lblsup label {
  cursor: pointer;
}
#lblsup2 {
  position: relative;
  width: 100%;
  text-align: center;
  top: 160px;
  font-size: 22px;
  font-weight: bolder;
}
#lblsup2 label {
  cursor: pointer;
}
#radio2:checked ~ #main #form1{
  transform: translateY(500px);
}
#radio2:checked ~ #main #form2{
  transform: translateY(0px);
}
#radio2:checked ~ #main {
  height: 500px;
  top: calc(50% - 300px);
}
#form1 {
  position: absolute;
  transform: 0.8s ease;
  width: 400px;
}
#form2{
  position: absolute;
  transform: translateY(-500px);
  transition: 0.8s ease;
}
#form1:checked ~ #main #form2{
  transform: translateY(-500px);
}


</style>