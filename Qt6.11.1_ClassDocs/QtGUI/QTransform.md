# QTransform

> Qt 6.11.1 · Qt GUI · 来自 `QTransform`

## 1. 先建立直觉

`QTransform` 是二维齐次 3x3 矩阵，统一表达平移、缩放、旋转、剪切与透视投影。它既可以交给 `QPainter` 改变后续绘制坐标，也可以直接把点、路径、矩形和区域从一个坐标空间映射到另一个。

最容易犯错的是组合顺序：连续 `translate()`、`rotate()`、`scale()` 不是“彼此独立的属性”，而是矩阵相乘。要先明确你要表达的是“先移动对象再旋转”还是“先旋转坐标系再移动”，并以实际点的 map 结果测试。

## 2. 类说明

- 头文件：`#include <QTransform>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：轻量值类型，适合按值保存于图元、视图状态和命中测试逻辑。
- 默认构造为恒等变换；`reset()` 同样恢复恒等矩阵。
- `QPainter` 自身维护一个 world transform；局部绘制通常用 `painter.save()`、设置 transform、绘制、`restore()`，不要污染后续绘制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTransform()` / `reset()` | 创建或恢复恒等矩阵 |
| `translate(dx, dy)` / `fromTranslate()` | 追加平移；静态版本直接构造 |
| `scale(sx, sy)` / `fromScale()` | 追加缩放；静态版本直接构造 |
| `rotate(degrees[, axis, distance])` | 追加角度制旋转，支持 Qt 6.5 的伪 3D 投影 |
| `rotateRadians()` | 追加弧度制旋转 |
| `shear(sh, sv)` | 追加水平/垂直剪切 |
| `operator*` / `operator*=` | 组合两个矩阵，顺序影响结果 |
| `map(point/line/path/polygon/region)` | 精确映射对应的几何对象 |
| `mapRect(rect)` | 返回变换后图形的轴对齐包围盒 |
| `mapToPolygon(rect)` | 将矩形映射为四边形，保留旋转/剪切形状 |
| `inverted(&ok)` / `isInvertible()` | 获取逆矩阵，用于屏幕到模型命中测试 |
| `determinant()` / `adjoint()` | 低层矩阵诊断和计算 |
| `isAffine()` | 判断是否无透视成分 |
| `isIdentity()` / `isTranslating()` / `isScaling()` / `isRotating()` | 快速分类和优化提示 |
| `type()` | 返回复杂度最高的 `TransformationType` |
| `quadToQuad()` | 求一个四边形到另一四边形的透视变换 |
| `quadToSquare()` / `squareToQuad()` | 在单位方形与四边形间求映射 |
| `m11...m33()` / `setMatrix()` | 读取/设置原始矩阵元素，适合算法或序列化 |
| `transposed()` | 返回转置矩阵 |
| `qFuzzyCompare()` / `qHash()` / 数据流运算符 | 浮点比较、缓存键与持久化 |

## 4. 关键用法

### 在 painter 中隔离局部坐标系

```cpp
void drawNeedle(QPainter &p, QPointF center, qreal angle)
{
    p.save();
    p.translate(center);
    p.rotate(angle);
    p.drawLine(QPointF(0, 0), QPointF(0, -80));
    p.restore();
}
```

这里以 center 建立局部原点，再旋转坐标轴，因此针可以按固定局部坐标绘制。`save()`/`restore()` 是关键：若遗漏 restore，后续文字、背景和其他部件都会继承该变换。

### 用逆矩阵进行命中测试

```cpp
bool Item::containsScreenPoint(QPointF screenPoint) const
{
    bool ok = false;
    const QTransform inverse = localToScreen.inverted(&ok);
    if (!ok)
        return false; // 缩放为 0 等奇异矩阵无法反向映射

    return localBounds.contains(inverse.map(screenPoint));
}
```

视图呈现走“模型坐标 -> 屏幕坐标”，鼠标命中通常反过来走逆变换。不要用 `mapRect()` 的包围盒替代精确命中：旋转对象会在包围盒空角落被错误命中。

### 区分包围盒与真实四边形

```cpp
const QRectF source(0, 0, 160, 80);
const QTransform t = QTransform().rotate(30);

const QRectF bounds = t.mapRect(source);     // 轴对齐外包框
const QPolygon precise = t.mapToPolygon(source.toRect());
```

`mapRect()` 适合脏区、粗略布局和裁剪范围；旋转或剪切后它会扩张成外接矩形。需要绘制边框、选择框或几何相交时用 path/polygon 映射，避免视觉和交互不一致。

### 让四边形贴到透视平面

```cpp
QTransform projection;
const QPolygonF source{
    {0, 0}, {1, 0}, {1, 1}, {0, 1}
};
const QPolygonF target{
    {50, 30}, {220, 55}, {190, 180}, {70, 160}
};

if (QTransform::quadToQuad(source, target, projection))
    painter.setTransform(projection);
```

四边形必须是有效、非退化的映射关系；失败时不要继续使用未初始化或旧的 `projection`。透视变换会改变直线以外的几何分布，也会让简单的矩形裁剪与反变换更复杂。

## 5. 变换类型速查

| `TransformationType` | 含义 |
| --- | --- |
| `TxNone` | 恒等变换 |
| `TxTranslate` | 只有平移 |
| `TxScale` | 含缩放，180/360 度旋转可能也会被归类于此 |
| `TxRotate` | 含普通旋转 |
| `TxShear` | 含剪切 |
| `TxProject` | 含透视投影 |

`type()` 是优化提示，不能取代数学判断。例如你不能仅因 `isRotating()` 为 false 就假定几何未发生视觉旋转，180 度有其特殊分类。

## 6. 常见坑与经验

- **矩阵顺序要用样例点验证。** 对同一矩阵调用顺序写成不同排列，结果可能完全不同；团队约定局部到世界、世界到屏幕的组合顺序。
- **整数 map 会取整。** 需要精确几何使用 `QPointF`、`QRectF`、`QPolygonF`、`QPainterPath`，不要过早落到 `QPoint`/`QRect`。
- **逆矩阵可能不存在。** 缩放为 0、退化投影等都导致不可逆；使用 `inverted(&ok)` 而不是忽略失败返回的恒等矩阵。
- **角度 API 的单位不一致。** `rotate()` 用度，`rotateRadians()` 用弧度；不要把 `M_PI` 直接传给前者。
- **Widget 坐标 y 轴向下。** 在数学坐标中逆时针的旋转，屏幕观感可能是顺时针；用视觉测试确认交互旋转方向。
- **Qt 6.5 的 X/Y axis rotate 是投影效果。** `distanceToPlane` 影响透视强度，不能把它当完整 3D 场景矩阵；真正 3D 管线使用 `QMatrix4x4`。

## 7. 知识点覆盖

二维齐次矩阵、坐标空间、变换组合、局部绘制、逆变换命中测试、包围盒与精确几何、透视四边形映射、浮点精度、widget 坐标方向、2D/3D 边界。
