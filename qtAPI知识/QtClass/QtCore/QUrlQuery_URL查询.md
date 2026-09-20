# Qt QUrlQuery：有序、可重复且保持 URL 编码边界的查询参数

`QUrlQuery` 管理 URL 中 `?` 之后、`#` 之前的 query 字符串。它把 `key=value&key2=value2` 拆成一组**有顺序、允许重复**的键值项，并能在保留 URL 百分号编码规则的前提下重新组成 query。

它适合构造 HTTP GET 参数、修改深链接、保留重复筛选条件、解析第三方回调 URL，或把 `QUrl` 的 query 部分交给通用代码处理。它不负责网络请求，不校验服务端参数语义，也不是 `QMap<QString, QString>`：键可以重复，顺序是状态的一部分。

```cpp
#include <QUrl>
#include <QUrlQuery>

using namespace Qt::StringLiterals;

QUrl url(u"https://example.com/search"_s);
QUrlQuery query;
query.addQueryItem(u"page"_s, u"2"_s);
query.addQueryItem(u"tag"_s, u"qt"_s);
query.addQueryItem(u"tag"_s, u"widgets"_s);
url.setQuery(query);
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUrlQuery>`  
> CMake：`Qt6::Core`  
> 线程：所有成员函数可重入；同一个实例是可变对象，多个线程并发修改时仍需调用方同步。

上例假定源文件已使用 `Qt::StringLiterals`；下文重点在 query 的结构和编码语义。

## 它解决什么问题

手工拼接 query 常在第一批需求之外失控：

- 值里出现空格、`&`、`=`、`#` 或 `%` 时，数据会不会被误解为分隔符；
- `tag=qt&tag=widgets` 是两个条件，不能塞进普通 map；
- 参数顺序可能影响签名、缓存键或服务器解释；
- 查不到键与查到空值都可能返回空字符串；
- 某些协议使用 `,` 和 `;`，而不是 `=` 和 `&`；
- HTML 表单里的 `+` 规则与通用 URL 规则并不相同。

`QUrlQuery` 专门保留这些差异。`QUrl` 负责 URL 的 scheme、host、path、fragment 和整体输出，`QUrlQuery` 只负责 query 内部项；组装完成后通过 `QUrl::setQuery(const QUrlQuery &)` 放回 URL。

## 先建立正确的心智模型：它不是 map

内部模型更接近 `QList<std::pair<QString, QString>>`：

```text
tag=qt&tag=widgets&sort=name

[
  ("tag", "qt"),
  ("tag", "widgets"),
  ("sort", "name")
]
```

因此有四条关键规则：

1. `addQueryItem()` 总是追加，不会覆盖同名 key。
2. `queryItems()` 保留输入/追加顺序。
3. `queryItemValue(key)` 只返回第一个匹配值。
4. `allQueryItemValues(key)` 返回所有匹配值；`removeQueryItem(key)` 只删第一个，`removeAllQueryItems(key)` 才删全部。

```cpp
QUrlQuery query;
query.addQueryItem(u"tag"_s, u"qt"_s);
query.addQueryItem(u"tag"_s, u"qml"_s);

Q_ASSERT(query.queryItemValue(u"tag"_s) == u"qt"_s);
Q_ASSERT(query.allQueryItemValues(u"tag"_s).size() == 2);

query.removeQueryItem(u"tag"_s);       // Leaves the "qml" item.
query.removeAllQueryItems(u"tag"_s);   // Removes every remaining "tag".
```

`operator==` 也按这个模型比较：两个对象必须包含相同内容、相同顺序，并且使用相同的 query 分隔符。若协议需要规范化或排序，必须在业务层明确排序；不要期待 `QUrlQuery` 自动排序。

## 最重要的边界：输入参数是百分号编码形式

这是 `QUrlQuery` 最反直觉、也最容易造成数据损坏的一点。

除 getter 的输出格式选项外，`setQuery()`、`addQueryItem()`、`setQueryItems()` 以及按 key 查找/删除的 API，接收的都是**URL 的百分号编码表示**。它们没有 `DecodedMode` 参数。传入未正确编码的文本时，Qt 会像 `QUrl::TolerantMode` 一样尽力恢复，而不是报告错误；恢复可能造成信息丢失。

从普通用户文本创建项时，先编码：

```cpp
static QString encodedQueryPart(const QString &plain)
{
    return QString::fromLatin1(QUrl::toPercentEncoding(plain));
}

QUrlQuery query;
query.addQueryItem(encodedQueryPart(u"title"_s),
                   encodedQueryPart(userEnteredTitle));
query.addQueryItem(encodedQueryPart(u"filter"_s),
                   encodedQueryPart(u"state:in progress"_s));
```

