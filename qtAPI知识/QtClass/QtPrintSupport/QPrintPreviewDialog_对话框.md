# QPrintPreviewDialog 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPrintPreviewDialog>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：`QDialog`

## 它解决什么问题

`QPrintPreviewDialog` 提供一个完整的打印预览对话框。它内部使用 `QPrintPreviewWidget`，并带有常用的缩放、页面浏览、方向和打印控制 UI；应用只需要在需要生成预览页面时把文档画到传入的 `QPrinter` 上。

```cpp
QPrinter printer;
QPrintPreviewDialog preview(&printer, this);

connect(&preview, &QPrintPreviewDialog::paintRequested,
        this, &ReportView::renderDocument);

preview.exec();
```

关键点在于 `renderDocument(QPrinter *printer)` 应与实际打印共用同一份绘制代码：

```cpp
void ReportView::renderDocument(QPrinter *printer)
{
    QPainter painter(printer);
    drawFirstPage(&painter);

    if (hasSecondPage()) {
        printer->newPage();
        drawSecondPage(&painter);
    }
}
```

预览每次需要重建页面时都会发出 `paintRequested()`，因此绘制函数必须是可重复调用的。不要在其中消耗一次性数据、永久修改文档状态，或假定只会被调用一次。

## 预览与实际打印的关系

预览使用 `QPrinter` 作为绘制设备，和直接打印的绘制流程基本一致，包括在新页前调用 `newPage()`。这正是它的价值：同一套页边距、分页和绘制代码可以先预览，再直接打印。

但预览不是 PDF 截图工具。它依赖你的 `paintRequested()` 槽重新生成页面；如果槽没有连接、绘制失败，预览就没有有效内容。

## 传入还是内部创建 `QPrinter`

传入 `QPrinter *` 的构造函数适合预览后继续打印，或希望页面设置和预览共享配置。仅传 `parent` 的构造函数会创建内部默认打印机，使用系统默认打印机。

外部传入的打印机不转移所有权。销毁对话框后，打印机仍由创建者管理。

## 模态与非模态

`exec()` 用于模态预览。`open(receiver, member)` 以非模态方式打开并在关闭时把 `finished(int)` 连接自动断开；它不像 `QPrintDialog::open()` 那样直接连接带打印机参数的接受信号。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QPrintPreviewDialog(QPrinter *printer, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())` | 基于指定打印机创建预览对话框。 | 推荐用于预览与实际打印共用配置；不接管 `printer` 所有权。 |
| 构造 | `QPrintPreviewDialog(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())` | 创建带内部默认打印机的预览对话框。 | 内部打印机使用系统默认设备；需要复用设置时使用 `printer()`。 |
| 析构 | `~QPrintPreviewDialog()` | 销毁预览对话框。 | 外部传入的打印机不会随之删除。 |
| 结束对话框 | `done(int result)` | 结束预览对话框并设置结果码。 | 常由用户关闭或 QDialog 流程调用，普通代码不需要手工控制。 |
| 非模态打开 | `open(QObject *receiver, const char *member)` | 打开对话框并将 `finished(int)` 连到指定槽。 | 关闭时连接自动断开；接收对象需存活。 |
| 生成页面请求 | `paintRequested(QPrinter *printer)` | 预览需要生成页面时发出，提供可绘制的打印机。 | 必须连接；槽应可重复执行，并按真实打印流程调用 `newPage()`。 |
| 关联打印机 | `printer()` | 返回预览当前操作的 `QPrinter`。 | 不转移所有权；用它读取或同步页面设置。 |
| 可见性 | `setVisible(bool visible)` | 显示或隐藏预览对话框。 | 常用 `exec()` 或 `open()`；展示时会触发预览生成。 |

## 易错点

1. `paintRequested()` 可能多次发出，绘制槽必须无副作用且可重入地重新生成页面。
2. 在预览和实际打印间复用同一绘制函数，并在每一页之间调用 `QPrinter::newPage()`。
3. 对话框不替你构建文档内容；没有连接 `paintRequested()` 就没有预览页面。
4. 外部 `QPrinter` 的生命周期仍由调用方管理。

### 一句话总结

`QPrintPreviewDialog` 是带完整控制 UI 的打印预览窗口：连接 `paintRequested(QPrinter *)`，并用与实际打印相同的绘制代码生成预览页面。
