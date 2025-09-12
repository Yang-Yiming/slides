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

# 一些失败尝试

| 方法  | 通过题数 | 得分  | 总用时(s)  | 速度倍率  | 备注 |
| --- | --- | --- | --- | --- | --- |
| 上文提及方法     | 3    | 10  | 906.97  | 1     |    |
| 卷积 + scatter  | 0    | 0   | -     | 0     | 增加了 bootstrap 次数 |
| 加法树降低深度。保存会被多次计算的地方 | 0  | 0   | 690.9   | 1.31  | m n较小时表现差   |
| Parallelized PBS([文档](https://docs.zama.ai/tfhe-rs/configuration/parallelized-pbs)) | 2    | 5   | 682.94  | 1.32  | 问题同上<br>              |
| 每线程细胞数：4   | 2    | 5   | 1181.76 | 0.77  | |
| 8    | 2    | 5   | 1176.23 | 0.77  |      |
| 16  | 2    | 5   | 1307.28 | 0.694 |   |


---
transition: fade-out
level: 2
---

# `FheUInt8` $\to$ `FheBool`

降低计算的 bit 数，且适合生命游戏。只要实现 3 位加法器用于计数。

## 加法器

半加器

```rust
fn half_adder(a: &FheBool, b: &FheBool) -> (FheBool, FheBool) {
    let sum = a ^ b;
    let carry = a & b;
    (sum, carry)
}
```

---
transition: fade-out
level: 2
---

# 史山加法树

```rust
// 加法树
// 第一层
let (s1, c1) = half_adder(&neighbors_vals[0], &neighbors_vals[1]);
let (s2, c2) = half_adder(&neighbors_vals[2], &neighbors_vals[3]);
let (s3, c3) = half_adder(&neighbors_vals[4], &neighbors_vals[5]);
let (s4, c4) = half_adder(&neighbors_vals[6], &neighbors_vals[7]);

// 第一位 和位
let (s12, c12) = half_adder(&s1, &s2);
let (s34, c34) = half_adder(&s3, &s4);
let (bit0, c_bit0) = half_adder(&s12, &s34); // 最低位

// 第一位 进位
let (c_temp1, c_temp1_carry) = half_adder(&c1, &c2);
let (c_temp2, c_temp2_carry) = half_adder(&c3, &c4);
let (c_sum, c_sum_carry) = half_adder(&c_temp1, &c_temp2);

// 第二位
let (bit1_part1, bit1_carry1) = half_adder(&c12, &c34);
let (bit1_part2, bit1_carry2) = half_adder(&bit1_part1, &c_bit0);
let (bit1, bit1_final_carry) = half_adder(&bit1_part2, &c_sum);
```

---
transition: fade-out
level: 2
---

```rust

// 第三位
let bit2_temp1 = &c_temp1_carry | &c_temp2_carry;
let bit2_temp2 = &c_sum_carry | &bit1_carry1;
let bit2_temp3 = &bit1_carry2 | &bit1_final_carry;
let bit2 = &bit2_temp1 | &bit2_temp2 | &bit2_temp3;

let is2 = !&bit0 & &bit1 & !&bit2; // 010
let is3 = &bit0 & &bit1 & !&bit2; // 011
is3 | (is2 & &grid[x][y])

```


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
