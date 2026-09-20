# Qt QMimeType MIME 类型描述笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMimeType>`  
> 所属模块：`Qt6::Core`  
> 类型性质：MIME 类型的只读值描述  
> 相关类型：`QMimeDatabase`、`QMimeData`、`QFileDialog`、`QHash`

## 1. 它解决什么问题

`QMimeType` 表示 MIME 数据库中的一个类型描述。`QMimeDatabase` 负责“查找”，`QMimeType` 负责“描述查到的结果”：

```text
QMimeDatabase::mimeTypeForFile(...)
              |
              v
          QMimeType
              |
              +-- canonical name
              +-- aliases
              +-- suffixes and glob patterns
              +-- parent/ancestor types
              +-- human-readable comment
              +-- icon names
              +-- file-dialog filter
```

它适合：

- 根据 canonical MIME 名称做程序分支；
- 根据 `comment()` 在界面显示人类可读类型；
- 根据 `preferredSuffix()` 生成默认文件名；
- 根据 `filterString()` 构造文件选择器过滤器；
- 根据 `parentMimeTypes()` 或 `inherits()` 判断类型层次；
- 根据 `iconName()` 或 `genericIconName()` 选择图标；
- 把 MIME 描述作为值对象保存在模型、缓存或哈希容器中。

## 2. 它不是什么

`QMimeType` 不是：

- 文件内容本身；
- 文件解析器；
- 文件图标对象；
- MIME 数据库的可写记录；
- 只由扩展名构造出来的临时字符串；
- 保证某个文件内容真实匹配的安全证明。

它描述的是数据库对一个 MIME 类型的认识。一个文件可以被错误扩展名伪装，数据库识别也可能只能退回默认二进制类型；真正打开文件前仍要做内容和安全验证。

## 3. 从 `QMimeDatabase` 获取

```cpp
QMimeDatabase database;
const QMimeType type =
    database.mimeTypeForFile(
        QStringLiteral("report.pdf"));

if (!type.isValid())
    return;

qDebug() << type.name()
         << type.comment()
         << type.preferredSuffix();
```

不要手工拼出一个 `QMimeType`。公开使用入口是 `QMimeDatabase` 的查询结果；带 `QMimeTypePrivate` 的构造形式属于 Qt 内部实现边界。

## 4. 三种状态要分清

### 4.1 invalid

默认构造的 `QMimeType` 没有有效描述：

```cpp
QMimeType type;
Q_ASSERT(!type.isValid());
```

查询不存在的名称或没有可用描述时，也可能得到 invalid 类型。此时不要依赖 `name()`、后缀或图标字段。

### 4.2 valid 且 default

无法识别具体格式的数据通常可以得到有效的默认 MIME 类型，例如 `application/octet-stream`：

```cpp
if (type.isValid() && type.isDefault()) {
    // 有一个通用默认类型，但没有具体格式结论。
}
```

它与 invalid 不同：数据库有一个明确的默认描述，但这不代表识别出了 PDF、PNG 或其他具体格式。

### 4.3 valid 且非 default

这是数据库匹配到具体 MIME 类型的常规结果。程序分支通常使用 `name()`，界面文本使用 `comment()`，文件名建议使用 `preferredSuffix()`。

## 5. canonical name、alias 和继承关系

### 5.1 `name()` 是程序身份

```cpp
const QString canonical = type.name();
```

`name()` 返回 canonical MIME 名称，例如：

```text
application/pdf
image/png
text/plain
```

程序逻辑、配置文件和日志优先保存 canonical name，不要把本地化 comment 或某个 alias 当作稳定类型身份。

### 5.2 `aliases()` 是替代名称

```cpp
for (const QString &alias : type.aliases())
    qDebug() << alias;
```

alias 可以用于兼容旧名称或不同数据库描述。它们不等于新的独立 MIME 类型。需要规范化用户输入时，可以通过 `QMimeDatabase::mimeTypeForName()` 查询后再保存 `name()`。

### 5.3 `parentMimeTypes()` 是直接父类型

```cpp
const QStringList directParents =
    type.parentMimeTypes();
```

它只列出数据库定义的直接父类型。父类型用于表达“该类型也属于更一般类别”的关系，不是 C++ 继承，也不会把文件转换成父类型数据。

### 5.4 `allAncestors()` 是传递闭包

```cpp
const QStringList ancestors =
    type.allAncestors();
```

它包含类型继承链上的全部祖先，适合做分类、过滤或调试。需要判断一个目标类型时，优先使用：

```cpp
if (type.inherits(QStringLiteral("text/plain"))) {
    // 按 text/plain 家族处理
}
```

