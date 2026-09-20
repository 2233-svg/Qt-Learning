# QHttpHeaders：保留语义与重复字段的 HTTP header 容器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHttpHeaders>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：隐式共享的值类型，Qt 6.8 起可用于 `QNetworkRequest`

## 它解决什么问题

`QHttpHeaders` 是一个结构化 HTTP header 容器。它保留字段条目、重复字段和顺序，提供名称校验、大小写无关查询，以及整数/HTTP 日期等常见值的解析接口。

它解决了 `QNetworkRequest::setRawHeader()` 只适合逐个覆写 header 的局限：很多 HTTP 场景需要保留多个同名字段，尤其 `Set-Cookie` 绝不能用逗号强行合并。`QHttpHeaders` 可作为请求或回复 headers 的完整值对象，在 Qt 6.8 起通过 `QNetworkRequest::setHeaders()` 一次设置。

## 实际使用场景

- 网关、代理或测试工具读取并转发多个同名 header，同时保留条目顺序。
- 处理响应中的多个 `Set-Cookie`，逐条读取而不是拼成一个字符串。
- 写需要严格校验 header 名和值的客户端，避免把控制字符或非法字段名送入请求。
- 将 `Content-Length`、`Retry-After` 等解析成整数，将 `Date`、`Expires` 等解析成 `QDateTime`。

它不解析每个 header 的业务语法。例如 `Cache-Control`、`Content-Type` 参数、Cookie 属性和授权方案仍需按各自规范或应用需求解析。

## 基本用法

```cpp
QHttpHeaders headers;
headers.append(QHttpHeaders::WellKnownHeader::Accept, u"application/json"_qs);
headers.append(QHttpHeaders::WellKnownHeader::SetCookie, u"theme=dark; Path=/"_qs);
headers.append(QHttpHeaders::WellKnownHeader::SetCookie, u"sid=abc; HttpOnly"_qs);

QNetworkRequest request(url);
request.setHeaders(headers);
```

`WellKnownHeader` 覆盖 IANA 注册的常用和历史字段名。对已知字段优先使用枚举重载：它避免重复创建/规范化名称，通常也更省内存和计算。自定义或尚未列入枚举的字段使用 `QAnyStringView` 重载。

## 字符校验、大小写与返回视图

设置 header 时，`QHttpHeaders` 会验证字段名和值：

- 名称必须非空，且仅含可见 ASCII 字符。
- 值可以是任意字节，但调用方仍须遵守该字段和具体用途规定的编码。
- 值首尾空白会自动移除。
- 名称大小写不敏感，`nameAt()` 和导出容器中的名称会以小写形式出现。

`value()`、`valueAt()` 和 `wellKnownHeaderName()` 返回 `QByteArrayView`，是非拥有视图。只在 `QHttpHeaders` 未被销毁且未发生可能改变内部存储的操作期间使用；若要跨作用域、跨线程或跨后续修改保存，复制为 `QByteArray`。

## 重复 header：何时合并，何时绝不能合并

`append()` 会保留新条目，适合可重复字段；`replaceOrAppend()` 则确保某字段最终只保留一条。

多数 HTTP 字段可以用逗号合并多个值，但 Qt 不会自动这样做，因为这会破坏一部分字段语义。最典型的是 `Set-Cookie`：应使用 `values(WellKnownHeader::SetCookie)` 逐项读取，不能依赖 `combinedValue()`。

```cpp
for (const QByteArray &cookie : headers.values(QHttpHeaders::WellKnownHeader::SetCookie))
    storeSetCookie(cookie);
```

`value(name)` 只返回第一项；需要所有值用 `values(name)`。`combinedValue(name)` 返回合并后的副本，调用前必须确认该字段允许逗号合并。若协议要求字段顺序，使用 `size()`、`nameAt()`、`valueAt()` 按索引遍历，或使用 `toListOfPairs()`；映射/散列表转换并不适合作为保序表示。

## 数值与日期 helper

Qt 6.10 起，`intValue()` / `intValues()` / `intValueAt()` 将值解析为 `qint64`，解析失败或字段不存在时返回 `std::nullopt`。`dateTimeValue()` 系列同样返回 `std::optional<QDateTime>`。

