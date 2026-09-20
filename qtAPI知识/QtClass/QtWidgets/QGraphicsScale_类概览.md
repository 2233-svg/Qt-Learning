<!-- 依据 Qt 6.11.1 头文件 qgraphicstransform.h 整理。 -->

# QGraphicsScale 深入笔记

> 头文件：`#include <QGraphicsScale>`  
> 模块：`Qt6::Widgets`  
> 继承：`QObject -> QGraphicsTransform -> QGraphicsScale`

## 1. 它解决的不是“把图元放大”这么简单

`QGraphicsScale` 是 Graphics View 中一条**可组合的缩放变换步骤**。它不绘制内容，也不持有图元；它描述“在变换链走到这里时，按 X、Y、Z 三个方向各缩放多少，以及围绕哪里缩放”。

最简单的缩放可以直接写：

```cpp
item->setScale(1.5);
```

但这只有一个统一倍率，且和图元自身的旋转、平移等基本变换混在一起。当一个图元需要“先绕某点旋转，再横向拉宽，最后做透视感的 Z 向缩放”，或者需要分别动画化各阶段时，`QGraphicsScale` 才是合适的工具。

典型场景：

- 图片编辑器的选中对象：横向拉伸和纵向拉伸独立控制。
- 节点图或时间轴：节点整体缩放，但文字和图标可安排在不同变换步骤中。
- 卡片翻转、拟物 3D 效果：配合 `QGraphicsRotation` 使用 Z 方向缩放。
- `QPropertyAnimation`：分别对 `xScale`、`yScale` 或 `origin` 做平滑动画。

它的继承关系很短，但分工很明确：

```text
QGraphicsItem
  └─ setTransformations(...)
       └─ QGraphicsScale     // 一步缩放
QGraphicsTransform
  └─ QGraphicsScale
```

`QGraphicsTransform` 负责“可挂入图元变换列表”的通用协议；`QGraphicsScale` 只补上缩放所需的参数。

## 2. 先看完整的使用路径

`QGraphicsScale` 作为 `QObject` 使用，通常在堆上创建，再交给一个图元的变换列表：

```cpp
#include <QGraphicsItem>
#include <QGraphicsScale>

auto *scale = new QGraphicsScale;
scale->setOrigin(QVector3D(50.0, 30.0, 0.0));
scale->setXScale(1.4);
scale->setYScale(0.8);

item->setTransformations({ scale });
```

调用 `QGraphicsItem::setTransformations()` 后，图元会接管列表中变换对象的所有权；不要再手动 `delete scale`。同一个 `QGraphicsScale` 也不应同时交给多个图元。

图元重绘、命中测试和坐标映射都会使用这条变换链。也就是说，缩放不只是视觉效果：`mapToScene()`、鼠标命中区域、子图元的坐标关系都会受它影响。

## 3. 三个倍率和一个原点

### `xScale`、`yScale`、`zScale`

三个倍率的默认值都是 `1.0`，即不缩放。

- `xScale`：沿本地图元 X 轴缩放。大于 `1` 拉宽，小于 `1` 压窄。
- `yScale`：沿本地图元 Y 轴缩放。大于 `1` 拉高，小于 `1` 压扁。
- `zScale`：沿 Z 轴缩放。普通二维绘制里往往没有肉眼可见的效果；它主要在与三维旋转或 `QMatrix4x4` 变换组合时才有意义。

倍率为 `0` 会把对应方向压到一条线或一个点，用户也无法再通过常规命中测试轻松选中它。实际交互式编辑器通常应限制一个很小的正值，而不是允许缩到零。

负倍率会发生镜像。例如 `setXScale(-1.0)` 可做左右翻转；但文字、方向性图标和鼠标交互的视觉预期也会随之反转，应有意使用。

### `origin`

`origin` 是缩放中心，坐标属于**图元本地坐标系**，不是 scene 坐标，也不是视图像素坐标。

例如一个 `100 x 60` 的矩形，若希望从中心放大，中心应是：

```cpp
scale->setOrigin(QVector3D(50.0, 30.0, 0.0));
```

若不设置原点，默认围绕 `(0, 0, 0)` 缩放，常见结果是图元看起来向右下或左上“跑掉了”。这不是布局错误，而是缩放围绕左上本地原点发生的正常几何结果。

## 4. 变换顺序决定最终画面

`setTransformations()` 接收的是一个有顺序的列表。矩阵变换不可交换，下面两段通常结果不同：

```cpp
item->setTransformations({ rotation, scale });
```

```cpp
item->setTransformations({ scale, rotation });
```

第一种是旋转和缩放按列表顺序组合，第二种则先缩放坐标轴再旋转。对各向异性缩放（`xScale != yScale`）而言，这个差异尤其明显。

因此，编写复杂效果时应先用一句业务语言定顺序，例如“卡片以中心绕 Y 轴翻转，同时沿 X 轴轻微收窄”，再按这个顺序组织 `QGraphicsRotation` 与 `QGraphicsScale`。不要在效果不对时盲目调数值，先检查列表顺序和每一步的 `origin`。

## 5. 与 `setScale()`、`setTransform()` 怎么选

| 需求 | 合适 API | 原因 |
| --- | --- | --- |
| 整个图元等比缩放 | `QGraphicsItem::setScale()` | 写法短，状态简单。 |
| 一次性给定二维矩阵 | `QGraphicsItem::setTransform()` | 适合已有 `QTransform` 的场景。 |
| 分轴缩放、3D 旋转、多个可动画步骤 | `QGraphicsScale` | 每一步独立、可观察、可重排。 |

不要为了普通的“放大 1.2 倍”引入变换链；也不要在需要独立控制多个步骤时把全部逻辑塞进一个 `QTransform`，后者会很难做属性动画和局部调整。

