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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QShaderBaker::GeneratedShader`

**作用与语义：**

STD的同义词：:p air<`QShader::Source`，`QShaderVersion`>。

### `enum class QShaderBaker::GlslOptionflags QShaderBaker::GlslOptions`

**作用与语义：**

- `QShaderBaker::GlslOption::GlslEsFragDefaultFloatPrecisionMedium`：`0x01`;GLSL ES的片段着色器中`precision mediump float;`
GlslOptions 类型是 QFlags 的 typedef<GlslOption>。它存储 GlslOption 值的 OR 组合。

### `enum class QShaderBaker::SpirvOptionflags QShaderBaker::SpirvOptions`

**作用与语义：**

- `QShaderBaker::SpirvOption::GenerateFullDebugInfo`：`0x01`;在SPIR-V二进制文件中生成并存储额外的调试信息。
- `QShaderBaker::SpirvOption::StripDebugAndVarInfo`：`0x02`;从SPIR-V二进制文件中剔除所有调试和变量名信息。
SpirvOptions 类型是 QFlag 的 typedef<SpirvOption>。它存储 SpirvOption 值的 OR 组合。

### `QShaderBaker::QShaderBaker()`

**作用与语义：**

他构建了一个新的QShaderBaker。

### `[noexcept] QShaderBaker::~QShaderBaker()`

**作用与语义：**

毁灭者。

### `QShader QShaderBaker::bake()`

**作用与语义：**

负责编译和翻译过程。
返回一个`QShader`实例。要检查进程是否成功，请调用`QShader::isValid()`。当表示 `false` 时，调用 `errorMessage()` 以获取日志。
这是一个昂贵的操作。在应用程序中调用时，建议在单独的线程中执行。
注意：`QShaderBaker`实例可重用：调用 bake() 后，同一实例可以再次用于不同的输入。然而，`QShaderBaker`实例在其生命周期内应仅在一个线程上使用。

### `QString QShaderBaker::errorMessage() const`

**作用与语义：**

返回上次`bake()`运行时的错误消息，若无错误则返回空字符串。
注意：错误包括文件读取错误、编译和翻译失败。不请求任何目标或变体不算错误，尽管最终`QShader`无效。

### `void QShaderBaker::setBatchableVertexShaderExtraInputLocation(int location)`

**作用与语义：**

生成`QShader::BatchableVertexShader`变体时，`location`指定插入顶点输入的输入位置。该值默认为7，只有当顶点着色器已经使用输入位置7时才需要覆盖。

### `void QShaderBaker::setBreakOnShaderTranslationError(bool enable)`

**作用与语义：**

控制着色器转换失败（从SPIR-V到GLSL/HLSL/MSL）失败时的行为。默认情况下，该设置为真，如果无法生成请求的着色器，`bake()`会返回错误。如果不希望如此，且意图是生成能生成的着色器但静默跳过其余部分，则将`enable`设为false。
针对多个 GLSL 版本可能导致错误，因为某个功能无法转换为某个版本。例如，尝试用 textureSize() 将着色器翻译成 GLSL ES 100 会整个 `bake()` 调用失败，错误信息为“textureSize is not supported in ESSL 100”。如果即使请求，结果中不包含 GLSL ES 100 着色器是可以接受的，那么将该标志设为 false 会使`bake()`成功。

### `void QShaderBaker::setGeneratedShaderVariants(const QList<QShader::Variant> &v)`

**作用与语义：**

指定生成哪些着色器变体。每个着色器版本的最终`QShader`中可以有多个变体。
大多数情况下，`v`只包含一个条目，`QShader::StandardShader`。
注意：当未设置变体时，生成的`QShader`将为空，因此无效。

### `void QShaderBaker::setGeneratedShaders(const QList<QShaderBaker::GeneratedShader> &v)`

**作用与语义：**

指定要编译或转换到哪种着色器。默认情况下没有生成任何函数，所以必须在 `bake()` 之前调用这个函数。
注意：当未调用该函数或`v`空或仅包含无效条目时，生成的`QShader`将为空，因此无效。
例如，最小可能的烘焙目标是SPIR-V，且不需额外翻译到其他语言。请求此目标时，请执行：
注意：`QShaderBaker`仅处理SPIR-V和人类可读源目标。进一步编译为API专用中间格式（如`QShader::DxbcShader`或`QShader::MetalLibShader`）由`qsb`命令行工具实现，不包含在`QShaderBaker`运行时API中。

**官方示例：**

```cpp
 baker.setGeneratedShaders({ QShader::SpirvShader, QShaderVersion(100) });
