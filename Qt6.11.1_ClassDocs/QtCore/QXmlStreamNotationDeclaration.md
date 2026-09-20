# QXmlStreamNotationDeclaration
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamNotationDeclaration`
## 作用定位
`QXmlStreamNotationDeclaration` 表示 DTD notation 声明，用于描述非 XML 数据格式或未解析实体的标识。
## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | notation 名称。 |
| `publicId()` / `systemId()` | 外部标识。 |
## 使用场景
维护旧式 DTD XML 兼容解析器时读取 notation 信息。
## 常见坑与经验
- 现代应用很少需要 notation；遇到它时优先确认格式需求。
- 外部标识不要自动联网解析。
## 知识点覆盖
DTD、notation、未解析实体、外部标识、旧格式兼容。
