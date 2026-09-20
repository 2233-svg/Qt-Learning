# Qt QMessageAuthenticationCode HMAC 消息认证笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMessageAuthenticationCode>`  
> 所属模块：`Qt6::Core`  
> 类型性质：基于 `QCryptographicHash` 算法计算 HMAC 的状态对象  
> 相关类型：`QCryptographicHash`、`QByteArrayView`、`QByteArray`、`QIODevice`、`QSpan`

## 1. 它解决什么问题

`QMessageAuthenticationCode` 用一个共享密钥和一个哈希算法计算消息认证码（HMAC）。它解决的是：

> 已知同一份秘密密钥的两端，如何确认消息来自持钥方，并确认消息内容没有被篡改。

典型流程是：

```text
选择哈希算法 + 密钥
        |
追加完整消息或消息片段
        |
读取 HMAC
        |
接收方用同样的算法和密钥重新计算并比较
```

它不是普通的摘要器，也不是加密器：

- `QCryptographicHash` 只计算公开消息的摘要，不提供密钥认证；
- HMAC 不隐藏消息内容，旁观者仍然可以读取明文；
- HMAC 不提供重放保护，协议仍需要时间戳、序列号、nonce 或其他防重放设计；
- HMAC 不自动协商算法、传输密钥或比较结果；
- 认证码的比较不能简单依赖普通字符串比较来处理攻击者可控输入，验证协议通常应使用常量时间比较。

不要用 `secret + message`、`hash(message + secret)` 等自行拼接方式代替 HMAC。`QMessageAuthenticationCode` 已经封装了 HMAC 的密钥处理和内外层哈希结构。

## 2. 实际使用场景

### 2.1 为网络请求生成认证字段

```cpp
const QByteArray key = loadSharedSecret();
const QByteArray body = requestBody;

const QByteArray tag =
    QMessageAuthenticationCode::hash(
        body, key, QCryptographicHash::Sha256).toHex();
```

发送时通常还要把算法标识、版本、时间戳、请求路径、方法、序列号等纳入明确的规范化消息。只对 body 做 HMAC 并不会自动保护其他请求元数据。

### 2.2 对大消息流式计算

```cpp
QMessageAuthenticationCode mac(QCryptographicHash::Sha256, key);
mac.addData(device);
if (!device->atEnd())
    handleReadFailure();

const QByteArray tag = mac.result();
```

`addData(QIODevice *)` 避免先把整个设备内容读入一个大的 `QByteArray`。如果设备读取失败，返回值为 `false`，当前认证对象可能已经处理了部分输入；应根据协议丢弃或 `reset()` 后重新开始，而不是把部分结果当成完整消息的认证码。

### 2.3 分块处理网络或序列化输出

```cpp
QMessageAuthenticationCode mac(QCryptographicHash::Sha256, key);
mac.addData(headerView);
mac.addData(payloadView);
mac.addData(trailerView);
const QByteArray tag = mac.result();
```

连续调用 `addData()` 的效果等价于把所有片段按调用顺序拼接后一次性计算。API 不会自动插入分隔符、长度字段或消息边界。

### 2.4 低分配或固定缓冲区路径

```cpp
std::array<std::byte, 32> output;
const QByteArrayView tag = QMessageAuthenticationCode::hashInto(
    QSpan<std::byte>(output), message, key,
    QCryptographicHash::Sha256);
```

