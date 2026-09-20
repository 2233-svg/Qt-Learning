# QByteArray
> Qt 6.11.1 · Qt Core · 来自 `QByteArray`

## 作用定位
`QByteArray` 是隐式共享的可变字节数组，适合二进制数据、UTF-8/Latin-1 文本、网络 payload 与 C API 交互。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` / `prepend()` | 追加或前置字节。|
| `mid()` / `sliced()` | 截取子序列。|
| `indexOf()` | 查找子序列。|
| `toBase64()` / `fromBase64()` | Base64 编解码。|
| `toHex()` / `fromHex()` | 十六进制编解码。|
| `toPercentEncoding()` | URL 百分号编码。|
| `constData()` | 获取 NUL 结尾只读 C 字符串指针。|

## 使用场景
HTTP body、二进制协议缓冲、哈希结果、UTF-8 互操作。

## 常见坑与经验
- 它不是 Unicode 字符串；用户可见文本优先 `QString`。
- 修改可能触发 detach，使此前取得的 data 指针失效。
- Base64 不是加密，不能保护敏感数据。

## 知识点覆盖
二进制、隐式共享、编码、C 互操作、指针失效、Base64。
