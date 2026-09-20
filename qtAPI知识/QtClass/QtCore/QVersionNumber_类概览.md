# Qt QVersionNumber：保存任意段的版本号，而不是字符串

`QVersionNumber` 用一组整数段表示版本，例如 `1.2.3`、`2026.9.11.4` 或 `5.4.0`。它解决的是版本号的构造、比较、前缀匹配、规范化和文本解析问题，避免业务代码把版本当普通字符串进行错误的词典序比较。

```cpp
#include <QVersionNumber>

const QVersionNumber installed(6, 8, 2);
const QVersionNumber minimum(6, 7);

if (installed >= minimum)
    enableFeature();
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVersionNumber>`  
> CMake：`Qt6::Core`  
> 类型：无 QObject 生命周期的可复制值类型；支持任意数量的整数段。

## 它解决什么问题

版本比较不能用字符串：

```cpp
QStringLiteral("1.10") < QStringLiteral("1.9") // 字典序，结论不适合版本语义
```

`QVersionNumber` 按第 0 段、第 1 段、后续段的数值顺序进行比较，并保留版本到底写了多少段。它适合：

- 检查安装的软件或插件是否满足最低版本；
- 解析 `5.4.0-alpha` 中的数值部分，同时保留 `-alpha` 的起始位置；
- 在协议或文件格式中表示 `major.minor.patch` 之外的多段版本；
- 判断两个版本是否共享某个 API/协议前缀。

它不解析 SemVer 的预发布和构建元数据规则，也不判断某个版本“是否兼容”。`-alpha`、`-rc.1`、发行渠道、vendor 版本和兼容策略需要调用方单独处理。

## 段数是值的一部分

最容易误解的地方是：`QVersionNumber(1, 2)` 与 `QVersionNumber(1, 2, 0)` **不相等**。

```cpp
const QVersionNumber a(1, 2);
const QVersionNumber b(1, 2, 0);

Q_ASSERT(a != b);
Q_ASSERT(QVersionNumber::compare(a, b) < 0);
Q_ASSERT(a.normalized() == b.normalized());
```

`compare()` 逐段比较到较长版本结束，因此缺失段和显式尾随零不是同一个原始版本。`normalized()` 会删除所有尾随零，适合业务语义把 `1.2` 与 `1.2.0` 看成等价的情况。

这也解释了两个不同问题：

- **严格相等**：使用 `==`，段数和每一段都必须相同；
- **忽略尾随零的版本等价**：比较 `normalized()` 结果；
- **最低版本门槛**：先定义清楚缺失段如何处理。若产品约定 `1.2` 等价于 `1.2.0`，应先规范化再比较。

不要把 `normalized()` 当成格式化操作后随手调用。若“写出 patch 0”和“未声明 patch”在协议中有不同含义，必须保留原对象。

## 构造、null 和读取缺失段

默认构造产生 null version，即**零个段**：

```cpp
const QVersionNumber none;
Q_ASSERT(none.isNull());
Q_ASSERT(none.segmentCount() == 0);
```

它不同于 `QVersionNumber(0)`，后者有一个值为 0 的段。`majorVersion()`、`minorVersion()`、`microVersion()` 与 `segmentAt()` 在请求不存在的段时都返回 `0`，所以不能只凭这些 getter 的返回值判断该段是否真的存在。

```cpp
const QVersionNumber version(7);
Q_ASSERT(version.minorVersion() == 0);
Q_ASSERT(version.segmentCount() == 1); // 没有显式 minor 段
```

只要需要区分“缺失”与“明确为零”，应结合 `segmentCount()` 判断。`segments()` 返回一份 `QList<int>`，适合需要完整段列表时读取；它不是可原位修改的视图。

构造方式覆盖常见数据来源：

```cpp
QVersionNumber semantic(1, 4, 2);
QVersionNumber extended { 2026, 9, 11, 4 };
QVersionNumber fromList(QList<int> { 3, 0, 7 });
```

Qt 6.8 起还可从 `QSpan<const int>` 构造。对象不可通过迭代器原位修改段；要修改版本，创建新版本或取出 `segments()` 后构造新的对象。

## 比较、前缀和共同父版本

`isPrefixOf(other)` 判断当前对象的所有段是否正好是 `other` 的开头：