`hashInto()` 将结果写入调用方提供的缓冲区并返回借用该缓冲区的视图。缓冲区长度应至少满足所选哈希算法的认证码长度；固定大小不要脱离算法配置硬编码。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMessageAuthenticationCode>
#include <QCryptographicHash>
#include <QByteArray>
#include <QIODevice>
#include <QSpan>
```

`QMessageAuthenticationCode` 位于 `Qt6::Core`，不需要额外的网络或加密模块链接。

## 4. 认证算法和协议边界

### 4.1 `method` 选择底层哈希算法

构造函数、`hash()` 和 `hashInto()` 都通过 `QCryptographicHash::Algorithm` 指定底层算法，例如：

```cpp
const auto method = QCryptographicHash::Sha256;
```

Qt 还提供 MD4、MD5、SHA-1、SHA-2、SHA-3、Keccak 和 BLAKE2 等枚举值。API 接受这些枚举不等于它们都适合新的安全协议：

- MD4、MD5 和 SHA-1 不应作为新认证协议的首选；
- 兼容旧协议时必须固定算法和编码，不能让对端任意选择算法；
- 新协议应依据威胁模型选择现代算法，并把算法标识纳入协议版本管理；
- HMAC 标签长度由底层摘要长度决定，截断标签需要由协议明确规定。

### 4.2 密钥是字节序列，不是密码字符串

```cpp
const QByteArray key = loadRandomSecretBytes();
QMessageAuthenticationCode mac(method, key);
```

`key` 以字节视图传入，类不会替你做密码派生、编码规范化或密钥轮换。若用户输入的是密码，应先使用合适的密码派生函数得到密钥；不要直接把用户可猜的短字符串当作高强度共享密钥。

### 4.3 空密钥在 API 层允许，但通常没有认证价值

构造函数的 key 参数默认是空视图，`setKey({})` 也可以表达空密钥。这是为了提供完整的值语义和兼容性，不代表空密钥适合身份认证。实际协议应明确拒绝空密钥或由更高层决定其含义。

### 4.4 HMAC 不等于加密和防重放

HMAC 只提供完整性和持钥方认证的基础。它不会：

- 加密消息；
- 自动隐藏密钥；
- 自动阻止旧消息再次发送；
- 自动确认消息来自某一个特定设备而不是所有持有同一共享密钥的设备；
- 自动解决密钥泄露后的撤销和轮换。

这些能力需要协议和系统设计配合。

## 5. 生命周期、状态和所有权

### 5.1 它是不可复制的状态对象

头文件使用 `Q_DISABLE_COPY`，因此不能复制构造或复制赋值：

```cpp
QMessageAuthenticationCode mac(method, key);
// QMessageAuthenticationCode copy = mac; // 不允许
```

对象内部维护着哈希状态和认证密钥相关状态。需要转移所有权时使用 Qt 6.6 起提供的移动构造或移动赋值：

```cpp
QMessageAuthenticationCode makeMac(QByteArrayView key)
{
    return QMessageAuthenticationCode(QCryptographicHash::Sha256, key);
}
```

移动后的源对象只适合销毁或再次赋值，不应继续假定它包含可用的认证状态。

### 5.2 输入视图不转移所有权

`QByteArrayView`、`QSpan` 和 `QIODevice *` 都不会把调用方的存储所有权交给认证对象：

- `addData(QByteArrayView)` 在调用期间读取视图内容；
- `hash()` 在调用期间读取 message 和 key；
- `hashInto()` 在调用期间读取输入，并把结果写入调用方缓冲区；
- `addData(QIODevice *)` 读取设备，但不销毁设备。

调用期间以及返回视图仍在使用时，底层存储必须保持有效。

### 5.3 结果有两种返回形态

- `result()` 返回拥有数据的 `QByteArray`，适合保存、返回或跨异步边界传递；
- `resultView()` 返回借用内部存储的 `QByteArrayView`，适合短时间读取，避免复制。

只要对象被 `reset()`、`setKey()`、`addData()`、移动赋值或 `swap()` 等操作修改，就不要继续依赖之前保存的 `resultView()`。需要跨越这些操作保存结果时，立即复制成 `QByteArray`。

## 6. 最小可用示例

### 6.1 一次性计算 HMAC

```cpp
#include <QMessageAuthenticationCode>
#include <QCryptographicHash>
#include <QByteArray>

