# QPageSetupDialog 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPageSetupDialog>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：`QDialog`

## 它解决什么问题

`QPageSetupDialog` 为 `QPrinter` 提供“页面相关设置”的用户界面。它重点处理纸张大小、方向、页边距等版面参数；选择具体打印机、份数和页码范围则更适合 `QPrintDialog`。

典型流程是先准备一份 `QPrinter`，再在打印预览或实际绘制前让用户设置页面：

```cpp
QPrinter printer;
QPageSetupDialog dialog(&printer, this);

if (dialog.exec() == QDialog::Accepted) {
    // printer 的 pageLayout 等页面配置已经更新。
}
```

这里的关键是同一个 `QPrinter`：对话框接受后会修改传入对象，后续的 `QPrintPreviewDialog` 或 `QPainter` 应继续使用它。

## 什么时候使用它

- 文档编辑器在打印预览前提供“页面设置”；
- 需要用户选择横向或纵向、纸张与边距；
- 程序有自己的打印按钮，但想复用平台原生的页设置交互。

不要把它当成完整打印对话框。它不负责选择打印机、份数或页码范围；那些交给 `QPrintDialog`。

## 原生对话框的限制

Windows 和 macOS 上通常会使用原生页面设置对话框。Qt 文档明确指出：

- 自定义纸张大小可能不会显示在 Windows 和 macOS 的原生对话框中；
- 在 macOS 原生对话框中，`QPrinter` 的自定义页边距可能不会显示。

因此，如果业务必须让用户精确查看或编辑自定义尺寸和边距，应在接受对话框后核对 `printer.pageLayout()`，必要时补充自己的设置界面。

## 模态与非模态

`exec()` 打开模态对话框并返回结果，代码直观但会启动局部事件循环。`open(receiver, member)` 则以非模态方式打开，并在接受时调用指定槽；对话框关闭后连接自动断开。

Qt 还会通过 `setVisible()`、`done()` 管理原生或非原生对话框的展示与结束。一般应用直接使用 `exec()` 或 `open()`，不需要手工调用 `done()`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QPageSetupDialog(QWidget *parent = nullptr)` | 创建带内部默认 `QPrinter` 的页面设置对话框。 | 若后续要使用设置结果，应通过 `printer()` 取得该内部对象并保证流程连续。 |
| 构造 | `QPageSetupDialog(QPrinter *printer, QWidget *parent = nullptr)` | 创建并配置指定 `QPrinter` 的页面设置对话框。 | 推荐用法；`printer` 必须在对话框和后续打印期间存活。 |
| 析构 | `~QPageSetupDialog()` | 销毁页面设置对话框。 | 不拥有外部传入的 `QPrinter`。 |
| 结束对话框 | `done(int result)` | 结束对话框并设置结果码。 | 一般由用户操作或 QDialog 接口驱动；原生对话框的行为受平台限制。 |
| 模态打开 | `exec()` | 以模态方式显示页面设置对话框并返回结果。 | 接受后再读取或使用 `QPrinter` 的页面配置。 |
| 非模态打开 | `open(QObject *receiver, const char *member)` | 显示对话框，并把 `accepted()` 连接到指定槽。 | 关闭时连接自动断开；接收对象应在对话框期间存活。 |
| 关联打印机 | `printer()` | 返回此对话框配置的 `QPrinter`。 | 指针不转移所有权；用同一对象进入预览或实际打印。 |
| 可见性 | `setVisible(bool visible)` | 显示或隐藏对话框。 | 应优先使用 `exec()` 或 `open()`；原生实现可能改变细节。 |

## 易错点

1. 页面设置和完整打印设置不是同一件事：选打印机、份数和页码范围应使用 `QPrintDialog`。
2. 原生对话框可能不显示自定义纸张或边距，不能只依赖其视觉结果。
3. 接受对话框后应继续使用同一个 `QPrinter`，否则页面设置不会带到预览或打印。
4. 非模态 `open()` 适合事件驱动流程，接收对象生命周期必须覆盖对话框。

### 一句话总结

`QPageSetupDialog` 专门修改 `QPrinter` 的页面布局设置；它适合打印预览前的纸张、方向和边距配置，而不是完整打印作业选择。
