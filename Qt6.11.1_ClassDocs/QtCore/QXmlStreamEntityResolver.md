# QXmlStreamEntityResolver
> Qt 6.11.1 · Qt Core · 来自 `QXmlStreamEntityResolver`
## 作用定位
`QXmlStreamEntityResolver` 自定义 XML 实体解析逻辑，让应用控制实体名称如何替换为文本。
## API 速查
| API | 是做什么的 |
|---|---|
| `resolveEntity()` | 按 publicId/systemId 或名称返回实体内容。 |
## 使用场景
解析受控 XML 方言时，把少量已知实体映射为安全文本。
## 常见坑与经验
- 不可信 XML 不应随意解析外部实体，避免 XXE 类风险。
- resolver 应快速且确定，不要在解析线程做慢网络请求。
## 知识点覆盖
实体解析、DTD、XXE 安全、受控映射、流式解析。
