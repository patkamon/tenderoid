<script setup>
import { useStore } from '@/stores/app';
import { storeToRefs } from 'pinia';
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router'

const route = useRoute()
const { bio } = storeToRefs(useStore());
const {getImg, fetchBio} = useStore();
const isBlocked = useStore(false);


onMounted(async () => {
  bio.value = await fetchBio(route.params.id);
  });
  isBlocked.value = false;
  const messages = ref([]);
  const message = ref("");
  const websocket = ref(null);
  const typing = ref(false);

  // WebSocket setup
  const connectWebSocket = () => {
    // Check if there's already an open WebSocket connection
    if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {
      return; // Connection is already open, no need to reconnect
    }

    // Connect to WebSocket server
    websocket.value = new WebSocket("ws://localhost:8000/ws/" + route.params.id);

    websocket.value.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    websocket.value.onmessage = (event) => {
      // Push received messages to the messages array
      const obj = JSON.parse(event.data)
      messages.value.push(obj);
      typing.value = false;
      if (obj.msg.includes('block')){
        isBlocked.value = true;
      }else if (obj.msg.includes('BLOCK')){
        isBlocked.value = true;
      }
    };

    websocket.value.onerror = (error) => {
      console.log("WebSocket error", error);
    };

    websocket.value.onclose = () => {
      console.log("WebSocket connection closed");
      // Automatically try to reconnect after 3 seconds
      setTimeout(() => {
        console.log("Reconnecting...");
        messages.value = []; // Clear the messages array when the connection is closed
        connectWebSocket();
      }, 3000);
    };
  };

  // Send message to WebSocket
  const sendMessage = () => {
    if (message.value && websocket.value && websocket.value.readyState === WebSocket.OPEN && !isBlocked.value) {
      websocket.value.send(message.value);
      messages.value.push({"id":1, "isUser": 'True', "msg": message.value, "time": 'now'}); // Add the sent message to the messages array
      message.value = ""; // Clear the input after sending
      typing.value = true; 
    } else {
      alert("Cannot send message, WebSocket is not open or maybe you are blocked!!");
    }
  };

  // Lifecycle hooks
  onMounted(() => {
    connectWebSocket(); // Open WebSocket connection when the component is mounted
  });

  onBeforeUnmount(() => {
    if (websocket.value) {
      websocket.value.close(); // Close WebSocket when the component is unmounted
    }
  });
  
</script>

<template>


    <div id="chat" class="flex flex-col h-full min-h-[90vh]">
  <!-- Chat Messages Section -->
   <RouterLink :to="'/bio/'+ $route.params.id" class="sticky top-14">
     <img v-bind:src="getImg(bio.img1)" class="lg:w-24 m-4 lg:h-24 w-12 h-12  rounded-full" /> 
    </RouterLink>

  <template v-if="messages.length ==0">
    <div class="h-[50vh] flex justify-center items-center">
      <div class="flex items-center justify-center h-16 px-4 bg-gray-800 text-white">
        <h1 class="text-2xl text-white">Start the chat with gentle greet!!</h1>
      </div>
    </div>
  </template>

  <template v-else>

<div class="text-white">
</div>
  <div class="flex-1 overflow-y-auto p-4">
    <div v-for="(c, index) in messages" :key="index" class="mb-4">
      <div :class="[
        'flex gap-4 items-center w-fit',
        c.isUser == 'True' ? 'ml-auto bg-white text-black' : 'mr-auto max-w-[80%] bg-red-500 text-white'
      ]">
        <div class="flex items-center p-2 rounded-2xl">
          <span class="text-sm">{{ c.msg }}</span>
        </div>
      </div>
    </div>

    <div v-if="typing" class="flex gap-4 items-center w-fit mr-auto max-w-[80%] bg-red-500 p-2 text-white">
      <div class="w-2.5 h-2.5 bg-white rounded-full animate-bounce-1"></div>
      <div class="w-2.5 h-2.5 bg-white rounded-full animate-bounce-2"></div>
      <div class="w-2.5 h-2.5 bg-white rounded-full animate-bounce-3"></div>
    </div>
  </div>
</template>


  <!-- Input Box Section -->
  <div  class="bg-white p-4 mb-14 flex items-center justify-between border-t border-gray-300">
    <input
      v-model="message"
      @keyup.enter="sendMessage"
      type="text"
      placeholder="Type a message..."
      class="w-full p-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
    />
    <button
      @click="sendMessage"
      class="ml-3 bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition duration-200"
    >
      Send
    </button>
  </div>


</div>


</template>


<style scoped>
@keyframes bounce1 {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

@keyframes bounce2 {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

@keyframes bounce3 {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

/* Applying animation with different delays for each dot */
.animate-bounce-1 {
  animation: bounce1 1.5s infinite;
}

.animate-bounce-2 {
  animation: bounce2 1.5s infinite;
  animation-delay: 0.2s; /* Delay the second dot */
}

.animate-bounce-3 {
  animation: bounce3 1.5s infinite;
  animation-delay: 0.4s; /* Delay the third dot */
}
</style>