# Qt QRegion 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRegion>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 定位：由矩形组成的整数区域，用于裁剪、脏区和区域布尔运算

## 1. 它解决什么问题

绘制窗口经常不需要重绘整块矩形。例如，一个窗口可能只有几个互不相邻的控件、图元或遮挡区域发生变化。`QRegion` 用一组互不重叠的矩形表示这样的区域，可以交给 `QPainter::setClipRegion()` 限制绘制范围，也可以用于描述需要刷新的脏区。

`QRegion` 还提供区域的并集、交集、差集和异或运算，因此可以把矩形、椭圆、多边形或位图转换成区域，再组合出复杂的可见区域。

它解决的是“哪些整数像素区域需要被处理”的问题，不是“如何构造任意平滑矢量形状”的问题。需要绘制路径、曲线、抗锯齿轮廓或复杂填充时，应使用 `QPainterPath`；需要限制 painter 的输出范围时，再把适当的 `QRegion` 作为裁剪区。

## 2. 真实使用场景

### 2.1 绘制脏区裁剪

自定义 `QWidget`、`QRasterWindow` 或其它 `QPainter` 绘制对象可以根据 `QPaintEvent::region()` 只重绘发生变化的区域：

```cpp
void Canvas::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    painter.setClipRegion(event->region());
    drawScene(painter);
}
```

### 2.2 图元可见区域

一个复杂图元可能被多个矩形遮挡。用 `visible = content.subtracted(occluded)` 得到可见区域，再把结果传给绘制或命中测试逻辑。

### 2.3 多个局部更新合并

当多个对象分别产生更新请求时，可以用 `united()` 或 `operator|` 合并区域，最终一次性提交给刷新接口，减少重复调度。

### 2.4 窗口系统和平台互操作

在 Windows 平台上，`toHRGN()` 和 `fromHRGN()` 可在 Qt 区域与 Win32 `HRGN` 之间转换。它们是平台 API，不能写成跨平台业务逻辑的唯一实现。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QRegion>
```

qmake 工程使用：`QT += gui`。

`QRegion` 是隐式共享值类型，复制通常成本较低。它不提供可修改迭代器，迭代只允许读取组成区域的矩形。

## 4. 最小可用示例

下面的例子把一个椭圆区域与两个矩形组合，并把结果作为 painter 裁剪区：

```cpp
#include <QPainter>
#include <QRegion>