```cpp
const QVersionNumber api(5, 3);
const QVersionNumber implementation(5, 3, 1);

Q_ASSERT(api.isPrefixOf(implementation));
```

这不是“范围匹配”或“兼容性检查”。`5.3` 是 `5.3.1` 的前缀，但 `5.3.0` 不是，因为显式的第三段必须匹配。

`commonPrefix(v1, v2)` 返回两个版本共有的最长前缀。例如 `5.3.1` 和 `5.3.8` 得到 `5.3`。它适合根据层次版号找到共同的协议族或 API 基线，不替代业务兼容矩阵。

`compare(v1, v2)` 返回负数、零或正数。比较运算符 `==`、`!=`、`<`、`<=`、`>`、`>=` 提供同一顺序语义；在支持 C++20 三路比较的构建下也可使用强比较。版本对象可放入排序容器，但是否需要先规范化取决于业务规则。

## 文本解析：数值部分和 suffix 分开

`fromString()` 解析由 `.` 分隔的非负十进制数字段；数值部分结束后的剩余文本视为 suffix，并可通过 `suffixIndex` 获得其起点：

```cpp
const QLatin1StringView text("5.4.0-alpha");
qsizetype suffixIndex = 0;
const QVersionNumber version =
    QVersionNumber::fromString(text, &suffixIndex);

Q_ASSERT(version == QVersionNumber(5, 4, 0));
Q_ASSERT(text.sliced(suffixIndex) == "-alpha");
```

`QVersionNumber` 不会解释 suffix 的优先级。例如按 SemVer，`1.0.0-alpha` 小于 `1.0.0`；`QVersionNumber` 只给你数值段和 suffix 边界，排序规则仍应由业务或专用 SemVer 解析器实现。

解析没有独立的错误对象。对外部文本应同时检查：

- `isNull()`，确认确实读到了需要的数值段；
- `suffixIndex`，确认数值部分在预期位置结束；
- 每段数值、段数和 suffix 是否符合产品协议；
- 不要把 null 版本自动当作 `0.0.0`。

Qt 6.4 起首选 `QAnyStringView` 与 `qsizetype *suffixIndex` 重载。旧版以 `int *` 为 suffix 索引的重载已经弃用，跨版本库接口不要继续围绕它设计。

## 格式化、遍历和存储

`toString()` 用 `.` 连接实际保存的所有段；它不会自动去除尾随零。需要规范输出时先调用 `normalized().toString()`。

Qt 6.8 起 `QVersionNumber` 提供只读随机访问迭代器，因此可以直接遍历：

```cpp
for (int segment : QVersionNumber { 1, 2, 3, 4 })
    qDebug() << segment;
```

这些迭代器的 `reference` 和 `pointer` 也是只读兼容类型，没有 mutable iterator；不能通过迭代器修改版本段。

`QDataStream << >>` 可读写该值，`qHash()` 支持作 `QHash`/`QSet` 键，`QDebug <<` 适合诊断。数据流的 `version` 对象和 `QDataStream::version()` 是两件事：前者是你要写入的数据，后者是流格式版本设置。跨进程、跨版本或落盘时仍须统一流版本、字节序和错误处理，不能把 Qt 数据流当作天然跨语言协议。

## 生命周期、线程和常见错误

它不需要事件循环，没有 QObject 线程归属，复制和移动都按值语义处理。小段数版本可使用内部紧凑存储，较长版本才需要额外存储；这是实现优化，不应成为调用方的 ABI 或性能假设。

不同线程各持有副本没有问题；共享同一个可变变量则仍要遵守 C++ 数据竞争规则。

