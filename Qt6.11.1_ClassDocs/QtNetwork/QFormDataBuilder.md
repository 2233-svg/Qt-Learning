# QFormDataBuilder
> Qt 6.11.1 · Qt Network · 来自 `QFormDataBuilder`

## 作用定位
`QFormDataBuilder` 是 Qt 6 的表单构建器，用声明式 API 生成带普通字段和文件字段的 multipart form-data 内容。

## API 速查
| API | 是做什么的 |
|---|---|
| `setName()` | 设置表单/部件名称。|
| `setValue()` | 设置文本或二进制字段值。|
| `setFileName()` | 设置上传文件名。|
| `setMimeType()` | 设置文件 MIME 类型。|
| `setBodyDevice()` | 使用流设备作为数据源。|
| `build()` | 构建对应 form-data 对象。|

## 使用场景
封装通用 REST 上传接口，避免每处手写 multipart header。

## 常见坑与经验
- builder 只构造描述，body device 的有效期仍要由调用者管理。
- 自动探测 MIME 类型不一定符合服务端约定，关键接口应显式设置。

## 知识点覆盖
表单编码、构建器、文件上传、MIME、资源生命周期。
