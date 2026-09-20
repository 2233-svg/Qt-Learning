# Qt QMimeData MIME 数据容器笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMimeData>`  
> 所属模块：`Qt6::Core`  
> 基类：`QObject`  
> 类型性质：为剪贴板和拖放保存多种 MIME 表示  
> 相关类型：`QClipboard`、`QDrag`、`QDropEvent`、`QMetaType`、`QUrl`

## 1. 它解决什么问题

`QMimeData` 是 Qt 在剪贴板和拖放流程中使用的数据载体。它把同一份内容按一个或多个 MIME 类型保存，使发送方和接收方可以协商彼此都理解的表示：

```text
同一内容
  +-- text/plain
  +-- text/html
  +-- text/uri-list
  +-- image/*
  +-- application/x-color
  +-- application/x-my-app-record
```

发送方可以同时提供高保真格式和通用降级格式。例如一个富文本编辑器可以同时设置 HTML 和纯文本；支持 HTML 的接收方使用 HTML，只支持文本的接收方使用纯文本。

它主要用于：

- `QClipboard` 的复制和粘贴；
- `QDrag` 发起拖动；
- `QDropEvent` 接收文件、文本、图片或自定义数据；
- `QAbstractItemModel::mimeData()` 编码模型索引；
- 应用内部通过 MIME 类型传输自定义二进制或结构化数据。

## 2. 它不是什么

`QMimeData` 不是：

- 只保存一种格式的字符串对象；
- MIME 类型数据库或文件类型识别器；
- 自动解析所有自定义二进制协议的序列化框架；
- 自动拥有拖放接收方对象的共享数据；
- 可以安全跨线程并发读写的容器；
- `QVariant` 的通用替代品。

它保存的是“格式到数据表示”的映射。MIME 类型本身只描述数据格式，不能自动告诉 Qt 你的自定义字节如何解码。

## 3. 对象所有权：通常把 new 出来的对象交给 Qt

`QMimeData` 继承自 `QObject`，并且禁止复制。典型代码是：

```cpp
auto *mimeData = new QMimeData;
mimeData->setText(QStringLiteral("hello"));

drag->setMimeData(mimeData);
```

`QDrag::setMimeData()` 和 `QClipboard::setMimeData()` 这类 API 通常会接管传入 `QMimeData` 的所有权。不要在交给 Qt 后再手动 `delete`，也不要把同一个对象同时交给多个所有者。

如果只是本地读取或构造测试，栈对象也可以：

```cpp
QMimeData mimeData;
mimeData.setData(QStringLiteral("text/plain"),
                 QByteArrayLiteral("hello"));
```

但栈对象不能跨出自身作用域交给需要异步使用的拖放或剪贴板流程。

## 4. 标准格式和便利 API

| 能力 | MIME 表示 | 查询 | 读取 | 设置 |
| --- | --- | --- | --- | --- |
| 纯文本 | `text/plain` | `hasText()` | `text()` | `setText()` |
| HTML | `text/html` | `hasHtml()` | `html()` | `setHtml()` |
| URL 列表 | `text/uri-list` | `hasUrls()` | `urls()` | `setUrls()` |
| 图片 | `image/*` | `hasImage()` | `imageData()` | `setImageData()` |
| 颜色 | `application/x-color` | `hasColor()` | `colorData()` | `setColorData()` |
| 任意字节 | 自定义 MIME 类型 | `hasFormat()` | `data()` | `setData()` |

便利 API 负责把常见 Qt 类型映射到标准 MIME 表示。需要跨应用互操作时，优先使用标准 MIME 类型；需要应用内部高保真传输时，再增加自定义格式。

## 5. 典型使用场景

### 5.1 拖入文件或 URL

```cpp
void MyWidget::dragEnterEvent(QDragEnterEvent *event)
{
    if (event->mimeData()->hasUrls())
        event->acceptProposedAction();
}

void MyWidget::dropEvent(QDropEvent *event)
{
    const QMimeData *data = event->mimeData();
    if (!data->hasUrls())
        return;

    for (const QUrl &url : data->urls()) {
        if (url.isLocalFile())
            importFile(url.toLocalFile());
    }
    event->acceptProposedAction();
}
```