QByteArray makeTag(QByteArrayView message, QByteArrayView key)
{
    return QMessageAuthenticationCode::hash(
        message, key, QCryptographicHash::Sha256);
}
```

### 6.2 增量计算并复用对象

```cpp
QMessageAuthenticationCode mac(QCryptographicHash::Sha256, key);
mac.addData(header);
mac.addData(payload);

const QByteArray tag = mac.result();

mac.reset();
mac.addData(nextMessage);
const QByteArray nextTag = mac.result();
```

`reset()` 清除已经追加的消息状态，使对象回到当前算法和当前 key 的初始状态；它不会把算法切换成另一个值，也不应被理解成自动生成新密钥。

### 6.3 使用设备输入

```cpp
QMessageAuthenticationCode mac(QCryptographicHash::Sha256, key);
if (!mac.addData(file)) {
    // 设备读取失败，丢弃本次认证结果
    return;
}

const QByteArray tag = mac.result();
```

设备必须提供可读内容。`addData()` 返回 `false` 时，应检查设备错误状态并决定是否重新定位、重新打开或丢弃本次状态。

### 6.4 读取借用结果

```cpp
QMessageAuthenticationCode mac(method, key);
mac.addData(message);

const QByteArrayView view = mac.resultView();
consumeImmediately(view);
```

如果 `consumeImmediately()` 需要把 view 存起来，就改用：

```cpp
const QByteArray owned = mac.result();
storeForLater(owned);
```

## 7. 逐项成员 API

### 7.1 `QMessageAuthenticationCode(Algorithm method, QByteArrayView key = {})`

```cpp
explicit QMessageAuthenticationCode(
    QCryptographicHash::Algorithm method,
    QByteArrayView key = {});
```

创建一个使用指定底层哈希算法和密钥的 HMAC 状态对象。构造时直接提供 key 通常比先构造再调用 `setKey()` 更合适，因为不需要额外初始化一次密钥状态：

```cpp
QMessageAuthenticationCode mac(
    QCryptographicHash::Sha256, key);
```

注意：

- `method` 应是协议明确允许的算法；
- `key` 只在构造调用期间作为视图读取，类会建立自己的内部状态；
- 空 key 在接口层合法，但不代表业务上安全；
- 该类没有默认构造函数，必须指定算法。

### 7.2 `QMessageAuthenticationCode(QMessageAuthenticationCode &&other)`

```cpp
QMessageAuthenticationCode(
    QMessageAuthenticationCode &&other) noexcept;
```

Qt 6.6 起提供移动构造，将认证对象的内部状态转移到新对象：

```cpp
QMessageAuthenticationCode makeMac(QByteArrayView key)
{
    QMessageAuthenticationCode result(
        QCryptographicHash::Sha256, key);
    return result;
}
```

移动后的 `other` 仍是一个已构造对象，但其具体内部状态不应再被调用方假设。不要在移动后继续对源对象追加数据或读取结果，除非先给它重新赋值。

### 7.3 `~QMessageAuthenticationCode()`

```cpp
~QMessageAuthenticationCode();
```

销毁对象并释放内部认证状态。对象不拥有传入的 `QByteArrayView` 底层存储，也不拥有传入的 `QIODevice`。

### 7.4 `operator=(QMessageAuthenticationCode &&other)`

```cpp
QMessageAuthenticationCode &operator=(
    QMessageAuthenticationCode &&other) noexcept;
```

Qt 6.6 起提供移动赋值。目标对象原有的内部状态会被释放或替换，源对象转为已移动状态：

```cpp
mac = makeMac(newKey);
```

移动赋值会使此前从目标对象取得的 `resultView()` 失去继续使用的前提。

### 7.5 `swap(QMessageAuthenticationCode &other)`

```cpp
void swap(QMessageAuthenticationCode &other) noexcept;
```

交换两个认证对象的内部状态、算法和密钥相关状态，不复制消息内容：

```cpp
mac.swap(other);
```

交换后，之前指向某个对象内部结果的 view 不应跨越交换继续使用。需要稳定结果时先复制为 `QByteArray`。

### 7.6 `reset()`

```cpp
void reset() noexcept;
```

清除当前已经追加的消息，把对象恢复到当前算法和当前 key 的初始 HMAC 状态：

```cpp
mac.addData(message);
const QByteArray first = mac.result();

