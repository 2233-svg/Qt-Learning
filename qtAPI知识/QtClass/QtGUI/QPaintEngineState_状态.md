# QPaintEngineState：传递给绘制引擎的增量状态快照

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPaintEngineState>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 相关类型：`QPaintEngine`、`QPainter`、`QPen`、`QBrush`、`QTransform`

`QPaintEngineState` 表示活跃 `QPaintEngine` 的当前绘制状态，以及自上次同步以来**哪些状态发生了变化**。Qt 在调用 `QPaintEngine::updateState(const QPaintEngineState &)` 时把它传给绘制引擎实现；引擎先读取 `state()` 返回的 `DirtyFlags`，再只同步对应变化项。

它不是应用绘图时要自行创建和保存的状态对象。普通应用应调用 `QPainter::setPen()`、`setBrush()`、`setTransform()`、`setOpacity()` 等 API；只有实现新的 `QPaintEngine` 时才会直接读取 `QPaintEngineState`。

Qt 文档将本类的所有函数标为可重入（reentrant），但这不意味着它可以脱离当前绘制调用而任意跨线程或长期保存。它描述的是一次活动绘制引擎更新中的状态。

## 它解决的问题

`QPainter` 的状态很多：笔、刷、字体、裁剪、变换矩阵、合成模式、透明度、抗锯齿提示等。若每画一个图元都把全部状态重新发给后端，代价很高。

`QPaintEngineState` 使用“脏标志 + 当前值”模型：

1. `QPainter` 改变了某项状态，例如 `setPen()`；
2. Qt 在状态中标记 `QPaintEngine::DirtyPen`；
3. 后端即将绘制时收到 `updateState(state)`；
4. 绘制引擎检查 `state.state()`；
5. 只有标记为 dirty 的项目才读取并同步到目标后端。

这样可以减少不必要的 GPU / 原生图形 API / 文件格式状态切换，也让自定义后端知道本次更新的最小集合。

## 实际使用场景

### 1. 自定义 `QPaintEngine` 中同步画笔、画刷与变换

```cpp
void VectorPaintEngine::updateState(const QPaintEngineState &state)
{
    const QPaintEngine::DirtyFlags dirty = state.state();

    if (dirty.testFlag(QPaintEngine::DirtyPen))
        backendSetPen(state.pen());

    if (dirty.testFlag(QPaintEngine::DirtyBrush))
        backendSetBrush(state.brush());

    if (dirty.testFlag(QPaintEngine::DirtyTransform))
        backendSetTransform(state.transform());

    if (dirty.testFlag(QPaintEngine::DirtyOpacity))
        backendSetOpacity(state.opacity());
}
```

关键点是先看 `DirtyFlags`。例如本次只有画笔变化，就不应无条件重设字体、裁剪和合成模式。

### 2. 正确处理裁剪更新

```cpp
void VectorPaintEngine::updateState(const QPaintEngineState &state)
{
    const auto dirty = state.state();
    const bool clipChanged =
        dirty.testFlag(QPaintEngine::DirtyClipRegion) ||
        dirty.testFlag(QPaintEngine::DirtyClipPath);

    if (clipChanged) {
        backendApplyClipOperation(state.clipOperation());

        if (dirty.testFlag(QPaintEngine::DirtyClipPath))
            backendSetClipPath(state.clipPath());
        else
            backendSetClipRegion(state.clipRegion());
    }

    if (dirty.testFlag(QPaintEngine::DirtyClipEnabled))
        backendSetClipEnabled(state.isClipEnabled());
}
```

裁剪路径和裁剪区域是不同表示，`clipOperation()` 则说明如何与已有裁剪组合。不能只看 `isClipEnabled()` 就跳过具体裁剪数据的同步。

### 3. 普通应用不直接使用它

```cpp
QPainter painter(&image);
painter.setPen(Qt::darkBlue);
painter.setOpacity(0.6);
painter.drawEllipse(QRectF(20, 20, 80, 80));
```

