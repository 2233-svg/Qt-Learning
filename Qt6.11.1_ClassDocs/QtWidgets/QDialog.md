# QDialog

> Qt 6.11.1 · Qt Widgets · 来自 `QDialog`

## 1. 先建立直觉

### 这是什么

`QDialog` 是 Qt Widgets 中所有“临时决策窗口”的基类。它仍然是一个 `QWidget`，但和普通窗口的重点不同：普通窗口负责承载长期界面，对话框负责在某个时刻向用户索取一个决定，然后用 `Accepted`、`Rejected` 或自定义整数结果把这个决定交回调用方。

理解 `QDialog` 时，不要只把它看成一个带按钮的小窗口。它真正管理的是三件事：如何限制用户和其他窗口交互，如何结束这次交互，以及结束时把什么结果通知出去。文件选择框、颜色选择框、消息框、向导页容器，本质上都建立在这个模型上。

### 适合使用的场景

- 需要用户确认或取消的操作，例如保存前确认、删除前确认、设置提交前校验。
- 需要短时间收集一组输入，例如登录、查找替换、导出选项、连接配置。
- 需要附属于某个主窗口的临时工具窗口，例如首选项、属性编辑器、非模态搜索面板。
- 需要统一处理“确定/取消/应用/关闭”语义，而不是让调用方猜测窗口为什么消失。

### 不适合的场景

- 长期停留的主工作区应使用 `QMainWindow`、普通 `QWidget` 页面或停靠窗口，而不是 `QDialog`。
- 后台任务进度不应该靠 `exec()` 阻塞 GUI 线程；需要进度反馈时优先考虑异步任务加 `QProgressDialog` 或自定义非模态面板。
- 对嵌套事件循环敏感的场景不要依赖 `exec()`；现代 Widgets 代码更适合 `open()` 加 `finished(int)`。

### 最小示例

```cpp
auto dialog = new SettingsDialog(this);
dialog->setAttribute(Qt::WA_DeleteOnClose);

connect(dialog, &QDialog::finished, this, [this, dialog](int result) {
    if (result == QDialog::Accepted)
        applySettings(dialog->settings());
});

dialog->open();
```

这段写法的重点是：对话框异步打开，关闭时靠信号取结果，生命周期由 `WA_DeleteOnClose` 收尾。它比在业务代码中到处写 `if (dialog.exec() == QDialog::Accepted)` 更不容易制造重入问题。

## 2. 依赖与对象关系

