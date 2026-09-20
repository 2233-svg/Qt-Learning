# Qt QShaderCode：一份 shader 源码或字节码

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QShaderCode>`  
> RHI 头文件：`#include <rhi/qshader.h>`  
> 所属模块：`Qt6::Gui` / RHI  
> 继承：无  
> 类型定位：shader 代码和入口点的轻量值类型

## 1. 它解决什么问题

`QShaderCode` 保存一份 shader 的实际代码和入口点名称。代码可以是：

- GLSL、HLSL、MSL、WGSL 等源代码；
- SPIR-V、DXBC、DXIL、Metal library 等二进制字节码。

它解决的是“`QShader` 的某个 `QShaderKey` 对应哪段代码、从哪个入口点开始执行”的数据承载问题。`QShaderCode` 本身不记录代码属于哪种语言或哪个管线阶段；这些信息由外层的 `QShaderKey` 和 `QShader::Stage` 提供。

它也不是编译器、反射器或 GPU shader module。把一段字符串放进 `QShaderCode` 不会自动检查语法，也不会生成其他后端代码。

## 2. 构建与兼容性

文档页列出的包含方式是：

```cpp
#include <QShaderCode>
```

但 `QShaderCode` 属于 Qt RHI API。Qt 6.11.1 文档明确提示，`QShader`、`QShaderCode` 和相关 QRhi 类型没有源代码兼容性和二进制兼容性保证。使用 RHI 头文件时，通常应使用：

```cpp
#include <rhi/qshader.h>
```

并链接 `Qt::GuiPrivate`：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::GuiPrivate)
```

qmake 工程至少需要：

```qmake
QT += gui
```

不要把 `QShaderCode` 暴露在跨 Qt 小版本的公共 ABI 中，也不要依赖其内部成员布局。

## 3. 最小使用方式

### 3.1 保存源代码和入口点

```cpp
#include <rhi/qshader.h>

QShaderCode vertexCode()
{
    return QShaderCode(
        QByteArrayLiteral("#version 450\nvoid main() {}"),
        QByteArrayLiteral("main"));
}
```

`QShaderCode` 只保存 bytes。上面的 GLSL 是否可编译，需要由 `qsb`、`QShaderBaker` 或目标图形 API 验证。

### 3.2 作为 `QShader` 的 key 值

```cpp
QShader shader;
shader.setStage(QShader::VertexStage);

QShaderKey key(QShader::GlslShader, QShaderVersion(450));
shader.setShader(key, vertexCode());

const QShaderCode code = shader.shader(key);
if (code.shader().isEmpty()) {
    // 没有找到这个精确 key 的代码。
}
```

`QShaderKey` 决定 source、版本和 variant；`QShaderCode` 决定实际 bytes 和入口点。两者必须和生成工具输出保持一致。

## 4. 核心使用模型

### 4.1 代码和入口点是两个独立字段

结构可以理解为：

```text
QShaderCode
  ├─ shader()      -> 源代码或字节码
  └─ entryPoint()  -> 入口点名称
