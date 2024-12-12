import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import DiscoverView from '../views/DiscoverView.vue'
import ChatView from '@/views/ChatView.vue'
import InChatView from '@/views/InChatView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Index,
    },
    {
      path: '/discover',
      name: 'discover',
      component: DiscoverView,
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
    },
    {
      path: '/chat/:id',
      name: 'in-chat',
      component: InChatView,
    },
    {
      path: '/bio/:id',
      name: 'bio',
      component: () => import('../views/BioView.vue'),
    }
  ],
})

export default router
