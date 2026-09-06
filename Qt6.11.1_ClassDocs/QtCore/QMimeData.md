# QMimeData

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMimeData` 是 Qt 的值类型，围绕“Mime数据”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMimeData` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QMimeData>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QMimeData()`
- `virtual ~QMimeData()`
- `void clear()`
- `QVariant colorData() const`
- `QByteArray data(const QString &mimeType) const`
- `virtual QStringList formats() const`
- `bool hasColor() const`
- `virtual bool hasFormat(const QString &mimeType) const`
- `bool hasHtml() const`
- `bool hasImage() const`
- `bool hasText() const`
- `bool hasUrls() const`
- `QString html() const`
- `QVariant imageData() const`
- `void removeFormat(const QString &mimeType)`
- `void setColorData(const QVariant &color)`
- `void setData(const QString &mimeType, const QByteArray &data)`
- `void setHtml(const QString &html)`
- `void setImageData(const QVariant &image)`
- `void setText(const QString &text)`
- `void setUrls(const QList<QUrl> &urls)`
- `QString text() const`
- `QList<QUrl> urls() const`

### 保护函数

- `virtual QVariant retrieveData(const QString &mimeType, QMetaType type) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMimeData::QMimeData()`

**作用与语义：**

构建一个新的MIME数据对象，但该对象中没有任何数据。

### `[virtual noexcept] QMimeData::~QMimeData()`

**作用与语义：**

销毁MIME数据对象。

### `void QMimeData::clear()`

**作用与语义：**

移除对象中所有 MIME 类型和数据条目。

### `QVariant QMimeData::colorData() const`

**作用与语义：**

如果对象中存储的数据代表颜色（MIME类型`application/x-color`），则返回颜色;否则返回空变体。
使用`QVariant`是因为`QMimeData`属于Qt核心模块，而`QColor`属于Qt GUI。要将`QVariant`转换为`QColor`，只需使用`qvariant_cast()`。例如：

**官方示例：**

```cpp
 if (event->mimeData()->hasColor()) {
     QColor color = qvariant_cast<QColor>(event->mimeData()->colorData());
     //...
 }
```

### `QByteArray QMimeData::data(const QString &mimeType) const`

**作用与语义：**

返回以`mimeType`指定MIME类型描述格式存储在对象中的数据。如果该对象不包含`mimeType` MIME类型的数据（见 `hasFormat()`），该函数可能会对该类型进行尽力转换。

### `[virtual] QStringList QMimeData::formats() const`

**作用与语义：**

返回对象支持的格式列表。这是对象可以返回合适数据的MIME类型列表。列表中的格式按优先级排序。
对于最常见的数据类型，你可以调用更高层次的函数 `hasText()`、`hasHtml()`、`hasUrls()`、`hasImage()` 和 `hasColor()`。

### `bool QMimeData::hasColor() const`

**作用与语义：**

如果对象能返回颜色（MIME类型`application/x-color`），则返回`true`;否则返回 `false`。

### `[virtual] bool QMimeData::hasFormat(const QString &mimeType) const`

**作用与语义：**

如果对象能够返回`mimeType`指定的MIME类型数据，则返回`true`;否则返回`false`。
对于最常见的数据类型，你可以调用更高层次的函数 `hasText()`、`hasHtml()`、`hasUrls()`、`hasImage()` 和 `hasColor()`。

### `bool QMimeData::hasHtml() const`

**作用与语义：**

如果对象可以返回 HTML（MIME 类型 `text/html`），则返回 `true`；否则返回 `false`。

### `bool QMimeData::hasImage() const`

**作用与语义：**

如果对象能够返回图像，则返回`true`;否则返回假。

### `bool QMimeData::hasText() const`

**作用与语义：**

如果对象能够返回纯文本（MIME类型`text/plain`），则返回`true`;否则返回`false`。

### `bool QMimeData::hasUrls() const`

**作用与语义：**

如果对象能够返回 URL 列表，返回`true`;否则返回 `false`。
URL对应MIME类型`text/uri-list`。

### `QString QMimeData::html() const`

**作用与语义：**

如果对象中存储的数据是 HTML（MIME 类型 `text/html`），则返回字符串;否则返回空字符串。

### `QVariant QMimeData::imageData() const`

**作用与语义：**

如果对象能够返回图像，则返回存储`QImage`的`QVariant`;否则返回空变体。
使用`QVariant`是因为`QMimeData`属于Qt核心模块，而`QImage`属于Qt图形界面。要将`QVariant`转换为`QImage`，只需使用`qvariant_cast()`。例如：

**官方示例：**

```cpp
 if (event->mimeData()->hasImage()) {
     QImage image = qvariant_cast<QImage>(event->mimeData()->imageData());
     //...
 }
```

### `void QMimeData::removeFormat(const QString &mimeType)`

**作用与语义：**

移除了对象中`mimeType`的数据条目。

### `[virtual protected] QVariant QMimeData::retrieveData(const QString &mimeType, QMetaType type) const`

**作用与语义：**

返回包含`mimeType`指定MIME类型数据的给定`type`变体。如果对象不支持MIME类型或变体类型，则返回空变体。
这个函数由通用`data()` getter 调用，方便 getter（`text()`、`html()`、`urls()`、`imageData()` 和 `colorData()`）。如果你想用自定义数据结构存储数据（而不是 `setData()` 提供的 `QByteArray`），可以重新实现它。你还需要重新实现 `hasFormat()` 和 `formats()`。

### `void QMimeData::setColorData(const QVariant &color)`

**作用与语义：**

将对象中的颜色数据设置为给定的`color`。
颜色对应MIME类型`application/x-color`。

### `void QMimeData::setData(const QString &mimeType, const QByteArray &data)`

**作用与语义：**

将`mimeType`给出的MIME类型关联到指定`data`。
对于最常见的数据类型，你可以调用更高层次的函数 `setText()`、`setHtml()`、`setUrls()`、`setImageData()` 和 `setColorData()`。
注意，如果你想在项目视图拖放操作中使用自定义数据类型，必须将其注册为 Qt 元类型，使用 `Q_DECLARE_METATYPE()` 宏，并实现流操作符。

### `void QMimeData::setHtml(const QString &html)`

**作用与语义：**

将`html`设置为用于表示数据的 HTML（MIME 类型 `text/html`）。

### `void QMimeData::setImageData(const QVariant &image)`

**作用与语义：**

将对象中的数据设置为给定的`image`。
使用`QVariant`是因为`QMimeData`属于Qt核心模块，而`QImage`属于Qt图形界面。从`QImage`转换为`QVariant`Gui是隐含的。例如：

**官方示例：**

```cpp
 mimeData->setImageData(QImage("beautifulfjord.png"));
```

### `void QMimeData::setText(const QString &text)`

**作用与语义：**

将`text`设置为用于表示数据的纯文本（MIME类型`text/plain`）。

### `void QMimeData::setUrls(const QList<QUrl> &urls)`

**作用与语义：**

将存储在MIME数据对象中的URL设置为`urls`指定的URL。
URL对应MIME类型`text/uri-list`。
自 Qt 5.0 起，setUrls 还会将 URL 导出为纯文本，如果之前未调用 `setText`，便于将它们放入任意 lineedit 和文本编辑器中。

### `QString QMimeData::text() const`

**作用与语义：**

如果该对象包含纯文本，则返回数据的纯文本（MIME类型`text/plain`）表示。如果包含其他内容，该函数会尽力将其转换为纯文本。

### `QList<QUrl> QMimeData::urls() const`

**作用与语义：**

返回包含在MIME数据对象内的URL列表。
URL对应于MIME类型`text/uri-list`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMimeData` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
