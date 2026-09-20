# QScreen
> Qt 6.11.1 · Qt GUI · 来自 `QScreen`

## 1. 先建立直觉

`QScreen` 代表一块物理或虚拟显示屏。它不是窗口，也不负责创建窗口；它回答的是“窗口所在屏幕的尺寸、可用区域、DPI、缩放、方向、刷新率是什么”，并在这些平台状态变化时发信号。

在多屏、高 DPI、旋转屏、投影和远程桌面场景中，直接写死 1920x1080 或固定缩放是最容易出问题的。`QScreen` 就是把这些平台信息纳入应用布局、截图和渲染尺寸计算的入口。

## 2. 类说明

- 头文件：`#include <QScreen>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 获取方式：`QGuiApplication::screens()`、`QGuiApplication::primaryScreen()`、`QWindow::screen()`
- 协作类：`QWindow`、`QGuiApplication`、`QPixmap`、`QTransform`

`QScreen` 对象通常由平台插件创建和维护。应用代码不要自己 new，也不要缓存很久后不检查有效性；屏幕可以热插拔，窗口也可能被用户拖到另一块屏幕。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `geometry()` / `size()` | 屏幕在虚拟桌面中的矩形和尺寸 |
| `availableGeometry()` / `availableSize()` | 排除任务栏、dock 等系统保留区域后的可用区域 |
| `virtualGeometry()` / `virtualSize()` | 同一虚拟桌面中所有 sibling 屏幕的总区域 |
| `availableVirtualGeometry()` | 虚拟桌面的可用区域合并 |
| `devicePixelRatio()` | 屏幕物理像素和设备无关像素的大致比例 |
| `logicalDotsPerInch*()` | 用于字体和 UI 标尺的逻辑 DPI |
| `physicalDotsPerInch*()` / `physicalSize()` | 物理尺寸与物理 DPI，受硬件报告准确性影响 |
| `orientation()` / `primaryOrientation()` / `nativeOrientation()` | 当前、主要、原生方向 |
| `angleBetween()` / `mapBetween()` / `transformBetween()` | 在不同屏幕方向之间换算角度、矩形和变换 |
| `refreshRate()` | 刷新率提示 |
| `grabWindow()` | 抓取指定窗口或屏幕区域为 `QPixmap` |
| `virtualSiblings()` / `virtualSiblingAt()` | 查询同一虚拟桌面的屏幕集合 |
| `manufacturer()` / `model()` / `serialNumber()` / `name()` | 平台提供的屏幕标识信息 |
| `geometryChanged` 等信号 | 监听几何、DPI、方向、刷新率变化 |

## 4. 关键用法

把窗口放到当前屏幕可用区域内：

```cpp
QScreen *screen = window->screen();
const QRect area = screen ? screen->availableGeometry()
                          : QGuiApplication::primaryScreen()->availableGeometry();
window->setGeometry(QStyle::alignedRect(Qt::LeftToRight, Qt::AlignCenter,
                                        window->size(), area));
```

处理高 DPI 时，优先从目标窗口取 DPR：

```cpp
const qreal dpr = window->devicePixelRatio();
const QSize pixelSize = window->size() * dpr;
```

`QScreen::devicePixelRatio()` 适合没有目标窗口时做估计；在 Wayland 分数缩放或窗口特殊属性下，窗口 DPR 可能和屏幕 DPR 不同。

监听屏幕变化时，不要只连 primary screen。用户拖动窗口跨屏时应监听 `QWindow::screenChanged`，再重新连接新屏幕的 `geometryChanged`、`logicalDotsPerInchChanged` 等信号。

## 5. 使用场景

- 多屏窗口定位、记忆窗口位置并校验是否仍在可见区域。
- 截屏、缩略图、屏幕录制的区域计算。
- 高 DPI 位图资源选择和渲染目标像素尺寸计算。
- 横竖屏切换、平板或移动设备方向适配。
- 自定义渲染循环根据刷新率估算动画节奏。

## 6. 常见坑与经验

- `geometry()` 是虚拟桌面坐标，副屏可能从负坐标开始。
- `availableGeometry()` 在某些 X11 环境下无法准确反映每个屏幕的工作区，这是窗口管理器协议限制。
- 物理 DPI 和物理尺寸经常来自显示器 EDID，硬件或驱动报告不准时不要用它做精密测量。
- `refreshRate()` 是平台信息，不是高精度计时器；动画节奏应依赖渲染回调或定时器策略。
- `grabWindow(0)` 抓全屏在不同平台权限差异很大，Wayland 和沙盒环境可能受限。

## 7. 知识点覆盖

本页覆盖：多屏虚拟坐标、可用区域、DPI 和 DPR、屏幕方向映射、刷新率、屏幕热插拔、截图、高 DPI 窗口尺寸。
