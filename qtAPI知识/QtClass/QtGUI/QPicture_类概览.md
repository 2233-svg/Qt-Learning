# QPicture：记录并重放 QPainter 命令的 Qt 元文件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPicture>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 基类：`QPaintDevice`  
> 相关类型：`QPainter`、`QDataStream`、`QIODevice`

`QPicture` 是一种 `QPaintDevice`，不会立即把图元画到屏幕或位图，而是记录 `QPainter` 命令。之后可通过 `play()` 或 `QPainter::drawPicture()` 在另一个绘制目标上重放这些命令。

它类似 Qt 自己的元文件：记录的是画笔、字体、图像、裁剪、变换等 painter 命令，采用 Qt 专有二进制格式。它适合应用内的延迟重放、WYSIWYG 预览或临时命令录制；不适合作为公开、长期、跨语言的图形交换格式。需要标准矢量文件时选择 SVG、PDF 或自己定义稳定格式。

## 它解决的问题

有时要先记录“画什么”，再决定“画到哪里”：

- 同一张报表既画到窗口预览，也画到打印机；
- 绘制过程复杂，希望缓存 painter 命令而不是最终位图；
- 需要延迟重放一组已生成的图元；
- 想把可重放的 Qt 绘制记录暂存到文件或 `QIODevice`。

`QPicture` 将这一组 `QPainter` 调用录制成平台无关的 Qt 二进制命令流。重放时，Qt 会根据目标设备的分辨率进行缩放，使结果在屏幕、打印机等设备上保持相近的视觉尺寸。

## 实际使用场景

### 1. 录制并在内存图像上重放

```cpp
QPicture picture;
{
    QPainter recorder(&picture);
    recorder.setPen(QPen(Qt::darkBlue, 2));
    recorder.setBrush(Qt::cyan);
    recorder.drawEllipse(QRectF(10, 20, 80, 70));
} // 结束录制

QImage preview(QSize(400, 300), QImage::Format_ARGB32_Premultiplied);
preview.fill(Qt::white);

QPainter painter(&preview);
painter.drawPicture(0, 0, picture);
```

在 `QPicture` 上开始一次新的 painter 绘制会重置之前记录的命令，所以录制应有清晰的开始和结束边界。

### 2. 保存和加载应用内部绘制记录

```cpp
if (!picture.save(QStringLiteral("preview.pic"))) {
    // 处理写入失败
}

QPicture loaded;
if (!loaded.load(QStringLiteral("preview.pic"))) {
    // loaded 已失效，不能继续重放
}
```

`.pic` 内容是 Qt 专有二进制数据。它适合由同一应用或受控 Qt 环境产生和读取，不能当成 SVG、PDF 或通用图像资源格式发布。

### 3. 在已有 painter 上直接播放

```cpp
QPainter painter(targetDevice);
painter.translate(20, 20);

if (!picture.play(&painter)) {
    // 处理重放失败
}
```

`play(&painter)` 等价于在坐标 `(0, 0)` 调用 `painter.drawPicture(...)`。要控制重放位置、缩放或裁剪，通常先设置 painter 的变换和裁剪，再播放 picture。

## 核心模型与边界

### 它记录命令，不是像素快照

`QPicture` 保存的是 `QPainter` 命令及其相关状态，不是已光栅化的位图。这带来两个结果：

- 可以在不同目标设备上重放，并根据 DPI 进行合适缩放；
- 文件内容依赖 Qt 的绘制与序列化实现，不是面向第三方渲染器的通用图形格式。

若目标是“固定像素结果”，使用 `QImage`；若目标是“可被外部工具编辑/显示的标准矢量文件”，使用 `QSvgGenerator` 或 PDF 输出。

### 录制会覆盖旧命令

Qt 文档规定，每次对 `QPicture` 调用 `QPainter::begin()` 开始录制时，已有命令列表会被重置：

```cpp
QPicture picture;

QPainter first(&picture);
first.drawRect(0, 0, 10, 10);
first.end();

QPainter second(&picture); // 开始新的录制，之前内容被重置
second.drawEllipse(0, 0, 10, 10);
```

