<template>
  <div class="tabbed-code">
    <div class="tabs">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        @click="activeTabIndex = index"
        :class="{ active: activeTabIndex === index }"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="content-wrapper">
      <div v-for="(tab, index) in tabs" :key="index" v-show="activeTabIndex === index" class="content">
        <slot :name="tab.slot" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  tabs: {
    type: Array,
    required: true,
  },
});

const activeTabIndex = ref(0);
</script>

<style scoped>
.tabbed-code {
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
  margin-bottom: 0;
}

.tabs button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-bottom: none;
  border-radius: 5px 5px 0 0;
  padding: 8px 16px;
  cursor: pointer;
  outline: none;
  transition: background-color 0.3s;
  color: #333;
}

.tabs button:hover {
  background-color: #e0e0e0;
}

.tabs button.active {
  background-color: #fff;
  border-color: #eee;
  z-index: 1;
  transform: translateY(1px);
  color: #333;
}

.content-wrapper {
  border: 1px solid #ccc;
  border-radius: 0 5px 5px 5px;
  padding: 10px;
  background-color: #fff;
  color: #333;
}

/* 深色模式样式 */
@media (prefers-color-scheme: dark) {
  .tabs button {
    background-color: #3a3a3a;
    border-color: #555;
    color: #e0e0e0;
  }

  .tabs button:hover {
    background-color: #4a4a4a;
  }

  .tabs button.active {
    background-color: #2d2d2d;
    border-color: #666;
    color: #e0e0e0;
  }

  .content-wrapper {
    background-color: #2d2d2d;
    border-color: #555;
    color: #e0e0e0;
  }
}
</style>