mac.reset();
mac.addData(otherMessage);
const QByteArray second = mac.result();
```

它不会：

- 改变底层哈希算法；
- 生成新 key；
- 撤销已经发出的认证码；
- 自动重置关联 `QIODevice` 的位置。

### 7.7 `setKey(QByteArrayView key)`

```cpp
void setKey(QByteArrayView key) noexcept;
```

替换 HMAC 密钥，并使当前对象回到新密钥的初始消息状态。设置新 key 后，不应把此前追加的消息和新 key 混合解释：

```cpp
mac.setKey(nextKey);
mac.addData(messageForNextKey);
```

如果 key 不变但希望开始新消息，使用 `reset()` 更直接。调用 `setKey()` 后，之前的 `resultView()` 不再有效。

### 7.8 `addData(QByteArrayView data)`

```cpp
void addData(QByteArrayView data) noexcept;
```

把一段字节追加到当前 HMAC 消息中。认证对象只在调用期间读取 view，不依赖调用方在返回后继续保留这段输入：

```cpp
mac.addData(QByteArrayView("header"));
mac.addData(payload);
```

多个片段按调用顺序连接，没有自动分隔符、长度前缀或编码转换。空 view 表示追加零字节，不会改变消息内容。

### 7.9 `addData(const char *data, qsizetype length)`

```cpp
void addData(const char *data, qsizetype length);
```

兼容指针加长度的输入形式，把 `data[0..length)` 追加到消息。它不是以 `'\0'` 为结束条件的 C 字符串接口：

```cpp
mac.addData(binaryData, binaryLength);
```

二进制数据中可以包含零字节。调用方必须保证当 `length > 0` 时，指针指向至少 `length` 个可读字节；长度应使用实际字节数而不是字符数。

### 7.10 `addData(QIODevice *device)`

```cpp
bool addData(QIODevice *device);
```

从设备读取数据并追加到 HMAC，直到设备结束或读取失败。返回 `true` 表示读取过程成功完成，`false` 表示设备读取失败或设备不可用：

```cpp
if (!mac.addData(device)) {
    discardPartialAuthentication();
}
```

边界：

- 设备应已打开并可读；
- 函数会消费设备当前位置开始的数据；
- 不会自动把设备位置恢复到调用前；
- 读取失败时，认证对象可能已经包含部分数据；
- 失败后的状态不应当被当成完整消息的认证结果；
- 设备由调用方拥有，认证对象不会销毁它。

### 7.11 `resultView() const`

```cpp
QByteArrayView resultView() const noexcept;
```

返回当前已经追加消息的 HMAC 结果的非拥有视图。认证码长度等于底层哈希算法的摘要长度：

```cpp
const QByteArrayView tag = mac.resultView();
```

适用场景是立即读取、编码或传给同步函数。它的存储由认证对象内部管理，不能在对象修改后继续保存使用。若需要长期保存，使用 `result()`。

### 7.12 `result() const`

```cpp
QByteArray result() const;
```

返回当前消息的 HMAC，结果由返回的 `QByteArray` 拥有：

```cpp
const QByteArray tag = mac.result();
```

它适合跨函数返回、加入队列、写入持久化或在认证对象随后 `reset()` 时继续保留。调用 `result()` 不应被当成自动清空输入；复用对象时显式调用 `reset()`。

### 7.13 `hash(QByteArrayView message, QByteArrayView key, Algorithm method)`

```cpp
static QByteArray hash(
    QByteArrayView message,
    QByteArrayView key,
    QCryptographicHash::Algorithm method);
