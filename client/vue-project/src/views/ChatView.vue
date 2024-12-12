<script setup>
import { useStore } from '@/stores/app';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

const { allChat} = storeToRefs(useStore());
const {fetchAllChat, getImg} = useStore();

  onMounted(async () => {
    allChat.value = await fetchAllChat();
  });

</script>

<template>
  <div class="flex flex-col gap-4 h-screen mt-12">
    <RouterLink :to="'/chat/'+ bio.id" v-for="bio in allChat"  :key="bio.id" class="border border-white p-1 w-full lg:h-28 h-20 rounded-3xl flex gap-4 items-center">
        <img v-bind:src="getImg(bio.img1)" class="lg:w-24 lg:h-24 w-16 h-16  rounded-full" /> 
        <p :class="[bio.isUser == 'False' ? 'text-white truncate' : 'text-gray-400 text-ellipsis overflow-hidden']"> {{ bio.msg }} </p>
      </RouterLink >
    </div>
</template>
