<!-- 依据 Qt 6.11.1 头文件 qgraphicstransform.h 整理。 -->

# QGraphicsRotation 深入笔记

> 头文件：`#include <QGraphicsRotation>`  
> 模块：`Qt6::Widgets`  
> 继承：`QObject -> QGraphicsTransform -> QGraphicsRotation`

## 1. 它解决什么问题

`QGraphicsRotation` 是 Graphics View 变换链中的一条**三维旋转步骤**。它不负责绘制图元，而是告诉 `QGraphicsItem`：围绕哪个本地点、沿哪根三维轴、旋转多少角度。

只需要让二维图元在平面内转一转时，直接使用：

```cpp
item->setRotation(30.0);
```

通常已经足够。`QGraphicsRotation` 的价值在于两件事：

1. 它可以与 `QGraphicsScale` 等步骤按顺序组合。
2. 它支持绕 X、Y、Z 轴旋转，能做卡片翻页、透视倾斜等带深度感的效果。

常见使用场景：

- 翻牌、轮播卡片：绕 `Qt::YAxis` 旋转。
- 折叠面板或门轴效果：绕 `Qt::XAxis` 旋转。
- 图元编辑器：把旋转步骤作为独立对象交给属性动画或检查器面板。
- 需要多个变换连续叠加的节点、贴图或信息面板。

```text
QGraphicsItem
  └─ setTransformations(...)
       └─ QGraphicsRotation    // 一步旋转
QGraphicsTransform
  └─ QGraphicsRotation
```

## 2. 如何挂到图元上

先创建并配置旋转对象，再放进 `QGraphicsItem` 的变换列表：

```cpp
#include <QGraphicsItem>
#include <QGraphicsRotation>

auto *rotation = new QGraphicsRotation;
rotation->setOrigin(QVector3D(80.0, 45.0, 0.0));
rotation->setAxis(Qt::YAxis);
rotation->setAngle(35.0);

item->setTransformations({ rotation });
```

`setTransformations()` 会接管列表中对象的所有权，所以不应再手动 `delete rotation`，也不要把同一个变换对象挂到多个图元上。图元销毁或替换整个变换列表时，原来的变换对象也会随之销毁。

旋转会参与绘制、坐标映射和命中测试。对于绕 X/Y 轴的旋转，画面看起来有透视变化；但它仍是 Graphics View 在二维视图中用矩阵变换呈现的结果，而不是完整的 3D 场景系统。

## 3. 旋转由三个属性共同决定

### `origin`：转轴穿过哪里

`origin` 是旋转中心，使用**图元本地坐标**。一个 `160 x 90` 的卡片若要绕中心翻转，常写为：

```cpp
rotation->setOrigin(QVector3D(80.0, 45.0, 0.0));
```

默认原点是 `(0, 0, 0)`。不设置它时，图元会围绕自身左上附近的本地原点旋转，像是被一角钉住。这很适合“门轴”效果，但通常不是卡片翻转想要的结果。

### `axis`：绕哪根轴转

`axis` 是一个 `QVector3D`，表示旋转轴方向。最常用的写法是枚举重载：

```cpp
rotation->setAxis(Qt::XAxis);
rotation->setAxis(Qt::YAxis);
rotation->setAxis(Qt::ZAxis);
```

- `Qt::ZAxis`：绕垂直屏幕的轴转，视觉上最接近普通二维 `setRotation()`。
- `Qt::XAxis`：绕水平轴转，上下边缘产生远近变化。
- `Qt::YAxis`：绕垂直轴转，左右边缘产生远近变化，常用于翻牌。

`setAxis(const QVector3D &axis)` 适合需要任意斜轴的效果，例如绕 `(1, 1, 0)` 倾斜旋转。轴向量应有明确方向且不要是零向量；零向量没有可定义的旋转轴，会使结果没有业务意义。

### `angle`：转多少度

`angle` 的单位是度。正负方向由右手定则和所选轴决定，和预期相反时应先改正负号，而不是在多个变换之间硬调补偿。

角度可以超过 `360` 或小于 `0`；几何结果会按完整圈数循环。用于动画时，`0 -> 360` 表示完整翻转，`0 -> 180` 常表示翻到背面。

## 4. 顺序不是细节，而是效果本身

变换列表按顺序组合。比如翻牌常要配合横向缩放：

```cpp
auto *rotation = new QGraphicsRotation;
auto *scale = new QGraphicsScale;

item->setTransformations({ rotation, scale });
```

交换成 `{ scale, rotation }`，因为先作用的坐标轴不同，结果通常会改变。尤其当 `QGraphicsScale` 的 X/Y 倍率不相等时，这不是细微误差，而是完全不同的几何效果。

一个可靠的做法是先把需求描述为“以中心绕 Y 轴翻 180 度，再把宽度收至 90%”，再让对象列表保持同样的业务顺序。调试时同时打印 `axis()`、`angle()`、`origin()`，不要只盯着角度值。

## 5. 与二维旋转、矩阵旋转的选择

| 需求 | 适合方式 | 原因 |
| --- | --- | --- |
| 普通平面旋转 | `QGraphicsItem::setRotation()` | 简单、直接，足够处理绕 Z 轴的常规旋转。 |
| 已有 `QTransform` | `QGraphicsItem::setTransform()` | 适合一次性应用二维矩阵。 |
| 翻页、倾斜、可排序的多步旋转 | `QGraphicsRotation` | 支持 X/Y/Z 轴、原点和变换链。 |

