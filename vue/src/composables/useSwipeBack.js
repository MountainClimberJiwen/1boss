import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const EDGE_THRESHOLD_PX = 24
const SWIPE_MIN_DISTANCE = 80
const SWIPE_MAX_VERTICAL = 60
const SWIPE_MAX_DURATION = 500

function isHorizontalScroller(el) {
  if (!el || el === document.body || el === document.documentElement) return false
  const style = window.getComputedStyle(el)
  const overflowX = style.overflowX
  if (overflowX === 'auto' || overflowX === 'scroll' || overflowX === 'hidden') {
    // Only treat as scroller if it actually scrolls (scrollWidth > clientWidth)
    // 'hidden' is included because some elements may use it with touch-scroll
    if (el.scrollWidth > el.clientWidth + 1) return true
  }
  if (el.classList && el.classList.contains('table-wrap')) return true
  return isHorizontalScroller(el.parentElement)
}

export function useSwipeBack() {
  const router = useRouter()

  let startX = 0
  let startY = 0
  let startTime = 0
  let active = false
  let indicatorEl = null

  function createIndicator() {
    const el = document.createElement('div')
    el.className = 'swipe-back-indicator'
    el.style.cssText = `
      position: fixed;
      left: 0;
      top: 0;
      bottom: 0;
      width: 3px;
      background: rgba(255,255,255,0.35);
      transform: translateX(-100%);
      transition: transform 0.08s linear, opacity 0.2s ease;
      opacity: 0;
      z-index: 9999;
      pointer-events: none;
      border-radius: 0 3px 3px 0;
    `
    document.body.appendChild(el)
    return el
  }

  function updateIndicator(deltaX) {
    if (!indicatorEl) indicatorEl = createIndicator()
    const maxWidth = Math.min(window.innerWidth * 0.55, 260)
    const progress = Math.min(deltaX / SWIPE_MIN_DISTANCE, 1)
    const width = 3 + progress * maxWidth
    indicatorEl.style.width = `${width}px`
    indicatorEl.style.transform = 'translateX(0)'
    indicatorEl.style.opacity = String(0.3 + progress * 0.45)
    if (progress >= 1) {
      indicatorEl.style.background = 'rgba(56,189,248,0.6)'
    } else {
      indicatorEl.style.background = 'rgba(255,255,255,0.35)'
    }
  }

  function hideIndicator() {
    if (!indicatorEl) return
    indicatorEl.style.opacity = '0'
    indicatorEl.style.transform = 'translateX(-100%)'
  }

  function canGoBack() {
    // Avoid swipe-back on root pages where there is no sensible parent
    const path = router.currentRoute.value.path
    if (path === '/' || path === '/auth') return false
    // Also require some history stack; on Capacitor WebView history may be shallow
    return window.history.length > 1
  }

  function onTouchStart(e) {
    const t = e.changedTouches[0]
    const edgeLimit = EDGE_THRESHOLD_PX
    if (t.clientX > edgeLimit) return
    if (isHorizontalScroller(e.target)) return

    startX = t.clientX
    startY = t.clientY
    startTime = Date.now()
    active = true
  }

  function onTouchMove(e) {
    if (!active) return
    const t = e.changedTouches[0]
    const dx = t.clientX - startX
    const dy = t.clientY - startY

    if (dx < 0) {
      // moving left; cancel
      active = false
      hideIndicator()
      return
    }

    if (Math.abs(dy) > SWIPE_MAX_VERTICAL) {
      active = false
      hideIndicator()
      return
    }

    if (dx > 4) {
      // prevent default only when we are sure it's a horizontal edge swipe
      // but avoid blocking scrolling of the page itself
      if (e.cancelable) e.preventDefault()
      updateIndicator(dx)
    }
  }

  function onTouchEnd(e) {
    if (!active) return
    active = false
    const t = e.changedTouches[0]
    const dx = t.clientX - startX
    const dy = t.clientY - startY
    const dt = Date.now() - startTime

    hideIndicator()

    if (
      dx >= SWIPE_MIN_DISTANCE &&
      Math.abs(dy) <= SWIPE_MAX_VERTICAL &&
      dt <= SWIPE_MAX_DURATION &&
      canGoBack()
    ) {
      router.back()
    }
  }

  function onTouchCancel() {
    active = false
    hideIndicator()
  }

  onMounted(() => {
    const opts = { passive: false }
    window.addEventListener('touchstart', onTouchStart, { passive: true })
    window.addEventListener('touchmove', onTouchMove, opts)
    window.addEventListener('touchend', onTouchEnd, { passive: true })
    window.addEventListener('touchcancel', onTouchCancel, { passive: true })
  })

  onUnmounted(() => {
    window.removeEventListener('touchstart', onTouchStart)
    window.removeEventListener('touchmove', onTouchMove)
    window.removeEventListener('touchend', onTouchEnd)
    window.removeEventListener('touchcancel', onTouchCancel)
    if (indicatorEl && indicatorEl.parentNode) {
      indicatorEl.parentNode.removeChild(indicatorEl)
    }
  })
}
