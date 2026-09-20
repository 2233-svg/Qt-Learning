# Qt Core 基础：文件、目录与流

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core  
> 核心类型：`QIODevice`、`QFile`、`QDir`、`QFileInfo`、`QTextStream`、`QDataStream`、`QSaveFile`

## 1. 先建立 I/O 分层模型

Qt 把“数据从哪里来”和“如何解释数据”分开：

```text
数据格式层
├─ QTextStream：字符、行、数字文本
└─ QDataStream：有版本的二进制值序列
             ↓
设备抽象层 QIODevice
├─ QFile：文件
├─ QBuffer：内存 QByteArray
├─ QTcpSocket：TCP 连接
├─ QProcess：子进程管道
└─ 其他设备
```

因此 `QTextStream` 不只可以读文件，也可以读内存或套接字；`QFile` 既可直接读写字节，也可交给流处理。

路径相关职责单独由以下类型承担：

- `QDir`：目录、路径组合、枚举和创建目录。
- `QFileInfo`：查询一个路径对应条目的名称、类型、大小和时间等元数据。
- `QStandardPaths`：获取跨平台标准目录。

## 2. QIODevice：统一的设备接口

`QIODevice` 是抽象基类，统一提供：

```cpp
open();
close();
read();
readAll();
readLine();
write();
seek();
pos();
size();
```

设备分两类：

- **随机访问设备**：可 `seek()`，例如普通文件。
- **顺序设备**：数据只能按到达顺序处理，例如套接字和某些进程管道。

```cpp
if (device->isSequential()) {
    // 不假设 size() 是完整数据长度，也不依赖任意 seek()
}
```

编写接受 `QIODevice *` 的函数，可以让同一解析逻辑同时用于文件、内存和网络。

## 3. 打开模式

常用 `QIODeviceBase::OpenModeFlag`：

| 标志 | 含义 |
|---|---|
| `ReadOnly` | 只读 |
| `WriteOnly` | 只写 |
| `ReadWrite` | 读写 |
| `Append` | 所有写入追加到末尾 |
| `Truncate` | 打开时清空原内容 |
| `Text` | 启用平台文本换行转换 |
| `Unbuffered` | 请求绕过 Qt 设备缓冲 |
| `NewOnly` | 仅当目标不存在时创建 |
| `ExistingOnly` | 仅打开已经存在的目标 |

组合标志：

```cpp
if (!file.open(QIODevice::WriteOnly |
               QIODevice::Text |
               QIODevice::Truncate)) {
    // 处理错误
}
```

写文件前必须明确：覆盖、追加还是仅新建。不要依赖自己记忆中的隐式截断规则。

## 4. 用 QFile 读取全部字节

```cpp
#include <QFile>

QFile file(QStringLiteral("data.json"));

if (!file.open(QIODevice::ReadOnly)) {
    qWarning() << "open failed:" << file.errorString();
    return;
}

const QByteArray bytes = file.readAll();

if (file.error() != QFileDevice::NoError) {
    qWarning() << "read failed:" << file.errorString();
    return;
}
```

打开成功并不保证后续读取一定成功。磁盘、网络文件系统和设备都可能在操作中途出错。

`QFile` 是栈对象时，析构会关闭文件。显式 `close()` 仍可用于需要尽早释放句柄的场景。

## 5. 读取文本文件

### 5.1 一次读取全部 UTF-8

```cpp
QFile file(path);
if (!file.open(QIODevice::ReadOnly)) {
    return std::nullopt;
}

const QByteArray bytes = file.readAll();
if (file.error() != QFileDevice::NoError) {
    return std::nullopt;
}

return QString::fromUtf8(bytes);
```

适合大小受控的配置或文档。不能对未知大小文件无条件 `readAll()`，否则可能占用过多内存。

### 5.2 用 QTextStream 逐行读取

```cpp
#include <QStringConverter>
#include <QTextStream>

QFile file(path);
if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    qWarning() << file.errorString();
    return;
}

QTextStream input(&file);
input.setEncoding(QStringConverter::Utf8);

while (!input.atEnd()) {
    const QString line = input.readLine();
    processLine(line);
}

if (input.status() != QTextStream::Ok)
    qWarning() << "text read failed";
```

