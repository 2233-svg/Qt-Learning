# QSGFlatColorMaterial
> Qt 6.11.1 · Qt Quick · 来自 `QSGFlatColorMaterial`

## 作用定位
`QSGFlatColorMaterial` 用单一颜色填充几何，是自定义 Scene Graph 中最轻量的实体色材质之一。

## API 速查
| API | 是做什么的 |
|---|---|
| `setColor()` | 设置填充颜色。|
| `color()` | 读取当前颜色。|
| `createShader()` | 创建内置单色 shader。|
| `compare()` | 按颜色等状态支持排序和批处理。|

## 使用场景
折线背景、网格块、选区遮罩、简单矢量图元。

## 常见坑与经验
- 需要透明色时材质必须正确声明 blending，否则 alpha 不会按预期合成。
- 每个不同颜色都可能拆分批次；大量小块可考虑顶点色材质。

## 知识点覆盖
单色材质、批处理、透明混合、简单几何绘制。