应用代码只操作 `QPainter`。Qt 自己把这些调用转化为 `QPaintEngineState`，再交给目标设备的绘制引擎。

## 核心模型与边界

### 它是增量更新，不是完整持久化配置

`state()` 返回的是 `QPaintEngine::DirtyFlags` 的按位组合，表示“相对于上一次引擎状态同步，哪些属性需要更新”。因此 getter 的正确阅读方式是：

> 某个 dirty flag 被设置时，读取与它对应的 getter，并把该值应用到后端。

不能把一次 `QPaintEngineState` 保存下来，等未来再把里面的全部值当作完整绘制上下文重放；后端自身仍保有未变化的状态，当前对象也只在引擎更新调用的语境中有意义。

### Dirty flag 与 getter 的对应关系

| Dirty flag | 应读取的当前值 |
| --- | --- |
| `DirtyBackground` | `backgroundBrush()` |
| `DirtyBackgroundMode` | `backgroundMode()` |
| `DirtyBrush` | `brush()` |
| `DirtyBrushOrigin` | `brushOrigin()` |
| `DirtyClipRegion` | `clipRegion()`，并读取 `clipOperation()` |
| `DirtyClipPath` | `clipPath()`，并读取 `clipOperation()` |
| `DirtyClipEnabled` | `isClipEnabled()` |
| `DirtyCompositionMode` | `compositionMode()` |
| `DirtyFont` | `font()` |
| `DirtyHints` | `renderHints()` |
| `DirtyOpacity` | `opacity()` |
| `DirtyPen` | `pen()` |
| `DirtyTransform` | `transform()` |

`AllDirty` 表示所有常规状态都需要同步。引擎刚开始一次绘制、底层上下文丢失后重建，或后端缓存被清空时，通常需要正确处理这种全量状态更新。

### 对象边界与指针有效期

`QPaintEngineState` 没有面向用户的公开构造函数，来源是 Qt 的绘制管线。`painter()` 返回当前正在更新该引擎的 `QPainter *`，不转移所有权，也不能在 `updateState()` 返回后保存并继续使用。

同样，`QPen`、`QBrush`、`QFont`、`QTransform` 等 getter 返回的是当前值。自定义引擎若需要在后续绘制函数中使用，应把它们转换、复制或同步到自身的后端状态，而不是持有对 `QPaintEngineState` 的引用。

### brush / pen resolving 的特殊性

`brushNeedsResolving()` 和 `penNeedsResolving()` 用于高级后端：当画刷或描边的坐标是相对于当前被渲染图元边界定义时，后端在真正知道当前图元后才可完成坐标解析。

普通光栅、PDF 或窗口应用不应基于这两个函数写业务分支。实现新后端时，若支持对象边界模式的渐变、图案或类似特性，才需要把“延迟到当前图元”的解析逻辑做正确。

### 线程与生命周期

可重入只说明不同实例的成员调用可安全并行；`QPaintEngineState` 本身仍与当前 `QPainter`、`QPaintEngine` 和 `QPaintDevice` 的绘制时段相关。自定义引擎应在同一绘制线程内消费它，避免将引用、`painter()` 指针或后台图形上下文跨线程保存。

## 关键 API 语义

### `state()`

`state()` 是更新入口。它返回一个按位或组合的 `DirtyFlags`，不是“绘制引擎是否可用”的状态码。正确模式是：

```cpp
const auto dirty = state.state();

if (dirty.testFlag(QPaintEngine::DirtyCompositionMode))
    backendSetCompositionMode(state.compositionMode());
```

使用 `testFlag()` 或位与判断。不要比较 `dirty == DirtyPen`，因为同一次更新很可能同时包含多个变化。

### 裁剪的三个组成部分

- `isClipEnabled()`：裁剪是否启用；
- `clipRegion()` / `clipPath()`：裁剪几何；
- `clipOperation()`：替换、相交等组合方式。

`DirtyClipEnabled` 和 `DirtyClipPath` / `DirtyClipRegion` 可独立出现。引擎需要分别处理“启用状态改变”和“几何内容改变”。