Qt 6 的 `QTextStream` 默认编码是 UTF-8，但在文件格式要求固定时显式设置编码能让约定更清楚。

## 6. 写入文本文件

```cpp
QFile file(path);
if (!file.open(QIODevice::WriteOnly |
               QIODevice::Text |
               QIODevice::Truncate)) {
    qWarning() << file.errorString();
    return false;
}

QTextStream output(&file);
output.setEncoding(QStringConverter::Utf8);
output << "name=" << userName << '\n';
output << "count=" << count << '\n';
output.flush();

if (output.status() != QTextStream::Ok) {
    qWarning() << "write failed:" << file.errorString();
    return false;
}

return true;
```

`flush()` 将流缓冲提交给设备，但不等同于保证物理磁盘已经持久化。对数据安全有严格要求时还需理解操作系统缓存和文件系统语义。

## 7. 为什么保存完整文档要用 QSaveFile

直接覆盖：

```text
打开原文件并截断
→ 写到一半断电或磁盘满
→ 原文件只剩半份甚至为空
```

`QSaveFile` 的默认策略：

```text
在同目录创建临时文件
→ 完整写入
→ commit()
→ 原子替换目标文件
```

示例：

```cpp
#include <QSaveFile>

bool saveText(const QString &path, const QString &text)
{
    QSaveFile file(path);

    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        qWarning() << file.errorString();
        return false;
    }

    QTextStream output(&file);
    output.setEncoding(QStringConverter::Utf8);
    output << text;
    output.flush();

    if (output.status() != QTextStream::Ok) {
        file.cancelWriting();
        return false;
    }

    if (!file.commit()) {
        qWarning() << file.errorString();
        return false;
    }

    return true;
}
```

`QSaveFile` 不使用普通 `close()` 完成保存，必须调用 `commit()`。对象销毁前未 commit，临时内容会被丢弃。

`setDirectWriteFallback(true)` 在无法创建临时文件时允许直接覆盖，但会失去原子性，崩溃时可能留下部分文件。内部配置和关键数据通常应保留默认的原子保证。

## 8. 二进制数据：QDataStream

`QDataStream` 把 C++/Qt 值按定义好的二进制格式写入 `QIODevice`：

```cpp
QFile file(path);
if (!file.open(QIODevice::WriteOnly))
    return false;

QDataStream output(&file);
output.setVersion(QDataStream::Qt_6_10);
output << quint32(0x4D594150);
output << QStringLiteral("Alice");
output << qint32(42);

return output.status() == QDataStream::Ok;
```

读取时使用同一字段顺序和版本：

```cpp
QDataStream input(&file);
input.setVersion(QDataStream::Qt_6_10);

quint32 magic = 0;
QString name;
qint32 score = 0;

input >> magic >> name >> score;
```

### 8.1 必须设计文件格式

至少包含：

- 魔数：确认文件类型
- 格式版本：支持未来升级
- 明确字段顺序和数值宽度
- 长度或边界检查
- 错误状态检查

```cpp
if (magic != ExpectedMagic)
    return ParseError::WrongFormat;
```

### 8.2 QDataStream 版本

Qt 的流格式可能随版本演进。持久化或跨程序交换时显式 `setVersion()`，读写双方保持一致。

`QDataStream::Version` 是 Qt 序列化格式版本，不是你自己的业务文件版本；通常两者都需要。

### 8.3 字节序

```cpp
stream.setByteOrder(QDataStream::LittleEndian);
```

只有协议明确规定时修改。网络协议常规定大端，私有文件格式则应写进格式规范。

### 8.4 不要用 QDataStream 猜测任意二进制协议

外部协议若规定逐字段字节布局，应严格按协议读写。`QDataStream << value` 使用的是 Qt 定义的序列化格式，不保证等于某个 C 结构体内存或第三方协议格式。

## 9. 顺序设备与增量解析

套接字的 `readyRead()` 只表示“现在有一些数据”，不代表完整消息已经到达：

