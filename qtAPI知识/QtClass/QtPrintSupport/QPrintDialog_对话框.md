# QPrintDialog 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPrintDialog>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：`QAbstractPrintDialog`

## 它解决什么问题

`QPrintDialog` 是面向用户的打印设置对话框。它允许用户选择打印机、纸张与方向、颜色模式、份数、页码范围等，然后把最终配置写入关联的 `QPrinter`。

最常见用法如下：

```cpp
QPrinter printer;
printer.setDocName("Monthly report");

QPrintDialog dialog(&printer, this);
dialog.setMinMax(1, document.pageCount());

if (dialog.exec() == QDialog::Accepted) {
    printDocument(&printer);
}
```

`printDocument()` 必须使用同一个 `printer`。用户在对话框中改过的打印机、范围、份数等信息都存放在它里面。

## 对话框不负责绘制

`QPrintDialog` 的职责是收集打印配置，而不是输出内容。接受对话框后，你仍要：

1. 根据 `QPrinter` 的页码范围、份数、颜色和设备能力决定输出策略；
2. 用 `QPainter painter(&printer)` 开始打印；
3. 绘制第一页；
4. 在后续页面之前调用 `printer.newPage()`；
5. 最后结束 `QPainter`。

很多配置要在 `QPainter::begin()` 之前完成。对话框应当出现在开始绘制之前。

## 对话框选项与原生平台行为

`options` 属性、`setOption()` 与 `testOption()` 控制哪些功能显示给用户，例如打印选区、当前页、打印到文件。

选项应在对话框显示前设置。Windows 和 macOS 通常使用原生打印对话框，因此部分 QWidget/QDialog 属性不会生效；Qt 文档还说明 macOS 原生对话框不支持通过 `setOptions()` 或 `setOption()` 配置打印选项。

如果某项业务设置必须在所有平台可控，不要只靠对话框的可见选项，应自己在打印流程中保留明确的业务状态。

## 模态与非模态

`exec()` 适合简单同步流程。`open(receiver, member)` 用非模态方式显示对话框，并在用户接受后调用槽；此时可在槽中通过 `printer()` 取得已配置的打印机。

`accepted(QPrinter *printer)` 比继承的无参数 `QDialog::accepted()` 多携带一个 `QPrinter *`，很适合直接连接到开始打印或更新预览的槽。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `options : PrintDialogOptions` | 保存影响打印对话框外观和可用功能的选项组合。 | 显示前设置；原生对话框可能忽略部分或全部选项。 |
| 构造 | `QPrintDialog(QWidget *parent = nullptr)` | 创建带内部默认 `QPrinter` 的打印对话框。 | 需要打印结果时通过 `printer()` 取得内部对象。 |
| 构造 | `QPrintDialog(QPrinter *printer, QWidget *parent = nullptr)` | 创建并配置指定 `QPrinter` 的打印对话框。 | 推荐用法；接受后继续使用同一 `QPrinter` 绘制。 |
| 析构 | `~QPrintDialog()` | 销毁打印对话框。 | 不拥有外部传入的 `QPrinter`。 |
| 接受通知 | `accepted(QPrinter *printer)` | 用户接受设置时发出，并传出已配置的打印机。 | 连接到绘制或预览前的准备槽；不要在信号中删除仍在执行的对话框。 |
| 结束对话框 | `done(int result)` | 关闭对话框并设置返回结果。 | Windows 和 macOS 原生打印对话框中可能不适用，因为只能由用户关闭。 |
| 模态打开 | `exec()` | 模态显示对话框并返回结果码。 | 只在 `Accepted` 后开始打印。 |
| 非模态打开 | `open(QObject *receiver, const char *member)` | 非模态显示对话框，并将 `accepted()` 连接到指定槽。 | 关闭后连接自动断开；接收对象需存活。 |
| 关联打印机 | `printer()` | 返回对话框当前操作的 `QPrinter`。 | 由对话框持有或外部传入，调用者不删除。 |
| 切换选项 | `setOption(PrintDialogOption option, bool on = true)` | 启用或清除单个对话框选项。 | 最好在显示前调用；平台原生实现可能不支持。 |
| 可见性 | `setVisible(bool visible)` | 显示或隐藏对话框。 | 优先选择 `exec()` 或 `open()` 来匹配流程。 |
| 查询选项 | `testOption(PrintDialogOption option) const` | 判断指定对话框选项是否启用。 | 反映 Qt 选项状态，不保证原生 UI 实际显示。 |

## 易错点

1. 用户接受 `QPrintDialog` 后不会自动打印，仍需自己用 `QPainter` 绘制。
2. 只在 `exec() == QDialog::Accepted` 后使用 `QPrinter` 新配置。
3. 打印范围和份数是用户意图，应用必须在文档分页中落实。
4. 原生对话框会带来平台差异，尤其不要假定 `setOption()` 在 macOS 原生对话框有效。

### 一句话总结

`QPrintDialog` 负责把用户的打印选择写进 `QPrinter`；它是打印作业的配置步骤，而实际分页和绘制仍由应用实现。
