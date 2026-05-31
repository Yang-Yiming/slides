---
theme: seriph
title: Spark Project 2
info: |
  Project 2 presentation generated from final-report/final.tex.
class: deck
transition: fade
drawings:
  persist: false
mdc: true
duration: 18min
fonts:
  sans: Inter, "Noto Sans SC"
  serif: "Noto Serif SC"
layout: default
---

# Project 2

<div class="subtitle">Data Agent 微调 & 舌诊 AI 商业与架构</div>

<div class="hero-grid">
  <div>
    <div class="eyebrow">Q1</div>
    <h2>从 DataMind-12K 筛选数据，微调 Data Agent。</h2>
  </div>
  <div>
    <div class="eyebrow">Q2</div>
    <h2>创业想法 : AI 舌诊。</h2>
  </div>
</div>

<div class="footer">12411332 杨一鸣</div>

<!--
老师好，我来做这次 project 的汇报
-->

---

# 目录

<div class="toc-grid">
  <div class="toc-index">01</div>
  <div>
    <h2>Data Agent System</h2>
    <p>数据选择方法（IFD / DEITA / InstructDiff）→ 数据处理与分层抽样 → LoRA 微调 → 本地 Demo 部署</p>
  </div>
  <div class="toc-index">02</div>
  <div>
    <h2>Startup Business Plan</h2>
    <p>商业计划书 & 架构设计</p>
  </div>
</div>

<!--
Q1 工作链路：先读数据选择相关综述，说明三种方法；再写 Python 从 datamind_12k.json 筛出 2500 条，并按 level + length_bucket 分层抽样分出 2000 条训练 + 500 条验证集；然后用 Ray Train + LoRA 微调 Qwen/Qwen3.5-0.8B；最后本地部署并扩展了 Qwen 官方 web demo。Q2 分商业计划和系统架构两大块：BP 从 LLM 提示词推导到完整商业计划书；架构从目标指标到七层工业级设计，再到高并发、监控运维、安全部署。
-->

---
layout: section
---

# Q1

## Data Agent System

<!--
第一题，训练 data agent
-->

---

# Q1 题目要求

<div class="detail-list">
  <div><b>系统目标</b><span>构建 Data Agent，通过自然语言数据分析。</span></div>
  <div><b>训练数据</b><span>DataMind-12K</span></div>
  <div><b>数据选择</b><span>阅读数据选择相关综述，说明三种适合数据科学和数学建模任务的数据选择方法。</span></div>
  <div><b>数据处理</b><span>从 datamind_12k.json 中筛选 2000 条训练样本和 500 条验证样本，并整理为 Qwen 训练格式。</span></div>
  <div><b>模型训练</b><span>使用 Ray Train 对 Qwen/Qwen3.5-0.8B 进一步微调。</span></div>
  <div><b>本地 Demo</b><span>在本地部署模型并准备网页 Demo，验证 Data Agent 交互链路。</span></div>
</div>

<!--
Q1 的核心目标是做一个生成式 Data Agent 系统，让不会编程或数据科学的用户，通过自然语言提示 LLM，也能获得数据分析流程、数学问题抽象和预测模型。训练数据来自 DataMind-12K。本题包含四个部分：先读数据选择相关综述并说明三种适合数据科学和数学建模的数据选择方法；然后写 Python 从 datamind_12k.json 筛出 2000 条训练样本和 500 条验证样本，整理为 Qwen 训练格式；再用 Ray Train 微调 Qwen/Qwen3.5-0.8B；最后本地部署并准备网页 Demo。
-->

---

# 数据选择方法

<div class="three-col-detail">
  <div>
    <h2>IFD</h2>
    <p>量化指令跟随难度，找"指令真正起作用"的样本。</p>
    <strong>有无指令时的生成概率差</strong>
  </div>
  <div>
    <h2>DEITA</h2>
    <p>质量、复杂度、多样性三维综合评分 + 贪心向量过滤。</p>
    <strong>最佳三个维度独立调节</strong>
  </div>
  <div>
    <h2>InstructDiff</h2>
    <p>比较 base model 和 warm-up 后模型在每条数据上的输出差异。</p>
    <strong>哪些样本带来的变化最大</strong>
  </div>
</div>

<!--
SFT阶段，数据质量远比数据数量重要。
在数据科学和数学建模领域，需要在三个方面实现平衡：质量、多样性、复杂度。
我找到了三个方法：IFD，DEITA和InstructDiff
-->

---

# IFD：Instruction-Following Difficulty

<div class="two-col compact">
  <div>
    <h2>核心假设</h2>
    <p>模型在有无指令条件下输出概率差异最大的样本最具学习价值。</p>
 
$$ \text{IFD} = \frac{\log P(\text{model}(x)) - \log P(\text{model}(x, \text{instruction}))}{\log P(\text{model}(x))} $$

  </div>
  <div>
    <h2>流程</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>预热</td><td>随机采样 5%-10%，初步微调基础 LLM 以获指令理解能力。</td></tr>
      <tr><td>评分</td><td>用预热模型计算每条数据的 IFD 分数。</td></tr>
      <tr><td>选择</td><td>按阈值或排序保留高价值样本。</td></tr>
      </tbody>
    </table>
  </div>
