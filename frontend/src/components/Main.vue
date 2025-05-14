<script setup>
import {onMounted, ref, onBeforeUnmount} from "vue";
import {init_particles} from "@/shared/background_main.js"
import {motion} from "motion-v"
import {skills, services} from "@/shared/lists.js"

const landing = ref(false)
let lastScrollY = window.scrollY;
let settings_icon = null
let settings_icon_rotate = 0

class Rocket {
  constructor() {
    this.x = window.innerWidth / 2
    this.y = window.innerHeight / 2
    this.tx = this.x
    this.ty = this.y
    this.angle = 0
    this.el = document.getElementById("rocket")
    this.animate()
  }

  animate() {
    const dx = this.tx - this.x
    const dy = this.ty - this.y

    this.x += dx * 0.01
    this.y += dy * 0.01
    this.angle = Math.floor(Math.atan2(dy, dx) * 180 / Math.PI) + 90

    if (this.el) {
      this.el.style.top = `${this.y}px`
      this.el.style.left = `${this.x}px`
      this.el.style.rotate = `${this.angle}deg`
    }

    requestAnimationFrame(() => this.animate())
  }
}

onMounted(() => {
  init_particles()
  const rocket = new Rocket()
  settings_icon = document.querySelector(".settings-icon")
  document.body.style.overflowY = "hidden"

  const RocketTransition = e => {
    rocket.tx = e.clientX
    rocket.ty = e.clientY
  }

  window.addEventListener('mousemove', RocketTransition)
  onBeforeUnmount(() => {
    window.removeEventListener('mousemove', RocketTransition)
  })
})

setTimeout(() => {
  document.querySelectorAll('.present-title').forEach(el => {
    el.classList.add('disappearance')
  });
}, 2000)

setTimeout(() => {
  landing.value = true;
  document.body.style.overflowY = "auto";
}, 3000)

function ScaleForScroll(el) {
  const lst_li = el.children;
  const rect = el.getBoundingClientRect();

  const currentScrollY = lst_li[0].getBoundingClientRect().top
  if (currentScrollY > lastScrollY) {
    settings_icon.style.transform = `rotate(${settings_icon_rotate+=1}deg)`;
  } else if (currentScrollY < lastScrollY) {
    settings_icon.style.transform = `rotate(${settings_icon_rotate-=1}deg)`;
  }
  lastScrollY = currentScrollY;

  for (let i = 0; i < lst_li.length; i++) {
    const itemRect = lst_li[i].getBoundingClientRect();

    const isFullyVisible =
        itemRect.top >= rect.top &&
        itemRect.bottom <= rect.bottom;

    if (isFullyVisible) {
      lst_li[i].classList.add('scale-anime-not-visible');
    } else {
      lst_li[i].classList.remove('scale-anime-not-visible');
    }
  }
}
</script>

