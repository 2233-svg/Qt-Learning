# QPaintEngineState

> Qt 6.11.1 · Qt GUI · 来自 `QPaintEngineState`

## 1. 先建立直觉

`QPaintEngineState` 是 `QPainter` 递交给 `QPaintEngine::updateState()` 的只读状态差分包。它告诉后端“这次只有笔、变换、裁剪或透明度等哪些部分变了”，并提供这些新值。

它不是应用层保存 painter 状态的对象。普通绘制代码使用 `QPainter::save()`/`restore()`；只有编写 paint engine 时才读取这个类，并且必须先看 `state()` 再读取对应 getter。

## 2. 类说明

- 头文件：`#include <QPaintEngineState>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：由 Qt 在更新阶段提供的只读状态视图，不由应用主动构造或长期保存。
- 关联：`QPaintEngine::updateState(const QPaintEngineState&)`、`QPaintEngine::DirtyFlags`、`QPainter`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `state()` | 取得本次真正变更的 `DirtyFlags`，所有读取的前提 |
| `pen()` / `penNeedsResolving()` | 取得新画笔与对象边界相关的 resolving 信息 |
| `brush()` / `brushOrigin()` / `brushNeedsResolving()` | 取得新画刷、原点与坐标 resolving 信息 |
| `font()` | 取得新字体请求 |
| `backgroundBrush()` / `backgroundMode()` | 取得背景画刷和背景模式 |
| `transform()` | 取得当前绘制变换 |
| `clipRegion()` / `clipPath()` | 取得本次裁剪数据 |
| `clipOperation()` | 取得裁剪是替换、相交等何种操作 |
| `isClipEnabled()` | 查询裁剪是否启用 |
| `compositionMode()` | 取得图元和目标的合成模式 |
| `opacity()` | 取得全局常量不透明度 |
| `renderHints()` | 取得抗锯齿、平滑 pixmap 等渲染提示 |
| `painter()` | 取得当前关联 painter，仅限更新期间观察 |

## 4. 关键用法

### 按 DirtyFlags 做增量同步

```cpp
void BackendEngine::updateState(const QPaintEngineState &s)
{
    const auto dirty = s.state();

    if (dirty.testFlag(QPaintEngine::DirtyPen))
        native.setPen(convertPen(s.pen()));

    if (dirty.testFlag(QPaintEngine::DirtyBrush))
        native.setBrush(convertBrush(s.brush()));

    if (dirty.testFlag(QPaintEngine::DirtyTransform))
        native.setTransform(convertTransform(s.transform()));

    if (dirty.testFlag(QPaintEngine::DirtyHints))
        native.setAntialiasing(
            s.renderHints().testFlag(QPainter::Antialiasing));
}
```

忽略 `state()` 而每次都同步一切，会把大量小 draw 调用变成昂贵的后端状态提交。更严重的是，试图只看当前值而不看 dirty 位，可能会误把上次局部裁剪/合成策略当作本次新指令。

### 正确更新裁剪栈

```cpp
if (dirty.testFlag(QPaintEngine::DirtyClipEnabled)) {
    native.setClippingEnabled(s.isClipEnabled());
}

if (dirty.testFlag(QPaintEngine::DirtyClipPath)) {
    native.applyClip(convertPath(s.clipPath()), s.clipOperation());
}
```

裁剪不只是一个矩形：可以是 region 或 path，且可被相交、替换等操作累积。后端需按 Qt 传入的 operation 维护自身剪裁状态；只保存“最后一个 clip path”会在嵌套 `save()`/`restore()` 与多重裁剪时渲染错误。

### 根据 object-bounding brush resolving 做选择

```cpp
if (dirty.testFlag(QPaintEngine::DirtyBrush)) {
    const QBrush brush = s.brush();
    if (s.brushNeedsResolving())
        deferBrushResolutionUntilPrimitiveBounds(brush);
    else
        native.setBrush(convertBrush(brush));
}
```

对象边界坐标系的渐变需要知道当前图元的 bounds 才能转换到后端坐标。`brushNeedsResolving()` / `penNeedsResolving()` 向 engine 提示这一点；忽略会让同一渐变在不同大小形状上显示错误。

## 5. 状态与 dirty 位对照

| 变化 | 应读取 |
| --- | --- |
| 画笔 | `pen()`，必要时 `penNeedsResolving()` |
| 画刷/原点 | `brush()`、`brushOrigin()`、`brushNeedsResolving()` |
| 字体 | `font()` |
| 变换 | `transform()` |
| 裁剪 | `clipRegion()` 或 `clipPath()`、`clipOperation()`、`isClipEnabled()` |
| 合成/透明度 | `compositionMode()`、`opacity()` |
| 渲染质量 | `renderHints()` |
| 背景 | `backgroundBrush()`、`backgroundMode()` |

## 6. 常见坑与经验

- **只在 `updateState()` 调用期间使用。** 不要把 `QPaintEngineState` 指针/引用保存到之后的 draw 调用。
- **不要无条件同时读取 region 和 path。** 相应 dirty flag 指出哪个表达形式在本次有效；混用会产生重复或错误裁剪。
- **opacity 和 alpha blend 是不同层次。** `opacity()` 是 painter 的常量全局 alpha，`compositionMode()` 决定合成规则，brush/pixmap 自身也可能有 alpha。
- **render hints 是请求。** 后端若无法原生满足，需依能力、fallback 或文档策略处理；不能假装已经抗锯齿。
- **`painter()` 不是后端控制器。** engine 应读取状态并写自己的后端，不应从回调中修改 painter 的公开状态。

## 7. 知识点覆盖

绘制状态差分、DirtyFlags、增量状态提交、裁剪栈、对象边界渐变、合成与 opacity、渲染提示、paint engine 生命周期。
