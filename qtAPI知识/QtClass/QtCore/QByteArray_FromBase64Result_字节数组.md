# QByteArray::FromBase64Result 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QByteArray>`  
> 所属模块：`Qt6::Core`  
> 类型性质：`QByteArray` 的嵌套结果类型，用于承载 Base64 解码数据和解码状态。

## 1. 它解决的是“结果为空到底是不是错误”

`QByteArray::FromBase64Result` 是 `QByteArray::fromBase64Encoding()` 的返回类型。它把两件必须同时关心的事情装在一起：

- 解码得到的字节数据。
- 输入是否按照当前解码策略成功处理。

只使用旧的 `QByteArray::fromBase64()` 时，返回值只有一个 `QByteArray`。严格解码失败时会得到空数组，但“输入本来就表示空数据”同样也可能得到空数组，于是结果是否可信变得模糊。

`FromBase64Result` 用显式状态解决这个歧义：

```cpp
const auto result = QByteArray::fromBase64Encoding(
    encoded,
    QByteArray::AbortOnBase64DecodingErrors);

if (!result) {
    // 输入不符合要求，不能把 decoded 当作有效业务数据
    return;
}

const QByteArray &payload = *result;
```

它很像一个轻量的 `expected<QByteArray, Error>`：真值表示成功，解引用取得值；不过它不是 `std::expected`，状态和数据字段是公开成员。

## 2. 从哪里得到它

这个类型不能独立调用构造函数来完成解码。正常入口是两个 `QByteArray::fromBase64Encoding()` 重载：

```cpp
const QByteArray encoded = "SGVsbG8=";
const auto result = QByteArray::fromBase64Encoding(encoded);
```

也可以把不再使用的输入作为右值传入：

```cpp
QByteArray encoded = readEncodedPayload();
auto result = QByteArray::fromBase64Encoding(std::move(encoded));
```

右值重载适合调用方明确不再需要 `encoded` 的场景。调用后不要再依赖 `encoded` 原来的内容；Qt 可以利用该所有权转移优化解码过程。

## 3. 推荐的两种用法

### 3.1 简洁的 bool 加解引用写法

```cpp
void process(const QByteArray &payload);

if (auto result = QByteArray::fromBase64Encoding(
        encoded,
        QByteArray::AbortOnBase64DecodingErrors)) {
    process(*result);
}
```

`operator bool()` 是显式转换，所以它适合 `if`、`while` 这类条件上下文，却不会在普通赋值中悄悄变成整数或布尔值。

### 3.2 需要错误分类时直接访问字段

```cpp
const auto result = QByteArray::fromBase64Encoding(
    encoded,
    QByteArray::AbortOnBase64DecodingErrors);

switch (result.decodingStatus) {
case QByteArray::Base64DecodingStatus::Ok:
    consume(result.decoded);
    break;
case QByteArray::Base64DecodingStatus::IllegalInputLength:
case QByteArray::Base64DecodingStatus::IllegalCharacter:
case QByteArray::Base64DecodingStatus::IllegalPadding:
    reportInvalidToken();
    break;
}
```

这种形式适合网络协议、令牌、配置文件等必须记录失败原因的边界层。

## 4. 解码策略决定“成功”意味着什么

`fromBase64Encoding()` 接受 `QByteArray::Base64Options`。最容易忽略的是默认策略：

```cpp
QByteArray::Base64Encoding
```

它也意味着默认的 `IgnoreBase64DecodingErrors`。在宽松模式下，输入中的非法字符会被跳过，解码会继续进行。因此即使结果对象为真，也不能把它当成“原始输入严格符合 Base64 规范”的证明。

需要把输入完整性当作业务前提时，必须显式启用严格模式：

```cpp
const auto result = QByteArray::fromBase64Encoding(
    encoded,
    QByteArray::Base64Encoding
        | QByteArray::AbortOnBase64DecodingErrors);

if (!result) {
    rejectRequest();
    return;
}
```

Base64 URL 变体则使用：

```cpp
QByteArray::Base64UrlEncoding
    | QByteArray::AbortOnBase64DecodingErrors
```

`KeepTrailingEquals` 与 `OmitTrailingEquals` 是编码输出选项；解码时会被忽略。严格解码要求输入没有填充，或包含正确数量的尾部 `=`；宽松策略则不会因缺少或多余的尾部 `=` 报错。

