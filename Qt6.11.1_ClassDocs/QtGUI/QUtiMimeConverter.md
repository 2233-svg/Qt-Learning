# QUtiMimeConverter
> Qt 6.11.1 · Qt GUI · 来自 `QUtiMimeConverter`

## 1. 先建立直觉

`QUtiMimeConverter` 是 macOS/iOS 平台上 Uniform Type Identifier 和 MIME 类型之间的转换扩展点。它服务于剪贴板、拖放等平台数据交换。

普通应用大多不需要碰它；只有平台集成或需要支持自定义 UTI 数据类型时才会用。

## 2. 类说明

- 头文件：`#include <QUtiMimeConverter>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：平台 MIME 转换接口
- 适用平台：Apple 平台 UTI 体系

它负责把 Qt 的 `QMimeData` 与平台原生 UTI 数据互相转换。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `utiForMime(mimeType)` | 给 MIME 类型返回平台 UTI |
| `mimeForUti(uti)` | 给 UTI 返回 MIME 类型 |
| `canConvertFromMime()` | 判断能否从 Qt MIME 转成 UTI |
| `convertFromMime()` | 从 `QMimeData` 生成平台数据 |
| `canConvertToMime()` | 判断能否从 UTI 转成 Qt MIME |
| `convertToMime()` | 从平台数据生成 Qt MIME 数据 |

## 4. 关键用法

自定义转换器的价值在“声明格式映射”和“实际转换字节”。例如把应用私有对象拖到 Finder 或从其他原生 App 接收自定义 UTI。

## 5. 使用场景

- macOS 剪贴板支持自定义 UTI。
- 拖放和其他原生应用交换专有数据。
- Qt 平台插件或集成层扩展。

## 6. 常见坑与经验

- MIME 与 UTI 并非一一对应，可能需要多个候选和优先级。
- 转换数据要考虑安全性，不要信任外部 App 提供的字节。
- 普通跨平台剪贴板优先用标准 MIME，如 `text/plain`、`text/uri-list`、`image/png`。

## 7. 知识点覆盖

UTI/MIME 映射、剪贴板、拖放、平台数据转换、自定义格式。
