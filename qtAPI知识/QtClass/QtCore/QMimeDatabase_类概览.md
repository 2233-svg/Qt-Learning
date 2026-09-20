# Qt QMimeDatabase MIME 类型识别数据库笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMimeDatabase>`  
> 所属模块：`Qt6::Core`  
> 类型性质：查询系统 MIME 类型数据库的值对象  
> 相关类型：`QMimeType`、`QFileInfo`、`QIODevice`、`QUrl`、`QStandardPaths`

## 1. 它解决什么问题

`QMimeDatabase` 把“文件或数据是什么类型”的判断统一交给 Qt MIME 数据库。调用方不必自己维护扩展名表、魔数表和父类型关系，就可以按不同信息源查询：

```text
类型名称/别名  -> mimeTypeForName()
文件名/后缀    -> mimeTypeForFile()
文件内容       -> mimeTypeForData()
URL            -> mimeTypeForUrl()
文件名 + 内容  -> mimeTypeForFileNameAndData()
```

查询结果是 `QMimeType`，里面包含 canonical name、别名、后缀、图标、父类型和继承关系等描述。

典型场景：

- 文件管理器展示图标和类型名称；
- “打开文件”对话框生成过滤器；
- 导入器在打开前选择解析器；
- 拖放或上传前判断内容类型；
- 处理没有可靠扩展名的二进制数据；
- 检查一个自定义 MIME 类型是否继承自通用类型。

## 2. 它不是什么

`QMimeDatabase` 不是：

- 文件格式解析器；
- 安全扫描器；
- 文件扩展名的简单哈希表；
- 保证识别结果绝对正确的协议验证器；
- 负责打开、读取、关闭文件的所有权对象；
- 用于创建或注册 MIME XML 数据库的公开管理器。

识别结果只适合帮助选择处理路径。真正解析前仍要检查文件内容、版本、大小和安全边界。尤其不要把 MIME 类型当成“文件一定安全”或“内容一定符合格式”的证明。

## 3. 查询模式：后缀和内容不是一回事

### 3.1 `MatchDefault`

```cpp
const QMimeType type =
    database.mimeTypeForFile(fileName,
                             QMimeDatabase::MatchDefault);
```

默认模式会结合文件名信息和内容信息进行常规判断：通常先利用扩展名，必要时再用内容识别。它是普通文件类型识别的推荐起点，但不应理解成“永远只看后缀”或“永远以内容覆盖后缀”。

### 3.2 `MatchExtension`

```cpp
const QMimeType type =
    database.mimeTypeForFile(fileName,
                             QMimeDatabase::MatchExtension);
```

只按文件名扩展名匹配，不读取文件内容。适合：

- 只拿到文件名而没有读取权限；
- 生成过滤器或预测用户选择；
- 明确要求保留用户扩展名语义。

扩展名可被伪造，因此不适合作为安全解析依据。

### 3.3 `MatchContent`

```cpp
const QMimeType type =
    database.mimeTypeForFile(fileName,
                             QMimeDatabase::MatchContent);
```

优先按文件内容识别。文件名仍可能作为上下文或辅助信息参与最终选择，但此模式的目的就是避免只信任扩展名。

内容识别需要读取文件或设备，可能产生 I/O。对大文件通常只读取识别所需的前缀，但调用方仍应把它当作可能阻塞的操作，不要在 GUI 线程对慢网络设备无条件调用。

## 4. 最小使用方式

### 4.1 根据文件名查询

```cpp
#include <QMimeDatabase>
#include <QMimeType>

QMimeDatabase database;
const QMimeType type =
    database.mimeTypeForFile(QStringLiteral("report.pdf"));

if (type.isValid())
    qDebug() << type.name() << type.preferredSuffix();
```

文件名查询不等于读取文件内容。需要抵抗错误扩展名时使用 `MatchContent`，或使用文件名和内容联合查询。

### 4.2 根据内存数据查询

```cpp
const QByteArray bytes = readHeader();
const QMimeType type = database.mimeTypeForData(bytes);

if (type.isValid())
    qDebug() << type.name();
```

空数据或无法识别的数据通常会得到一个有效的默认二进制类型，而不是“数据库查询失败”的异常对象。后续应根据 `type.isDefault()` 和 `type.name()` 决定是否继续。

### 4.3 文件名和内容联合判断

```cpp
const QMimeType type =
    database.mimeTypeForFileNameAndData(
        QStringLiteral("download.bin"),
        bytes);
```

当内容提供了魔数、文件名提供了扩展名时，这个 API 比只使用其中一种信息更适合导入和下载场景。仍要把结果当作提示，真正解析时进行格式验证。