### 不透明度和合成模式

`opacity()` 是当前全局不透明度，`compositionMode()` 是源与目标像素的合成规则。它们不是同一个概念：

- 透明度影响源图元整体 alpha；
- 合成模式决定源、目标 alpha / 颜色如何组合。

后端若只实现其中之一，会使 `QPainter` 设置的视觉结果与其他绘制设备不一致。

## 常见错误

### 无条件读取并设置所有属性

这样会失去 `QPaintEngineState` 设计的增量同步优势，还可能在某些后端引发不必要的状态切换。始终先检查 `state()`。

### 把 `DirtyFlags` 当作单一枚举值比较

```cpp
if (state.state() == QPaintEngine::DirtyPen) // 不可靠
    backendSetPen(state.pen());
```

一次更新可同时包含 `DirtyPen | DirtyBrush | DirtyTransform`。应使用 `testFlag(QPaintEngine::DirtyPen)`。

### 只同步裁剪几何，不同步裁剪操作

同一个裁剪路径配合 `ReplaceClip`、`IntersectClip` 等操作的结果不同。遇到 `DirtyClipPath` 或 `DirtyClipRegion` 时，应同步 `clipOperation()`。

### 长期缓存 `painter()`

该指针仅指向当前正在更新引擎的 painter。缓存它会把实现与已结束或已切换的绘制会话绑定，容易产生悬空访问或错误的状态耦合。

## API 速查表

| API | 当前值含义 | 何时读取 |
| --- | --- | --- |
| `state() const` | 本次需要同步的 `QPaintEngine::DirtyFlags` 组合。 | 每次 `updateState()` 先读取。 |
| `backgroundBrush() const` | 当前背景画刷。 | `DirtyBackground`。 |
| `backgroundMode() const` | 当前背景模式。 | `DirtyBackgroundMode`。 |
| `brush() const` | 当前填充画刷。 | `DirtyBrush`。 |
| `brushOrigin() const` | 当前画刷原点。 | `DirtyBrushOrigin`。 |
| `brushNeedsResolving() const` | 画刷坐标是否须在当前图元边界中延迟解析。 | 高级后端处理对象边界相关画刷时。 |
| `clipOperation() const` | 当前裁剪组合操作。 | `DirtyClipPath` 或 `DirtyClipRegion`。 |
| `clipPath() const` | 当前裁剪路径。 | `DirtyClipPath`。 |
| `clipRegion() const` | 当前裁剪区域。 | `DirtyClipRegion`。 |
| `compositionMode() const` | 当前源/目标合成模式。 | `DirtyCompositionMode`。 |
| `font() const` | 当前字体。 | `DirtyFont`。 |
| `isClipEnabled() const` | 当前是否启用裁剪。 | `DirtyClipEnabled`。 |
| `opacity() const` | 当前全局不透明度。 | `DirtyOpacity`。 |
| `painter() const` | 正在更新此引擎的 `QPainter *`。 | 仅当前更新调用中、确有后端协作需求时；不保存。 |
| `pen() const` | 当前描边笔。 | `DirtyPen`。 |
| `penNeedsResolving() const` | 描边坐标是否须依当前图元延迟解析。 | 高级后端处理对象边界相关描边时。 |
| `renderHints() const` | 当前渲染提示标志集合。 | `DirtyHints`。 |
| `transform() const` | 当前坐标变换矩阵。 | `DirtyTransform`。 |

## 与相邻类型的分工

| 类型 | 责任 |
| --- | --- |
| `QPainter` | 面向应用的绘制命令和状态设置 API。 |
| `QPaintEngineState` | 将本次变化的状态和值交给绘制引擎。 |
| `QPaintEngine` | 把 painter 命令和状态转化为具体后端操作。 |
| `QPaintDevice` | 描述实际绘制目标的尺寸、DPI 和绘制引擎。 |

一句话记忆：`QPaintEngineState` 不是完整的画笔配置，而是“这一次有哪些 painter 状态变了，以及它们现在是什么值”。
