# Qt QJsonDocument 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJsonDocument>`  
> 所属模块：`Qt6::Core`  
> 定位：表示一个以 JSON object 或 JSON array 为根节点的完整 JSON 文档

## 1. QJsonDocument 解决什么问题

`QJsonDocument` 是 JSON 文本与 Qt JSON 值树之间的顶层容器：

```text
UTF-8 JSON bytes
       |
       | fromJson()
       v
QJsonDocument
   ├─ QJsonObject  根是 object
   └─ QJsonArray   根是 array
       |
       | toJson()
       v
UTF-8 JSON bytes
```

它适合配置文件、HTTP JSON 响应、导入导出和调试数据。根节点只能是 object 或 array；JSON 标量，例如 `"text"`、`42`、`true` 和 `null`，不能单独构成一个 `QJsonDocument` 根。

它不负责：

- 验证业务字段是否存在、类型正确或数值在范围内。
- 对不可信大输入自动设置资源上限。
- 维持 JSON 字段顺序作为业务语义。
- 提供流式解析。超大 JSON 需要评估内存占用或使用更适合的流式方案。

## 2. 解析外部 JSON：错误对象必须检查

```cpp
QJsonParseError error;
const QJsonDocument document =
    QJsonDocument::fromJson(replyBytes, &error);

if (error.error != QJsonParseError::NoError) {
    qWarning() << "JSON parse error at" << error.offset
               << error.errorString();
    return;
}

if (!document.isObject())
    return;

const QJsonObject root = document.object();
```

解析成功只说明字节符合 JSON 语法。业务层还应继续验证：

```cpp
const QJsonValue idValue = root.value("id");
if (!idValue.isDouble())
    return;

const double id = idValue.toDouble();
if (id < 0 || id > 9e15)
    return;
```

JSON 的 number 在 Qt 中以 `double` 表示。不能精确表示的 64 位整数 ID 不应裸写为 JSON number；使用字符串，或定义明确的编码规则。

## 3. 构建 JSON：object、array 和 document 的关系

```cpp
QJsonObject user;
user.insert("name", "Ada");
user.insert("active", true);
user.insert("roles", QJsonArray{"admin", "writer"});

QJsonDocument document(user);
const QByteArray body = document.toJson(QJsonDocument::Compact);
```

也可以后设根节点：

```cpp
QJsonDocument document;
document.setObject(user);
```

根节点在 object 和 array 之间切换时，旧根内容会被替换。`QJsonObject`、`QJsonArray`、`QJsonValue` 和 `QJsonDocument` 是值类型，复制成本通常较低，但修改共享数据会触发必要的分离。

## 4. 修改时不要丢掉值类型的更新结果

下面的写法只是修改 `object()` 返回的副本，document 本身不会变：

```cpp
QJsonDocument document(QJsonObject{{"enabled", false}});
document.object().insert("enabled", true); // 错误：修改丢失
```

正确做法：

```cpp
QJsonObject object = document.object();
object.insert("enabled", true);
document.setObject(object);
```

嵌套 object/array 也遵循同一规则。拿到子对象后修改，最后沿路径写回父对象：

```cpp
QJsonObject root = document.object();
QJsonObject options = root.value("options").toObject();
options.insert("timeoutMs", 3'000);
root.insert("options", options);
document.setObject(root);
```

## 5. `toVariant()` 和 `fromVariant()`：边界转换工具

```cpp
QVariantMap map;
map.insert("enabled", true);
map.insert("limit", 10);

QJsonDocument document = QJsonDocument::fromVariant(map);
const QVariant value = document.toVariant();
```

它适合把简单 Qt 数据结构接入 JSON API，但不应把它理解成任意 C++ 类型的无损序列化。只使用 JSON 能表示的 null、bool、number、string、list 和 map 结构；日期、二进制、枚举、大整数和自定义对象要定义明确的转换策略。

## 6. 输出格式与持久化

```cpp
QFile file("settings.json");
if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate))
    return false;

const QByteArray json = document.toJson(QJsonDocument::Indented);
return file.write(json) == json.size();
```

- `Indented` 用于配置、诊断和人工审核。
- `Compact` 用于网络请求和体积敏感的传输。

写重要配置时，不要直接截断后覆盖，使用 `QSaveFile`：

```cpp
QSaveFile file("settings.json");
if (!file.open(QIODevice::WriteOnly))
    return false;
if (file.write(document.toJson(QJsonDocument::Indented)) < 0)
    return false;
return file.commit();
```

## 7. 常见误区

### 把 parse success 当 schema success

`fromJson()` 只验证 JSON 语法。字段、类型、枚举值、数组长度和业务约束必须自己校验。

### 直接把 qint64 写成 JSON number

JSON number 会经过 double。对超过精确范围的整数 ID 使用字符串。

