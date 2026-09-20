# QVector3D

> Qt 6.11.1 · Qt GUI · 来自 `QVector3D`

## 1. 先建立直觉

`QVector3D` 是三维数学向量 `(x, y, z)`。它可表达模型中的位置、方向、速度、表面法线和颜色三元组；同样，它不是 Qt 容器。它的价值在于将“空间关系”变成明确的点积、叉积、距离和投影运算。

三维计算里最常见的语义错误是把位置当方向。位置受平移影响，方向与法线不应受平移影响；当这些数据进入 `QMatrix4x4` 或 `QVector4D` 时，这一区别决定 `w` 应为 1 还是 0。

## 2. 类说明

- 头文件：`#include <QVector3D>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 对象模型：可复制的 `float` 三元组；不关联线程或事件循环。
- 协作类型：`QMatrix4x4` 用于模型/观察/投影变换，`QVector4D` 用于齐次坐标，`QRect` 表示投影视口。

## 3. API 速查

| API | 用途 |
|---|---|
| `QVector3D(x, y, z)` | 构造三维向量。 |
| `x()` / `y()` / `z()`，对应 setters | 读取或修改分量。 |
| `length()` / `lengthSquared()` | 向量模长与模长平方。 |
| `normalize()` / `normalized()` | 得到单位方向或单位法线。 |
| `dotProduct(a, b)` | 测量两个方向的对齐程度。 |
| `crossProduct(a, b)` | 得到垂直于二者平面的向量，方向遵守右手法则。 |
| `normal(a, b)` | 返回两个非平行向量的单位法线。 |
| `normal(p1, p2, p3)` | 返回三点构成三角形的单位法线。 |
| `distanceToPoint()` | 到另一点的距离。 |
| `distanceToLine()` | 到一条直线的最短距离。 |
| `distanceToPlane()` | 到平面的有符号距离。 |
| `project()` | 从模型坐标变到窗口坐标。 |
| `unproject()` | 从窗口坐标反推模型坐标。 |
| `toVector2D()` / `toVector4D()` | 降维或扩展维度。 |
| `qFuzzyCompare()` | 容忍浮点误差的向量比较。 |

## 4. 关键用法

### 计算三角形法线

```cpp
const QVector3D p0(0.0f, 0.0f, 0.0f);
const QVector3D p1(1.0f, 0.0f, 0.0f);
const QVector3D p2(0.0f, 1.0f, 0.0f);

const QVector3D normal = QVector3D::normal(p0, p1, p2);
```

法线方向取决于顶点绕序：交换 `p1` 和 `p2` 会反转法线。退化三角形的三点共线，不能产生可信法线；网格导入或动态几何中，应检测边叉积的 `lengthSquared()` 是否接近零。

### 平面距离与正反面判断

```cpp
const QVector3D planePoint(0.0f, 0.0f, 0.0f);
const QVector3D planeNormal(0.0f, 1.0f, 0.0f); // 已归一化
const float signedDistance =
    cameraPosition.distanceToPlane(planePoint, planeNormal);
```

返回值正负由法线方向决定：正值在法线一侧，负值在背面，零表示在平面上。双参数重载假定 `normal` 是单位向量；未归一化的法线会使“距离”带上法线长度的缩放。

### 从 3D 投影到 Qt 窗口坐标

```cpp
QVector3D screen = worldPoint.project(modelView, projection, viewport);
screen.setY(viewport.height() - screen.y()); // 转为 Qt 顶部原点坐标
```

`project()` / `unproject()` 采用 OpenGL 视口方向，即 y=0 位于底部；Qt 传统控件坐标则以顶部为原点。鼠标拾取时要翻转 y，并确保 `modelView`、`projection` 与真正渲染时完全一致，否则反投影出的射线不会命中画面对象。

## 5. 使用场景

| 场景 | 使用方式 |
|---|---|
| 光照与背面剔除 | 三角形法线、视线与法线的点积。 |
| 物体移动与相机控制 | 位置差归一化为移动方向。 |
| 碰撞、切平面与裁剪 | `distanceToPlane()` 的符号作为空间侧别。 |
| 编辑器选取、标注 | `project()` 映射到屏幕，`unproject()` 重建空间点或射线。 |
| 2D/3D 数据桥接 | 从 `QPointF` 构造，或转为 `QVector4D` 进入矩阵管线。 |

## 6. 常见坑与经验

- `crossProduct()` 的结果长度是 `|a| * |b| * sin(theta)`；若需要单位法线，调用 `normal()` 或自行归一化。
- `normal(v1, v2)` 要求两向量不平行；三点版本要求三点不共线。
- `operator*(a, b)` 仍是逐分量乘法；它不是点积，也不是叉积。
- 零向量归一化后仍是零向量。不要把它送入假定单位方向的 `distanceToLine()` 或平面计算。
- `project()` 的 z 是深度空间的结果，不要直接当作世界坐标距离。
- 精确 `operator==` 对浮点几何通常过于严格；使用 `qFuzzyCompare()` 或与业务尺度匹配的 epsilon。

## 7. 知识点覆盖

- 位置、方向、法线的空间语义
- 点积、叉积、右手法则与顶点绕序
- 直线和有符号平面距离
- 退化几何检测
- 模型、观察、投影矩阵与 OpenGL/Qt y 轴方向差异
