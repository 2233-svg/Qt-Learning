# QXmlStreamAttribute
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamAttribute`
## 作用定位
`QXmlStreamAttribute` 表示 XML 元素上的一个属性，包含命名空间 URI、前缀、本地名、限定名和值。
## API 速查
| API | 是做什么的 |
|---|---|
| `name()` / `qualifiedName()` | 查询属性名。 |
| `namespaceUri()` / `prefix()` | 查询命名空间信息。 |
| `value()` | 获取属性值。 |
| `isDefault()` | 判断是否为默认属性。 |
## 使用场景
在 `QXmlStreamReader::StartElement` 时遍历 `attributes()` 读取配置项。
## 常见坑与经验
- 命名空间 XML 中不要只比较 qualifiedName，优先比较 URI 加本地名。
- 属性值是文本，数字和布尔值要显式解析并处理失败。
## 知识点覆盖
XML 属性、命名空间、限定名、流式读取、类型转换。
