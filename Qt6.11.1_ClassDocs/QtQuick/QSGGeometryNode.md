# QSGGeometryNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGGeometryNode`

## 作用定位
`QSGGeometryNode` 是最常用的通用绘制节点，承载几何与材质，并可通过标志声明自己拥有这些资源。

## API 速查
| API | 是做什么的 |
|---|---|
| `setGeometry()` | 指定顶点/索引数据。|
| `setMaterial()` | 指定渲染材质。|
| `setOpaqueMaterial()` | 指定不透明时的优化材质。|
| `OwnsGeometry` / `OwnsMaterial` | 由节点析构时释放相应资源。|

## 使用场景
自定义 `QQuickItem` 的 `updatePaintNode()` 中创建几何节点，后续帧更新其顶点数据和材质参数。

## 常见坑与经验
- 先建立所有权约定，再决定是否手动 delete；混用最容易双重释放。
- 不透明材质必须与正常材质视觉等价，否则在透明度变化时会跳变。

## 知识点覆盖
几何节点、资源归属、不透明优化、Scene Graph 更新。
