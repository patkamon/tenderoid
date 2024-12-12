<script setup>
import { useStore } from '@/stores/app';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

const { allBio} = storeToRefs(useStore());
const {fetchAllBio, getImg} = useStore();

  onMounted(async () => {
    allBio.value = await fetchAllBio();
  });

</script>

<template>
  <div class="flex justify-center overflow-auto h-screen">
    <div class="grid grid-cols-2 gap-x-4 gap-y-2 h-fit ">
      <RouterLink :to="'/bio/'+ bio.id" v-for="bio in allBio" :key="bio.id" class="bg-white p-1 lg:w-64 lg:h-80 h-48 w-36">
        <img v-bind:src="getImg(bio.img1)" class="lg:w-64 lg:h-64 w-36 h-36 " /> 
        <p class="h-12">{{ bio.bio.slice(40,60) }}</p>
      </RouterLink>
    </div>
  </div>
</template>

