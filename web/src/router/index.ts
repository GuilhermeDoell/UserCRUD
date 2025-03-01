import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/MainView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: '/main',
            component: MainView,
        },
        {
            path: '/users/:id',
            name: 'userDetails',
            component: () => import('../views/UserDetails.vue'),
        },
    ],
})

export default router
