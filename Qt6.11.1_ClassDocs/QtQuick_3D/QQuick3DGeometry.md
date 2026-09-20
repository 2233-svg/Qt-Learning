# QQuick3DGeometry
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3DGeometry`

## 1. 先建立直觉

`QQuick3DGeometry` 让你从 C++ 提供自定义网格数据给 Quick 3D `Model` 使用。它关心顶点缓冲、索引缓冲、属性布局、primitive type、bounds 和 subset，而不是加载 `.mesh` 文件。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3DGeometry`，属于 Qt Quick 3D 模块，用于向 Quick 3D 提供自定义几何数据。

典型派生类会在构造或数据变化时调用 `setVertexData()`、`setIndexData()`、`addAttribute()`，最后 `update()` 通知渲染侧重建几何。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `setVertexData()` / `vertexData()` | 设置顶点 buffer 原始字节。 |
| `setIndexData()` / `indexData()` | 设置索引 buffer。 |
| `setStride()` / `stride()` | 设置单个顶点步长。 |
| `addAttribute()` | 声明位置、法线、UV、颜色等顶点属性布局。 |
| `addSubset()` | 定义几何子集，供多材质或局部 bounds 使用。 |
| `clear()` | 清空几何定义。 |
| `setPrimitiveType()` / `primitiveType()` | 三角形、线、点等绘制拓扑。 |
| `setBounds(min, max)` | 设置包围盒，影响裁剪和拾取。 |
| `setTargetData()` | 为 morph target 等目标数据提供属性。 |
| `update()` | 标记几何数据已变，需要同步到渲染后端。 |

## 4. 典型流程

```cpp
setStride(sizeof(Vertex));
setVertexData(vertexBytes);
setIndexData(indexBytes);
addAttribute(QQuick3DGeometry::Attribute::PositionSemantic, 0,
             QQuick3DGeometry::Attribute::F32Type);
setPrimitiveType(QQuick3DGeometry::PrimitiveType::Triangles);
setBounds(min, max);
update();
```

## 5. 使用场景

| 场景 | 说明 |
| --- | --- |
| 程序生成网格 | 地形、曲线管道、CAD 预览。 |
| 动态顶点数据 | 数据变化后更新 buffer。 |
| 特殊顶点布局 | 自定义属性语义与材质配合。 |

## 6. 常见坑与经验

stride、offset、attribute type 必须和 QByteArray 里的真实内存布局一致。这里错了，结果通常不是报错，而是模型扭曲、消失或法线乱掉。

bounds 要认真设置。包围盒太小会被裁剪，太大则影响裁剪效率和阴影/拾取表现。

频繁全量更新大 buffer 很贵。高频动画优先考虑骨骼、morph、shader 或 instancing，而不是每帧重传整张网格。

## 7. 知识点覆盖

- 顶点/索引缓冲和属性布局。
- primitive type、bounds、subset。
- 自定义 geometry 与 Model/Material 的配合。
- GPU 数据同步和动态更新成本。
