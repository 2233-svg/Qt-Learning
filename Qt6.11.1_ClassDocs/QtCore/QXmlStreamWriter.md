# QXmlStreamWriter
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamWriter`
## 作用定位
`QXmlStreamWriter` 是前向 XML 写入器，按调用顺序输出格式正确的元素、属性、文本、命名空间和文档声明。
## API 速查
| API | 是做什么的 |
|---|---|
| `setDevice()` | 设置输出设备。 |
| `writeStartDocument()` / `writeEndDocument()` | 写文档边界。 |
| `writeStartElement()` / `writeEndElement()` | 写元素边界。 |
| `writeAttribute()` | 写当前开始元素的属性。 |
| `writeTextElement()` | 写包含文本的完整元素。 |
| `writeCharacters()` | 写文本并自动转义。 |
| `writeNamespace()` | 写命名空间声明。 |
| `setAutoFormatting()` | 控制缩进换行。 |
| `hasError()` | 查询写入错误。 |
## 使用场景
```cpp
QXmlStreamWriter w(&file);
w.setAutoFormatting(true);
w.writeStartDocument();
w.writeTextElement("name", userName);
w.writeEndDocument();
```
## 常见坑与经验
- 属性必须在对应 start element 之后、写子内容之前写出。
- 文本用 `writeCharacters()`，不要手动拼接转义。
- 结束元素必须配平；可用小函数封装复杂结构。
## 知识点覆盖
流式生成、XML 转义、元素配平、命名空间、格式化、写入错误。
