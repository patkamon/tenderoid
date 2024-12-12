import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('app', () => {
  const allBio = ref([])
  const bio = ref({})
  const allChat = ref([])
  const chat = ref([])

  async function fetchAllBio(){
    return await fetch('http://localhost:8000/all-bio')
    .then(response => response.json())
  }

  async function fetchBio(id){
    return await fetch(`http://localhost:8000/get-bio/${id}`)
    .then(response => response.json())
  }

  function getImg(img) {
    if (!img) return;
    return `../../public/${img.slice(2)}`;
  }


  async function fetchAllChat(){
    return fetch('http://localhost:8000/all-chat')
    .then(response => response.json())
  }

  async function fetchChat(id){
    return fetch(`http://localhost:8000/chat/${id}`)
    .then(response => response.json())
  }

  async function sendChat(data){
    return fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
  }

  async function createBio(){
    return fetch('http://localhost:8000/create-bio', {
      method: 'POST',
    })
    .then(response => response.json())
  }

  return { allBio, fetchAllBio, bio, fetchBio, getImg, allChat, fetchAllChat, chat, fetchChat, sendChat, createBio }
})