</div>

<div class="note">IFD 寻找模型的"最近发展区"：太难则 IFD 低（有指令也答不对）；太简单则 IFD 接近 1（无需指令也能答对）。</div>

<!--
IFD 的核心是量化指令跟随难度。
它比较模型在有无指令条件下生成目标输出的概率差异。
样本太难，有指令也答不对，没有学习价值
样本太简单，不需要指令也能答对，也没学习价值

最值得训练的是"指令真正起作用"的样本。这个逻辑和教育心理学中的最近发展区类似，用在数学推理和数据分析任务上比较自然。

具体是这么算的
-->

---

# DEITA：综合质量、复杂度、多样性

<div class="detail-list">
  <div><b>复杂度评分</b><span>树状指令结构节点越多、推理步骤越多，复杂度越高。</span></div>
  <div><b>质量评分</b><span>用奖励模型或大模型评估回答准确性。</span></div>
  <div><b>综合分数</b><span>复杂度 * 质量</span></div>
  <div><b>多样性过滤</b><span>排序后，新样本与已选集合的最近邻距离需超过阈值 τ，保证多样性。</span></div>
  <div><b>优势</b><span>质量、复杂度、多样性三个维度独立解释和调节。打基础阶段侧重质量，上强度阶段侧重复杂度。</span></div>
  <div><b>代价</b><span>需要额外训练复杂度评分器，并依赖模型做质量评估，成本和计算复杂度较高。</span></div>
</div>

<!--
DEITA 分数是复杂度与质量的乘积，再通过贪心距离过滤处理引入多样性。具体流程是
1) 复杂度评分，用 WizardLM 的进化指令技术训练专门的复杂度评分器，树状指令结构的节点数越多，推理步骤越多，复杂度越高。
2) 质量评分，用奖励模型或大模型评估回答的准确性。
3) 综合分数为复杂度与质量的乘积。
4) 多样性感知选择：按综合分排序后，用贪心策略做向量距离过滤，新样本与已选集合的最近邻距离需超过 τ。

DEITA 的优势在于三个维度都可以独立解释和调节，构建训练集时可以针对性地调权重。但代价是成本高。
-->

---

# InstructDiff：模型反馈排序


## 核心直觉

比较**基础模型**和**少量预热微调后模型**在每条数据上的输出差异；差异最大的数据是模型最需要学的。
  

## 两个指标

| | | |
|---|---|---|
| $\Delta\text{NLL}$ | $\mathcal{L}_\text{inst}(x,y)-\mathcal{L}_\text{base}(x,y)$ | 衡量学习信号强度
| $\Delta H$ | $H_\text{base}(x,y)-H_\text{inst}(x,y)$ | 揭示学习模式 |


<div class="note">ΔH 的域自适应特性

数学推理等"认知扩展"任务最优样本 ΔH &lt; 0（不确定性增大，遇新推理模式）；

一般指令遵循为"认知压缩"，最优样本 ΔH &gt; 0。
</div>

<!--
InstructDiff 的核心直觉是比较基础模型和经少量预热微调后模型在每条的输出差异，差异大的数据就是模型最需要学的。
它定义两个指标：
ΔNLL 衡量学习信号强度，ΔH 熵差异揭示学习模式。
关键发现是 ΔH 呈现域自适应的特性：数学推理这类需要"认知扩展"的任务，最优样本的 ΔH < 0，也就是校准后模型不确定性反而增大，说明遇到了新推理模式；
而一般指令遵循需要"认知压缩"，最优样本 ΔH > 0。

另外，它支持用小模型如 Qwen2.5-0.5B 校准来为大模型如 Qwen2.5-7B 选择数据，能达到同尺寸校准 89.8% 的性能，但节省约 14 倍计算量。
-->

---

# 数据处理

<div class="stage-row">
  <div>
    <span>1</span>
    <h3>DEITA 粗筛</h3>
    <p>从 12K 原始数据筛出 4500 条候选。兼顾质量、复杂度和多样性。</p>
  </div>
  <div>
    <span>2</span>
    <h3>IFD 评分</h3>
    <p>使用 Qwen/Qwen3.5-0.8B 给 4500 条数据计算 IFD 分数。</p>
  </div>
  <div>
    <span>3</span>
    <h3>InstructDiff 排序</h3>
    <p>使用 256 条最高质量样本 warm-up LoRA 模型，再与基础模型比较差异。</p>
  </div>
  <div>
    <span>4</span>
    <h3>最终抽样</h3>
    <p>加权综合分数 → 按 level + length bucket 分层抽样 2000/500。</p>
  </div>
</div>

<div class="claim">原始数据为 OpenAI messages 格式，Qwen 原生支持该格式，因此不需要额外做格式转换。</div>

<!--
这是我对 Datamind 12k 数据处理的具体步骤，而且原始数据就是 OpenAI messages 格式，Qwen 在文档里说是原生支持的，所以不用额外的格式转换。
-->

---

# DEITA 粗筛

<div class="formula small">
deita_score = 0.45 × quality + 0.35 × complexity + 0.20 × diversity
</div>

