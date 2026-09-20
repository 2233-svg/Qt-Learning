# QSGVertexColorMaterial
> Qt 6.11.1 · Qt Quick · 来自 `QSGVertexColorMaterial`

## 作用定位
`QSGVertexColorMaterial` 使用顶点自带颜色插值渲染几何，适合渐变、多色网格和大量同 shader 小图元。

## API 速查
| API | 是做什么的 |
|---|---|
| `createShader()` | 创建内置顶点色 shader。|
| `compare()` | 支持材质排序。|

## 使用场景
热力图、线段强度渐变、低成本背景渐变或每个顶点颜色不同的可视化。

## 常见坑与经验
- 顶点布局必须包含颜色属性，否则 shader 读到的数据无意义。
- 颜色插值是按三角形线性插值，不等于感知均匀的高级渐变。

## 知识点覆盖
顶点属性、颜色插值、可视化网格、批处理。
