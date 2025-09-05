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
}

.tabs button:hover {
  background-color: #e0e0e0;
}

.tabs button.active {
  background-color: #fff;
  border-color: #fff;
  z-index: 1;
  transform: translateY(1px);
}

.content-wrapper {
  border: 1px solid #ccc;
  border-radius: 0 5px 5px 5px;
  padding: 10px;
  background-color: #fff;
}
</style>