<div class="three-col-detail compact">
  <div>
    <h2>quality</h2>
    <p>检查轨迹是否完整：是否包含 answer/code/interpreter 等关键标签、最终答案非空、无未解决报错。</p>
  </div>
  <div>
    <h2>complexity</h2>
    <p>考虑问题级别、代码块数量、工具调用轮数和总长度。</p>
  </div>
  <div>
    <h2>diversity</h2>
    <p>考虑 filename 稀有度、答案长度分布和近重复问题惩罚；同时做相似问题去重和 filename 平衡。</p>
  </div>
</div>

<div class="claim">最终从 12K 原始数据中筛选出 4500 条候选数据，作为后续 IFD 和 InstructDiff 的基础。</div>

<!--
首先进行了一个简化版的 DEITA 粗筛，从 12K 原始数据里选出了 4500 条候选数据
-->

---

# IFD 评分

<div class="two-col compact">
  <div>
    <h2>计算方式</h2>
    <p>使用 Qwen/Qwen3.5-0.8B 分别计算 loss_with_instruction 和 loss_without_instruction。</p>
    <div class="formula small">ifd_score = loss_without_inst / loss_with_inst</div>
    <p>只在 assistant token 上计算归一化 NLL，避免把用户问题、数据库描述和工具输出计入学习目标。</p>
  </div>
  <div>
    <h2>分布</h2>
    <table class="dense-table">
      <thead><tr><td>min</td><td>median</td><td>mean</td><td>max</td></tr></thead>
      <tbody><tr><td>1.054688</td><td>1.478261</td><td>1.508805</td><td>2.967742</td></tr></tbody>
    </table>
  </div>
</div>

<div class="note">IFD 分数 > 1 说明有指令时模型更容易生成目标轨迹。分数越高代表指令对生成帮助越大。</div>

<!--
然后算 IFD 分数， 使用 Qwen/Qwen3.5-0.8B 作为需要的模型，因为之后微调的就是他。
对 4500 条候选数据计算后，分数最小 1.054，中位数 1.48，均值 1.51，最大 2.97。
-->

---

# InstructDiff 排序

<div class="two-col compact">
  <div>
    <h2>实施方法</h2>
    <p>先用候选集中最高质量的 256 条样本 warm-up 一个 LoRA adapter，然后比较 base model 和 warm-up 后模型在所有候选上的 loss 和 entropy。</p>
  </div>
  <div>
    <h2>分布</h2>
    <table class="dense-table">
      <thead><tr><td>min</td><td>median</td><td>mean</td><td>max</td></tr></thead>
      <tbody><tr><td>0.007646</td><td>0.485497</td><td>0.500000</td><td>0.999800</td></tr></tbody>
    </table>
  </div>
</div>

<div class="note">Agent 轨迹较长，InstructDiff 只作为排序分数，不作为硬过滤条件。warm-up 后 loss 下降明显的样本与指令微调目标更一致。</div>

<!--
InstructDiff 部分，我们先用候选中最高质量的 256 条样本 warm-up 一个 LoRA adapter，然后比较 base model 和 warm-up 后的模型在所有候选样本上的 loss 和 entropy。

最终的分数分布：是最小 0.008，中位数 0.485，均值 0.500000，最大 0.999800。分数越接近 1 表示样本对 warm-up 后的模型变化越大。
-->

---

# 最终选择规则

<div class="split-grid">
  <div>
    <h3>综合分数</h3>
    <div class="formula small">final_score = 0.60 × deita + 0.20 × ifd + 0.20 × instructdiff</div>
  </div>
  <div>
    <h3>选择策略</h3>
    <ul>
      <li>保留所有非 easy 样本</li>
      <li>easy 样本按 final_score 排列补足 2500</li>
      <li>单 filename 最多保留 5 条，防止源单一</li>
      <li>按长度分位数建立 5 个 bucket</li>
      <li>按 level + length_bucket 分层抽样 train/validation</li>
    </ul>
  </div>
</div>

<div class="three-table-grid">
  <div>
    <h2>level</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>easy</td><td>1476</td></tr>
      <tr><td>Highly Complex</td><td>697</td></tr>
      <tr><td>N/A</td><td>246</td></tr>
      <tr><td>Moderate</td><td>40</td></tr>
      <tr><td>Simple</td><td>30</td></tr>
      <tr><td>Complex</td><td>11</td></tr>
      </tbody>
    </table>
  </div>
  <div>
    <h2>长度 bucket</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>len_q0_25</td><td>626</td></tr>
      <tr><td>len_q25_50</td><td>625</td></tr>
      <tr><td>len_q50_75</td><td>617</td></tr>
      <tr><td>len_q75_90</td><td>337</td></tr>
      <tr><td>len_q90_100</td><td>295</td></tr>
      </tbody>
    </table>
  </div>
  <div>
    <h2>整体</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>unique_filenames</td><td>1581</td></tr>
      <tr><td>max_per_filename</td><td>5</td></tr>
      <tr><td>final_score min</td><td>0.669</td></tr>
      <tr><td>final_score median</td><td>0.785</td></tr>
      <tr><td>final_score max</td><td>1.039</td></tr>
      </tbody>
    </table>
  </div>
</div>

<!--
最终对 4500 条数据加权平均三个分数