```cpp
connect(socket, &QTcpSocket::readyRead, this, [this] {
    buffer_.append(socket->readAll());
    parseCompleteFrames();
});
```

解析器需要处理：

- 半个消息
- 一次到达多个消息
- 非法长度
- 超大输入
- 连接关闭时剩余数据

`QDataStream` 的事务 API 可以在数据不足时回滚读取位置：

```cpp
stream.startTransaction();
stream >> header >> payload;

if (!stream.commitTransaction()) {
    // 数据尚不完整，等待下一次 readyRead
}
```

这与普通文件一次性读取的思维不同。

## 10. QDir：目录和路径组合

### 10.1 组合路径

```cpp
QDir directory(basePath);
QString configPath = directory.filePath(QStringLiteral("config/app.json"));
```

不要手工拼接 `/` 或 `\`：

```cpp
QString path = basePath + "/" + fileName; // 不推荐
```

Qt 内部路径通常可使用 `/`，需要显示原生分隔符时：

```cpp
QString shown = QDir::toNativeSeparators(path);
```

### 10.2 清理路径

```cpp
QString clean = QDir::cleanPath(QStringLiteral("a/./b/../c"));
```

`cleanPath()` 做字符串层面的规范化，不等同于访问文件系统，也不保证解析符号链接。

### 10.3 绝对路径与规范路径

- `absolutePath()`：根据当前目录形成绝对路径。
- `canonicalPath()`：解析 `.`、`..` 和符号链接，目标需存在；失败可能返回空字符串。

安全校验目录边界时，仅做字符串前缀比较通常不够，要考虑规范路径、符号链接、大小写和竞态条件。

## 11. 创建和枚举目录

递归创建：

```cpp
QDir directory;
if (!directory.mkpath(targetPath)) {
    qWarning() << "Cannot create" << targetPath;
}
```

枚举 `.json` 文件：

```cpp
QDir directory(path);
const QFileInfoList files = directory.entryInfoList(
    {QStringLiteral("*.json")},
    QDir::Files | QDir::Readable,
    QDir::Name | QDir::IgnoreCase);

for (const QFileInfo &info : files)
    qDebug() << info.absoluteFilePath();
```

使用过滤器排除 `.`、`..`，区分文件、目录、隐藏项和符号链接。

### 11.1 removeRecursively 的危险性

```cpp
QDir(path).removeRecursively();
```

这是破坏性操作，会尽力删除整个目录树。调用前必须：

1. 验证路径非空。
2. 转换并检查规范绝对路径。
3. 确认目标位于允许的工作目录内。
4. 禁止根目录、用户目录和过宽父目录。
5. 考虑符号链接和竞态。

它失败时仍会继续尝试删除其他内容，最后返回 false，因此失败不表示“什么都没删”。

## 12. QFileInfo：查询文件元数据

```cpp
QFileInfo info(path);

qDebug() << info.fileName();
qDebug() << info.baseName();
qDebug() << info.completeBaseName();
qDebug() << info.suffix();
qDebug() << info.absoluteFilePath();
qDebug() << info.size();
qDebug() << info.lastModified();
qDebug() << info.isFile();
qDebug() << info.isDir();
qDebug() << info.isSymLink();
```

`QFileInfo` 可能缓存文件系统查询结果。外部程序可能修改文件，需要最新状态时调用：

```cpp
info.refresh();
```

即使刚刚检查 `exists()`，下一行操作时文件仍可能被其他进程删除或替换。这是典型的检查与使用竞态；真正的操作结果才是最终依据。

## 13. 标准目录：QStandardPaths

不要把配置和数据硬编码到当前目录：

```cpp
const QString configDir = QStandardPaths::writableLocation(
    QStandardPaths::AppConfigLocation);