`hasUrls()` 只说明数据可以按 URL 列表读取；它不保证每个 URL 都是本地文件，也不保证文件存在。接收方仍要检查 `QUrl::isLocalFile()`、权限和业务格式。

### 5.2 同时提供 HTML 和纯文本

```cpp
auto *mimeData = new QMimeData;
mimeData->setHtml(QStringLiteral("<b>Hello</b>"));
mimeData->setText(QStringLiteral("Hello"));
```

接收方根据能力选择表示：

```cpp
if (data->hasHtml()) {
    const QString html = data->html();
} else if (data->hasText()) {
    const QString plain = data->text();
}
```

设置多种表示不会自动让接收方理解 HTML。接收方应先选择自己信任和支持的格式。

### 5.3 自定义 MIME 二进制

```cpp
auto *mimeData = new QMimeData;
mimeData->setData(QStringLiteral("application/x-my-app-record"),
                  encodeRecord(record));
```

接收方必须同时知道：

- 完整 MIME 类型；
- 字节编码、版本和字节序；
- 数据长度和错误处理；
- 是否允许来自外部应用的不可信输入。

MIME 类型匹配不等于数据已经验证。解析自定义字节前要做长度、版本和边界检查。

## 6. MIME 格式优先级

### 6.1 `formats()` 返回可用格式列表

`formats()` 返回对象能够提供数据的 MIME 类型，并按优先级排列。一个对象可以同时拥有多种表示：

```cpp
const QStringList supported = mimeData->formats();
for (const QString &format : supported)
    qDebug() << format;
```

接收方不要假设列表顺序永远固定，也不要把“第一个格式”直接当作最安全格式。应从自己支持的格式中选择，并按业务策略确定优先级。

### 6.2 `hasFormat()` 是能力查询

```cpp
if (mimeData->hasFormat(QStringLiteral("text/csv"))) {
    const QByteArray csv = mimeData->data(
        QStringLiteral("text/csv"));
}
```

对自定义或非标准格式，先调用 `hasFormat()` 再读取更清晰。对于 `data()` 支持的尽力转换，不要把“可以返回某些字节”误解为原始格式确实存在。

## 7. `data()` 的尽力转换语义

### 7.1 `data(mimeType)`

```cpp
QByteArray data(const QString &mimeType) const;
```

返回指定 MIME 类型的原始字节。如果对象没有直接保存该格式，Qt 可能尝试做 best-effort 转换。例如请求 `text/plain` 时，已有的文本或 URL 表示可能可以转换成文本。

因此要区分：

```text
hasFormat(type) == true
    -> 对象声明能提供该 MIME 类型

data(type) 返回非空
    -> 这次读取得到了字节，不一定说明原始条目就是该类型
```

如果应用协议要求严格格式匹配，应先检查 `hasFormat()`，再读取并验证字节内容。

### 7.2 空 QByteArray 不一定等于失败

自定义格式可能合法地表示空字节数据。不能只通过：

```cpp
if (mimeData->data(type).isEmpty())
```

判断格式不存在。需要区分不存在和空数据时，使用 `hasFormat()`。

## 8. 惰性自定义数据：重写三个虚函数

当数据很大、生成成本高，或数据只在接收方真正请求时才需要生成，可以派生 `QMimeData`，重写：

```cpp
bool hasFormat(const QString &mimeType) const override;
QStringList formats() const override;
QVariant retrieveData(const QString &mimeType,
                      QMetaType preferredType) const override;
```

三者职责必须一致：

```text
formats() 列出哪些格式
hasFormat() 对这些格式返回 true
retrieveData() 真正提供对应数据
```

示例：

```cpp
class LazyCsvMimeData final : public QMimeData
{
public:
    explicit LazyCsvMimeData(ModelSnapshot snapshot)
        : m_snapshot(std::move(snapshot))
    {
    }

    QStringList formats() const override
    {
        return {QStringLiteral("text/csv")};
    }

    bool hasFormat(const QString &mimeType) const override
    {
        return mimeType == QStringLiteral("text/csv");
    }

protected:
    QVariant retrieveData(const QString &mimeType,
                          QMetaType preferredType) const override
    {
        if (mimeType != QStringLiteral("text/csv"))
            return {};

        const QByteArray bytes = encodeCsv(m_snapshot);
        if (preferredType == QMetaType::fromType<QByteArray>())
            return bytes;
        return QString::fromUtf8(bytes);
    }

private:
    ModelSnapshot m_snapshot;
};
```

