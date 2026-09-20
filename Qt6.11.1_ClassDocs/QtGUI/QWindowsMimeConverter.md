# QWindowsMimeConverter
> Qt 6.11.1 · Qt GUI · 来自 `QWindowsMimeConverter`

## 1. 先建立直觉

`QWindowsMimeConverter` 是 Windows 平台剪贴板和拖放格式与 Qt MIME 类型之间的转换接口。它把 CF_ 格式、COM IDataObject 数据和 `QMimeData` 连接起来。

普通应用通常用 `QClipboard` 和 `QMimeData` 就够了；本类面向需要支持自定义 Windows 剪贴板格式的场景。

## 2. 类说明

- 头文件：`#include <QWindowsMimeConverter>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：平台 MIME 转换接口
- 适用平台：Windows

它解决 Qt MIME 名称和 Windows 原生 format id/数据块之间的双向转换。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `formatsForMime()` | 某个 MIME 类型可转换成哪些 Windows 格式 |
| `mimeForFormat()` | 某个 Windows 格式对应哪个 MIME 类型 |
| `canConvertFromMime()` | 能否从 `QMimeData` 转为 Windows 数据 |
| `convertFromMime()` | 执行 Qt 到 Windows 原生数据转换 |
| `canConvertToMime()` | 能否从 Windows 数据转为 Qt MIME |
| `convertToMime()` | 执行 Windows 到 Qt MIME 转换 |

## 4. 关键用法

实现自定义转换器时，先注册或识别 Windows clipboard format，再把它映射到稳定 MIME 名称。应用内部也应能处理标准 MIME 作为 fallback。

## 5. 使用场景

- 与 Office、CAD、图像软件交换专有剪贴板格式。
- Windows 拖放接收自定义二进制对象。
- 平台插件或企业内部集成。

## 6. 常见坑与经验

- Windows 原生格式可能有多种同义表达，选择转换优先级很重要。
- 剪贴板数据来自外部进程，解析前必须校验大小和格式。
- 自定义格式跨平台不可用，应同时提供标准 MIME fallback。

## 7. 知识点覆盖

Windows clipboard format、MIME 映射、拖放、`QMimeData`、原生数据安全解析。
