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
**M**ulti**m**odal Evaluation Benchmark

- MME: A Comprehensive Evaluation Benchmark  for Multimodal Large Language Models

- MME-RealWorld: Could Your Multimodal LLM Challenge High-Resolution Real-World Scenarios that are Difficult for Humans?

- Video MME

- etc.

---

# MME

## 着重点：

- 覆盖广, including perception and cognition abilities.

- Avoid data leakage

- Insturciton should be **clear**

- MLLM 的回复应该直观且易于评估

---

# MME

<img src="/images/MME.png" width=85%>

- 同一张图出两道题，groud-truth 分别为 Y N，都对才算对 （防猜）


---

# MME
Data

- Perception
  - Coarse-Grained Recognition. (e.g. count, color, position)
  - Fine-Grained Recognition:  recognizing movie posters, celebrities, scenes, landmarks, and artworks
  - OCR
- Cognition
  - Commensense: basic knowledge in daily life (**zero-shot**)
  - Calculation: 读图中公式（较简单的）
  - 翻译写文本
  - 根据图片生成代码 / debug

---

# MME-RealWorld
Could Your Multimodal LLM Challenge High-Resolution Real-World Scenarios that are Difficult for Humans?

<div class="grid grid-cols-[25%_75%] gap-4">
<div>

MME 难度不够用了

- 全手工
- high res
- contain CN data
- contain reasoning problem
  - 理解全图
  - 看漫画分析人物关系

</div>
<div>

<img src="/images/MME-realworld.png" width=100%>

</div>
</div>

---

# Video MME
900 videos

Question-Answer pair 全是完整看完视频后手动编写并审查过的
<img src="/images/video_mme_1.png" width="66%">

<img src="/images/video_mme_2.png" width="60%">

---

# Aligning and Prompting Everything All at Once for Universal Visual Perception

<img src="/images/alignningatonce.png" width="70%">

GLIP / Grounding DINO $\to$ word-region alignment

- need BERT
- 计算量大

---

# Aligning and Prompting Everything All at Once for ...

## Description Prompting at Scale

- **Independent Prompt** 分开 prompt（忽略上下文关系）$\to$ Llama $\to$ prompt embedding

- **Sentence-level Embeddings** 

  word Level embedding $\to$ sentence level

  $\overline{P_{n,d}}=\frac 1 l \sum^{l}_{j=0}P_{n,j,d}$

  实验证明性能不会发生太大变化 极大减少复杂度

---

# Aligning and Prompting Everything All at Once for ...

## Description Prompting at Scale

- **Gated Cross-modality Interaction** 在 GLIP 基础上：

  - 处理单个词汇：传入全 0 向量 $\overline{P_{zero}}$，不融合，只激发模型微调视觉特征($V_{voc}$) 保留语言特征($P_{voc}$)
  - 处理句子：正常融合（注入 $P_{set}$ 到 $V_{set}$.）

- **Region-sentence Alignment**

  - Object Embedings $\hat{O}$: Score $S=\hat{O} \cdot (\bar{P}_{voc}, \hat{P}_{set})$.
  - 为弥补 Sentence-level embedding 的缺陷加入了不相关的 prompt 作为negative

---

# Aligning and Prompting Everything All at Once for ...

## Thing-stuff-equalizing Alignment

- Things : 可以被识别的物体（例如猫狗）
- Stuff : 无法被识别定型的（如天空草地）

将 stuff 当作 things 处理

- Train ：将大块的 stuff mask 切割（connected-component labeling）成小块, 当作 thing 训练
- Inference :  将被识别为相同类别的东西合并：
  $$\hat{M}_{c,h,w} =\sum_{i=1}^q S_{i,c}M_{i,h,w} $$

---

# Aligning and Prompting Everything All at Once for ...

## Single State Train

$$\mathcal{L} = \underbrace{\mathcal{L}_{\text{class}} + \mathcal{L}_{\text{bbox}} + \mathcal{L}_{\text{giou}}}_{\text{encoder and decoder}} + \underbrace{\mathcal{L}_{\text{mask}} + \mathcal{L}_{\text{dice}}}_{\text{last layer of decoder}}$$

**Train multi-data at once :**

I : an image,

T : a phrase that describes an instance in $I$

B : the corresponding bounding box.


Vallina: $\{I,T,B\}$

Now: $\{I,(T_1,B_1),(T_2,B_2),...,(T_n,B_n)\}$

---

# Thyme