不要把 `QGraphicsRotation` 当作所有旋转的默认方案。它解决的是“旋转成为独立可组合对象”的需求，而不是替代简单的 `setRotation()`。

## 6. 属性动画与状态通知

`QGraphicsRotation` 是 `QObject`，可直接作为 `QPropertyAnimation` 的目标：

```cpp
auto *animation = new QPropertyAnimation(rotation, "angle", rotation);
animation->setStartValue(0.0);
animation->setEndValue(180.0);
animation->setDuration(240);
animation->start(QAbstractAnimation::DeleteWhenStopped);
```

- `angleChanged()`：旋转角变化。
- `axisChanged()`：旋转轴变化。
- `originChanged()`：旋转中心变化。

大多数翻转动画只改变 `angle`，轴与中心保持固定。若每一帧同时改变轴、中心和角度，视觉会难以预测，也更难排查。

`QGraphicsRotation` 与目标 `QGraphicsItem` 都属于 GUI 线程对象；后台线程可计算动画参数，但必须通过队列信号等方式把 setter 调用安排回 GUI 线程。

## 7. API 逐项说明

### 构造与析构

- `QGraphicsRotation(QObject *parent = nullptr)`：创建一条旋转步骤。
- `~QGraphicsRotation()`：销毁旋转步骤；对象挂入图元后，由图元管理。

### 属性读写

- `origin()` / `setOrigin(const QVector3D &point)`：读取或设置本地坐标中的转轴中心。
- `angle()` / `setAngle(qreal angle)`：读取或设置旋转角度，单位为度。
- `axis()` / `setAxis(const QVector3D &axis)`：读取或设置任意三维旋转轴。
- `setAxis(Qt::Axis axis)`：使用 `Qt::XAxis`、`Qt::YAxis` 或 `Qt::ZAxis` 设置常用轴。

### 框架接口与信号

- `applyTo(QMatrix4x4 *matrix) const`：把旋转写入累计矩阵，供 Graphics View 内部调用。
- `originChanged()`、`angleChanged()`、`axisChanged()`：分别通知三项属性变化。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsRotation(QObject *parent = nullptr)` | 创建一条可加入图元变换链的旋转步骤。 | 交给 `setTransformations()` 后由图元接管。 |
| 析构 | `~QGraphicsRotation()` | 销毁旋转步骤。 | 已被图元接管时不要手动删除。 |
| 属性 | `origin : QVector3D` | 保存转轴穿过的本地坐标点。 | 默认 `(0, 0, 0)`；不是 scene 坐标。 |
| 读取 | `QVector3D origin() const` | 读取旋转中心。 | 用于检查图元为何像被某个角固定。 |
| 设置 | `void setOrigin(const QVector3D &point)` | 设置旋转中心。 | 卡片翻转一般取图元中心。 |
| 属性 | `angle : qreal` | 保存旋转角度，单位为度。 | 可为负值或超过 `360`。 |
| 读取 | `qreal angle() const` | 读取当前旋转角。 | 调试动画时可与 `axis()` 一起检查。 |
| 设置 | `void setAngle(qreal angle)` | 设置旋转角。 | 正负方向与所选轴有关。 |
| 属性 | `axis : QVector3D` | 保存旋转轴方向。 | 默认轴用于平面旋转；任意轴不可为零向量。 |
| 读取 | `QVector3D axis() const` | 读取当前旋转轴。 | 结果是向量形式，不一定是枚举轴。 |
| 设置 | `void setAxis(const QVector3D &axis)` | 设置任意三维方向的旋转轴。 | 适合斜轴效果；确保向量有明确非零方向。 |
| 设置 | `void setAxis(Qt::Axis axis)` | 使用 X、Y、Z 三个标准轴设置旋转轴。 | 翻牌通常用 `Qt::YAxis`，普通平面旋转用 `Qt::ZAxis`。 |
| 框架接口 | `void applyTo(QMatrix4x4 *matrix) const` | 将本旋转乘入累计矩阵。 | 由框架调用，普通业务代码不直接调用。 |
| 信号 | `void originChanged()` | 通知旋转中心改变。 | 用于同步检查器或编辑器控件。 |
| 信号 | `void angleChanged()` | 通知旋转角改变。 | `QPropertyAnimation` 更新时会频繁触发。 |
| 信号 | `void axisChanged()` | 通知旋转轴改变。 | 多数动画不需要逐帧改变轴。 |

## 9. 排查清单

1. 图元像绕角落翻转：为 `origin` 设置图元中心的本地坐标。
2. 翻转方向反了：先将 `angle` 的正负号取反，再确认所选轴。
3. 组合效果不对：检查 `setTransformations()` 列表顺序。
4. 看不出 X/Y 轴旋转：确认没有用纯二维逻辑覆盖图元变换，并在有足够尺寸的图元上观察。

### 一句话总结

`QGraphicsRotation` 让旋转成为图元变换链中独立、可动画的一步；用它处理 X/Y 轴翻转和多步骤组合，用 `setRotation()` 处理普通二维旋转。