不要只比较 `parentMimeTypes()`，否则会漏掉多级祖先。

## 6. 后缀、glob 和文件过滤器

### 6.1 `suffixes()`

```cpp
const QStringList suffixes = type.suffixes();
```

返回该 MIME 类型关联的所有后缀。它们不一定包含点号：

```text
pdf
```

生成文件名时应自己决定是否添加 `"."`，并处理用户输入已经带后缀的情况。

### 6.2 `preferredSuffix()`

```cpp
const QString suffix = type.preferredSuffix();
```

返回数据库认为最适合展示或生成文件名的一个后缀。它不保证是唯一正确后缀，也不保证与当前平台用户习惯完全一致。

### 6.3 `globPatterns()`

```cpp
const QStringList patterns = type.globPatterns();
```

返回文件名匹配模式，例如：

```text
*.pdf
```

glob 是名称匹配规则，不是内容识别规则。不要用 glob 命中结果替代安全解析。

### 6.4 `filterString()`

```cpp
const QString filter = type.filterString();
```

返回适合文件选择器使用的过滤器字符串，例如带有类型描述和 glob 模式的组合。它面向 UI，不适合作为程序逻辑或持久化协议。

如果应用需要自定义本地化、多个 MIME 合并或平台特定显示，应根据 `suffixes()`/`globPatterns()` 自己构造过滤器，而不是假设 `filterString()` 完全符合自己的界面规范。

## 7. comment 和图标名称

### 7.1 `comment()`

```cpp
const QString label = type.comment();
```

返回人类可读的类型描述，可能受系统语言和 MIME 数据库本地化影响。它适合列表、状态栏和文件属性界面，不适合作为稳定比较键。

### 7.2 `iconName()`

```cpp
const QString icon = type.iconName();
```

返回该类型的专用图标名称。名称是否存在、由哪个图标主题提供，取决于平台和 Qt GUI 的图标主题环境。

### 7.3 `genericIconName()`

```cpp
const QString genericIcon = type.genericIconName();
```

返回更通用的图标名称。专用图标不存在时，可以把 generic icon 作为降级选择。

Core 只提供名称字符串，不负责把名称解析成 `QIcon`。在 Qt GUI 中使用时，再交给 `QIcon::fromTheme()` 或应用自己的图标系统。

## 8. 隐式共享、复制和比较

`QMimeType` 使用共享数据语义。复制一个类型描述通常只是复制共享状态的 handle：

```cpp
QMimeType a = database.mimeTypeForName(
    QStringLiteral("image/png"));
QMimeType b = a;
```

复制不会复制文件，也不会创建新的数据库条目。类型描述是只读查询值，普通应用不需要分离或修改内部记录。

值对象可以比较和哈希：

```cpp
if (a == b)
    qDebug() << "same MIME description";

QHash<QMimeType, int> counts;
counts[a] += 1;
```

程序逻辑最好仍按 canonical `name()` 进行跨进程、跨版本或持久化比较。哈希和对象相等适合当前 Qt 进程内的值容器，不应替代稳定的字符串协议。

## 9. 逐项 API 语义

### 9.1 `QMimeType()`

```cpp
QMimeType();
```

构造 invalid MIME 类型。它不查询数据库，也不代表默认二进制类型。

### 9.2 `QMimeType(const QMimeType &other)`

```cpp
QMimeType(const QMimeType &other);
```

复制 MIME 类型描述。复制后的对象仍描述同一个逻辑 MIME 类型，不拥有独立的数据库记录。

### 9.3 `operator=(const QMimeType &other)`

```cpp
QMimeType &operator=(const QMimeType &other);
```

复制替换当前描述。当前对象原先的 MIME 类型不会被数据库删除，只是当前值改为描述另一个类型。

### 9.4 移动构造和移动赋值

```cpp
QMimeType(QMimeType &&other) noexcept;
QMimeType &operator=(QMimeType &&other) noexcept;
```

移动共享数据 handle。移动后的源对象仍可析构和重新赋值，但不要继续把它当成原来的有效 MIME 描述。

### 9.5 `~QMimeType()`

```cpp
~QMimeType() noexcept;
```

释放当前对象的共享描述引用。不会删除系统 MIME 数据或影响其他 `QMimeType` 值。

### 9.6 `swap(QMimeType &other)`

```cpp
void swap(QMimeType &other) noexcept;
```

交换两个值对象持有的描述状态。不会修改 MIME 数据库，也不会改变类型继承关系。

### 9.7 `isValid() const`

```cpp
bool isValid() const;
```

判断当前对象是否有有效 MIME 描述。它不能说明具体文件内容一定匹配该类型。

