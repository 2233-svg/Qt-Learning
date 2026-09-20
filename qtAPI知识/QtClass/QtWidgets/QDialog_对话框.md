# Qt QDialog 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QDialog>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QDialog`  
> 定位：对话框窗口

## 1. 先建立整体认识：QDialog 到底解决什么问题

`QDialog` 是 Qt 中专门用于短期交互的顶层窗口基类。它适合做：

- 设置对话框；
- 打开文件 / 选择颜色 / 输入文本；
- 确认与取消；
- 显示扩展选项；
- 需要返回“接受/拒绝”结果的窗口。

它和普通 `QWidget` 的关键区别，不是“能不能显示”，而是**它自带对话框语义**：

- 可以模态或非模态；
- 可以返回结果码；
- 可以响应 Enter / Esc；
- 常和默认按钮、取消按钮、扩展按钮一起工作。

```text
QWidget
  └─ QDialog
```

## 2. 直接结论：什么时候该用它

| 场景 | 建议 |
| --- | --- |
| 需要用户先处理完再继续操作主窗口 | 用模态 `QDialog` |
| 需要非阻塞式设置窗口 | 用 modeless `QDialog` |
| 需要返回 Accepted / Rejected | 用 `QDialog` |
| 需要可展开的“More...”对话框 | 用 `QDialog` |
| 只是一个普通顶层窗口 | 用 `QWidget` 或 `QMainWindow` |

`QDialog` 不是主工作区窗口，它更像“交互节点”：用户在这里完成一次决定，然后回到主流程。

## 3. 父对象语义：对话框和普通控件不完全一样

对 `QDialog` 来说，`parent` 不只是生命周期归属，它还影响窗口位置和任务栏表现。

如果对话框有父窗口：

- 它仍然是顶层窗口；
- 默认会居中在父窗口上方；
- 通常会共享父窗口任务栏条目。

但“有父对象”不等于“一定压在父窗口上面”。  
如果你想确保它阻塞别的窗口或保持在前面，还是要用模态。

## 4. 模态、非模态、exec、open、show：一定要分清

这是 `QDialog` 最核心的一组语义。

### 4.1 `show()`：普通显示

`show()` 只是把窗口显示出来。  
如果对话框是非模态，它不会阻塞主线程。

### 4.2 `setModal(true)` + `show()`

这会把对话框变成应用模态。  
用户在关闭它之前，通常不能操作同应用的其他窗口。

### 4.3 `open()`

`open()` 是异步显示模态对话框的推荐方式。  
它会立即返回，不会像 `exec()` 那样开一个嵌套事件循环。

在 Qt 6.11 文档里，`open()` 被描述为以 window modal 方式显示并立即返回。

### 4.4 `exec()`

`exec()` 会阻塞，直到对话框关闭，并返回 `DialogCode`。

但是官方明确建议：**尽量避免使用 `exec()`**。  
原因是它会创建嵌套事件循环，这在某些平台上支持并不完整，也更容易引入隐藏 bug。

### 4.5 选择建议

| 需求 | 建议 |
| --- | --- |
| 只是展示一个普通窗口 | `show()` |
| 想异步地弹出模态对话框 | `open()` |
| 想要简单的接受/拒绝返回值且能接受阻塞 | `exec()`，但不推荐 |
| 想让对话框成为应用模态 | `setModal(true)` + `show()` |

## 5. 返回值与生命周期

### 5.1 `DialogCode`

`QDialog::DialogCode` 只有两个值：

| 常量 | 值 | 含义 |
| --- | --- | --- |
| `QDialog::Rejected` | `0` | 拒绝 / 取消 |
| `QDialog::Accepted` | `1` | 接受 / 确认 |

`exec()` 返回的就是这个结果码。  
`result()` 读取的也是当前结果码。

### 5.2 `accept()` / `reject()` / `done()`

- `accept()`：将结果设为 `Accepted` 并关闭对话框；
- `reject()`：将结果设为 `Rejected` 并关闭对话框；
- `done(int)`：用自定义结果码关闭对话框。

通常：

- OK 按钮连 `accept()`；
- Cancel 按钮连 `reject()`；
- 更复杂的状态可以连 `done(customCode)`。

### 5.3 `finished()` / `accepted()` / `rejected()`

状态关闭后，QDialog 会发出对应信号：