编码后的值是 ASCII 百分号序列，存入 `QString` 时用 `QString::fromLatin1()` 不会改变字节。不要把完整 query 先 `fromPercentEncoding()` 再传给 `setQuery()`；这样其中编码的 `&`、`=`、`#` 可能变成结构分隔符。

按 key 查询时同样传入编码形式。下面这种流程可能查不到数据：

```cpp
const auto items = query.queryItems(QUrl::FullyDecoded);
const QString displayKey = items.first().first;

query.queryItemValue(displayKey); // Not reliable: lookup expects encoded key.
```

`FullyDecoded` 仅适合将结果交给人类可见的非 URL 文本环境；它可能丢失无法以 Unicode 表示的数据，也没有与之对应的 decoded setter。需要再次查找时，保留原始编码 key，或重新使用 `QUrl::toPercentEncoding()` 编码。

## 输出编码、空格和 `+`

所有 getter 都可带 `QUrl::ComponentFormattingOptions`：

| 输出选项 | 适合什么 | 边界 |
| --- | --- | --- |
| `QUrl::PrettyDecoded` | 默认日志/一般检查 | 仍必须当作 URL 编码字符串，某些字符为了无歧义会继续编码。 |
| `QUrl::FullyEncoded` | 放回 URL、传输、签名输入前的明确序列化 | 以 URL 编码形式输出；保留项顺序。 |
| `QUrl::FullyDecoded` | 向用户展示单个 key/value | 可能丢失不可表达字节；不能将结果直接回传给查找或 setter。 |

`QUrlQuery` 遵循 URL，而不是 HTML 表单的 `application/x-www-form-urlencoded` 约定：

- 空格输出为 `%20`，不会输出为 `+`；
- `+` 不会被解码为空格；
- `%2B` 不会自动解码为 `+`；
- 输入中的 `+` 和 `%2B` 会被原样保留（百分号十六进制可能规范为大写）。

如果对接服务端明确要求表单编码，应在协议适配层自行实现“空格转 `+`、加号转 `%2B`”的规则，且在边界处完成一次。不要假定 `QUrlQuery` 会替浏览器表单做这种转换。

## 常用工作流

### 从 URL 中读取、修改后写回

```cpp
QUrl url(u"https://example.com/search?tag=qt&tag=qml&page=1"_s);
QUrlQuery query(url);

query.removeAllQueryItems(u"page"_s);
query.addQueryItem(u"page"_s, u"2"_s);
url.setQuery(query);
```

`QUrlQuery(const QUrl &)` 使用默认 `=` 和 `&` 解析 URL 的 query。它复制的是 query 内容，不会持有或修改原 `QUrl`，因此写回 `url.setQuery(query)` 是必要步骤。

### 构建有重复键的筛选条件

```cpp
QUrlQuery query {
    { u"tag"_s, u"qt"_s },
    { u"tag"_s, u"qml"_s },
    { u"sort"_s, u"updated"_s }
};

url.setQuery(query);
```

initializer-list 构造按列表顺序调用 `addQueryItem()`。它方便构造已处于 URL 编码形式的常量 ASCII 参数；含用户数据、空格、非 ASCII、`&`、`=` 或 `%` 的值仍应先编码。

### 区分缺失项和空值

`queryItemValue()` 在 key 不存在时返回空 `QString`，而 `flag=` 这样的空 value 也会得到空 `QString`。必须先用 `hasQueryItem()` 区分：

```cpp
if (!query.hasQueryItem(u"cursor"_s)) {
    // No cursor key.
} else {
    const QString cursor = query.queryItemValue(u"cursor"_s);
    // An empty cursor value is now distinguishable from a missing key.
}
```

这不是服务器参数验证。即使 key 存在，也应由业务代码检查枚举、范围、重复项是否允许，以及是否出现不能接受的未知参数。

## 非标准分隔符

默认值是 `=` 分隔 key/value、`&` 分隔项；对应的 constexpr 静态函数返回 `char16_t`：

```cpp
static_assert(QUrlQuery::defaultQueryValueDelimiter() == u'=');
static_assert(QUrlQuery::defaultQueryPairDelimiter() == u'&');
```

若协议使用其他规则，先设置分隔符，再解析或构建 query：

```cpp
QUrlQuery query;
query.setQueryDelimiters(u',', u';');
query.setQuery(u"type,pie;color,green"_s);
```

同一对象之后的 `setQuery()` 和 `query()` 都采用新分隔符；在 encoded key/value 中出现这些分隔符时，输出会把它们百分号编码。非标准分隔符应从 RFC 3986 的 sub-delims 选择：`! $ & ' ( ) * + , ; =`。Qt 不验证传入字符；使用其它字符是未支持行为，可能造成意外解析。