QDir().mkpath(configDir);
```

常见位置：

- `AppConfigLocation`：应用配置
- `AppDataLocation`：应用数据
- `CacheLocation`：可重建缓存
- `DocumentsLocation`：用户文档
- `TempLocation`：临时文件

缓存、配置和用户文档具有不同生命周期，不应全部堆在可执行文件目录。

## 14. 临时文件与临时目录

```cpp
QTemporaryFile file;
if (file.open()) {
    file.write(data);
}
```

```cpp
QTemporaryDir directory;
if (directory.isValid()) {
    const QString path = directory.filePath(QStringLiteral("work.dat"));
}
```

对象析构时默认清理临时内容，适合测试、中间产物和安全生成唯一名称。需要保留时使用相应的自动移除设置。

不要用时间戳或随机数手工猜临时文件名，这容易碰撞并产生安全问题。

## 15. Qt 资源系统

编译进程序的资源使用 `:/` 路径：

```cpp
QFile file(QStringLiteral(":/templates/default.json"));
if (file.open(QIODevice::ReadOnly)) {
    const QByteArray data = file.readAll();
}
```

资源路径是只读的，并被视为绝对路径。它适合图标、固定模板和内置配置默认值，不适合运行时保存用户数据。

## 16. 文件复制、重命名与删除

```cpp
bool copied = QFile::copy(source, destination);
bool renamed = QFile::rename(oldPath, newPath);
bool removed = QFile::remove(path);
```

注意：

- 目标已存在时，`copy()` 和 `rename()` 通常不会直接覆盖。
- 操作返回 false 时读取 `errorString()` 或记录相关路径。
- 删除是不可恢复动作；用户文件优先考虑 `moveToTrash()`。
- 跨文件系统重命名可能退化为复制后删除，不应假设永远是原子操作。

## 17. 错误处理原则

错误信息应包含操作、路径和系统说明：

```cpp
if (!file.open(QIODevice::ReadOnly)) {
    qWarning().noquote()
        << QStringLiteral("无法读取 %1：%2")
               .arg(QDir::toNativeSeparators(file.fileName()),
                    file.errorString());
}
```

需要分别检查：

1. 打开是否成功。
2. read/write 返回的字节数。
3. 流的 `status()`。
4. 关闭或 `commit()` 是否成功。
5. 解析后的格式是否合法。

不要捕获所有错误后只返回空字符串，因为空文件可能是合法结果。使用 `std::optional`、结果结构或明确错误枚举表达失败。

## 18. 完整示例：安全保存和加载 UTF-8 文本

```cpp
#include <QFile>
#include <QSaveFile>
#include <QStringConverter>
#include <QTextStream>
#include <optional>

struct LoadError
{
    QString message;
};

std::optional<QString> loadUtf8Text(const QString &path,
                                    LoadError *error)
{
    QFile file(path);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        if (error)
            error->message = file.errorString();
        return std::nullopt;
    }

    QTextStream input(&file);
    input.setEncoding(QStringConverter::Utf8);
    const QString text = input.readAll();

    if (input.status() != QTextStream::Ok) {
        if (error)
            error->message = file.errorString();
        return std::nullopt;
    }

    return text;
}

