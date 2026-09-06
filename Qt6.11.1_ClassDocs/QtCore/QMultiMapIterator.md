# QMultiMapIterator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMultiMapIterator` 是容器或范围的迭代器类型，用于按约定遍历元素；重点是有效期、可写性和失效规则。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMultiMapIterator` 是 迭代器与范围机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 迭代器表示容器或目录遍历中的当前位置，通常通过 begin/end 或 range-for 使用。迭代器是否可写、是否支持随机跳转、end/sentinel 如何表示结束，取决于具体类型。

**适用场景：** 优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要解引用 end/sentinel；不要在活跃迭代器存在时复制或修改隐式共享容器；不要缓存容器元素引用跨越可能重分配的操作。

## 2. 依赖与对象关系

- 头文件：`#include <QMultiMapIterator>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

迭代器表示容器或目录遍历中的当前位置，通常通过 begin/end 或 range-for 使用。迭代器是否可写、是否支持随机跳转、end/sentinel 如何表示结束，取决于具体类型。

### 状态、生命周期和线程

**生命周期：** 迭代器依赖底层容器、目录枚举或视图对象存活；容器修改、隐式共享 detach 或目录资源关闭可能使迭代器失效。sentinel 只用于比较结束，不能解引用。

**状态与结果：** 有效迭代器、尾后迭代器和失效迭代器是不同状态。每次递增前要保证尚未到 end；删除当前元素时使用类提供的 erase/remove 规则，不要继续使用被删除位置。

**线程与事件循环：** 迭代器不提供跨线程同步；后台遍历应拥有稳定的数据快照或独占容器，结果再通过消息传回。

## 3. 直接使用

优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
for (auto it = container.cbegin(); it != container.cend(); ++it) {
    // 读取 *it，不要在遍历期间让 container 发生会使迭代器失效的修改
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QMultiMapIterator(const QMultiMap<Key, T> &map)`
- `bool findNext(const T &value)`
- `bool findPrevious(const T &value)`
- `bool hasNext() const`
- `bool hasPrevious() const`
- `const Key & key() const`
- `QMultiMapIterator<Key, T>::Item next()`
- `QMultiMapIterator<Key, T>::Item peekPrevious() const`
- `QMultiMapIterator<Key, T>::Item previous()`
- `void toBack()`
- `void toFront()`
- `const T & value() const`
- `QMultiMapIterator<Key, T> & operator=(const QMultiMap<Key, T> &map)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMultiMapIterator::QMultiMapIterator(const QMultiMap<Key, T> &map)`

**作用与语义：**

构建一个遍历`map`的迭代器。迭代器设置为位于地图前端（第一个物品之前）。

### `bool QMultiMapIterator::findNext(const T &value)`

**作用与语义：**

从当前迭代位置开始搜索`value`。如果找到值为`value`的（键值）对，返回`true`;否则返回`false`。
调用后，如果找到`value`，迭代器会被放置在匹配的物品之后;否则，迭代器会被放置在容器的后部。

### `bool QMultiMapIterator::findPrevious(const T &value)`

**作用与语义：**

从当前迭代位置向后搜索`value`。如果找到值为`value`的（键，值）对，返回`true`;否则返回`false`。
调用后，如果找到`value`，迭代器会被放置在匹配的物品之前;否则，迭代器会被放置在容器的前端。

### `bool QMultiMapIterator::hasNext() const`

**作用与语义：**

如果迭代器前方至少有一个项，即迭代器不在容器的后方，返回`true`;否则返回`false`。

### `bool QMultiMapIterator::hasPrevious() const`

**作用与语义：**

如果迭代器后面至少有一个项目，即迭代器不在容器前端，返回`true`;否则返回`false`。

### `const Key &QMultiMapIterator::key() const`

**作用与语义：**

返回使用某个遍历函数（`next()`、`previous()`、`findNext()`、`findPrevious()`）跳过的最后一个项目的键。
在调用`next()`或`findNext()`后，`key()`等价于`peekPrevious()`。`key()`。在调用`previous()`或`findPrevious()`后，`key()`等价于peekNext()。`key()`。

### `QMultiMapIterator<Key, T>::Item QMultiMapIterator::next()`

**作用与语义：**

返回下一项，并使迭代器前进一个位置。
调用返回值的 `key()` 以获取该项的密钥，`value()` 获取值。
在容器后部的迭代器上调用该函数会导致未定义的结果。

### `QMultiMapIterator<Key, T>::Item QMultiMapIterator::peekPrevious() const`

**作用与语义：**

返回上一个项目，无需移动迭代器。
调用返回值的 `key()` 以获取该项的密钥，`value()` 获取值。
在容器前端的迭代器上调用该函数会导致未定义的结果。

### `QMultiMapIterator<Key, T>::Item QMultiMapIterator::previous()`

**作用与语义：**

返回上一个项，并将迭代器后退一个位置。
调用返回值的 `key()` 以获取该项的键，`value()` 以获取值。
在容器前端的迭代器上调用该函数会导致未定义的结果。

### `void QMultiMapIterator::toBack()`

**作用与语义：**

将迭代器移到容器的后方（最后一个物品之后）。

### `void QMultiMapIterator::toFront()`

**作用与语义：**

将迭代器移到容器前端（第一个物品之前）。

### `const T &QMultiMapIterator::value() const`

**作用与语义：**

返回使用遍历函数（`next()`、`previous()`、`findNext()`、`findPrevious()`）跳过的最后一个项目的值。
在调用`next()`或`findNext()`后，`value()`等价于`peekPrevious()`。`value()`。调用`previous()`或`findPrevious()`后，`value()`等价于peekNext()。`value()`。

### `QMultiMapIterator<Key, T> &QMultiMapIterator::operator=(const QMultiMap<Key, T> &map)`

**作用与语义：**

让迭代器在`map`上运行。迭代器设置为在地图前端（第一个项目之前）。

## 6. 深入实践与常见坑

### 生命周期和资源边界

迭代器依赖底层容器、目录枚举或视图对象存活；容器修改、隐式共享 detach 或目录资源关闭可能使迭代器失效。sentinel 只用于比较结束，不能解引用。

### 状态和错误边界

有效迭代器、尾后迭代器和失效迭代器是不同状态。每次递增前要保证尚未到 end；删除当前元素时使用类提供的 erase/remove 规则，不要继续使用被删除位置。

### 线程边界

迭代器不提供跨线程同步；后台遍历应拥有稳定的数据快照或独占容器，结果再通过消息传回。

### 最容易出现的错误

不要解引用 end/sentinel；不要在活跃迭代器存在时复制或修改隐式共享容器；不要缓存容器元素引用跨越可能重分配的操作。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMultiMapIterator` 所属机制类型：迭代器与范围机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
