<script setup>
import {ref, onMounted} from "vue";
import {motion} from "motion-v"

let active_menu = ref(false);
let width_screen = ref(window.innerWidth >= 800);
let nav = null

onMounted(() => {
  nav = document.querySelector("nav");
})

function checkAnime() {
  if (active_menu.value) {
    nav.classList.add("animate-nav-reverse");
    console.log(active_menu.value);
    setTimeout(()=> {
      nav.classList.remove("animate-nav-reverse");
      active_menu.value = !active_menu.value;
      }, 300);
  }
}

window.addEventListener("resize", () => {
  width_screen.value = window.innerWidth >= 800;
})
</script>

<template>
    <img v-show="!active_menu" @click="active_menu = !active_menu" class="burger" src="./assets/burger.svg" alt="">
    <nav class="animate-nav" v-show="active_menu || width_screen">
      <div class="nav__block">
        <img v-show="active_menu" @click="checkAnime()" class="burger cross" src="./assets/cross.svg" alt="">
        <motion.div :class="{'w-100':active_menu}" :whileHover="{ scale: 1.05 }" :whilePress="{ scale: 0.95 }"><RouterLink class="subtitle nav__block_el" to="/">Главная</RouterLink></motion.div>
        <motion.div :class="{'w-100':active_menu}" :whileHover="{ scale: 1.05 }" :whilePress="{ scale: 0.95 }"><RouterLink class="subtitle nav__block_el" to="/satellites">Спутники</RouterLink></motion.div>
        <motion.div :class="{'w-100':active_menu}" :whileHover="{ scale: 1.05 }" :whilePress="{ scale: 0.95 }"><RouterLink class="subtitle nav__block_el" to="/calendar">Календарь</RouterLink></motion.div>
        <motion.div :class="{'w-100':active_menu}" :whileHover="{ scale: 1.05 }" :whilePress="{ scale: 0.95 }"><RouterLink class="subtitle nav__block_el" to="/missions">Миссии</RouterLink></motion.div>
      </div>
    </nav>
  <main>
    <RouterView/>
  </main>
</template>

<style scoped>

</style>