```

### `[since 6.9] void QShaderBaker::setGlslOptions(QShaderBaker::GlslOptions options)`

**作用与语义：**

为生成的GLSL和GLSL ES源设置额外`options`。默认情况下不设置任何标志。

### `[since 6.7] void QShaderBaker::setMultiViewCount(int count)`

**作用与语义：**

在使用多视图转译着色器时（例如顶点着色器使用gl_ViewIndex渲染器，依赖GL_OVR_multiview2、VK_KHR_multiview等），部分目标需要声明着色器中的视图数量。这在Vulkan风格的GLSL代码中不存在，也对SPIR-V或HLSL等目标不相关，但对OpenGL和GLSL是必需的，因此必须作为额外元数据提供该值。
默认值为0，这会禁用注入`num_views`语句。设置1无用，因为无论如何都是默认`num_views`。因此，`count`应为>= 2才能产生效果。例如，当设置为2时，生成的GLSL着色器将包含`layout(num_views = 2) in;`语句。
设置`count`为2或更大还会注入一些预处理器语句：`QSHADER_VIEW_COUNT`设置为`count`，而`GL_EXT_multiview`扩展则自动启用。因此，设置合适的`count`也可以适用于其他类型的着色器，例如当顶点和片段之间共享统一缓冲区时，两个着色器都必须能够写出类似`#if QSHADER_VIEW_COUNT >= 2`的内容。

### `void QShaderBaker::setPerTargetCompilation(bool enable)`

**作用与语义：**

将每个目标的编译设置为`enable`。默认情况下，该功能被禁用，意味着每个变体将 Vulkan/GLSL 源代码编译为 SPIR-V。（因此默认为一次，如果是顶点着色器则编译两次，按要求编译为批量可变体）。生成的 SPIR-V 随后被翻译成各种目标语言（GLSL、HLSL、MSL）。
在每个目标编译模式下，每个目标都有单独的GLSL到SPIR-V编译步骤，即每个通过`setGeneratedShaders()`请求的GLSL/HLSL/MSL版本。输入源相同，但插入了针对特定目标的预处理器。这需要更多时间，但允许应用程序提供单一着色器，并用`#ifdef`块进行区分。当该模式被禁用时，唯一实现相同效果的方法是提供多个版本的着色器文件，分别处理每个版本，为每个版本发送{.qsb}文件，并根据运行逻辑选择合适的文件。
以下宏将在该模式下自动定义。注意，宏始终绑定于着色语言，而非图形API。
- `QSHADER_SPIRV` - 定义在针对SPIR-V（通常由Vulkan消耗）时。
- `QSHADER_SPIRV_VERSION` - 目标SPIR-V版本号，如`100`。
- `QSHADER_GLSL` - 在针对GLSL或GLSL ES（通常由OpenGL或OpenGL ES消耗）时定义
- `QSHADER_GLSL_VERSION` - 目标GLSL或GLSL ES版本号，如`100`、`300`或`330`。
- `QSHADER_GLSL_ES` - 仅在针对GLSL ES时定义
- `QSHADER_HLSL` - 在针对HLSL（通常由直接3D消耗）时定义
- `QSHADER_HLSL_VERSION` - 目标HLSL着色器模型版本，如`50`
- `QSHADER_MSL` - 针对金属阴影语言定义（通常由金属用户使用）
- `QSHADER_MSL_VERSION` - 目标MSL版本，如`12`或`20`。
这允许编写如下着色器代码。
注意：版本号遵循受GLSL启发的`QShaderVersion`语法，因此始终为单整数。
注意：每个`QShader`只有一个`QShaderDescription`，无论有多少个独立目标。因此，统一块、顶点输入等的成员不得使用上述宏的条件。
警告：请注意图形API和着色语言概念的区别。`QShaderBaker`及相关工具严格遵循着色语言的概念，忽略了结果之后如何被消费。因此，如果Qt图形栈的高层有一天也开始为非Vulkan的API使用SPIR-V，那么认为QSHADER_SPIRV意味着Vulkan的假设将不再成立。

**官方示例：**

```cpp
 #if QSHADER_HLSL || QSHADER_MSL
 vec2 uv = vec2(uv_coord.x, 1.0 - uv_coord.y);
 #else
 vec2 uv = uv_coord;
 #endif
```

### `void QShaderBaker::setPreamble(const QByteArray &preamble)`

**作用与语义：**

指定一个自定义`preamble`，在正常着色器代码之前处理。
这不仅仅是在源字符串前加：GLSL 版本指令的有效性（必须置于所有指令之前）不受影响。报告错误消息中的行号也保持不变，忽略`preamble`中给出的内容。
前言的一个用例是透明地插入动态生成的`#define`语句。

### `void QShaderBaker::setSourceDevice(QIODevice *device, QShader::Stage stage, const QString &fileName = QString())`

**作用与语义：**

