# QGraphicsTransform：Graphics View 的可组合变换步骤

> Qt 6.11.1 · `#include <QGraphicsTransform>` · 模块：`Qt6::Widgets` · 继承：`QObject`

`QGraphicsTransform` 是给 `QGraphicsItem` 构建高级变换链的抽象基类。相比直接设置一个 `QTransform`，它把缩放、旋转或自定义矩阵操作拆成可独立配置、可动画的对象，再按顺序组合到 item 上。

## 使用场景

常用的是现成派生类 `QGraphicsScale` 和 `QGraphicsRotation`。例如把一个 3D 旋转对象放进 item 的 transformations 列表，再用 `QPropertyAnimation` 动画它的 angle。多个 `QGraphicsTransform` 会按列表顺序逐个应用，顺序不同结果也不同。

只有现有 scale/rotation 不够表达时才需要自定义派生类，例如自定义投影、剪切、依赖业务参数的矩阵操作。

## 自定义边界

派生类必须实现 `applyTo(QMatrix4x4 *matrix) const`，把自身变换叠加到传入矩阵上，而不是无视已有矩阵。自定义属性变化后必须调用受保护槽 `update()`，通知关联 item 重新计算变换；否则数值变了但画面可能不更新。

变换在 3D 矩阵中计算，最终投影回 2D `QTransform` 应用到 item。它只属于 Graphics View，不是普通 QWidget 的通用变换系统。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsTransform(QObject *parent = nullptr)` | 构造抽象变换基类；直接实例化无意义。 |
| `~QGraphicsTransform()` | 虚析构，支持通过基类指针销毁派生对象。 |
| `applyTo(QMatrix4x4 *matrix) const` | 纯虚函数；派生类把自身变换叠加到矩阵上。 |
| `update()` | 受保护槽；属性变化后调用，通知 item 刷新变换。 |
| `QGraphicsItem::setTransformations()` | 把多个 transform 按顺序应用到 item。 |
| `QGraphicsScale` | 常用派生类，表达可动画缩放。 |
| `QGraphicsRotation` | 常用派生类，表达绕轴旋转。 |
| 与 `setTransform()` | 可共用，但要理解最终组合顺序和投影效果。 |
