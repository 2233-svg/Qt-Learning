# QSSGRenderHelpers
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGRenderHelpers`

## 1. 先建立直觉

`QSSGRenderHelpers` 是 Quick 3D 渲染侧的工具箱。它把一些常见渲染辅助操作包装成静态函数，供扩展或内部代码处理纹理、pass、屏幕空间绘制、资源转换等任务。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGRenderHelpers`，属于 Qt Quick 3D 模块，用于提供渲染阶段常用辅助函数。

这类 API 面向熟悉 RHI/Quick 3D 内部渲染的人，不是普通 QML 应用层入口。

## 3. API 速查

| API 类别 | 用来做什么 |
| --- | --- |
| render pass 辅助 | 简化 pass 开始、结束或状态组合。 |
| texture/resource 辅助 | 创建、更新或使用 RHI 纹理资源。 |
| fullscreen/quad 绘制 | 做后处理、拷贝、调试可视化。 |
| 坐标/矩阵辅助 | 在渲染数据和屏幕空间之间转换。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 写后处理扩展 | 全屏绘制和纹理输入输出。 |
| 调试渲染结果 | 快速把中间纹理画出来。 |
| 避免重复底层 RHI 样板代码 | 复用 Quick 3D helper。 |

## 5. 常见坑与经验

helper 不会替你管理所有资源生命周期。QRhiTexture、pipeline、buffer 仍要按 RHI 规则创建、释放、重建。

不同渲染阶段可用的 render target 和 command buffer 状态不同。调用 helper 前要确认当前 pass 是否允许相应操作。

## 6. 知识点覆盖

- Quick 3D 渲染辅助函数。
- 后处理、纹理、全屏绘制和 RHI 状态。
- helper 与资源生命周期的边界。
