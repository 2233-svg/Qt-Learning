# QUuid
> Qt 6.11.1 · Qt Core · 来自 `QUuid`
## 作用定位
`QUuid` 表示 UUID/GUID，用于跨系统唯一标识对象、记录、会话或资源。它不表达安全认证，也不保证顺序。
## API 速查
| API | 是做什么的 |
|---|---|
| `createUuid()` | 生成随机 UUID。 |
| `createUuidV3/V5()` | 基于命名空间和名称生成确定性 UUID。 |
| `fromString()` / `toString()` | 文本解析与输出。 |
| `toRfc4122()` / `fromRfc4122()` | RFC 4122 字节形式转换。 |
| `isNull()` | 判断全零 UUID。 |
| `variant()` / `version()` | 查询 UUID 规范类别。 |
## 使用场景
为离线创建的业务实体生成 id，稍后同步到服务器。
## 常见坑与经验
- UUID 不是权限令牌，不能仅凭不可猜测性做访问控制。
- 文本大小写和花括号形式应在持久化层统一。
- 需要按时间排序的 id 另选专门方案。
## 知识点覆盖
UUID、GUID、RFC 4122、随机标识、命名空间 UUID、安全边界。