然后呢，保留所有的非 easy 样本（因为它们数量少）；
2) easy 样本按 final_score 排列补足到 2500 条；
3) 保持单个 filename 最多为 5，防止数据源单一；
4) 按长度的分位数建立 5 个 bucket 分层采样保证长度分布均匀；

最终的 2500 条数据分布是这样
-->

---

# 训练 / 验证集分布

<div class="split-grid">
  <div>
    <h2>训练集（2000）</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>unique_filenames</td><td>1378</td></tr>
      <tr><td>max_per_filename</td><td>4</td></tr>
      <tr><td>final_score median</td><td>0.768</td></tr>
      <tr><td>easy</td><td>1181</td></tr>
      <tr><td>Highly Complex</td><td>558</td></tr>
      </tbody>
    </table>
  </div>
  <div>
    <h2>验证集（500）</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>unique_filenames</td><td>439</td></tr>
      <tr><td>max_per_filename</td><td>3</td></tr>
      <tr><td>final_score median</td><td>0.820</td></tr>
      <tr><td>easy</td><td>295</td></tr>
      <tr><td>Highly Complex</td><td>139</td></tr>
      </tbody>
    </table>
  </div>
</div>

<div class="note">分层抽样保证两个数据集的 level 比例、长度分布和 filename 覆盖度基本一致。</div>

<!--
然后再按照 level + length_bucket 分层均匀抽样出 validation set。训练集 2000 条，覆盖 1378 个 unique filename，最终分数 中位数 0.768；验证集 500 条，覆盖 439 个 unique filename，，最终分数中位数 0.820。
-->

---

# LoRA 微调超参数

<div class="two-col">
  <div>
    <h2>训练配置</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>max sequence length</td><td>2048</td></tr>
      <tr><td>batch size per worker</td><td>1</td></tr>
      <tr><td>gradient accumulation steps</td><td>8</td></tr>
      <tr><td>learning rate</td><td>2e-4</td></tr>
      <tr><td>warmup ratio</td><td>0.03</td></tr>
      <tr><td>epochs</td><td>1</td></tr>
      <tr><td>workers</td><td>1</td></tr>
      </tbody>
    </table>
  </div>
  <div>
    <h2>训练曲线</h2>
    <img class="image-fit" :src="'/assets/training_curve.png'" alt="Training curve" />
  </div>
</div>

<!--
训练部分修改了课上的那个notebook进行训练。

只有 assistant 内容参与 loss 计算。
每个 Ray worker 独立加载 tokenizer、模型和数据集。

用了LoRA，这是主要超参数。
有效 batch size 为 8

右侧是训练曲线，这条蓝线是train曲线每五个点滑动窗口平均。
-->

---

# 本地部署与 Demo

<div class="demo-grid">
  <div>
    <img :src="'/assets/demo-qwen.png'" alt="Demo with Qwen checkpoint" />
    <p style="text-align:center;margin-top:0.4rem">Qwen checkpoint</p>
  </div>
  <div>
    <img :src="'/assets/demo-lora.png'" alt="Demo with LoRA model" />
    <p style="text-align:center;margin-top:0.4rem">LoRA 微调后</p>
  </div>
</div>

<!--
在 Qwen 官方 web demo 的基础上作了修改，支持用户上传数据文件，在一个独立文件夹运行生成的代码并返回结果。

左侧是使用原版 checkpoint 时的 Demo 界面，右侧是加载 LoRA 微调模型后的效果。微调过的模型更少出现不断重复的问题，且具有一些思考的形式。
-->

---

<div class="live-architecture">
  <div class="live-architecture-bar">
    <span>Q1 local Data Agent demo</span>
    <div class="live-architecture-actions">
      <a href="http://127.0.0.1:8001/" target="_blank">Open demo page</a>
    </div>
  </div>
  <iframe src="http://127.0.0.1:8001/" title="Q1 Data Agent Demo"></iframe>
</div>

<!--
额这里就是界面，时间原因就不展示了
-->

---

# Q1 小结

<div class="summary-line">
  <span>数据选择</span><span>DEITA 粗筛 → IFD 评分 → InstructDiff 排序 → 分层抽样</span>
</div>
<div class="summary-line">
  <span>训练数据</span><span>2000 训练 + 500 验证，按 level + length_bucket 分层</span>
</div>
<div class="summary-line">
  <span>模型微调</span><span>Ray Train + LoRA 微调 Qwen/Qwen3.5-0.8B</span>
</div>
<div class="summary-line">
  <span>本地 Demo</span><span>扩展 Qwen 官方 Demo，支持文件上传和代码执行返回</span>
</div>

<!--
本题围绕 DataMind-12K 构建了一个数据分析 Agent 的训练与部署流程。数据选择阶段结合 DEITA、IFD 和 InstructDiff，先保证样本质量、复杂度和多样性，再用模型相关信号排序，最后通过分层抽样得到 2000 条训练数据和 500 条验证数据。训练阶段使用 Ray Train 和 LoRA 对 Qwen/Qwen3.5-0.8B 进行微调，并保留验证集用于超参数设计和 checkpoint 选择。部署阶段在官方 Qwen demo 的基础上扩展了文件上传和代码执行返回能力，使界面更适合数据分析任务。
-->

---
layout: section
---

# Q2

## Startup Business Plan

