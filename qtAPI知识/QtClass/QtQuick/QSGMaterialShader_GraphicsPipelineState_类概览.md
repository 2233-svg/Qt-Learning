# QSGMaterialShader::GraphicsPipelineState：材质可请求的有限管线状态

> Qt 6.11.1 · `#include <QSGMaterialShader>` · 模块：`Qt6::Quick`

`QSGMaterialShader::GraphicsPipelineState` 是传给 `updateGraphicsPipelineState()` 的可修改结构体。它让自定义材质以跨后端方式改变混合、颜色写入、面剔除和多边形栅格化设置，而不是自行操作某个原生图形 API。

## 为什么不是自己绑 pipeline

Qt Quick 负责排序、批处理和在不同图形 API 间创建实际 pipeline。这个结构只暴露材质真正需要且能够安全整合的部分。进入回调时，所有成员已经带有反映当前渲染器状态的有效值；保持不改等价于接受 Qt Quick 的默认决策，默认值会受 `QSGMaterial` flags 等影响，并非固定常量。

要让 callback 被调用，shader 构造时必须设置 `QSGMaterialShader::UpdatesGraphicsPipelineState`。不要把这条路径当作修改深度、视口、render target 或任意命令状态的通道，那些状态不在材质权限范围内。

## 实际使用

自定义混合模式是常见场景。例如带预乘 alpha 的普通颜色材质通常交给默认处理；仅在需要加色、乘法等非默认混合时，才开启 `blendEnable` 并调整 source/destination factors。双面几何可设 `CullNone`，但会带来额外片段工作，应只对确实需要双面显示的材质使用。

结构体仅在回调期间由场景图使用，不应保留其地址。更改成员后，`updateGraphicsPipelineState()` 返回 `true` 才表示已有修改需要应用。

## API 速查表

| API / 字段 | 语义与边界 |
|---|---|
| `blendEnable` | 启用或关闭颜色混合。 |
| `srcColor` / `dstColor` | RGB 混合的源/目标因子；未启用独立 alpha 因子时也决定 alpha 因子。 |
| `srcAlpha` / `dstAlpha` | Qt 6.5 起的 alpha 独立混合因子，仅 `separateBlendFactors` 为真时生效。 |
| `separateBlendFactors` | 为真时 RGB 与 alpha 使用不同因子；默认 `false`。 |
| `opColor` / `opAlpha` | Qt 6.8 起的 RGB/alpha 混合运算，如 `Add`、`Subtract`、`Min`、`Max`。 |
| `blendConstant` | 使用 `ConstantColor` 或 `ConstantAlpha` 因子时的常量颜色。 |
| `colorWrite` | 颜色写入掩码，可组合 `R`、`G`、`B`、`A`；例如深度预写的特殊材质可禁止颜色通道写入。 |
| `cullMode` | `CullNone`、`CullFront` 或 `CullBack`，控制正反面剔除。 |
| `polygonMode` | Qt 6.4 起的 `Fill` 或 `Line` 栅格化模式；后端支持度需按目标平台验证。 |
| `BlendFactor` | 包含 `Zero`、`One`、源/目标颜色与 alpha、常量颜色/alpha 等混合因子。 |
| `BlendOp` | Qt 6.8 起的混合运算枚举。 |
| `ColorMask` | `ColorMaskComponent` 的位集。 |
| `QSGMaterialShader::updateGraphicsPipelineState()` | 只有 shader 开启 `UpdatesGraphicsPipelineState` 时才可借此结构返回改动。 |
