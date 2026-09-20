# QQuaternion::Axes：用三个正交轴表达一个三维旋转

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 头文件：`#include <QQuaternion>`  
> 所属模块：`Qt6::Gui`

`QQuaternion::Axes` 是 `QQuaternion` 内部的聚合结构，保存旋转所对应的三个正交单位轴：`x`、`y`、`z`。它本身没有成员函数，也不执行归一化、正交化或合法性检查；它的意义来自 `QQuaternion::toAxes()` 和 `QQuaternion::fromAxes()`。

相比只看四元数的四个浮点分量，轴结构更适合调试相机姿态、显示物体局部坐标系、将旋转交给需要三个基向量的渲染或物理代码。它也比欧拉角少一层旋转顺序和万向节锁的歧义。

## 它解决的问题

三维旋转通常既需要“旋转一个向量”，也需要知道旋转后的局部坐标系朝向。例如：

- 相机需要将右方向、上方向和前方向交给视图矩阵构造代码。
- 编辑器需要绘制对象的三个局部坐标轴。
- 机器人或飞行器姿态需要把四元数转换成三个基向量。
- 需要从三个已知正交方向重新生成旋转时，使用 `fromAxes()` 比手工推导四元数更直接。

```cpp
const QQuaternion rotation =
    QQuaternion::fromAxisAndAngle(QVector3D(0, 1, 0), 30.0f);

const QQuaternion::Axes axes = rotation.toAxes();
const QVector3D right = axes.x.toVector3D();
const QVector3D up = axes.y.toVector3D();
const QVector3D forward = axes.z.toVector3D();
```

这里的 `x`、`y`、`z` 不是四元数的 `x/y/z` 分量，而是旋转后的三个轴向量。不要把 `axes.x.x` 误解为四元数的 x 分量；它表示 x 轴向量的 x 坐标。

## 结构布局与构造

结构体只有三个公开字段：

```cpp
QQuaternion::Axes axes{
    {1.0f, 0.0f, 0.0f},
    {0.0f, 1.0f, 0.0f},
    {0.0f, 0.0f, 1.0f}
};
```

每个字段的类型是 `QQuaternion::Axis`，而 `Axis` 又公开 `float x, y, z`。因此 `Axes` 是可聚合初始化的普通值结构，不是拥有隐藏状态的对象。

手工构造时，调用方必须自行保证：

- 三个轴长度接近 `1`。
- 三个轴两两垂直。
- 三个轴组成所需的右手或左手坐标约定。
- 轴顺序与下游 API 的 x/y/z 约定一致。

`QQuaternion::fromAxes()` 不应被当作任意三个向量的“自动修复器”。若轴不正交、未归一化或方向约定相反，得到的结果可能不是预期的纯旋转。

## `toAxes()` 与 `fromAxes()` 的边界

`toAxes()` 从四元数返回定义该旋转的三个正交轴。旋转四元数应当是单位四元数；若四元数包含缩放信息，转换出的轴也不应被当作纯旋转基向量。

```cpp
QQuaternion q = source.normalized();
QQuaternion::Axes axes = q.toAxes();
QQuaternion rebuilt = QQuaternion::fromAxes(axes);
```

`QQuaternion::fromAxes(Axes)` 是 Qt 6.11 提供的结构体重载。Qt 还提供 `fromAxes(const QVector3D &, const QVector3D &, const QVector3D &)` 与 `getAxes(QVector3D *, QVector3D *, QVector3D *)` 作为不直接使用 `Axis` 字段的桥接接口。

若只想从已有四元数读取轴，优先调用 `toAxes()`；若只是把轴用于矩阵或向量计算，转换成 `QVector3D` 后使用。不要为了比较两个姿态直接比较三个浮点向量的 `operator==`，应使用 `qFuzzyCompare()` 或业务允许的误差。

## 和旋转矩阵、欧拉角的关系

`Axes` 可以看作旋转矩阵的三条基向量。它适合表达姿态坐标系，但不携带平移，也不表示缩放、剪切或投影。