`retrieveData()` 可能被 `data()` 和便利 getter 调用。它必须返回与 `preferredType` 兼容的 `QVariant`，不支持的 MIME 类型或类型应返回 null variant。

惰性对象仍然要保存足够的数据让异步拖放期间可以生成结果。不要只保存已经销毁的临时对象指针。

## 9. 应用内自定义子类和 `qobject_cast`

如果拖放只发生在同一个应用内，可以派生自定义 `QMimeData`，直接把高层对象放进子类成员，再在接收端识别：

```cpp
class ProjectMimeData final : public QMimeData
{
public:
    QList<int> selectedIds;
};

void Target::dropEvent(QDropEvent *event)
{
    const auto *data =
        qobject_cast<const ProjectMimeData *>(
            event->mimeData());
    if (data) {
        importProjects(data->selectedIds);
        event->acceptProposedAction();
        return;
    }

    // 也可以继续处理跨应用的标准 MIME 格式。
}
```

这种方式的优点是避免在应用内部重复序列化；代价是它只适用于同一进程中能看到该 C++ 类型的接收端。跨进程或跨应用必须使用真正可传输的 MIME 字节表示。

## 10. 图片、颜色和跨模块 QVariant

### 10.1 `imageData()`

`QMimeData` 属于 Qt Core，而 `QImage` 属于 Qt GUI，因此接口使用 `QVariant`：

```cpp
mimeData->setImageData(QImage("picture.png"));

if (mimeData->hasImage()) {
    const QImage image =
        qvariant_cast<QImage>(mimeData->imageData());
}
```

读取前先检查 `hasImage()`。`imageData()` 返回 null variant 时表示当前对象不能提供图片；不要把任意 `QVariant` 都强制转换成 `QImage`。

### 10.2 `colorData()`

颜色也使用 `QVariant`：

```cpp
mimeData->setColorData(QColor(Qt::red));

if (mimeData->hasColor()) {
    const QColor color =
        qvariant_cast<QColor>(mimeData->colorData());
}
```

`QColor` 属于 Qt GUI，使用该示例时目标需要链接 Qt GUI；`QMimeData` 本身仍属于 Qt Core。

## 11. URL 列表的特殊行为

### 11.1 `setUrls()` 和纯文本降级

```cpp
mimeData->setUrls({
    QUrl::fromLocalFile(QStringLiteral("C:/tmp/a.txt")),
    QUrl(QStringLiteral("https://example.com"))
});
```

URL 对应 `text/uri-list`。Qt 还可能在此前没有显式调用 `setText()` 的情况下，把 URL 导出成纯文本，方便拖入普通文本编辑器。

因此：

- `hasUrls()` 和 `hasText()` 可能同时为 true；
- 如果先调用 `setText()`，纯文本表示会保留调用方明确设置的内容；
- 接收端要按自己的意图选择 `urls()` 或 `text()`，不要假设两者内容完全相同。

### 11.2 不要把 URL 当已验证路径

外部拖放得到的 URL 可能是：

- 本地文件；
- HTTP、FTP 或其他 scheme；
- 不存在或无法访问的路径；
- 带有特殊字符或权限限制的 URL。

导入前应根据业务决定是否只接受 `isLocalFile()`，并重新检查路径和文件类型。

## 12. 清空、替换和移除格式

### 12.1 `clear()`

```cpp
mimeData->clear();
```

清除对象中的所有 MIME 条目。它不会销毁 `QMimeData` 对象本身，也不改变对象的 QObject 父子关系。

清空后：

- `formats()` 应为空；
- 标准 `hasText()`、`hasHtml()`、`hasUrls()` 等应反映没有对应数据；
- 之前从 `data()` 取得的 `QByteArray` 值副本仍可独立使用；
- 惰性子类要确保重写的 `formats()`/`hasFormat()` 不会与自己的缓存状态冲突。

### 12.2 `removeFormat()`

```cpp
mimeData->removeFormat(QStringLiteral("text/html"));
```

移除指定格式的直接数据条目。移除一种表示不一定会清除同一内容的其他表示，例如删除 HTML 后纯文本仍可能存在。

