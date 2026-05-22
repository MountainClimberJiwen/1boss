<template>
  <router-view />
  <!-- Mobile Play Notification -->
  <div v-if="mobilePlayUrl" class="mobile-play-toast" @click="playMobileAudio">
    <div class="mobile-play-content">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      <span>Tap to play daily summary</span>
    </div>
    <button class="mobile-play-dismiss" @click.stop="dismissMobilePlay">&times;</button>
  </div>
  <audio ref="mobileAudioRef" style="display:none;" @ended="onMobileAudioEnded" />
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useSwipeBack } from './composables/useSwipeBack.js'
import { getMobilePlayQueue, ackMobilePlayRequest, getApiBase } from './api.js'

useSwipeBack()

const mobilePlayUrl = ref('')
const mobileRequestId = ref(null)
const mobileAudioRef = ref(null)
let mobilePollInterval = null

async function pollMobilePlayQueue() {
  try {
    const data = await getMobilePlayQueue()
    const requests = data.play_requests || []
    if (requests.length > 0) {
      const req = requests[0]
      if (mobileRequestId.value !== req.id) {
        mobileRequestId.value = req.id
        mobilePlayUrl.value = req.audio_url
      }
    }
  } catch (err) {
    // Silently ignore polling errors
  }
}

function playMobileAudio() {
  if (!mobileAudioRef.value || !mobilePlayUrl.value) return
  const apiBase = getApiBase()
  const url = mobilePlayUrl.value.startsWith('http') ? mobilePlayUrl.value : `${apiBase}${mobilePlayUrl.value}`
  mobileAudioRef.value.src = url
  mobileAudioRef.value.play().catch(() => {})
  if (mobileRequestId.value !== null) {
    ackMobilePlayRequest(mobileRequestId.value).catch(() => {})
  }
  mobilePlayUrl.value = ''
}

function onMobileAudioEnded() {
  mobilePlayUrl.value = ''
  mobileRequestId.value = null
}

function dismissMobilePlay() {
  mobilePlayUrl.value = ''
  if (mobileRequestId.value !== null) {
    ackMobilePlayRequest(mobileRequestId.value).catch(() => {})
  }
}

onMounted(() => {
  pollMobilePlayQueue()
  mobilePollInterval = setInterval(pollMobilePlayQueue, 10000)
})

onUnmounted(() => {
  if (mobilePollInterval) {
    clearInterval(mobilePollInterval)
  }
})
</script>

<style>
.mobile-play-toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.95), rgba(99, 102, 241, 0.95));
  color: white;
  padding: 12px 20px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(12px);
  animation: slideUp 0.4s var(--ease-out-expo);
  cursor: pointer;
  max-width: 90vw;
}
.mobile-play-content {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 14px;
}
.mobile-play-dismiss {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}
@keyframes slideUp {
  from { transform: translate(-50%, 100px); opacity: 0; }
  to { transform: translate(-50%, 0); opacity: 1; }
}
</style>
