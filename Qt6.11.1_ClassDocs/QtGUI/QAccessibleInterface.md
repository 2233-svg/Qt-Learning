# QAccessibleInterface

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是一个抽象接口或框架基类，重点是理解它定义的协议，并通过具体子类、工厂或回调来使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAccessibleInterface` 是 Qt GUI 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAccessibleInterface>`
- 继承自：未在类页中列出
- 直接派生类：QAccessibleObject

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QAccessibleActionInterface * actionInterface()`
- `virtual QColor backgroundColor() const`
- `virtual QAccessibleInterface * child(int index) const = 0`
- `virtual QAccessibleInterface * childAt(int x, int y) const = 0`
- `virtual int childCount() const = 0`
- `virtual QAccessibleInterface * focusChild() const`
- `virtual QColor foregroundColor() const`
- `virtual int indexOfChild(const QAccessibleInterface *child) const = 0`
- `virtual void * interface_cast(QAccessible::InterfaceType type)`
- `virtual bool isValid() const = 0`
- `virtual QObject * object() const = 0`
- `virtual QAccessibleInterface * parent() const = 0`
- `virtual QRect rect() const = 0`
- `virtual QList<std::pair<QAccessibleInterface *, QAccessible::Relation>> relations(QAccessible::Relation match = QAccessible::AllRelations) const`
- `virtual QAccessible::Role role() const = 0`
- `(since 6.5) QAccessibleSelectionInterface * selectionInterface()`
- `virtual void setText(QAccessible::Text t, const QString &text) = 0`
- `virtual QAccessible::State state() const = 0`
- `QAccessibleTableCellInterface * tableCellInterface()`
- `QAccessibleTableInterface * tableInterface()`
- `virtual QString text(QAccessible::Text t) const = 0`
- `QAccessibleTextInterface * textInterface()`
- `QAccessibleValueInterface * valueInterface()`
- `virtual QWindow * window() const`

### 保护函数

- `virtual ~QAccessibleInterface()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 25 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[virtual noexcept protected] QAccessibleInterface::~QAccessibleInterface()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAccessibleInterface` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QColor QAccessibleInterface::backgroundColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::backgroundColor` 用于计算、查询或取得与“background、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessibleInterface *QAccessibleInterface::child(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::child` 用于计算、查询或取得与“child”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessibleInterface *QAccessibleInterface::childAt(int x, int y) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::childAt` 用于计算、查询或取得与“child、按位置访问”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAccessibleInterface::childCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::childCount` 用于计算、查询或取得与“child、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QAccessibleInterface *QAccessibleInterface::focusChild() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::focusChild` 用于计算、查询或取得与“focus、Child”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QColor QAccessibleInterface::foregroundColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::foregroundColor` 用于计算、查询或取得与“foreground、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAccessibleInterface::indexOfChild(const QAccessibleInterface *child) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::indexOfChild` 用于计算、查询或取得与“索引、Of、Child”相关的操作。调用时要先确认当前状态和 `child` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `child`：类型为 `const QAccessibleInterface *`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void *QAccessibleInterface::interface_cast(QAccessible::InterfaceType type)`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::interface_cast` 用于计算、查询或取得与“interface、cast”相关的操作。调用时要先确认当前状态和 `type` 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数 `type`：类型为 `QAccessible::InterfaceType`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QAccessibleInterface::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QObject *QAccessibleInterface::object() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::object` 用于计算、查询或取得与“object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessibleInterface *QAccessibleInterface::parent() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::parent` 用于计算、查询或取得与“父对象”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRect QAccessibleInterface::rect() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::rect` 用于计算、查询或取得与“rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QList<std::pair<QAccessibleInterface *, QAccessible::Relation>> QAccessibleInterface::relations(QAccessible::Relation match = QAccessible::AllRelations) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::relations` 用于计算、查询或取得与“relations”相关的操作。调用时要先确认当前状态和 `match` 的有效范围；返回类型是 `QList<std::pair<QAccessibleInterface *, QAccessible::Relation>>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<std::pair<QAccessibleInterface *, QAccessible::Relation>>`。
- 参数 `match`：类型为 `QAccessible::Relation`。默认值为 `QAccessible::AllRelations`。传入 `QAccessible::Relation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessible::Role QAccessibleInterface::role() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::role` 用于计算、查询或取得与“角色”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessible::Role`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessible::Role`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QAccessibleSelectionInterface *QAccessibleInterface::selectionInterface()`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::selectionInterface` 用于计算、查询或取得与“selection、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleSelectionInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleSelectionInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QAccessibleInterface::setText(QAccessible::Text t, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setText`。调用它会改变 `QAccessibleInterface` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `QAccessible::Text`。没有默认值，调用时必须提供。传入 `QAccessible::Text` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessible::State QAccessibleInterface::state() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessible::State`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessible::State`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QString QAccessibleInterface::text(QAccessible::Text t) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::text` 用于计算、查询或取得与“文本”相关的操作。调用时要先确认当前状态和 `t` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `t`：类型为 `QAccessible::Text`。没有默认值，调用时必须提供。传入 `QAccessible::Text` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QWindow *QAccessibleInterface::window() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleInterface::window` 用于计算、查询或取得与“window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWindow *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWindow *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAccessibleActionInterface * actionInterface()`

**API 类别：** 公有函数

**中文解读：** `QAccessibleInterface::actionInterface` 用于计算、查询或取得与“action、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleActionInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleActionInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAccessibleTableCellInterface * tableCellInterface()`

**API 类别：** 公有函数

**中文解读：** `QAccessibleInterface::tableCellInterface` 用于计算、查询或取得与“table、Cell、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleTableCellInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleTableCellInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAccessibleTableInterface * tableInterface()`

**API 类别：** 公有函数

**中文解读：** `QAccessibleInterface::tableInterface` 用于计算、查询或取得与“table、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleTableInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleTableInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAccessibleTextInterface * textInterface()`

**API 类别：** 公有函数

**中文解读：** `QAccessibleInterface::textInterface` 用于计算、查询或取得与“文本、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleTextInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleTextInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAccessibleValueInterface * valueInterface()`

**API 类别：** 公有函数

**中文解读：** `QAccessibleInterface::valueInterface` 用于计算、查询或取得与“值访问、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleValueInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleValueInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAccessibleInterface` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
