# QAbstractPrintDialog
> Qt 6.11.1 · Qt Print Support · 来自 `QAbstractPrintDialog`

## 1. 先建立直觉

`QAbstractPrintDialog` 是打印对话框的共同基类。它把“用户能选哪些打印范围、页码范围、附加页签，以及操作哪一个 `QPrinter`”这些通用能力抽出来，具体界面由 `QPrintDialog` 提供。

普通应用通常不直接实例化它；你会通过它理解 `QPrintDialog` 的页码和选项 API。

## 2. 类说明

保留类说明：这些 API 来自 `QAbstractPrintDialog`，属于 Qt Print Support 模块，用于抽象打印对话框的通用配置。

它继承 `QDialog`，所以有模态/非模态显示、返回 `Accepted`/`Rejected`、父窗口和事件循环等 QWidget 对话框语义。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QAbstractPrintDialog(QPrinter *printer, QWidget *parent)` | 绑定一个要被对话框修改的 `QPrinter`。 |
| `printer() const` | 返回当前对话框操作的打印设备。 |
| `setMinMax(min, max)` / `minPage()` / `maxPage()` | 设置或读取允许输入的页码边界。 |
| `setFromTo(from, to)` / `fromPage()` / `toPage()` | 设置或读取当前页码范围。 |
| `setPrintRange(range)` / `printRange()` | 设置全部、选区、页码范围或当前页。 |
| `setOptionTabs(tabs)` | 给对话框添加自定义选项页。 |
| `PrintDialogOption` | 控制“打印到文件、选区、页码范围、页面大小、逐份整理、当前页”等 UI 能力。 |
| `PrintDialogOptions` | `PrintDialogOption` 的 flags 组合。 |
| `PrintRange` | 用户最终选择的打印范围。 |

## 4. 典型流程

```cpp
QPrintDialog dialog(&printer, this);
dialog.setMinMax(1, document.pageCount());
dialog.setFromTo(1, document.pageCount());
dialog.setPrintRange(QAbstractPrintDialog::AllPages);
```

这些设置只是约束和初始值。真正应该打印哪些页，要在对话框接受后再从同一个 `QPrinter` 或对话框读取配置。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 文档有明确页数 | 用 `setMinMax()` 限制页码输入。 |
| 支持打印选中内容 | 打开 `PrintSelection`，并在业务层实现选区输出。 |
| 支持当前页打印 | 打开 `PrintCurrentPage`，结合当前视图页码。 |
| 需要额外打印设置 | `setOptionTabs()` 添加业务页签。 |

## 6. 常见坑与经验

对话框显示某个选项，不代表你的业务自动支持它。比如启用 `PrintSelection` 后，如果绘制代码仍然按全文打印，用户选择“选区”也没有意义。

页码按用户习惯通常从 1 开始；内部数据结构可能从 0 开始。打印页码范围时要明确转换，避免漏第一页或多打一页。

自定义 option tab 的控件生命周期要比对话框显示期长，且必须在 GUI 线程使用。不要在 tab 里做耗时打印预计算。

## 7. 知识点覆盖

- 打印范围、页码边界和页码选择。
- `QPrinter` 被对话框修改的工作方式。
- `PrintDialogOptions` 与业务能力的对应。
- `QDialog` 模态/非模态语义和自定义页签。