- `finished(int result)`：总是带结果码；
- `accepted()`：只有接受时发；
- `rejected()`：只有拒绝时发。

注意：`hide()` 或 `setVisible(false)` 不会触发这些信号。

### 5.4 `WA_DeleteOnClose` 的边界

如果对话框设置了 `Qt::WA_DeleteOnClose`，关闭时对象可能被删除。  
这时不要在销毁后再去读 `result()`。

## 6. 默认按钮和 Escape

### 6.1 默认按钮

对话框通常会有一个默认按钮，比如 OK。  
它在用户按 Enter / Return 时被触发。

这个能力不是 `QDialog` 自己的按钮 API 提供的，而是通过 `QPushButton::setDefault()` 和 `autoDefault()` 配合完成。

### 6.2 Esc 键

按下 Esc 时，`QDialog::reject()` 会被调用。  
这意味着关闭行为会走拒绝语义，且 close event 不能被忽略。

这是很多对话框天然支持“Esc 取消”的原因。

## 7. 可调大小、位置和再次显示

### 7.1 `sizeGripEnabled`

启用后，对话框右下角会出现一个 `QSizeGrip`，方便用户拖拽调整大小。

### 7.2 `sizeHint()` 和 `minimumSizeHint()`

对话框的推荐尺寸通常来自内部布局，而不是你手写固定像素。  
如果对话框有可展开区域，`QLayout::SetFixedSize` 很常见，因为展开/收起时可以让窗口自动贴合内容。

### 7.3 位置恢复

如果是 modeless 对话框，`show()` 再次打开时，窗口管理器可能把它放回原始位置。  
如果你希望记住用户拖拽后的窗口位置，通常要在 `closeEvent()` 里保存位置，再在重新显示前恢复。

## 8. 扩展对话框：More 按钮是一种很常见的模式

Qt 官方文档里专门提到可扩展对话框：

- 默认先显示常用选项；
- 再提供一个 `More...` 按钮；
- 按下后展开更多内容。

常见做法是：

```cpp
moreButton->setCheckable(true);
connect(moreButton, &QAbstractButton::toggled,
        extensionWidget, &QWidget::setVisible);
```

如果配合 `QLayout::SetFixedSize`，展开和收起时窗口会自动跟着内容变大变小。

## 9. 典型使用场景

### 9.1 模态确认框

```cpp
QDialog dialog(this);
if (dialog.exec() == QDialog::Accepted) {
    // 用户确认
}
```

### 9.2 异步设置窗口

```cpp
auto *dialog = new QDialog(this);
connect(dialog, &QDialog::finished, dialog, &QObject::deleteLater);
dialog->open();
```

### 9.3 可扩展设置面板

```cpp
moreButton->setCheckable(true);
connect(moreButton, &QAbstractButton::toggled,
        extension, &QWidget::setVisible);
```

## 10. 受保护函数和内部辅助

### 10.1 `showEvent()` / `resizeEvent()`

对话框打开和尺寸变化时，Qt 会在这里做布局和位置相关的更新。  
如果你要保存位置、调整内部结构，通常会碰到这些事件。

### 10.2 `closeEvent()`

如果你想保存对话框位置，通常在这里做。  
如果你想改变标准关闭行为，也可以重写它，但要小心不要把正常的拒绝流程破坏掉。

### 10.3 `eventFilter()`

这是对 `QObject::eventFilter()` 的重写，主要参与对话框内部事件处理。  
一般业务代码不会优先重写它，除非你确实需要接管对话框内部事件流。

### 10.4 `adjustPosition(QWidget *)`

这个函数在头文件里作为受保护辅助函数暴露出来，但官方公共页面没有重点展开。  
从命名和对话框定位语义看，它是用于调整对话框相对某个窗口的位置，属于内部辅助能力，不是日常直接调用点。

## 11. 常见误区与排查顺序

### 11.1 “modal 了，但还是能操作别的窗口”

检查你是用了 `show()` 还是 `exec()`，以及是否真的设置了正确的 window modality。

### 11.2 “open() 调用后对话框立刻没了”

不要把 modal 对话框创建在栈上。  
`open()` 是异步的，函数返回后对象必须还活着。

### 11.3 “finished 没触发”

确认你不是直接 `hide()` 或 `setVisible(false)`。  
`finished/accepted/rejected` 只在结果码真正设置后发出。