要从已有 `QUrl` 解析这种非标准 query，不能直接使用 `QUrlQuery(url)`，因为该构造函数已按默认分隔符解析。应先创建对象、设置分隔符，再把 `url.query()` 传给 `setQuery()`。

## 生命周期、值语义与线程

`QUrlQuery` 是没有 QObject 所有权关系的隐式共享值类型。复制对象不会共享“可见的可变状态”：任一副本被修改时会按需分离；复制赋值也会复制 query 分隔符。可以安全地按值返回和存进容器。

它不依赖事件循环，不访问网络，也没有平台专属行为。类的函数可重入，但这不等于一个实例可无锁并发读写：共享同一 `QUrlQuery` 对象时由调用方加锁或传值到工作线程。

`isDetached()` 是隐式共享实现的低层查询，用于诊断共享状态；日常业务不应据此建立逻辑。移动构造自 Qt 6.5 起可用，`swap()` 是快速且不抛异常的交换。

## 与 `QUrl` 的协作边界

`QUrlQuery::query()` 返回的是**没有前导 `?`** 的 query 字符串。正确的整合方式通常是：

```cpp
QUrl url(u"https://example.com/items"_s);
QUrlQuery query;
query.addQueryItem(u"limit"_s, u"50"_s);
url.setQuery(query);
```

避免以下混用：

- 不要把 `QUrl::toString()` 的完整 URL 传给 `QUrlQuery::setQuery()`；
- 不要在 query 字符串中附带前导 `?` 或 fragment；
- 不要把 `QUrlQuery::toString()` 当作完整可访问地址；
- 不要同时手工拼接 `?`/`&` 和使用 `QUrl::setQuery()`。

query 本身不能证明 URL 安全。日志中的 query 可能含 access token、session id 或 PII；URL 签名、缓存键和权限决策也必须明确采用哪一种编码、是否保留顺序、是否允许重复 key。

## 常见错误与排查顺序

- 把 `QUrlQuery` 当 `QMap`，无意中丢掉重复 key 或打乱顺序。
- 使用 `queryItemValue()` 后把空字符串直接当作“参数不存在”，却遗漏了空值。
- 调用 `removeQueryItem()` 后以为所有同名项都被删掉。
- 直接把用户输入传给 `addQueryItem()`，没有先百分号编码。
- 通过 `FullyDecoded` 取出 key 再去查询，因查找 API 期望编码 key 而失败。
- 把 `+` 当空格，或者指望 `QUrlQuery` 自动做 HTML form encoding。
- 先用默认构造函数解析非标准分隔符，再去设置分隔符；分隔符必须在 `setQuery()` 之前设置。
- 对不支持的分隔符寄予期望。Qt 不会验证参数是否合法。
- 忽略 query 中的敏感 token，直接用 `toString()` 写日志。
- 以 query 是否存在判断用户权限或请求是否可信，忽略服务端验证和签名规则。

## 逐项 API 说明

### 构造、复制和状态

#### `QUrlQuery()`、`QUrlQuery(const QString &)`、`QUrlQuery(const QUrl &)`

默认构造为空 query。字符串构造按默认分隔符解析已编码 query；URL 构造仅提取其 query。若需要非标准分隔符，先默认构造、调用 `setQueryDelimiters()`，再调用 `setQuery()`。

#### `QUrlQuery(initializer_list)`、复制/移动与赋值

initializer-list 逐项追加，故保留重复和顺序。复制/赋值会带上内容与分隔符；移动构造自 Qt 6.5 起。它们都是值操作，不会自动回写某个 `QUrl`。

#### `isEmpty()`、`clear()`、`isDetached()`

`isEmpty()` 仅表示没有项。`clear()` 移除所有项，但保留已经设定的非标准分隔符。`isDetached()` 只反映隐式共享实现，通常不作为业务判断。

### 项操作和查找

`addQueryItem()` 追加而不覆盖；`queryItemValue()` 返回第一个；`allQueryItemValues()` 返回全部；所有按 key API 的 key 都应是百分号编码形式。处理重复或空值时，应显式使用 `hasQueryItem()` 和 `allQueryItemValues()`，而不要依据一个空 `QString` 推断全部语义。

### 字符串化和分隔符

