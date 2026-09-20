# QShaderCode
> Qt 6.11.1 · Qt GUI · 来自 `QShaderCode`

## 1. 先建立直觉

`QShaderCode` 是一段 shader 代码加入口点名称的简单容器。代码可以是文本源，也可以是二进制字节码；它并不解释内容，具体含义由外层 `QShaderKey::source()` 决定。

## 2. 类说明

- 头文件：`#include <QShaderCode>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型，可比较、可哈希
- 协作类：`QShader`、`QShaderKey`

`QShaderCode` 只保存 `QByteArray`。GLSL 文本、SPIR-V、DXBC、DXIL、Metal library 都可以放进去，关键是外层 key 要标明类型。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建空代码对象 |
| `QShaderCode(code, entry)` | 保存代码和入口点 |
| `setShader()` / `shader()` | 设置或读取代码字节 |
| `setEntryPoint()` / `entryPoint()` | 设置或读取入口函数名 |
| `operator==` / `operator!=` / `qHash()` | 用于比较和缓存 |

## 4. 关键用法

```cpp
QShaderCode code(spirvBytes, "main");
shader.setShader(QShaderKey(QShader::SpirvShader, QShaderVersion(100)), code);
```

入口点为空时，后端或工具通常会使用默认入口，例如 `main`。但当一个库或字节码里有多个入口时，应明确设置。

## 5. 使用场景

- 从 `.qsb` 包里读取某个后端版本。
- 构建工具把编译后的字节码塞进 `QShader`。
- 对 shader 包做去重、缓存、比较。
- 调试时导出某个后端生成的 shader 文本。

## 6. 常见坑与经验

- 不要通过 `shader()` 的字节内容猜语言；语言类型在 `QShaderKey`。
- 文本 shader 建议明确编码为 UTF-8 字节。
- 入口点和代码不匹配时，错误通常在后端创建 pipeline 时才出现。
- `QShaderCode` 不做编译和验证，它只是容器。

## 7. 知识点覆盖

本页覆盖：shader 字节容器、入口点、文本源与二进制代码、`QShaderKey` 分工、缓存比较。
