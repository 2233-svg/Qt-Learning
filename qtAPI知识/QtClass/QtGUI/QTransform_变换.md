# QTransform 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTransform>`  
> 所属模块：`Qt6::Gui`

## 1. 它解决什么问题

`QTransform` 是 Qt 的二维齐次变换矩阵。它把平移、缩放、旋转、错切和透视投影统一放进一个 3x3 矩阵里，用来把一个坐标系中的点、线、矩形、路径或区域映射到另一个坐标系。

典型场景包括 `QPainter` 绘制前设置坐标变换、图形编辑器中的画布缩放和平移、命中测试时把屏幕坐标转回模型坐标、把图片或矢量路径做旋转/透视变形，以及在缓存几何时批量映射 `QPainterPath`、`QPolygonF` 或 `QRegion`。

## 2. 矩阵语义和坐标映射

默认构造得到单位矩阵。6 参数构造用于仿射变换，等价于固定 `m13 = 0`、`m23 = 0`、`m33 = 1`；9 参数构造用于完整投影矩阵。Qt 的二维映射可以按下面的形式记忆：

```text
x' = m11 * x + m21 * y + dx
y' = m12 * x + m22 * y + dy
w' = m13 * x + m23 * y + m33
非仿射时最终点为 (x' / w', y' / w')
```

其中 `dx()` 是 `m31()`，`dy()` 是 `m32()`。如果只做平移、缩放、旋转、错切，优先用 `translate()`、`scale()`、`rotate()`、`shear()` 这样的语义函数；只有在导入外部矩阵、做投影或需要完全控制元素时再直接使用 `setMatrix()`。

## 3. 使用场景中的几个边界

矩阵乘法不满足交换律，`a * b` 与 `b * a` 的效果通常不同。连续调用 `translate()`、`scale()`、`rotate()` 时，最好用一个具体点调用 `map()` 验证结果，尤其是在“围绕某个中心缩放/旋转”这类需求中。

`mapRect()` 返回映射后的轴对齐矩形。旋转或错切后它通常是外接矩形，而不是四个角连成的真实四边形；需要精确四角时用 `mapToPolygon()` 或直接映射 `QPolygonF`。

`inverted()` 只有在矩阵可逆时才有业务意义。传入 `bool *invertible` 可以区分“得到的矩阵是真逆矩阵”还是“原矩阵奇异导致不可逆”。浮点比较不要直接依赖 `operator==`；判断近似相等用 `qFuzzyCompare()`。

## 4. 与绘制系统协作

`QTransform` 是值类型，可复制、可放入 `QVariant`，本身不拥有平台图形资源。它常与 `QPainter::setTransform()`、`QPainter::worldTransform()`、`QGraphicsItem`、`QPainterPath`、`QRegion` 等类型组合。

```cpp
QTransform view;
view.translate(width() / 2.0, height() / 2.0);
view.scale(zoom, zoom);
view.rotate(angle);

bool ok = false;
const QPointF scenePos = view.inverted(&ok).map(mousePos);
if (ok)
    selectAt(scenePos);
```

