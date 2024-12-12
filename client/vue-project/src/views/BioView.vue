<script setup>
import { useStore } from '@/stores/app';
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';
import Carousel from 'primevue/carousel';
import { useRoute } from 'vue-router';

const { bio } = storeToRefs(useStore());
const images = ref([]);
const {fetchBio, getImg} = useStore();
const route = useRoute()


onMounted(async () => {
  bio.value = await fetchBio(route.params.id);
  console.log(bio.value);

  // loop 5 time
  for (let i = 0; i < 5; i++) {
    if (bio.value['img'+(i+1)].includes('/')) {
      images.value.push({
      img: bio.value['img'+(i+1)]
    });
    }
  }
    console.log(images.value);
});



</script>

<template>
  <main class="h-screen overflow-auto">
    <!-- <img v-bind:src="getImg(bio.img1)"/> -->

    <!-- <template> -->
    <div class="card">
        <Carousel :value="images" :numVisible="1" :numScroll="1" class="text-white" :responsiveOptions="responsiveOptions">
            <template #item="slotProps">
                <div class="border border-surface-200 dark:border-surface-700 rounded m-2 flex justify-center p-4">
                    <div class="mb-4">
                        <div class="relative mx-auto text-white">
                            <img v-bind:src="getImg(slotProps.data.img)" :alt="slotProps.data.name" class="w-full rounded lg:w-96 lg:h-96" />
                        </div>
                    </div>
                </div>
            </template>
        </Carousel>
    </div>

    <p class="text-white p-4 bg-gray-600 opacity-80">
      {{ bio.bio }}
    </p>


  </main>
</template>