```

一次性计算消息的 HMAC，返回拥有数据的 `QByteArray`：

```cpp
const QByteArray tag =
    QMessageAuthenticationCode::hash(
        message, key, QCryptographicHash::Sha256);
```

它相当于创建对象、追加一段消息并读取 `result()`。消息和密钥只在调用期间通过 view 读取，不会取得调用方存储的所有权。

### 7.14 `hashInto(QSpan<char>, QByteArrayView, QByteArrayView, Algorithm)`

```cpp
static QByteArrayView hashInto(
    QSpan<char> buffer,
    QByteArrayView message,
    QByteArrayView key,
    QCryptographicHash::Algorithm method) noexcept;
```

Qt 6.8 起提供。将单段消息的 HMAC 写入调用方的可写 `char` 缓冲区，并返回写入区域的 `QByteArrayView`：

```cpp
std::array<char, 32> buffer;
const QByteArrayView tag =
    QMessageAuthenticationCode::hashInto(
        QSpan<char>(buffer), message, key,
        QCryptographicHash::Sha256);
```

返回的 view 借用 `buffer`。缓冲区不足时不会得到完整认证码，调用方必须检查返回 view 是否为空或长度是否符合预期。建议根据算法摘要长度分配缓冲区，而不是假设所有算法都是 32 字节。

### 7.15 `hashInto(QSpan<uchar>, QByteArrayView, QByteArrayView, Algorithm)`

```cpp
static QByteArrayView hashInto(
    QSpan<uchar> buffer,
    QByteArrayView message,
    QByteArrayView key,
    QCryptographicHash::Algorithm method) noexcept;
```

语义与 `QSpan<char>` 重载相同，只是输出缓冲区元素类型为 `uchar`。返回 view 仍然借用调用方存储：

```cpp
std::array<uchar, 32> buffer;
const auto tag = QMessageAuthenticationCode::hashInto(
    QSpan<uchar>(buffer), message, key,
    QCryptographicHash::Sha256);
```

### 7.16 `hashInto(QSpan<std::byte>, QByteArrayView, QByteArrayView, Algorithm)`

```cpp
static QByteArrayView hashInto(
    QSpan<std::byte> buffer,
    QByteArrayView message,
    QByteArrayView key,
    QCryptographicHash::Algorithm method) noexcept;
```

语义与前两个输出缓冲区重载相同，适合使用现代 C++ 字节数组：

```cpp
std::array<std::byte, 32> buffer;
const auto tag = QMessageAuthenticationCode::hashInto(
    QSpan<std::byte>(buffer), message, key,
    QCryptographicHash::Sha256);
```

`std::byte` 只是存储元素类型，不会改变 HMAC 的字节结果或编码。

### 7.17 `hashInto(QSpan<char>, QSpan<const QByteArrayView>, QByteArrayView, Algorithm)`

```cpp
static QByteArrayView hashInto(
    QSpan<char> buffer,
    QSpan<const QByteArrayView> messageParts,
    QByteArrayView key,
    QCryptographicHash::Algorithm method) noexcept;
```

Qt 6.8 起提供。按 `messageParts` 的顺序把多个消息视图连续输入 HMAC，并将结果写入 `char` 缓冲区：

```cpp
const std::array<QByteArrayView, 2> parts = {
    header, payload
};
std::array<char, 32> buffer;

const auto tag = QMessageAuthenticationCode::hashInto(
    QSpan<char>(buffer), QSpan<const QByteArrayView>(parts),
    key, QCryptographicHash::Sha256);
```

片段边界不会进入认证数据。也就是说，`["ab", "c"]` 和 `["a", "bc"]` 认证的是相同的字节序列；如果协议需要区分字段，调用方必须把长度、标签或规范化编码纳入消息。

### 7.18 `hashInto(QSpan<uchar>, QSpan<const QByteArrayView>, QByteArrayView, Algorithm)`

```cpp
static QByteArrayView hashInto(
    QSpan<uchar> buffer,
    QSpan<const QByteArrayView> messageParts,
    QByteArrayView key,
    QCryptographicHash::Algorithm method) noexcept;