void paintClipped(QPainter &painter)
{
    const QRegion ellipse(QRect(20, 20, 240, 140), QRegion::Ellipse);
    const QRegion left(QRect(0, 0, 150, 180));
    const QRegion right(QRect(100, 40, 180, 160));

    const QRegion visible = ellipse.intersected(left.united(right));
    if (visible.isEmpty())
        return;

    painter.save();
    painter.setClipRegion(visible);
    painter.fillRect(visible.boundingRect(), Qt::darkCyan);
    painter.restore();
}
```

`visible.boundingRect()` 只是区域的包围矩形，可能包含区域外的空洞；真正的绘制限制由 `setClipRegion(visible)` 提供。不要把包围矩形误当成区域本身。

## 5. 表示模型和几何语义

### 5.1 区域是矩形分解，不是一个单独的多边形

`QRegion` 内部表示为一组互不重叠的矩形。对区域使用 `begin()`/`end()`、范围 `for` 或 `rects()`，得到的是这组分解矩形；所有矩形的并集才等于原始区域。

同一个几何区域可能存在不同的矩形分解方式，因此不要把 `rectCount()` 当成区域复杂度的绝对几何指标。它更适合作为绘制和数据传输成本的粗略信号。

### 5.2 `RegionType`

用 `QRegion(QRect, RegionType)` 或坐标构造函数创建简单区域时：

- `Rectangle` 覆盖整个矩形。
- `Ellipse` 表示内接于该矩形的填充椭圆。

这些区域以整数像素区域表达，不提供 `QPainterPath` 那样的连续曲线和抗锯齿轮廓。

### 5.3 空区域、null 区域和包围矩形

默认构造得到空区域。Qt 6.11.1 文档中 `isNull()` 与 `isEmpty()` 语义相同，均表示区域不包含任何点。

空区域的 `boundingRect()` 返回 `QRect::isNull()` 的矩形。一个非空区域的包围矩形只保证包住整个区域，不能保证包围矩形内每个点都属于该区域。

### 5.4 坐标是整数

`QRegion` 的基本几何类型是 `QRect`、`QPoint` 和整数偏移。需要亚像素几何、旋转路径或浮点边界时，使用 `QPainterPath`、`QRectF` 等绘图类型，并在确实需要像素裁剪时再转换策略。

## 6. 区域布尔运算

| 运算 | 成员函数 | 中缀运算符 | 结果 |
| --- | --- | --- | --- |
| 并集 | `united()` | `operator|`、`operator+` | 两个区域中任一点的集合 |
| 交集 | `intersected()` | `operator&` | 同时属于两个区域的点 |
| 差集 | `subtracted()` | `operator-` | 当前区域中减去另一个区域 |
| 异或 | `xored()` | `operator^` | 只属于其中一个区域的点 |

`united()`、`intersected()`、`subtracted()` 和 `xored()` 返回新区域，不修改左操作数；对应的复合赋值运算会修改当前对象。对 `QRect` 的重载可避免为了一个矩形临时构造 `QRegion`。

复杂区域的矩形分解可能很多。大量交集、差集和 XOR 运算会增加计算成本，结果用于 painter 裁剪时也可能让底层绘制变慢。应根据实际脏区和绘制成本测量，而不是盲目追求更碎的区域。

## 7. 查询、迭代和 `QSpan`

### 7.1 `contains()` 的矩形重载

`contains(const QPoint &)` 的语义直观：判断点是否在区域内。

但 Qt 6.11.1 文档对 `contains(const QRect &)` 的定义是：判断区域是否与给定矩形重叠。它不是“给定矩形的所有点都被区域完全包含”的严格测试。需要完全包含语义时，应自行计算区域与矩形的关系，例如同时检查交集结果和面积/矩形分解，不能只看函数名。

`intersects()` 则明确用于测试区域与矩形或另一个区域是否相交。

### 7.2 迭代得到的是非重叠矩形

`const_iterator` 和 `const_reverse_iterator` 都只读。`begin()`/`end()`、`cbegin()`/`cend()` 用于正向遍历，`rbegin()`/`rend()`、`crbegin()`/`crend()` 用于反向遍历。

范围 `for` 是最直观的读取方式：

```cpp
for (const QRect &rect : region)
    processDirtyRect(rect);