对于自定义惰性子类，如果 `formats()` 和 `hasFormat()` 是重写的，`removeFormat()` 不会自动替你修改子类自己的格式列表；子类应自行设计可变状态。

## 13. 逐项 API 语义

### 13.1 `QMimeData()`

```cpp
QMimeData();
```

构造一个没有 MIME 数据的对象。它不设置 QObject parent，也不自动注册到剪贴板或拖放系统。

### 13.2 `~QMimeData()`

```cpp
virtual ~QMimeData();
```

销毁对象及其内部 MIME 数据。它不负责释放由自定义子类借用的外部对象；外部资源仍按子类自己的所有权设计管理。

### 13.3 `urls() const`

```cpp
QList<QUrl> urls() const;
```

返回 `text/uri-list` 表示的 URL 列表。返回的是列表值，不是内部列表引用。没有 URL 数据时返回空列表。

空列表本身不总能区分“没有 URL 格式”和“存在但列表为空”，需要区分时先调用 `hasUrls()`。

### 13.4 `setUrls(const QList<QUrl> &urls)`

```cpp
void setUrls(const QList<QUrl> &urls);
```

设置 URL 列表。它会把内容作为 `text/uri-list` 表示，并可能提供纯文本降级。

传入的列表按值语义保存；调用方之后修改原列表不会改变已保存的 MIME 数据。URL 是否有效、是否可访问由调用方和接收方负责。

### 13.5 `hasUrls() const`

```cpp
bool hasUrls() const;
```

判断对象能否提供 URL 列表。它是能力查询，不是对每个 URL 可访问性的验证。

### 13.6 `text() const`

```cpp
QString text() const;
```

返回纯文本表示。若没有直接的纯文本数据，Qt 可能尝试从其他内容做尽力转换。没有可转换内容时返回空字符串。

空字符串不等于一定没有文本格式；需要严格区分时使用 `hasText()`。

### 13.7 `setText(const QString &text)`

```cpp
void setText(const QString &text);
```

设置 `text/plain` 表示。空字符串也是合法的纯文本内容，因此：

```cpp
mimeData.setText(QString());
Q_ASSERT(mimeData.hasText());
```

不要用 `text().isEmpty()` 代替 `hasText()`。

### 13.8 `hasText() const`

```cpp
bool hasText() const;
```

判断对象能否提供纯文本表示。它返回 true 时，`text()` 应按文本接口读取；内容是否为空仍由文本本身决定。

### 13.9 `html() const`

```cpp
QString html() const;
```

返回 `text/html` 表示。没有 HTML 时返回空字符串。空 HTML 与没有 HTML 需要用 `hasHtml()` 区分。

### 13.10 `setHtml(const QString &html)`

```cpp
void setHtml(const QString &html);
```

设置 HTML 表示。它不会自动生成等价的纯文本 `text/plain`；如果接收端可能只理解纯文本，应同时调用 `setText()` 提供降级表示。

### 13.11 `hasHtml() const`

```cpp
bool hasHtml() const;
```

判断对象能否提供 HTML 表示。它不验证 HTML 语法，也不代表内容可信。

### 13.12 `imageData() const`

```cpp
QVariant imageData() const;
```

返回图片数据的 `QVariant` 表示。没有图片时返回 null variant。调用方通常使用 `qvariant_cast<QImage>()` 转回 GUI 类型。

### 13.13 `setImageData(const QVariant &image)`

```cpp
void setImageData(const QVariant &image);
```

设置图片表示。常见传入值是 `QImage`；接口使用 `QVariant` 是因为 `QMimeData` 位于 Core，不直接依赖 GUI 类型。

### 13.14 `hasImage() const`

```cpp
bool hasImage() const;
```

判断对象能否提供图片。它不保证图片格式、尺寸或像素内容符合接收方要求。

### 13.15 `colorData() const`

```cpp
QVariant colorData() const;
```

返回 `application/x-color` 表示的颜色数据。没有颜色时返回 null variant。

### 13.16 `setColorData(const QVariant &color)`

```cpp
void setColorData(const QVariant &color);
```

设置颜色表示。常见传入值是 `QColor`。跨应用传输时，接收方仍需确认平台和应用是否理解该非通用 MIME 类型。

### 13.17 `hasColor() const`

```cpp
bool hasColor() const;
```

判断对象能否提供颜色。它不验证颜色值是否符合业务范围。

