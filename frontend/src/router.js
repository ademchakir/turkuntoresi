import { createRouter, createWebHistory } from 'vue-router'
import MathGame from './components/MathGame.vue'
import PuzzleGame from './components/PuzzleGame.vue'
import Home from './components/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/math',
    name: 'MathGame',
    component: MathGame
  },
  {
    path: '/puzzle',
    name: 'PuzzleGame',
    component: PuzzleGame
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
