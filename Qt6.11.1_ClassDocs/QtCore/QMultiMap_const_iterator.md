# QMultiMap::const_iterator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMultiMap::const_iterator` 是容器或范围的迭代器类型，用于按约定遍历元素；重点是有效期、可写性和失效规则。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMultiMap::const_iterator` 是 迭代器与范围机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 迭代器表示容器或目录遍历中的当前位置，通常通过 begin/end 或 range-for 使用。迭代器是否可写、是否支持随机跳转、end/sentinel 如何表示结束，取决于具体类型。

**适用场景：** 优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要解引用 end/sentinel；不要在活跃迭代器存在时复制或修改隐式共享容器；不要缓存容器元素引用跨越可能重分配的操作。

## 2. 依赖与对象关系

- 头文件：`#include <QMultiMap>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

### 公有类型

- `iterator_category`

### 公有函数

- `const_iterator()`
- `const_iterator(const QMultiMap<Key, T>::iterator &other)`
- `const Key & key() const`
- `const T & value() const`
- `const T & operator*() const`
- `QMultiMap<Key, T>::const_iterator & operator++()`
- `QMultiMap<Key, T>::const_iterator operator++(int)`
- `QMultiMap<Key, T>::const_iterator & operator--()`
- `QMultiMap<Key, T>::const_iterator operator--(int)`
- `const T * operator->() const`

### 相关非成员函数

- `bool operator!=(const QMultiMap<Key, T>::const_iterator &lhs, const QMultiMap<Key, T>::const_iterator &rhs)`
- `bool operator==(const QMultiMap<Key, T>::const_iterator &lhs, const QMultiMap<Key, T>::const_iterator &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 14 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias] const_iterator::iterator_category`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的配置属性。初始化或状态切换时通过 `setIterator_category(...)` 设置，之后用 `iterator_category()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:iterator_category`。
- 属性名：`const_iterator`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_iterator::const_iterator()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_iterator::const_iterator(const QMultiMap<Key, T>::iterator &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QMultiMap<Key, T>::iterator &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const Key &const_iterator::key() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::const_iterator::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const Key &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const Key &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &const_iterator::value() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QMultiMap::const_iterator` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &const_iterator::operator*() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator &const_iterator::operator++()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator const_iterator::operator++(int)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator &const_iterator::operator--()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator const_iterator::operator--(int)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T *const_iterator::operator->() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const T *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QMultiMap<Key, T>::const_iterator &lhs, const QMultiMap<Key, T>::const_iterator &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMultiMap<Key, T>::const_iterator &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiMap<Key, T>::const_iterator &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QMultiMap<Key, T>::const_iterator &lhs, const QMultiMap<Key, T>::const_iterator &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap::const_iterator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMultiMap<Key, T>::const_iterator &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiMap<Key, T>::const_iterator &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iterator_category`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap::const_iterator` 的 `iterator、类别` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QMultiMap::const_iterator` 所属机制类型：迭代器与范围机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
