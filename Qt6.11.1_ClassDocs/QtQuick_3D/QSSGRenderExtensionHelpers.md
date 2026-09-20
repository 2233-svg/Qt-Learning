# QSSGRenderExtensionHelpers
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGRenderExtensionHelpers`

## 1. 先建立直觉

`QSSGRenderExtensionHelpers` 是服务 `QSSGRenderExtension` 的辅助函数集合。它帮助扩展在渲染侧更方便地访问 frame data、RHI context 或扩展相关内部对象。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGRenderExtensionHelpers`，属于 Qt Quick 3D 模块，用于辅助实现渲染扩展。

## 3. API 速查

| API 类别 | 用来做什么 |
| --- | --- |
| frame data 辅助 | 从当前帧提取扩展常用信息。 |
| RHI 访问辅助 | 更便捷地取得 context、render target、pass。 |
| 扩展状态辅助 | 管理扩展每帧参与渲染所需状态。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 实现自定义 render extension | 减少重复访问 frameData 的代码。 |
| 做 texture provider extension | 帮助对接纹理资源和渲染阶段。 |
| 快速验证扩展原型 | 用 helper 聚焦核心绘制逻辑。 |

## 5. 常见坑与经验

helper 面向渲染扩展上下文，离开扩展生命周期使用很容易拿到无效状态。

如果扩展要长期维护 GPU 资源，helper 只能帮你取得入口，资源重建策略仍要自己设计。

## 6. 知识点覆盖

- 渲染扩展 helper。
- frame/RHI/render pass 访问。
- 每帧临时状态和长期资源状态区分。