```

按片段顺序计算 HMAC，并写入 `uchar` 缓冲区。输入片段和输出缓冲区在调用期间必须保持有效，返回 view 不能脱离输出缓冲区使用。

### 7.19 `hashInto(QSpan<std::byte>, QSpan<const QByteArrayView>, QByteArrayView, Algorithm)`

```cpp
static QByteArrayView hashInto(
    QSpan<std::byte> buffer,
    QSpan<const QByteArrayView> messageParts,
    QByteArrayView key,
    QCryptographicHash::Algorithm method) noexcept;
```

这是分段输入与 `std::byte` 输出的组合重载。它适合把多个已有字节视图直接送入 HMAC，同时避免先拼接一个新的 `QByteArray`。

## 8. 认证码长度、缓冲区和结果验证

### 8.1 HMAC 长度等于底层摘要长度

对给定 `method`，HMAC 输出的字节长度与对应 `QCryptographicHash` 摘要长度一致。使用 `hashInto()` 前，应按选定算法计算所需容量：

```cpp
const int required =
    QCryptographicHash::hashLength(method);
```

输出长度是原始字节数，不是十六进制字符串长度。若之后调用 `.toHex()`，可见字符数通常会变成原始字节数的两倍。

### 8.2 不要忽略 `hashInto()` 的返回值

返回的 `QByteArrayView` 同时表达了“结果在哪里”和“实际结果有多长”。不要只假定缓冲区写满了：

```cpp
const auto tag = QMessageAuthenticationCode::hashInto(
    buffer, message, key, method);

if (tag.size() != QCryptographicHash::hashLength(method))
    handleOutputBufferError();
