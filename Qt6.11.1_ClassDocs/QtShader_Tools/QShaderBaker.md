# QShaderBaker

> Qt 6.11.1 · Qt Shader Tools

## 1. 先建立直觉

**一句话定位：** 这是 Qt Shader Tools 中围绕“着色器Baker”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Shader Tools 提供着色器翻译、预处理和图形管线工具。

### 这是什么

`QShaderBaker` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QShaderBaker>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

- `GeneratedShader`
- `enum class GlslOption { GlslEsFragDefaultFloatPrecisionMedium }`
- `flags GlslOptions`
- `enum class SpirvOption { GenerateFullDebugInfo, StripDebugAndVarInfo }`
- `flags SpirvOptions`

### 公有函数

- `QShaderBaker()`
- `~QShaderBaker()`
- `QShader bake()`
- `QString errorMessage() const`
- `void setBatchableVertexShaderExtraInputLocation(int location)`
- `void setBreakOnShaderTranslationError(bool enable)`
- `void setGeneratedShaderVariants(const QList<QShader::Variant> &v)`
- `void setGeneratedShaders(const QList<QShaderBaker::GeneratedShader> &v)`
- `(since 6.9) void setGlslOptions(QShaderBaker::GlslOptions options)`
- `(since 6.7) void setMultiViewCount(int count)`
- `void setPerTargetCompilation(bool enable)`
- `void setPreamble(const QByteArray &preamble)`
- `void setSourceDevice(QIODevice *device, QShader::Stage stage, const QString &fileName = QString())`
- `void setSourceFileName(const QString &fileName)`
- `void setSourceFileName(const QString &fileName, QShader::Stage stage)`
- `void setSourceString(const QByteArray &sourceString, QShader::Stage stage, const QString &fileName = QString())`
- `void setSpirvOptions(QShaderBaker::SpirvOptions options)`
- `void setTessellationMode(QShaderDescription::TessellationMode mode)`
- `void setTessellationOutputVertexCount(int count)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 27 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias] QShaderBaker::GeneratedShader`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShaderBaker` 的配置属性。初始化或状态切换时通过 `setGeneratedShader(...)` 设置，之后用 `GeneratedShader()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:GeneratedShader`。
- 属性名：`QShaderBaker`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QShaderBaker::GlslOptionflags QShaderBaker::GlslOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShaderBaker` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:GlslOptionflags QShaderBaker::GlslOptions`。
- 属性名：`QShaderBaker`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QShaderBaker::SpirvOptionflags QShaderBaker::SpirvOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShaderBaker` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SpirvOptionflags QShaderBaker::SpirvOptions`。
- 属性名：`QShaderBaker`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShaderBaker::QShaderBaker()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShaderBaker` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QShaderBaker::~QShaderBaker()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShaderBaker` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader QShaderBaker::bake()`

**API 类别：** 成员函数说明

**中文解读：** `QShaderBaker::bake` 用于计算、查询或取得与“bake”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QShader`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QShader`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QShaderBaker::errorMessage() const`

**API 类别：** 成员函数说明

**中文解读：** `QShaderBaker::errorMessage` 用于计算、查询或取得与“错误、Message”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setBatchableVertexShaderExtraInputLocation(int location)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBatchableVertexShaderExtraInputLocation`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setBreakOnShaderTranslationError(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBreakOnShaderTranslationError`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setGeneratedShaderVariants(const QList<QShader::Variant> &v)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeneratedShaderVariants`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `v`：类型为 `const QList<QShader::Variant> &`。没有默认值，调用时必须提供。传入 `const QList<QShader::Variant> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setGeneratedShaders(const QList<QShaderBaker::GeneratedShader> &v)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeneratedShaders`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `v`：类型为 `const QList<QShaderBaker::GeneratedShader> &`。没有默认值，调用时必须提供。传入 `const QList<QShaderBaker::GeneratedShader> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QShaderBaker::setGlslOptions(QShaderBaker::GlslOptions options)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGlslOptions`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `options`：类型为 `QShaderBaker::GlslOptions`。没有默认值，调用时必须提供。传入 `QShaderBaker::GlslOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QShaderBaker::setMultiViewCount(int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMultiViewCount`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setPerTargetCompilation(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPerTargetCompilation`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setPreamble(const QByteArray &preamble)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPreamble`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `preamble`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setSourceDevice(QIODevice *device, QShader::Stage stage, const QString &fileName = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceDevice`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `stage`：类型为 `QShader::Stage`。没有默认值，调用时必须提供。传入 `QShader::Stage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fileName`：类型为 `const QString &`。默认值为 `QString()`。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setSourceFileName(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceFileName`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setSourceFileName(const QString &fileName, QShader::Stage stage)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceFileName`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `stage`：类型为 `QShader::Stage`。没有默认值，调用时必须提供。传入 `QShader::Stage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setSourceString(const QByteArray &sourceString, QShader::Stage stage, const QString &fileName = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceString`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sourceString`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `stage`：类型为 `QShader::Stage`。没有默认值，调用时必须提供。传入 `QShader::Stage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fileName`：类型为 `const QString &`。默认值为 `QString()`。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setSpirvOptions(QShaderBaker::SpirvOptions options)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSpirvOptions`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `options`：类型为 `QShaderBaker::SpirvOptions`。没有默认值，调用时必须提供。传入 `QShaderBaker::SpirvOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setTessellationMode(QShaderDescription::TessellationMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTessellationMode`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QShaderDescription::TessellationMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShaderBaker::setTessellationOutputVertexCount(int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTessellationOutputVertexCount`。调用它会改变 `QShaderBaker` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GeneratedShader`

**API 类别：** 公有类型

**中文解读：** 这是 `QShaderBaker` 的 `Generated、Shader` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class GlslOption { GlslEsFragDefaultFloatPrecisionMedium }`

**API 类别：** 公有类型

**中文解读：** 这是 `QShaderBaker` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags GlslOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QShaderBaker` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class SpirvOption { GenerateFullDebugInfo, StripDebugAndVarInfo }`

**API 类别：** 公有类型

**中文解读：** 这是 `QShaderBaker` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags SpirvOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QShaderBaker` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QShaderBaker` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