- 头文件：`#include <QDialog>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：`QColorDialog`、`QErrorMessage`、`QFileDialog`、`QFontDialog`、`QInputDialog`、`QMessageBox`、`QProgressDialog`、`QWizard`

### 父窗口关系

`QDialog` 通常给一个父窗口。这个 parent 不只是对象所有权，还影响窗口居中、任务栏归属和窗口模态范围。没有 parent 的对话框容易变成“漂浮的顶层窗口”，在多窗口应用里尤其容易跑到错误的屏幕或错误的窗口栈顺序里。

即使有 parent，`QDialog` 仍然是顶层窗口；它不会像普通子控件那样嵌入父控件的布局中。要把一块界面嵌入页面，应使用 `QWidget` 子类而不是对话框。

### 模态关系

`QDialog` 有三种常见打开方式：

- `show()`：按普通窗口显示；是否模态取决于 `modal` 或 `windowModality`。
- `open()`：窗口模态、立即返回；结束后用 `finished(int)`、`accepted()`、`rejected()` 接收结果。
- `exec()`：应用模态并启动局部事件循环；代码看起来同步，但会增加重入和生命周期风险。

经验上，业务复杂、对象会被外部删除、涉及网络/线程/异步回调时，优先用 `open()`。简单的短命本地对话框可以用 `exec()`，但不要在 `exec()` 打开期间假设外部世界静止。

### 结果模型

`QDialog` 的结果是一个整数。内置约定只有两个：`Accepted` 为 `1`，`Rejected` 为 `0`。如果需要更多结果，可以调用 `done(customCode)`，但调用方要清楚这些自定义码属于当前对话框协议，不是 Qt 通用枚举。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum DialogCode { Accepted, Rejected }` | 标准对话框结果：接受或拒绝。 |
| `modal : bool` | 控制 `show()` 显示时是否应用模态；不影响 `exec()`。 |
| `sizeGripEnabled : bool` | 是否在右下角显示可拖拽调整大小的握柄。 |
| `QDialog(QWidget *parent, Qt::WindowFlags f)` | 创建一个顶层对话框，可指定父窗口和窗口标志。 |
| `~QDialog()` | 销毁对话框及其子对象。 |
| `accept()` | 以 `Accepted` 结束对话框，并发出相应信号。 |
| `reject()` | 以 `Rejected` 结束对话框，并发出相应信号。 |
| `done(int r)` | 以任意结果码结束对话框，是 `accept()` / `reject()` 的底层出口。 |
| `exec()` | 模态显示并阻塞到结束，返回结果码。 |
| `open()` | 窗口模态显示并立即返回，适合异步流程。 |
| `result() const` | 读取最近一次完成时的结果码。 |
| `setResult(int i)` | 设置结果码但不关闭窗口。 |
| `setModal(bool modal)` | 设置 `show()` 的默认模态行为。 |
| `isSizeGripEnabled() const` | 查询是否启用尺寸握柄。 |
| `setSizeGripEnabled(bool)` | 启用或禁用右下角尺寸握柄。 |
| `setVisible(bool visible)` | 显示或隐藏对话框；被重写以处理对话框状态。 |
| `sizeHint() const` | 返回推荐尺寸，通常由布局和子控件决定。 |
| `minimumSizeHint() const` | 返回推荐最小尺寸。 |
| `accepted()` | 对话框以接受状态结束时发出。 |
| `rejected()` | 对话框以拒绝状态结束时发出。 |
| `finished(int result)` | 对话框完成时总是携带结果码发出。 |
| `closeEvent(QCloseEvent *e)` | 处理窗口关闭请求，默认通常走拒绝语义。 |
| `keyPressEvent(QKeyEvent *e)` | 处理按键；Escape 默认触发拒绝。 |
| `contextMenuEvent(QContextMenuEvent *e)` | 默认上下文菜单策略下的右键菜单入口。 |
| `eventFilter(QObject *o, QEvent *e)` | 对安装过的过滤对象拦截事件。 |
| `resizeEvent(QResizeEvent *)` | 对话框尺寸变化后的通知入口。 |
| `showEvent(QShowEvent *event)` | 对话框即将显示后的初始化入口。 |

## 4. API 逐项说明

### `enum QDialog::DialogCode`

标准结果码只有 `Accepted` 和 `Rejected`。它们不是按钮本身，而是一次对话流程的结论：用户同意继续，或者用户取消、关闭、按 Escape、校验失败后主动中止。

对于简单设置对话框，直接使用这两个值即可。对于“保存/不保存/取消”这类三态结果，通常更适合用 `QMessageBox::StandardButton`，或者在自定义对话框中通过 `done(customCode)` 建立明确协议。

### `modal : bool`

这个属性决定 `show()` 是否以模态方式显示。设置为 `true` 大致等价于把 `windowModality` 设为 `Qt::ApplicationModal`；但 `exec()` 本来就会模态显示，所以它不受这个属性控制。

容易混淆的一点是：`modal` 管的是用户能不能操作其他窗口，不是管调用代码会不会阻塞。`open()` 是模态但不阻塞，`exec()` 是模态且阻塞，`show()` 可以非模态也可以模态。

### `sizeGripEnabled : bool`

启用后，对话框右下角显示 `QSizeGrip`，用户可以直接拖动改变大小。它适合内容可伸缩的对话框，例如高级搜索、日志查看、可调整列表；不适合尺寸固定的短确认框。

如果启用了握柄但拖动效果很奇怪，通常要检查布局、`minimumSize`、`maximumSize`、子控件的 `sizePolicy`，而不是只盯着这个属性。

### `QDialog(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

构造对话框。`parent` 建议传入当前主窗口或发起操作的窗口，这样平台窗口管理器能正确处理居中、置顶关系和任务栏归属。`f` 可以定制标题栏按钮、窗口类型等，但不要随手堆窗口标志；过度定制会导致不同平台表现不一致。

对话框一般在构造函数中创建子控件、布局和按钮盒，然后把按钮连接到 `accept()`、`reject()` 或自定义校验槽。

### `~QDialog()`