```

调用方应把缓冲区长度和返回长度一起检查，特别是算法由配置或协议协商得到时。

### 8.3 `resultView()` 和 `hashInto()` 的生命周期不同

- `resultView()` 借用 `QMessageAuthenticationCode` 对象内部存储；
- `hashInto()` 借用调用方提供的输出缓冲区；
- `result()` 和 `hash()` 返回拥有数据的 `QByteArray`。

这三种返回形态不能互换生命周期假设。

### 8.4 验证时使用明确的比较策略

认证失败时，调用方需要比较“收到的 tag”和“本地计算的 tag”。不要让早停的普通字符串比较成为攻击者可利用的时间差异。Qt 类本身负责计算 HMAC，不负责提供完整的协议验证器；比较策略应使用项目已有的常量时间字节比较工具，并先检查长度。

## 9. 常见错误与排查顺序

### 9.1 把 HMAC 当成普通哈希

**症状：** 发送方和接收方都能计算摘要，但攻击者也能伪造消息。

**原因：** 普通摘要没有密钥，任何人都能重新计算。

**修复：** 双方使用同一秘密 key 和同一算法计算 HMAC，并保护 key。

### 9.2 自行拼接 key 和消息

**症状：** 认证协议在边界输入或密钥长度变化时出现不可预期结果。

**原因：** `hash(key + message)` 不是 HMAC，不能替代 HMAC 的标准结构。

**修复：** 使用 `QMessageAuthenticationCode`，并固定算法和消息规范化规则。

### 9.3 追加片段时忘记字段边界

**症状：** 不同字段拆分方式生成相同认证码，协议解析边界不唯一。

**原因：** `addData()` 和分段 `hashInto()` 只认证拼接后的原始字节，不认证片段边界。

**修复：** 为字段加入明确长度、类型标签或规范化编码后再认证。

### 9.4 把 `resultView()` 保存到对象修改之后

**症状：** 读取到旧结果、悬空视图或不符合预期的字节。

**原因：** view 借用认证对象内部存储，对象修改后不能假定旧 view 仍有效。

**修复：** 立即消费，或复制为 `QByteArray`。

### 9.5 设备读取失败仍然发送结果

**症状：** 对方验证失败，或者部分文件被误认为完整文件。

**原因：** `addData(QIODevice *)` 可能已经追加部分数据后返回 `false`。

**修复：** 检查返回值，失败时丢弃本次 tag；必要时先 `reset()` 并重新定位设备。

### 9.6 `hashInto()` 缓冲区太小

**症状：** 返回 view 为空或长度不符合算法摘要长度。

**原因：** 输出容量不足，且不同算法的摘要长度不同。

**修复：** 用 `QCryptographicHash::hashLength(method)` 计算容量并检查返回长度。

### 9.7 把十六进制长度当成认证码字节长度

**症状：** 缓冲区分配大了一倍，或协议比较长度错误。

**原因：** 原始 tag 是二进制字节；`.toHex()` 后每个字节变成两个 ASCII 字符。

**修复：** 明确协议传输的是原始字节还是十六进制文本，并分别处理长度。

### 9.8 直接使用弱算法或可猜的短 key

**症状：** HMAC 形式正确，但整体认证强度不足。

**原因：** 算法和密钥的安全性仍取决于协议选择与密钥熵。

**修复：** 新协议使用现代哈希算法和高熵密钥；密码输入先做密钥派生；兼容旧系统时明确风险和迁移方案。

### 9.9 以为 HMAC 自动防重放

**症状：** 攻击者重新发送一个曾经合法的请求，服务器再次接受。

**原因：** 相同消息和 key 会产生相同 HMAC，完整性不等于新鲜性。

**修复：** 把时间戳、nonce、单调递增序列号或服务端状态纳入认证消息，并验证其新鲜性。

## 10. 推荐设计模板

### 10.1 一次性消息认证

```cpp
QByteArray makeHmac(QByteArrayView canonicalMessage,
                    QByteArrayView secret)
{
    return QMessageAuthenticationCode::hash(
        canonicalMessage, secret,
        QCryptographicHash::Sha256);
}
```

`canonicalMessage` 应来自协议定义的规范化编码，而不是把多个可变字符串随意拼接。

### 10.2 读取大文件并拒绝部分结果

```cpp
QByteArray hmacDevice(QIODevice *device,
                      QByteArrayView secret)
{
    QMessageAuthenticationCode mac(
        QCryptographicHash::Sha256, secret);

    if (!mac.addData(device))
        return {};

    return mac.result();
}
```

空 `QByteArray` 也可能是合法的某种返回值约定，因此真实接口最好额外返回错误状态或使用项目统一的结果类型，不要只靠空数组区分失败。

### 10.3 固定缓冲区并验证容量

```cpp
QByteArrayView hmacIntoBuffer(
    QSpan<std::byte> buffer,
    QByteArrayView message,
    QByteArrayView secret)
{
    constexpr auto method = QCryptographicHash::Sha256;
    const auto tag = QMessageAuthenticationCode::hashInto(
        buffer, message, secret, method);

    Q_ASSERT(tag.size() == QCryptographicHash::hashLength(method));
    return tag;
}
```

生产代码应将容量不足转成可处理的错误，而不是只依赖断言。

### 10.4 比较收到的认证码

```cpp
const QByteArray expected =
    QMessageAuthenticationCode::hash(message, key, method);

if (received.size() != expected.size())
    reject();

if (!constantTimeEquals(received, expected))
    reject();
