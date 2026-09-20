# QClipboard：在应用与系统之间交换 MIME 数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QClipboard>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QObject`，但由 `QGuiApplication` 管理

## 它解决什么问题

`QClipboard` 提供应用间复制和粘贴的数据通道。它不只支持文本，也可传递图像、pixmap、HTML、URL 和任意 `QMimeData` 格式，使用模型与拖放数据类似。

每个应用只有一个剪贴板对象，应通过 `QGuiApplication::clipboard()` 取得。构造函数和析构函数不是公共 API，应用既不应 `new QClipboard`，也不应删除返回指针。

```cpp
QClipboard *clipboard = QGuiApplication::clipboard();
clipboard->setText(selectedText);

const QString pastedText = clipboard->text();
```

## 三种模式与平台支持

`Mode` 选择操作系统剪贴板的哪一部分：

| 模式 | 含义 | 常见平台 |
| --- | --- | --- |
| `Clipboard` | 全局复制粘贴板。 | 所有支持剪贴板的平台。 |
| `Selection` | 全局鼠标选区。 | 具有全局选择概念的平台，例如 X11。 |
| `FindBuffer` | 当前查找字符串缓冲。 | macOS。 |

不要因为枚举存在就假定平台支持。调用 `supportsSelection()` 和 `supportsFindBuffer()` 后再访问相应模式；不支持的模式上 `mimeData()` 可返回 `nullptr`。

Windows 和 macOS 不支持全局鼠标选区，只有显式复制或剪切才写入全局剪贴板。macOS 的查找缓冲则独立于普通剪贴板。

## 简单数据与 MIME 数据

`setText()` 写入纯文本，`setImage()` 写入 `QImage`，`setPixmap()` 写入 pixmap。读取端对应 `text()`、`image()`、`pixmap()`。

需要同时提供纯文本和 HTML、内部对象数据或文件 URL 时，应直接使用 `QMimeData`：

```cpp
auto *mime = new QMimeData;
mime->setText(plainText);
mime->setHtml(htmlText);
mime->setData("application/x-myapp-items", serializedItems);

QGuiApplication::clipboard()->setMimeData(mime);
// 此后 mime 的所有权属于剪贴板，不要 delete 或继续修改它。
```

`setMimeData()` 会转移 `QMimeData` 的所有权给剪贴板。要替换或清除内容，调用 `setMimeData()` 传入新的对象或调用 `clear()`，不能手工删除已经交出去的指针。

`mimeData()` 返回的 `const QMimeData *` 不转移所有权，而且任何剪贴板内容变化都可能使它失效，包括本应用 setter 调用和系统中其他应用的写入。应在当前代码段内立即读取或复制需要的数据，不要缓存指针。

## 读取策略与格式选择

粘贴端最好以 `mimeData()` 的能力检测为中心：

```cpp
const QMimeData *mime = QGuiApplication::clipboard()->mimeData();
if (mime && mime->hasHtml()) {
    insertHtml(mime->html());
} else if (mime && mime->hasText()) {
    insertPlainText(mime->text());
}
```

`text()` 只返回纯文本，不含文本时返回空字符串。带 `QString &subtype` 的重载可请求或接收实际文本子类型，常见值是 `"plain"` 和 `"html"`；若初始 `subtype` 为空，可接受任意可用子类型，函数会把选中的类型写回。

不要在每次按键或定时器回调中反复调用这个文本子类型重载，它可能较慢。需要追踪变更时，监听 `dataChanged()` 或更通用的 `changed(Mode)`。

## 图像和 pixmap 的区别

`image()` 在没有图像或格式不受支持时返回 null `QImage`。`pixmap()` 在没有 pixmap 时返回 null `QPixmap`，并且可能丢失信息，例如显示深度降低或 alpha 被转成 mask。

写入时 `setPixmap()` 比 `setImage()` 更慢，因为前者需要先将 `QPixmap` 转成 `QImage`。处理、存储或跨线程准备剪贴板图像时优先使用 `QImage`，仅在 UI 侧确有 pixmap 时才使用 `setPixmap()`。

## 信号、所有权和事件循环

`changed(Mode)` 是统一的变更信号，能告诉你哪个模式变了。`dataChanged()` 对普通 `Clipboard`，`selectionChanged()` 对鼠标选区，`findBufferChanged()` 对 macOS 查找缓冲。

`ownsClipboard()`、`ownsSelection()` 和 `ownsFindBuffer()` 只报告当前 Qt 剪贴板对象是否拥有对应数据。它们不是“数据是否有效”的判断，也不应替代 `supports*()`。

