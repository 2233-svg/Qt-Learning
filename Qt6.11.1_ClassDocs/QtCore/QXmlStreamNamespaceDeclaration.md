# QXmlStreamNamespaceDeclaration
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamNamespaceDeclaration`
## 作用定位
`QXmlStreamNamespaceDeclaration` 表示 XML 中 `xmlns` 声明，记录前缀和命名空间 URI。
## API 速查
| API | 是做什么的 |
|---|---|
| `prefix()` | 命名空间前缀。 |
| `namespaceUri()` | 命名空间 URI。 |
| 比较运算 | 判断声明是否相同。 |
## 使用场景
读取元素时检查当前作用域内声明的 XML 命名空间。
## 常见坑与经验
- 默认命名空间前缀为空，但仍有 URI。
- 判断元素语义时用 URI，不要依赖前缀字符串。
## 知识点覆盖
XML 命名空间、默认命名空间、前缀、URI、作用域。