```

代码可以非空而入口点为空，也可以通过 setter 分别修改两个字段。Qt 不会从 GLSL、HLSL 或其他源代码中自动解析入口点。

### 4.2 字节内容是 opaque data

`shader()` 返回 `QByteArray`，它没有类型标签，也不会因为写入了 SPIR-V magic number 就自动识别格式。调用方和外层 `QShaderKey::source()` 共同决定如何解释这些 bytes。

不要把二进制 shader 当作以零结尾的 C 字符串；处理字节码时使用 `QByteArray::size()` 和字节接口，不要无条件调用 `constData()` 后按字符串读取。

### 4.3 空代码有明确查询语义

Qt 文档特别说明：当从 `QShader` 取出的 `QShaderCode` 的 `shader()` 为空时，表示请求的 key 没有找到 shader code。它不是“QShaderCode 默认构造一定代表有效空 shader”，也不是编译错误对象。

如果应用自己把空 `QByteArray` 写入某个 key，查询也会得到空代码；业务层应自行决定是否把这种条目视为无效。

### 4.4 入口点名称由生成器和语言决定

SPIR-V、HLSL、MSL 和 WGSL 可能使用不同的入口点命名规则。应把生成器实际输出的入口点写入 `entryPoint()`，不要假设所有代码都叫 `main`。

某些后端可能允许或默认使用空入口点，但 `QShaderCode` 本身不定义这种 fallback。是否允许为空取决于外层 shader 工具和后端消费者。

## 5. 实际使用场景

### 5.1 `qsb` 生成的多后端 shader package

生产环境通常由 `qsb` 生成多个 `QShaderCode`，每份代码使用不同 `QShaderKey` 保存到 `QShader`。应用运行时选择一个精确 key，再把结果交给 QRhi。

### 5.2 运行时 shader 工具

材质编辑器或开发工具可以通过 `QShaderBaker` 运行时生成代码，使用 `QShaderCode` 检查输出 bytes 和入口点，再序列化到 package。运行时编译成本较高，不适合普通应用每次启动都执行。

### 5.3 代码和字节码诊断

工具可以根据 `QShaderKey::source()` 选择不同的展示方式：

- GLSL、HLSL、MSL、WGSL：按文本显示；
- SPIR-V、DXBC、DXIL、MetalLib：按二进制大小、哈希或反汇编结果显示。

不要只看 `QByteArray::isEmpty()` 就判断代码“可执行”；非空 bytes 仍可能是截断文件、错误格式或与 key 不匹配的内容。

### 5.4 自定义 shader 容器

应用可以用 `QShaderCode` 作为自己的中间值类型，把源代码、入口点和 `QShaderKey` 一起交给 package 构建器。但应用需要自己负责版本、编码、错误和生成器一致性。

## 6. 生命周期、所有权和线程

### 6.1 轻量值类型

`QShaderCode` 不继承 `QObject`，不拥有 GPU 资源或外部内存。它可以按值返回、复制、放入 `QList` 或作为信号参数。内部 `QByteArray` 具有 Qt 的值语义和隐式共享特性。

### 6.2 修改是值修改

`shader()` 和 `entryPoint()` 都按值返回 `QByteArray`。修改查询结果不会改变原对象：

```cpp
QByteArray bytes = code.shader();
bytes.append(extraData); // 不会修改 code
```

需要修改对象时调用 `setShader()` 或 `setEntryPoint()`。

### 6.3 可以跨线程复制，但不代表 GPU 资源可跨线程使用

作为值对象，`QShaderCode` 可以复制到工作线程生成或检查。但 QRhi pipeline、shader module 和渲染设备有自己的线程约束。不要因为代码 bytes 可以跨线程传递，就在工作线程直接修改正在被渲染线程消费的 pipeline。

### 6.4 `QByteArray` 的数据生命周期

传入构造函数或 setter 的 `QByteArray` 按值保存；调用方可以在函数返回后销毁原始变量。返回的 `QByteArray` 也是独立的值语义对象，适合复制给异步任务。

## 7. 与相关类型的边界

### 7.1 与 `QShaderKey`

`QShaderKey` 说明代码的 source、版本和 variant；`QShaderCode` 保存 bytes 和入口点。只看 `QShaderCode` 无法知道代码该交给哪个后端。

### 7.2 与 `QShader`

`QShader` 以 `QShaderKey -> QShaderCode` 的形式保存多份代码，并额外保存 stage、反射和后端映射。单独的 `QShaderCode` 不具备 `QShader` 的 package 和序列化能力。

### 7.3 与 `QShaderBaker`

`QShaderBaker` 负责从源代码生成多后端结果、反射和 package；`QShaderCode` 只是其中每份输出的承载类型。

### 7.4 与 `QShaderDescription`

`QShaderDescription` 描述 shader 的输入、输出和资源；`QShaderCode` 不提供反射。代码非空并不说明资源 binding 或 vertex input 正确。

### 7.5 与 `QRhiShaderStage`

QRhi 的 shader stage 配置需要 stage 和 `QShader` 等信息。`QShaderCode` 不能直接替代完整 `QShader` package，也不会创建底层 shader module。

## 8. 常见误区与排查顺序

### 8.1 把 `QShaderCode` 当作编译结果

构造 `QShaderCode(source, entry)` 不会编译。先用 `qsb` 或 `QShaderBaker` 验证，再将生成结果放入 `QShader`。

### 8.2 用错 source key

把 GLSL bytes 放进 `QShaderKey` 标记为 SPIR-V，或者把 DXIL 当成 DXBC，会让后端以错误格式解释数据。排查时同时记录 key 的 source、version、variant 和 bytes 大小。

### 8.3 入口点一律写 `main`

`main` 是常见约定，不是 `QShaderCode` 强制值。对于生成器输出的 HLSL、MSL 或 WGSL，入口点可能不同。

### 8.4 只检查 `QByteArray` 非空

非空只表示有 bytes，不表示语法、版本、资源布局和后端兼容性正确。仍需经过编译工具和实际 pipeline 创建验证。

### 8.5 把二进制代码当 C 字符串

SPIR-V、DXBC、DXIL 和 Metal library 可以包含零字节。用 `QByteArray` 的长度语义处理，不要使用依赖 `'\0'` 终止的字符串函数。

### 8.6 修改 `shader()` 返回值期待原对象变化

查询按值返回。修改临时 `QByteArray` 不会写回，必须调用 `setShader()`。

### 8.7 忽略 RHI 的有限兼容性

`QShaderCode` 属于 RHI API。不要将它的二进制布局、序列化细节或内部约定跨 Qt 小版本保存为公共 ABI。

### 8.8 直接加载不可信 shader bytes

shader package 和 shader bytes 应视为可信资产。用户可控的 shader 输入可能触发编译器、驱动或资源解析风险，应在产品层面限制来源并做大小、格式和版本控制。

## 9. 逐项 API 说明

### 构造函数

#### `[constexpr noexcept] QShaderCode::QShaderCode()`

默认构造一个空的 `QShaderCode`。`shader()` 和 `entryPoint()` 都为空。默认对象适合表示“还没有代码”的中间状态；不要将其当作已经可执行的 shader。

#### `QShaderCode::QShaderCode(const QByteArray &code, const QByteArray &entry = QByteArray())`

用代码 bytes 和入口点名称创建对象。`code` 可以是源代码或字节码，`entry` 默认为空。

构造函数不检查代码格式、不验证入口点是否存在，也不根据代码内容推断 source、stage 或版本。

### 代码字段

#### `QByteArray QShaderCode::shader() const`

返回 shader 源代码或字节码。返回值按 `QByteArray` 值语义提供；二进制数据应使用长度接口处理。

当该对象是从 `QShader::shader(key)` 取得的结果时，空返回值表示该精确 key 没有找到代码。

#### `void QShaderCode::setShader(const QByteArray &code)`

设置 shader 源代码或字节码。它只替换代码 bytes，不会自动修改入口点、`QShaderKey`、stage、反射描述或其他 package 元数据。

### 入口点字段

#### `QByteArray QShaderCode::entryPoint() const`

返回入口点名称。返回值为空时，不代表 Qt 会自动选择 `main`；具体是否允许由目标语言、生成器和后端决定。

#### `void QShaderCode::setEntryPoint(const QByteArray &entry)`

设置入口点名称。它只替换名称，不会检查该名称是否出现在 shader bytes 中，也不会重新编译代码。

### 相关非成员

#### `[noexcept] bool operator==(const QShaderCode &lhs, const QShaderCode &rhs)`

比较两个 `QShaderCode` 的值是否相等，包括代码 bytes 和入口点。它不比较外层 `QShaderKey`、stage 或反射信息。

#### `[noexcept] bool operator!=(const QShaderCode &lhs, const QShaderCode &rhs)`

返回 `operator==` 的反值。

#### `[noexcept] size_t qHash(const QShaderCode &key, size_t seed = 0)`

为 `QShaderCode` 提供哈希值，可用于 `QHash` 或 `QSet`。哈希是进程内容器用途，不是稳定文件指纹或安全校验值。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QShaderCode()` | 创建空代码对象 | code 和入口点为空；不是可执行 shader |
| 构造 | `QShaderCode(const QByteArray &code, const QByteArray &entry = QByteArray())` | 保存代码 bytes 和入口点 | 不验证格式、stage、source 或入口点存在性 |
| 查询 | `QByteArray shader() const` | 获取源代码或字节码 | 空值从 `QShader` 查询时表示精确 key 未找到；二进制不能按 C 字符串处理 |
| 写入 | `setShader(const QByteArray &code)` | 替换代码 bytes | 不修改入口点、key、stage 或反射描述 |
| 查询 | `QByteArray entryPoint() const` | 获取入口点名称 | 不保证自动 fallback 到 `main` |
| 写入 | `setEntryPoint(const QByteArray &entry)` | 替换入口点名称 | 不检查代码中是否真的存在该入口 |
| 比较 | `operator==(const QShaderCode &, const QShaderCode &)` | 比较代码和入口点值 | 不比较外层 key、stage、反射和后端 |
| 比较 | `operator!=(const QShaderCode &, const QShaderCode &)` | `operator==` 的反值 | 仍是值比较，不是编译兼容性判断 |
| 哈希 | `qHash(const QShaderCode &, size_t seed = 0)` | 用于 `QHash`/`QSet` | 不是稳定文件 ID 或安全哈希 |
| 相关 | `QShaderKey` | 描述 source、版本和 variant | `QShaderCode` 本身不带格式标签 |
| 相关 | `QShader` | 按 key 保存多份代码和 package 元数据 | 单个 code 不能替代完整 shader package |
| 相关 | `QShaderBaker` | 生成代码、反射和 package | 编译/转换职责不属于 `QShaderCode` |
| 相关 | `QShaderDescription` | 描述资源和接口反射 | 代码非空不等于反射和资源布局正确 |
| 兼容性 | RHI API | 提供 Qt 的 shader 代码值类型 | 无源/二进制兼容保证，应锁定 Qt 版本 |

---

### 一句话总结

`QShaderCode` 是一份 shader bytes 加入口点的轻量值类型：它不记录 source 或 stage，不编译、不反射、不创建 GPU 资源；使用时通过外层 `QShaderKey` 解释代码，区分文本与二进制，明确入口点，并把非空 bytes 之外的格式、版本和资源正确性留给生成工具与后端验证。
