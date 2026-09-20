# QPrintPreviewWidget 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPrintPreviewWidget>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：`QWidget`

## 它解决什么问题

`QPrintPreviewWidget` 是可嵌入任意窗口布局的打印预览控件。`QPrintPreviewDialog` 内部正是使用它；当应用不想使用 Qt 提供的完整预览对话框，而是要把预览放进自己的文档窗口、侧边栏或工作台页面时，就使用这个类。

它的工作方式不是“把已有内容截图显示出来”，而是需要应用在 `paintRequested(QPrinter *)` 信号中把文档重新绘制到给定打印机上：

```cpp
auto *preview = new QPrintPreviewWidget(&printer, this);
connect(preview, &QPrintPreviewWidget::paintRequested,
        this, &ReportWindow::renderDocument);

layout->addWidget(preview);
preview->updatePreview();
```

绘制函数与直接打印复用，遇到后续页面时调用 `printer->newPage()`。当预览需要刷新时，控件会再次发出 `paintRequested()`，因此该绘制函数必须可以重复调用，不能依赖一次性消费的数据。

## 它和 `QPrintPreviewDialog` 如何选择

- 想快速获得带工具栏和打印按钮的完整对话框：使用 `QPrintPreviewDialog`；
- 想把预览整合进自己的多文档界面、自己的工具栏和业务按钮：使用 `QPrintPreviewWidget`。

`QPrintPreviewWidget` 只提供预览画布与控制 API，不强制你的 UI 形态。你可以把 `zoomIn()`、`setPortraitOrientation()`、`setAllPagesViewMode()` 等槽连接到自己工具栏中的动作。

## 视图模式与缩放模式

`ViewMode` 决定页面怎么排布：

- `SinglePageView`：一次显示一页；
- `FacingPagesView`：双页对开；
- `AllPagesView`：连续显示全部页。

`ZoomMode` 决定缩放策略：

- `CustomZoom`：使用明确的 `zoomFactor`；
- `FitToWidth`：宽度适应可视区域；
- `FitInView`：整页适应可视区域。

一旦调用 `setZoomFactor()`，应把它理解为明确的自定义缩放；需要恢复自适应时调用 `setZoomMode()`、`fitInView()` 或 `fitToWidth()`。

## 页面与方向

`setCurrentPage(page)` 跳到指定预览页，页码应根据 `pageCount()` 进行校验。`setOrientation()` 修改关联 `QPrinter` 的页面方向并导致预览状态变化；快捷槽 `setPortraitOrientation()` 和 `setLandscapeOrientation()` 分别设置纵向与横向。