### 13.18 `data(const QString &mimeType) const`

```cpp
QByteArray data(const QString &mimeType) const;
```

读取指定 MIME 类型的字节。直接存储的自定义数据通常通过该函数得到；如果没有直接条目，Qt 可能进行尽力转换。

需要严格协议时：

```cpp
const QString type = QStringLiteral("application/x-record");
if (!mimeData->hasFormat(type))
    return;

const QByteArray bytes = mimeData->data(type);
```

### 13.19 `setData(const QString &, const QByteArray &)`

```cpp
void setData(const QString &mimeType,
             const QByteArray &data);
```

为指定 MIME 类型保存字节表示。`mimeType` 应使用完整、稳定且符合 MIME 约定的名称；数据编码由应用协议定义。

如果自定义数据要用于 Qt item view 的拖放，跨进程或跨应用时应使用可传输的字节格式。只在同一进程内传递 C++ 对象时，可以考虑自定义 `QMimeData` 子类和 `qobject_cast()`。

### 13.20 `removeFormat(const QString &)`

```cpp
void removeFormat(const QString &mimeType);
```

移除指定 MIME 类型的数据条目。它不保证清除其他等价表示，也不改变对象的 QObject 生命周期。

### 13.21 `hasFormat(const QString &) const`

```cpp
virtual bool hasFormat(const QString &mimeType) const;
```

判断对象能否提供指定 MIME 类型。普通 `QMimeData` 根据内部数据条目回答；惰性子类应重写它，使答案与 `formats()` 和 `retrieveData()` 一致。

### 13.22 `formats() const`

```cpp
virtual QStringList formats() const;
```

返回对象支持的 MIME 类型列表，通常按优先级排列。惰性子类重写时要列出所有真正可以由 `retrieveData()` 提供的格式。

列表是值返回，不是对内部格式表的可写引用。

### 13.23 `clear()`

```cpp
void clear();
```

移除所有 MIME 数据条目。不会销毁对象或改变其 parent。

### 13.24 `retrieveData(const QString &, QMetaType) const`

```cpp
virtual QVariant retrieveData(
    const QString &mimeType,
    QMetaType preferredType) const;
```

受保护的惰性数据扩展点。`data()` 和便利 getter 会通过它请求指定 MIME 类型的表示。

重写时：

- 对支持的 MIME 类型生成对应数据；
- 尽量返回与 `preferredType` 兼容的 `QVariant`；
- 对不支持的 MIME 类型或类型返回 null variant；
- 不要返回指向临时内存的裸指针；
- 不要在 getter 中修改逻辑上 const 的对象状态，除非缓存设计明确且线程安全。

## 14. 常见错误

### 14.1 把 `QMimeData` 交给 Qt 后又手动删除

**问题：** 拖放或剪贴板使用期间崩溃或 double free。

**原因：** 接收 API 通常接管传入对象的所有权。

**处理：** 交给 `QDrag`/`QClipboard` 后不再手动删除，并明确对象生命周期。

### 14.2 只用 `isEmpty()` 判断格式存在

**问题：** 空文本或空字节数据被误判为没有格式。

**原因：** 合法数据可以为空。

**处理：** 使用 `hasText()`、`hasFormat()` 等能力查询，再读取内容。

### 14.3 只设置 HTML，不提供纯文本降级

**问题：** 纯文本编辑器粘贴不到预期内容。

**原因：** 接收方只理解 `text/plain`。

**处理：** 同时设置 `setHtml()` 和 `setText()`。

### 14.4 只检查 `hasUrls()` 就把 URL 当本地文件

**问题：** 对远程 URL 直接调用本地文件 API。

**原因：** `text/uri-list` 可以包含不同 scheme。

**处理：** 检查 `url.isLocalFile()`、路径存在性和权限。

### 14.5 依赖 `formats().first()` 作为安全格式

**问题：** 选择了不适合当前业务的高优先级格式。

**原因：** 优先级表示发送方偏好，不等于接收方安全策略。

**处理：** 在自己支持的格式集合中按业务顺序选择，并验证数据。

### 14.6 惰性子类只重写 `retrieveData()`

**问题：** `hasFormat()` 返回 false，接收方根本不会请求数据。

**原因：** 三个虚函数没有形成一致协议。

