# QRegularExpressionMatchIterator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 正则匹配结果迭代器，负责遍历同一文本中的多次匹配。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRegularExpressionMatchIterator`：正则匹配结果迭代器，负责遍历同一文本中的多次匹配。

**内部模型：** 迭代器表示容器或目录遍历中的当前位置，通常通过 begin/end 或 range-for 使用。迭代器是否可写、是否支持随机跳转、end/sentinel 如何表示结束，取决于具体类型。

**适用场景：** 优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要解引用 end/sentinel；不要在活跃迭代器存在时复制或修改隐式共享容器；不要缓存容器元素引用跨越可能重分配的操作。

## 2. 依赖与对象关系

- 头文件：`#include <QRegularExpressionMatchIterator>`
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

优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
for (auto it = container.cbegin(); it != container.cend(); ++it) {
    // 读取 *it，不要在遍历期间让 container 发生会使迭代器失效的修改
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRegularExpressionMatchIterator()`
- `QRegularExpressionMatchIterator(const QRegularExpressionMatchIterator &iterator)`
- `(since 6.1) QRegularExpressionMatchIterator(QRegularExpressionMatchIterator &&iterator)`
- `~QRegularExpressionMatchIterator()`
- `bool hasNext() const`
- `bool isValid() const`
- `QRegularExpression::MatchOptions matchOptions() const`
- `QRegularExpression::MatchType matchType() const`
- `QRegularExpressionMatch next()`
- `QRegularExpressionMatch peekNext() const`
- `QRegularExpression regularExpression() const`
- `void swap(QRegularExpressionMatchIterator &other)`
- `QRegularExpressionMatchIterator & operator=(QRegularExpressionMatchIterator &&iterator)`
- `QRegularExpressionMatchIterator & operator=(const QRegularExpressionMatchIterator &iterator)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QRegularExpressionMatchIterator::QRegularExpressionMatchIterator()`

**作用与语义：**

构造一个空的有效QRegularExpressionMatchIterator对象。正则表达式设置为默认构造的;匹配类型为`QRegularExpression::NoMatch`，匹配选项为`QRegularExpression::NoMatchOption`。
在构造对象上调用`hasNext()`成员函数会返回false，因为迭代器没有在有效的匹配序列上迭代。

### `QRegularExpressionMatchIterator::QRegularExpressionMatchIterator(const QRegularExpressionMatchIterator &iterator)`

**作用与语义：**

构建一个QRegularExpressionMatchIterator对象，作为`iterator`的副本。

### `[constexpr noexcept, since 6.1] QRegularExpressionMatchIterator::QRegularExpressionMatchIterator(QRegularExpressionMatchIterator &&iterator)`

**作用与语义：**

通过从 `iterator` 移动构建 QRegularExpressionMatchIterator 对象。
注意，移动 QRegularExpressionMatchIterator 只能被销毁或赋值。调用除解构函数或赋值操作符外的其他函数效果未定义。

### `[noexcept] QRegularExpressionMatchIterator::~QRegularExpressionMatchIterator()`

**作用与语义：**

摧毁`QRegularExpressionMatchIterator`物体。

### `bool QRegularExpressionMatchIterator::hasNext() const`

**作用与语义：**

如果迭代前方至少有一个匹配结果，返回`true`;否则返回`false`。

### `bool QRegularExpressionMatchIterator::isValid() const`

**作用与语义：**

如果迭代对象是从对有效`QRegularExpression`对象调用的`QRegularExpression::globalMatch()`函数获得的，返回`true`;返回 `false` 如果`QRegularExpression`无效。

### `QRegularExpression::MatchOptions QRegularExpressionMatchIterator::matchOptions() const`

**作用与语义：**

返回用于获得该`QRegularExpressionMatchIterator`对象的匹配选项，即传递给`QRegularExpression::globalMatch()`的匹配选项。

### `QRegularExpression::MatchType QRegularExpressionMatchIterator::matchType() const`

**作用与语义：**

返回用于获得该`QRegularExpressionMatchIterator`对象的匹配类型，也就是传递给`QRegularExpression::globalMatch()`的匹配类型。

### `QRegularExpressionMatch QRegularExpressionMatchIterator::next()`

**作用与语义：**

返回下一场比赛结果，并将迭代器前进一位。
注意：当迭代器位于结果集末尾时调用该函数会导致未定义的结果。

### `QRegularExpressionMatch QRegularExpressionMatchIterator::peekNext() const`

**作用与语义：**

返回下一个匹配结果，无需移动迭代器。
注意：当迭代器位于结果集末尾时调用该函数会导致未定义的结果。

### `QRegularExpression QRegularExpressionMatchIterator::regularExpression() const`

**作用与语义：**

返回 globalMatch() 函数返回该对象的 `QRegularExpression` 对象。

### `[noexcept] void QRegularExpressionMatchIterator::swap(QRegularExpressionMatchIterator &other)`

**作用与语义：**

将这个迭代器与`other`交换。这个操作非常快，从未失败过。

### `[noexcept] QRegularExpressionMatchIterator &QRegularExpressionMatchIterator::operator=(QRegularExpressionMatchIterator &&iterator)`

**作用与语义：**

Move-assign `iterator` 到该对象，并返回对结果的引用。
注意，移出`QRegularExpressionMatchIterator`只能被销毁或分配到。调用除解构器或赋值操作符外的其他函数效果尚无定义。

### `QRegularExpressionMatchIterator &QRegularExpressionMatchIterator::operator=(const QRegularExpressionMatchIterator &iterator)`

**作用与语义：**

将迭代器`iterator`分配给该对象，并返回对该副本的引用。

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

`QRegularExpressionMatchIterator` 所属机制类型：迭代器与范围机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
