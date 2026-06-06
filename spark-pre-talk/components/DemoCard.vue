<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{
  src: string
  demo: string
  label: string
}>()

const open = ref(false)
const base = import.meta.env.BASE_URL.endsWith('/')
  ? import.meta.env.BASE_URL
  : `${import.meta.env.BASE_URL}/`
const publicPrefix = import.meta.env.DEV ? 'public/' : ''

function publicUrl(path: string) {
  if (/^(https?:|data:|blob:)/.test(path)) {
    return path
  }

  if (path.startsWith('./public/')) {
    return `${base}${publicPrefix}${path.slice('./public/'.length)}`
  }

  if (path.startsWith('/')) {
    return `${base}${publicPrefix}${path.slice(1)}`
  }

  return path
}

const imageSrc = computed(() => publicUrl(props.src))
const demoSrc = computed(() => publicUrl(props.demo))

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && open.value) {
    closeDemo()
  }
}

function openDemo() {
  open.value = true
  document.addEventListener('keydown', onKeydown)
}

function closeDemo() {
  open.value = false
  document.removeEventListener('keydown', onKeydown)
}
</script>

<template>
  <figure class="demo-card" @click.stop="openDemo">
    <img :src="imageSrc" />
    <figcaption>{{ label }} <span class="demo-hint">▶ 点击演示</span></figcaption>
  </figure>

  <Teleport to="body">
    <Transition name="demo-fade">
      <div v-if="open" class="demo-overlay" @click.stop>
        <div class="demo-bar">
          <button class="demo-close" @click="closeDemo">
            ← 返回幻灯片
          </button>
          <span class="demo-label">{{ label }}</span>
        </div>
        <iframe :src="demoSrc" class="demo-iframe" />
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.demo-card {
  margin: 0;
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
  background: #111;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  position: relative;
}

.demo-card:hover {
  transform: scale(1.02);
  box-shadow: 0 0 0 2px var(--teal);
}

.demo-card img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  object-position: center;
}

.demo-card figcaption {
  background: var(--ink);
  color: var(--bg);
  padding: 0.45rem 0.7rem;
  font-size: 0.82rem;
  font-weight: 700;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.demo-hint {
  font-size: 0.7rem;
  font-weight: 400;
  opacity: 0.75;
}

/* --- overlay --- */
.demo-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.92);
  display: flex;
  flex-direction: column;
}

.demo-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.6rem 1rem;
  background: rgba(24, 23, 22, 0.9);
  flex-shrink: 0;
}

.demo-close {
  background: var(--teal);
  color: #fff;
  border: none;
  padding: 0.45rem 1rem;
  border-radius: 6px;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s;
}

.demo-close:hover {
  background: #16665f;
}

.demo-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.88rem;
}

.demo-iframe {
  flex: 1;
  width: 100%;
  border: none;
  background: #fff;
}

/* --- transition --- */
.demo-fade-enter-active,
.demo-fade-leave-active {
  transition: opacity 0.2s ease;
}

.demo-fade-enter-from,
.demo-fade-leave-to {
  opacity: 0;
}
</style>