```

`constantTimeEquals` 代表项目提供的常量时间比较函数；`QMessageAuthenticationCode` 不会自动替你完成这一步。

## API 速查表
### 11.1 生命周期和状态

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMessageAuthenticationCode(Algorithm, QByteArrayView = {})` | 创建指定算法和 key 的 HMAC 状态 | 空 key 虽合法，通常不适合作为认证密钥 |
| `QMessageAuthenticationCode(QMessageAuthenticationCode &&)` | 移动构造 | Qt 6.6 起；移动后的源对象不要继续使用 |
| `~QMessageAuthenticationCode()` | 释放内部状态 | 不拥有输入 view 或 `QIODevice` |
| `operator=(QMessageAuthenticationCode &&)` | 移动赋值 | Qt 6.6 起；目标对象原状态被替换 |
| `swap(QMessageAuthenticationCode &)` | 交换内部状态 | 会影响此前取得的内部结果 view |
| `reset()` | 清除已追加消息并保留算法和 key | 不生成新 key，不重置设备位置 |
| `setKey(QByteArrayView)` | 更换 key 并开始新消息状态 | 不要把旧消息与新 key 混用 |

### 11.2 增量输入和结果

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `addData(QByteArrayView)` | 追加一段二进制消息 | 无分隔符；输入 view 只需在调用期间有效 |
| `addData(const char *, qsizetype)` | 按指针和长度追加消息 | 不是 C 字符串；长度必须覆盖可读字节 |
| `addData(QIODevice *)` | 从设备读到结束并追加 | 检查返回值；失败时可能已有部分状态 |
| `resultView() const` | 返回内部 HMAC 的借用视图 | 对象修改后不要继续使用旧 view |
| `result() const` | 返回拥有数据的 HMAC | 适合保存、返回和跨操作使用 |

### 11.3 一次性计算

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `hash(QByteArrayView, QByteArrayView, Algorithm)` | 一次性计算单段消息 HMAC | 返回拥有数据的 `QByteArray` |
| `hashInto(QSpan<char>, QByteArrayView, QByteArrayView, Algorithm)` | 写入 `char` 缓冲区 | Qt 6.8 起；检查返回长度 |
| `hashInto(QSpan<uchar>, QByteArrayView, QByteArrayView, Algorithm)` | 写入 `uchar` 缓冲区 | 返回 view 借用调用方缓冲区 |
| `hashInto(QSpan<std::byte>, QByteArrayView, QByteArrayView, Algorithm)` | 写入 `std::byte` 缓冲区 | Qt 6.8 起；不自动分配 |
| `hashInto(QSpan<char>, QSpan<const QByteArrayView>, QByteArrayView, Algorithm)` | 分段输入并写入 `char` 缓冲区 | 片段按顺序拼接，无边界标记 |
| `hashInto(QSpan<uchar>, QSpan<const QByteArrayView>, QByteArrayView, Algorithm)` | 分段输入并写入 `uchar` 缓冲区 | 输入和输出存储必须在调用期间有效 |
| `hashInto(QSpan<std::byte>, QSpan<const QByteArrayView>, QByteArrayView, Algorithm)` | 分段输入并写入 `std::byte` 缓冲区 | 适合避免拼接临时数组 |

### 11.4 协作类型和协议检查

| API 或类型 | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QCryptographicHash::Algorithm` | 选择底层哈希算法 | 新协议不要随意使用弱算法 |
| `QCryptographicHash::hashLength(method)` | 获取认证码原始字节长度 | 用于分配 `hashInto()` 缓冲区 |
| `QByteArrayView` | 不拥有输入或结果存储的字节视图 | 关注底层存储生命周期 |
| `QSpan<T>` | 描述输出缓冲区或分段输入数组 | 不拥有元素存储 |
| `result().toHex()` | 把二进制 tag 转成文本 | 长度通常变为原始字节数的两倍 |
| 常量时间比较 | 验证收到的 tag | 先检查长度，再使用项目安全比较函数 |

## 12. 一句话总结

`QMessageAuthenticationCode` 是 Qt 的 HMAC 状态对象：用固定算法和共享密钥对规范化消息做认证，流式输入用 `addData()`，一次性计算用 `hash()`，低分配场景用 `hashInto()`，结果需要长期保存时用拥有数据的 `result()`，并始终把密钥管理、常量时间比较和防重放设计留在协议层明确处理。
