# QSGMaterial
> Qt 6.11.1 · Qt Quick · 来自 `QSGMaterial`

## 作用定位
`QSGMaterial` 描述“用什么 GPU 状态和 shader 画这份几何”。它不包含顶点数据；同一份 geometry 可按不同材质呈现。

## API 速查
| API | 是做什么的 |
|---|---|
| `createShader()` | 必须重实现，返回匹配当前后端的 shader 对象。|
| `compare()` | 为批处理/排序比较材质状态。|
| `setFlag(Blending)` | 声明是否需要 alpha 混合。|

## 使用场景
需要单色、贴图以外的特殊效果，例如热力图颜色映射、虚线、圆角距离场或自定义混合规则。

## 常见坑与经验
- `compare()` 必须稳定且与真正渲染状态一致；错误比较会导致不正确批处理。
- Qt 6 shader 应面向 `QShader`/RHI，而非只写一个 OpenGL GLSL 版本。

## 知识点覆盖
材质、管线状态、批处理、混合、跨后端 shader。