不要把同一 `QPicture` 当作可通过多次 `begin()` 追加的命令日志。需要组合内容时，在同一次 painter 会话中完成绘制，或建立多个 picture 再按顺序重放。

### 分辨率独立不等于任意环境完全一致

`QPicture` 以默认系统 DPI 录制，并在重放时根据目标分辨率缩放 painter。它适合维持相近的视觉输出，但字体可用性、平台字体渲染、外部 pixmap 资源和目标引擎能力仍会影响最终观感。

不要把“resolution independent”理解为跨平台逐像素一致，也不要把它当作印刷生产的最终交换格式。

### 隐式共享与修改分离

`QPicture` 是隐式共享值类型。复制构造和复制赋值通常很快，副本会共享底层数据；对任一副本进行修改、重新录制、`setData()` 等操作时会按需分离。

这适合把同一录制结果按值传给多个预览或绘制函数。但每个副本仍可能保存大量二进制命令，修改时的分离成本应在大图片缓存场景中评估。

### 数据指针的有效期

`data()` 返回内部 picture 二进制数据指针：

```cpp
const char *bytes = picture.data();
const uint byteCount = picture.size();
```

该指针只在下一次对同一 `QPicture` 调用**非 const**成员函数之前有效；空 picture 返回空指针。若需在之后使用或跨线程传递，立即复制到自己的 `QByteArray`。

`setData(data, size)` 会复制输入数据，不会借用调用者的缓冲区。

### 文件与网络输入是不可信数据边界

`QPicture` 的保存/加载基于 `QDataStream`。Qt 文档明确要求遵循 `QDataStream` 读取不可信数据时的安全限制：对外部文件、网络输入或用户上传内容要设置长度、大小和资源使用限制，并将解析放在受控错误处理路径中。

不要因为 `.pic` 是 Qt 格式就直接信任它，也不要把来自不可信来源的数据直接交给 `setData()` 后立即重放。

### `formatVersion` 的兼容含义

`QPicture(int formatVersion = -1)` 中：

- `-1` 表示当前 Qt 版本使用的默认格式；
- 指定格式版本可用于生成面向较早 Qt 应用可读取的 picture。

它是 Qt 内部格式兼容工具，不是长期文件格式版本策略。跨 Qt 大版本、长期存档或第三方互操作时，应优先选择明确稳定的公开格式。

### 线程与生命周期

`QPicture` 是记录数据的值类型，但它仍继承 `QPaintDevice`，录制和播放会与 `QPainter` 及目标设备协作。若目标是窗口、`QPixmap`、打印机等 GUI / 平台资源，应遵守对应对象的线程限制。

可将完整录制完成、且不再修改的 picture 按值传递给后台任务做纯数据管理；实际播放到 GUI 资源时回到其所属线程。不要在同一个 picture 被一个 painter 录制时同时从另一线程 `save()`、`data()` 或 `play()`。

## 关键 API 语义

### 录制和播放

```cpp
QPicture picture;
QPainter recorder(&picture);
drawReport(recorder);
recorder.end();

QPainter destination(&image);
picture.play(&destination);
```

`play()` 在给定 painter 上重放命令，并以布尔值报告是否成功。`QPainter::drawPicture()` 更适合需要指定位置或与其他 `QPainter` 绘制代码自然组合的场景。

### 自定义包围盒

`boundingRect()` 对含数据的 picture 返回自动计算的包围矩形；没有数据时返回无效矩形。`setBoundingRect()` 可以覆盖自动值：

```cpp
picture.setBoundingRect(QRect(0, 0, 200, 100));
```

仅在你确实知道自动推导不足、并且能保证覆盖所有重放内容时才覆盖。错误包围盒会导致布局、缓存裁剪或命中范围估算错误。

### 二进制导入导出

```cpp
QByteArray bytes(picture.data(), picture.size());

QPicture restored;
restored.setData(bytes.constData(), bytes.size());
```

这里 `QByteArray` 拷贝了内部数据，因此之后可安全修改或销毁原 picture。调用 `setData()` 后仍要通过 `isNull()`、`boundingRect()` 或受控 `play()` 验证数据是否可用。

## 常见错误

### 用 QPicture 作为通用文件格式

