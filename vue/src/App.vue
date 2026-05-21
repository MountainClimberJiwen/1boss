<template>
  <router-view />
</template>

<script setup>
import { useSwipeBack } from './composables/useSwipeBack.js'

useSwipeBack()
</script>
