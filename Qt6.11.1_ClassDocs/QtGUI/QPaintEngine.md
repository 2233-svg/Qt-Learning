# QPaintEngine

> Qt 6.11.1 · Qt GUI · 来自 `QPaintEngine`

## 1. 先建立直觉

`QPainter` 是统一绘制 API，`QPaintEngine` 是其后端翻译器。前者接收“画路径、图片、文字、渐变、合成”等命令，后者把这些命令输出到 raster、PDF、SVG、窗口系统或自定义设备。

这是绘制后端作者的接口，不是普通 `paintEvent()` 的工作面。绝大多数应用只使用 `QPainter`；直接实现 engine 的理由应当是你需要新输出格式、录制绘制命令、对接特定图形系统，且接受完整状态同步与渲染正确性的复杂度。

## 2. 类说明

- 头文件：`#include <QPaintEngine>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：抽象多态类，与一个 `QPaintDevice` 协作。
- 必须实现：`begin()`、`end()`、`drawPixmap()`、`type()`、`updateState()`；至少实现一个 `drawPolygon()` 重载。
- `QPainter` 在真正绘制前调用 `updateState()`，只把发生变化的状态以 DirtyFlags 传入。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `begin(QPaintDevice *)` | 初始化一次 painter 会话，绑定设备与后端资源 |
| `end()` | 刷新/提交并结束会话，释放临时后端状态 |
| `updateState(state)` | 同步 pen、brush、font、clip、transform、opacity 等变化 |
| `drawPixmap(target, pixmap, source)` | 必须实现：输出 pixmap 区域 |
| `drawPolygon()` | 至少实现一个整数或浮点多边形绘制入口 |
| `drawPath()` | 绘制 `QPainterPath`；默认空实现，不重载就会丢路径 |
| `drawRects()` / `drawLines()` / `drawPoints()` | 批量基本图元；默认可能退化到路径/多边形 |
| `drawEllipse()` | 椭圆；默认通常由多边形路径近似 |
| `drawImage()` | 输出 `QImage`；默认可转 pixmap，后端可优化 |
| `drawTextItem()` | 输出已布局文字；默认可能转为路径，质量/性能较差 |
| `drawTiledPixmap()` | 平铺 pixmap；后端可实现高效重复纹理 |
| `hasFeature(features)` | 查询构造时声明的原生能力 |
| `PaintEngineFeature` | 声明 alpha、路径、渐变、变换、合成等能力 |
| `DirtyFlags` | 指出 `updateState()` 中哪些状态确实变了 |
| `PolygonDrawMode` | 区分奇偶/绕组填充、凸多边形和仅描边 |
| `type()` | 返回 engine 类型；自定义实现使用 `User..MaxUser` 范围 |
| `paintDevice()` / `painter()` / `isActive()` | 查询当前会话关联对象和活动状态 |
| `setActive()` | 由 engine 生命周期实现维护活动标记 |

## 4. 状态同步的核心规则

| Dirty flag | 读取 `QPaintEngineState` 的成员 |
| --- | --- |
| `DirtyPen` | `pen()`、`penNeedsResolving()` |
| `DirtyBrush` / `DirtyBrushOrigin` | `brush()`、`brushOrigin()`、`brushNeedsResolving()` |
| `DirtyFont` | `font()` |
| `DirtyTransform` | `transform()` |
| `DirtyClipRegion` / `DirtyClipPath` / `DirtyClipEnabled` | clip region/path、clip operation、启用状态 |
| `DirtyHints` | `renderHints()` |
| `DirtyCompositionMode` | `compositionMode()` |
| `DirtyOpacity` | `opacity()` |
| `DirtyBackground` / `DirtyBackgroundMode` | background brush/mode |

只读取标记为 dirty 的部分。每次 `updateState()` 都重新上传所有 GPU/后端状态会让大量小图元的性能崩塌；反过来，漏掉一个 dirty flag 会使后续绘制继承错误状态。

## 5. 关键用法

### 最小会话骨架

```cpp
bool VectorEngine::begin(QPaintDevice *device)
{
    m_device = static_cast<VectorDevice *>(device);
    openDocument(m_device->output());
    setActive(true);
    return true;
}

bool VectorEngine::end()
{
    closeDocument();
    m_device = nullptr;
    setActive(false);
    return true;
}
```

`begin()` 失败必须返回 `false`，让 `QPainter::begin()` 失败；不要设置半活动状态。`end()` 是最后一次提交机会，写文件、flush 图形命令或检测输出失败应在这里处理。

### 增量更新状态

```cpp
void VectorEngine::updateState(const QPaintEngineState &s)
{
    const auto dirty = s.state();
    if (dirty.testFlag(DirtyPen))
        backend.setPen(s.pen());
    if (dirty.testFlag(DirtyBrush))
        backend.setBrush(s.brush());
    if (dirty.testFlag(DirtyTransform))
        backend.setTransform(s.transform());
    if (dirty.testFlag(DirtyOpacity))
        backend.setOpacity(s.opacity());
}
```

paint engine 应把 Qt 状态转为后端状态，而不是试图修改 `QPainter`。裁剪的 `IntersectClip`、`ReplaceClip` 等操作顺序尤其重要；不能只保存最后一个 path 而忽略 operation。

### 如实报告能力

```cpp
VectorEngine::VectorEngine()
    : QPaintEngine(PainterPaths
                 | Antialiasing
                 | AlphaBlend
                 | LinearGradientFill
                 | RadialGradientFill)
{
}
```

feature flags 是能力声明，不是愿望清单。虚报 `PorterDuff`、`AlphaBlend` 或 `PerspectiveTransform` 会使 `QPainter` 跳过软件回退，最终渲染错误；不支持时宁可不声明并实现可靠降级。

## 6. 使用场景

- 为自定义矢量、打印、远程绘制或命令记录格式实现输出后端。
- 对接专用 GPU/硬件设备，重用 Qt 的 `QPainter` 前端。
- 实现测试用录制 engine，验证业务绘制发出了哪些图元。
- 维护 Qt 内建绘制系统的扩展，而不是普通控件 UI。

## 7. 常见坑与经验

- **不要漏掉默认实现为 no-op 的函数。** 若后端需要路径或文字，必须实现 `drawPath()`/`drawTextItem()`；默认不会神奇输出正确内容。
- **文字转 path 是保底，不是最佳方案。** 它可能失去 hinting、字形缓存和文本语义；高质量后端应尽可能支持文字/glyph。
- **坐标已经受 Qt transform 管理。** 设计清楚你的后端接受逻辑坐标还是已应用 transform 的坐标，避免二次变换。
- **图像与 pixmap 的线程/格式不同。** 自定义 engine 处理 `QPixmap` 时仍遵守 GUI 线程约束；必要时转为 `QImage`，但要估算成本。
- **`type()` 不是功能开关。** 它主要供识别与分支；自定义类型放在 `User..MaxUser`，不要冒充平台后端。
- **端到端测试不可少。** 覆盖剪裁、透明、笔刷、浮点变换、RTL 文本、DPR、保存/恢复嵌套与设备故障。

## 8. 知识点覆盖

QPainter 后端、绘制会话、增量状态同步、DirtyFlags、渲染能力协商、路径与文本、alpha/合成、坐标变换、自定义输出设备、端到端渲染测试。