### 11.4 “result() 读不到想要的值”

先看对话框是不是已经销毁，尤其是 `WA_DeleteOnClose` 场景。  
还要确认你调用的是 `accept/reject/done`，而不是单纯隐藏。

### 11.5 “Esc 没有取消”

检查对话框当前是否接管了键盘事件，或内部焦点是否被别的控件吞掉。  
标准语义下，Esc 应该走 reject。

## 12. 逐项 API 说明

### 成员类型

#### `enum QDialog::DialogCode`

**作用：** 表示模态对话框的返回结果。

**取值：**

| 常量 | 值 | 含义 |
| --- | --- | --- |
| `QDialog::Rejected` | `0` | 取消 / 拒绝 |
| `QDialog::Accepted` | `1` | 接受 / 确认 |

### 属性

#### `modal : bool`

**作用：** 控制 `show()` 时是否以模态方式弹出。

**关键点：** `exec()` 会忽略这个属性，始终模态。

#### `sizeGripEnabled : bool`

**作用：** 控制右下角是否显示大小调节点。

### 成员函数

#### `[explicit] QDialog::QDialog(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用：** 构造对话框，并可通过 `f` 控制窗口标志。

**边界：** 作为对话框的顶层窗口，父对象主要影响位置和任务栏关系。

#### `[virtual noexcept] QDialog::~QDialog()`

**作用：** 销毁对话框及其子对象。

#### `int QDialog::result() const`

**作用：** 读取当前结果码。

**边界：** 对设置了 `WA_DeleteOnClose` 的对话框，不要在销毁后再读取。

#### `void QDialog::setResult(int i)`

**作用：** 手动设置结果码。

**建议：** 优先使用 `QDialog::DialogCode` 定义的值。

#### `void QDialog::setModal(bool modal)`

**作用：** 设置是否模态。

#### `bool QDialog::isSizeGripEnabled() const`

**作用：** 查询大小调节点是否启用。

#### `void QDialog::setSizeGripEnabled(bool)`

**作用：** 设置是否启用大小调节点。

#### `[override virtual] void QDialog::setVisible(bool visible)`

**作用：** 重写可见性切换行为。

#### `[override virtual] QSize QDialog::sizeHint() const`

**作用：** 返回推荐尺寸。

#### `[override virtual] QSize QDialog::minimumSizeHint() const`

**作用：** 返回最小推荐尺寸。

### 公共槽

#### `[virtual slot] void QDialog::open()`

**作用：** 异步打开模态对话框。

**边界：** 不会阻塞；不要把它放在栈对象上使用。

#### `[virtual slot] int QDialog::exec()`

**作用：** 以阻塞方式显示模态对话框并返回结果码。

**边界：** 会创建嵌套事件循环，官方不推荐。

#### `[virtual slot] void QDialog::done(int)`

**作用：** 关闭对话框并设置结果码。

#### `[virtual slot] void QDialog::accept()`

**作用：** 以 Accepted 结果关闭对话框。

#### `[virtual slot] void QDialog::reject()`

**作用：** 以 Rejected 结果关闭对话框。

### 信号

#### `[signal] void QDialog::finished(int result)`

**作用：** 对话框结果码设置后发出。

#### `[signal] void QDialog::accepted()`

**作用：** 对话框被接受时发出。

#### `[signal] void QDialog::rejected()`

**作用：** 对话框被拒绝时发出。

### 受保护函数

#### `[override virtual protected] void QDialog::closeEvent(QCloseEvent *e)`

**作用：** 处理关闭事件。

**边界：** 常用于保存窗口位置。

#### `[override virtual protected] void QDialog::contextMenuEvent(QContextMenuEvent *e)`

**作用：** 处理上下文菜单事件。

#### `[override virtual protected] bool QDialog::eventFilter(QObject *o, QEvent *e)`

**作用：** 处理内部事件过滤。

#### `[override virtual protected] void QDialog::keyPressEvent(QKeyEvent *e)`

**作用：** 处理键盘按下，包含 Esc / Enter 等对话框行为。

#### `[override virtual protected] void QDialog::resizeEvent(QResizeEvent *)`

**作用：** 处理尺寸变化。

#### `[override virtual protected] void QDialog::showEvent(QShowEvent *event)`