`print()` 会把当前预览输出到关联打印机。打印前仍应确保打印机配置、错误处理和用户确认符合应用流程；控件不能替代完整的打印权限或任务管理。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum ViewMode` | 指定预览页面的排列方式。 | 用 `setViewMode()` 或三个快捷槽切换。 |
| 枚举值 | `SinglePageView` | 一次显示单页。 | 默认视图模式，适合逐页阅读。 |
| 枚举值 | `FacingPagesView` | 以对开方式显示页面。 | 适合书籍或双页排版预览。 |
| 枚举值 | `AllPagesView` | 连续显示全部页面。 | 大文档可能带来更多渲染和滚动开销。 |
| 类型 | `enum ZoomMode` | 指定预览缩放策略。 | 自定义倍率与自适应策略要分开理解。 |
| 枚举值 | `CustomZoom` | 使用明确的缩放倍率。 | 通常由 `setZoomFactor()` 进入此模式。 |
| 枚举值 | `FitToWidth` | 缩放到页面宽度适应视图。 | 适合纵向连续阅读。 |
| 枚举值 | `FitInView` | 缩放到整页适应视图。 | 默认缩放模式，适合查看完整单页。 |
| 构造 | `QPrintPreviewWidget(QPrinter *printer, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())` | 使用外部 `QPrinter` 创建预览控件。 | 推荐用于与页面设置、打印流程共享同一打印机配置；不接管所有权。 |
| 构造 | `QPrintPreviewWidget(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())` | 创建带内部默认打印机的预览控件。 | 需要跨流程共享配置时，外部传入 `QPrinter` 更清晰。 |
| 析构 | `~QPrintPreviewWidget()` | 销毁预览控件。 | 外部传入的打印机仍由调用方管理。 |
| 当前页 | `currentPage() const` | 返回当前正在查看的预览页。 | 页码范围以实际 `pageCount()` 为准。 |
| 适合视图 | `fitInView()` | 将缩放模式设为 `FitInView`。 | 适合完整查看当前页面。 |
| 适合宽度 | `fitToWidth()` | 将缩放模式设为 `FitToWidth`。 | 适合阅读纵向文档内容。 |
| 方向 | `orientation() const` | 返回关联打印机当前页面方向。 | 值来自关联 `QPrinter` 的页面布局。 |
| 页数 | `pageCount() const` | 返回当前预览生成的页面数量。 | 预览尚未生成或生成失败时不能假定大于零。 |
| 生成请求 | `paintRequested(QPrinter *printer)` | 需要应用绘制预览页时发出。 | 必须连接；槽应可重复调用并按打印流程分页。 |
| 预览变化通知 | `previewChanged()` | 预览内部状态发生变化时发出，例如方向改变。 | 用于刷新自定义工具栏状态或页码显示。 |
| 打印预览 | `print()` | 将预览输出到关联打印机。 | 不是系统级任务确认；调用前确认打印机和业务权限。 |
| 全部页视图 | `setAllPagesViewMode()` | 切换到 `AllPagesView`。 | 大文档预览时注意性能与滚动体验。 |
| 跳转页面 | `setCurrentPage(int page)` | 跳到指定预览页的开始位置。 | 先依据 `pageCount()` 校验页码。 |
| 对开页视图 | `setFacingPagesViewMode()` | 切换到 `FacingPagesView`。 | 适用于对页布局的文档检查。 |
| 横向快捷设置 | `setLandscapeOrientation()` | 将方向设为 `QPageLayout::Landscape`。 | 会更新关联打印机并刷新预览。 |
| 设置方向 | `setOrientation(QPageLayout::Orientation orientation)` | 设置关联打印机的页面方向。 | 预览会重新生成或改变；与打印机页面设置保持一致。 |
| 纵向快捷设置 | `setPortraitOrientation()` | 将方向设为 `QPageLayout::Portrait`。 | 会更新关联打印机并刷新预览。 |
| 单页视图 | `setSinglePageViewMode()` | 切换到 `SinglePageView`。 | 适合默认逐页预览。 |
| 设置视图模式 | `setViewMode(ViewMode mode)` | 设置页面排列方式。 | 切换后当前页和滚动位置的呈现会变化。 |
| 可见性 | `setVisible(bool visible)` | 显示或隐藏预览控件。 | 初次显示通常会触发预览生成；保证绘制槽已连接。 |
| 设置倍率 | `setZoomFactor(qreal factor)` | 设置明确缩放倍率，例如 1.0 为近似纸张实际尺寸。 | 会进入自定义缩放语义；倍率应为合理正数。 |
| 设置缩放模式 | `setZoomMode(ZoomMode zoomMode)` | 设置自定义或自适应缩放策略。 | 与 `setZoomFactor()` 的固定倍率语义区分。 |
| 刷新预览 | `updatePreview()` | 请求重新生成预览，并发出 `paintRequested()`。 | 文档内容或打印机配置改变后调用；绘制槽必须可重复执行。 |
| 查询视图模式 | `viewMode() const` | 返回当前页面排列方式。 | 用于同步自定义工具栏动作状态。 |
| 查询倍率 | `zoomFactor() const` | 返回当前预览缩放倍率。 | 自适应模式下显示值仍应结合 `zoomMode()` 理解。 |
| 放大 | `zoomIn(qreal factor = 1.1)` | 按因子放大预览。 | 默认每次约放大 10%；避免无限放大影响可用性。 |
| 查询缩放模式 | `zoomMode() const` | 返回当前缩放策略。 | 决定当前倍率是固定值还是自适应结果。 |
| 缩小 | `zoomOut(qreal factor = 1.1)` | 按因子缩小预览。 | 因子应大于 1，避免传入无效比例。 |

## 易错点

1. `QPrintPreviewWidget` 不会自己知道如何画文档，必须连接 `paintRequested()`。
2. 绘制槽可能重复执行，避免修改文档状态或消耗不可重放的数据。
3. `setZoomFactor()` 和 `setZoomMode()` 表达不同缩放策略，切换时不要只更新工具栏文字。
4. 文档、方向、页边距或打印机配置改变后调用 `updatePreview()`。

### 一句话总结

`QPrintPreviewWidget` 是可嵌入式打印预览画布：应用在 `paintRequested(QPrinter *)` 中复用实际打印绘制逻辑，再用它提供的缩放、分页、方向和视图 API 构建自己的预览界面。
