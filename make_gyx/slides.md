---
theme: seriph
background: https://cover.sli.dev
title: Makefile & CMake 简介
info: |
  参考 https://www.bilibili.com/video/BV188411L7d2/

class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true

seoMeta:
  ogImage: auto
---

# Makefile & CMake 简介



<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  下一页 <carbon:arrow-right />
</div>

---

# 简单的 C++ 例子

<TabbedCode :tabs="[{ label: 'main.cpp', slot: 'code1' }, { label: 'printhello.cpp', slot: 'code2' }, { label: 'factorial.cpp', slot: 'code3' }, { label: 'functions.h', slot: 'code4' }]">
  
  <template #code1>

  ```cpp
  // main.cpp
  #include <iostream>
  #include "functions.h"
  using namespace std;

  int main() {
    printhello();
    cout << factorial(5) << endl;
    return 0;
  }
  ```

  </template>

  <template #code2>

  ```cpp
  // printhello.cpp
  #include <iostream>
  #include "functions.h"
  using namespace std;

  void printhello() {
    cout << "hello world" << endl;
  }
  ```

  </template>

  <template #code3>

  ```cpp
  // factorial.cpp
  #include "functions.h"

  int factorial(int n) {
    if (n == 1) {
      return 1;
    } else {
      return n * factorial(n - 1);
    }
  }

  ```

  </template>

  <template #code4>

  ```cpp
  // functions.h
  #ifndef _FUNCTIONS_H_
  #define _FUNCTIONS_H_
  int factorial(int n);
  void printhello();
  #endif
  ```

  </template>

</TabbedCode>

<div v-click="1">
```bash
g++ main.cpp factorial.cpp printhello.cpp -o main
./main
```
</div>

<div v-click="2"> <!-- 逐个编译，以后修改单个文件就不用重新编译全部，只要编译被修改的文件然后重新链接 -->
```bash
g++ main.cpp -c
... # 每个文件都编译出一个 .o 文件
g++ *.o -o main # 链接所有的文件
./main
```
</div>



---

# 什么是 Makefile？

- Makefile 将上述流程自动化
- 基于规则：目标、依赖、命令
- 常用于 C/C++ 项目，但也可用于其他语言
- 使用 `make` 命令执行

---

# Makefile 基本语法

```makefile
target: dependencies
    command
```

- **target**: 要生成的文件或任务名
- **dependencies**: 目标依赖的文件
- **command**: 生成目标的命令（必须以 Tab 开头）

`make` 会检查文件是否被更新过，并根据依赖关系执行命令 

---

# Makefile

1.
```makefile
hello: main.cpp printhello.cpp factorial.cpp
    g++ -o hello main.cpp printhello.cpp factorial.cpp
```

```bash
make
```

<div v-click="1">
2.

```makefile

CXX = g++
TARGET = hello
OBJ = main.o printhello.o factorial.o

$(TARGET): $(OBJ) # TARGET 依赖于 OBJ，即 如果 OBJ 更新，那么就执行下面的代码更新 TARGET
  $(CXX) -o $(TARGET) $(OBJ)

%.o : %.cpp
  $(CXX) -c $< -o $@ # $< - 依赖的第一个 $@ - 目标

.PHONY: clean # 防止目录里有一个叫做 clean 的文件引起歧义
clean:
  rm *.o $(TARGET) # 如果输入 `make clean` 就执行这个。

```
```bash
make
```
</div>

---

# Makefile 只是检查依赖、执行 shell

所以完全可以用来构建 latex 等其他东西，甚至做这些：

```makefile
1.txt : 2.txt 3.txt
	cat 2.txt 3.txt > 1.txt

.PHONY: miao
miao:
	sed -i '' 's/$$/喵～/' *.txt
```

```bash
make # 保证 1.txt 是 2.txt + 3.txt
make miao # 在每一句加上喵
```


---

# 什么是 CMake？

- CMake 是一个**跨平台**的构建系统生成器
- 生成 Makefile
- 更高级和灵活，适合大型项目
- 使用：编写 CMakeLists.txt

<div v-click>

**CMakeLists.txt 基本结构**

```cmake
cmake_minimum_required(VERSION 3.10) # 设置最小 CMake 版本
project(MyProject) # 定义项目名

add_executable(main main.c utils.c) # 添加可执行文件
```
</div>

---

# CMake 例子

最前面的例子

```cmake
cmake_minimum_required(VERSION 3.10)
project(CppTest) # 设置名称

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 定义源文件
set(SOURCE_FILES
    main.cpp
    printhello.cpp
    factorial.cpp
)

# 添加可执行文件
add_executable(main ${SOURCE_FILES})
```


---

# 使用 CMake / 一般的开发流程

1. 在工作目录下创建 build 目录: `mkdir build && cd build`
2. 生成构建文件: `cmake ..`
3. 编译: `make`

---

# 总结

- Makefile: 自动化构建脚本
- CMake: 构建系统生成器，跨平台
- 根据项目规模选择合适工具

---

# 谢谢大家

参考文献：

\[1\] 于仕琪(OpenCV 中文站站长, 南科大最受欢迎计算机教授). (2022). Makefile/CMake 教学视频 \[EB/OL\]. 哔哩哔哩. 检索自: https://www.bilibili.com/video/BV188411L7d2/?spm_id_from=333.337.search-card.all.click&vd_source=d92c6d9c9e0385696e357756b334caf3

\[2\] ChatGPT

<PoweredBySlidev mt-10 />
