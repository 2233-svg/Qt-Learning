# QUrl
> Qt 6.11.1 · Qt Core · 来自 `QUrl`
## 作用定位
`QUrl` 解析、构造和规范化 URL/URI，处理 scheme、host、path、query、fragment 及百分号编码。它不是普通字符串拼接工具。
## API 速查
| API | 是做什么的 |
|---|---|
| `fromUserInput()` | 将用户输入解释为 URL 或本地路径。 |
| `fromLocalFile()` / `toLocalFile()` | 本地路径与 file URL 转换。 |
| `setScheme/Host/Path/Query/Fragment` | 分部构造 URL。 |
| `isValid()` / `errorString()` | 校验解析结果。 |
| `toString()` / `toEncoded()` | 生成文本或字节形式。 |
| `resolved()` | 按基础 URL 解析相对地址。 |
| `matches()` / `adjusted()` | 比较或去除部分组件。 |
## 使用场景
```cpp
QUrl url;
url.setScheme("https");
url.setHost("example.com");
url.setPath("/search");
QUrlQuery q;
q.addQueryItem("q", term);
url.setQuery(q);
```
## 常见坑与经验
- 不要手动拼 `?`、`&` 和百分号编码，查询用 `QUrlQuery`。
- 本地路径用 `fromLocalFile()`，尤其是 Windows 盘符和空格。
- `isValid()` 不代表网络可达，只代表语法可接受。
## 知识点覆盖
URI、百分号编码、本地文件 URL、相对解析、查询参数、安全拼接。