**作用：** 处理显示事件。

#### `void QDialog::adjustPosition(QWidget *)`

**作用：** 调整对话框相对某个窗口的位置。

**说明：** 这是头文件里暴露的受保护辅助函数，不是日常直接使用点。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `enum QDialog::DialogCode` | 返回结果码 | `Accepted=1`，`Rejected=0` |
| 属性 | `modal : bool` | 控制是否模态 | `exec()` 会忽略它 |
| 属性 | `sizeGripEnabled : bool` | 控制大小调节点 | 影响右下角外观 |
| 成员函数 | `[explicit] QDialog::QDialog(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())` | 构造对话框 | `parent` 影响位置和任务栏关系 |
| 成员函数 | `[virtual noexcept] QDialog::~QDialog()` | 销毁对话框 | 会销毁子对象 |
| 成员函数 | `int QDialog::result() const` | 查询结果码 | 销毁后不要再读 |
| 成员函数 | `void QDialog::setResult(int i)` | 设置结果码 | 推荐用 `DialogCode` 值 |
| 成员函数 | `void QDialog::setModal(bool modal)` | 设置模态 | 适合配合 `show()` |
| 成员函数 | `bool QDialog::isSizeGripEnabled() const` | 查询大小调节点 | 只查询状态 |
| 成员函数 | `void QDialog::setSizeGripEnabled(bool)` | 设置大小调节点 | 常用于可拉伸窗口 |
| 成员函数 | `[override virtual] void QDialog::setVisible(bool visible)` | 切换可见性 | 与对话框语义联动 |
| 成员函数 | `[override virtual] QSize QDialog::sizeHint() const` | 推荐尺寸 | 交给布局系统 |
| 成员函数 | `[override virtual] QSize QDialog::minimumSizeHint() const` | 最小推荐尺寸 | 防止内容被挤坏 |
| 公共槽 | `[virtual slot] void QDialog::open()` | 异步打开模态对话框 | 推荐首选，别放栈上 |
| 公共槽 | `[virtual slot] int QDialog::exec()` | 阻塞执行模态对话框 | 不推荐，嵌套事件循环 |
| 公共槽 | `[virtual slot] void QDialog::done(int)` | 设置结果并关闭 | 会触发 finished |
| 公共槽 | `[virtual slot] void QDialog::accept()` | 接受并关闭 | 对应 Accepted |
| 公共槽 | `[virtual slot] void QDialog::reject()` | 拒绝并关闭 | 对应 Rejected |
| 信号 | `[signal] void QDialog::finished(int result)` | 结果码变化通知 | `hide()` 不会触发 |
| 信号 | `[signal] void QDialog::accepted()` | 接受通知 | 只有接受关闭时触发 |
| 信号 | `[signal] void QDialog::rejected()` | 拒绝通知 | 只有拒绝关闭时触发 |
| 受保护函数 | `[override virtual protected] void QDialog::closeEvent(QCloseEvent *e)` | 关闭事件 | 常用于保存位置 |
| 受保护函数 | `[override virtual protected] void QDialog::contextMenuEvent(QContextMenuEvent *e)` | 右键菜单事件 | 一般很少改 |
| 受保护函数 | `[override virtual protected] bool QDialog::eventFilter(QObject *o, QEvent *e)` | 内部事件过滤 | 多数业务不需要 |
| 受保护函数 | `[override virtual protected] void QDialog::keyPressEvent(QKeyEvent *e)` | 键盘事件 | Esc 会走 reject |
| 受保护函数 | `[override virtual protected] void QDialog::resizeEvent(QResizeEvent *)` | 尺寸变化 | 与布局和扩展区有关 |
| 受保护函数 | `[override virtual protected] void QDialog::showEvent(QShowEvent *event)` | 显示事件 | 可用于定位和初始化 |
| 受保护函数 | `void QDialog::adjustPosition(QWidget *)` | 调整显示位置 | 头文件里有，通常不直接调 |

---

### 一句话总结

`QDialog` 是对话框窗口基类。它最重要的不是“能显示”，而是完整的对话框语义：模态/非模态、接受/拒绝、返回结果、默认按钮、Esc、以及可展开和可恢复位置这些交互边界。处理它时，优先用 `open()` 或 `show()` + 信号，尽量少用 `exec()`。
