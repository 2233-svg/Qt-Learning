# QSGMaterial：定义 geometry 如何由 scene graph shader 绘制

> Qt 6.11.1 | `#include <QSGMaterial>` | CMake: `Qt6::Quick`

`QSGMaterial` 是 `QSGGeometryNode` 的“绘制方式”抽象：geometry 描述数据，material 描述 shader 身份、渲染状态需求、批处理可行性及同类材质的排序规则。自定义渐变、特殊纹理采样、距离场效果或自定义 QRhi shader 时，都需要 material 和 `QSGMaterialShader` 成对设计。

同一个 scene graph 中，每个 `QSGMaterialType` 通常只有一个对应 shader 实例；各个 material 实例只保存每个 node 不同的参数。因此 `type()` 不是“返回一个临时类型对象”，而是 shader 缓存键。`createShader()` 不是每帧或每个 node 调用，它按 material type 与 render mode 组合调用一次并由 Qt Quick 缓存。

## 最小派生骨架

```cpp
class WaveMaterial final : public QSGMaterial
{
public:
    QSGMaterialType *type() const override
    {
        static QSGMaterialType type;
        return &type;
    }

    QSGMaterialShader *createShader(QSGRendererInterface::RenderMode) const override
    {
        return new WaveShader;
    }
};
```

如果同一 C++ material 类会按不同 shader 组合渲染，`type()` 必须为每一种 shader 组合返回不同的唯一 `QSGMaterialType`。错误地复用 type 会导致 Qt 复用不兼容 shader，常见现象是部分 node 使用了错误的 uniform 布局或渲染状态。

`compare(other)` 用于将同 type 材质排序，帮助降低 `updateState()` 中的状态切换。只比较能影响渲染状态或 shader uniform 的字段；`other` 保证与当前 material 有相同 type。返回 0 表示可视作相等，-1/1 决定排序，不是“内容相等”的通用比较。

## Flags 是正确性和性能契约

`Blending` 表示绘制需要开启混合；不透明材质错误开启会增加成本，透明材质漏设会产生错误合成。`RequiresDeterminant`、`RequiresFullMatrixExceptTranslate`、`RequiresFullMatrix` 告诉 renderer shader 需要多少变换信息，按需选择最小集合。`NoBatching` 只给确实与 batching 不兼容的高级 shader 使用，通常会增加 draw call；不要把它当作解决显示问题的默认开关。

Qt 6.8 的 `viewCount()` 用于 multiview 材质。它只有在 `createShader()` 及之后才可靠；需要支持多视图的 shader 应据此选择 shader variant 并处理每 view 的矩阵。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `type()` | 返回 material 的唯一 shader 身份键 | 纯虚；同一 shader 组合应共享一个静态 type，不同组合必须不同 |
| `createShader(renderMode)` | 创建对应的 `QSGMaterialShader` | 纯虚；每个 type + render mode 组合只调用一次并被缓存 |
| `compare(other)` | 对同 type 材质排序，减少状态切换 | `other` 保证同 type；只比较影响绘制的字段 |
| `setFlag(flags, on)` / `flags()` | 配置 renderer 所需状态/信息 | 更改 flags 是 material 状态变化，必要时标记 node `DirtyMaterial` |
| `Blending` | 声明材质需要 alpha blending | 透明输出必须设；不透明输出不应无故设 |
| `RequiresDeterminant` | 请求节点变换矩阵的 determinant | 仅 shader 真正依赖时设置 |
| `RequiresFullMatrixExceptTranslate` | 请求除平移外的完整矩阵 | 比完整矩阵要求更小，按实际需求选择 |
| `RequiresFullMatrix` | 请求完整节点变换矩阵 | 只有 shader 用到完整变换时设置 |
| `NoBatching` | 禁止 renderer 对此材质进行 batching | Qt 6.3 起；会降低性能，只用于已证实不兼容的高级 shader |
| `MultiView2` / `MultiView3` / `MultiView4` | 声明 multiview 视图数 | 配合 multiview render pass 和正确 shader variant |
| `viewCount()` | 获取当前 multiview 的实际视图数 | Qt 6.8 起；仅 `createShader()` 及之后有效 |
| `CustomCompileStep` | 已废弃的兼容别名 | Qt 6 中等同 `NoBatching`，新代码使用 `NoBatching` |
