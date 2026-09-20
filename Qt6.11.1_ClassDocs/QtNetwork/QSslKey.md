# QSslKey
> Qt 6.11.1 · Qt Network · 来自 `QSslKey`

## 作用定位
`QSslKey` 表示 TLS 私钥或公钥，可从 PEM/DER 编码导入并交给 TLS 配置。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 从编码数据、算法和类型创建密钥。|
| `toPem()` / `toDer()` | 导出编码。|
| `algorithm()` | 查询 RSA、EC 等算法。|
| `type()` | 查询公钥或私钥。|
| `isNull()` | 判断是否有效。|

## 使用场景
加载 mTLS 客户端私钥或 TLS 服务端身份密钥。

## 常见坑与经验
- 私钥必须受操作系统或加密存储保护，不能提交到代码仓库或日志。

## 知识点覆盖
公私钥、PEM/DER、TLS 身份、密钥保护、算法。