<!--
第二道题
-->

---

# 提示词
LLM：OpenCode 接入 DeepSeek V4 Flash

<div class="demo-grid">

<div>
brainstorm:

读 `@refrences/` 里的资料，和我一起 brainstorm 一个以LLM应用为核心的盈利性创业公司，采用独立开发方式。
我们先来确认创业想法，给我点建议

`[...AI输出...]`

我觉得我做不出很深的技术壁垒，所以为了防止被大厂直接平替，我觉得应该做比较小以至于大厂懒得管的领域。
另外，中国好像做数据的人比较少，也许可以在产品里加入数据收集和标注来售卖。


<div class="prompt-block">
BP:

我现在有这样的 idea：[xxx]，请你根据 `refrences` 里的资料写BP，涵盖里面强调的各个方面。

`[...AI输出...]`

我刚才做了一些修改，你重新阅读相关文件，然后根据 refrences 检查，并上网调研该创业项目与市场上主要竞争对手的对比分析，写为另一个报告。
</div>
</div>

<div>
项目设计：

请你阅读 `@../report/*.md` 来了解一下我的这个项目计划，然后帮我设计我的产品的系统架构。

它需要支持工业级部署和10玩级别的并发（包括视觉模型、AI报告的LLM模型等）。

应当至少包括 LLM引擎、数据处理、数据库、高并发支持模块、监控运维模块。

将你的设计写为详细的html架构设计文档（你可以用vite/ts以便开发），其中至少要包括一个系统设计图。
</div>
</div>

<!--
第二道题所有大模型相关，我都是使用 OpenCode 接入 DeepSeek V4 Flash，推理能力设为 Max。
对于外界资料，如果是 PDF，就用 MinerU 转成 markdown；如果是网页，就用 Obsidian 插件解析成 markdown，再放在专门的文件夹里让它读取。
这里是我之后三个任务使用的提示词
-->

---

# 项目概况

<div class="two-col compact">
  <div>
    <h2>舌诊 AI</h2>
    <p>一款面向 C 端用户的健康追踪工具。用户每日拍摄舌苔照片并记录简单的身体感受（精力、排便、睡眠、饮食等），AI 自动输出舌象分析结果和健康趋势报告。</p>
    <p style="margin-top:0.8rem">同时构建标注舌诊数据集，服务医疗健康产业。</p>
  </div>
  <div>
    <h2>双引擎变现</h2>
    <p><strong>C 端</strong>：订阅制健康追踪服务</p>
    <p><strong>B 端</strong>：数据 API、行业定制、标准/深度标注数据集</p>
    <p style="margin-top:0.4rem;color:var(--accent)">独立开发方式，当前处于概念验证阶段（2026年5月）</p>
  </div>
</div>

<div class="claim">一次拍摄，多重价值：用户获得个人健康追踪，行业获得高质量标注数据。</div>

<!--
这是我和AI讨论后得到的idea：

通过 AI 舌象分析帮助用户每天追踪自身健康状况，同时构建标注舌诊数据集服务医疗健康产业。
同时在C端和B端变现。
-->

---

# 用户痛点

<div class="pain-grid">
  <div><b>不知道自己身体有没有问题</b><span>亚健康状态普遍，城市白领亚健康比例达 76%<sup>[2]</sup>，缺少可量化的日常健康监测手段。</span></div>
  <div><b>体检频率低、反馈慢</b><span>年度体检只能反映"单点"状况，无法追踪日常变化趋势。</span></div>
  <div><b>养生缺乏数据支撑</b><span>市面健康建议泛泛而谈，缺少针对个人体质的量化依据。</span></div>
  <div><b>舌象异常无人提醒</b><span>舌苔变化往往是身体变化的早期信号，但普通人无法识别。</span></div>
</div>

<div class="metrics" style="margin-top:1.2rem">
  <div><span>70%+<sup>[1]</sup></span><p>中国亚健康人群占比</p></div>
  <div><span>76%<sup>[2]</sup></span><p>城市白领亚健康比例</p></div>
  <div><span>500万+</span><p>"舌诊"话题月均搜索量</p></div>
  <div><span>¥20-50</span><p>目标用户对养生 App 月消费接受度</p></div>
</div>

<div class="slide-source">来源：[1] 《柳叶刀》相关数据引述；[2]《2009 中国城市白领健康状况白皮书》。社媒搜索量和付费区间为报告调研估计。</div>

<!--
用户痛点主要是中国亚健康人群占比超过 70%，城市白领亚健康比例达 76%。
中医舌诊有群众认知基础，无需推广教育。
在小红书/抖音"舌诊"相关话题月均搜索量超 500 万次。目标用户群（25-50 岁注重健康人群）付费意愿强，对养生类 App 月消费 ¥20-50 接受度高。验证依据来自《柳叶刀》引述数据、2009 年中国城市白领健康状况白皮书、社媒搜索趋势和行业报告。
-->

---

# 解决方案

<div class="product-flow">
  <div>晨起拍照</div>
  <div>30 秒健康记录</div>
  <div>AI 舌象分析</div>
  <div>每日评分+趋势</div>
  <div>生活建议</div>
</div>