上例只有在矩阵可逆时才适合把鼠标坐标映射回场景。实际代码中应检查 `inverted(&ok)` 的 `ok`，防止缩放为 0 或投影矩阵退化。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `enum TransformationType` | 描述矩阵复杂度：`TxNone`、`TxTranslate`、`TxScale`、`TxRotate`、`TxShear`、`TxProject`。 | `type()` 返回能覆盖当前矩阵的最高复杂度，适合优化分支，不是互斥“开关集合”。 |
| `QTransform()` | 创建单位矩阵。 | 映射任何点都保持原坐标。 |
| `QTransform(m11, m12, m21, m22, dx, dy)` | 创建仿射矩阵。 | 没有透视项；适合平移、缩放、旋转、错切组合。 |
| `QTransform(m11, m12, m13, m21, m22, m23, m31, m32, m33)` | 创建完整 3x3 矩阵。 | 可表达投影；错误的 `m33` 或透视项容易导致除以接近 0 的 `w'`。 |
| `m11()` / `m12()` / `m13()` | 读取第一行矩阵元素。 | 直接读元素适合调试和序列化；业务含义要结合整体矩阵。 |
| `m21()` / `m22()` / `m23()` | 读取第二行矩阵元素。 | 旋转、缩放、错切会同时影响多个元素。 |
| `m31()` / `m32()` / `m33()` | 读取第三行矩阵元素。 | `m31`/`m32` 分别对应 `dx`/`dy`；`m33` 影响齐次归一化。 |
| `dx()` / `dy()` | 读取平移分量。 | 只代表矩阵中的平移元素，不等于复合变换后的视觉位移总效果。 |
| `setMatrix(...)` | 用 9 个元素替换整个矩阵。 | 会覆盖旧值；只改一个元素也要提供完整矩阵。 |
| `reset()` | 恢复为单位矩阵。 | 会清掉此前所有平移、缩放、旋转等。 |
| `translate(dx, dy)` | 在当前矩阵上加入坐标系平移并返回自身引用。 | 与已有缩放/旋转组合时，视觉效果取决于调用顺序。 |
| `scale(sx, sy)` | 加入水平和垂直缩放。 | `sx` 或 `sy` 为 0 会让矩阵不可逆。 |
| `shear(sh, sv)` | 加入水平/垂直错切。 | 错切后矩形通常不再保持轴对齐。 |
| `rotate(a, axis)` | 按角度旋转，默认围绕 `Qt::ZAxis`。 | X/Y 轴旋转会引入投影效果；Qt 6.5 起有带 `distanceToPlane` 的重载。 |
| `rotateRadians(a, axis)` | 用弧度而不是角度旋转。 | 与 `rotate()` 单位不同，混用时最容易出错。 |
| `fromTranslate(dx, dy)` | 创建只包含平移的矩阵。 | 比先默认构造再 `translate()` 更直接。 |
| `fromScale(sx, sy)` | 创建只包含缩放的矩阵。 | 仍要避免 0 缩放造成不可逆。 |
| `map(x, y, *tx, *ty)` | 映射数值坐标并通过输出参数返回。 | 输出指针必须有效；非仿射矩阵会做齐次除法。 |
| `map(const QPoint &)` / `map(const QPointF &)` | 映射单个点。 | 整数点版本会返回整数坐标，精度敏感时用 `QPointF`。 |
| `map(const QLine &)` / `map(const QLineF &)` | 映射线段两个端点。 | 投影变换下视觉直线仍按端点映射；复杂形状用路径。 |
| `map(const QPolygon &)` / `map(const QPolygonF &)` | 映射多边形所有顶点。 | 顶点数不变；只改变坐标。 |
| `map(const QPainterPath &)` | 映射绘制路径。 | 适合保留曲线和路径结构；成本高于单点映射。 |
| `map(const QRegion &)` | 映射区域。 | 复杂区域和非仿射变换可能带来较高计算成本。 |
| `mapRect(const QRect &)` / `mapRect(const QRectF &)` | 返回映射后的轴对齐外接矩形。 | 旋转/错切后不是精确四边形。 |
| `mapToPolygon(const QRect &)` | 把矩形四角映射为多边形。 | 需要真实角点时优先用它而不是 `mapRect()`。 |
| `determinant()` | 计算矩阵行列式。 | 接近 0 表示不可逆或数值不稳定。 |
| `isInvertible()` | 判断矩阵是否可逆。 | 使用浮点近似判断；严格业务仍建议调用 `inverted(&ok)`。 |
| `inverted(bool *invertible = nullptr)` | 返回逆矩阵。 | 用 `invertible` 判断结果是否有效。 |
| `adjoint()` | 返回伴随矩阵。 | 主要用于矩阵代数；普通绘制代码较少直接调用。 |
| `transposed()` | 返回转置矩阵。 | 不等于逆矩阵。 |
| `type()` | 返回当前矩阵的复杂度分类。 | 可用于走平移/缩放等快速路径。 |
| `isIdentity()` | 判断是否单位矩阵。 | 浮点构造后的近似值可能影响判断。 |
| `isAffine()` | 判断是否不含投影项。 | 仿射矩阵仍可能包含旋转、缩放、错切。 |
| `isTranslating()` / `isScaling()` / `isRotating()` | 查询矩阵复杂度是否至少包含相应类别。 | 这是按 `type()` 分类的便利判断，不要当作独立标志位。 |
| `squareToQuad()` / `quadToSquare()` / `quadToQuad()` | 构造单位方形与四边形之间的投影变换。 | 四边形退化时返回 `false`；调用方要检查返回值。 |
| `operator*(const QTransform &)` / `operator*=` | 组合两个矩阵。 | 乘法顺序会改变结果。 |
| `operator*=(qreal)` / `operator/=(qreal)` / `operator+=` / `operator-=` | 对矩阵元素做标量运算。 | 这是逐元素数学操作，不是“整体缩放坐标系”的同义词。 |
| `operator==` / `operator!=` | 精确比较矩阵元素。 | 浮点结果来自计算时优先用 `qFuzzyCompare()`。 |
| `operator QVariant()` | 转为 `QVariant` 保存或传递。 | 取回时仍要确认类型。 |
| `qFuzzyCompare(t1, t2)` | 近似比较两个矩阵。 | 适合浮点变换结果校验。 |
| `qHash(transform, seed)` | 为哈希容器计算哈希值。 | 与浮点近似相等无关，哈希依据实际元素值。 |
| `QDataStream <<` / `>>` | 序列化和反序列化矩阵。 | 流版本和数据格式要与应用兼容策略一致。 |

## 5. 记忆重点

`QTransform` 是“坐标系映射”而不是简单的几何属性包。平移、旋转、缩放的顺序会改变结果；矩形映射要区分外接矩形和真实四角；反向命中测试前一定确认矩阵可逆。