设置源 `device`。这允许使用任意`QIODevice`而不仅仅是文件。`stage` 指定着色器阶段，而可选的 `fileName` 包含错误信息中使用的文件名。
警告：`device`预计包含可信内容。建议应用开发者在从非应用控制的来源传递用户提供的数据前，仔细考虑潜在影响。

### `void QShaderBaker::setSourceFileName(const QString &fileName)`

**作用与语义：**

将着色器源文件的名称设置为`fileName`。这是调用`bake()`时将要读取的文件。着色器阶段是通过文件扩展名自动推导出来的。如果不希望或无法实现，则使用带有阶段参数的超载功能。
支持的文件扩展名有：
- `.vert` - 顶点着色器
- `.frag` - 片段（像素）着色器
- `.tesc` - 镶嵌控制（船体）着色器
- `.tese` - 镶嵌评估（域）着色器
- `.geom` - 几何着色器
- `.comp` - 计算着色器
警告：`fileName`预计包含可信内容。建议应用开发者在提交非应用部分的用户提供源文件前仔细考虑潜在影响。

### `void QShaderBaker::setSourceFileName(const QString &fileName, QShader::Stage stage)`

**作用与语义：**

将着色器源文件的名称设置为`fileName`。这是调用`bake()`时将要读取的文件。着色器阶段由`stage`指定。
警告：`fileName`预计包含可信内容。建议应用开发者在提交非应用部分的用户提供的源文件前，仔细考虑潜在影响。

### `void QShaderBaker::setSourceString(const QByteArray &sourceString, QShader::Stage stage, const QString &fileName = QString())`

**作用与语义：**

设置输入着色器`sourceString`。`stage`指定着色器阶段，而可选`fileName`包含用于错误信息的文件名。
警告：`sourceString`预计包含可信内容。建议应用开发者在从非应用控制的来源传递用户提供的数据前，仔细考虑潜在影响。

### `void QShaderBaker::setSpirvOptions(QShaderBaker::SpirvOptions options)`

**作用与语义：**

为生成的SPIR-V二进制设置额外`options`。默认情况下不设置任何标志。

### `void QShaderBaker::setTessellationMode(QShaderDescription::TessellationMode mode)`

**作用与语义：**

在为镶嵌控制着色器生成MSL着色器代码时，必须事先知道镶嵌`mode`（三角形或四边形）。在GLSL中，这通常在镶嵌评估着色器中声明，但对于Metal，在从镶嵌控制着色器生成计算着色器时也必须知道。
未设置时默认为三角形。

### `void QShaderBaker::setTessellationOutputVertexCount(int count)`

**作用与语义：**

在为镶嵌评估着色器生成MSL着色器代码时，必须事先知道镶嵌控制着色器的输出顶点`count`。在GLSL中，通常会在镶嵌控制着色器中声明这一点，但在Metal中，在从镶嵌评估着色器生成顶点着色器时也必须知道。
未设置时，默认值为3。

### `GeneratedShader`

**作用与语义：**

STD的同义词：:p air<`QShader::Source`，`QShaderVersion`>。

### `enum class GlslOption { GlslEsFragDefaultFloatPrecisionMedium }`

**作用与语义：**

- `QShaderBaker::GlslOption::GlslEsFragDefaultFloatPrecisionMedium`：`0x01`;GLSL ES的片段着色器中`precision mediump float;`
GlslOptions 类型是 QFlags 的 typedef<GlslOption>。它存储 GlslOption 值的 OR 组合。

### `flags GlslOptions`

**作用与语义：**

- `QShaderBaker::GlslOption::GlslEsFragDefaultFloatPrecisionMedium`：`0x01`;GLSL ES的片段着色器中`precision mediump float;`
GlslOptions 类型是 QFlags 的 typedef<GlslOption>。它存储 GlslOption 值的 OR 组合。

### `enum class SpirvOption { GenerateFullDebugInfo, StripDebugAndVarInfo }`

**作用与语义：**

- `QShaderBaker::SpirvOption::GenerateFullDebugInfo`：`0x01`;在SPIR-V二进制文件中生成并存储额外的调试信息。
- `QShaderBaker::SpirvOption::StripDebugAndVarInfo`：`0x02`;从SPIR-V二进制文件中剔除所有调试和变量名信息。
SpirvOptions 类型是 QFlag 的 typedef<SpirvOption>。它存储 SpirvOption 值的 OR 组合。

### `flags SpirvOptions`

**作用与语义：**

- `QShaderBaker::SpirvOption::GenerateFullDebugInfo`：`0x01`;在SPIR-V二进制文件中生成并存储额外的调试信息。
- `QShaderBaker::SpirvOption::StripDebugAndVarInfo`：`0x02`;从SPIR-V二进制文件中剔除所有调试和变量名信息。
SpirvOptions 类型是 QFlag 的 typedef<SpirvOption>。它存储 SpirvOption 值的 OR 组合。

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
