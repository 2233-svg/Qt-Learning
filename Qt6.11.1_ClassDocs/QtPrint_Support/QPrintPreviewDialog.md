# QPrintPreviewDialog
> Qt 6.11.1 · Qt Print Support · 来自 `QPrintPreviewDialog`

## 1. 先建立直觉

`QPrintPreviewDialog` 是带工具栏和窗口外壳的打印预览对话框。它向你发出 `paintRequested(QPrinter *)`，你用和平时打印一样的代码把页面画到这个 printer 上，Qt 再把结果显示成预览。

它的关键价值是复用同一份绘制逻辑：预览画一次，真正打印也画一次，避免“预览像这样、打印又变样”。

## 2. 类说明

保留类说明：这些 API 来自 `QPrintPreviewDialog`，属于 Qt Print Support 模块，用于提供完整打印预览窗口。

如果你想把预览嵌进自己的窗口，而不是弹出对话框，用 `QPrintPreviewWidget`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QPrintPreviewDialog(parent, flags)` | 创建带内部 printer 的预览对话框。 |
| `QPrintPreviewDialog(QPrinter *printer, parent, flags)` | 基于调用者提供的 `QPrinter` 预览。 |
| `printer()` | 返回预览使用的打印设备。 |
| `paintRequested(QPrinter *)` | 需要生成预览页时发出；业务代码在这里绘制。 |
| `open(receiver, member)` | 非模态打开对话框。 |
| `done(result)` / `setVisible(visible)` | 对话框生命周期重实现。 |

## 4. 典型流程

```cpp
QPrintPreviewDialog preview(&printer, this);
connect(&preview, &QPrintPreviewDialog::paintRequested,
        this, &ReportWindow::printDocument);
preview.exec();
```

`printDocument(QPrinter *)` 应该只根据 printer 和文档状态绘制，不要弹对话框、不要修改业务数据。

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 标准桌面应用预览 | 自带翻页、缩放、打印入口。 |
| 报表打印前确认 | 用户先检查分页和版式，再决定打印。 |
| 复用现有打印函数 | 连接 `paintRequested` 到同一打印函数。 |

## 6. 常见坑与经验

`paintRequested` 可能被多次触发：打开预览、缩放、改方向、刷新都可能重新生成页面。绘制函数必须是可重复调用的纯输出过程，不要每次调用都消耗业务队列或递增文档状态。

预览不是最终打印机的绝对保证。不同打印机驱动、不可打印边距、字体和 DPI 可能让最终纸面略有差异；预览主要保证你的 Qt 绘制逻辑和分页一致。

大文档预览要注意性能。一次性绘制几百页可能卡 UI，可以考虑限制预览、缓存分页结果或优化绘制函数。

## 7. 知识点覆盖

- 预览对话框与 `QPrinter` 的关系。
- `paintRequested` 复用打印绘制逻辑。
- 预览刷新、重复绘制和副作用控制。
- 预览对话框与嵌入式预览控件的取舍。
