---
theme: seriph
background: https://cover.sli.dev
title: Prof. Fuchaoyou's papers (2024-2025)
info: |
  Prof. Fuchaoyou's papaers.
  Also see in Feishu: https://pcnibbp4qon9.feishu.cn/wiki/GuZfwVTk5iMp8qkzoO2czJNanXb

class: text-center
drawings:
  persist: false
transition: None
mdc: true
---

# Prof. Fu Chaoyou's Papers (2024-2025)

His Homepage: https://bradyfu.github.io/

Slide Outline in [Feishu](https://pcnibbp4qon9.feishu.cn/wiki/GuZfwVTk5iMp8qkzoO2czJNanXb)

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Press Space for next page <carbon:arrow-right />
</div>

<div class="abs-br m-6 text-xl">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="slidev-icon-btn">
    <carbon:edit />
  </button>
  <a href="https://github.com/slidevjs/slidev" target="_blank" class="slidev-icon-btn">
    <carbon:logo-github />
  </a>
</div>

---

# MM-RLHF: The Next Step Forward in Multimodal LLM Alignment

## Dataset : MM-RLHF

- Rich & granular
- 人工审查 / 标记

---

# MM-RLHF

## Critique-Based Reward Model

<img src="/images/MM-RLHF-model.png" width="80%">

- Reward Model (Trained on MM-RLHF)
- Critique Head : 对 prefer 和 less-prefer ansewr 分别生成批评
  - GPT4o 对 ground truth 添加细节后训练
- Scoring head 根据生成的批评打分
  - 用 ground truth 训练

---

# MM-RLHF

## MM-DPO

<img src="/images/MM-DPO.png" width="80%">

- reward model 天然生成 reward margin ($\delta$)

$$\delta = r(y_w)-r(y_l)$$

$r(y_w),r(y_l)$: score of positive and negative samples.

- reward margin 越大 $\beta$ 越大

$$ \beta(\delta)=\beta_{\text{ori}}(1+\omega(1-e^{-k \delta})) $$

---

# Long-VITA: Scaling Large Multi-modal Models to 1 Million Tokens with Leading Short-Context Accuracy

## Train Data

- Comic-9K (Image-Text) (9K个漫画，200K图文对)
- 长视频 (MovieNet Summary)

---

# Long-VITA

## Training

Four Stages:

1. **Vision-Language Alignment**

    -  Freeze LLM & visual encoder , train visual projecter

2. **General Knowledge Learning**

    - Image-text, video, + pure text math & calculation

3. **Long-Sequence Fine-Tuning**

    - 加入更长文本、漫画和视频

4. **Even Longer Sequence Fine-Tuning**

    - 1024K，加入更长的 movie summary data

<!-- 点击时显示的边框 -->
<div v-click="1" v-click-hide="2" class="absolute left-[5%] top-[32%] w-[50%] h-[35%] border-4 border-blue-400 rounded-lg pointer-events-none"></div>

<div v-click="2" class="absolute left-[5%] top-[66%] w-[40%] h-[33%] border-4 border-blue-400 rounded-lg pointer-events-none"></div>

<!-- 点击时显示的右侧说明 -->
<div v-click="1" v-click-hide="2" style="position: absolute; left: 58%; right:5%; top: 30%; border: 3px solid #60a5fa; border-radius: 8px; padding: 1rem; background: rgba(30, 58, 138, 0.2);">

  - pack all training data to a fixed sequence length 
  
  - random sample data from same source, concatenate into one sample , token length = 32K(stage1) / 16K(stage2)

  - Reset positional embeddings & attention masks 
</div>

<div v-click="2" style="position: absolute; left: 58%; right:5%; top: 30%; border: 3px solid #60a5fa; border-radius: 8px; padding: 1rem; background: rgba(30, 58, 138, 0.2);">

  - 同样固定长度
  - 不 reset positional embeddings & attention masks
  - 不使用任何减少参数的方法，例如 LoRA, approximate attention.

</div>

---

# Long-VITA

## Details

- 模型分布在不同 GPU，

- 输入 chunk 以后分布在不同 GPU 计算(对不足 max-tokens 的 input 做 padding)

- Logits-Masked Language Modeling Head
  - 最后一层 $h \cdot W^T$ 只计算最后需要的 next-token ($O(n^2) \rightarrow O(n)$)

---

# MME