---
theme: seriph
background: https://cover.sli.dev
title: Rust
info: |
  RUSTCSC competition - basic - rust

class: text-center
drawings:
  persist: false

transition: slide-left
mdc: true
seoMeta:
  ogImage: auto
---

# Rust

SUSTCSC - basic track

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Press Space for next page <carbon:arrow-right />
</div>

<div class="abs-br m-6 text-xl">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="slidev-icon-btn">
    <carbon:edit />
  </button>
  <a href="https://github.com/Yang-Yiming/slides" target="_blank" class="slidev-icon-btn">
    <carbon:logo-github />
  </a>
</div>

---
transition: fade-out
---

# Client

- 计算量极小
  - 加密: 573.0 ms
  - 其余: 0.0 ms 
- `iter()` $\to$ `par_iter()`

- [文档](https://docs.zama.ai/tfhe-rs/configuration/parallelized-pbs)，可指定密钥参数如`V1_2_PARAM_MULTI_BIT_GROUP_3_MESSAGE_2_CARRY_2_KS_PBS_TUNIFORM_2M64`. 
  - 测试: 几乎没有性能改变(见后文表格)


---
transition: fade-out
level: 2
---

# Server - `step()` 并行

rayon : `iter()` $\to$ `par_iter()`

`set_server_key()` 需要每线程都设置. `BorrowMutErr` 解决：

[官方文档](https://docs.zama.ai/tfhe-rs/1.1/fhe-computation/advanced-features/rayon_crate)

```rust
// set the server key in all of the rayon's threads so that
// we won't need to do it later
rayon::broadcast(|_| set_server_key(sks.clone()));
// Set the server key in the main thread
set_server_key(sks);
```

后再开线程

---
transition: fade-out
level: 2
---

# 细胞计算不均

<img src="/test1_heatmap.png" style="width: 30%; height: auto;">

`tfhe` 加法开销大,资源浪费

`par_iter()` 自带 `workstealing`.

```rust
.into_par_iter()
with_min_len(std::cmp::max(
	1,
	total_cells / (rayon::current_num_threads() * 4),
))
```

<div v-click="1">
  这里 `4` 是每个线程处理 4 个细胞，后续调出的最优解
</div>

---
transition: fade-out
level: 2
---

# 问题
=

- `main.rs` 要求和原始 secret 完全一致，但是最终精度始终不够。
- 在 $n>5$ 时，构造的格基会线性相关导致 BKZ 产生接近 $\mathbf{0}$ 结果
- 产生 $\mathbf{0}$ 后 Gram-Schmidt 失效 $\to$ Babai 失效 $\to$ LWE 爆了


---
transition: fade-out
level: 2
---

# 谢谢大家！
