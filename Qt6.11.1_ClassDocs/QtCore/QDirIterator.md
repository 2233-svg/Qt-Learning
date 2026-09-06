# QDirIterator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDirIterator` 是容器或范围的迭代器类型，用于按约定遍历元素；重点是有效期、可写性和失效规则。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDirIterator` 是 迭代器与范围机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 迭代器表示容器或目录遍历中的当前位置，通常通过 begin/end 或 range-for 使用。迭代器是否可写、是否支持随机跳转、end/sentinel 如何表示结束，取决于具体类型。

**适用场景：** 优先使用类支持的 range-for 或 STL/ranges 算法，明确 const 与可写迭代器的区别；目录 sentinel 类型使用 C++20 ranges 或 Qt 推荐的范围写法。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要解引用 end/sentinel；不要在活跃迭代器存在时复制或修改隐式共享容器；不要缓存容器元素引用跨越可能重分配的操作。

## 2. 依赖与对象关系

- 头文件：`#include <QDirIterator>`
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

### 公有类型

- `enum IteratorFlag { NoIteratorFlags, Subdirectories, FollowSymlinks }`
- `flags IteratorFlags`

### 公有函数

- `QDirIterator(const QDir &dir, QDirIterator::IteratorFlags flags = NoIteratorFlags)`
- `QDirIterator(const QString &path, QDirIterator::IteratorFlags flags = NoIteratorFlags)`
- `QDirIterator(const QString &path, QDir::Filters filters, QDirIterator::IteratorFlags flags = NoIteratorFlags)`
- `QDirIterator(const QString &path, const QStringList &nameFilters, QDir::Filters filters = QDir::NoFilter, QDirIterator::IteratorFlags flags = NoIteratorFlags)`
- `~QDirIterator()`
- `QFileInfo fileInfo() const`
- `QString fileName() const`
- `QString filePath() const`
- `bool hasNext() const`
- `QString next()`
- `(since 6.3) QFileInfo nextFileInfo()`
- `QString path() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDirIterator::IteratorFlagflags QDirIterator::IteratorFlags`

**作用与语义：**

这个枚举描述了你可以组合起来配置`QDirIterator`行为的标志。
- `QDirIterator::NoIteratorFlags`：`0x0`;默认值，表示无标志。迭代器将返回分配路径的条目。
- `QDirIterator::Subdirectories`：`0x2`;所有子目录中的条目也列出。
- `QDirIterator::FollowSymlinks`：`0x1`;当与子目录结合时，该标志使得遍历指定路径的所有子目录，遵循所有符号链路。符号链路循环（例如，“link” => “.” 或 “link” => “..”）会自动检测并忽略。
IteratorFlags 类型是 QFlags 的 typedef<IteratorFlag>。它存储 IteratorFlag 值的 OR 组合。

### `QDirIterator::QDirIterator(const QDir &dir, QDirIterator::IteratorFlags flags = NoIteratorFlags)`

**作用与语义：**

构建一个QDirIterator，可以遍历`dir`的条目列表，使用`dir`的名称过滤器和常规过滤器。你可以通过`flags`传递选项，决定目录的迭代方式。
默认情况下，`flags`是`NoIteratorFlags`，这与`QDir::entryList()`中行为相同。
`dir`的分院被忽略了。
注意：要列出指向不存在文件的符号链接，必须`QDir::System`传递给旗标。

### `QDirIterator::QDirIterator(const QString &path, QDirIterator::IteratorFlags flags = NoIteratorFlags)`

**作用与语义：**

构建一个可以迭代`path`的QDirIterator。你可以通过`flags`传递选项，决定目录的迭代方式。
默认情况下，`flags`是`NoIteratorFlags`，这与`QDir::entryList()`中表现相同。
注意：要列出指向不存在文件的符号链接，必须`QDir::System`传递给旗标。

### `QDirIterator::QDirIterator(const QString &path, QDir::Filters filters, QDirIterator::IteratorFlags flags = NoIteratorFlags)`

**作用与语义：**

构建了一个可以对`path`进行迭代的QDirIterator，无需名称过滤，且`filters`条目过滤。您可以通过`flags`传递选项，决定目录的迭代方式。
默认情况下，`filters`是`QDir::NoFilter`，`flags`是`NoIteratorFlags`，这与`QDir::entryList()`中表现相同。
注意：要列出指向不存在文件的符号链接，必须`QDir::System`传递给旗标。