### 9.8 `isDefault() const`

```cpp
bool isDefault() const;
```

判断当前描述是否是数据库的默认 MIME 类型。默认类型可以是 valid，但只表达“未知/通用数据”的兜底分类。

### 9.9 `name() const`

```cpp
QString name() const;
```

返回 canonical MIME 名称。程序分支、日志、缓存键和持久化配置优先使用它。

### 9.10 `comment() const`

```cpp
QString comment() const;
```

返回人类可读描述。它可能本地化、变化或为空，不要用它做稳定逻辑判断。

### 9.11 `genericIconName() const`

```cpp
QString genericIconName() const;
```

返回通用图标名称。它只是名称，不是已加载的 `QIcon`，也不保证当前主题提供该图标。

### 9.12 `iconName() const`

```cpp
QString iconName() const;
```

返回更具体的图标名称。没有可用专用名称时，可以回退到 `genericIconName()`。

### 9.13 `globPatterns() const`

```cpp
QStringList globPatterns() const;
```

返回数据库用于匹配文件名的 glob 模式。模式适合过滤器，不等于文件内容验证。

### 9.14 `parentMimeTypes() const`

```cpp
QStringList parentMimeTypes() const;
```

返回直接父 MIME 类型名称。它描述 MIME 分类关系，不会执行数据转换。

### 9.15 `allAncestors() const`

```cpp
QStringList allAncestors() const;
```

返回所有祖先类型名称。需要判断多级继承关系时使用它或 `inherits()`，不要只读取直接父类型。

### 9.16 `aliases() const`

```cpp
QStringList aliases() const;
```

返回该类型的替代名称。用于兼容名称和诊断，不是额外独立类型。

### 9.17 `suffixes() const`

```cpp
QStringList suffixes() const;
```

返回关联的全部文件后缀。它们是数据库规则，不代表内容一定符合格式。

### 9.18 `preferredSuffix() const`

```cpp
QString preferredSuffix() const;
```

返回首选后缀。适合生成默认文件名，但保存文件时仍应由用户或业务规则决定最终扩展名。

### 9.19 `inherits(const QString &mimeTypeName) const`

```cpp
Q_INVOKABLE bool inherits(
    const QString &mimeTypeName) const;
```

判断当前 MIME 类型是否继承指定 MIME 类型：

```cpp
if (type.inherits(QStringLiteral("text/plain"))) {
    // 按 text/plain 类型家族处理
}
```

实际使用时应传入 MIME 数据库中的具体类型名称，例如 `text/plain`；不要把参数当成支持任意通配符的字符串模式。它判断的是 MIME 分类关系，不是 C++ 类型继承，也不是数据能否转换。

### 9.20 `filterString() const`

```cpp
QString filterString() const;
```

返回适合文件选择器显示的过滤器字符串。它面向 UI，可能包含本地化文本和 glob 模式；不要把它作为跨平台配置格式。

### 9.21 `operator==`、`operator!=`

Qt 6.11.1 仍在兼容条件下提供相等比较，并通过 `Q_DECLARE_EQUALITY_COMPARABLE` 提供现代比较支持。相等比较表示两个值描述同一个逻辑 MIME 类型；程序跨环境保存时仍应比较 canonical `name()`。

### 9.22 `qHash(const QMimeType &, size_t)`

```cpp
size_t qHash(const QMimeType &key,
             size_t seed = 0) noexcept;
```

允许把 `QMimeType` 放入 `QHash`。哈希适合当前进程内的值容器；跨版本或持久化场景应使用 `name()`。

## 10. 实际使用模式

### 10.1 按 MIME 类型选择解析器

```cpp
QMimeDatabase database;
const QMimeType type =
    database.mimeTypeForData(bytes);

const QString name = type.name();
if (name == QStringLiteral("image/png")) {
    parsePng(bytes);
} else if (type.inherits(
               QStringLiteral("text/plain"))) {
    parseText(bytes);
} else {
    handleUnknown(bytes);
}
```

如果 type 是 default 类型，`name()` 可能只提供通用二进制分类。未知数据不要强行交给具体解析器。

### 10.2 生成文件对话框过滤器

```cpp
const QMimeType pdf =
    database.mimeTypeForName(
        QStringLiteral("application/pdf"));

const QString filter = pdf.filterString();
```

如果要合并多个类型，先收集过滤器或 glob，再按 UI 设计去重；不要直接把多个已经带描述文本的 filter 字符串用任意分隔符拼接。

### 10.3 生成默认文件名

```cpp
QString makeDefaultName(const QMimeType &type)
{
    const QString suffix = type.preferredSuffix();
    return suffix.isEmpty()
        ? QStringLiteral("untitled")
        : QStringLiteral("untitled.") + suffix;
}
```