<template>
  <canvas id="canvas"></canvas>
  <div id="present_block">
    <div v-if="!landing" class="group">
      <h1 data-aos="zoom-in-down" data-aos-delay="500" data-aos-duration="1000" class="title present-title" style="margin: 0;">Узнай все события из космоса</h1>
      <h1 data-aos="zoom-out" data-aos-delay="500" data-aos-duration="1000" class="title present-title">вместе с CaSpace 🚀</h1>
      <h2 data-aos="zoom-out-up" data-aos-delay="500" data-aos-duration="1000" class="subtitle present-title"><i>Листай и узнавай</i></h2>
    </div>
    <div data-aos="fade-left" data-aos-duration="1000" v-if="landing" class="calendar">
      <motion.div class="calendar__el" v-for="i in 31" :key="i"
      :whileHover="{ scale: 1.1 }" :whilePress="{ scale: 0.95 }">
          <h2 class="subtitle">{{ i }}</h2>
      </motion.div>
    </div>
    <div v-if="landing" data-aos="zoom-in" data-aos-duration="1000" class="present-title__text">
      <h1 class="title" style="margin-top: 0">Немного о CaSpace</h1>
      <p class="text-center description">
        Мы создали умную платформу, которая автоматически отслеживает все значимые космические события: от запусков спутников до редких затмений
      </p>
    </div>
    <motion.div v-if="landing" :initial="{ opacity: 0, y: 150 }" :while-in-view="{ opacity: 1, y: 0 }" :transition="{ duration: 1 }"  class="scroll-hint">
      <img src="../assets/down.svg" alt="" class="scroll-hint_img">
    </motion.div>
  </div>

  <motion.div id="rocket" class="rocket-wrapper"
  :initial="{ opacity: 0, display: 'block', x: 200, y: 200, rotate: -90 }"
  :animate="{opacity: 1, x: 0, y: 0, rotate: 0 }"
  :transition="{ duration: 1, delay: 2.5}">
    <div class="rocket"></div>
    <div class="flame"></div>
  </motion.div>

  <div id="advantages_block" class="landing-section">
    <motion.div
        class="title w-100"
        :initial="{ opacity: 0, y: -50 }"
        :while-in-view="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.6, ease: 'easeOut' }"
    >Что умеет CaSpace?
    </motion.div>

    <div class="scroll m-40 flex flex-col gap-8">
      <motion.div
          v-for="(skill, i) in skills"
          :key="i"
          class="list__block scroll-x__el p-6 rounded-xl shadow-md bg-white"
          :initial="{ opacity: 0, y: 100 }"
          :while-in-view="{ opacity: 1, y: 0 }"
          :transition="{ duration: 0.5, delay: i * 0.1, ease: 'easeOut' }"
          viewport="{ once: true }"
      >
        <h2 class="list__block_el subtitle w-100">{{ skill.title }}</h2>
        <p class="list__block_el description">{{ skill.description }}</p>
      </motion.div>
    </div>
  </div>

  <div id="service_block" class="landing-section">
    <motion.div class="title w-100"
    :initial="{ opacity: 0, y: 100}" :while-in-view="{ opacity: 1, y: 0 }" :transition="{ duration: .5}"
    >
      Преимущества нашей платформы</motion.div>
    <div class="list m-40">
      <motion.div
          v-for="(service, i) in services"
          :key="i"
          class="list__block"
          :initial="{ opacity: 0, x: i % 2 === 0 ? -50 : 50, y: i % 2 === 0 ? -50 : 50 }"
          :while-in-view="{ opacity: 1, x: 0, y: 0 }"
          :transition="{ duration: 0.6, delay: i * 0.1, ease: 'easeOut' }"
          viewport="{ once: true }"
      >
        <h2 class="list__block_el subtitle">{{ service.title }}</h2>
        <p class="list__block_el description">{{ service.description }}</p>
      </motion.div>
    </div>
  </div>

  <div id="services-detail_block" class="landing-section">
    <motion.div
    class="title w-100 loading"
    :initial="{ opacity: 0, y: -50 }"
    :while-in-view="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.6, ease: 'easeOut' }">
      <span class="settings-icon">⚙️</span>Рассмотрим детальнее
    </motion.div>
    <motion.ol class="push scroll-list" @scroll="ScaleForScroll($event.target)"
               :initial="{ opacity: 0, y: 100 }"
               :while-in-view="{ opacity: 1, y: 0 }"
               :transition="{ duration: 0.6, ease: 'easeOut', delay: .5}">
      <li class="scale-anime scale-anime-not-visible">
        <h1 class="subtitle">Спутники</h1>
        <p class="description">С помощью этого сервиса вы легко узнаете, какая цель запуска данного спутника, его местоположение и много другого. Мы отслеживаем предстоящие старты и окончание миссий, чтобы вы всегда были в курсе самых свежих и важных новостей из мира орбитальных технологий. Всё это — в одном месте, без лишнего поиска.</p>
        <button class="btn-more">Узнать больше</button>
      </li>
      <li class="scale-anime">
        <h1 class="subtitle">Календарь</h1>
        <p class="description">Благодаря данному сервису вы сможете посмотреть узнать какая планета прямо напротив вас, какие созвездия вы можете посмотреть, когда начнётся полнолуние и много остальной не менее интересной информации</p>
        <button class="btn-more">Узнать больше</button>
      </li>
      <li class="scale-anime">
        <h1 class="subtitle">Миссии</h1>
        <p class="description">Этот сервис поможет вам ознакомиться с актуальными новостями касательно космических миссий и операций, запусков спутников и многого прочего. Также вы сможете узнать ход миссии и её результат</p>
      <button class="btn-more">Узнать больше</button>
      </li>
      <li class="scale-anime b-50" style="margin-bottom: 0">
        <h1 class="subtitle">Подписка на рассылку</h1>
        <p class="description">На нашем сайте вы можете подписаться на рассылку, чтобы получать актуальные уведомления о космических миссиях, событиях, пролётах спутников и о всём остальном, что касается космоса без рекламы и спама</p>
      <button class="btn-more">Узнать больше</button>
      </li>
    </motion.ol>
  </div>

  <div id="mailing_block" class="landing-section">
    <motion.div class="title w-100"
      :initial="{ opacity: 0, y: -50 }"
      :while-in-view="{ opacity: 1, y: 0 }"
      :transition="{ duration: 0.6, ease: 'easeOut'}"
    >Получайте актуальные новости в мире космоса</motion.div>
    <motion.div class="email-form-container m-40"
    :initial="{ opacity: 0, y: 50 }"
    :while-in-view="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.6, ease: 'easeOut'}"
    >
      <form class="email-form">
        <input type="email" placeholder="Введите ваш email" required />
        <motion.button class="btn-continue" type="submit" :whileHover="{ scale: 1.1 }" :whilePress="{ scale: 0.95 }">
        Подписаться</motion.button>
      </form>
    </motion.div>
  </div>

  <div id="author" class="landing-section" style="margin-bottom: 0">
    <motion.div class="description"
    :animate="{
      rotate: [0, 2, -2, 1, -1, 0],
    }"
    :transition="{
      duration: 1.5,
      repeat: Infinity,
      ease: 'easeInOut'
    }"><i>Made by Landik</i></motion.div>
  </div>
</template>

<style>
.group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.present-title {
  width: 90%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
}
</style>