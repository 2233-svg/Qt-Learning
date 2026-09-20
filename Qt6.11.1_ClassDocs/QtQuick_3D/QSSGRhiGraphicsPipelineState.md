# QSSGRhiGraphicsPipelineState
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGRhiGraphicsPipelineState`

## 1. 先建立直觉

`QSSGRhiGraphicsPipelineState` 描述 RHI 图形管线状态：shader、顶点输入、混合、深度模板、剔除、拓扑、render pass 等。它服务 Quick 3D 内部和扩展构建 pipeline。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGRhiGraphicsPipelineState`，属于 Qt Quick 3D 模块，用于描述图形 pipeline 创建所需状态。

它不是绘制命令本身，而是“创建或选择 pipeline 的配方”。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| shader stage 相关字段 | 指定顶点/片段等 shader。 |
| vertex input layout | 描述顶点 buffer 和 attribute。 |
| blending/depth/stencil/cull | 控制片元混合、深度测试、模板和剔除。 |
| topology/sample/render pass | 控制图元拓扑、MSAA、目标 pass。 |
| reset/compare 类操作 | 复用或判断状态是否变化。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 自定义渲染扩展 | 需要创建与 Quick 3D 兼容的 graphics pipeline。 |
| 内部材质/模型渲染 | Quick 3D 根据材质和几何状态组织 pipeline。 |
| 调试渲染状态 | 判断深度/混合/剔除是否符合预期。 |

## 5. 常见坑与经验

RHI pipeline 状态通常不可随意部分修改后立即生效；状态变化可能意味着重建或重新查找 pipeline，成本比普通 uniform 更新高。

pipeline 必须匹配 render pass、sample count 和 vertex layout。任一项不一致都可能导致绘制失败或后端验证报错。

## 6. 知识点覆盖

- 图形 pipeline 配方。
- shader、顶点布局、混合、深度模板、拓扑。
- pipeline 与 render pass/MSAA 的匹配关系。