首选后缀可能为空，调用方必须处理这种情况。

## 11. 常见错误

### 11.1 用 comment 做逻辑分支

**问题：** 中文系统和英文系统走不同代码路径。

**原因：** `comment()` 面向人类，可能本地化。

**处理：** 用 `name()` 或 `inherits()`，comment 只用于显示。

### 11.2 把 valid 当成具体格式确认

**问题：** default `application/octet-stream` 被当成已识别格式。

**原因：** valid 只说明描述有效。

**处理：** 同时检查 `isDefault()`，必要时重新做内容解析。

### 11.3 只看一个后缀

**问题：** 复合后缀或多个合法后缀被遗漏。

**原因：** `preferredSuffix()` 只返回一个首选值。

**处理：** 需要完整候选时使用 `suffixes()` 和 `globPatterns()`。

### 11.4 把 glob 当内容验证

**问题：** 伪造扩展名通过导入。

**原因：** glob 只匹配文件名。

**处理：** 对实际字节和格式结构做验证。

### 11.5 把 `inherits()` 当数据转换

**问题：** 因为类型分类关系成立，就直接按目标格式解析。

**原因：** MIME 继承只表示分类关系。

**处理：** 仍要检查实际格式语法和解析器能力。

### 11.6 把 iconName 当 QIcon

**问题：** 直接把字符串当图标对象使用。

**原因：** Core 只返回图标名称。

**处理：** 在 Qt GUI 中通过 `QIcon::fromTheme()` 或自定义主题加载。

### 11.7 把 QMimeType 当可写数据库记录

**问题：** 试图修改别名、后缀或父类型。

**原因：** QMimeType 是只读查询值。

**处理：** 修改 MIME 数据库属于部署和系统数据管理问题，不是 QMimeType 的公开 API。

## API 速查表
### 12.1 状态和身份

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMimeType()` | 构造 invalid 描述 | 不查询数据库，不等于默认类型 |
| `QMimeType(const QMimeType &)` | 复制描述值 | 共享只读状态，不复制文件或数据库记录 |
| 移动构造/移动赋值 | 移动描述 handle | moved-from 对象不要继续当原类型使用 |
| `~QMimeType()` | 释放共享描述 | 不修改系统 MIME 数据 |
| `swap()` | 交换两个描述值 | 不改变数据库和类型关系 |
| `isValid()` | 判断描述是否有效 | 不等于某个文件内容已验证 |
| `isDefault()` | 判断是否为默认兜底类型 | valid 也可能 default |
| `name()` | 返回 canonical MIME 名称 | 程序逻辑和持久化优先使用 |
| `aliases()` | 返回替代名称 | 用于兼容和诊断，不是独立类型 |

### 12.2 层次和文件规则

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `parentMimeTypes()` | 返回直接父类型 | 只是一层关系 |
| `allAncestors()` | 返回全部祖先类型 | 适合多级分类检查 |
| `inherits(name)` | 判断 MIME 分类继承关系 | 不代表 C++ 继承或数据可转换 |
| `suffixes()` | 返回所有后缀 | 完整候选，不是内容验证 |
| `preferredSuffix()` | 返回首选后缀 | 可能为空；不一定是唯一合法后缀 |
| `globPatterns()` | 返回文件名 glob 模式 | 只匹配名称 |

### 12.3 UI 描述和图标

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `comment()` | 返回人类可读描述 | 可能本地化，不用于逻辑判断 |
| `iconName()` | 返回专用图标名称 | 需要 GUI 侧再加载 |
| `genericIconName()` | 返回通用图标名称 | 专用图标不存在时可降级 |
| `filterString()` | 返回文件选择器过滤器 | 面向 UI，不是跨平台持久化格式 |

### 12.4 值类型辅助

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator==` / `operator!=` | 比较逻辑 MIME 描述 | 跨环境稳定判断优先比较 `name()` |
| `qHash(const QMimeType &, size_t)` | 放入哈希容器 | 当前进程内使用；持久化用 canonical name |
| `QMimeDatabase` | 创建和查询 `QMimeType` | 区分查找责任和描述责任 |

## 13. 一句话总结

`QMimeType` 是 MIME 数据库返回的只读描述值：`name()` 是程序身份，`comment()` 和图标字段服务 UI，后缀和 glob 用于文件名规则，`parentMimeTypes()`、`allAncestors()` 和 `inherits()` 表达类型分类关系。使用时区分 invalid 与 valid-but-default，不要把 MIME 描述、文件扩展名或继承关系误当成真实内容验证。
