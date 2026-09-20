# QRectF：连续坐标系中的有限浮点矩形

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QRectF>`  
> 所属模块：Qt Core

`QRectF` 表示二维平面中的有限浮点矩形。它用于缩放后的几何、动画插值、矢量绘制、场景坐标、触控命中测试和设备无关像素计算。它是无 QObject 的值类型，可复制、可跨线程传递；但从 GUI 对象取得或传回的几何仍要遵守那些对象的线程规则。

与 `QRect` 最大的区别不只是 `qreal`：`QRectF` 使用通常的连续几何语义，`right() == x() + width()`、`bottom() == y() + height()`，没有整数矩形的历史减 1 规则。

## 它解决的问题

整数矩形只能精确表示像素格。遇到高 DPI 缩放、旋转后的包围盒、动画中间帧或画布坐标时，过早取整会不断积累抖动和一像素误差：

```cpp
QRectF itemBounds(12.5, 8.25, 96.0, 32.0);
itemBounds.translate(0.2, 0.0);
```

`QRectF` 让这些计算保留连续坐标，直到真正交给整数像素 API 时才明确选择取整策略。

典型场景：

- `QPainter`、`QGraphicsView`、Qt Quick 或自定义画布的浮点几何；
- 动画、缩放、拖拽和变换后的边界计算；
- 用 `intersected()` 裁剪浮点内容；
- 最后以 `toAlignedRect()` 生成完整覆盖的整数重绘区。

## 坐标模型：没有减 1

`QRectF(x, y, width, height)` 表示左上边 `(x, y)` 和尺寸 `(width, height)`：

```text
left()   == x()
top()    == y()
right()  == x() + width()
bottom() == y() + height()
```

```cpp
QRectF r(10.0, 20.0, 3.0, 2.0);
// right() == 13.0
// bottom() == 22.0
```

这正是 `QRect` 与 `QRectF` 互换时必须停下来核对的地方。`QRectF(QRect)` 会把整数矩形转换为等价的连续覆盖范围，例如整数 `QRect(10, 20, 3, 2)` 变为宽 3、高 2 的 `QRectF`，而不是把其 `right()==12` 当作连续几何右边界。

## 构造、有效性与有限值要求

```cpp
QRectF a(10.5, 20.0, 80.25, 40.0);
QRectF b(QPointF(10.5, 20.0), QSizeF(80.25, 40.0));
QRectF c(QPointF(10.5, 20.0), QPointF(90.75, 60.0));
QRectF fromPixels(QRect(10, 20, 80, 40));
```

标量构造和绝大部分改动 API 要求传入有限数值。不要将 `NaN`、`+infinity` 或 `-infinity` 交给 `QRectF`；文档以“finite rectangle”为对象契约，非有限数会让比较、范围关系与绘制结果失去可靠语义。

状态定义：

- `isNull()`：宽高严格都为 `0.0`；
- `isEmpty()`：宽或高小于等于 `0.0`；
- `isValid()`：宽和高都大于 `0.0`。

与 `QRect` 一样，empty 等于 invalid；但浮点计算中“接近 0”不等于严格的 0。Qt 6.8 起可用 `qFuzzyIsNull(rect)` 判断宽高是否近似为零。

从两个点构造时，若第二点在第一点的左上方，宽或高为负。面对手势选择、反向缩放或外部输入时，在做交集和包含前用 `normalized()`。

## 精度、比较与转换策略

### `==` 不是严格逐位比较

`QRectF` 的 `operator==` 和 `operator!=` 使用模糊比较，不是浮点严格相等：

```cpp
if (first == second) {
    // 坐标和尺寸在 Qt 的模糊容差内近似相等
}
```

这对布局和绘制去抖有用，但不适合把 `QRectF` 的 `==` 当作哈希键、缓存键、序列化完整性校验或精确几何断言。需要明确表达近似语义时，可直接使用 Qt 6.8 起的 `qFuzzyCompare(lhs, rhs)`；需要严格策略时，应在业务层比较各坐标并自行定义容差或位级规则。

### 转为 `QRect` 时必须选策略

```cpp
const QRect rounded = bounds.toRect();
const QRect covering = bounds.toAlignedRect();
```

- `toRect()`：各坐标取最接近的整数；结果可能不能完全覆盖原浮点矩形；
- `toAlignedRect()`：返回**完全包含**原矩形的最小整数矩形，适合更新区、裁剪区和避免漏画；
- `QRect::toRectF()`：把整数矩形升级为浮点矩形，Qt 6.4 起提供。

绘制脏区域通常选 `toAlignedRect()`；仅为了显示整数坐标、接受少量取整误差时才选 `toRect()`。

## 移动、调整和边界设置

`setLeft()`、`setRight()`、`setTop()`、`setBottom()` 固定对边并改变尺寸；`moveLeft()`、`moveRight()`、`moveTop()`、`moveBottom()` 固定尺寸并平移。和 `QRect` 相同，但没有右/下减 1：

```cpp
QRectF r(10.0, 20.0, 30.0, 10.0);
r.setRight(50.0);  // left 仍为 10，宽度变为 40
r.moveRight(70.0); // 宽度仍为 40，left 变为 30
```

`adjust(dx1, dy1, dx2, dy2)` 分别把偏移加到左、上、右、下坐标；`adjusted()` 返回副本。参数必须有限，且过度收缩可能产生 empty/invalid 矩形。

`marginsAdded()` / `marginsRemoved()` 和 `QMarginsF` 适合表达外扩阴影、触控热区、内边距和视口裁剪。不要混用 `QMargins` 与 `QMarginsF`，否则会提前丢失小数边距。

## 包含、交集、并集

`contains()` 默认认为边界也在矩形内；它没有 `QRect::contains(..., proper)` 那个严格内部开关。需要排除边界时，调用方应按自己的容差规则比较坐标。

`QRectF::intersects()` 返回 true 的条件是两个矩形有**非空面积**的重叠。只在一条边或一个点接触，不算相交。这与 `QRect` 的“共享至少一个像素就相交”不同：

```cpp
QRectF a(0, 0, 10, 10);
QRectF b(10, 0, 5, 5);

