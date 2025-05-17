<script setup>
import {motion} from "motion-v"
import {PostRequest} from "@/shared/requests.js";
import {ref} from 'vue'

let loading = ref(false)
const data = ref(false)
const show = ref(false)
const selectedDate = ref(null)

const openModal = (obj) => {
  if (obj['events'].length > 0) {
    selectedDate.value = obj
    show.value = true
  }
}

const closeModal = (e) => {
  e.classList.add('smooth_disappearance')
  setTimeout(() => {
    e.classList.remove('smooth_disappearance')
    show.value = false
  }, 300)
}

async function sendDate() {
  if (!selectedDate.value) return alert('Выберите дату')
  loading.value = true
  const splitDate = selectedDate.value.split('-', 2)
  const json = JSON.stringify({
    year: splitDate[0],
    month: splitDate[1],
  })
  data.value = await PostRequest(json, 'http://localhost/api/calendar')
  loading.value = false
}
</script>

<template>
  <motion.section v-if="!loading && !data"
  :initial="{ opacity: 0, y: 50 }"
  :while-in-view="{ opacity: 1, y: 0 }"
  :transition="{ duration: 0.6, ease: 'easeOut'}">
    <h1 class="title w-100">Календарь</h1>
    <motion.div class="subtitle w-100 text-center"><i>Выберите дату для просмотра событий</i></motion.div>
    <form class="form m-40" @submit.prevent="sendDate">
      <input type="date" class="form-date" v-model="selectedDate">
      <motion.button class="btn-continue" type="submit" :whileHover="{ scale: 1.1 }" :whilePress="{ scale: 0.9 }">
      Посмотреть</motion.button>
      <br>
    </form>
  </motion.section>

  <section v-if="loading && !data">
    <motion.div class="title w-100 loading"
    :initial="{ opacity: 0, y: -50 }"
    :while-in-view="{ opacity: 1, y: 0 }"
    :transition="{ duration: .6, ease: 'easeOut'}">
      Загрузка
    </motion.div>
  </section>

  <motion.section v-if="data"
  :initial="{ opacity: 0, scale: .8 }"
  :while-in-view="{ opacity: 1, scale: 1 }"
  :transition="{ duration: .6, ease: 'easeOut'}">
    <h1 class="title w-100">Календарь событий</h1>
    <h2 class="subtitle text-center w-100">Просто тыкни: <span style="color: red">красный</span> - нет события, а
      <span style="color: green">зелёный</span> - есть событие</h2>
    <div class="calendar">
      <motion.div class="calendar__el" v-for="i in data" :key="i['num']" @click="openModal(i)"
                  :class="{ 'calendar_box-shadow_red': i['events'].length === 0, 'calendar_box-shadow_green': i['events'].length > 0}"
                  :whileHover="{ scale: 1.1 }" :whilePress="{ scale: 0.95 }">
        <h2 class="subtitle">{{ i['num'] }}</h2>
      </motion.div>
    </div>
  </motion.section>

  <motion.div
      v-if="show"
      class="modal-overlay"
      :initial="{ opacity: 0 }"
      :animate="{ opacity: 1 }"
      :transition="{ duration: 0.3 }"
      @click.self="closeModal($event.target)"
  >
    <motion.div
        class="modal-content"
        :initial="{ scale: 0.8, opacity: 0 }"
        :animate="{ scale: 1, opacity: 1 }"
        :transition="{ duration: 0.3 }"
    >
      <h2 class="subtitle text-center">{{ selectedDate['num'] }} число</h2>
      <div class="blocks_mini" v-for="i in selectedDate['events']">
        <p class="description">{{ i['title'] }}</p>
        <motion.button class="btn-more" :whileHover="{ scale: 1.05 }" :whilePress="{ scale: 0.95 }">
          <a :href="i['link']" class="description" style="padding: 5px">Подробнее</a>
        </motion.button>
        <hr style="margin-top: 20px">
      </div>
    </motion.div>
  </motion.div>
</template>

<style scoped>

</style>