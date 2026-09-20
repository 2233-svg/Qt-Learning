# Qt QCryptographicHash 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QCryptographicHash>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QByteArray`、`QByteArrayView`、`QIODevice`、`QMessageAuthenticationCode`

## 1. 它解决什么问题：为同一份字节数据得到可重复的摘要

`QCryptographicHash` 用选定的密码学哈希算法，把任意长度的字节序列映射成固定长度的摘要。相同算法、相同字节输入必然得到相同摘要；输入哪怕只改动一个字节，摘要通常也会完全不同。

它适合解决这些问题：

- 下载文件后比对发布方给出的 SHA-256 摘要，确认传输内容没有意外损坏或被替换；
- 对大文件、网络流或持续产生的数据做流式摘要，不必一次读入内存；
- 生成内容指纹，作为缓存键、去重索引或构建产物标识；
- 对协议要求的 SHA-2、SHA-3、Keccak 或 BLAKE2 格式计算摘要。

它**不是**加密器：哈希不能还原原文，也不会输出可“解密”的密文。它也不是签名或认证机制：攻击者若能同时替换文件和摘要，普通无密钥哈希无法证明内容来自谁。

| 目标 | `QCryptographicHash` 是否合适 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 完整性校验 | 合适 | 计算可信渠道给出的 SHA-256 或更强摘要并比较 | 摘要本身必须来自可信来源 |
| 内容指纹、缓存键 | 合适 | 选择碰撞风险与性能符合需求的算法 | 缓存键还要包含版本、配置等输入 |
| 口令存储 | 不合适 | 使用带盐和工作因子的专用 KDF，例如 Argon2id、scrypt、PBKDF2 | 直接 SHA-256 密码非常容易被离线爆破 |
| 消息认证 | 不直接合适 | 使用 HMAC，例如 `QMessageAuthenticationCode` | 不能自己简单拼接 `secret + data` 替代 HMAC |
| 数字签名 | 不合适 | 使用经过审计的签名库和私钥体系 | 哈希只能是签名流程中的一个组成部分 |

## 2. 最小可用代码：一次性计算文本的 SHA-256

```cpp
#include <QCryptographicHash>
#include <QDebug>

int main()
{
    const QByteArray input = "hello Qt";
    const QByteArray digest = QCryptographicHash::hash(
        input, QCryptographicHash::Sha256);

    qDebug().noquote() << digest.toHex();
}
```

`digest` 保存的是原始二进制摘要，不是可读文本。日志、JSON、命令行输出或与常见校验和文本比较时，通常再调用 `toHex()` 变成十六进制表示；不要把二进制摘要直接当作 UTF-8 字符串显示。

`hash()` 的输入是 `QByteArrayView`。这意味着它可以接受 `QByteArray`、字符串字面量等连续字节数据，而不会因为函数参数本身额外复制整段输入。

## 3. 选择算法：兼容性和安全性是两件不同的事

### 3.1 日常新项目怎么选

若协议或第三方格式没有固定要求，完整性校验通常选 `Sha256`；已有 BLAKE2 生态或性能协议时可选对应的 `Blake2b_*` 或 `Blake2s_*`。实际选型还要服从发布格式、服务端和其它语言实现的约定。

`Md4`、`Md5`、`Sha1` 都已不应承担抗碰撞的安全职责。它们可能仍被遗留文件格式、旧协议或非安全的兼容标识要求使用，但不能用于签名、证书验证、对抗性完整性校验或口令保护。

| 算法组 | 常见用途 | 不应承担的任务 | 使用时重点注意 |
| --- | --- | --- | --- |
| `Md4`、`Md5`、`Sha1` | 旧格式兼容、非对抗性遗留标识 | 需要抗碰撞的安全校验 | 新设计不要选它们 |
| `Sha224`、`Sha256`、`Sha384`、`Sha512` | 通用完整性校验、跨工具互操作 | 口令拉伸 | `Sha256` 是最常见的通用交换格式 |
| `Sha3_*` | 明确要求 NIST SHA-3 的协议 | 与旧 Qt 的 Keccak 结果兼容 | 它和 Keccak 不是同一输出系列 |
| `Keccak_*` | 与 Qt 5.8 及更早版本的 “SHA3” 结果兼容 | 替代当前 SHA-3 | 只有兼容旧数据时才主动选择 |
| `Blake2b_*`、`Blake2s_*` | 已约定 BLAKE2 的内容校验或指纹 | 自行实现带密钥认证 | 位数后缀就是输出摘要长度 |

### 3.2 SHA-3 和 Keccak 的历史坑

Qt 5.9 之前，请求 `Sha3_*` 实际计算的是 Keccak；现在的 `Sha3_*` 对应标准 SHA-3。需要复现旧 Qt 输出时，要显式使用 `Keccak_224`、`Keccak_256`、`Keccak_384` 或 `Keccak_512`。

