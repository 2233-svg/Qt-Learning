# QMimeData
> Qt 6.11.1 · Qt Core · 来自 `QMimeData`

## 作用定位
`QMimeData` 是剪贴板和拖放操作的数据载体，可同时提供同一内容的文本、HTML、URL、图像、文件列表和自定义 MIME 字节。

## API 速查
| API | 是做什么的 |
|---|---|
| `setText()` / `text()` | 设置或读取纯文本。|
| `setHtml()` / `html()` | 设置或读取富文本 HTML。|
| `setUrls()` / `urls()` | 设置或读取 URL/文件列表。|
| `setImageData()` | 设置图像数据。|
| `setData(mimeType, bytes)` | 设置任意 MIME 格式字节。|
| `data()` | 读取指定 MIME 数据。|
| `formats()` | 枚举可提供格式。|
| `hasFormat()` | 判断格式是否存在。|

## 使用场景
实现拖放导入、复制粘贴、跨应用共享图片或传递自定义应用内部对象数据。

## 常见坑与经验
- 不可信拖放/剪贴板内容必须验证 MIME、大小、URL 协议和文件权限，不能根据扩展名直接执行或导入。
- 同时提供 `text/plain` 与自定义 MIME 可提高跨应用兼容性。
- 数据可能延迟获取，接收端读取时不要假设格式一定仍可用或内容很小。

## 知识点覆盖
MIME、拖放、剪贴板、富文本、URL、数据验证、跨应用互操作。
