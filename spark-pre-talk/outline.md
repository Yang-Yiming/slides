# 从模型到 Agent：Coding Harness 在做什么

## 0. 核心立意

这次小讲不把 coding agent 讲成“最近很火的产品”，而是讲它背后更具体的一层：harness。

主线可以概括为：

> 模型负责理解、生成和推理；harness 负责把这些能力放进一个能工作的开发环境里。

也就是说，coding agent 的差别不只来自模型，还来自上下文管理、工具接入、任务循环、安全边界和产品工作流。

## 1. 开场：为什么要看 harness

### 论点

模型已经能写出不错的代码后，下一个问题变成：怎么让它稳定地做完真实项目里的任务。

### 展开

- 早期重点是模型本身：补全、问答、单次生成。
- 现在任务更接近真实开发：读仓库、跑命令、改文件、处理失败、恢复上下文。
- 这些能力需要外层工程系统支撑，不只是把模型接到一个输入框里。

### 过渡

所以比较 coding agent 时，不能只问用了哪个模型，也要问它背后的 harness 怎么设计。

## 2. 先定义：什么是 harness

### 论点

Harness 是把模型放进工作流的运行框架：它决定模型看见什么、能做什么、什么时候停、失败后怎么继续。

### 四个维度

1. Context：历史怎么保留、压缩、删除。
2. Tools：文件、终端、浏览器、搜索等工具怎么接入。
3. Control：什么时候规划、执行、暂停、恢复。
4. Safety：权限、沙箱、审批、文件边界。

### 过渡

用这个定义看，Claude Code、Codex、OpenCode 的差别并不只是界面不同，而是三套不同的 harness 取舍。

## 3. 三种常见做法

### 论点

当前 coding agent 大致可以看成三种做法：模型厂深度适配、强安全和产品工作台、跨 provider 的开放 harness。

### 对应例子

- Claude Code：深度适配 Claude，重点放在长任务连续性。
- Codex CLI / App：围绕 GPT 生态做强沙箱和任务工作台。
- OpenCode：跨 provider 通用 harness，强调开放和可迁移。

### 过渡

三者都能写代码，但差别主要在上下文、安全、工具和工作流。

## 4. Claude Code：把上下文当任务状态

### 论点

Claude Code 的特点是上下文管理很细，目标是在长任务里尽量保住关键状态。

### 证据

可以讲四层：

- HISTORY_SNIP：删掉明显没用的历史片段。
- Microcompact：在缓存层面做更细粒度的编辑。
- CONTEXT_COLLAPSE：把旧轮次归档成带结构的摘要，之后再重放回来。
- Autocompact：窗口快撑不住时的兜底，把整体历史压成摘要。

### 可强调

这套设计不是为了显得复杂，而是为了让长程开发任务更不容易断线。代价是 harness 自身复杂度会上升。

## 5. Codex：安全边界和工作流

### 论点

Codex 的重点不是做最通用的 harness，而是把 GPT 系列模型放进一个安全、可长期使用的开发环境。

### CLI 侧

- system prompt + tool schema 是核心结构。
- 上下文到阈值后自动 compact。
- 沙箱比较强，危险操作在系统层面被挡住。
- 代价是跨模型适配弱一些，可编程性也会受安全边界影响。

### App 侧

- worktree 多任务后台执行。
- 日常模式、远程连接、goal 模式。
- 宠物和状态可视化，说明它在向“日常工作台”演化。

### 可强调

Codex 在回答一个产品问题：怎么让 agent 不只是终端工具，而是能长期待在工作流里。

## 6. OpenCode：通用 provider 的 harness

### 论点

OpenCode 的重点是跨模型、跨 provider 的通用设计：尽量不把 harness 绑死在某一个模型厂。

### 证据

- system prompt = provider 特定提示 + 通用模板。
- 上下文先 prune，再 compact。
- Prune 只在释放量足够大时触发。
- 最近上下文和重要 skill 输出会保留。
- Compact 会压缩旧历史，但保证最后两轮完整。

### 可强调

它用部分深度适配换开放性和可替换性。好处是通用，代价是很难把单个模型的特性用到极致。

## 7. Harness 对比：不是排座次，而是看取舍

| 维度 | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| 模型适配 | 深度绑定 Claude | 深度绑定 GPT | 跨 provider |
| 上下文策略 | 多层记忆 / 归档 | 简洁 compact | prune + compact |
| 安全边界 | 工具与权限控制 | 强系统沙箱 | 取决于部署和配置 |
| 产品方向 | CLI 长程任务 | CLI + App 工作台 | 开源通用 agent |
| 主要优势 | 长任务连续性 | 安全和产品体验 | 开放和可迁移 |
| 主要代价 | 复杂、绑定强 | 跨模型弱 | 极致适配较难 |

这张表重点不是判断谁绝对更好，而是说明每个 harness 都在做工程取舍。

## 8. Benchmark：harness 会改变模型表现

### 论点

同一个模型放进不同 harness，表现可能变化。所以 benchmark 测到的不只是模型，也包括外层工程系统。

### 数据用法

不要把表格讲成“谁第一”，而是讲成：

- SpatialBench：Claude Code 相比 bare mini-SWE-agent 有明显提升。
- RTHarnessBench：Claude Code 和 OpenCode 接近。
- 翻译基准：不同 harness 会拉开差距。

### 过渡

公开 benchmark 能说明 harness 有影响；自己的小实验可以让这个影响更直观。

## 9. 同一项目实验：三种运行方式的成本差异

### 论点

同一个 2D SPH 流体模拟任务，不同 harness 在时间、token 和执行路径上差异很大。

### 数据

| Harness | 用时 | Token |
| --- | ---: | ---: |
| 网页端 | 202s | - |
| Claude Code | 10m52s | 57.4k |
| OpenCode | 27m25s | 101.5k |

### 解释重点

- 网页端快，但更像一次性生成，项目级操作能力有限。
- Claude Code 更像进入项目后规划和执行，时间和 token 成本会上升。
- OpenCode 花费更多，可能来自通用 harness 的额外规划和上下文处理。

### 注意

这不是严格实验，只能作为观察样例；但它能帮助大家理解 harness 不是纯外壳，会实际影响效率和可控性。

## 10. 回到行业：Model + Harness = Agent

### 论点

厂商开始把 harness 当作专门方向，说明 agent 的能力公式已经从模型扩展到了系统。

### 例子

DeepSeek 招募 harness 相关岗位，并写下 “Model + Harness = Agent”。

### 可强调

这句话的含义是：模型负责语言和推理，harness 负责把推理组织成可控行动。

## 11. 小结：三个判断

### 判断 1

Coding agent 的关键变化，是模型能力被放进了工程流程。

### 判断 2

不同 agent 的差别，主要来自上下文、安全、工具和工作流的取舍。

### 判断 3

以后比较 agent，模型和 harness 都要看。

## 12. 结尾句

可以用这句话收束：

> 模型是发动机，harness 是让它能上路的一整套系统。
