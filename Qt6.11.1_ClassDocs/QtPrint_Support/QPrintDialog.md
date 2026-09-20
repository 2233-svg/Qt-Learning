# QPrintDialog
> Qt 6.11.1 · Qt Print Support · 来自 `QPrintDialog`

## 1. 先建立直觉

`QPrintDialog` 是给用户选择打印机和打印参数的对话框。它不会替你绘制文档；它只是把用户选择写回 `QPrinter`。对话框接受之后，你仍然要用 `QPainter` 在这个 `QPrinter` 上画页面。

## 2. 类说明

保留类说明：这些 API 来自 `QPrintDialog`，属于 Qt Print Support 模块，用于显示打印设置界面并更新 `QPrinter`。

它继承 `QAbstractPrintDialog`，所以页码范围、打印范围和选项 flags 都来自基类。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QPrintDialog(parent)` | 使用内部默认 `QPrinter` 创建对话框。 |
| `QPrintDialog(QPrinter *printer, parent)` | 操作调用者提供的 `QPrinter`，最常用。 |
| `exec()` | 模态显示，返回 `Accepted`/`Rejected`。 |
| `open(receiver, member)` | 非模态显示，完成后调用指定槽。 |
| `printer()` | 返回被对话框配置的 `QPrinter`。 |
| `setOption(option, on)` | 单独开关某个打印选项。 |
| `setOptions(options)` / `options()` | 批量设置或读取选项 flags。 |
| `testOption(option)` | 判断某个选项是否启用。 |
| `accepted(QPrinter *)` | 用户接受设置时发出。 |
| `done(result)` / `setVisible(visible)` | 对话框生命周期重实现，通常不直接调用。 |

## 4. 典型流程

```cpp
QPrinter printer(QPrinter::HighResolution);
QPrintDialog dialog(&printer, this);
dialog.setOption(QAbstractPrintDialog::PrintPageRange);
dialog.setOption(QAbstractPrintDialog::PrintSelection, hasSelection());

if (dialog.exec() == QDialog::Accepted)
    printDocument(&printer);
```

非模态写法要保证 `QPrinter` 和对话框活到回调结束：

```cpp
auto *dialog = new QPrintDialog(&printer, this);
dialog->setAttribute(Qt::WA_DeleteOnClose);
dialog->open(this, SLOT(printAccepted()));
```

## 5. 使用场景

| 场景 | 建议 |
| --- | --- |
| 标准桌面打印 | `exec()` 后同步调用打印函数。 |
| 大文档或复杂 UI | 非模态 `open()`，避免嵌套事件循环影响状态。 |
| 只允许 PDF/指定设备 | 先配置 `QPrinter`，再按需限制选项。 |
| 有选区/当前页 | 只在业务确实支持时打开对应选项。 |

## 6. 常见坑与经验

`accepted(QPrinter *)` 不是“已经打印成功”。它只表示用户接受了对话框设置。真正打印失败仍可能发生在 `QPainter::begin()`、`newPage()` 或 `end()` 阶段。

不要在用户点打印前就开始生成所有页面，尤其是大文档。对话框可能被取消，预先计算会白耗时间。

平台原生打印对话框表现不完全一致。有些选项在某些系统上可能被隐藏、合并或由驱动接管，业务逻辑不能只依赖 UI 长相。

## 7. 知识点覆盖

- 打印对话框如何修改 `QPrinter`。
- 模态 `exec()` 与非模态 `open()`。
- 打印选项 flags、页码范围和业务能力。
- 对话框接受和实际打印成功的区别。
