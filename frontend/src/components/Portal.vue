<template>
  <div class="portal">
    <div>{{ msg }}</div>
    <div>{{ now() }}</div>
  </div>
</template>

<script>
export default {
  name: 'Portal',
  data () {
    return {
      msg: 'Welcome to bbgo'
    }
  },
  methods: {
    now: function () {
      return new Date().toLocaleString()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
