# QXmlStreamAttributes
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamAttributes`
## 作用定位
`QXmlStreamAttributes` 是当前 XML 元素属性列表的轻量容器，提供按名称查询和遍历。
## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 按命名空间/名称取得属性值。 |
| `hasAttribute()` | 判断属性是否存在。 |
| `append()` | 构造写入属性列表时添加项。 |
| 迭代接口 | 遍历所有属性。 |
## 使用场景
读取 `<item id="42" enabled="true">` 时检查必需属性并转换。
## 常见坑与经验
- 缺失属性和空字符串属性不同。
- 解析时记录行列号，错误信息更有用。
- 名称空间场景使用带 URI 的查询重载。
## 知识点覆盖
属性集合、必填校验、命名空间、流式 XML、错误报告。
