# Qt QByteArray 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QByteArray>`  
> 所属模块：`Qt6::Core`  
> 定位：保存任意 8-bit 字节的隐式共享值类型，可用于二进制数据、UTF-8 文本和协议负载

## 1. QByteArray 解决什么问题

`QByteArray` 保存的是字节，不是“默认 UTF-8 字符串”。它适合：

- 网络包、哈希、压缩数据、文件内容和二进制协议。
- UTF-8/Latin-1 等编码后的文本字节。
- 和 `QIODevice`、`QBuffer`、`QDataStream` 交换数据。

它不适合直接按用户可见字符处理 Unicode 文本。界面文本、自然语言搜索、大小写转换和按字符切片优先使用 `QString`。

```cpp
QByteArray packet = socket->readAll();  // 二进制或协议字节
QString text = QString::fromUtf8(packet); // 明确按 UTF-8 解码
```

## 2. 隐式共享、data 和指针有效期

```cpp
QByteArray a = "abc";
QByteArray b = a; // 通常共享底层数据
b[0] = 'A';       // 修改时分离
```

复制 QByteArray 通常很便宜，但任何可能修改数据的操作都可能 detach 并让先前的裸指针、迭代器和 view 失效：

```cpp
const char *p = bytes.constData();
bytes.append('x'); // p 之后不要再使用
```

- `constData()` 返回只读指针，不触发分离。
- 非 const `data()` 允许修改，并可能触发分离。
- `QByteArrayView` 不拥有数据，源 QByteArray 改动、析构或分离后 view 可能悬空。

跨线程传递 QByteArray 的值通常安全，但不要让多个线程同时修改同一个实例或共享同一裸 `data()` 指针。

## 3. 二进制数据可以包含零字节

```cpp
const QByteArray binary("A\0B", 3);
qDebug() << binary.size(); // 3
```

不要用依赖零结尾的 API 处理二进制内容：

```cpp
bytes.append(data, length); // 正确，显式长度
bytes.append(data);         // 只适合零结尾 C 字符串
```

同理，`QByteArray(const char *)` 默认依赖 `strlen`，`QByteArray(const char *, size)` 才适合任意协议字节。

## 4. 容量和构造输出

```cpp
QByteArray payload;
payload.reserve(4096);
payload.append(header);
payload.append(body);
```

重复追加前 `reserve()` 能减少重新分配。读取到已有大小的输出缓冲时：

```cpp
QByteArray bytes;
bytes.resizeForOverwrite(expectedSize);
const qint64 count = device.read(bytes.data(), bytes.size());
```

`resizeForOverwrite()` 生成未初始化字节，只能在后续立即完整写满时使用。不要把未初始化内容写入日志、网络或文件。

## 5. 文本、数值和编码

```cpp
const QByteArray utf8 = QStringLiteral("你好").toUtf8();
const QString text = QString::fromUtf8(utf8);

bool ok = false;
const int port = QByteArray("8080").toInt(&ok);
```

数值转换必须检查 `ok`：

```cpp
const int value = input.toInt(&ok, 10);
if (!ok || value < 0 || value > 65535)
    return;
```

`toLower()`、`toUpper()`、`trimmed()` 和 `simplified()` 主要是字节/ASCII 风格操作；国际化文本规范化和大小写处理交给 QString。

## 6. Base64、hex 和 percent 编码

```cpp
const QByteArray token = raw.toBase64(
    QByteArray::Base64UrlEncoding
    | QByteArray::OmitTrailingEquals);

const auto decoded =
    QByteArray::fromBase64Encoding(
        token,
        QByteArray::Base64UrlEncoding
        | QByteArray::AbortOnBase64DecodingErrors);

if (!decoded)
    return;
consume(*decoded);
```

`fromBase64()` 默认可能忽略某些错误。处理令牌、签名、协议字段等不可信数据时，使用 `fromBase64Encoding()` 并检查 `Base64DecodingStatus`。

`toHex()`、`fromHex()` 适合日志、调试和固定编码字段；它们会使数据体积大约翻倍。percent 编码主要用于 URL 组件，不要手写编码规则，URL 整体处理优先 `QUrl`。

## 7. `fromRawData()` 和 `setRawData()`：零拷贝但高风险

```cpp
QByteArray view = QByteArray::fromRawData(data, length);
```

它不会复制 `data`，也不会取得所有权。源内存必须在 QByteArray 使用期间有效，且不应被意外修改。要得到独立副本：

```cpp
QByteArray copy = QByteArray::fromRawData(data, length);
copy.detach();
```

这种接口只适合严格控制生命周期的底层优化，不适合普通业务代码。

## 8. 常见误区

### 把 QByteArray 当 Unicode 字符串

字节长度不等于字符数，`indexOf()` 位置是字节位置。用户可见文本用 QString。

### 用 const char * 传二进制数据

嵌入零字节会被截断。始终传指针和长度，或传 QByteArray/QByteArrayView。

### 忽略 Base64 解码错误

认证、令牌和协议解析需要严格模式，并检查 result。

### 保存 `data()` 后继续修改数组

append、resize、detach 都可能让指针失效。缩小指针使用范围。