bool saveUtf8Text(const QString &path,
                  const QString &text,
                  QString *error)
{
    QSaveFile file(path);

    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        if (error)
            *error = file.errorString();
        return false;
    }

    QTextStream output(&file);
    output.setEncoding(QStringConverter::Utf8);
    output << text;
    output.flush();

    if (output.status() != QTextStream::Ok) {
        file.cancelWriting();
        if (error)
            *error = file.errorString();
        return false;
    }

    if (!file.commit()) {
        if (error)
            *error = file.errorString();
        return false;
    }

    return true;
}
```

这个接口区分：

- 成功读取空文件：返回包含空 `QString` 的 optional。
- 读取失败：返回 `std::nullopt` 并提供错误。
- 保存失败：返回 false，不留下半写入的正式文件。

## 19. 常见错误

### 19.1 不检查 open 返回值

后续读写只会产生更多误导结果。任何 I/O 操作都先处理打开失败。

### 19.2 用 QString 直接猜字节编码

读取文件先得到字节，再按文件格式规定解码。不要靠 `fromLocal8Bit()` 碰运气。

### 19.3 对巨大或未知输入使用 readAll

可能耗尽内存。使用分块、逐行或有上限的协议解析。

### 19.4 直接覆盖重要文档

中途失败会破坏原文件。完整保存优先 `QSaveFile`。

### 19.5 只检查文件是否存在

存在不代表可读，检查之后状态也可能改变。直接执行并处理真实错误。

### 19.6 混淆路径清理和真实规范化

`cleanPath()` 是字符串操作；`canonicalPath()` 查询文件系统并解析链接。

### 19.7 二进制流不设置版本

应用升级后可能无法稳定读取旧数据。固定 `QDataStream` 版本并另设业务格式版本。

### 19.8 假设一次 readyRead 是完整消息

顺序设备可能分片或合并消息。必须设计帧边界并增量解析。

## 20. API 速查

| API | 作用 | 关键点 |
|---|---|---|
| `QFile::open()` | 打开文件 | 检查 bool 和 errorString |
| `readAll()` | 读取剩余全部字节 | 输入大小必须受控 |
| `readLine()` | 读取一行 | 返回字节或配合 QTextStream |
| `write()` | 写入字节 | 检查实际写入量或设备错误 |
| `QTextStream` | 文本格式读写 | 明确 encoding 和 status |
| `QDataStream` | Qt 二进制值序列 | 固定版本和字段顺序 |
| `QSaveFile::commit()` | 原子提交完整文件 | 替代 close |
| `QDir::filePath()` | 组合目录与文件名 | 避免手拼分隔符 |
| `QDir::cleanPath()` | 字符串层面清理路径 | 不解析符号链接 |
| `QDir::canonicalPath()` | 获取真实规范路径 | 目标通常需存在 |
| `QDir::mkpath()` | 递归创建目录 | 检查返回值 |
| `entryInfoList()` | 枚举目录项及元数据 | 设置过滤和排序 |
| `QFileInfo::refresh()` | 刷新缓存元数据 | 外部状态可能变化 |
| `QStandardPaths` | 获取标准系统目录 | 区分配置、数据和缓存 |
| `QTemporaryFile/Dir` | 创建安全临时资源 | 默认随对象清理 |

## 21. 自测题

1. `QFile` 与 `QTextStream` 的职责有什么区别？
2. 为什么 `readAll()` 不适合未知大小输入？
3. `postEvent()` 和文件 I/O 无关，但为什么异步套接字读取仍依赖事件循环？
4. `QSaveFile` 为什么比直接覆盖更安全？
5. `QDataStream` 版本和业务文件版本有什么区别？
6. `cleanPath()` 与 `canonicalPath()` 有何区别？
7. 为什么 `exists()` 成功后，真正打开仍可能失败？
8. `QIODevice::Text` 主要处理什么平台差异？
9. 顺序设备为何不能把 `size()` 当成完整消息长度？
10. 清空 Qt 资源文件内容为什么不可行？

### 参考答案

1. QFile 提供文件设备和字节 I/O；QTextStream 在设备上编码、解码和格式化文本。
2. 它会尝试把剩余内容全部放进内存，可能耗尽资源。
3. `readyRead` 等通知和排队槽需要所属线程事件循环分发。
4. 先写同目录临时文件，成功后原子替换，失败时保留原文件。
5. 前者控制 Qt 类型的序列化规则，后者描述应用自定义字段结构的演进。
6. 前者只清理路径字符串，后者访问文件系统并解析真实路径和符号链接。
7. 两次操作之间状态可能变化，也可能存在权限、锁定等问题。
8. 文本模式主要处理换行等平台文本约定。
9. 当前可用字节只是数据流的一部分，后续仍可能到达。
10. `:/` 资源编译进程序，是只读数据。

---

## 总结

Qt I/O 的正确思路是先分层：`QIODevice` 提供统一设备，`QFile` 访问文件字节，`QTextStream` 和 `QDataStream` 分别解释文本与二进制，`QDir/QFileInfo` 管理路径和元数据。可靠代码必须明确编码、打开模式、数据边界和所有权，并在打开、读写、流状态和最终提交的每一步检查错误。保存完整文档时使用 `QSaveFile`，处理外部数据时设置大小上限和格式版本，才能避免乱码、半写文件、内存耗尽和升级后不兼容。