```

迭代期间不要通过其它代码修改同一个区域；任何改变区域的非 const 操作都可能让迭代器失效。

### 7.3 `rects()` 的借用视图

Qt 6.8 新增的 `rects()` 返回 `QSpan<const QRect>`，直接暴露组成区域的矩形序列，避免先构造 `QVector<QRect>` 的额外复制。

这个 span 在对该 `QRegion` 调用下一次修改对象的非 const 成员函数前有效。不要把它保存到长期缓存，也不要在 `translate()`、复合赋值或其它修改操作后继续使用旧 span。

### 7.4 `setRects()` 的输入契约

`setRects(QSpan<const QRect>)` 要求输入矩形已经是最优的 Y-X 排序，并满足：

- 矩形之间不能相交。
- 相同 top 坐标的矩形必须具有相同高度。
- 水平方向相邻的矩形必须先合并，不能彼此 abut。
- 按 Y 为主排序键、X 为次排序键递增排列。
- 矩形数量必须小于 `INT_MAX`。

这是一个面向已规范化矩形数据的低层接口，不适合把任意未排序、相交矩形数组直接塞进去。普通代码更适合使用构造函数和布尔运算，让 Qt 负责规范化。

## 8. 与绘制和脏区协作

### 8.1 作为 `QPainter` 裁剪区

`QPainter::setClipRegion()` 的区域使用逻辑坐标。它会把当前 painter 裁剪限制替换为给定区域，除非指定其它 `Qt::ClipOperation`。调用 `save()`/`restore()` 可以把临时裁剪限制在一段绘制代码内。

区域裁剪只限制输出，不会自动减少业务代码计算。如果 `drawScene()` 在设置裁剪之前已经生成了所有复杂几何，CPU 计算仍然会发生；要获得真正收益，需要让图元查询也使用脏区或包围盒。

### 8.2 作为窗口更新区域

在 `QPaintDeviceWindow` 中，`update(const QRegion &region)` 会标记该区域为脏并异步安排重绘。下一次绘制事件前的多次请求会合并，未暴露窗口的更新可能延迟到重新暴露时处理。

`QPaintEvent::region()` 是本次需要更新的区域，可以直接传给 `QPainter::setClipRegion()`。如果图元带有阴影、抗锯齿边缘或会影响邻近像素，请把完整受影响区域加入更新区域。

## 9. 常见错误与排查

### 把 `QRegion` 当作矢量路径

区域由矩形分解表示，椭圆和多边形也会被转换为像素区域。需要平滑轮廓、描边、旋转或浮点变换时使用 `QPainterPath`。

### 把 `boundingRect()` 当成精确区域

`boundingRect()` 只给出包围矩形。对有孔洞、凹形或多个分离部分的区域，直接绘制包围矩形会处理大量不属于原区域的像素。需要精确限制时使用完整 `QRegion`。

### 误读 `contains(QRect)`

该重载表示与矩形有重叠，而不是矩形完全在区域内部。需要严格包含判断时不要直接依赖它。

### 忽略复杂区域的成本

位图逐像素转换、复杂多边形和反复差集/XOR 都可能产生大量矩形，进而拖慢绘制。对于遮罩图片，Qt 文档特别提示，直接使用 `QPixmap::setMask()` 往往比把位图转换成 `QRegion` 再绘制更快。

### 保存 `rects()` 返回值后继续修改区域

`QSpan` 不拥有数据，且在区域发生下一次非 const 修改后失效。需要长期保存时，复制成自己的 `QVector<QRect>` 或其它拥有型容器。

### 把 Windows `HRGN` API 写成通用代码

`toHRGN()` 和 `fromHRGN()` 只在 Windows 平台可用。跨平台代码应通过条件编译隔离，并保留 `QRegion` 作为业务层类型。

## 10. 逐项 API 说明

### `enum QRegion::RegionType`

**作用：** 指定由矩形创建的区域形状。

- `Rectangle`：覆盖整个矩形。
- `Ellipse`：位于矩形内部的填充椭圆。

它只影响构造阶段，不改变后续布尔运算和迭代的矩形区域语义。

### `QRegion::const_iterator`

**作用：** 遍历组成区域的互不重叠矩形。

**边界：** 只能读取，不能通过迭代器修改区域；所有矩形的并集等于原始区域。

### `QRegion::const_reverse_iterator`

**作用：** 以反向顺序遍历组成区域的互不重叠矩形。

**边界：** 只能读取，修改区域后不要继续使用旧迭代器。

### `QRegion::QRegion()`

**作用：** 构造空区域。

**结果：** `isEmpty()` 和 `isNull()` 都返回 `true`，`boundingRect()` 返回 null `QRect`。

### `QRegion::QRegion(const QBitmap &bitmap)`

**作用：** 从位图构造区域。位图中为 `Qt::color1` 的像素会各自作为一个 1x1 矩形进入区域。

**性能边界：** 可能形成非常复杂的区域并拖慢绘制。若目标是绘制带遮罩的 pixmap，Qt 文档建议优先考虑 `QPixmap::setMask()`。

### `QRegion::QRegion(const QPolygon &polygon, Qt::FillRule fillRule = Qt::OddEvenFill)`

**作用：** 按指定填充规则把多边形转换成区域。

**规则：**

- `Qt::OddEvenFill` 使用奇偶填充。
- `Qt::WindingFill` 使用 winding 填充。

**性能边界：** 复杂多边形可能生成复杂区域，影响后续绘制。

### `QRegion::QRegion(int x, int y, int w, int h, QRegion::RegionType type = Rectangle)`

**作用：** 创建矩形或椭圆区域。

**参数语义：** `Rectangle` 覆盖 `(x, y, w, h)`；`Ellipse` 创建中心位于该矩形中心、尺寸为 `w` 和 `h` 的填充椭圆。应用应传入符合预期的有效尺寸。

### `QRegion::QRegion(const QRect &rect, QRegion::RegionType type = Rectangle)`

**作用：** 从 `QRect` 创建矩形或椭圆区域。

**边界：** 如果矩形无效，创建 null 区域。`type` 只决定创建形状，不改变坐标类型。

### `QRegion::QRegion(const QRegion &other)`

**作用：** 复制区域值。

**语义：** `QRegion` 隐式共享，复制通常轻量；任一副本后续修改时由 Qt 处理分离。

### `QRegion::QRegion(QRegion &&other) noexcept`

**作用：** 移动构造区域。

**边界：** 移动后 `other` 为 null 区域。不要继续依赖它原有的矩形内容。

### `QRegion::begin() const`

**作用：** 返回指向组成区域的非重叠矩形序列开头的只读迭代器。

**注意：** 与 `end()` 配对使用；区域修改可能使迭代器失效。

### `QRegion::boundingRect() const`

**作用：** 返回包住整个区域的最小包围矩形。

**边界：** 空区域返回 `QRect::isNull()` 的矩形；非空区域的包围矩形可能包含原区域之外的点。

### `QRegion::cbegin() const`

**作用：** `begin()` 的只读别名。

### `QRegion::cend() const`

**作用：** `end()` 的只读别名。

### `QRegion::contains(const QPoint &point) const`

**作用：** 判断区域是否包含给定点。

**结果：** 点在区域内返回 `true`，否则返回 `false`。

### `QRegion::contains(const QRect &rect) const`

**作用：** 判断区域是否与给定矩形重叠。

**关键边界：** Qt 文档将此重载定义为 overlap 测试，不是严格的“矩形完全被区域包含”测试；不要因函数名而误读语义。

### `QRegion::crbegin() const`

**作用：** `rbegin()` 的只读别名，返回反向只读迭代器。

### `QRegion::crend() const`

**作用：** `rend()` 的只读别名。

### `QRegion::end() const`

**作用：** 返回指向矩形序列末尾后一位置的只读迭代器。

**注意：** 不能解引用 end 迭代器；与 `begin()` 配合遍历。

### `[since 6.0, Windows] QRegion QRegion::fromHRGN(HRGN hrgn)`

**作用：** 把 Win32 `HRGN` 转换成等价的 `QRegion`。

**平台边界：** 仅 Windows API 可用；调用前后应按 Win32 句柄的所有权规则管理传入句柄，不能把该函数当成通用跨平台入口。

### `QRegion QRegion::intersected(const QRect &rect) const`

**作用：** 返回当前区域与矩形的交集，不修改当前对象。

**结果：** 没有重叠时得到空区域。

### `QRegion QRegion::intersected(const QRegion &region) const`

**作用：** 返回两个区域的交集，不修改当前对象。

**适用场景：** 把内容区域限制到视口、脏区或多个可见区域的共同范围。

### `bool QRegion::intersects(const QRect &rect) const`

**作用：** 判断当前区域与矩形是否相交。

**注意：** 这是布尔测试，不返回相交部分；需要具体区域时使用 `intersected()`。

### `bool QRegion::intersects(const QRegion &region) const`

**作用：** 判断两个区域是否有共同部分。

**性能习惯：** 只需要真假时使用该函数，避免为了测试相交而先构造完整交集。

### `bool QRegion::isEmpty() const`

**作用：** 判断区域是否不包含任何点。

**注意：** 空区域可能来自默认构造、无效矩形、空交集或差集结果。空区域的 `boundingRect()` 是 null `QRect`。

### `bool QRegion::isNull() const`

**作用：** 判断区域是否为空。

**语义：** 在 Qt 6.11.1 中它与 `isEmpty()` 相同；不要把它当作与“曾经有过内容但后来被清空”不同的状态。

### `QRegion::rbegin() const`

**作用：** 返回反向遍历矩形分解的只读迭代器。

### `int QRegion::rectCount() const`

**作用：** 返回区域分解成的矩形数量。

**注意：** 等价于 `end() - begin()`；数量越大通常意味着遍历和裁剪管理成本更高，但不是区域面积或几何复杂度的唯一指标。

### `[since 6.8] QSpan<const QRect> QRegion::rects() const`

**作用：** 以不拥有数据的 span 形式返回组成区域的非重叠矩形。

**生命周期：** span 在对该区域进行下一次修改对象的非 const 操作前有效。不要跨修改操作保存或使用。

**版本边界：** Qt 5 中曾返回 `QVector<QRect>`；Qt 6.8 起返回 `QSpan<const QRect>`，迁移代码时要注意不再拥有独立容器。

### `QRegion::rend() const`

**作用：** 返回反向矩形序列末尾后一位置的只读迭代器。

### `[since 6.8] void QRegion::setRects(QSpan<const QRect> rects)`

**作用：** 用一组已经规范化的矩形替换当前区域。

**输入契约：** 矩形不能相交；同一 top 的矩形高度相同；水平相邻矩形必须合并；按 Y-X 顺序排列；数量小于 `INT_MAX`。不满足这些条件时不要调用该低层接口。

### `[deprecated] void QRegion::setRects(const QRect *rects, int number)`

**作用：** 旧的指针加数量版本，用矩形数组替换当前区域。

**版本建议：** Qt 6.11.1 文档将其标记为 deprecated，新的代码应使用 `QSpan<const QRect>` 重载，并遵守相同的矩形排序和规范化要求。

### `QRegion QRegion::subtracted(const QRegion &region) const`

**作用：** 返回当前区域减去 `region` 后的结果。

**边界：** 结果可能被分解为多个矩形；完全覆盖时得到空区域。

### `void QRegion::swap(QRegion &other) noexcept`

**作用：** 交换两个区域值。

**语义：** 操作快速且不会失败，适合在临时区域准备完成后交换到成员对象。

### `[since 6.0, Windows] HRGN QRegion::toHRGN() const`

**作用：** 把当前区域转换为等价的 Win32 `HRGN`。

**平台边界：** 仅 Windows 可用。返回的原生句柄应按 Qt/Win32 对应 API 的所有权约定处理，不要在非 Windows 代码中依赖该类型。

### `void QRegion::translate(int dx, int dy)`

**作用：** 原地移动区域，沿 X 轴移动 `dx`，沿 Y 轴移动 `dy`。

**方向：** 正值向右、向下；负值向左、向上。

### `void QRegion::translate(const QPoint &offset)`

**作用：** 按 `offset.x()` 和 `offset.y()` 原地移动区域。

**注意：** 这是修改当前对象的重载，不要与返回副本的 `translated()` 混淆。

### `QRegion QRegion::translated(int dx, int dy) const`

**作用：** 返回移动后的区域副本，不修改当前区域。

**方向：** 正值向右、向下；负值向左、向上。

### `QRegion QRegion::translated(const QPoint &offset) const`

**作用：** 按点偏移返回移动后的区域副本，不修改当前区域。

### `QRegion QRegion::united(const QRect &rect) const`

**作用：** 返回当前区域与矩形的并集。

**注意：** 不修改当前对象；只需要合并一个矩形时比显式构造临时 `QRegion` 更直接。

### `QRegion QRegion::united(const QRegion &region) const`

**作用：** 返回两个区域的并集。

**性能边界：** 两个复杂区域合并后可能产生较多矩形，应避免在每个像素或高频循环中重复构造。

### `QRegion QRegion::xored(const QRegion &region) const`

**作用：** 返回两个区域的异或结果，即只属于其中一个区域的部分。

**适用场景：** 计算切换区域或差异区域；如果只需要新增/移除部分，先确认 XOR 是否真的符合业务语义。

### `QRegion::operator QVariant() const`

**作用：** 把区域转换为 `QVariant`，用于元对象系统、属性或通用值传递。

**注意：** 这是值转换，不改变区域；跨进程或持久化时仍应选择明确的数据格式。

### `bool QRegion::operator!=(const QRegion &other) const`

**作用：** 判断两个区域是否不同。

**语义：** 按区域几何值比较，而不是比较内部矩形分解的指针或共享存储身份。

### `QRegion QRegion::operator&(const QRegion &region) const`

**作用：** `intersected(region)` 的运算符形式，返回交集。

### `QRegion QRegion::operator&(const QRect &rect) const`

**作用：** `intersected(rect)` 的运算符形式，返回与矩形的交集。

### `QRegion &QRegion::operator&=(const QRegion &region)`

**作用：** 将当前区域替换为与 `region` 的交集。

### `QRegion &QRegion::operator&=(const QRect &rect)`

**作用：** 将当前区域替换为与矩形的交集。

### `QRegion QRegion::operator+(const QRegion &region) const`

**作用：** `united(region)` 的运算符形式。

**注意：** `+` 在这里表示区域并集，不是几何平移或面积相加；新代码也可使用语义更直观的 `united()` 或 `operator|`。

### `QRegion QRegion::operator+(const QRect &rect) const`

**作用：** 返回当前区域与矩形的并集。

### `QRegion &QRegion::operator+=(const QRect &rect)`

**作用：** 把矩形并入当前区域并修改当前对象。

### `QRegion &QRegion::operator+=(const QRegion &region)`

**作用：** 把另一个区域并入当前区域并修改当前对象。

### `QRegion QRegion::operator-(const QRegion &region) const`

**作用：** `subtracted(region)` 的运算符形式，返回差集副本。

### `QRegion &QRegion::operator-=(const QRegion &region)`

**作用：** 从当前区域减去另一个区域并修改当前对象。

### `QRegion::operator=(QRegion &&other) noexcept`

**作用：** 移动赋值，把 `other` 的区域内容转移到当前对象。

**边界：** 移动后的 `other` 为 null 区域，不应继续依赖其旧内容。

### `QRegion &QRegion::operator=(const QRegion &other)`

**作用：** 把另一个区域值赋给当前对象。

**语义：** 使用隐式共享值语义，当前对象原有内容被替换；后续修改会按 Qt 的分离规则处理。

### `bool QRegion::operator==(const QRegion &region) const`

**作用：** 判断两个区域的几何值是否相等。

**注意：** 相等比较关注区域值，不应把 `rectCount()` 或矩形分解顺序当作几何相等的替代判断。

### `QRegion QRegion::operator^(const QRegion &region) const`

**作用：** `xored(region)` 的运算符形式，返回异或区域。

### `QRegion &QRegion::operator^=(const QRegion &region)`

**作用：** 将当前区域替换为与另一个区域的异或结果。

### `QRegion QRegion::operator|(const QRegion &region) const`

**作用：** `united(region)` 的运算符形式，返回并集区域。

### `QRegion &QRegion::operator|=(const QRegion &region)`

**作用：** 将另一个区域并入当前区域。

### `QDataStream &operator<<(QDataStream &stream, const QRegion &region)`

**作用：** 把区域写入 `QDataStream`。

**边界：** 只有启用 Qt DataStream 支持时可用；持久化数据还应考虑 `QDataStream` 版本和字节序约定。

### `QDataStream &operator>>(QDataStream &stream, QRegion &region)`

**作用：** 从 `QDataStream` 读取区域。

**边界：** 输入数据必须与写入端采用兼容的数据流格式；读取后应检查流状态和区域值是否符合业务约束。

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum QRegion::RegionType { Rectangle, Ellipse }` | 指定矩形构造器生成矩形还是填充椭圆区域 | 区域最终仍是整数矩形分解，不是矢量路径 |
| 类型 | `QRegion::const_iterator` | 正向遍历非重叠矩形分解 | 只读；区域修改后旧迭代器可能失效 |
| 类型 | `QRegion::const_reverse_iterator` | 反向遍历非重叠矩形分解 | 只读；不能通过迭代器修改区域 |
| 构造 | `QRegion()` | 创建空区域 | `isEmpty()`/`isNull()` 为 true，包围矩形为 null |
| 构造 | `QRegion(const QBitmap &bitmap)` | 从 `Qt::color1` 位图像素创建区域 | 可能非常复杂并拖慢绘制；遮罩 pixmap 可考虑 `QPixmap::setMask()` |
| 构造 | `QRegion(const QPolygon &polygon, Qt::FillRule fillRule)` | 从多边形创建填充区域 | `OddEvenFill` 与 `WindingFill` 结果不同；复杂多边形成本高 |
| 构造 | `QRegion(int x, int y, int w, int h, RegionType type)` | 创建矩形或椭圆区域 | `Ellipse` 是内接填充椭圆；传入有效尺寸 |
| 构造 | `QRegion(const QRect &rect, RegionType type)` | 从矩形创建区域 | 无效矩形创建 null 区域 |
| 构造 | `QRegion(const QRegion &other)` | 复制区域值 | 隐式共享，复制通常轻量 |
| 构造 | `QRegion(QRegion &&other) noexcept` | 移动构造区域 | 移动后 `other` 为 null |
| 迭代 | `begin()` / `end()` | 正向遍历区域矩形 | `end()` 不可解引用；修改区域可能使迭代器失效 |
| 迭代 | `cbegin()` / `cend()` | const 正向遍历 | 分别等同于 `begin()`/`end()` |
| 几何查询 | `QRect boundingRect() const` | 获取区域的包围矩形 | 空区域返回 null 矩形；包围矩形可能包含区域外点 |
| 包含测试 | `bool contains(const QPoint &point) const` | 判断点是否在区域内 | 点级语义直观 |
| 包含测试 | `bool contains(const QRect &rect) const` | 判断区域是否与矩形重叠 | 文档语义是 overlap，不是完全包含 |
| 交集测试 | `bool intersects(const QRect &rect) const` | 判断是否与矩形相交 | 只返回真假，不生成交集区域 |
| 交集测试 | `bool intersects(const QRegion &region) const` | 判断两个区域是否相交 | 只需真假时比先调用 `intersected()` 更直接 |
| 状态 | `bool isEmpty() const` | 判断区域是否不包含点 | 空交集、无效构造等都会得到 true |
| 状态 | `bool isNull() const` | 判断区域是否为空 | Qt 6.11.1 中与 `isEmpty()` 相同 |
| 迭代 | `rbegin()` / `rend()` | 反向遍历区域矩形 | 只读反向迭代器 |
| 统计 | `int rectCount() const` | 获取矩形分解数量 | 是遍历/裁剪成本线索，不代表面积 |
| 读取 | `[since 6.8] QSpan<const QRect> rects() const` | 无复制读取矩形分解 | span 在下一次非 const 修改后失效，不拥有数据 |
| 写入 | `[since 6.8] void setRects(QSpan<const QRect> rects)` | 用已规范化矩形直接设置区域 | 必须满足不相交、Y-X 排序、同 top 同高、无水平相邻等契约 |
| 写入 | `[deprecated] void setRects(const QRect *rects, int number)` | 旧式数组设置区域 | 新代码使用 `QSpan` 重载 |
| 布尔运算 | `QRegion united(const QRect &rect) const` | 与矩形求并集 | 返回新区域，不修改当前对象 |
| 布尔运算 | `QRegion united(const QRegion &region) const` | 与区域求并集 | 复杂区域可能产生大量矩形 |
| 布尔运算 | `QRegion intersected(const QRect &rect) const` | 与矩形求交集 | 无重叠时为空 |
| 布尔运算 | `QRegion intersected(const QRegion &region) const` | 与区域求交集 | 适合限制到视口或脏区 |
| 布尔运算 | `QRegion subtracted(const QRegion &region) const` | 从当前区域扣除另一块区域 | 结果可能分裂为多个矩形 |
| 布尔运算 | `QRegion xored(const QRegion &region) const` | 获取区域异或结果 | 只保留单独属于一方的部分 |
| 平移 | `void translate(int dx, int dy)` | 原地移动区域 | 正值向右下，修改当前对象 |
| 平移 | `void translate(const QPoint &offset)` | 按点偏移原地移动 | 与 `translated()` 的返回副本语义不同 |
| 平移 | `QRegion translated(int dx, int dy) const` | 返回平移后的副本 | 当前对象不变 |
| 平移 | `QRegion translated(const QPoint &offset) const` | 按点偏移返回副本 | 当前对象不变 |
| 交换 | `void swap(QRegion &other) noexcept` | 快速交换两个区域 | 不抛异常，不改变其它对象所有权语义 |
| 平台转换 | `[since 6.0, Windows] HRGN toHRGN() const` | 转换为 Win32 区域句柄 | 仅 Windows；按原生句柄约定管理 |
| 平台转换 | `[since 6.0, Windows] static QRegion fromHRGN(HRGN hrgn)` | 从 Win32 区域句柄创建 Qt 区域 | 仅 Windows；隔离平台代码 |
| 裁剪协作 | `QPainter::setClipRegion(const QRegion &, Qt::ClipOperation)` | 限制 painter 输出到区域 | 使用逻辑坐标；包围矩形不是精确裁剪 |
| 更新协作 | `QPaintDeviceWindow::update(const QRegion &)` | 异步安排区域重绘 | 多次请求会合并，非暴露窗口可能延迟 |
| 比较 | `bool operator==(const QRegion &region) const` | 比较两个区域几何值是否相等 | 不要按矩形分解数量判断相等 |
| 比较 | `bool operator!=(const QRegion &region) const` | 比较两个区域是否不同 | 与 `operator==` 互补 |
| 并集运算符 | `operator|` / `operator+` | 以运算符形式求并集 | `+` 不是平移或面积相加 |
| 并集复合 | `operator|=` / `operator+=` | 原地并入区域或矩形 | 修改当前对象 |
| 交集运算符 | `operator&` / `operator&=` | 求交集或原地限制区域 | `QRect` 与 `QRegion` 均有重载 |
| 差集运算符 | `operator-` / `operator-=` | 求差集或原地扣除区域 | 复合版本修改当前对象 |
| 异或运算符 | `operator^` / `operator^=` | 求异或或原地切换区域 | 只对 `QRegion` 提供 |
| QVariant 转换 | `operator QVariant() const` | 将区域放入通用 Qt 值容器 | 仅值转换，不等于持久化格式 |
| 序列化 | `QDataStream &operator<<(QDataStream &, const QRegion &)` | 把区域写入数据流 | 受 DataStream 构建选项和版本影响 |
| 反序列化 | `QDataStream &operator>>(QDataStream &, QRegion &)` | 从数据流读取区域 | 检查流状态和输入格式兼容性 |

---

### 一句话总结

`QRegion` 是面向整数像素区域的值类型：用它描述脏区、裁剪区和可见区域，用布尔运算组合区域，用 `rects()` 或只读迭代器读取矩形分解；需要平滑矢量形状时应使用 `QPainterPath`，需要严格矩形完全包含判断时不要误读 `contains(QRect)`。