## 6. 动画和通知

这是一个带 `Q_PROPERTY` 的 `QObject`，因此可以直接动画化：

```cpp
auto *animation = new QPropertyAnimation(scale, "xScale", scale);
animation->setStartValue(1.0);
animation->setEndValue(1.25);
animation->setDuration(160);
animation->start(QAbstractAnimation::DeleteWhenStopped);
```

`xScaleChanged()`、`yScaleChanged()`、`zScaleChanged()` 和 `originChanged()` 分别表示对应属性变化；`scaleChanged()` 是任意一个缩放倍率变化时的汇总通知。若界面只需知道“缩放变了”，连接汇总信号即可；若要区分具体方向，再连接单独的信号。

这类对象和图元都应在 GUI 线程中创建、修改和销毁。跨线程计算倍率可以，但把结果交回 GUI 线程后再调用 setter。

## 7. API 逐项说明

### 构造与析构

- `QGraphicsScale(QObject *parent = nullptr)`：创建一条缩放步骤。实际挂到 `QGraphicsItem` 前，可以用 `parent` 管理临时生命周期；一旦交给 `setTransformations()`，由图元接管更清晰。
- `~QGraphicsScale()`：销毁对象。已被图元接管时无需手动销毁。

### 属性访问

- `origin()` / `setOrigin(const QVector3D &point)`：读取或设置本地坐标中的缩放中心。
- `xScale()` / `setXScale(qreal factor)`：读取或设置 X 方向倍率。
- `yScale()` / `setYScale(qreal factor)`：读取或设置 Y 方向倍率。
- `zScale()` / `setZScale(qreal factor)`：读取或设置 Z 方向倍率。

### 框架协作

- `applyTo(QMatrix4x4 *matrix) const`：把本对象的缩放步骤乘入矩阵。正常业务代码不直接调用它；`QGraphicsItem` 在计算自身变换时调用。自定义 `QGraphicsTransform` 子类才需要实现同名虚函数。

### 通知信号

- `originChanged()`：缩放中心改变。
- `xScaleChanged()`、`yScaleChanged()`、`zScaleChanged()`：对应轴倍率改变。
- `scaleChanged()`：任意轴倍率改变。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsScale(QObject *parent = nullptr)` | 创建一条可放入图元变换链的缩放步骤。 | 通常由 `QGraphicsItem::setTransformations()` 接管所有权。 |
| 析构 | `~QGraphicsScale()` | 销毁缩放步骤。 | 已交给图元时不要手动删除。 |
| 属性 | `origin : QVector3D` | 保存缩放中心。 | 是图元本地坐标；默认是 `(0, 0, 0)`。 |
| 读取 | `QVector3D origin() const` | 取得当前缩放中心。 | 读到的是本地坐标，不是 scene 坐标。 |
| 设置 | `void setOrigin(const QVector3D &point)` | 指定围绕哪个点缩放。 | 图元看似“位移”时先检查此值。 |
| 属性 | `xScale : qreal` | 保存 X 方向缩放倍率。 | 默认 `1.0`；负值会左右镜像。 |
| 读取 | `qreal xScale() const` | 取得 X 方向倍率。 | `0` 会把图元在此轴压平。 |
| 设置 | `void setXScale(qreal factor)` | 设置 X 方向倍率。 | 交互式缩放通常应限制最小正值。 |
| 属性 | `yScale : qreal` | 保存 Y 方向缩放倍率。 | 默认 `1.0`；负值会上下镜像。 |
| 读取 | `qreal yScale() const` | 取得 Y 方向倍率。 | 和 X 轴倍率不同会产生非等比缩放。 |
| 设置 | `void setYScale(qreal factor)` | 设置 Y 方向倍率。 | 注意与旋转的变换顺序。 |
| 属性 | `zScale : qreal` | 保存 Z 方向缩放倍率。 | 纯二维画面通常需配合 3D 旋转才明显。 |
| 读取 | `qreal zScale() const` | 取得 Z 方向倍率。 | 默认 `1.0`。 |
| 设置 | `void setZScale(qreal factor)` | 设置 Z 方向倍率。 | 主要用于带 3D 变换的组合效果。 |
| 框架接口 | `void applyTo(QMatrix4x4 *matrix) const` | 将本缩放写入累计变换矩阵。 | 由 Graphics View 调用，业务代码通常不直接调用。 |
| 信号 | `void originChanged()` | 通知缩放中心改变。 | 用于同步编辑器控件或动画状态。 |
| 信号 | `void xScaleChanged()` | 通知 X 轴倍率改变。 | 只关心横向缩放时连接它。 |
| 信号 | `void yScaleChanged()` | 通知 Y 轴倍率改变。 | 只关心纵向缩放时连接它。 |
| 信号 | `void zScaleChanged()` | 通知 Z 轴倍率改变。 | 常用于三维效果参数面板。 |
| 信号 | `void scaleChanged()` | 通知任意一个轴的倍率改变。 | 不区分轴时比连接三个单独信号更方便。 |

## 9. 排查清单

1. 图元缩放后位置不对：检查 `origin` 是否按图元本地坐标设置。
2. 旋转加缩放的效果不对：检查 `setTransformations()` 中对象的先后顺序。
3. 缩放没有生效：确认对象已交给正确的图元，且该图元仍在 scene 中。
4. 动画没有画面更新：确认动画的目标是该 `QGraphicsScale`，并且 GUI 线程事件循环正在运行。

### 一句话总结

`QGraphicsScale` 用于把“缩放”拆成一条可组合、可动画、可独立观察的图元变换步骤；重点始终是本地原点、各轴倍率和变换列表的顺序。
