# QSGBasicGeometryNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGBasicGeometryNode`

## 作用定位
`QSGBasicGeometryNode` 把 `QSGGeometry` 和 `QSGMaterial` 关联为可绘制节点，但不承担它们的所有权，便于外部共享或精细管理资源。

## API 速查
| API | 是做什么的 |
|---|---|
| `setGeometry()` / `geometry()` | 绑定或读取几何对象。|
| `setMaterial()` / `material()` | 绑定或读取主材质。|
| `setOpaqueMaterial()` | 为不透明路径提供单独材质。|
| `markDirty()` | 标记几何或材质变化。|

## 使用场景
资源由专门缓存对象管理，多个节点按需复用或替换几何/材质时使用。

## 常见坑与经验
- 默认不删除 geometry 和 material；必须明确资源拥有者。
- 若资源只属于该节点，`QSGGeometryNode` 更省心。

## 知识点覆盖
绘制节点、资源所有权、材质切换、脏标记、缓存设计。
