# QByteArray::FromBase64Result
> Qt 6.11.1 · Qt Core · 来自 `QByteArray::FromBase64Result`

## 作用定位
`QByteArray::FromBase64Result` 是严格 Base64 解码的结果对象，同时保存解码字节和错误状态。

## API 速查
| API | 是做什么的 |
|---|---|
| `decoded` | 取得成功解码出的字节。|
| `decodingStatus` | 判断输入是否合法。|
| `operator bool()` | 快速判断是否成功。|

## 使用场景
解析外部 token、配置或协议字段时，需要拒绝格式错误而不是默默得到部分结果。

## 常见坑与经验
- 成功 Base64 解码不表示内容可信或安全；还需验证签名、长度和协议结构。

## 知识点覆盖
严格解码、错误状态、输入验证、二进制协议、安全边界。
