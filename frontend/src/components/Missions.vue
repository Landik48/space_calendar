<script setup>
import {GetRequest} from "@/shared/requests.js";
import {motion} from "motion-v"
import {onMounted, ref} from "vue";

const loading = ref(true)
const data = ref([])

const getData = async () => {
  data.value = await GetRequest('http://localhost/api/missions')
  loading.value = false
}

onMounted(() => {
  getData()
})

</script>

<template>
  <canvas id="canvas"></canvas>
  <section v-if="loading">
    <motion.div class="title w-100 loading"
                :initial="{ opacity: 0, y: -50 }"
                :while-in-view="{ opacity: 1, y: 0 }"
                :transition="{ duration: .6, ease: 'easeOut'}">
      Собираем данные
    </motion.div>
  </section>

  <motion.section v-if="!loading" class="landing-section"
  :initial="{ opacity: 0, y: 50 }"
  :while-in-view="{ opacity: 1, y: 0 }"
  :transition="{ duration: 0.4, ease: 'easeOut'}">
    <h1 class="title w-100">Последние миссии</h1>
    <div class="big-block">
      <motion.div
          v-for="i in data"
      class="list__block big-block__el"
      :initial="{ opacity: 0, scale: .7 }"
      :while-in-view="{ opacity: 1, scale: 1 }"
      :transition="{ duration: 0.4, ease: 'easeInOut'}">
        <h2 class="list__block_el subtitle w-100">{{ i['name'] }}</h2>
        <p class="description w-100">{{i['date']}}</p>
        <p class="description w-100"><i>{{i['info']}}</i></p>
        <p class="description">{{i['description']}}</p>
      </motion.div>
    </div>
  </motion.section>
</template>

<style scoped>

</style>