a.intersects(b); // false：只接触 x == 10 的边
```

`intersected()` / `operator&` 返回交集；`united()` / `operator|` 返回包围两者的最小矩形。后者仍是包围盒，分离矩形的中间空白也会包含在结果里；需要精确区域集合时选择更合适的区域或路径类型。

## 平台转换

`fromCGRect()` / `toCGRect()` 只在 Apple 平台可用，用于 Core Graphics 互操作。

`fromDOMRect()` / `toDOMRect()` 仅在 WebAssembly 平台可用，Qt 6.5 起提供。`fromDOMRect()` 的实参必须是真实 DOM `DOMRect`；传入其他 JavaScript 值的行为未定义。将 Web API 数值交给 `QRectF` 前同样要确保它们有限。

## 常见错误

1. **沿用 `QRect` 的 `-1` 规则。** 对 `QRectF`，`right()` 就是 `x()+width()`，`bottom()` 就是 `y()+height()`。
2. **使用 `toRect()` 做重绘范围。** 四舍五入可能裁掉边缘；重绘或完整裁剪选 `toAlignedRect()`。
3. **认为接边算 `intersects()`。** `QRectF` 要求非空面积重叠。
4. **把 `==` 当严格浮点相等。** Qt 使用模糊比较；不能直接作为精确身份判断。
5. **让 `NaN` 或无穷进入几何计算。** 所有标量几何输入应先验证有限性。
6. **忽略负宽高。** 手势和坐标变换后先 `normalized()`，再做包含或交并。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QRectF()` | 构造 null 矩形。 | 宽高均为 0，因而 empty、invalid。 |
| `QRectF(QRect)` | 从整数矩形构造等价的浮点范围。 | 保持完整几何范围，避免手工使用 `QRect::right()`。 |
| `QRectF(QPointF topLeft, QPointF bottomRight)` | 以两个连续几何角点构造。 | 点序反转会得到负宽或高。 |
| `QRectF(QPointF topLeft, QSizeF size)` | 以左上角和浮点尺寸构造。 | `QSizeF` 必须表达有限数值。 |
| `QRectF(qreal x, y, width, height)` | 以四个标量构造。 | 全部参数必须有限。 |
| `x()` / `left()`，`y()` / `top()` | 读取左、上边坐标。 | 两组别名相等。 |
| `right()` / `bottom()` | 读取连续几何右、下边。 | 分别等于 `x()+width()`、`y()+height()`，没有减 1。 |
| `width()` / `height()` / `size()` | 读取浮点尺寸。 | 有效矩形的宽高均大于 0。 |
| `topLeft()` / `topRight()` / `bottomLeft()` / `bottomRight()` / `center()` | 读取角点或中心。 | 结果保留浮点精度。 |
| `isNull()` | 严格判断宽高都为 0。 | 近似零改用 `qFuzzyIsNull()`。 |
| `isEmpty()` | 宽或高小于等于 0。 | empty 与 invalid 等价。 |
| `isValid()` | 宽和高都大于 0。 | 交并等复杂操作前先保证有效。 |
| `normalized()` | 交换反向边，得到非负尺寸副本。 | 处理反向拖拽、镜像或外部数据。 |
| `setRect()` / `getRect()` | 按 `x,y,width,height` 设置或读取。 | 标量必须有限。 |
| `setCoords()` / `getCoords()` | 按左上、右下连续边坐标设置或读取。 | 不采用 `QRect` 的包含端点约定。 |
| `setLeft()` / `setRight()` / `setTop()` / `setBottom()` | 固定对边，改变尺寸。 | 指定坐标必须有限，可能得到 invalid。 |
| `setX()` / `setY()` | `setLeft()` / `setTop()` 的别名。 | 改变位置边，同时会改变尺寸。 |
| `setTopLeft()` / `setTopRight()` / `setBottomLeft()` / `setBottomRight()` | 设置一个角，固定对角。 | 可能生成负宽或高。 |
| `setWidth()` / `setHeight()` / `setSize()` | 固定左上角，设置尺寸。 | 尺寸必须有限；零或负值使其 invalid。 |
| `moveTo()` | 把左上角移动到指定位置。 | 尺寸不变，位置必须有限。 |
| `moveLeft()` / `moveRight()` / `moveTop()` / `moveBottom()` | 把指定边移动到目标位置。 | 尺寸不变，标量位置必须有限。 |
| `moveTopLeft()` / `moveTopRight()` / `moveBottomLeft()` / `moveBottomRight()` / `moveCenter()` | 以指定锚点平移整个矩形。 | 尺寸不变。 |
| `translate()` / `translated()` | 原地或副本式平移。 | 标量偏移必须有限；正值向右、下。 |
| `adjust()` / `adjusted()` | 独立移动四条边。 | 可能改变位置和尺寸；参数必须有限。 |
| `transposed()` | 返回宽高互换的副本。 | 左上角保持不变。 |
| `contains(QPointF)` / `contains(qreal, qreal)` | 判断点是否在内或边界上。 | 没有 `proper` 参数；严格内部需自行定义。 |
| `contains(QRectF)` | 判断矩形是否被完全包含。 | 边界也算包含。 |
| `intersects()` | 判断是否存在非空面积重叠。 | 只有边或点接触时为 false。 |
| `intersected()` / `operator&` / `operator&=` | 求交集。 | 无面积交集时结果 empty。 |
| `united()` / `operator|` / `operator|=` | 求最小包围矩形。 | 不是分离区域的精确并集。 |
| `marginsAdded()` / `marginsRemoved()` | 返回加/减 `QMarginsF` 后的矩形。 | 收缩过多会使矩形 invalid。 |
| `operator+=` / `operator-=` | 原地加/减浮点 margin。 | 改变当前对象。 |
| `operator+` / `operator-` | 非成员 margin 加减。 | 返回新矩形。 |
| `qFuzzyCompare(lhs, rhs)` | 近似比较两个矩形。 | Qt 6.8 起；适合显式表达容差意图。 |
| `qFuzzyIsNull(rect)` | 判断宽高是否都近似零。 | Qt 6.8 起；不同于严格 `isNull()`。 |
| `==` / `!=` | 对四个几何值进行模糊相等/不等比较。 | 不是严格身份比较，避免作精确键。 |
| `toRect()` | 转整数矩形，坐标取最接近整数。 | 不保证完全覆盖原矩形。 |
| `toAlignedRect()` | 转为完全覆盖原矩形的最小整数矩形。 | 重绘、裁剪和像素覆盖优先选择它。 |
| `fromCGRect()` / `toCGRect()` | 与 Core Graphics `CGRect` 转换。 | 仅 Apple 平台可用。 |
| `fromDOMRect()` / `toDOMRect()` | 与 Web `DOMRect` 转换。 | 仅 WebAssembly，Qt 6.5 起；输入必须是 DOMRect。 |
| `QDataStream <<` / `>>` | 序列化和反序列化。 | 流版本和跨端数据兼容性由调用方负责。 |

## 一句话总结

`QRectF` 用连续、有限的浮点坐标表达矩形：右下边界没有 `-1`，接边不算相交，比较是模糊的；保持浮点计算到最后，再按是否必须完整覆盖选择 `toAlignedRect()` 或 `toRect()`。
