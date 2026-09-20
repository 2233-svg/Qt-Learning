# QRhiScissor

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiScissor`

## 1. 先建立直觉

`QRhiScissor` 是 RHI 的剪刀矩形：它限制后续 draw 只能写入矩形范围内的像素。它和 viewport 不同，viewport 决定坐标映射，scissor 决定像素裁剪范围。

RHI 中 scissor 的位置按左下角坐标系描述，类似 OpenGL 语义。这一点和 Qt UI 常见的左上角原点不同，做 UI 裁剪或高 DPI 换算时要特别小心。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 类型性质：小型值类型，可比较、可哈希
- 使用入口：`QRhiCommandBuffer::setScissor()`
- 前提：graphics pipeline 通常要声明 `QRhiGraphicsPipeline::UsesScissor`

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QRhiScissor()` | 创建空剪刀矩形。 |
| `QRhiScissor(x, y, w, h)` | 以左下角原点坐标创建剪刀矩形。 |
| `setScissor(x, y, w, h)` | 设置位置和尺寸。 |
| `scissor()` | 返回 `{x, y, w, h}`。 |
| `operator==` / `operator!=` | 比较剪刀值。 |
| `qHash()` | 用作缓存键或哈希容器键。 |

## 4. 关键用法

```cpp
ps->setFlags(ps->flags() | QRhiGraphicsPipeline::UsesScissor);

cb->setGraphicsPipeline(ps);
cb->setScissor(QRhiScissor(x, y, w, h));
cb->draw(vertexCount);
```

如果 pipeline 没声明使用 scissor，却调用 `setScissor()`，不同后端可能表现不一致。把它当成 pipeline 动态状态的一部分来管理。

## 5. 使用场景

- UI 子区域裁剪。
- 渲染图集或 tiled rendering。
- 只允许某个面板、视口、分屏区域写入。
- 调试脏区和局部重绘。
- 与 viewport 配合实现多视口渲染。

## 6. 常见坑与经验

- **坐标原点是左下角。** UI 左上角坐标要换算到 render target 像素坐标。
- **宽高不能为负。** 负宽高会被 command buffer 忽略。
- **scissor 不改变投影。** 它只裁剪像素输出，不影响顶点坐标映射。
- **要和 DPR 一起考虑。** 逻辑像素矩形要转成 render target 像素。
- **pipeline 需要动态状态 flag。** 不声明 `UsesScissor` 就不要依赖运行时 scissor。

## 7. 知识点覆盖

- scissor 与 viewport 的区别
- 左下角原点和高 DPI 换算
- 动态 pipeline 状态
- 局部裁剪和多视口渲染