在 X11 上，剪贴板是事件驱动的：事件循环不运行时功能不会正常工作。Qt 文档还建议在鼠标或键盘等用户输入事件的直接响应中读写剪贴板，而不是在定时器或无用户输入的事件中持续轮询。X11 的 Selection 所有权变更不会广播给所有应用，不能假定每个外部变化都会触发本进程的通知。

macOS 上，其他应用造成的剪贴板或查找缓冲变更，可能要等本应用再次激活才会被检测到。Android 仅支持 `text/plain`、`text/html` 与 `text/uri-list` 三种 MIME 类型。

剪贴板与 GUI 平台交互，应从 GUI 线程访问。后台线程准备的数据可通过信号交回 GUI 线程后再写入。

## 常见误区

- 自己构造或销毁 `QClipboard`，而不是使用 `QGuiApplication::clipboard()`。
- `setMimeData()` 后继续持有并删除 `QMimeData`。
- 缓存 `mimeData()` 返回的裸指针，跨越一次剪贴板变更后继续访问。
- 不检查 `supportsSelection()` 就假定 `Selection` 在 Windows 或 macOS 可用。
- 使用 `pixmap()` 作为无损图像读取接口，忽略可能的颜色深度与 alpha 信息损失。
- 在 X11 的定时器里频繁读写剪贴板，或未运行事件循环就期待它正常工作。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `Mode::Clipboard` | 全局剪贴板模式。 | 默认模式，跨平台最可靠。 |
| `Mode::Selection` | 全局鼠标选区模式。 | 先用 `supportsSelection()` 检查，Windows 和 macOS 不支持。 |
| `Mode::FindBuffer` | 查找字符串缓冲模式。 | 主要用于 macOS，先用 `supportsFindBuffer()` 检查。 |
| `void clear(Mode mode = Clipboard)` | 清空指定剪贴板区域。 | 根据 mode 清除全局板、选区或查找缓冲。 |
| `bool supportsSelection() const` | 查询是否支持全局鼠标选区。 | 访问 `Selection` 前先检查。 |
| `bool supportsFindBuffer() const` | 查询是否支持独立查找缓冲。 | 访问 `FindBuffer` 前先检查。 |
| `bool ownsClipboard() const` | 查询是否拥有全局剪贴板数据。 | 不表示数据永久有效。 |
| `bool ownsSelection() const` | 查询是否拥有鼠标选区数据。 | 平台不支持选区时不能据此判断能力。 |
| `bool ownsFindBuffer() const` | 查询是否拥有查找缓冲数据。 | 应与 `supportsFindBuffer()` 配合。 |
| `void setText(const QString &text, Mode mode = Clipboard)` | 将纯文本复制到指定模式。 | 不提供 HTML 或自定义 MIME 格式。 |
| `QString text(Mode mode = Clipboard) const` | 读取纯文本。 | 没有文本时返回空字符串。 |
| `QString text(QString &subtype, Mode mode = Clipboard) const` | 读取指定或协商子类型的文本。 | 常见 subtype 为 `"plain"`、`"html"`；频繁调用可能慢。 |
| `void setImage(const QImage &image, Mode mode = Clipboard)` | 将图像复制到指定模式。 | 是 `QMimeData::setImageData()` 的便捷封装。 |
| `QImage image(Mode mode = Clipboard) const` | 读取图像。 | 无图像或格式不支持时返回 null image。 |
| `void setPixmap(const QPixmap &pixmap, Mode mode = Clipboard)` | 将 pixmap 复制到指定模式。 | 比 `setImage()` 慢，内部需要转换。 |
| `QPixmap pixmap(Mode mode = Clipboard) const` | 读取 pixmap。 | 可能丢失深度或 alpha 信息。 |
| `void setMimeData(QMimeData *data, Mode mode = Clipboard)` | 写入任意 MIME 数据。 | 所有权转移给剪贴板，调用后不能删除该对象。 |
| `const QMimeData *mimeData(Mode mode = Clipboard) const` | 取得当前 MIME 数据表示。 | 不转移所有权；内容变化后指针可能立刻失效。 |
| `void changed(QClipboard::Mode mode)` | 任一模式数据变化时发出。 | 首选的统一监听信号。 |
| `void dataChanged()` | 普通剪贴板变化时发出。 | macOS 外部变更可能等应用激活后才被发现。 |
| `void selectionChanged()` | 鼠标选区变化时发出。 | 仅支持全局选区的平台有意义。 |
| `void findBufferChanged()` | 查找缓冲变化时发出。 | 只适用于 macOS。 |
