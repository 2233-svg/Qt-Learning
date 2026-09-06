# QStringTokenizer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“StringTokenizer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringTokenizer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStringTokenizer>`
- 继承自：QtPrivate::Tok::HaystackPinning (private)、QtPrivate::Tok::NeedlePinning (private)、and
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `const_iterator`
- `const_pointer`
- `const_reference`
- `difference_type`
- `iterator`
- `pointer`
- `reference`
- `sentinel`
- `size_type`
- `value_type`

### 公有函数

- `QStringTokenizer(Haystack haystack, Needle needle, Qt::CaseSensitivity cs, Qt::SplitBehavior sb = Qt::KeepEmptyParts)`
- `QStringTokenizer(Haystack haystack, Needle needle, Qt::SplitBehavior sb = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringTokenizer<Haystack, Needle>::iterator begin() const`
- `QStringTokenizer<Haystack, Needle>::iterator cbegin() const`
- `QStringTokenizer<Haystack, Needle>::sentinel cend() const`
- `QStringTokenizer<Haystack, Needle>::sentinel end() const`
- `LContainer toContainer(LContainer &&c = {}) const &`
- `RContainer toContainer(RContainer &&c = {}) const &&`

### 相关非成员函数

- `(since 6.0) auto qTokenize(Haystack &&haystack, Needle &&needle, Flags... flags)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QStringTokenizer::const_iterator`

**作用与语义：**

该typedef为`QStringTokenizer`提供了一个STL风格的const迭代器。

### `[alias] QStringTokenizer::const_pointer`

**作用与语义：**

`value_type *`的别名。

### `[alias] QStringTokenizer::const_reference`

**作用与语义：**

`value_type &`的别名。

### `[alias] QStringTokenizer::difference_type`

**作用与语义：**

qsizetype 的别名。

### `[alias] QStringTokenizer::iterator`

**作用与语义：**

该typedef为`QStringTokenizer`提供了STL风格的const迭代器。
`QStringTokenizer`不支持可变迭代器，所以这和`const_iterator`一样。

### `[alias] QStringTokenizer::pointer`

**作用与语义：**

`value_type *`的别名。
`QStringTokenizer`不支持可变迭代器，所以这和`const_pointer`一样。

### `[alias] QStringTokenizer::reference`

**作用与语义：**

`value_type &`的别名。
`QStringTokenizer`不支持可变引用，所以这和`const_reference`一样。

### `[alias] QStringTokenizer::sentinel`

**作用与语义：**

该typedef为`QStringTokenizer::iterator`和`QStringTokenizer::const_iterator`提供了类似STL风格的哨兵。

### `[alias] QStringTokenizer::size_type`

**作用与语义：**

qsizetype 的别名。

### `[alias] QStringTokenizer::value_type`

**作用与语义：**

`const QStringView`或`const QLatin1StringView`的别名，取决于分词器的`Haystack`模板参数。

### `[explicit constexpr noexcept(...)] QStringTokenizer::QStringTokenizer(Haystack haystack, Needle needle, Qt::SplitBehavior sb = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

构建一个字符串分词器，它会在每当 `needle` 出现的时候，将字符串 `haystack` 分割成子字符串，并允许在找到这些子字符串时进行迭代。如果 `needle` 在 `haystack` 中未匹配到任何内容，则会产生一个包含 `haystack` 的单个元素。
`cs` 指定 `needle` 是否应区分大小写匹配。
如果 `sb` 是 `Qt::SkipEmptyParts`，则空条目不会出现在结果中。默认情况下，空条目是包含的。
注意：(1) 当 `std::is_nothrow_copy_constructible<QStringTokenizer>::value` 是 `true` 时，不会抛出异常。
注意：(2) 当 `std::is_nothrow_copy_constructible<QStringTokenizer>::value` 是 `true` 时，不会抛出异常。

### `[noexcept] QStringTokenizer<Haystack, Needle>::iterator QStringTokenizer::cbegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向列表中的第一个令牌。

### `[constexpr noexcept] QStringTokenizer<Haystack, Needle>::sentinel QStringTokenizer::cend() const`

**作用与语义：**

和`end()`一样。

### `[constexpr noexcept] QStringTokenizer<Haystack, Needle>::sentinel QStringTokenizer::end() const`

**作用与语义：**

返回一个const STL风格的哨兵，指向列表中最后一个令牌之后的虚数令牌。

### `template <typename LContainer> LContainer QStringTokenizer::toContainer(LContainer &&c = {}) const &`

**作用与语义：**

将懒惰序列转换为（通常）类型为`LContainer`的随机访问容器。
该函数仅在`Container`的`value_type`与该分词器`value_type`匹配时可用。
如果你输入一个命名容器（lvalue）作为`c`，那么该容器已被填充，并返回对它的引用。如果你输入一个临时容器（r值，包含默认参数），那么该容器被填充，并返回值。
这让你在存储序列时有最大的灵活性。