<div class="feature-table">
  <div><b>舌象识别</b><span>AI 自动分析舌色、苔质、舌形、齿痕等 12 项指标</span></div>
  <div><b>每日次数</b><span>Free 3次 / Plus 5次 / Pro 无限</span></div>
  <div><b>趋势追踪</b><span>Free 7天 / Plus 30天 / Pro 无限+对比</span></div>
  <div><b>健康关联</b><span>舌象变化与精力/排便/饮食的交叉分析（Plus+）</span></div>
  <div><b>AI 建议</b><span>基于舌象+体质的生活/饮食建议（Plus+）</span></div>
  <div><b>数据导出</b><span>生成健康报告 PDF，可分享给医生（Plus+）</span></div>
  <div><b>数据上传控制</b><span>可手动关闭数据上传（Plus+）</span></div>
  <div><b>本地模型</b><span>设备端离线推理，无需联网（Pro）</span></div>
  <div><b>专属咨询</b><span>优先响应+中医师在线咨询额度（Pro）</span></div>
</div>

<!--
初期产品形态为
微信小程序 + iOS/Android App，或更简单的 PWA。
工作流程：
用户起床后拍摄舌苔照片，可选地填写 30 秒健康记录，AI 输出舌象分析，然后生成每日评分、趋势图、生活建议。

核心功能按 Free/Plus/Pro 三层划分：基础舌象识别每日 3 次免费；Plus 解锁趋势追踪和 AI 建议；Pro ¥69.9/月支持本地模型离线推理。
产品优势是零门槛拍照即用，高频驱动且与刷牙绑定可养成每日习惯、市场上无专门做 AI 舌诊追踪的产品。
-->

---

# 行业与市场分析

<div class="metrics">
  <div><span>¥5,500亿+<sup>[3]</sup></span><p>2025 年中国中医药市场规模</p></div>
  <div><span>¥150亿<sup>[4]</sup></span><p>AI 中医诊断市场</p></div>
  <div><span>50%+<sup>[4]</sup></span><p>AI 中医诊断年复合增长率</p></div>
  <div><span>¥300亿</span><p>TAM（市场总量）</p></div>
</div>

<div class="split-grid compact">
  <div>
    <h2>市场结构</h2>
    <table class="dense-table">
      <tbody>
      <tr><td>TAM</td><td>¥300 亿</td><td>亚健康管理 + 中医数字化</td></tr>
      <tr><td>SAM</td><td>¥30 亿</td><td>移动端 AI 健康追踪 + 中医诊断</td></tr>
      <tr><td>SOM</td><td>¥3 亿</td><td>独立开发团队首期可触达</td></tr>
      </tbody>
    </table>
  </div>
  <div>
    <h2>市场趋势</h2>
    <ul>
      <li>亚健康管理从可选变必需</li>
      <li>中医年轻化，年轻一代对中医接受度上升</li>
      <li>AI 降低中医门槛，不再依赖老中医经验</li>
      <li>高质量医疗标注数据集成为稀缺资源</li>
    </ul>
  </div>
</div>

<div class="slide-source">来源：[3] 中商产业研究院中医药市场预测；[4] WAIC 2025 智慧眼科技等发布数据。TAM/SAM/SOM 为报告基于市场规模、目标人群和转化率的估算。</div>

<!--
中医数字化正在经历快速渗透。2025 年中国中医药市场规模约 5,500-6,000 亿元，其中 AI 中医诊断市场约 150 亿元，2020-2025 年年复合增长率超过 50%。国家政策明确支持"中医药+人工智能"融合发展。
-->

---

# 竞争分析

<div class="competitor-list">
  <div><b>看舌智能检测</b><span>在线问诊 App 子功能，仅单次识别，无追踪、无历史对比。</span></div>
  <div><b>体质测试类 App</b><span>问卷式，无 AI 图像分析，依赖主观填写，缺少客观影像数据。</span></div>
  <div><b>中医馆舌诊仪</b><span>专业设备，价格高（¥5000+），无法家用。</span></div>
  <div><b>通用 AI 健康助手</b><span>对话式，无视觉输入，无专用模型，舌象分析不专业。</span></div>
</div>

<div class="split-grid compact">
  <div>
    <h2>我们的优势</h2>
    <ul>
      <li><b>持续纵向追踪</b>：不只单次识别，还做日维度趋势分析</li>
      <li><b>舌象数据积累</b>：随着用户量增长形成不可复制壁垒</li>
      <li><b>用户习惯绑定</b>：每日拍照形成习惯，转换成本高</li>
      <li><b>双模式变现</b>：C 端 + B 端风险分散</li>
    </ul>
  </div>
  <div>
    <h2>竞争定位</h2>
    <p class="note">不做高 ROI 正面战场，做窄场景的数据壁垒。大厂 ROI 门槛高，舌诊场景足够窄但需求真实。</p>
  </div>
</div>

<!--
我们的竞争对手包括四类。
第一类是在线问诊 App 的子功能如看舌智能检测，它仅单次识别，没有追踪和历史对比也没有专有模型。

问卷式体质测试 App，完全依赖主观填写，而我们有模型分析。

第三类是中医馆的舌诊仪设备，价格高（¥5000+），无法家用。

第四类是通用 AI 健康助手如豆包等，依旧无专用模型而我们有并且有自己数据集；而且该方向较窄，不会与大场形成竞争
-->