### 用 `setRawData()` 管理外部内存

QByteArray 不拥有外部内存，容易悬空或误以为会释放。普通代码使用复制构造。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QByteArray()` | 创建空字节数组。 | 空数组可能是 null，和仅 size 为 0 的已分配数组语义可区分。 |
| 构造 | `QByteArray(const char *, qsizetype size = -1)` | 从原始字节创建数组。 | `size=-1` 依赖零结尾；二进制数据务必传显式长度。 |
| 构造 | `QByteArray(qsizetype, char)` | 创建指定长度并填充相同字节。 | 适合初始化固定缓冲；避免用于敏感数据残留。 |
| 构造 | `QByteArray(qsizetype, Qt::Initialization)` | 创建指定长度的初始化或未初始化缓冲。 | Uninitialized 内容必须立即完全写入。 |
| 构造 | `QByteArray(QByteArrayView)` | 从非拥有 view 复制字节。 | 得到独立值，适合延长数据生命周期。 |
| 复制移动 | 拷贝、移动、赋值、`swap()` | 复制、移动或交换数组。 | 复制通常隐式共享，首次修改可能 detach。 |
| 容量 | `size()` / `length()` | 返回字节数。 | 是字节长度，不是 Unicode 字符数。 |
| 容量 | `isEmpty()` | 判断 size 是否为 0。 | 空不等于输入有效；协议还要验证字段规则。 |
| 容量 | `isNull()` | 判断是否为 null 数组。 | Qt 兼容语义存在，普通业务通常关注 isEmpty。 |
| 容量 | `capacity()` | 返回已分配容量。 | 容量不是有效数据长度，不要序列化未使用部分。 |
| 容量 | `reserve(qsizetype)` | 预留容量减少反复追加重分配。 | 只优化已确认的热点，不改变 size。 |
| 容量 | `squeeze()` / `shrink_to_fit()` | 尝试缩小多余容量。 | 可能重新分配并使指针、view、迭代器失效。 |
| 容量 | `resize(qsizetype)` | 改变数组长度。 | 扩展部分的内容规则要确认；敏感输出要显式初始化。 |
| 容量 | `resize(qsizetype, char)` | 改变长度并填充新增部分。 | 适合可预测填充值，不适合省略初始化。 |
| 容量 | `resizeForOverwrite(qsizetype)` | 申请未初始化输出缓冲。 | 只能在完全覆盖写入前使用，不能读取未初始化字节。 |
| 数据 | `data()` | 返回可修改数据指针。 | 可能 detach；任何后续修改/重分配都可能使指针失效。 |
| 数据 | `constData()` | 返回只读数据指针。 | 不拥有指针；数组析构或分离后指针无效。 |
| 共享 | `detach()` | 强制将共享数据分离为独占副本。 | 仅在生命周期或性能确有需求时使用。 |
| 共享 | `isDetached()` | 判断当前是否独占底层数据。 | 是优化诊断，不应作为业务逻辑分支。 |
| 共享 | `isSharedWith(QByteArray)` | 判断两个数组是否共享同一底层数据。 | 只用于调试/优化分析，修改后关系会变化。 |
| 清空 | `clear()` | 清空数组内容。 | 不保证安全擦除内存；敏感数据需专门方案。 |
| 元素 | `at()` / `operator[]` | 按字节索引读取或修改元素。 | 越界是编程错误；位置是字节偏移。 |
| 元素 | `front()` / `back()` | 读取或修改首尾字节。 | 空数组调用无效，先检查 isEmpty。 |
| 查找 | `indexOf()` / `lastIndexOf()` | 查找字节或字节序列位置。 | 返回字节偏移，找不到为 -1。 |
| 查找 | `contains()` / `count()` | 判断或统计字节序列出现情况。 | 对大数据会遍历；不要放在不必要的嵌套循环。 |
| 比较 | `compare(QByteArrayView, CaseSensitivity)` | 按字节比较两个数组。 | 忽略大小写是 ASCII 风格，Unicode 文本用 QString。 |
| 切片 | `left()` / `right()` / `mid()` | 返回数组一部分。 | 返回新值；索引是字节位置。 |
| 切片 | `first()` / `last()` / `sliced()` / `chopped()` | 以更明确边界取得子数组。 | Qt 6 API 对越界有断言契约，先验证范围。 |
| 修改 | `truncate()` / `chop()` | 截断末尾字节。 | 会改变 size，已保存 view/迭代器可能失效。 |
| 修改 | `slice()` | 原地保留指定子范围。 | 修改自身且可能影响共享；输入范围必须有效。 |
| 修改 | `append()` / `prepend()` / `operator+=` | 在尾部或头部追加字节。 | 对 C 字符串重载依赖零结尾；二进制用长度或 QByteArrayView。 |
| 修改 | `insert()` | 在指定位置插入字节。 | 可能重分配；频繁头部插入会有成本。 |
| 修改 | `remove()` / `removeAt()` / `removeFirst()` / `removeLast()` | 删除指定字节或范围。 | 索引是字节位置，修改后迭代器失效。 |
| 修改 | `removeIf()` | 按谓词删除满足条件的字节。 | 谓词应轻量且不修改同一数组。 |
| 修改 | `replace()` | 替换位置、字节或字节序列。 | 二进制替换传 QByteArrayView 和长度，避免 C 字符串截断。 |
| 填充 | `fill(char, size)` | 用相同字节填充全部或指定长度。 | 可用于初始化；不是可靠的敏感数据擦除承诺。 |
| 文本 | `toLower()` / `toUpper()` | 返回 ASCII 风格大小写变换的字节数组。 | 国际化文本不要用，转换前先解码为 QString。 |
| 文本 | `trimmed()` / `simplified()` | 去除或压缩 ASCII 空白。 | 不是 Unicode 全语义文本规范化。 |
| 文本 | `isValidUtf8()` | 判断字节是否构成有效 UTF-8。 | 有效 UTF-8 不等于业务文本有效或安全。 |
| 文本 | `split(char)` | 按一个字节分割为多个 QByteArray。 | 适合简单 ASCII 协议；大数据会产生多个副本。 |
| 文本 | `repeated(qsizetype)` | 重复数组内容。 | 参数过大可能造成巨大分配，外部输入需限制。 |
| 数值 | `toInt()` / `toUInt()` / `toLongLong()` / `toULongLong()` | 将字节文本解析为整数。 | 必须使用 ok 参数并验证范围与进制。 |
| 数值 | `toShort()` / `toUShort()` / `toLong()` / `toULong()` | 将字节文本解析为其他整数类型。 | 平台 long 宽度不同，协议优先固定 qint 类型。 |
| 数值 | `toFloat()` / `toDouble()` | 将字节文本解析为浮点数。 | 检查 ok，避免用于精确金额。 |
| 数值 | `number()` / `setNum()` | 将数值编码为字节文本。 | 协议明确进制、格式和精度，避免默认 locale 误解。 |
| Base64 | `toBase64(Base64Options)` | 把字节编码为 Base64 或 URL-safe Base64。 | 选择是否保留 `=`，读写双方约定一致。 |
| Base64 | `fromBase64()` | 从 Base64 解码字节。 | 默认容错策略可能过宽；安全输入优先 fromBase64Encoding。 |
| Base64 | `fromBase64Encoding()` | 返回解码结果和明确状态。 | 检查 bool/status，令牌和签名输入使用 AbortOnBase64DecodingErrors。 |
| Base64 | `Base64Option` / `Base64Options` | 控制普通/URL-safe、尾随等号和错误策略。 | 传输协议必须固定选项组合。 |
| Base64 | `Base64DecodingStatus` | 表示 Base64 是否成功及失败原因。 | 把非法长度、字符和 padding 当输入错误处理。 |
| Hex | `toHex(char separator = '\0')` | 将字节编码为十六进制文本。 | 体积约翻倍，适合日志、调试和固定文本协议。 |
| Hex | `fromHex()` | 将十六进制文本解码为字节。 | 外部输入仍要验证格式和长度。 |
| Percent | `toPercentEncoding()` | 进行百分号编码。 | 更适合 URL 组件；完整 URL 优先使用 QUrl。 |
| Percent | `fromPercentEncoding()` / `percentDecoded()` | 还原百分号编码。 | 不会自动验证 URL 语义或安全性。 |
| 原始内存 | `fromRawData(const char *, qsizetype)` | 创建不拥有外部内存的 QByteArray view。 | 源内存必须持续有效；普通代码优先复制。 |
| 原始内存 | `setRawData(const char *, qsizetype)` | 让数组改为引用外部原始内存。 | 不接管释放责任，极易产生悬空引用。 |
| 终止符 | `nullTerminated()` / `nullTerminate()` | 确保数据有额外零终止符。 | 不改变 binary 的 size 语义；仅在调用 C API 时按需使用。 |
| STL | `begin()` / `end()` / `rbegin()` / `rend()` | 提供字节迭代器。 | 修改数组会使迭代器失效；不要跨 detach 保存。 |
| STL | `fromStdString()` / `toStdString()` | 与 std::string 转换。 | std::string 仍是字节序列，不自动代表 UTF-8 文本。 |
| 压缩 | `qCompress()` / `qUncompress()` | 压缩或解压 QByteArray。 | 解压不可信输入前限制大小，避免资源耗尽。 |
| 流 | `operator<<(QDataStream &, QByteArray)` | 将字节数组写入 QDataStream。 | 格式含长度，外部读端应限制分配并检查 stream status。 |
| 流 | `operator>>(QDataStream &, QByteArray &)` | 从 QDataStream 读取字节数组。 | 不可信长度可能导致资源压力，协议层需要上限。 |
| 宏 | `QByteArrayLiteral` | 从编译期字面量创建 QByteArray。 | 适合固定 ASCII/字节常量；不要误用于动态 Unicode 文本。 |

---

### 一句话总结

`QByteArray` 是字节容器，不是 Unicode 文本类。二进制接口始终携带长度，文本转换显式指定编码，外部 Base64 严格检查状态，修改后不保留旧 data/view 指针；这几条能避免绝大多数协议和生命周期问题。
