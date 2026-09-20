# QPicture

> Qt 6.11.1 · Qt GUI · 来自 `QPicture`

## 1. 先建立直觉

`QPicture` 是一个记录 `QPainter` 绘图命令的 paint device。你可以先把一段绘制过程录下来，之后再用另一个 `QPainter` 回放。它不是像 `QPixmap` / `QImage` 那样保存最终像素，而是保存“画了什么、如何画”的命令流。

这让它适合做轻量矢量式缓存、绘图命令序列化、重复回放。但也要记住：回放结果仍然依赖目标 painter、设备特性和当时的绘制环境，不等同于一张固定截图。

## 2. 类说明

- 头文件：`#include <QPicture>`
- CMake：`Qt6::Gui`
- 继承自：`QPaintDevice`
- 类型性质：隐式共享值类型，内部保存绘图命令数据
- 绘制方式：用 `QPainter` 画到 `QPicture`，再 `play()` 或 `QPainter::drawPicture()` 回放

`QPicture` 的数据格式主要面向 Qt 自身。它适合在同一 Qt 生态里保存/回放绘图命令，不应被当作通用矢量图格式替代 SVG、PDF 或图片文件。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPicture(int formatVersion = -1)` | 创建空 picture，可指定旧格式版本用于兼容。 |
| `boundingRect()` / `setBoundingRect()` | 读取或手动设置命令内容的边界矩形。 |
| `isNull()` | 判断是否没有录制数据。 |
| `play(QPainter *painter)` | 在目标 painter 上回放记录的绘图命令。 |
| `load(file/device)` | 从文件或设备读取 picture 数据；失败会使对象失效。 |
| `save(file/device)` | 保存 picture 数据。 |
| `data()` / `size()` | 获取内部数据指针和大小；指针只在下次非 const 操作前有效。 |
| `setData(const char *data, uint size)` | 直接设置 picture 数据，会复制输入。 |
| `swap()` | 快速交换两个 picture。 |
| `operator<<` / `operator>>` | 通过 `QDataStream` 序列化。 |

## 4. 关键用法

### 录制绘制命令

```cpp
QPicture picture;

{
    QPainter p(&picture);
    p.setPen(QPen(Qt::blue, 2));
    p.drawEllipse(QRectF(0, 0, 80, 80));
    p.drawText(QPointF(12, 45), "Qt");
}
```

只要 painter 绑定的是 `QPicture`，绘制操作就会被记录。作用域结束后 painter 析构，录制完成。

### 回放时保护 painter 状态

```cpp
painter.save();
painter.translate(20, 20);
picture.play(&painter);
painter.restore();
```

官方文档特别提醒：`play()` 不会为你保留目标 painter 状态。picture 中的命令可能改变 pen、brush、font、transform、clip 等状态，所以回放前后用 `save()` / `restore()` 更安全。

### 保存和加载

```cpp
picture.save("shape.pic");

QPicture loaded;
if (loaded.load("shape.pic"))
    painter.drawPicture(QPoint(0, 0), loaded);
```

`.pic` 这类文件更适合应用内部缓存或同一 Qt 版本/生态下使用；公开交换格式优先考虑 PDF、SVG 或常规图片。

## 5. 使用场景

- 把复杂绘制命令录制后多次回放。
- 应用内部保存一段可缩放的绘图操作。
- 在自定义控件中缓存不经常变化的矢量绘制层。
- 通过 `QDataStream` 在内部协议中传递绘图命令。
- 做绘制调试：记录一段 painter 操作，换设备回放观察差异。

## 6. 常见坑与经验

- **它不是位图。** 需要像素缓存时用 `QImage` 或 `QPixmap`；需要 PDF 输出时用 `QPdfWriter`。
- **回放会影响 painter 状态。** `play()` 前后最好手动保存/恢复目标 painter。
- **格式不适合长期公共归档。** `QPicture` 是 Qt 绘图命令格式，不是跨生态标准。
- **边界矩形可能需要手动设置。** 如果自动边界不符合你的缓存/布局需求，可以用 `setBoundingRect()`。
- **`data()` 指针很短命。** 下次非 const 操作后可能失效，需要长期保存就复制数据。
- **回放结果仍依赖设备。** 字体、DPI、高 DPI、paint engine 差异都可能影响最终视觉。

## 7. 知识点覆盖

- 绘图命令录制与像素缓存的区别
- `QPicture` 作为 `QPaintDevice` 的录制流程
- `play()`、`drawPicture()` 和 painter 状态污染
- 内部数据、边界矩形、文件/设备序列化
- 与 `QImage`、`QPixmap`、`QPdfWriter`、SVG 的取舍
