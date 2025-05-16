import './assets/form.css'
import './assets/main.css'
import './assets/nav.css'
import './assets/animations.css'
import {createRouter, createWebHistory} from 'vue-router'
import {createApp} from 'vue'
import App from './App.vue'
import Main from './components/Main.vue'
import Satellites from "@/components/Satellites.vue";
import 'aos/dist/aos.css'
import AOS from 'aos'
import Calendar from "@/components/Calendar.vue";
import Missions from "@/components/Missions.vue";

const routes = [
    {
        path: '/',
        component: Main,
    },
    {
        path: '/satellites',
        component: Satellites,
    },
    {
        path: '/calendar',
        component: Calendar,
    },
    {
        path: '/missions',
        component: Missions,
    },
]

const router  = createRouter({
    history: createWebHistory(),
    routes: routes,
    linkActiveClass: 'active-router',
})

const app = createApp(App)
app.mixin({
    mounted () {
        AOS.init()
    }
})
app.use(router)
app.mount('#app')