## 5. 结果状态：invalid 和 default 要分开

### 5.1 invalid `QMimeType`

查询名称不存在，或数据库没有可用描述时，结果可能是无效 `QMimeType`：

```cpp
if (!type.isValid()) {
    // 没有可用的 MIME 类型描述
}
```

无效结果的 `name()`、`comment()`、后缀和图标等属性通常为空或无意义。

### 5.2 default MIME type

对于无法从内容或名称确定具体格式的普通数据，数据库通常使用默认二进制类型 `application/octet-stream`。这通常是一个有效的 `QMimeType`，但：

```cpp
type.isValid() == true
type.isDefault() == true
```

它表示“有一个通用默认类型”，不表示识别出了具体文件格式。不要把 `isValid()` 当成“识别足够精确”。

## 6. QIODevice 的读取边界

### 6.1 `mimeTypeForData(QIODevice *)`

```cpp
QFile file(fileName);
if (!file.open(QIODevice::ReadOnly))
    return;

const QMimeType type =
    database.mimeTypeForData(&file);
```

传入设备时，设备必须能够被读取，且设备的打开状态、当前位置、可随机访问性和 I/O 错误都会影响结果。`QMimeDatabase` 不接管设备所有权，调用方仍负责设备的生命周期和关闭。

识别过程可能读取设备内容。若设备不是可随机访问的流，不能假设查询后可以从原位置无条件继续消费；需要保留业务读取位置时，调用前后按设备能力保存和恢复位置，或先把需要的字节复制到 `QByteArray`。

### 6.2 `mimeTypeForFileNameAndData(QString, QIODevice *)`

```cpp
QFile file(fileName);
if (!file.open(QIODevice::ReadOnly))
    return;

const QMimeType type =
    database.mimeTypeForFileNameAndData(
        fileName, &file);
```

它把文件名和设备内容一起交给识别器。设备仍是借用对象，不会转移所有权。调用前要确认设备可读，并把可能的阻塞 I/O 放在合适线程。

## 7. URL 查询的边界

```cpp
const QMimeType type =
    database.mimeTypeForUrl(
        QUrl(QStringLiteral("file:///tmp/report.pdf")));
```

`mimeTypeForUrl()` 主要适合本地文件 URL 或带有文件名信息的 URL。对于远程 URL，Qt 通常只能根据 URL 路径和后缀做有限判断，不能凭 URL 自动下载并验证远程内容。

因此：

- 本地 URL 可以先转为 `QFileInfo` 或本地路径，再按文件和内容查询；
- HTTP 等远程 URL 的 MIME 类型可能来自后缀或有限信息；
- 网络响应的 `Content-Type` 和实际 payload 仍要由网络层和解析器验证；
- 不要因为返回了某个 MIME 类型就自动执行远程内容。

## 8. 文件名查询和后缀查询

### 8.1 `mimeTypesForFileName()`

```cpp
const QList<QMimeType> candidates =
    database.mimeTypesForFileName(
        QStringLiteral("archive.tar.gz"));
```

返回所有匹配文件名的候选 MIME 类型。它只根据文件名规则，不读取内容。一个文件名可能对应多个候选，调用方要结合业务优先级或内容识别选择最终类型。

### 8.2 `suffixForFileName()`

```cpp
const QString suffix =
    database.suffixForFileName(
        QStringLiteral("archive.tar.gz"));
```

返回适合 MIME 查询的文件名后缀。对于复合后缀，结果可能包含多段后缀，而不是简单地取最后一个点之后的字符串。它不返回 MIME 类型，也不保证该后缀对应的文件内容真实匹配。

## 9. 枚举整个数据库

```cpp
const QList<QMimeType> types =
    database.allMimeTypes();
```

`allMimeTypes()` 返回数据库当前可见的所有 MIME 类型，适合：

- 生成调试报告；
- 构建类型选择器；
- 检查系统安装的 MIME 描述；
- 诊断某个类型为什么没有被识别。

它可能返回较大的列表，不应在每次绘制或每个文件判断时重复枚举。需要反复查询时，在合适范围内保存结果或直接用按名称查询。

## 10. MIME 数据库来自哪里

Qt 通常读取平台提供的 MIME 数据描述，并结合 Qt 自己可见的数据目录。数据库内容可能随操作系统、安装的软件包和环境变量变化，因此：

- 同一文件在不同平台上可能得到不同 comment、icon 或候选类型；
- 类型名称和标准 MIME 语义通常比 comment 更适合程序逻辑；
- 测试不应只断言本地化 comment；
- 自定义 MIME 类型的安装位置和刷新行为属于部署问题，不能只依赖开发机结果。