销毁对话框及子对象。带 parent 的子控件会跟着删除；使用 `WA_DeleteOnClose` 时，对话框可能在关闭流程中自动销毁。

如果对话框会自动删除，不要在 `finished()` 之后继续解引用裸指针。需要安全引用时用 `QPointer<QDialog>`，或把需要的数据在销毁前复制出来。

### `accept()`

把结果设为 `Accepted` 并结束对话框。常见连接是 `QDialogButtonBox::accepted` 到 `QDialog::accept`。

如果点击“确定”前需要校验输入，不要直接把按钮连到 `accept()`；应连接到自定义槽，校验通过后再调用 `accept()`，校验失败则保持对话框打开并提示用户。

### `reject()`

把结果设为 `Rejected` 并结束对话框。默认取消按钮、窗口关闭和 Escape 键通常都会走这个语义。

`reject()` 表示“这次对话没有提交有效结果”，并不代表发生错误。调用方应把它当作正常用户路径处理。

### `done(int r)`

用指定结果码结束对话框，并触发 `finished(r)`。当 `r` 等于 `Accepted` 或 `Rejected` 时，还会分别触发 `accepted()` 或 `rejected()`。

它适合自定义结论，例如“应用但不关闭”“保存副本”“以后再说”等，不过这种用法要谨慎：结果码越多，对话框和调用方之间的隐式协议越重。公开给团队使用的对话框最好用命名枚举包装这些值。

### `exec()`

模态显示对话框，启动局部事件循环，直到对话框结束后返回结果码。它写起来很顺手：

```cpp
SettingsDialog dialog(this);
if (dialog.exec() == QDialog::Accepted)
    applySettings(dialog.settings());
```

但 `exec()` 的代价是重入：局部事件循环运行期间，定时器、信号、窗口事件仍可能继续发生，外部对象也可能被删除或状态改变。对简单、短小、栈上创建的对话框问题不大；对复杂应用，优先考虑 `open()`。

### `open()`

以窗口模态方式显示并立即返回。它不会启动额外事件循环，结束后通过 `finished(int)`、`accepted()`、`rejected()` 通知调用方。

这是更适合现代 Qt 应用的写法，尤其当对话框和业务逻辑之间存在异步操作、对象生命周期较复杂、或调用方本身处在信号处理过程中。

### `result() const`

返回当前或最近一次结束时的结果码。典型用途是在 `exec()` 返回后读取，或在 `finished()` 里确认结果。

若对话框设置了 `WA_DeleteOnClose`，关闭后对象可能已经销毁，不应再通过旧指针调用 `result()`。此时应该使用 `finished(int)` 信号参数，它就是最安全的结果来源。

### `setResult(int i)`

只设置内部结果码，不关闭窗口，也不发出完成信号。它通常用于少数需要预设结果的高级场景。

大多数代码不应该单独调用它。想结束对话框时用 `accept()`、`reject()` 或 `done(int)`，语义更完整。

### `setModal(bool modal)`

设置 `show()` 后的模态行为。若你随后调用 `open()` 或 `exec()`，它们有自己的显示语义，不必再依赖这个属性。

需要精细控制模态范围时，优先直接设置 `setWindowModality(Qt::WindowModal)` 或 `Qt::ApplicationModal`，可读性更好。

### `isSizeGripEnabled() const` / `setSizeGripEnabled(bool)`

查询或设置右下角尺寸握柄。它只是提供用户交互入口；最终可调整范围仍然受最小/最大尺寸、布局和窗口管理器控制。

设计上，内容密集且有列表、表格、文本区的对话框适合开启；只有几个按钮的提示框开启握柄会显得多余。

### `setVisible(bool visible)`

`QDialog` 重写了可见性切换，以便配合对话框结果和模态行为。直接 `hide()` 或 `setVisible(false)` 只是隐藏窗口，不等同于 `accept()`、`reject()` 或 `done()`，因此不会发出 `finished()`。

这点非常重要：如果调用方等待 `finished(int)`，就不要用 `hide()` 当成关闭对话框的方式。

### `sizeHint() const` / `minimumSizeHint() const`

返回推荐尺寸和推荐最小尺寸。对话框的尺寸主要由布局、子控件的 `sizeHint`、按钮区、边距和平台 style 决定。

