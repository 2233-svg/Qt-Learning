# QCache

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QCache` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCache` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QCache>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

### 状态、生命周期和线程

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QCache(qsizetype maxCost = 100)`
- `~QCache()`
- `void clear()`
- `bool contains(const Key &key) const`
- `qsizetype count() const`
- `bool insert(const Key &key, T *object, qsizetype cost = 1)`
- `bool isEmpty() const`
- `QList<Key> keys() const`
- `qsizetype maxCost() const`
- `T * object(const Key &key) const`
- `bool remove(const Key &key)`
- `void setMaxCost(qsizetype cost)`
- `qsizetype size() const`
- `T * take(const Key &key)`
- `qsizetype totalCost() const`
- `T * operator[](const Key &key) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit noexcept] QCache::QCache(qsizetype maxCost = 100)`

**作用与语义：**

构建一个缓存，其内容总成本永远不会超过`maxCost`。

### `QCache::~QCache()`

**作用与语义：**

销毁缓存。删除缓存中的所有对象。

### `[noexcept(...)] void QCache::clear()`

**作用与语义：**

删除缓存中的所有对象。
注意：该功能仅在`std::is_nothrow_destructible_v<Node>`为`true`时使用。

### `[noexcept] bool QCache::contains(const Key &key) const`

**作用与语义：**

如果缓存包含与密钥`key`相关的对象，返回`true`;否则返回`false`。

### `[noexcept] qsizetype QCache::count() const`

**作用与语义：**

和`size()`一样。

### `bool QCache::insert(const Key &key, T *object, qsizetype cost = 1)`

**作用与语义：**

插入`object`到缓存中，密钥`key`及其相关成本`cost`。缓存中已有相同密钥的对象将被移除。
调用后，`object`归`QCache`所有，随时可被删除。特别是，如果`cost`大于`maxCost()`，该对象将立即被删除。
如果对象入缓存，函数返回`true`;否则返回`false`。

### `[noexcept] bool QCache::isEmpty() const`

**作用与语义：**

如果缓存中没有对象，返回`true`;否则返回`false`。

### `QList<Key> QCache::keys() const`

**作用与语义：**

返回缓存中的密钥列表。

### `[noexcept] qsizetype QCache::maxCost() const`

**作用与语义：**

返回缓存的最大允许总成本。

### `[noexcept] T *QCache::object(const Key &key) const`

**作用与语义：**

返回与密钥`key`关联的对象;如果缓存中不存在密钥，则返回`nullptr`。
警告：归还的物品归`QCache`所有，随时可能被删除。

### `[noexcept(...)] bool QCache::remove(const Key &key)`

**作用与语义：**

删除与密钥`key`相关的对象。如果该对象在缓存中被发现，返回`true`;否则返回`false`。
注意：该功能仅在`std::is_nothrow_destructible_v<Node>` `true`时使用。

### `[noexcept(...)] void QCache::setMaxCost(qsizetype cost)`

**作用与语义：**

将缓存的最大允许总成本设置为`cost`。如果当前总成本大于`cost`，部分对象会立即被删除。
注意：该功能仅在`std::is_nothrow_destructible_v<Node>` `true`时才适用。

### `[noexcept] qsizetype QCache::size() const`

**作用与语义：**

返回缓存中的对象数量。

### `[noexcept(...)] T *QCache::take(const Key &key)`

**作用与语义：**

将与密钥 `key` 关联的对象从缓存中移除，但不删除该对象。返回指向被移除对象的指针，如果缓存中不存在密钥则返回 0。
返回对象的所有权转移给调用者。
注意：该功能仅在`std::is_nothrow_destructible_v<Key>` `true`时才使用。

### `[noexcept] qsizetype QCache::totalCost() const`

**作用与语义：**

返回缓存中对象的总成本。
该值通常低于`maxCost()`，但`QCache`对Qt隐式共享类有例外。如果缓存对象与另一个实例共享内部数据，`QCache`可能会让该对象保持闲置，可能导致总成本()大于`maxCost()`。

### `[noexcept] T *QCache::operator[](const Key &key) const`

**作用与语义：**

返回与密钥`key`关联的对象，如果密钥不存在于缓存中，则返回`nullptr`。
这和`object()`一样。
警告：返回的物品归`QCache`所有，可能随时被删除。

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCache` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
