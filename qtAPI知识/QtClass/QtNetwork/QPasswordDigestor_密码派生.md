# QPasswordDigestor：从口令和盐派生固定长度密钥

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPasswordDigestor>`  
> 所属模块：`Qt6::Network`  
> 类型性质：命名空间，提供 PBKDF 密钥派生函数

## 它解决什么问题

`QPasswordDigestor` 将口令数据、随机盐、哈希算法和迭代次数组合为固定长度的派生密钥。它解决的是“不能直接把用户口令当作加密密钥或数据库校验值使用”的问题。

它不是登录系统、证书工具或通用哈希对象。它只计算 PBKDF1/PBKDF2 的结果；盐的生成、保存、迭代策略、密钥用途隔离、比较方式和账户限速都必须由应用设计。

## 实际使用场景

- 从用户输入的口令派生用于加密本地数据的密钥。
- 验证旧系统中已有的 PBKDF1 派生结果。
- 读取包含盐、算法、迭代次数和派生长度的旧数据格式。
- 为自定义协议准备密钥材料，前提是协议明确要求 PBKDF2。

新系统通常使用 `deriveKeyPbkdf2()`。`deriveKeyPbkdf1()` 只适合兼容遗留格式，Qt 文档明确建议新应用改用 PBKDF2。

## 最小使用方式

```cpp
const QByteArray password = readPasswordUtf8();
const QByteArray salt = secureRandomBytes(16);

const QByteArray key = QPasswordDigestor::deriveKeyPbkdf2(
    QCryptographicHash::Sha256,
    password,
    salt,
    iterations,
    32);

if (key.size() != 32)
    reportDerivationFailure();
```

`password` 是字节序列，不存在隐式的文本规范化。注册和验证必须采用同一字符编码和规范化规则；例如一次使用 UTF-8、另一次使用本地编码，会得到不同结果。

## `deriveKeyPbkdf2()` 的语义与边界

```cpp
QByteArray deriveKeyPbkdf2(
    QCryptographicHash::Algorithm algorithm,
    const QByteArray &password,
    const QByteArray &salt,
    int iterations,
    quint64 dkLen);
```

它按 PBKDF2 定义重复执行 HMAC，直到生成至少 `dkLen` 字节后截断为所需长度。实际 HMAC 次数取决于：

```text
iterations * ceil(dkLen / hashLength(algorithm))
```

因此，派生长度翻倍不只是多复制一倍字节，可能还会额外执行一整轮迭代。调用点应在 UI 线程之外或采用异步任务处理高成本派生，避免冻结界面。

`algorithm` 决定 HMAC 的底层哈希。可用性和策略应以目标平台及应用安全要求为准；不要把“函数返回非空”误解为参数一定满足安全策略。

## `deriveKeyPbkdf1()` 的遗留边界

```cpp
QByteArray deriveKeyPbkdf1(
    QCryptographicHash::Algorithm algorithm,
    const QByteArray &password,
    const QByteArray &salt,
    int iterations,
    quint64 dkLen);
```

PBKDF1 只支持 `MD5` 和 `SHA-1`：

- 盐必须恰好为 8 字节；
- `dkLen` 不能超过该哈希输出长度；
- MD5 的最大结果是 16 字节；
- SHA-1 的最大结果是 20 字节；
- 参数违反这些限制时，函数发出警告并返回空 `QByteArray`。

PBKDF1 的限制来自算法规范，不是 Qt 可以通过额外扩展消除的实现细节。新格式应避免选择它。

## 盐、参数保存和验证流程

每个口令应使用独立的、密码学安全随机生成的盐。持久化时至少要保存：

- 使用的 KDF 版本或算法标识；
- 哈希算法；
- 迭代次数；
- 盐；
- 派生长度；
- 派生结果或由它产生的认证数据。

验证时读取同一套参数重新派生，再用适合秘密比较的方式比较结果。`QPasswordDigestor` 不保存状态，也不提供数据库模式或恒定时间比较 API。

不要把盐当作秘密；盐需要与验证数据一起保存。真正需要保密的是原始口令和由其派生、仍被当作密钥使用的结果。

## 常见误区

- 直接用 `QCryptographicHash::hash(password, ...)` 替代口令 KDF。
- 所有账户复用同一个盐，或使用用户名等可预测值代替随机盐。
- 忘记保存迭代次数和算法，导致未来无法正确验证旧记录。
- 把空结果当成“空口令的合法密钥”，却不检查 PBKDF1 参数错误。
- 在 GUI 线程执行高迭代次数派生，造成界面卡顿。
- 把 PBKDF1 当作新格式的默认选择。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 命名空间 | `QPasswordDigestor` | 放置口令密钥派生函数。 | 不保存盐、策略或账户状态。 |
| 派生 | `deriveKeyPbkdf1(algorithm, password, salt, iterations, dkLen)` | 计算 PBKDF1 结果。 | 仅为旧格式兼容；只支持 MD5/SHA-1。 |
| PBKDF1 限制 | `salt` | PBKDF1 输入盐。 | 必须恰好 8 字节。 |
| PBKDF1 限制 | `dkLen` | 请求结果长度。 | MD5 最大 16 字节，SHA-1 最大 20 字节；超限返回空数组。 |
| 派生 | `deriveKeyPbkdf2(algorithm, password, salt, iterations, dkLen)` | 计算 PBKDF2 结果。 | 新代码优先；成本随迭代次数和输出长度增加。 |
| 参数 | `algorithm` | 指定底层哈希算法。 | 注册与验证必须保持一致。 |
| 参数 | `password` | 输入口令的字节表示。 | 编码和文本规范化由应用负责。 |
| 参数 | `salt` | 每次派生使用的盐。 | 应独立、随机，并与记录共同保存。 |
| 参数 | `iterations` | 派生工作因子。 | 策略由应用维护；避免阻塞 UI 线程。 |
| 参数 | `dkLen` | 请求派生结果长度。 | 与目标密钥用途匹配，不是字符长度。 |

### 一句话总结

`QPasswordDigestor` 负责按 PBKDF 规则派生字节密钥；新代码优先 PBKDF2，并由应用完整管理盐、参数版本和验证流程。
