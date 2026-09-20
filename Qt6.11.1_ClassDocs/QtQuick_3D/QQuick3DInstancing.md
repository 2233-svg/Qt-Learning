# QQuick3DInstancing
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3DInstancing`

## 1. 先建立直觉

`QQuick3DInstancing` 用来给同一个模型提供大量实例的变换、颜色和自定义数据。它的目标是“一个 mesh/material，很多个位置”，例如草、星点、粒子式物体、重复零件。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3DInstancing`，属于 Qt Quick 3D 模块，用于自定义模型实例化数据。

派生类必须实现 `getInstanceBuffer(int *instanceCount)`，返回实例表字节数据，并在数据变化后 `markDirty()`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `getInstanceBuffer(instanceCount)` | 生成实例 buffer，派生类必须实现。 |
| `calculateTableEntry()` | 根据位置、缩放、欧拉角、颜色、自定义数据生成表项。 |
| `calculateTableEntryFromQuaternion()` | 使用四元数旋转生成表项。 |
| `markDirty()` | 标记实例数据变化。 |
| `depthSortingEnabled` | 透明实例需要按深度排序时启用。 |
| `hasTransparency` | 实例颜色 alpha 是否影响透明渲染。 |
| `instanceCountOverride` | 限制实际渲染实例数量。 |
| `shadowBoundsMinimum/Maximum` | 指定实例阴影 bounds，Qt 6.9 起。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 大量重复对象 | 显著减少 draw call 和对象开销。 |
| 程序化分布 | 每个实例位置/颜色由 C++ 生成。 |
| 半透明实例 | 需要处理 depth sorting 和 alpha。 |

## 5. 常见坑与经验

实例化不是复制完整 Model。所有实例共享同一套几何和材质，适合“形状相同、属性轻微不同”的对象。

透明实例成本更高。启用 depth sorting 之前先确认真的需要，因为排序本身也有 CPU 开销。

阴影 bounds 对大范围实例很关键。bounds 不准会导致阴影缺失或渲染范围过大。

## 6. 知识点覆盖

- GPU instancing 概念。
- 实例表项：位置、旋转、缩放、颜色、自定义数据。
- 透明排序、数量覆盖和阴影 bounds。