- 将 `1.2` 和 `1.2.0` 当作 `==` 的相等值。
- 以 `majorVersion() == 0` 推断版本缺失，忽略它可能是显式 `0`。
- 用 `segmentAt()` 的 0 回退值代替 `segmentCount()` 做输入完整性校验。
- 以为 `fromString("1.0-rc1")` 会替你比较 `rc1` 与正式版。
- 将 `isPrefixOf()` 当作“任意小版本兼容”的通用判断。
- 直接把 `QDataStream` 输出作为跨语言稳定版本字符串。
- 在老 Qt 支持目标上使用 Qt 6.8 的 `QSpan` 构造或迭代器 API。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QVersionNumber()` | 构造 null version | 零个段，不等于显式的 `0` 或 `0.0`。 |
| `QVersionNumber(maj)` | 构造一段版本 | 如 `QVersionNumber(6)`；段为整数。 |
| `QVersionNumber(maj, min)` | 构造两段版本 | 如 `6.8`；不同于 `6.8.0`。 |
| `QVersionNumber(maj, min, mic)` | 构造三段版本 | 如 `6.8.2`。 |
| `QVersionNumber({segments...})` | 从初始化列表构造 | 可表达任意段数。 |
| `QVersionNumber(const QList<int> &)` | 从段列表复制构造 | 保留列表中的实际段数。 |
| `QVersionNumber(QList<int> &&)` | 从段列表移动构造 | 可避免部分复制；移动后不依赖源列表内容。 |
| `QVersionNumber(QSpan<const int>)` | 从连续只读段范围构造 | Qt 6.8 起；范围只在构造时读取，不会被对象借用。 |
| `isNull()` | 判断是否零个段 | 不等于所有段为零。 |
| `segmentCount()` | 返回实际保存段数 | 用于区分缺失段和显式零。 |
| `segmentAt(index)` | 读取指定段 | 不存在的 index 返回 0，不能单独用于存在性判断。 |
| `majorVersion()` | 读取第 0 段 | null 时返回 0。 |
| `minorVersion()` | 读取第 1 段 | 缺失时返回 0。 |
| `microVersion()` | 读取第 2 段 | 缺失时返回 0。 |
| `segments()` | 取得完整段列表 | 返回 `QList<int>` 值，修改它不会修改原版本。 |
| `isNormalized()` | 判断是否无尾随零 | null 也视为已规范化。 |
| `normalized()` | 删除尾随零后返回新版本 | 用于“忽略尾随零”的业务等价比较。 |
| `isPrefixOf(other)` | 判断是否为 `other` 的精确段前缀 | `5.3` 是 `5.3.1` 前缀，`5.3.0` 不是。 |
| `compare(v1, v2)` | 三态比较两个原始版本 | 逐段且保留段数；`1.2 < 1.2.0`。 |
| `commonPrefix(v1, v2)` | 取得最长共同段前缀 | 用于层次版本共同父节点，不表示兼容性。 |
| `fromString(text, suffixIndex)` | 解析 `.` 分隔非负数字段 | Qt 6.4 起；suffix 起点写入非空指针，suffix 规则由调用方处理。 |
| `toString()` | 以 `.` 输出所有实际段 | 不自动规范化；`1.2.0` 仍输出 `1.2.0`。 |
| `begin()` / `end()` | 只读正向迭代 | Qt 6.8 起；支持范围 for，不能原位修改段。 |
| `cbegin()` / `cend()` / `constBegin()` / `constEnd()` | 只读正向迭代别名 | Qt 6.8 起。 |
| `rbegin()` / `rend()` / `crbegin()` / `crend()` | 只读反向迭代 | Qt 6.8 起。 |
| `const_iterator`, `const_reverse_iterator` | 段的只读随机访问迭代器 | Qt 6.8 起；没有 mutable iterator。 |
| `value_type`, `reference`, `const_reference`, `pointer`, `const_pointer`, `size_type`, `difference_type` | STL 兼容类型别名 | Qt 6.8 起；引用/指针别名不提供可修改段的通道。 |
| `operator==`, `!=`, `<`, `<=`, `>`, `>=` | 严格比较版本 | 段数属于比较语义；要忽略尾随零先 `normalized()`。 |
| `operator<=>` | 三路强比较 | 取决于编译器/C++ 标准库可用性；语义同严格比较。 |
| `qHash(version, seed)` | 计算哈希 | 用于 `QHash` / `QSet`；严格不同的段数产生不同键语义。 |
| `QDataStream << >>` | 读写 Qt 数据流 | 与 `QDataStream::version()` 无关；跨端需约定流协议。 |
| `QDebug <<` | 调试输出 | 面向日志诊断，不是稳定机器协议。 |

---

### 一句话总结

`QVersionNumber` 用整数段而非字符串管理版本；记住段数会影响严格比较、缺失段读取为 0、尾随零等价必须显式 `normalized()`，而 suffix 兼容规则始终属于你的业务层。