---

# 商业模式

<div class="price-strip">
  <span>Free ¥0<br>每日 3 次 + 7 天趋势</span>
  <span>Plus ¥9.9/月<br>30 天趋势 + AI 建议 + 报告导出</span>
  <span>Plus 年费 ¥99/年<br>额外赠送 2 个月</span>
  <span>Pro ¥69.9/月<br>无限次数 + 本地模型 + 咨询</span>
</div>

<div class="split-grid compact">
  <div>
    <h2>C 端收入估算</h2>
    <p>首年目标 5 万付费用户（Plus 为主，Pro 约占 10-15%），对应 ¥800 万-900 万年订阅收入。</p>
  </div>
  <div>
    <h2>B 端数据服务</h2>
    <p>标准数据集 ¥0.5-2/条，深度标注集 ¥5-15/条，行业 API ¥3-8 万/年起，定制研究 ¥20-50 万/项目。预计第二年启动，第三年成为主要利润来源。</p>
  </div>
</div>

<div class="slide-source">估算依据：C 端收入按报告中的目标付费用户数、Plus/Pro 价格和 Pro 占比测算；B 端价格区间为报告调研与商业计划假设。</div>

<!--
C 端采用三层订阅制

B 端数据服务收入模型：标准数据集 ¥0.5-2/条卖给 AI 医疗公司，深度标注集 ¥5-15/条卖给药企和中医馆系统商，行业 API ¥3-8 万/年起卖给健康 App 和体检机构，定制研究 ¥20-50 万/项目卖给药企和化妆品公司。
-->

---

# 发展规划

<div class="timeline">
  <div>
    <span>Phase 1</span>
    <b>1-3 个月</b>
    <p>MVP 开发与验证：舌象识别模型、MVP 小程序、用户访谈。</p>
  </div>
  <div>
    <span>Phase 2</span>
    <b>3-9 个月</b>
    <p>产品打磨与用户获取：全功能上线、10,000 MAU、50 万张标注图片。</p>
  </div>
  <div>
    <span>Phase 3</span>
    <b>9-18 个月</b>
    <p>B 端商业化：数据质量审计、首批 B 端客户、数据 API 产品化。</p>
  </div>
</div>

<div class="claim">启动成本低，验证路径清楚；先证明每日追踪价值，再放大数据资产。</div>

<!--
第一阶段是 1 到 3 个月 MVP 开发与验证，交付舌象识别模型、MVP 小程序和用户访谈。

第二阶段是 3 到 9 个月产品打磨与用户获取，完成全功能上线、10,000 MAU 和 50 万张标注舌象图片积累。

第三阶段是 9 到 18 个月 B 端商业化，完成数据质量审计、首批 B 端客户和数据 API 产品化。
-->

---

# 风险与应对

<div class="risk-list">
  <div><b>AI 准确率不达标</b><span>中概率 / 高影响 · MVP 阶段先用 GPT-4o 视觉验证需求，再训练专用小模型</span></div>
  <div><b>用户留存率低</b><span>中概率 / 高影响 · 每日推送、打卡、连续记录奖励等习惯机制</span></div>
  <div><b>大厂进入市场</b><span>低概率 / 中影响 · 先建立数据壁垒，避开高 ROI 正面战场</span></div>
  <div><b>中医行业规范性风险</b><span>低概率 / 中影响 · 定位健康追踪工具，不涉及诊断/治疗</span></div>
  <div><b>数据隐私问题</b><span>低概率 / 高影响 · Plus/Pro 可关闭上传，Pro 支持本地模型，B 端匿名化</span></div>
  <div><b>变现周期过长</b><span>中概率 / 中影响 · C 端从 Day 1 收费，B 端用户量达标后开启</span></div>
</div>

<!--
我们总共有三类风险
AI 模型准确率不达标，MVP 阶段先用多模态模型+prompt来视觉能力验证需求，再训练专用小模型；

用户留存率低（概率中、影响高），每日推送、打卡、连续记录奖励；

大厂进入市场（概率低、影响中），先做窄场景和数据壁垒；

中医行业规范性风险（概率低、影响中），定位为健康追踪工具不做诊断治疗；

数据隐私问题，Plus/Pro 可关闭上传，B 端数据全匿名化；

变现周期过长（概率中、影响中），C 端订阅从 Day 1 开始收费，B 端在用户量达标后开启。
-->

---
layout: section
---

# Q2

## 系统架构设计

<div class="section-note">目标：10 万级并发、API P99 小于 500ms、SLA 99.95%，并支撑视觉模型、LLM 报告和数据服务。</div>

<!--
下面是AI生成的系统架构设计
-->

---

# 架构目标

<div class="arch-brief">
  <div>
    <span>01</span>
    <h2>异步优先</h2>
    <p>图片上传和推理任务解耦，重计算不阻塞 API。</p>
  </div>
  <div>
    <span>02</span>
    <h2>水平扩展</h2>
    <p>应用服务、GPU 推理、缓存、消息队列都能独立扩容。</p>
  </div>
  <div>
    <span>03</span>
    <h2>数据驱动</h2>
    <p>分析结果、用户反馈、时序记录进入数据湖和训练闭环。</p>
  </div>
