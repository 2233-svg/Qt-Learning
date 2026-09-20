# QResizeEvent

> Qt 6.11.1 · Qt GUI · 来自 `QResizeEvent`

## 1. 先建立直觉

`QResizeEvent` 表示控件或窗口的大小发生变化。它携带新尺寸和旧尺寸，适合重建与尺寸绑定的资源，例如绘制缓存、视口映射、OpenGL 后备缓冲、图像缩放结果或布局辅助数据。

它不是绘制事件。尺寸变化后通常会导致重绘，但真正绘制仍应放在 `paintEvent()` 或对应渲染函数里。`resizeEvent()` 更像是“尺寸配置发生改变，请调整依赖尺寸的状态”。

## 2. 类说明

`QResizeEvent` 继承自 `QEvent`。Widgets 常通过 `QWidget::resizeEvent()` 接收，也可以在 `event()` 中处理 `QEvent::Resize`。

类说明只用于表明这些 API 来自 `QResizeEvent`：它只关心新旧尺寸，位置变化由 `QMoveEvent` 表达；完整几何变化需要结合位置和尺寸两类事件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QResizeEvent(size, oldSize)` | 构造尺寸变化事件，指定新尺寸和旧尺寸。 |
| `size() const` | 返回调整后的新尺寸，通常等同于控件当前 `size()`。 |
| `oldSize() const` | 返回调整前的旧尺寸，可用于判断是否真的跨过阈值。 |
| `type()` | 来自 `QEvent`，尺寸变化事件通常为 `QEvent::Resize`。 |

## 4. 关键用法

### 重建尺寸相关缓存

```cpp
void ChartWidget::resizeEvent(QResizeEvent *event)
{
    QWidget::resizeEvent(event);

    if (event->size() != event->oldSize()) {
        m_plotArea = calculatePlotArea(event->size());
        m_gridCache = QPixmap(event->size() * devicePixelRatioF());
        m_gridCache.setDevicePixelRatio(devicePixelRatioF());
        rebuildGridCache();
    }
}
```

和尺寸强相关的缓存可以在这里更新；真正的曲线绘制仍放在绘制阶段。

### 只在跨阈值时调整模式

```cpp
void ResponsivePanel::resizeEvent(QResizeEvent *event)
{
    const bool wasCompact = event->oldSize().width() < 480;
    const bool isCompact = event->size().width() < 480;

    if (wasCompact != isCompact)
        setCompactMode(isCompact);

    QWidget::resizeEvent(event);
}
```

频繁 resize 时，不要每一像素变化都重建全部 UI；很多逻辑只需要在状态阈值变化时触发。

## 5. 使用场景

`QResizeEvent` 用于自定义绘图控件、图像查看器、视频窗口、OpenGL/QRhi 渲染视口、响应式面板、复杂表格、嵌入式原生窗口和高 DPI 后备缓存。

它也适合做资源预算。窗口变大时可能需要更大的缓冲区，窗口变小时可以释放多余缓存；这些操作放在尺寸变化点，比每次绘制检查更清晰。

## 6. 常见坑与经验

不要在 `resizeEvent()` 里直接做全部重绘逻辑。调用 `update()` 请求重绘即可，Qt 会合并绘制请求。

不要无条件调用 `resize()` 或改变布局约束，容易造成递归 resize。需要修正尺寸时，优先通过 `sizeHint()`、`minimumSizeHint()`、布局策略或外层逻辑处理。

不要忘记高 DPI。为像素缓存分配内存时，要考虑 `devicePixelRatioF()`，否则图像可能模糊或尺寸不匹配。

不要把旧尺寸永远当作有效业务尺寸。首次显示或平台初始化阶段，旧尺寸可能是特殊值或不符合你的业务假设。

## 7. 知识点覆盖

学习 `QResizeEvent` 应覆盖控件尺寸生命周期、绘制缓存、视口重建、高 DPI 后备存储、响应式阈值、布局递归风险、`update()` 与 `paintEvent()` 分工、OpenGL/QRhi 视口调整。
