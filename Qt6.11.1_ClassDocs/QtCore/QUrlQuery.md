# QUrlQuery
> Qt 6.11.1 · Qt Core · 来自 `QUrlQuery`
## 作用定位
`QUrlQuery` 专门管理 URL 查询字符串中的键值项，负责分隔符与百分号编码，避免手写 `a=b&c=d` 的漏洞。
## API 速查
| API | 是做什么的 |
|---|---|
| `addQueryItem()` | 添加一个键值项。 |
| `queryItemValue()` | 获取某键的值。 |
| `hasQueryItem()` | 判断键是否存在。 |
| `removeQueryItem(s)` | 删除一个或多个键。 |
| `queryItems()` | 取得全部键值对。 |
| `toString()` | 生成查询字符串。 |
| `setQueryDelimiters()` | 自定义分隔符。 |
## 使用场景
构造 HTTP GET 参数、深链接参数和 OAuth redirect 参数。
## 常见坑与经验
- 同名键可以出现多次，读取时要确认业务期望单值还是多值。
- 值为空和键不存在是不同状态。
- 编码由 API 处理，不要提前重复百分号编码。
## 知识点覆盖
查询字符串、键值重复、百分号编码、HTTP 参数、深链接。