## 11. 逐项 API 语义

### 11.1 `QMimeDatabase()`

```cpp
QMimeDatabase();
```

构造 MIME 数据库查询对象。它不是一个需要手动打开的文件数据库连接，也不负责独占系统 MIME 数据文件。

### 11.2 `~QMimeDatabase()`

```cpp
~QMimeDatabase();
```

销毁查询对象。它不删除系统 MIME 数据，也不影响已经返回的 `QMimeType` 值对象。

### 11.3 `mimeTypeForName(const QString &nameOrAlias) const`

```cpp
QMimeType mimeTypeForName(
    const QString &nameOrAlias) const;
```

按 canonical MIME 名称或别名查询类型：

```cpp
const QMimeType pdf =
    database.mimeTypeForName(
        QStringLiteral("application/pdf"));
```

未知名称或别名得到的结果应检查 `isValid()`。程序逻辑通常保存 canonical `name()`，而不是继续保存用户输入的 alias。

### 11.4 `mimeTypeForFile(const QString &, MatchMode) const`

```cpp
QMimeType mimeTypeForFile(
    const QString &fileName,
    MatchMode mode = MatchDefault) const;
```

根据路径字符串和指定模式识别文件类型。路径可以是存在或不存在的文件名；是否能进行内容识别取决于路径可访问性和模式。

不要把 `fileName` 重载与 `QFileInfo` 重载当成完全相同的输入语义：`QFileInfo` 可以携带已解析的文件状态、目录信息和符号链接相关信息。

### 11.5 `mimeTypeForFile(const QFileInfo &, MatchMode) const`

```cpp
QMimeType mimeTypeForFile(
    const QFileInfo &fileInfo,
    MatchMode mode = MatchDefault) const;
```

根据 `QFileInfo` 查询。使用 `MatchContent` 时，Qt 可以利用文件信息打开或读取对应文件；调用方仍要保证路径、权限和文件状态适合读取。

文件在查询前后可能被其他线程或进程替换。安全导入不能只依赖一次 MIME 识别结果。

### 11.6 `mimeTypesForFileName(const QString &) const`

```cpp
QList<QMimeType> mimeTypesForFileName(
    const QString &fileName) const;
```

返回按文件名规则匹配的候选类型列表，不读取文件内容。列表为空表示没有匹配规则；多个结果需要调用方进一步选择。

### 11.7 `mimeTypeForData(const QByteArray &) const`

```cpp
QMimeType mimeTypeForData(
    const QByteArray &data) const;
```

根据内存字节的内容识别类型。`data` 是值参数视图之外的独立 QByteArray 值语义，调用不会让数据库拥有调用方缓冲区。

识别能力依赖输入数据是否包含足够的文件头；短片段、截断数据和文本内容可能只能得到通用类型。

### 11.8 `mimeTypeForData(QIODevice *) const`

```cpp
QMimeType mimeTypeForData(
    QIODevice *device) const;
```

从可读设备读取必要内容进行识别。设备由调用方拥有，数据库不会 delete 它。不要传入已经销毁、不可读或正在被另一个线程改变的设备。

### 11.9 `mimeTypeForUrl(const QUrl &) const`

```cpp
QMimeType mimeTypeForUrl(
    const QUrl &url) const;
```

根据 URL 的本地路径或名称信息推断 MIME 类型。它不是网络下载 API，不应期待它读取远程资源内容。

### 11.10 `mimeTypeForFileNameAndData(const QString &, QIODevice *) const`

```cpp
QMimeType mimeTypeForFileNameAndData(
    const QString &fileName,
    QIODevice *device) const;
```

联合使用文件名和设备内容进行识别。文件名提供扩展名线索，设备提供内容线索；二者出现冲突时，最终选择由 Qt MIME 数据库和识别规则决定，调用方仍应做格式验证。

### 11.11 `mimeTypeForFileNameAndData(const QString &, const QByteArray &) const`

```cpp
QMimeType mimeTypeForFileNameAndData(
    const QString &fileName,
    const QByteArray &data) const;
```

联合使用文件名和内存字节识别类型，适合下载缓存、上传缓冲区和“文件名已知但尚未落盘”的场景。

### 11.12 `suffixForFileName(const QString &) const`

```cpp
QString suffixForFileName(
    const QString &fileName) const;
```

提取用于 MIME 文件名匹配的后缀，支持 MIME 数据库理解的复合后缀。它只处理名称，不验证文件内容。

### 11.13 `allMimeTypes() const`

```cpp
QList<QMimeType> allMimeTypes() const;
```

