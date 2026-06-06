<template>
  <div class="benchmark-title-row">
    <h1>Harness 带来的性能影响</h1>
    <div class="benchmark-tabs" role="tablist" aria-label="Benchmark source">
      <button
        type="button"
        :class="{ active: activeTab === 'code-edit' }"
        role="tab"
        :aria-selected="activeTab === 'code-edit'"
        @click="activeTab = 'code-edit'"
      >
        code edit format benchmark
      </button>
      <button
        type="button"
        :class="{ active: activeTab === 'terminal-bench' }"
        role="tab"
        :aria-selected="activeTab === 'terminal-bench'"
        @click="activeTab = 'terminal-bench'"
      >
        terminal-bench@2.0
      </button>
    </div>
  </div>

  <div class="benchmark-embed-slide">
    <div
      ref="benchmarkContainer"
      class="benchmark-pane benchmark-custom-host"
      :class="{ active: activeTab === 'code-edit' }"
      :aria-hidden="activeTab !== 'code-edit'"
    />
    <iframe
      class="benchmark-pane"
      :class="{ active: activeTab === 'terminal-bench' }"
      :aria-hidden="activeTab !== 'terminal-bench'"
      src="https://www.tbench.ai/leaderboard/terminal-bench/2.0"
      title="terminal-bench@2.0 leaderboard"
      loading="eager"
      referrerpolicy="no-referrer-when-downgrade"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

const benchmarkScript = 'https://blog.can.ac/benchmark/benchmark_v2.js'
const tbenchOrigin = 'https://www.tbench.ai'
const activeTab = ref<'code-edit' | 'terminal-bench'>('code-edit')
const benchmarkContainer = ref<HTMLElement | null>(null)

function addPreconnect(href: string) {
  const selector = `link[rel="preconnect"][href="${href}"]`
  if (document.querySelector(selector)) return

  const link = document.createElement('link')
  link.rel = 'preconnect'
  link.href = href
  document.head.appendChild(link)
}

function loadBenchmarkScript() {
  if (customElements.get('benchmark-embed')) return

  const existing = document.querySelector<HTMLScriptElement>(
    `script[src="${benchmarkScript}"]`,
  )
  if (existing) return

  const script = document.createElement('script')
  script.src = benchmarkScript
  script.defer = true
  document.head.appendChild(script)
}

function mountBenchmark() {
  const container = benchmarkContainer.value
  if (!container || container.querySelector('benchmark-embed')) return

  container.appendChild(document.createElement('benchmark-embed'))
}

onMounted(() => {
  addPreconnect(tbenchOrigin)
  loadBenchmarkScript()
  mountBenchmark()
})
</script>