### `QDirIterator::QDirIterator(const QString &path, const QStringList &nameFilters, QDir::Filters filters = QDir::NoFilter, QDirIterator::IteratorFlags flags = NoIteratorFlags)`

**作用与语义：**

构建一个QDirIterator，可以对`path`进行迭代，使用`nameFilters`和 `filters`。你可以通过 `flags` 传递选项，决定目录的复制方式。
默认情况下，`flags`是`NoIteratorFlags`，这与`QDir::entryList()`提供相同的行为。
例如，以下迭代器可用于对音频文件进行迭代：
注意：要列出指向不存在文件的符号链接，必须将`QDir::System`传递给旗标。

**官方示例：**

```cpp
 QDirIterator audioFileIt(audioPath, {"*.mp3", "*.wav"}, QDir::Files);
```

### `[noexcept] QDirIterator::~QDirIterator()`

**作用与语义：**

摧毁了`QDirIterator`。

### `QFileInfo QDirIterator::fileInfo() const`

**作用与语义：**

返回当前目录条目的`QFileInfo`。

### `QString QDirIterator::fileName() const`

**作用与语义：**

返回当前目录条目的文件名，不加路径。
这个功能在迭代单个目录时非常方便。使用 `QDirIterator::Subdirectories` 标志时，可以使用 `filePath()` 获取完整路径。

### `QString QDirIterator::filePath() const`

**作用与语义：**

返回当前目录条目的完整文件路径。

### `bool QDirIterator::hasNext() const`

**作用与语义：**

如果目录中至少还有一个条目，返回`true`;否则返回 false。

### `QString QDirIterator::next()`

**作用与语义：**

将迭代器推进到下一个条目，并返回该新条目的文件路径。如果`hasNext()`返回`false`，该函数不做任何操作，返回空`QString`。理想情况下，你应在调用此方法前先调用`hasNext()`。
你可以调用`fileName()`或`filePath()`获取当前条目的文件名或路径，或者`fileInfo()`获取当前条目的`QFileInfo`。
如果你对`QFileInfo`感兴趣，请打电话给`nextFileInfo()`而不是next()。

### `[since 6.3] QFileInfo QDirIterator::nextFileInfo()`

**作用与语义：**

将迭代器推进到下一个条目，并返回该新条目的文件信息。如果`hasNext()`返回`false`，这个函数什么都不做，只返回一个空`QFileInfo`。理想情况下，你应该在调用此方法之前先调用`hasNext()`。
你可以调用`fileName()`或`filePath()`获取当前条目的文件名或路径，或者`fileInfo()`获取当前条目的`QFileInfo`。
当你只需要`filePath()`时，打电话给`next()`而不是nextFileInfo()。

### `QString QDirIterator::path() const`

**作用与语义：**

返回迭代器的基础目录。

### `enum IteratorFlag { NoIteratorFlags, Subdirectories, FollowSymlinks }`

**作用与语义：**

这个枚举描述了你可以组合起来配置`QDirIterator`行为的标志。
- `QDirIterator::NoIteratorFlags`：`0x0`;默认值，表示无标志。迭代器将返回分配路径的条目。
- `QDirIterator::Subdirectories`：`0x2`;所有子目录中的条目也列出。
- `QDirIterator::FollowSymlinks`：`0x1`;当与子目录结合时，该标志使得遍历指定路径的所有子目录，遵循所有符号链路。符号链路循环（例如，“link” => “.” 或 “link” => “..”）会自动检测并忽略。
IteratorFlags 类型是 QFlags 的 typedef<IteratorFlag>。它存储 IteratorFlag 值的 OR 组合。

### `flags IteratorFlags`

**作用与语义：**

这个枚举描述了你可以组合起来配置`QDirIterator`行为的标志。
- `QDirIterator::NoIteratorFlags`：`0x0`;默认值，表示无标志。迭代器将返回分配路径的条目。
- `QDirIterator::Subdirectories`：`0x2`;所有子目录中的条目也列出。
- `QDirIterator::FollowSymlinks`：`0x1`;当与子目录结合时，该标志使得遍历指定路径的所有子目录，遵循所有符号链路。符号链路循环（例如，“link” => “.” 或 “link” => “..”）会自动检测并忽略。
IteratorFlags 类型是 QFlags 的 typedef<IteratorFlag>。它存储 IteratorFlag 值的 OR 组合。

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

`QDirIterator` 所属机制类型：迭代器与范围机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
