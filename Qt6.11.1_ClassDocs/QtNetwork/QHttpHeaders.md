# QHttpHeaders
> Qt 6.11.1 · Qt Network · 来自 `QHttpHeaders`

## 作用定位
`QHttpHeaders` 是 HTTP 头集合的值类型，提供比手写 `QList<QPair>` 更明确的已知头字段和原始字段访问。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 添加一个字段值，可保留重复头。|
| `replace()` | 替换某字段的值。|
| `removeAll()` | 删除同名字段。|
| `value()` / `values()` | 读取一个或多个值。|
| `contains()` | 判断字段是否存在。|
| `nameAt()` / `valueAt()` | 按索引遍历字段。|
| `WellKnownHeader` | 使用标准头字段枚举。|

## 使用场景
构建需要多值 `Accept`、`Cache-Control` 或自定义追踪头的请求/响应处理逻辑。

## 常见坑与经验
- HTTP 字段名大小写不敏感，但重复字段是否可合并取决于具体语义，不能一概逗号拼接。
- 不要把机密 token 记入日志，即使它只是 headers 容器中的一个条目。

## 知识点覆盖
HTTP 头、多值字段、标准字段、大小写规则、敏感信息。
