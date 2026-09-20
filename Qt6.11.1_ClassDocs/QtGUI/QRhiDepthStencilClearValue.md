# QRhiDepthStencilClearValue

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiDepthStencilClearValue`

## 1. 先建立直觉

`QRhiDepthStencilClearValue` 是 render pass 开始时用于清除 depth/stencil 附件的小值对象。它只保存两个值：深度清除值和模板清除值。默认是深度 `1.0f`、模板 `0`，对应传统深度测试里“远平面最大深度、模板清零”的常见设置。

它不创建 depth buffer，也不决定是否启用 depth/stencil 测试；这些由 render target 附件和 `QRhiGraphicsPipeline` 状态决定。它只回答“beginPass 清除时写什么值”。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 类型性质：小型值类型，可比较、可哈希
- 使用入口：`QRhiCommandBuffer::beginPass(...)`
- 默认值：depth `1.0f`，stencil `0`

如果 render target 以 preserve depth/stencil 内容创建，清除值可能被忽略。清除值是否生效取决于 render target 的 load/preserve 语义。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QRhiDepthStencilClearValue()` | 创建默认清除值：深度 1.0，模板 0。 |
| `QRhiDepthStencilClearValue(float d, quint32 s)` | 指定深度和模板清除值。 |
| `depthClearValue()` / `setDepthClearValue()` | 读取/设置深度清除值。 |
| `stencilClearValue()` / `setStencilClearValue()` | 读取/设置模板清除值。 |
| `operator==` / `operator!=` | 比较两个清除值。 |
| `qHash()` | 让清除值可用于哈希容器或缓存键。 |

## 4. 关键用法

```cpp
QRhiDepthStencilClearValue dsClear(1.0f, 0);
cb->beginPass(rt, QColor(Qt::black), dsClear, updates);
```

这是最普通的清除方式：颜色清成黑色，深度清成最远，模板清成 0。

### Reverse-Z 场景

```cpp
QRhiDepthStencilClearValue dsClear(0.0f, 0);
```

如果你的深度比较和投影矩阵采用 reverse-Z，即越远越接近 0、越近越接近 1，清除深度通常要变成 `0.0f`，并且 pipeline 的 depth compare 也要配套改变。

## 5. 使用场景

- 每个 render pass 开始时清 depth/stencil。
- 常规 3D 渲染：depth 清 1.0。
- reverse-Z 渲染：depth 清 0.0。
- stencil mask、轮廓、裁剪等算法开始前重置 stencil。
- 作为 render pass 配置缓存键的一部分。

## 6. 常见坑与经验

- **清除值不启用测试。** Depth/stencil test 在 `QRhiGraphicsPipeline` 中设置。
- **默认深度值不适合所有管线。** reverse-Z 或自定义深度范围要同步修改 clear value 和 compare op。
- **stencil 是整数值。** 它不是颜色，也不是归一化浮点。
- **preserve 内容时清除值可能无效。** render target 要求保留内容时，beginPass 的 clear value 会被忽略。
- **深度范围受后端 clip space 影响。** 但 RHI 仍以 pass clear value 表达你要写入的深度值。

## 7. 知识点覆盖

- render pass 清除值和附件 load/preserve 语义
- depth clear、stencil clear 与 pipeline test 的分离
- 常规深度、reverse-Z 和 compare op 配套
- 值类型比较、哈希和缓存用途
