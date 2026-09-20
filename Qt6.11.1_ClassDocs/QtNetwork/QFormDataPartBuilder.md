# QFormDataPartBuilder
> Qt 6.11.1 · Qt Network · 来自 `QFormDataPartBuilder`

## 作用定位
`QFormDataPartBuilder` 描述 multipart 表单中的单个字段，负责名称、值、文件名、MIME 类型和数据设备。

## API 速查
| API | 是做什么的 |
|---|---|
| `setName()` | 设置 form 字段名。|
| `setBody()` | 设置内存内容。|
| `setBodyDevice()` | 设置流式内容设备。|
| `setFileName()` | 设置文件字段名。|
| `setMimeType()` | 设置内容类型。|
| `build()` | 生成可加入表单的部分。|

## 使用场景
在同一个上传请求中分别创建 metadata 文本字段与 image 文件字段。

## 常见坑与经验
- 普通文本字段也应使用明确 UTF-8 编码，避免服务端按本地编码误解。
- 设备必须已打开并保持有效，直到网络请求完成。

## 知识点覆盖
表单字段、文件字段、UTF-8、流式上传、构建器。