**处理：** 一起重写 `formats()`、`hasFormat()` 和 `retrieveData()`。

### 14.7 试图把自定义 MIME 名称当作数据校验

**问题：** 解析外部字节时越界或接受恶意内容。

**原因：** MIME 类型只标识格式，不验证 payload。

**处理：** 对版本、长度、编码和字段范围做完整验证。

### 14.8 把应用内子类数据当跨进程协议

**问题：** 另一个应用或进程无法通过 `qobject_cast()` 取得自定义数据。

**原因：** C++ 子类对象只存在于当前进程地址空间。

**处理：** 跨进程使用 `setData()` 保存可解析字节，或提供标准 MIME 表示。

## API 速查表
### 15.1 标准数据

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMimeData()` | 创建空 MIME 数据对象 | 默认没有数据和 parent |
| `~QMimeData()` | 销毁对象 | 交给 Qt 管理后不要重复删除 |
| `urls()` | 读取 URL 列表 | 空列表不等于没有 URL 格式；先看 `hasUrls()` |
| `setUrls()` | 设置 `text/uri-list` | 可能自动提供纯文本降级 |
| `hasUrls()` | 查询 URL 能力 | 不验证 scheme、路径和权限 |
| `text()` | 读取纯文本 | 可能尽力转换；空字符串不代表格式不存在 |
| `setText()` | 设置 `text/plain` | 空文本仍可能是合法格式 |
| `hasText()` | 查询纯文本能力 | 与文本是否为空分开判断 |
| `html()` | 读取 HTML | 空 HTML 要用 `hasHtml()` 区分 |
| `setHtml()` | 设置 `text/html` | 不自动保证有纯文本降级 |
| `hasHtml()` | 查询 HTML 能力 | 不验证 HTML 语法和可信度 |
| `imageData()` | 读取图片 QVariant | 常用 `qvariant_cast<QImage>()` |
| `setImageData()` | 设置图片表示 | Core API 用 QVariant 承载 GUI 图片 |
| `hasImage()` | 查询图片能力 | 不保证格式、尺寸或像素符合业务要求 |
| `colorData()` | 读取颜色 QVariant | 常用 `qvariant_cast<QColor>()` |
| `setColorData()` | 设置颜色表示 | `application/x-color` 的互操作性有限 |
| `hasColor()` | 查询颜色能力 | 不验证颜色业务范围 |

### 15.2 任意 MIME 数据

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `data(mimeType)` | 读取指定格式字节 | 可能发生尽力转换；严格协议先检查 `hasFormat()` |
| `setData(mimeType, data)` | 保存指定格式字节 | 编码、版本、字节序由应用协议定义 |
| `removeFormat(mimeType)` | 移除一个格式 | 不一定清除其他表示 |
| `hasFormat(mimeType)` | 查询格式能力 | 惰性子类要与 `formats()`/`retrieveData()` 一致 |
| `formats()` | 返回支持格式和优先级 | 发送方优先级不等于接收方安全策略 |
| `clear()` | 清除全部 MIME 条目 | 不销毁对象，不改变 QObject parent |

### 15.3 扩展和协作

| API/类型 | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `retrieveData(mimeType, preferredType)` | 惰性生成自定义格式 | 与 `hasFormat()`、`formats()` 成套重写 |
| `QClipboard::setMimeData()` | 把 MIME 数据交给剪贴板 | 通常转移对象所有权；适合异步使用 |
| `QDrag::setMimeData()` | 把 MIME 数据交给拖放对象 | 通常转移对象所有权；不要再手动 delete |
| `QDropEvent::mimeData()` | 取得接收到的 MIME 数据 | 数据来自外部时要验证并选择可信格式 |
| `qobject_cast<CustomMimeData *>` | 应用内识别自定义子类 | 只适用于同一进程中的 C++ 类型 |

## 16. 一句话总结

`QMimeData` 是剪贴板和拖放使用的多格式 MIME 数据容器：它可以同时提供文本、HTML、URL、图片、颜色和自定义字节表示，`formats()` 表达发送方的格式优先级，`hasFormat()` 表达可用能力，`data()` 可能做尽力转换。使用时先分清对象所有权和格式存在性，再验证外部 payload；需要惰性数据时必须让 `formats()`、`hasFormat()` 和 `retrieveData()` 三者保持一致。