`query()` 重建 query 并保持项目顺序；`toString()` 是其同义 API。`setQuery()` 使用当前分隔符重新解析。默认 `=`/`&` 由静态 constexpr API 提供；定制分隔符时选择支持的 sub-delims，并在解析前设定。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QUrlQuery()` | 创建空 query | 没有项，不含 `?`；可后续追加或 `setQuery()`。 |
| `QUrlQuery(const QString &queryString)` | 按默认分隔符解析 query 文本 | 输入应为百分号编码 query；不含完整 URL 或前导 `?`。 |
| `QUrlQuery(const QUrl &url)` | 提取并解析 URL 的 query | 只读取 query，使用默认 `=` / `&` 分隔符。 |
| `QUrlQuery(initializer_list<pair<QString, QString>>)` | 从有序项列表构造 | 保留顺序和重复项；各项仍应是编码表示。 |
| `QUrlQuery(const QUrlQuery &)` | 复制 query | 内容和分隔符一起复制。 |
| `QUrlQuery(QUrlQuery &&)` | 移动 query | Qt 6.5 起；移动后源对象只保持有效的未指定状态。 |
| `operator=(const QUrlQuery &)` | 复制赋值 | 复制项和分隔符。 |
| `operator=(QUrlQuery &&)` | 移动赋值 | 不抛异常；不涉及任何 `QUrl` 回写。 |
| `isEmpty()` | 判断是否没有 query 项 | 空 query 字符串解析后也为 true。 |
| `clear()` | 删除全部项 | 保留自定义分隔符。 |
| `isDetached()` | 查询隐式共享数据是否已分离 | 低层诊断/性能接口，不宜作业务状态。 |
| `addQueryItem(key, value)` | 追加一项 | 不覆盖同名 key；key/value 应先百分号编码。 |
| `setQueryItems(items)` | 用有序项列表整体替换 | 保留传入顺序与重复项；输入为编码形式。 |
| `queryItems(encoding)` | 返回全部有序键值对 | 不是 map；输出默认 `PrettyDecoded`。 |
| `hasQueryItem(key)` | 判断 key 是否存在 | key 必须是编码形式；可与 `queryItemValue()` 区分空值/缺失。 |
| `queryItemValue(key, encoding)` | 返回第一个匹配 value | key 不存在返回空字符串；重复 key 只返回第一个。 |
| `allQueryItemValues(key, encoding)` | 返回全部匹配 value | key 不存在返回空列表；保持原始顺序。 |
| `removeQueryItem(key)` | 删除第一个匹配项 | 重复 key 只移除一项。 |
| `removeAllQueryItems(key)` | 删除所有匹配项 | key 应使用编码形式。 |
| `setQuery(queryString)` | 按当前分隔符重新解析 query | 输入是编码 query；宽松恢复错误编码可能导致数据丢失。 |
| `query(encoding)` | 重建 query 字符串 | 不含 `?`；顺序保持；`#` 会为避免 fragment 歧义而编码。 |
| `toString(encoding)` | 返回 query 字符串 | `query()` 的同义 API。 |
| `QUrl::PrettyDecoded` | 默认 getter 输出格式 | 仍可含百分号编码，不能当完全解码文本。 |
| `QUrl::FullyEncoded` | 完整编码 getter 输出 | 适合放回 URL 或稳定传输表示。 |
| `QUrl::FullyDecoded` | 完全解码 getter 输出 | 仅展示用；可能丢失数据，不能直接拿来查找/设置。 |
| `setQueryDelimiters(valueDelimiter, pairDelimiter)` | 设置 key/value 和项间分隔符 | 先设再 `setQuery()`；仅支持 sub-delims，Qt 不验证传入字符。 |
| `queryValueDelimiter()` | 获取当前 key/value 分隔符 | 默认 `=`。 |
| `queryPairDelimiter()` | 获取当前项间分隔符 | 默认 `&`。 |
| `defaultQueryValueDelimiter()` | 获取默认 `=` | `constexpr char16_t`；Qt 6 前返回类型为 `QChar`。 |
| `defaultQueryPairDelimiter()` | 获取默认 `&` | `constexpr char16_t`；Qt 6 前返回类型为 `QChar`。 |
| `swap(QUrlQuery &)` | 快速交换两个对象 | 不抛异常；项和分隔符一并交换。 |
| `qHash(const QUrlQuery &, seed)` | 计算哈希 | 用于 `QHash` / `QSet`；等价状态的定义包含顺序和分隔符。 |
| `operator==` / `operator!=` | 比较两个 query | 内容、顺序、分隔符都必须一致才相等。 |
| `QUrl::setQuery(const QUrlQuery &)` | 将结构化 query 放入 URL | 推荐的组合入口；由 `QUrl` 负责加入 `?`。 |
| `QUrl::toPercentEncoding()` | 编码普通文本以供 query API 输入 | `QUrlQuery` 不提供 decoded setter 时的显式边界转换。 |

---

### 一句话总结

`QUrlQuery` 是有序且允许重复的 URL 查询项容器：所有写入和按 key 操作都应使用百分号编码形式，空格不是 `+`，重复键要用全部值 API 处理，完成后再交给 `QUrl::setQuery()`。
