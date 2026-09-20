# QXmlStreamReader
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamReader`
## 作用定位
`QXmlStreamReader` 是前向只读 XML 流解析器，逐 token 读取文档，适合大文件和低内存解析。它不构建 DOM 树。
## API 速查
| API | 是做什么的 |
|---|---|
| `setDevice()` / `addData()` | 设置输入来源。 |
| `readNext()` | 读取下一个 token。 |
| `tokenType()` | 查询当前 token 类型。 |
| `isStartElement()` / `isEndElement()` | 判断元素边界。 |
| `name()` / `namespaceUri()` | 查询当前元素名。 |
| `attributes()` | 读取当前元素属性。 |
| `readElementText()` | 读取当前元素文本内容。 |
| `hasError()` / `errorString()` | 处理解析错误。 |
| `lineNumber()` / `columnNumber()` | 定位错误位置。 |
## 使用场景
逐个读取大型 XML 配置或导入文件，不把整份文档载入内存。
## 常见坑与经验
- 每次读取后当前 token 会变化，需要立即处理或保存必要数据。
- 命名空间判断用 URI 和本地名。
- 不可信 XML 注意实体解析和资源消耗。
## 知识点覆盖
StAX、流式解析、token、命名空间、属性、错误定位、大文件。
