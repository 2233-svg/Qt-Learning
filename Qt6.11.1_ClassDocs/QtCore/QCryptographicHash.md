# QCryptographicHash
> Qt 6.11.1 · Qt Core · 来自 `QCryptographicHash`

## 作用定位
`QCryptographicHash` 计算 SHA-2、SHA-3、BLAKE2 等哈希摘要，用于完整性校验、内容寻址和签名流程中的摘要步骤。

## API 速查
| API | 是做什么的 |
|---|---|
| `addData()` | 增量加入字节或 `QIODevice` 数据。|
| `result()` | 取得当前摘要结果。|
| `reset()` | 重置为初始状态。|
| `hash(data, algorithm)` | 一次性计算摘要。|
| `algorithm()` | 查询使用的算法。|
| `supportsAlgorithm()` | 判断当前构建是否支持算法。|

## 使用场景
下载文件校验、内容去重、对大文件流式计算 SHA-256、签名前先得到固定长度摘要。

## 常见坑与经验
- 哈希不是加密，不能从摘要恢复数据，也不能代替保密传输。
- 密码不能直接哈希存储；应使用专门的慢哈希/KDF 和随机盐。
- `result()` 后仍可继续 `addData()`，但语义要由调用方明确。

## 知识点覆盖
哈希、完整性、流式处理、SHA、BLAKE、密码存储边界、内容寻址。
