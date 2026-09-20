# QXmlStreamEntityDeclaration
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamEntityDeclaration`
## 作用定位
`QXmlStreamEntityDeclaration` 描述 DTD 中声明的实体名称、值和外部标识。现代应用通常只在需要兼容 DTD 的 XML 中读取它。
## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | 实体名称。 |
| `value()` | 内部实体值。 |
| `publicId()` / `systemId()` | 外部实体标识。 |
| `notationName()` | 未解析实体关联记号。 |
## 使用场景
处理带 DTD 的旧 XML 格式时记录实体声明。
## 常见坑与经验
- 外部实体可能带来安全风险，解析不可信 XML 时要限制实体解析。
- 多数配置格式不需要 DTD，能禁用就简化。
## 知识点覆盖
DTD、实体、外部标识、XML 安全、兼容旧格式。
