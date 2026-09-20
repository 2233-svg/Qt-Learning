# QSGGeometry
> Qt 6.11.1 · Qt Quick · 来自 `QSGGeometry`

## 作用定位
`QSGGeometry` 保存顶点、索引和绘制拓扑，是 Scene Graph 中自定义三角形、线段和点集的 CPU 侧描述。

## API 速查
| API | 是做什么的 |
|---|---|
| `defaultAttributes_Point2D()` | 取得仅含二维位置的顶点布局。|
| `defaultAttributes_TexturedPoint2D()` | 取得位置加纹理坐标布局。|
| `allocate(vertices, indices)` | 分配或调整顶点/索引数量。|
| `vertexDataAsPoint2D()` | 以常用二维顶点格式访问内存。|
| `indexDataAsUShort()` / `indexDataAsUInt()` | 访问索引缓冲。|
| `setDrawingMode()` | 设置三角形、线段等拓扑。|
| `setVertexDataPattern()` | 提示静态或动态更新频率。|

## 使用场景
画折线、扇形、波形或自定义网格时，写入顶点并让 `QSGGeometryNode` 持有它。

## 常见坑与经验
- 每帧改变顶点后要在节点上标记 `DirtyGeometry`。
- 属性布局和 shader 输入必须一致；类型或偏移错配会出现花屏而不是编译错误。
- 预估最大容量、复用 geometry，避免动画中重复分配。

## 知识点覆盖
顶点布局、索引绘制、图元拓扑、动态缓冲、shader 输入约定。