</div>

<div class="metrics architecture">
  <div><span>10 万+</span><p>并发用户</p></div>
  <div><span>&lt;500ms</span><p>API P99</p></div>
  <div><span>99.95%</span><p>SLA</p></div>
  <div><span>500 万+</span><p>日处理图片</p></div>
</div>

<div class="slide-source">说明：本页指标为项目架构设计目标，用于约束微服务、异步推理、缓存和扩容方案，不作为外部市场统计。</div>

<!--
核心目标是支撑 10 万级并发用户访问，确保高负载下低延迟（API P99 < 500ms）、高可用（SLA 99.95%）、日处理图片 500 万以上、年数据增长 50TB 以上。

设计原则包括微服务解耦、异步优先、水平扩展、数据驱动、成本优化和隐私合规。
-->

---
class: architecture-embed
---

<div class="live-architecture">
  <div class="live-architecture-bar">
    <span>q2/design/architecture-design</span>
    <div class="live-architecture-actions">
      <a href="/architecture-design/index.html" target="_blank">Open report page</a>
    </div>
  </div>
  <iframe src="/architecture-design/index.html" title="舌诊 AI 系统架构设计文档"></iframe>
</div>

<!--
这是AI写的的总体设计文档

第一步看总体架构：
系统从下到上分为基础设施层、数据存储层、数据处理层、AI 推理层、应用服务层、网关层和接入层，每层之间通过明确接口通信，便于独立扩容和升级。

第二步看业务链路：
用户上传舌苔照片后，图片预处理进入视觉推理；系统查询历史数据做时序分析，再由 LLM 生成个性化健康报告和生活建议；结果通过 WebSocket 推送给客户端，同时异步写入数据库和数据湖。

第三步看高并发支撑：
舌诊分析不做同步等待，而是任务队列 + WebSocket 推送；缓存分为 CDN、Redis、本地缓存三级；应用服务、GPU 推理节点、Redis、Kafka 都设计为可水平扩容。第四步看 AI 引擎：视觉模型用 Triton、TensorRT、动态批处理和多实例并发优化；LLM 报告生成用 vLLM、、量化和 Prefix Caching。第五步看监控和安全：Prometheus/Grafana 看指标，Loki 做日志聚合，Jaeger 做链路追踪；健康数据强制 TLS 1.3 传输，图片、健康记录和身份信息使用 AES-256-GCM 加密存储，密钥由 KMS 管理。

docker compose 文件因为比较长没有贴出来，在报告和代码文件里都上传了。
-->

---

# 参考文献

<div class="reference-list">
  <p>[1] 中国亚健康人群占比约 70%：中国工程院院士单杨于 2024 年"湘江大讲堂"引述《柳叶刀》数据。<br><a href="https://www.21jingji.com/article/20220224/herald/9143d274fc45f8929abd049e671259cb.html">21jingji.com</a></p>
  <p>[2] 城市白领亚健康比例 76%：中国医师协会等机构《2009 中国城市白领健康状况白皮书》。<br><a href="https://www.chinanews.com.cn/jk/jk-ysbb/news/2010/02-01/2101483.shtml">chinanews.com.cn</a></p>
  <p>[3] 2025 年中国中医药市场规模约 5,500-6,000 亿元：中商产业研究院《2025-2030年中国中医药市场需求预测及发展趋势前瞻报告》。<br><a href="https://www.askci.com/news/chanye/20250425/104205274554892438486735.shtml">askci.com</a></p>
  <p>[4] AI 中医诊断市场 2025 年约 150 亿元，2020-2025 年 CAGR 超 50%：2025 年世界人工智能大会（WAIC）智慧眼科技等企业发布数据。<br><a href="http://www.cnr.cn/hunan/flxw/dj/20250727/t20250727_527284709.shtml">cnr.cn</a></p>
</div>

<!--
这里列出 Q2 中涉及外部市场和健康数据的主要来源。报告中没有外部出处的经营、定价和架构容量数字，统一标为商业计划估算或设计目标。
-->

---

# 总结

<div class="final-grid">
  <div>
    <h2>Q1</h2>
    <p>从 DataMind-12K 出发，结合 DEITA、IFD、InstructDiff 三种数据选择方法，通过分层抽样得到 2000/500 训练验证集，用 Ray Train + LoRA 微调 Qwen/Qwen3.5-0.8B，最终通过扩展官方 Demo 验证了 Data Agent 交互链路。</p>
  </div>
  <div>
    <h2>Q2</h2>
    <p>把舌诊 AI 从创业想法扩展到完整商业计划（用户痛点、市场分析、竞争定位、定价模型、发展规划与风险），再落地到支持 10 万级并发的七层工业级系统架构设计。</p>
  </div>
</div>

<div class="closing">两题共同点：都在围绕"数据"做系统。Q1 用数据训练 Agent，Q2 用产品持续生产有价值的数据——数据既是输入，也是输出。</div>

<!--
结尾回扣两题共同点。Q1 是数据选择方法到模型训练的完整闭环，Q2 是创业 BP 到工业级系统架构的全面覆盖。核心思路：先用窄场景解决真实需求，再通过持续数据沉淀形成长期壁垒。
-->