`setDateTimeValue()` 按标准 HTTP IMF-fixdate 写入日期，并在字段不存在时追加。解析 helper 减少样板代码，但不等于该字段在业务上有效，例如负数 `Content-Length` 或过去的 `Expires` 仍须由上层作语义判断。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `WellKnownHeader` | IANA 登记的常见/历史 HTTP 字段名；已知字段优先用此枚举重载。 |
| 构造与赋值 | `QHttpHeaders()`、复制/移动构造、`operator=`、`swap()` | 值类型操作；移动后对象只应销毁或重新赋值。 |
| 添加 | `append(name, value)` / `append(WellKnownHeader, value)` | 在末尾保留一个新条目；名称或值不合法时返回 `false`。 |
| 插入 | `insert(index, name, value)` / 枚举重载 | 在指定有效索引插入；失败返回 `false`。适用于需要控制 header 顺序的协议。 |
| 按项替换 | `replace(index, name, value)` / 枚举重载 | 替换一个已有索引的条目；索引必须有效，校验失败返回 `false`。 |
| 唯一设置 | `replaceOrAppend(name, value)` / 枚举重载 | 已有同名条目时保留一个并删除额外项，否则追加；不适合 `Set-Cookie` 等应重复保留的字段。 |
| 查询存在 | `contains(name)` / 枚举重载 | 大小写无关地判断是否存在同名字段。 |
| 首值读取 | `value(name, defaultValue)` / 枚举重载 | 返回第一条值的 `QByteArrayView`，不存在时返回默认 view；不要在修改容器后保留该 view。 |
| 所有值 | `values(name)` / 枚举重载 | 返回所有同名值的 `QList<QByteArray>`；处理 `Set-Cookie` 应使用它。 |
| 合并值 | `combinedValue(name)` / 枚举重载 | 逗号合并并返回副本；只用于明确允许合并的字段。 |
| 按索引读取 | `nameAt(index)` / `valueAt(index)` | 返回指定条目的小写名称与非拥有值 view；索引必须有效。 |
| 整数解析 | `intValue(name)`、`intValues(name)`、`intValueAt(index)` 及枚举重载 | Qt 6.10 起；解析失败或不存在返回 `std::nullopt`。 |
| 日期解析 | `dateTimeValue(name)`、`dateTimeValues(name)`、`dateTimeValueAt(index)` 及枚举重载 | Qt 6.10 起；解析 HTTP 日期，失败或不存在返回 `std::nullopt`。 |
| 日期设置 | `setDateTimeValue(name, QDateTime)` 及枚举重载 | Qt 6.10 起；以 IMF-fixdate 写入，字段不存在时追加。 |
| 删除 | `removeAll(name)` / 枚举重载 | 删除该名称的全部条目。 |
| 删除 | `removeAt(index)` | 删除一个索引位置的条目；索引必须有效。 |
| 容量 | `size()` / `isEmpty()` / `reserve(size)` / `clear()` | 查询、预留、清空条目；`reserve()` 只优化构建大量 headers 的分配。 |
| 静态名称 | `wellKnownHeaderName(WellKnownHeader)` | 返回枚举对应的非拥有名称 view。 |
| 导入 | `fromListOfPairs()` | 从有序的 `(name, value)` 列表构造；适合保留可观察的条目序列。 |
| 导入 | `fromMultiMap()` / `fromMultiHash()` | 从多值映射构造；用于映射数据转换，不能把它当作顺序语义的保存方式。 |
| 导出 | `toListOfPairs()` | 导出有序名称-值条目，名称为小写。 |
| 导出 | `toMultiMap()` / `toMultiHash()` | 导出多值映射，名称为小写。 |
| 调试 | `operator<<(QDebug, const QHttpHeaders &)` | 在启用 Qt debug stream 时输出 headers，避免在生产日志中泄露认证或 cookie。 |
| 请求协作 | `QNetworkRequest::setHeaders()` / `headers()` | Qt 6.8 起，以完整 `QHttpHeaders` 读写请求 headers。 |

## 一句话总结

`QHttpHeaders` 是能保留重复字段和顺序的 HTTP header 值对象：优先用 `WellKnownHeader`，把 `value()` 与 `values()` 区分开，并且永远不要将 `Set-Cookie` 当作可自动逗号合并的字段。