若为了保留旧源代码行为而定义 `QT_SHA3_KECCAK_COMPAT`，`Sha3_*` 枚举别名会指向 Keccak。这个宏只解决源级兼容，不应该让新协议继续含糊地写 “SHA3”；数据格式里应明确究竟使用 SHA-3 还是 Keccak。

## 4. 两种工作方式：小数据一次性算，大数据增量喂

### 4.1 静态 `hash()`：输入已经在内存中

```cpp
QByteArray digest = QCryptographicHash::hash(
    payload, QCryptographicHash::Sha256);
```

这适合小配置、网络响应体、内存缓冲区或已完整读取的文件内容。代码短，调用后直接得到新 `QByteArray`。

### 4.2 对象加 `addData()`：输入分段到达

```cpp
QCryptographicHash hash(QCryptographicHash::Sha256);

hash.addData(header);
hash.addData(bodyChunk1);
hash.addData(bodyChunk2);

const QByteArray digest = hash.result();
```

顺序就是输入的一部分。上例等价于哈希 `header + bodyChunk1 + bodyChunk2` 拼接后的字节流；它不记录段边界。协议若需要区分 `["ab", "c"]` 和 `["a", "bc"]`，必须自行加入长度、分隔符或明确编码。

`QCryptographicHash` 是不可复制类型，但 Qt 6.5 起可移动。它很适合作为一个处理流程中的成员或局部状态，而不是在多个线程之间共享的通用对象。一个实例不要被多个线程并发 `addData()` 或同时读取结果。

### 4.3 从 `QIODevice` 读取

```cpp
QFile file(path);
if (!file.open(QIODevice::ReadOnly))
    return;

QCryptographicHash hash(QCryptographicHash::Sha256);
if (!hash.addData(&file)) {
    // 读取失败或设备在读取中发生错误。
    return;
}

const QByteArray digest = hash.result();
```

`addData(QIODevice *)` 会从当前读取位置一直读到设备结束，并返回读取是否成功。它不接管 `device` 的所有权，也不会替你打开、关闭或重置设备位置。

这意味着：

- 调用前先检查设备确实处于打开且可读状态；
- 只想哈希文件的一部分时，应自行控制 `seek()`、读取长度和分块，再调用字节视图重载；
- 顺序设备如 socket、pipe 读到“暂时没有数据”未必代表真正结束，通常需要在 `readyRead()` 中持续分块 `addData()`，在协议定义的结束点取 `result()`。

## 5. 结果、复位与零分配输出

### 5.1 `result()` 与 `resultView()`

```cpp
const QByteArray owned = hash.result();       // 自己持有一份摘要
const QByteArrayView borrowed = hash.resultView(); // 借用内部摘要
```

`result()` 返回拥有数据的 `QByteArray`，最适合把摘要存起来、跨函数返回或排队发送。`resultView()` 从 Qt 6.3 起提供，避免为读取摘要而分配；但它只在 `QCryptographicHash` 对象未被其它操作修改期间有效。调用 `addData()`、`reset()`、移动赋值、`swap()` 或析构后，都不要继续保存和使用之前的 view。

需要开始计算一份新的独立输入时调用 `reset()`。它恢复为同一算法的初始状态，不会改成别的算法。

### 5.2 `hashInto()`：调用方提供输出缓冲区

`hashInto()` 从 Qt 6.8 起提供。它将结果写入调用方的 `QSpan<char>`、`QSpan<uchar>` 或 `QSpan<std::byte>`，并返回实际写入区域的 `QByteArrayView`。

```cpp
#include <array>

std::array<std::byte, 32> output;
const auto view = QCryptographicHash::hashInto(
    QSpan<std::byte>(output),
    QByteArrayView("content"),
    QCryptographicHash::Sha256);

if (view.isNull()) {
    // 缓冲区不足；本例 SHA-256 需要 32 字节。
}
```

调用前用 `hashLength(method)` 分配足够空间。缓冲区不足时函数返回 null `QByteArrayView`，不会神奇地扩容。传入 `QSpan<const QByteArrayView>` 时，Qt 按 span 中每段出现的顺序连续计算，避免为了拼接分段数据而新建巨大 `QByteArray`。

这是性能敏感、反复计算摘要、希望避免临时分配的接口；普通业务更适合可读性更高的 `hash()`。

## 6. 比对摘要：格式和时序都可能影响正确性

```cpp
const QByteArray expectedHex = "8f434346648f6b96df89dda901c5176b...";
const QByteArray actualHex = hash.result().toHex();

if (actualHex == expectedHex.toLower()) {
    // 文件内容与可信发布的摘要一致。
}
```

有三个实际问题经常导致“算法没错，结果却不一致”：