**官方示例：**

```cpp
 // assuming tok's value_type is QStringView, then...
 auto tok = QStringTokenizer{~~~};
 // ... rac1 is a QList:
 auto rac1 = tok.toContainer();
 // ... rac2 is std::pmr::vector<QStringView>:
 auto rac2 = tok.toContainer<std::pmr::vector<QStringView>>();
 auto rac3 = QVarLengthArray<QStringView, 12>{};
 // appends the token sequence produced by tok to rac3
 //  and returns a reference to rac3 (which we ignore here):
 tok.toContainer(rac3);
```

### `template <typename RContainer> RContainer QStringTokenizer::toContainer(RContainer &&c = {}) const &&`

**作用与语义：**

将懒惰序列转换为（通常）随机访问的`RContainer`型容器。
除了对lvalue-这个超载的约束外，这个r值-这个超载只有在该 `QStringTokenizer` 内部不存储干草堆时才可用，因为这可能会形成一个充满悬挂引用的容器：
修复方法是暂时存放这些`QStringTokenizer`：
你可以通过传递一个视图来强制启用这个函数：
如果你为`c`传递一个命名容器（lvalue），那么该容器被填满，并返回对它的引用。如果你传递一个临时容器（rvalue，包含默认参数），那么该容器被填满，并返回值。

**官方示例：**

```cpp
 auto tokens = QStringTokenizer{widget.text(), u','}.toContainer();
 // ERROR: cannot call toContainer() on rvalue
 // 'tokens' references the data of the copy of widget.text()
 // stored inside the QStringTokenizer, which has since been deleted
```

### `[constexpr noexcept(...), since 6.0] template < typename Haystack, typename Needle, typename... Flags > auto qTokenize(Haystack &&haystack, Needle &&needle, Flags... flags)`

**作用与语义：**

工厂函数，`QStringTokenizer`将字符串`haystack`分割成子串，`needle`出现时允许对这些字符串进行迭代。如果`needle`在`haystack`中任何地方不匹配，则生成包含`haystack`的单一元素。
将`Qt::CaseSensitivity`和`Qt::SplitBehavior`枚举器的值传递为`flags`以修改分词器的行为。
注意：该功能仅在`QtPrivate::Tok::is_nothrow_constructible_from<Haystack, Needle>::value` 被`true`时才使用。

### `const_iterator`

**作用与语义：**

该typedef为`QStringTokenizer`提供了一个STL风格的const迭代器。

### `const_pointer`

**作用与语义：**

`value_type *`的别名。

### `const_reference`

**作用与语义：**

`value_type &`的别名。

### `difference_type`

**作用与语义：**

qsizetype 的别名。

### `iterator`

**作用与语义：**

该typedef为`QStringTokenizer`提供了STL风格的const迭代器。
`QStringTokenizer`不支持可变迭代器，所以这和`const_iterator`一样。

### `pointer`

**作用与语义：**

`value_type *`的别名。
`QStringTokenizer`不支持可变迭代器，所以这和`const_pointer`一样。

### `reference`

**作用与语义：**

`value_type &`的别名。
`QStringTokenizer`不支持可变引用，所以这和`const_reference`一样。

### `sentinel`

**作用与语义：**

该typedef为`QStringTokenizer::iterator`和`QStringTokenizer::const_iterator`提供了类似STL风格的哨兵。

### `size_type`

**作用与语义：**

qsizetype 的别名。

### `value_type`

**作用与语义：**

`const QStringView`或`const QLatin1StringView`的别名，取决于分词器的`Haystack`模板参数。

### `QStringTokenizer(Haystack haystack, Needle needle, Qt::CaseSensitivity cs, Qt::SplitBehavior sb = Qt::KeepEmptyParts)`

**作用与语义：**

构建一个字符串分词器，它会在每当 `needle` 出现的时候，将字符串 `haystack` 分割成子字符串，并允许在找到这些子字符串时进行迭代。如果 `needle` 在 `haystack` 中未匹配到任何内容，则会产生一个包含 `haystack` 的单个元素。
`cs` 指定 `needle` 是否应区分大小写匹配。
如果 `sb` 是 `Qt::SkipEmptyParts`，则空条目不会出现在结果中。默认情况下，空条目是包含的。
注意：(1) 当 `std::is_nothrow_copy_constructible<QStringTokenizer>::value` 是 `true` 时，不会抛出异常。
注意：(2) 当 `std::is_nothrow_copy_constructible<QStringTokenizer>::value` 是 `true` 时，不会抛出异常。

### `QStringTokenizer<Haystack, Needle>::iterator begin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向列表中的第一个令牌。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStringTokenizer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