### 修改 `document.object()` 的临时值

`object()` 返回值类型副本。修改后必须 `setObject()` 写回。

### 相信键顺序

JSON object 是键值映射。不要把 object 成员顺序当协议语义或签名依据。

### 把巨型 JSON 一次读入内存

QJsonDocument 是整棵树。对大体积或攻击面输入限制文件/响应大小，并设计流式或分页协议。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QJsonDocument()` | 创建空 JSON 文档。 | `isNull()` 为 true，既不是 object 也不是 array。 |
| 构造 | `QJsonDocument(const QJsonObject &)` | 用 object 创建完整 JSON 文档。 | 根节点固定为 object；后续修改 object 要写回 document。 |
| 构造 | `QJsonDocument(const QJsonArray &)` | 用 array 创建完整 JSON 文档。 | 根节点固定为 array；不适合表示 JSON 标量根。 |
| 析构 | `~QJsonDocument()` | 销毁 JSON 文档值。 | 值类型复制和销毁通常廉价，但大型树仍有内存成本。 |
| 复制移动 | 拷贝构造、赋值、移动构造、移动赋值、`swap()` | 复制、移动或交换文档数据。 | 修改副本可能触发分离；交换适合高效替换状态。 |
| 解析 | `fromJson(const QByteArray &, QJsonParseError *)` | 从 UTF-8 JSON 字节解析文档。 | 必须检查 parse error；语法成功不等于业务数据有效。 |
| 输出 | `toJson(JsonFormat)` | 将文档编码为 UTF-8 JSON。 | `Indented` 便于阅读，`Compact` 节省体积；输出失败要由写设备另行检查。 |
| 格式 | `Indented` | 生成带缩进和换行的 JSON。 | 适合配置和日志，不适合极端体积敏感传输。 |
| 格式 | `Compact` | 生成紧凑 JSON。 | 适合 HTTP 请求；不改变 JSON 语义。 |
| 根类型 | `isEmpty()` | 判断根 object 或 array 是否为空。 | 空文档和空 object/array 的含义不同，必要时同时检查 isNull。 |
| 根类型 | `isNull()` | 判断文档是否为空文档。 | 解析失败或默认构造可得到空文档；不要和空 object 混淆。 |
| 根类型 | `isObject()` | 判断根节点是否是 object。 | 调用 object 前先检查，避免把类型错误吞成空 object。 |
| 根类型 | `isArray()` | 判断根节点是否是 array。 | 调用 array 前先检查，避免把类型错误吞成空 array。 |
| 根访问 | `object()` | 返回根 object 值。 | 返回值需要修改后用 setObject 写回。 |
| 根访问 | `array()` | 返回根 array 值。 | 返回值需要修改后用 setArray 写回。 |
| 根设置 | `setObject(const QJsonObject &)` | 以 object 替换当前根。 | 会丢弃原根内容；适合明确重建文档。 |
| 根设置 | `setArray(const QJsonArray &)` | 以 array 替换当前根。 | 会丢弃原根内容；不要用于 JSON 标量。 |
| 根索引 | `operator[](QString/QStringView/QLatin1StringView)` | 从 object 根按键读取 JSON value。 | 非 object 或不存在键通常得到 undefined value；要检查类型和值。 |
| 根索引 | `operator[](qsizetype)` | 从 array 根按索引读取 JSON value。 | 越界和非 array 根返回 undefined value；不应当作异常替代。 |
| 变体转换 | `fromVariant(const QVariant &)` | 从 QVariant、QVariantMap 或 QVariantList 构建 JSON 文档。 | 只会转换 JSON 支持的结构；日期、二进制和自定义类型需显式规则。 |
| 变体转换 | `toVariant()` | 将 JSON 文档转成 QVariant 值树。 | 类型信息可能不如原始 C++ 对象丰富；用于边界转换而非持久化 schema。 |
| 常量 | `BinaryFormatTag` | Qt 内部二进制 JSON 格式标识常量。 | 不要将其当作公共持久化协议；使用标准 JSON 或明确自己的格式。 |
| 流 | `operator<<(QDataStream &, QJsonDocument)` | 把 JSON 文档写入 QDataStream。 | 依赖 QDataStream version；不等同于标准 JSON 文本格式。 |
| 流 | `operator>>(QDataStream &, QJsonDocument &)` | 从 QDataStream 读取 JSON 文档。 | 读取外部数据仍要检查 stream status 和文档根类型。 |

---

### 一句话总结

`QJsonDocument` 管理完整 object/array JSON 文档，但不会替你定义 schema。解析后校验每个业务字段，修改时将 object/array 写回 document，持久化时配合 `QSaveFile`，并把大整数、版本和资源上限作为协议的一部分设计。