1. 输入字节不同：文本编码、换行符、BOM、文件是否包含末尾换行都会改变摘要。
2. 摘要格式不同：一个值可能是原始二进制、十六进制文本、Base64 文本或带空格分组的命令行输出。
3. 算法名称不同：`Sha3_256` 与 `Keccak_256`、`Sha256` 与 `Sha512` 都不能混用。

比较不公开的令牌或认证材料时，还需要考虑比较时间是否泄露前缀匹配长度。`QCryptographicHash` 的普通 `QByteArray` 比较不是用于构造恒定时间认证流程的专用 API；应使用经过审计的认证方案或密码库。

## 7. 算法可用性和部署环境

`supportsAlgorithm()` 从 Qt 6.5 起可在使用某个算法前检查当前构建和后端是否支持它。Qt 使用 OpenSSL 作为提供者时，可用性会受 OpenSSL 配置与查询结果影响；非 OpenSSL 实现通常没有这类运行时限制。

```cpp
using Hash = QCryptographicHash;

if (!Hash::supportsAlgorithm(Hash::Sha256)) {
    // 给出明确错误；不要静默换成弱算法。
    return;
}
```

不要在安全路径中“SHA-256 不可用就退回 MD5”。这会把部署问题悄悄变成安全缺陷。正确的策略是报告不兼容环境，或由协议在设计时提供同等级的受控协商。

## API 速查表
### 8.1 `Algorithm` 枚举

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Md4` | 计算 MD4 摘要 | 仅遗留兼容；不具备现代抗碰撞安全性 |
| 枚举 | `Md5` | 计算 MD5 摘要 | 仅遗留兼容；不能用于安全完整性或签名 |
| 枚举 | `Sha1` | 计算 SHA-1 摘要 | 已不适合抗碰撞安全场景 |
| 枚举 | `Sha224` | 计算 SHA-2 的 224 位摘要 | 使用方必须明确接受 28 字节输出 |
| 枚举 | `Sha256` | 计算 SHA-2 的 256 位摘要 | 通用完整性校验的常见选择 |
| 枚举 | `Sha384` | 计算 SHA-2 的 384 位摘要 | 输出为 48 字节，双方格式必须一致 |
| 枚举 | `Sha512` | 计算 SHA-2 的 512 位摘要 | 输出为 64 字节，不能与 SHA-256 比较 |
| 枚举 | `Sha3_224` | 计算标准 SHA3-224 摘要 | 与 `Keccak_224` 不同；旧 Qt 兼容见正文 |
| 枚举 | `Sha3_256` | 计算标准 SHA3-256 摘要 | 不要把协议中的 Keccak 名称写成 SHA-3 |
| 枚举 | `Sha3_384` | 计算标准 SHA3-384 摘要 | 与对端确认算法和输出编码 |
| 枚举 | `Sha3_512` | 计算标准 SHA3-512 摘要 | 旧代码定义兼容宏时别名可能变为 Keccak |
| 枚举 | `Keccak_224` | 计算 Keccak-224 摘要 | 用于明确协议或 Qt 5.8 及以前结果兼容 |
| 枚举 | `Keccak_256` | 计算 Keccak-256 摘要 | 不是标准 SHA3-256 的替代名称 |
| 枚举 | `Keccak_384` | 计算 Keccak-384 摘要 | 仅在数据格式要求时使用 |
| 枚举 | `Keccak_512` | 计算 Keccak-512 摘要 | 仅在数据格式要求时使用 |
| 枚举 | `Blake2b_160` | 计算 160 位 BLAKE2b 摘要 | 输出长度为 20 字节 |
| 枚举 | `Blake2b_256` | 计算 256 位 BLAKE2b 摘要 | 输出长度为 32 字节 |
| 枚举 | `Blake2b_384` | 计算 384 位 BLAKE2b 摘要 | 输出长度为 48 字节 |
| 枚举 | `Blake2b_512` | 计算 512 位 BLAKE2b 摘要 | 输出长度为 64 字节 |
| 枚举 | `Blake2s_128` | 计算 128 位 BLAKE2s 摘要 | 输出长度为 16 字节 |
| 枚举 | `Blake2s_160` | 计算 160 位 BLAKE2s 摘要 | 输出长度为 20 字节 |
| 枚举 | `Blake2s_224` | 计算 224 位 BLAKE2s 摘要 | 输出长度为 28 字节 |
| 枚举 | `Blake2s_256` | 计算 256 位 BLAKE2s 摘要 | 输出长度为 32 字节 |
| 枚举 | `NumAlgorithms` | 枚举项数量的哨兵值 | 不要传给构造函数或哈希函数作为真实算法 |

### 8.2 构造、状态和流式输入

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCryptographicHash(Algorithm method)` | 创建指定算法的增量哈希状态 | 创建前可用 `supportsAlgorithm()` 检查；实例不可复制 |
| 移动构造 | `QCryptographicHash(QCryptographicHash &&other)` | 从另一个实例转移内部计算状态 | Qt 6.5 起；被移动对象只可析构或重新赋值 |
| 析构 | `~QCryptographicHash()` | 销毁哈希状态 | 不会关闭或删除曾传给 `addData(QIODevice *)` 的设备 |
| 移动赋值 | `operator=(QCryptographicHash &&other)` | 用另一个实例的状态替换当前状态 | Qt 6.5 起；移动源进入部分形成状态 |
| 状态 | `algorithm() const` | 返回当前实例使用的算法 | Qt 6.5 起；不能据此推断输入内容 |
| 状态 | `reset()` | 清空当前输入并回到同算法初始状态 | 之前的 `resultView()` 立即失效 |
| 状态 | `swap(QCryptographicHash &other)` | 高效交换两个实例的计算状态 | Qt 6.5 起；交换后结果归属也随之交换 |
| 输入 | `addData(QByteArrayView bytes)` | 将一个字节片段追加到当前哈希输入 | Qt 6.3 起签名使用 view；输入顺序和每一个字节都会影响摘要 |
| 输入 | `addData(QIODevice *device)` | 从已打开设备当前位置读到末尾并追加计算 | 不接管设备；返回 `false` 时检查设备错误和读取状态 |
| 兼容 API | `addData(const char *data, qsizetype length)` | 向当前哈希追加裸字节范围 | Qt 6.4 起弃用；新代码改用 `QByteArrayView` |
| 兼容 API | `addData(const QByteArray &data)` | 向当前哈希追加字节数组 | Qt 6.3 前的旧签名；新代码依赖 `QByteArrayView` 重载 |