## 5. decodingStatus 的含义

`decodingStatus` 的类型是 `QByteArray::Base64DecodingStatus`。Qt 头文件定义的状态如下：

| 状态 | 是否成功 | 含义 | 业务处理建议 |
| --- | --- | --- | --- |
| `Ok` | 是 | 解码按当前选项成功完成。 | 才能把 `decoded` 作为可靠的解码结果使用。 |
| `IllegalInputLength` | 否 | 输入长度不符合 Base64 可解码的长度规则。 | 检查截断、拼接或 URL 参数传递是否丢失字符。 |
| `IllegalCharacter` | 否 | 输入出现当前 Base64 字母表不允许的字符。 | 区分标准 Base64 与 URL Base64，并检查传输是否污染。 |
| `IllegalPadding` | 否 | 尾部填充 `=` 的位置或数量不合法。 | 检查是否启用了严格模式，以及发送方是否省略或错误补齐填充。 |

`operator bool()` 只是在判断：

```cpp
result.decodingStatus == QByteArray::Base64DecodingStatus::Ok
```

严格模式失败后，`decoded` 包含什么由 Qt 文档标为未指定。不要因为字段存在就继续消费它。

## 6. 解引用的三种引用限定重载

`operator*()` 返回解码出的 `QByteArray`，但返回类型依赖结果对象的值类别：

```cpp
auto result = QByteArray::fromBase64Encoding(encoded);

QByteArray &mutableBytes = *result;            // 左值，得到可写引用
const QByteArray &readOnlyBytes =
    *std::as_const(result);                     // const 左值，得到只读引用

QByteArray ownedBytes =
    *std::move(result);                         // 右值，可移动取得字节数组
```

通常只需写 `*result`。只有在很清楚生命周期和所有权时才使用 `*std::move(result)`：

- 结果对象之后不再需要。
- 需要把其中的 `QByteArray` 转移到长期持有者。
- 仍然要先确认 `result` 为真。

不要返回指向临时 `FromBase64Result` 解引用结果的引用：

```cpp
// 错误：临时 result 在语句结束后销毁
const QByteArray &bad =
    *QByteArray::fromBase64Encoding(encoded);
```

若要持久保存，复制或移动到自己的 `QByteArray`：

```cpp
QByteArray decoded =
    *QByteArray::fromBase64Encoding(encoded);
```

但上面仍遗漏了失败检查。生产代码应先保存结果、判断成功，再取数据。

## 7. 两个公开字段的使用边界

`decoded` 和 `decodingStatus` 都是 public 成员：

```cpp
QByteArray::FromBase64Result result =
    QByteArray::fromBase64Encoding(encoded);

qDebug() << result.decodingStatus << result.decoded;
```

公开不代表建议随意改写。手动修改 `decoded` 或 `decodingStatus` 能制造出不反映真实解码过程的对象，特别是在测试以外的业务代码中没有意义。

读取时的顺序应该固定为：

1. 先检查 `result` 或 `decodingStatus`。
2. 仅在 `Ok` 时使用 `decoded`。

## 8. 比较和哈希的一个非直觉细节

两个 `FromBase64Result` 相等的条件是：

1. `decodingStatus` 相同。
2. 如果状态为 `Ok`，`decoded` 也必须相同。

这意味着同为某个失败状态的两个对象相等比较时，`decoded` 内容不参与比较。这样做是合理的，因为严格失败时 decoded 内容未指定，不能把它当稳定结果。

```cpp
if (left == right) {
    // 两者状态相同；若成功，解码字节也相同
}
```

`qHash()` 遵循相同的比较语义，因此该类型可以作为 `QHash` 键。用它做缓存键时要想清楚：失败结果聚合的是状态，而不是任何未指定的部分解码内容。

## 9. 什么时候用它，什么时候用 fromBase64()

优先使用 `fromBase64Encoding()` 和 `FromBase64Result`：

- 输入来自网络、URL、JWT 片段、配置、剪贴板或用户输入。
- 需要区分“合法的空数据”和“解码失败”。
- 需要严格拒绝非法字符、长度或 padding。
- 需要记录失败分类。

`fromBase64()` 适合你明确选择宽松解码，且只关心最终字节的简单场景。但 Qt 文档建议新代码使用 `fromBase64Encoding()`，因为结果类型能保留成功与失败信息。

