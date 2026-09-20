# QClipboard

> Qt 6.11.1 · Qt GUI · 来自 `QClipboard`

## 1. 先建立直觉

`QClipboard` 是 Qt 对系统剪贴板的访问入口。它不只保存文本，也可以保存图片、pixmap、HTML、URL、自定义 MIME 数据。

剪贴板属于桌面环境资源，不是你应用内部的普通变量。数据可能被其他应用替换，平台还可能支持 Selection、FindBuffer 这类额外模式。

## 2. 类说明

`QClipboard` 继承自 `QObject`，通常通过 `QGuiApplication::clipboard()` 获取。不要自己 new 一个剪贴板对象。

它围绕 `QMimeData` 工作：`setText()`、`setImage()`、`setPixmap()` 是便利函数；复杂数据使用 `setMimeData()`。读取时要先判断 MIME 能力，再取对应格式。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGuiApplication::clipboard()` | 获取应用的剪贴板对象。 |
| `setText()` / `text()` | 写入或读取文本。 |
| `setImage()` / `image()` | 写入或读取图像。 |
| `setPixmap()` / `pixmap()` | 写入或读取 pixmap。 |
| `setMimeData(QMimeData *)` | 写入复杂 MIME 数据；剪贴板接管所有权。 |
| `mimeData()` | 读取当前 MIME 数据。 |
| `clear()` | 清空指定剪贴板模式。 |
| `supportsSelection()` | 当前平台是否支持鼠标选择剪贴板。 |
| `supportsFindBuffer()` | 当前平台是否支持查找缓冲区。 |
| `ownsClipboard()` / `ownsSelection()` / `ownsFindBuffer()` | 判断数据是否由本应用提供。 |
| `changed(mode)` | 任意模式变化时发出。 |
| `dataChanged()` | 普通 clipboard 变化时发出。 |
| `selectionChanged()` | selection 模式变化时发出。 |
| `findBufferChanged()` | find buffer 变化时发出。 |

## 4. 关键用法

```cpp
auto *clipboard = QGuiApplication::clipboard();
clipboard->setText(editor->selectedText());
```

写入多格式数据：

```cpp
auto *data = new QMimeData;
data->setText("https://example.com");
data->setUrls({ QUrl("https://example.com") });
QGuiApplication::clipboard()->setMimeData(data);
```

读取前判断：

```cpp
const QMimeData *data = clipboard->mimeData();
if (data->hasImage())
    pasteImage(qvariant_cast<QImage>(data->imageData()));
```

## 5. 使用场景

适合复制/粘贴文本、图片、富文本、文件 URL、自定义对象引用、跨应用数据交换、编辑器剪贴板集成。

如果只是应用内部拖动或复制对象，内部命令模型可能更可靠；剪贴板适合用户明确要跨位置/跨应用传递数据。

## 6. 常见坑与经验
`Selection` 只在部分平台可用，典型如 X11。使用前检查 `supportsSelection()`。

`setMimeData()` 后剪贴板拥有对象，不要再手动删除。

剪贴板内容随时可能被外部应用替换。粘贴时永远按当前 MIME 数据判断，不要缓存旧假设。
