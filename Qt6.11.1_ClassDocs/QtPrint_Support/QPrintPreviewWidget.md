# QPrintPreviewWidget
> Qt 6.11.1 · Qt Print Support · 来自 `QPrintPreviewWidget`

## 1. 先建立直觉

`QPrintPreviewWidget` 是可嵌入窗口布局的打印预览控件。和 `QPrintPreviewDialog` 相比，它不强迫你使用 Qt 自带的完整对话框，而是把预览页面、缩放、视图模式这些能力做成 widget，方便放进你自己的工具栏和界面结构。

## 2. 类说明

保留类说明：这些 API 来自 `QPrintPreviewWidget`，属于 Qt Print Support 模块，用于在 QWidget 界面中嵌入打印预览。

它的核心信号仍然是 `paintRequested(QPrinter *)`：需要预览内容时，你用同一套打印函数把页面画到 printer 上。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QPrintPreviewWidget(parent, flags)` | 创建带内部 printer 的预览控件。 |
| `QPrintPreviewWidget(QPrinter *printer, parent, flags)` | 使用外部 `QPrinter` 生成预览。 |
| `paintRequested(QPrinter *)` | 请求业务代码绘制预览页面。 |
| `previewChanged()` | 预览内容或显示状态改变时通知外层 UI。 |
| `updatePreview()` | 重新生成预览，通常在页面设置或文档内容变化后调用。 |
| `print()` | 打开打印流程并打印当前预览内容。 |
| `currentPage()` / `setCurrentPage(page)` | 查询或跳转当前页。 |
| `pageCount()` | 查询预览总页数。 |
| `setViewMode()` / `viewMode()` | 设置单页、对开页、全部页面视图。 |
| `setSinglePageViewMode()`、`setFacingPagesViewMode()`、`setAllPagesViewMode()` | 常用视图模式快捷槽。 |
| `setZoomMode()` / `zoomMode()` | 设置自定义缩放、适合宽度、适合窗口。 |
| `setZoomFactor()` / `zoomFactor()` | 自定义缩放比例。 |
| `zoomIn()` / `zoomOut()` | 按倍率放大或缩小。 |
| `fitToWidth()` / `fitInView()` | 快速切换到适宽或整页显示。 |
| `setOrientation()` / `orientation()` | 设置横向或纵向。 |
| `setPortraitOrientation()`、`setLandscapeOrientation()` | 方向快捷槽。 |
| `ViewMode` | `SinglePageView`、`FacingPagesView`、`AllPagesView`。 |
| `ZoomMode` | `CustomZoom`、`FitToWidth`、`FitInView`。 |

## 4. 典型流程

```cpp
auto *preview = new QPrintPreviewWidget(&printer, this);
connect(preview, &QPrintPreviewWidget::paintRequested,
        this, &ReportWindow::printDocument);

toolbar->addAction("Fit Width", preview, &QPrintPreviewWidget::fitToWidth);
toolbar->addAction("Print", preview, &QPrintPreviewWidget::print);
layout->addWidget(preview);
```

当文档内容或页面设置改变：

```cpp
preview->updatePreview();
```

## 5. 使用场景

| 场景 | 为什么用 widget |
| --- | --- |
| 自定义报表设计器 | 预览要嵌在复杂界面中，而不是独立对话框。 |
| 文档编辑器右侧预览 | 可以和页面设置面板、目录、属性栏联动。 |
| 自定义工具栏和快捷键 | 外层 UI 自己控制缩放、翻页、打印按钮。 |
| 多文档预览 | 每个 tab 放一个预览控件。 |

## 6. 常见坑与经验

`setCurrentPage()` 使用文档页码语义，界面上一般从 1 开始展示。外层页码输入框要和控件当前页保持一致，并处理越界。

`updatePreview()` 会重新触发绘制，代价取决于文档复杂度。用户拖动边距滑块时，不要每个像素都重绘全部页面，做防抖或只在释放时刷新。

视图模式和缩放模式是显示策略，不改变文档实际分页。横向/纵向、纸张和边距才会改变 `QPrinter` 页面布局，从而影响分页。

## 7. 知识点覆盖

- 嵌入式打印预览控件的工作模型。
- `paintRequested`、`updatePreview`、`previewChanged`。
- 页码、总页数、视图模式、缩放模式。
- 方向设置与分页重算。
- 自定义工具栏和预览性能控制。
