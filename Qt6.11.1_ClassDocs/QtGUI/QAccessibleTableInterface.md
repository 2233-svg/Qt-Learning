# QAccessibleTableInterface

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是一个抽象接口或框架基类，重点是理解它定义的协议，并通过具体子类、工厂或回调来使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAccessibleTableInterface` 是 Qt GUI 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAccessibleTableInterface>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

- `virtual ~QAccessibleTableInterface()`
- `virtual QAccessibleInterface * caption() const = 0`
- `virtual QAccessibleInterface * cellAt(int row, int column) const = 0`
- `virtual int columnCount() const = 0`
- `virtual QString columnDescription(int column) const = 0`
- `virtual bool isColumnSelected(int column) const = 0`
- `virtual bool isRowSelected(int row) const = 0`
- `virtual void modelChange(QAccessibleTableModelChangeEvent *event) = 0`
- `virtual int rowCount() const = 0`
- `virtual QString rowDescription(int row) const = 0`
- `virtual bool selectColumn(int column) = 0`
- `virtual bool selectRow(int row) = 0`
- `virtual int selectedCellCount() const = 0`
- `virtual QList<QAccessibleInterface *> selectedCells() const = 0`
- `virtual int selectedColumnCount() const = 0`
- `virtual QList<int> selectedColumns() const = 0`
- `virtual int selectedRowCount() const = 0`
- `virtual QList<int> selectedRows() const = 0`
- `virtual QAccessibleInterface * summary() const = 0`
- `virtual bool unselectColumn(int column) = 0`
- `virtual bool unselectRow(int row) = 0`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 21 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[virtual noexcept] QAccessibleTableInterface::~QAccessibleTableInterface()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAccessibleTableInterface` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessibleInterface *QAccessibleTableInterface::caption() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::caption` 用于计算、查询或取得与“caption”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessibleInterface *QAccessibleTableInterface::cellAt(int row, int column) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::cellAt` 用于计算、查询或取得与“cell、按位置访问”相关的操作。调用时要先确认当前状态和 `row`、`column` 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAccessibleTableInterface::columnCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::columnCount` 用于计算、查询或取得与“列、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QString QAccessibleTableInterface::columnDescription(int column) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::columnDescription` 用于计算、查询或取得与“列、Description”相关的操作。调用时要先确认当前状态和 `column` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QAccessibleTableInterface::isColumnSelected(int column) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isColumnSelected`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QAccessibleTableInterface::isRowSelected(int row) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRowSelected`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QAccessibleTableInterface::modelChange(QAccessibleTableModelChangeEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::modelChange` 用于执行与“model、Change”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QAccessibleTableModelChangeEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAccessibleTableInterface::rowCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::rowCount` 用于计算、查询或取得与“行、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QString QAccessibleTableInterface::rowDescription(int row) const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::rowDescription` 用于计算、查询或取得与“行、Description”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QAccessibleTableInterface::selectColumn(int column)`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectColumn` 用于计算、查询或取得与“select、列”相关的操作。调用时要先确认当前状态和 `column` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QAccessibleTableInterface::selectRow(int row)`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectRow` 用于计算、查询或取得与“select、行”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAccessibleTableInterface::selectedCellCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectedCellCount` 用于计算、查询或取得与“selected、Cell、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QList<QAccessibleInterface *> QAccessibleTableInterface::selectedCells() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectedCells` 用于计算、查询或取得与“selected、Cells”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QAccessibleInterface *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QAccessibleInterface *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAccessibleTableInterface::selectedColumnCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectedColumnCount` 用于计算、查询或取得与“selected、列、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QList<int> QAccessibleTableInterface::selectedColumns() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectedColumns` 用于计算、查询或取得与“selected、列”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<int>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAccessibleTableInterface::selectedRowCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectedRowCount` 用于计算、查询或取得与“selected、行、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QList<int> QAccessibleTableInterface::selectedRows() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::selectedRows` 用于计算、查询或取得与“selected、行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<int>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QAccessibleInterface *QAccessibleTableInterface::summary() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::summary` 用于计算、查询或取得与“summary”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QAccessibleTableInterface::unselectColumn(int column)`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::unselectColumn` 用于计算、查询或取得与“unselect、列”相关的操作。调用时要先确认当前状态和 `column` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QAccessibleTableInterface::unselectRow(int row)`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleTableInterface::unselectRow` 用于计算、查询或取得与“unselect、行”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

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

`QAccessibleTableInterface` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