遇到对话框过小或内容被挤压，先检查布局是否完整、是否给主要内容设置了合理的伸缩因子，再考虑重写这些函数。

### `accepted()` / `rejected()` / `finished(int result)`

这三个信号用于接收对话框结论。`finished(int)` 最通用，因为它携带结果码；`accepted()` 和 `rejected()` 更适合连接简单动作。

注意：调用 `hide()`、`setVisible(false)` 或直接删除正在显示的对话框，不会自动发出这些“完成语义”的信号。想通知调用方，就用 `done()` 家族结束对话框。

### `closeEvent(QCloseEvent *e)`

处理窗口系统发来的关闭请求。默认关闭对话框时通常相当于拒绝；如果对话框里有未保存内容，可以重写此函数，在确认后接受或忽略事件。

不要在 `closeEvent()` 中直接删除自己。若需要关闭即删除，设置 `Qt::WA_DeleteOnClose`，让 Qt 在合适的时机处理。

### `keyPressEvent(QKeyEvent *e)`

处理键盘输入。`QDialog` 默认会把 Escape 作为取消路径，因此按 Escape 通常触发 `reject()`。

如果重写这个函数处理快捷键，未处理的按键应交回基类，否则 Escape、默认按钮、焦点控件的键盘行为可能失效。

### `contextMenuEvent(QContextMenuEvent *e)`

在默认上下文菜单策略下处理右键菜单。对话框本身很少需要全局右键菜单，但高级设置、属性编辑器、文本区域周边工具可以用它提供局部动作。

实际项目中，更多时候会把上下文菜单交给具体子控件处理，而不是让整个对话框截获。

### `eventFilter(QObject *o, QEvent *e)`

事件过滤器入口。可用于拦截子控件事件，例如按 Enter 时不要立即提交、某个编辑器失焦时触发校验、或在多个输入框之间统一处理快捷键。

过滤器要克制使用。能通过信号、验证器、按钮状态表达的逻辑，不必塞进事件过滤器；否则对话框行为会变得难以追踪。

### `resizeEvent(QResizeEvent *)`

尺寸变化后调用。适合更新依赖窗口尺寸的辅助状态，但不适合手工摆放已经由布局管理的子控件。

如果你在对话框中使用布局，绝大多数响应式调整应交给布局系统完成。

### `showEvent(QShowEvent *event)`

显示时调用。适合做依赖最终窗口状态的轻量初始化，例如首次聚焦某个控件、延迟计算列宽、根据屏幕空间调整默认尺寸。

不要把耗时加载放在这里阻塞显示；需要加载数据时，让对话框先出现，再异步填充内容。

## 5. 深入实践与常见坑

### `open()` 和 `exec()` 的取舍

`exec()` 的优势是局部代码直线化，劣势是嵌套事件循环。嵌套事件循环不是“暂停世界”，它只是让当前函数等在那里，同时 GUI 仍然处理其他事件。复杂程序中，这会带来对象提前销毁、状态被外部改变、信号顺序难以推理等问题。

`open()` 的优势是事件流清晰。你把“用户结束对话框之后做什么”写在 `finished(int)` 里，调用栈不会被长时间挂住。对需要长期维护的桌面应用，这是更稳的默认选择。

### 确定按钮不要绕过校验

常见错误是直接写：

```cpp
connect(buttonBox, &QDialogButtonBox::accepted, this, &QDialog::accept);
```

如果对话框有必填项、路径检查、数值范围、权限检查，应改成连接到自己的提交函数。只有当数据真正可用时才调用 `accept()`。

### 关闭、隐藏、删除是三件事

`accept()` / `reject()` / `done()` 是完成对话流程；`hide()` 只是不可见；析构是对象消失。调用方等待结果时，必须让对话框以完成语义退出，否则状态机会断掉。

### 数据读取时机

用 `exec()` 时，通常在返回 `Accepted` 后从栈上对象读取数据。用 `open()` 且可能 `WA_DeleteOnClose` 时，应在 `finished()` 触发时立即读取，或在对话框发出自定义信号时把业务数据作为参数传出。

### 默认按钮与 Escape

`QDialogButtonBox` 能帮你建立平台一致的按钮顺序和角色。默认按钮负责 Enter 路径，Escape 通常走拒绝路径。不要随意吞掉按键事件，否则用户熟悉的键盘操作会失灵。