返回当前数据库中的所有类型描述。返回的是值列表；列表和其中的 `QMimeType` 可以独立保存，但它们反映的是查询时可见的数据库状态。

## 12. 常见错误

### 12.1 把扩展名当成内容验证

**问题：** `report.pdf.exe` 或伪造扩展名被当成安全 PDF。

**原因：** `MatchExtension` 只读取名称规则。

**处理：** 安全导入使用内容识别和真实格式解析，扩展名只作为辅助线索。

### 12.2 把 `isValid()` 当成具体识别成功

**问题：** `application/octet-stream` 被当成已确认的业务格式。

**原因：** 默认类型本身可以是有效 `QMimeType`。

**处理：** 同时检查 `isDefault()` 和 canonical `name()`。

### 12.3 把 `mimeTypeForUrl()` 当网络探测

**问题：** 根据远程 URL 自动决定解析器或执行动作。

**原因：** URL 查询通常不下载远程 payload。

**处理：** 使用网络响应头和实际字节，并执行内容验证。

### 12.4 忽略 `QIODevice` 的阻塞和位置

**问题：** GUI 卡顿或后续读取从错误位置开始。

**原因：** 内容识别可能读取设备。

**处理：** 在工作线程处理慢设备，必要时保存/恢复位置或先缓存字节。

### 12.5 每个文件都调用 `allMimeTypes()`

**问题：** 不必要的扫描和分配。

**原因：** 全量枚举不是单文件查询的替代品。

**处理：** 使用 `mimeTypeForFile()`、`mimeTypeForName()` 等定向 API。

### 12.6 用本地化 comment 做程序判断

**问题：** 不同系统语言下逻辑失效。

**原因：** `comment()` 面向人类显示。

**处理：** 用 canonical `name()` 做程序分支，用 comment 做界面文本。

## API 速查表
### 13.1 模式和按来源查询

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `MatchDefault` | 常规结合名称和内容判断 | 具体优先级由 MIME 规则决定，不要当作只看后缀 |
| `MatchExtension` | 只按扩展名规则判断 | 快但可伪造，不适合安全验证 |
| `MatchContent` | 以内容识别为主 | 可能产生 I/O；不能保证解析安全 |
| `mimeTypeForName(nameOrAlias)` | 按名称或别名查类型 | 未知名称检查 `isValid()`；优先保存 canonical name |
| `mimeTypeForFile(fileName, mode)` | 根据路径字符串查类型 | 内容模式需要可访问文件 |
| `mimeTypeForFile(fileInfo, mode)` | 根据 QFileInfo 查类型 | 文件状态可能变化；结果不是安全证明 |
| `mimeTypesForFileName(fileName)` | 返回文件名匹配的候选列表 | 只看名称，不读取内容；可能有多个结果 |

### 13.2 内容、URL 和后缀

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `mimeTypeForData(QByteArray)` | 按内存字节识别 | 短数据或截断数据可能只能得到默认类型 |
| `mimeTypeForData(QIODevice *)` | 从设备内容识别 | 设备由调用方管理；考虑阻塞和位置 |
| `mimeTypeForUrl(QUrl)` | 根据 URL 本地路径/名称推断 | 不等于下载远程内容 |
| `mimeTypeForFileNameAndData(QString, QByteArray)` | 联合文件名和内存内容识别 | 适合下载或上传缓冲区；仍需解析验证 |
| `mimeTypeForFileNameAndData(QString, QIODevice *)` | 联合文件名和设备内容识别 | 设备必须可读；注意 I/O 与生命周期 |
| `suffixForFileName(fileName)` | 提取 MIME 规则使用的后缀 | 可能保留复合后缀；不验证内容 |
| `allMimeTypes()` | 枚举全部 MIME 类型 | 适合诊断和构建选择器，不要高频调用 |

### 13.3 协作类型

| 类型 | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMimeType` | 描述一次 MIME 查询结果 | 区分 invalid、default 和具体类型 |
| `QFileInfo` | 携带文件状态的查询输入 | 状态可能在查询期间改变 |
| `QIODevice` | 提供内容读取 | 所有权和线程安全由调用方负责 |
| `QUrl` | 提供 URL 及路径信息 | 远程 URL 不代表内容已读取 |

## 14. 一句话总结

`QMimeDatabase` 是 Qt 的 MIME 类型识别入口：按名称、扩展名、文件内容、URL 或“文件名加内容”查询 `QMimeType`。使用时先选择正确的 `MatchMode`，再区分 invalid 和有效但通用的 `application/octet-stream`；扩展名和 MIME 结果都只是识别线索，真正导入前仍要验证内容、处理 I/O 和执行安全检查。
