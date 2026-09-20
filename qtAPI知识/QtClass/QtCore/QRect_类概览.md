# QRect：面向整数像素网格的矩形值类型

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QRect>`  
> 所属模块：Qt Core

`QRect` 表示整数坐标上的矩形，常用于像素区域、窗口几何、绘制裁剪区、命中测试和图像子区域。它是无 QObject、无事件循环、可按值复制的轻量几何类型。

它看似简单，真正的难点却在坐标约定：`QRect` 沿用历史上的**离散像素、右下角包含**表示。因此 `right()` 和 `bottom()` 比数学几何中的真实右/下边界小 1。这是 Qt 代码里最常见的矩形边界错误来源。

## 它解决的问题

UI 布局和图像处理常需表达“从这里开始，覆盖这么宽这么高”的区域：

```cpp
QRect thumbnail(16, 24, 120, 90);
```

这表示左上角 `(16, 24)`、宽 `120`、高 `90` 的整数像素区域。它适合传给绘制、裁剪、窗口定位或与鼠标点做命中测试：

```cpp
if (thumbnail.contains(mousePos)) {
    // 鼠标落在缩略图覆盖的像素区域中
}
```

对于连续坐标、缩放、动画或设备无关像素计算，优先考虑 `QRectF`；不要在浮点和整数矩形之间反复转换后期待边界完全不变。

## 最重要的坐标规则

`QRect(x, y, width, height)` 的主表达方式是“左上角 + 尺寸”。在正常有效矩形中：

```text
left()   == x()
top()    == y()
right()  == x() + width()  - 1
bottom() == y() + height() - 1
```

例如：

```cpp
QRect r(10, 20, 3, 2);
// 覆盖 x = 10, 11, 12；y = 20, 21
// right() == 12，bottom() == 21
// 数学意义上的右/下边界是 x()+width()==13、y()+height()==22
```

因此：

- 传给以 `(x, y, width, height)` 表示范围的 API，直接使用 `x()`、`y()`、`width()`、`height()`；
- 若要得到连续坐标系中的右/下边界，使用 `x() + width()`、`y() + height()`；
- 不要把 `right()` / `bottom()` 当成半开区间的尾后坐标；
- `topRight()`、`bottomLeft()`、`bottomRight()` 同样遵循这个减 1 的历史规则。

Qt 官方不建议常规代码用“左上、右下点”构造函数。两点顺序可能反转时，用 `QRect::span(p1, p2)`，它始终包含两个端点及其间所有整数点。

## 构造、有效性与规范化

```cpp
QRect a(10, 20, 80, 40);                  // 推荐：左上角 + 宽高
QRect b(QPoint(10, 20), QSize(80, 40));   // 语义相同
QRect c = QRect::span(QPoint(15, 8), QPoint(3, 5));
```

默认构造得到 null 矩形：宽高均为 0。它也是 empty 和 invalid。三种状态不要混为一谈：

- `isNull()`：宽和高恰好都为 0；
- `isEmpty()`：至少一个方向没有可覆盖的像素，即 `left() > right()` 或 `top() > bottom()`；
- `isValid()`：存在至少一个整数像素，即 `left() <= right()` 且 `top() <= bottom()`。

对 `QRect`，empty 与 `!isValid()` 等价；null 只是 empty 的特殊情形。负宽高得到无效矩形；需要把反向拖拽框修正为正常区域时，调用 `normalized()`：

```cpp
QRect selection(start, end);
selection = selection.normalized();
```

两点构造函数只有在 `bottomRight` 位于 `topLeft` 的右下方时才把两端作为包含端点；顺序颠倒时会产生非包含、可能无效的矩形。鼠标拖拽始终用 `span()` 或 `normalized()` 更清楚。

## 常见实际场景

### 绘制或截图裁剪

```cpp
const QRect sourceArea(0, 0, image.width(), image.height());
painter.drawImage(targetRect, image, sourceArea);
```

图片尺寸正好天然对应 `QRect(0, 0, width, height)`。不要写成 `QRect(0, 0, image.width() - 1, image.height() - 1)`，后者会少一行和一列。

### 鼠标选择框

```cpp
const QRect selection = QRect::span(pressPos, currentPos);
widget->update(selection.adjusted(-1, -1, 1, 1));
```

`span()` 保证反向拖动也能产生有效的、包含起止点的范围。`adjusted()` 返回副本，适用于计算更新区域而不改原选择框。

### 布局碰撞和无效区域

```cpp
if (dirtyRect.intersects(viewport)) {
    const QRect repaint = dirtyRect.intersected(viewport);
    // 只重绘可见交集
}
```

两个 `QRect` 只要共享至少一个像素，`intersects()` 即返回 true。这与 `QRectF` 的“非空面积重叠”细节不同。

## 修改、移动与尺寸：哪些边不动

这三个家族有不同语义，混用会造成布局跳动：

- `setLeft()` / `setRight()` / `setTop()` / `setBottom()`：固定对边，改变尺寸；
- `moveLeft()` / `moveRight()` / `moveTop()` / `moveBottom()`：固定尺寸，平移整个矩形；
- `setWidth()` / `setHeight()`：固定左/上边，改变右/下边；
- `moveTo()` / `translate()`：固定尺寸，改变位置；
- `adjust()`：分别移动四条边，可能改变位置和尺寸。

```cpp
QRect r(10, 10, 50, 20);
r.setLeft(20);       // 右边不动，宽度缩小
r.moveLeft(0);       // 宽度不变，整体左移
r.adjust(1, 2, -1, -2); // 四边向内收缩
```

`adjust()` 原地修改；`adjusted()` 返回修改后的副本。`marginsAdded()` / `marginsRemoved()` 是同一类扩张和收缩操作的语义化写法，适合表达阴影、边框和安全边距。

## 包含、交集、并集

`contains(point, proper)` 默认包含边界。`proper == true` 时，点或子矩形必须严格位于内部，贴着任意边都不算包含。

```cpp
QRect r(0, 0, 10, 10);
r.contains(QPoint(0, 0));        // true
r.contains(QPoint(0, 0), true);  // false
```

`intersected()` / `operator&` 返回交集；无重叠时为 empty 矩形。`united()` / `operator|` 返回能覆盖两者的**包围矩形**，不是几何并集；若两块区域分离，结果会包含中间原本不属于任何一方的空白。需要表示非矩形区域并集时用 `QRegion`。

## 范围、溢出与平台边界

`QRect` 的坐标与尺寸基于 `int`。文档规定，可能超出 `int` 最小/最大值的操作具有未定义行为。大画布、拼接多层 margin、累积平移和从外部数据转换时，要先做范围控制，不能把“发生了回绕”当作错误处理方式。

`toRectF()` 从 Qt 6.4 起提供，把整数矩形转换为浮点矩形并保持其完整几何范围。`toCGRect()` 只在 Apple 平台可用；跨平台代码不要无条件调用它。

`QRect` 只是值类型，没有对象线程亲和性；但它经常来自 `QWidget`、`QWindow`、`QScreen` 或绘制设备。这些对象的 API 仍有各自的 GUI 线程和生命周期限制，不能因为 `QRect` 可跨线程传递就跨线程访问其来源对象。

## 常见错误

1. **把 `right()` 当作 `x() + width()`。** 对 `QRect` 它少 1；半开边界使用 `x() + width()`。
2. **用 `width() - 1`、`height() - 1` 再构造矩形。** 构造函数的最后两个参数是尺寸，不是右下坐标。
3. **反向拖拽时直接两点构造。** 用 `span()` 或 `normalized()`。
4. **把 `united()` 当精确几何并集。** 它只返回包围盒；不连续区域应使用 `QRegion`。
5. **在 invalid 矩形上做复杂集合运算。** 文档不定义这类非平凡操作的行为；先 `isValid()` 或 `normalized()`。
6. **忽略整数溢出。** 坐标加 margin 或累计平移不能越过 `int` 范围。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QRect()` | 构造 null 矩形。 | 默认值是 empty、invalid，不是 1x1 矩形。 |
| `QRect(QPoint topLeft, QPoint bottomRight)` | 以两个包含端点构造。 | 顺序可能反转时改用 `span()`。 |
| `QRect(QPoint topLeft, QSize size)` | 以左上角和尺寸构造。 | 推荐的点加尺寸形式。 |
| `QRect(int x, int y, int width, int height)` | 以左上角和整数尺寸构造。 | 最后两个参数不是右下坐标。 |
| `span(p1, p2)` | 构造包含两点及中间全部整数点的矩形。 | 不受两点先后顺序影响；Qt 6.0 起。 |
| `x()` / `left()`，`y()` / `top()` | 取得左、上坐标。 | `x()==left()`，`y()==top()`。 |
| `width()` / `height()` / `size()` | 取得尺寸。 | 有效矩形的宽高均大于 0。 |
| `right()` / `bottom()` | 取得历史包含式右、下像素坐标。 | 分别等于 `x()+width()-1`、`y()+height()-1`。 |
| `topLeft()` / `topRight()` / `bottomLeft()` / `bottomRight()` | 取得四个历史像素角点。 | 右/下相关坐标同样有减 1 规则。 |
| `center()` | 取得整数中心点。 | 偶数尺寸会产生整数截断后的中心。 |
| `isNull()` | 宽高均为 0。 | null 是 empty 的特殊情况。 |
| `isEmpty()` | 至少一个方向无像素。 | 与 `!isValid()` 等价。 |
| `isValid()` | 两方向均至少有一个像素。 | invalid 矩形不要用于复杂交并运算。 |
| `normalized()` | 交换反向边，得到非负尺寸的副本。 | 处理反向拖拽或负宽高。 |
| `setRect()` / `getRect()` | 按 `x,y,width,height` 设置或读取。 | 最适合尺寸语义，不混用右下坐标。 |
| `setCoords()` / `getCoords()` | 按包含式左上、右下坐标设置或读取。 | 牢记 `right()` / `bottom()` 的历史规则。 |
| `setLeft()` / `setRight()` / `setTop()` / `setBottom()` | 固定对边，改变当前尺寸。 | 设过对边会导致 invalid。 |
| `setX()` / `setY()` | `setLeft()` / `setTop()` 的别名。 | 不是移动；会改变宽高。 |
| `setTopLeft()` / `setTopRight()` / `setBottomLeft()` / `setBottomRight()` | 设置一个角，固定对角。 | 可能改变尺寸并产生 invalid。 |
| `setWidth()` / `setHeight()` / `setSize()` | 固定左上角，设置尺寸。 | 负或零尺寸会使矩形 invalid。 |
| `moveTo()` | 将左上角移到指定点。 | 尺寸不变。 |
| `moveLeft()` / `moveRight()` / `moveTop()` / `moveBottom()` | 将指定边移动到坐标。 | 尺寸不变，整块平移。 |
| `moveTopLeft()` / `moveTopRight()` / `moveBottomLeft()` / `moveBottomRight()` / `moveCenter()` | 将指定锚点移到目标点。 | 尺寸不变。 |
| `translate()` / `translated()` | 原地平移或返回平移副本。 | 正 dx/dy 分别向右/下移动。 |
| `adjust()` / `adjusted()` | 分别调整左、上、右、下边。 | 原地与副本版本的区别要分清。 |
| `transposed()` | 交换宽和高，返回副本。 | 左上角不变。 |
| `contains(point, proper)` | 判断点是否在内。 | 默认包含边界；`proper` 排除边界。 |
| `contains(rect, proper)` | 判断子矩形是否被包含。 | `proper` 要求完全不接触边界。 |
| `intersects(rect)` | 判断是否共享至少一个整数像素。 | 与 `QRectF` 的面积重叠条件不同。 |
| `intersected(rect)` / `operator&` / `operator&=` | 求交集。 | 无重叠得到 empty 矩形。 |
| `united(rect)` / `operator|` / `operator|=` | 求包围两者的最小矩形。 | 不是不连续区域的精确并集。 |
| `marginsAdded()` / `marginsRemoved()` | 返回加/减 `QMargins` 后的矩形。 | 收缩过多可能得到 invalid。 |
| `operator+=` / `operator-=` | 原地加/减 `QMargins`。 | 与上述副本函数对应。 |
| `operator+` / `operator-` | 非成员的 margin 加减形式。 | 结果为新矩形。 |
| `==` / `!=` | 比较矩形的四个存储边。 | 对整数矩形是精确比较。 |
| `toRectF()` | 转为浮点矩形。 | Qt 6.4 起；适合进入连续坐标计算。 |
| `toCGRect()` | 转为 Core Graphics 的 `CGRect`。 | 仅 Apple 平台可用。 |
| `QDataStream <<` / `>>` | 序列化和反序列化。 | 流版本和数据来源的兼容性由调用方管理。 |

## 一句话总结

`QRect` 是整数像素区域的基础值类型。优先用“左上角加尺寸”表示它，记住 `right()` / `bottom()` 的历史减 1 规则，反向两点用 `span()`，不连续区域改用 `QRegion`。
