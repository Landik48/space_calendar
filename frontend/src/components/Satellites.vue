<script setup>
import {onMounted, ref} from 'vue'
import {GetRequest} from "@/shared/requests.js";
import L from 'leaflet'
import {motion} from "motion-v"
import 'leaflet/dist/leaflet.css'

const loading = ref(true)
const markers = ref([])
const data = ref([])

const getData = async () => {
  data.value = await GetRequest('http://45.90.216.58/api/satellites')
  loading.value = false
}

onMounted(async () => {
  await getData()
  const map = L.map('map').setView([0, 0], 2)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)
  if (data.value.length > 0) {
    data.value.forEach((satellite) => {
      const marker = L.marker([satellite.lat, satellite.lng]).addTo(map)
      marker.bindTooltip(satellite["name"], { permanent: true, direction: 'right' }).openTooltip()
      markers.value.push(marker)
    })
  }
})
</script>

<template>
  <canvas id="canvas"></canvas>
  <section v-if="loading">
    <motion.div class="title w-100 loading"
                :initial="{ opacity: 0, y: -50 }"
                :while-in-view="{ opacity: 1, y: 0 }"
                :transition="{ duration: .6, ease: 'easeOut'}">
      🛰️ Ищем спутники
    </motion.div>
  </section>

  <motion.section v-if="!loading"
  class="title w-100 loading"
  :initial="{ opacity: 0, y: 50, scale: .9 }"
  :while-in-view="{ opacity: 1, y: 0, scale: 1 }"
  :transition="{ duration: .6, ease: 'easeOut'}">
    <h1 class="title" style="margin: 0">Карта спутников</h1>
    <h2 class="subtitle text-center w-100">Актуальное местоположение топ 100 спутников, запущенных за последние 30 дней</h2>
    <div id="map" class="map"></div>
  </motion.section>
</template>