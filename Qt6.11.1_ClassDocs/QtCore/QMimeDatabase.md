# QMimeDatabase
> Qt 6.11.1 · Qt Core · 来自 `QMimeDatabase`

## 作用定位
`QMimeDatabase` 查询系统和 Qt 的 MIME 类型数据库，可通过名称、文件名模式或文件内容识别类型。

## API 速查
| API | 是做什么的 |
|---|---|
| `mimeTypeForName()` | 按 MIME 名称查类型。|
| `mimeTypeForFile(fileName)` | 按文件名模式匹配类型。|
| `mimeTypeForFile(fileInfo, mode)` | 指定按扩展名或内容匹配。|
| `mimeTypeForData()` | 根据字节内容嗅探 MIME 类型。|
| `allMimeTypes()` | 枚举已知类型。|
| `suffixForFileName()` | 从路径提取最匹配扩展名。|

## 使用场景
导入文件时给出合理预览、选择正确解码器、构建文件过滤器或检查下载响应内容。

## 常见坑与经验
- 文件扩展名和 MIME 声明都可伪造；安全敏感场景要解析真实格式并限制允许类型。
- 内容嗅探可能涉及 I/O 且并非总能识别，不能把 Unknown 当成安全。
- 数据库内容依平台和部署环境变化，测试目标系统而不是只测开发机。

## 知识点覆盖
MIME、文件类型识别、扩展名、内容嗅探、跨平台、输入安全。
