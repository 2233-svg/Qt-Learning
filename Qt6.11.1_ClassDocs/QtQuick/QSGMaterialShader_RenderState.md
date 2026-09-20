# QSGMaterialShader::RenderState
> Qt 6.11.1 · Qt Quick · 来自 `QSGMaterialShader::RenderState`

## 作用定位
`RenderState` 是 shader 更新时收到的本帧状态快照，包括组合矩阵、不透明度、视口和脏状态。

## API 速查
| API | 是做什么的 |
|---|---|
| `combinedMatrix()` | 取得模型到裁剪空间的组合矩阵。|
| `opacity()` | 取得继承后的有效透明度。|
| `viewportRect()` | 取得当前视口。|
| `isMatrixDirty()` | 判断矩阵是否须重写入 uniform。|
| `isOpacityDirty()` | 判断透明度是否改变。|

## 使用场景
在 `updateUniformData()` 中只在 dirty 时更新对应字节，减少无意义的 uniform 写入。

## 常见坑与经验
- 有效 opacity 已包含父层影响，不应再重复乘一次父节点 alpha。
- state 只在回调期间有效，不能保存指针到下一帧。

## 知识点覆盖
渲染状态快照、组合矩阵、增量更新、uniform 优化。