### 8.3 结果与一次性计算

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结果 | `result() const` | 返回当前输入的最终摘要副本 | 返回二进制 `QByteArray`；显示或文本交换常需 `toHex()` |
| 结果 | `resultView() const` | 返回内部摘要的非拥有视图 | Qt 6.3 起；任何修改实例的操作后都不要使用旧 view |
| 一次性 | `hash(QByteArrayView data, Algorithm method)` | 直接计算一段内存数据的摘要 | Qt 6.3 前参数是 `QByteArray`；简单场景优先用它 |
| 长度 | `hashLength(Algorithm method)` | 返回该算法摘要的字节长度 | 用于分配 `hashInto()` 缓冲区；按字节而不是十六进制字符数返回 |
| 支持性 | `supportsAlgorithm(Algorithm method)` | 查询当前运行环境能否提供该算法 | Qt 6.5 起；不可用时不要静默降级到弱算法 |

### 8.4 `hashInto()` 六个重载

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 零分配 | `hashInto(QSpan<char>, QByteArrayView, Algorithm)` | 将单段输入的摘要写进 `char` 缓冲区 | Qt 6.8 起；缓冲区不足返回 null view |
| 零分配 | `hashInto(QSpan<uchar>, QByteArrayView, Algorithm)` | 将单段输入的摘要写进 `uchar` 缓冲区 | 返回 view 借用调用方缓冲区，不能让缓冲区先失效 |
| 零分配 | `hashInto(QSpan<std::byte>, QByteArrayView, Algorithm)` | 将单段输入的摘要写进 `std::byte` 缓冲区 | 适合现代 C++ 字节容器；长度先用 `hashLength()` 获得 |
| 零分配 | `hashInto(QSpan<char>, QSpan<const QByteArrayView>, Algorithm)` | 连续计算多个片段并写入 `char` 缓冲区 | 分段按 span 顺序拼接；不会记录原始片段边界 |
| 零分配 | `hashInto(QSpan<uchar>, QSpan<const QByteArrayView>, Algorithm)` | 连续计算多个片段并写入 `uchar` 缓冲区 | 用于避免为了拼接分段输入而额外分配 |
| 零分配 | `hashInto(QSpan<std::byte>, QSpan<const QByteArrayView>, Algorithm)` | 连续计算多个片段并写入 `std::byte` 缓冲区 | Qt 6.8 起；所有 span 在调用期间必须有效 |

## 9. 实用封装：校验本地文件是否匹配预期 SHA-256

```cpp
#include <QCryptographicHash>
#include <QFile>

bool fileMatchesSha256(const QString &path, const QByteArray &expectedHex)
{
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly))
        return false;

    QCryptographicHash hash(QCryptographicHash::Sha256);
    if (!hash.addData(&file))
        return false;

    return hash.result().toHex() == expectedHex.trimmed().toLower();
}
```

这个函数只回答“文件字节是否匹配一个可信的 SHA-256 十六进制值”。它不验证摘要的来源、不做签名验证，也不把文件读取失败伪装成“不匹配”。在真实发布系统中，应把获取摘要、验证签名和下载文件的信任链分层处理。
