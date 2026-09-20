# QHttpPart
> Qt 6.11.1 · Qt Network · 来自 `QHttpPart`

## 作用定位
`QHttpPart` 是 multipart 请求中的一个部分，携带该部分独立的头字段和内存数据或 `QIODevice` 数据体。

## API 速查
| API | 是做什么的 |
|---|---|
| `setHeader()` | 设置 Content-Disposition 等已知头。|
| `setRawHeader()` | 设置任意部分头。|
| `setBody()` | 用内存字节作为内容。|
| `setBodyDevice()` | 用流设备作为内容，适合大文件。|

## 使用场景
为上传文件设置 `Content-Disposition: form-data; name="file"; filename="..."`，并以 `QFile` 作为 body device。

## 常见坑与经验
- `setBody()` 会将内容放在内存；大文件应使用已打开的 `QFile`。
- filename 需要按 MIME/HTTP 规则正确编码，不能直接信任用户输入。

## 知识点覆盖
multipart part、Content-Disposition、文件流、内存占用、文件名编码。
