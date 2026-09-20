# QJsonDocument
> Qt 6.11.1 · Qt Core · 来自 `QJsonDocument`

## 作用定位
`QJsonDocument` 是 JSON 根文档值类型，根只能是对象或数组。它负责从文本解析 JSON、生成紧凑或缩进文本，并与二进制 JSON/variant 表示转换。

## API 速查
| API | 是做什么的 |
|---|---|
| `fromJson()` | 从 UTF-8 JSON 文本解析文档。|
| `toJson()` | 输出 Compact 或 Indented JSON 文本。|
| `isObject()` / `isArray()` | 判断根类型。|
| `object()` / `array()` | 取得根对象或根数组。|
| `setObject()` / `setArray()` | 设置根内容。|
| `fromVariant()` / `toVariant()` | 与 QVariant 树转换。|
| `isNull()` / `isEmpty()` | 判断无文档或空根。|

## 使用场景
读取配置文件、解析 HTTP JSON 响应、生成请求 body 或导出结构化数据。

## 常见坑与经验
- `fromJson()` 必须配合 `QJsonParseError`，不要将空 document 当成“服务器返回空对象”。
- JSON 数字使用双精度表示，大整数 ID 可能失去精度；超过安全范围的 ID 应用字符串传输。
- 文档根不能直接是标量，标量需包在对象或数组中。

## 知识点覆盖
JSON 文档、UTF-8 解析、格式化输出、解析错误、数值精度、QVariant 互操作。
