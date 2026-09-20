# QSGTransformNode：把矩阵变换施加给场景图子树

> Qt 6.11.1 · `#include <QSGTransformNode>` · 模块：`Qt6::Quick` · 继承：`QSGNode`

`QSGTransformNode` 是一个不直接绘制内容的变换容器。它用一张 `QMatrix4x4` 同时变换所有后代，避免对每个几何节点重复改顶点坐标。

## 它适合什么

缩放一组标尺、旋转一套标记、把离屏图层整体平移到某个锚点，都是将节点置于同一个 `QSGTransformNode` 下的情形。嵌套节点会组合矩阵，因此局部坐标系可以逐层建立。

```cpp
auto *transform = new QSGTransformNode;
QMatrix4x4 matrix;
matrix.translate(origin.x(), origin.y());
matrix.rotate(angleDegrees, 0, 0, 1);
transform->setMatrix(matrix);
transform->appendChildNode(content);
```

## 语义与限制

新节点使用单位矩阵。`setMatrix()` 只设置本节点的局部矩阵；最终作用于叶子的矩阵还会和祖先矩阵组合。使用 `QMatrix4x4` 并不表示 Qt Quick 对任意 3D 场景都有同等优化：默认渲染器主要针对 2D 路径优化，透视、非平面旋转或大量 3D 变换需用实际目标后端测量。

所有 QSG 节点仅能在场景图渲染线程修改。直接篡改与矩阵有关的内部状态时才需要 `markDirty(DirtyMatrix)`；正常使用 `setMatrix()` 不需要额外标记。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSGTransformNode()` | 创建局部矩阵为单位矩阵的变换节点。 |
| `matrix()` | 返回本节点保存的局部 `QMatrix4x4`。 |
| `setMatrix(matrix)` | 替换局部矩阵，并使渲染器重新处理矩阵状态。 |
| `combinedMatrix()` | 继承 API 内部使用的累计矩阵；应用代码通常应依赖自身局部矩阵，而非把它当作跨线程状态。 |
| 继承的 `appendChildNode()` | 后代均受该变换影响；同级子节点的绘制顺序不变。 |
| `QSGNode::DirtyMatrix` | 直接维护自定义变换数据时应使用的脏状态。 |
