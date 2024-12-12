<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Footer from './components/Footer.vue'
import Navbar from './components/Navbar.vue';


</script>

<template>
  <div class="bg-black min-h-screen w-screen flex flex-col">
    <Navbar/>

    <div class="wrapper lg:px-80 px-2 h-full">
      <RouterView />
    </div>

    <footer class="w-full flex justify-center sticky bottom-0">
      <Footer />
    </footer>
   
  </div>

</template>

<style scoped>

</style>