## 10. 常见错误

### 10.1 用默认选项验证安全敏感输入

默认会忽略解码错误。需要验证 token 或签名相关编码时，必须使用 `AbortOnBase64DecodingErrors`，再判断结果。

### 10.2 失败后仍使用 decoded

严格解码失败时，`decoded` 的内容未指定。失败分支只能处理错误，不能继续解析该字段。

### 10.3 忘记 Base64UrlEncoding

URL、JWT 等场景经常使用 `-` 和 `_` 的 Base64 URL 字母表。把它按普通 Base64 严格解码会得到 `IllegalCharacter`。

### 10.4 把结果对象当长期字节容器

它的职责是传递一次解码结果和状态。长期保存解码数据时，先检查状态，再保存 `decoded` 或通过右值解引用移动取出。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结果字段 | `QByteArray decoded` | 保存 Base64 解码出的字节数组。 | 仅在 `decodingStatus == Ok` 时视为有效；严格失败时内容未指定。 |
| 结果字段 | `QByteArray::Base64DecodingStatus decodingStatus` | 保存解码成功或失败的分类状态。 | 用它或 `operator bool()` 先判断，不要只靠 `decoded.isEmpty()`。 |
| 状态转换 | `explicit operator bool() const noexcept` | 判断解码是否成功。 | 等价于检查状态是否为 `Ok`；适合 `if (result)`。 |
| 取值 | `QByteArray &operator*() & noexcept` | 从可写左值结果对象取得可写解码数据引用。 | 结果对象必须存活；仍应先确认解码成功。 |
| 取值 | `const QByteArray &operator*() const & noexcept` | 从 const 左值结果对象取得只读解码数据引用。 | 引用随结果对象生命周期结束而失效。 |
| 取值 | `QByteArray &&operator*() && noexcept` | 从右值结果对象移动取出解码数据。 | 适合 `*std::move(result)`；移动后不再依赖 result 中的数据。 |
| 工具 | `void swap(FromBase64Result &other) noexcept` | 交换两个结果对象的数据和状态。 | 交换后成功状态和 decoded 会一并互换。 |
| 比较 | `operator==(const FromBase64Result &lhs, const FromBase64Result &rhs)` | 比较两个解码结果是否相等。 | 状态必须相同；仅当状态为 `Ok` 时比较 decoded。 |
| 比较 | `operator!=(const FromBase64Result &lhs, const FromBase64Result &rhs)` | 比较两个解码结果是否不相等。 | 与相等比较互补。 |
| 哈希 | `qHash(const FromBase64Result &key, size_t seed = 0)` | 生成可用于 Qt 哈希容器的哈希值。 | 哈希语义与相等比较一致，失败结果不应依赖 decoded 内容区分。 |

## 12. 相关入口速查

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 解码入口 | `QByteArray::fromBase64Encoding(const QByteArray &base64, Base64Options options)` | 从保留的输入数组解码并返回带状态结果。 | 适合输入后续仍要使用的场景；新代码优先选它。 |
| 解码入口 | `QByteArray::fromBase64Encoding(QByteArray &&base64, Base64Options options)` | 从右值输入解码并返回带状态结果。 | 传入 `std::move` 后不应依赖原数组内容。 |
| 旧入口 | `QByteArray::fromBase64(const QByteArray &base64, Base64Options options)` | 解码后只返回字节数组。 | 失败和有效空输出难区分；Qt 推荐新代码使用带结果对象的入口。 |
| 选项 | `QByteArray::Base64Encoding` | 使用普通 Base64 字母表。 | 默认编码和解码字母表；URL 场景不一定适用。 |
| 选项 | `QByteArray::Base64UrlEncoding` | 使用 URL 友好的 Base64 字母表。 | JWT 等常见；严格模式时应与输入格式匹配。 |
| 选项 | `QByteArray::IgnoreBase64DecodingErrors` | 解码时跳过非法输入并继续。 | 默认宽松策略，不可用作严格格式验证。 |
| 选项 | `QByteArray::AbortOnBase64DecodingErrors` | 在第一个解码错误处停止。 | 验证外部输入时应组合使用，并检查结果状态。 |

## 13. 一句话总结

`QByteArray::FromBase64Result` 把 Base64 的“解码字节”和“是否可信”绑定在一起；外部输入应使用严格选项、先检查结果状态，再消费 `decoded`。