- 需要连续插值时，保留 `QQuaternion`，使用 `slerp()` 或 `nlerp()`，不要先转成轴再逐分量插值。
- 需要给矩阵 API 时，使用 `toRotationMatrix()` 或将轴按目标矩阵约定放入列/行。
- 需要显示给用户时，使用欧拉角或轴角，但要明确旋转顺序、角度范围和奇异姿态。

四元数的 `q` 和 `-q` 表示同一个三维旋转；因此从等价四元数得到的轴应表达同一坐标系，即使底层分量符号不同。浮点误差会使轴长度和点积出现很小偏差，不要用精确相等判断几何合法性。

## 坐标系约定是调用方责任

Qt 的 `x`、`y`、`z` 字段只表示三个轴的命名，不会替你决定“前方是 +Z 还是 -Z”、矩阵是按行还是按列存储、屏幕 y 轴是否向下。渲染引擎、相机代码和物理引擎之间必须统一约定。

```cpp
const QQuaternion::Axes axes = cameraRotation.toAxes();
// 这里的 forward 取 z 轴还是 -z 轴，取决于项目的相机约定。
const QVector3D forward = axes.z.toVector3D();
```

如果轴的方向来自用户输入或传感器，先归一化并按项目约定建立右手系；否则重建出的四元数可能看似数值正常，却让相机左右翻转或模型朝向相反。

## 生命周期、线程与性能

`Axes` 是由三个浮点向量组成的轻量值类型，不拥有资源、不依赖事件循环，也没有 QObject 线程亲和性。可以按值返回、复制和在线程间传递。

但它只描述几何数据；如果来源是共享的渲染对象、传感器状态或场景节点，线程安全仍由来源对象和调用方同步策略决定。读取 `Axes` 本身不会锁住外部旋转对象。

## 常见错误

- 把 `Axes::x` 当成四元数的 x 分量，而不是一个完整的 `QQuaternion::Axis`。
- 手工填入三个未归一化或不正交向量后，期待 `fromAxes()` 自动修复。
- 未先 `normalized()` 就把包含缩放信息的四元数当成纯旋转分解。
- 在不同坐标系约定间直接把 `z` 当作 forward，导致相机或模型前后颠倒。
- 将轴向量逐分量线性插值作为旋转动画；应在四元数空间用 `slerp()` / `nlerp()`。
- 用精确浮点比较判断轴相同；应采用模糊比较或角度误差。

## API 速查表

| API / 成员 | 语义与使用边界 |
| --- | --- |
| `QQuaternion::Axes` | Qt 6.11 起提供的聚合结构，表示一个四元数对应的三个正交轴。 |
| `Axes::x` | `QQuaternion::Axis` 类型的 x 轴向量；不是四元数 x 分量。 |
| `Axes::y` | `QQuaternion::Axis` 类型的 y 轴向量；通常应与 x、z 正交。 |
| `Axes::z` | `QQuaternion::Axis` 类型的 z 轴向量；正负方向由项目坐标约定决定。 |
| 聚合初始化 `Axes{{...}, {...}, {...}}` | 直接创建三个轴；调用方负责长度、正交性和手性。 |
| `QQuaternion::toAxes()` | 从四元数取得三个正交轴；输入应代表纯旋转，必要时先归一化。 |
| `QQuaternion::fromAxes(Axes)` | 从 `Axes` 重建四元数；不会替调用方验证或修复任意轴组。 |
| `QQuaternion::getAxes(QVector3D *, QVector3D *, QVector3D *)` | 将三个轴直接写入 `QVector3D` 输出参数；指针必须有效。 |
| `QQuaternion::fromAxes(xAxis, yAxis, zAxis)` | 从三个 `QVector3D` 轴重建四元数；轴的正交归一和坐标约定由调用方保证。 |
| `QQuaternion::Axis::toVector3D()` | 将单个轴字段转换为 `QVector3D`，便于矩阵、点积和绘制。 |
| `QQuaternion::Axis::fromVector3D()` | 从 `QVector3D` 创建一个轴值；不执行归一化或正交化。 |