它是 Qt 专有二进制元文件，外部浏览器、办公软件和普通矢量工具通常不能读取。对外导出选 SVG、PDF、PNG/WebP 等合适格式。

### 多次 `QPainter::begin(&picture)` 期待追加内容

新录制会重置旧命令。需要累积绘制时只开始一次 recorder，或自己组织多个 picture 的重放顺序。

### 缓存 `data()` 指针

非 const 调用会使指针失效。传输、异步保存或网络发送前必须复制字节。

### `load()` 失败后继续使用旧内容

文件名重载加载失败会使 picture 无效。检查返回值，失败后不要继续 `play()` 或假定旧命令仍存在。

### 从不可信来源直接重放

二进制解析和重放可能消耗大量内存或绘制资源。先限制输入、检查读取结果，并在受控环境中处理外部数据。

## API 速查表

### 构造、复制与状态

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `QPicture(int formatVersion = -1)` | 创建空 picture；可指定 Qt picture 格式版本。 | 默认 `-1` 为当前格式；仅用于受控 Qt 兼容场景。 |
| `QPicture(const QPicture &other)` | 快速复制 picture。 | 隐式共享；之后修改会按需分离。 |
| `operator=(const QPicture &other)` | 复制赋值。 | 同样采用隐式共享语义。 |
| `operator=(QPicture &&other)` | 移动赋值。 | `noexcept`；适合容器和返回值优化。 |
| `swap(QPicture &other)` | 快速交换两个 picture 的数据。 | `noexcept`；不重放也不复制命令。 |
| `~QPicture()` | 销毁 picture。 | 不影响已复制出的数据或已结束的目标绘制。 |
| `isNull() const` | 是否不含任何 picture 数据。 | 空 picture 的 `data()` 为 null，`boundingRect()` 无效。 |

### 录制、重放与几何

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `play(QPainter *painter)` | 在给定 painter 上重放命令，等价于原点 `(0, 0)` 的 `drawPicture()`。 | painter 必须有效且适合当前目标；检查返回值。 |
| `boundingRect() const` | 返回 picture 包围矩形。 | 空 picture 返回无效矩形；自动值可能被手工覆盖。 |
| `setBoundingRect(const QRect &rect)` | 覆盖自动计算的包围矩形。 | 只在确知范围时使用；错误范围会影响布局/裁剪。 |

### 文件、设备与原始数据

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `save(const QString &fileName)` | 保存到文件。 | Qt 专有二进制格式；检查返回值。 |
| `save(QIODevice *device)` | 保存到已打开的 I/O 设备。 | 调用方管理 device 的打开模式、错误和生命周期。 |
| `load(const QString &fileName)` | 从文件加载。 | 失败会使 picture 无效；外部输入按不可信数据处理。 |
| `load(QIODevice *device)` | 从 I/O 设备加载。 | 控制读取上限和 `QDataStream` 错误处理。 |
| `data() const` | 返回内部二进制数据指针。 | 下一次非 const 成员调用前有效；空 picture 返回 null。 |
| `size() const` | 返回内部二进制数据字节数。 | 与 `data()` 配对复制数据。 |
| `setData(const char *data, uint size)` | 从字节缓冲区设置 picture 数据。 | 会复制输入；不要信任外部字节，使用前验证。 |
| `operator<<(QDataStream &, const QPicture &)` | 将 picture 写入数据流。 | 与版本、错误处理和不可信输入策略配套。 |
| `operator>>(QDataStream &, QPicture &)` | 从数据流读入 picture。 | 检查 stream 状态，限制外部输入资源。 |

## 与相邻类型的选择

| 需求 | 推荐类型 |
| --- | --- |
| 记录并在 Qt 绘制目标上重放 painter 命令 | `QPicture` |
| 生成固定像素快照或后台绘制结果 | `QImage` |
| 输出通用 PDF 文档 | `QPdfWriter` |
| 输出通用 SVG 矢量图 | `QSvgGenerator` |
| 缓存频繁使用的 GUI 像素图 | `QPixmapCache` / `QPixmap` |

一句话记忆：`QPicture` 记录的是 Qt 的 painter 命令，不是像素；它适合 Qt 内部延迟重放，不适合承担长期、开放式图形交换格式的职责。
