# Qt QProgressDialog 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QProgressDialog>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QDialog -> QProgressDialog`  
> 定位：会根据任务耗时决定是否出现、并允许取消工作的进度对话框

## 1. QProgressDialog 解决什么问题

`QProgressDialog` 不是单纯“带文字的 `QProgressBar`”。它解决的是一个交互取舍：

```text
任务很快完成       -> 不要突然弹窗打扰用户
任务可能很慢       -> 告诉用户程序仍在工作，并给出取消机会
```

例如“扫描某个目录”“导入一批图片”“复制若干文件”。同一个操作在开发机上可能 0.2 秒结束，在用户的网络盘或旧硬盘上却要十几秒；如果每次都立即显示对话框，短任务会造成界面闪烁。`QProgressDialog` 会依据前面若干步的耗时估计总时长，默认只有预计超过 4000 ms 才显示。

它适合：

- 前台批处理任务，用户需要等待并可能想中止；
- 有自然进度单位的操作，例如文件数、记录数、字节数或算法步骤数；
- 后台任务需要一个独立、可取消的进度入口。

它不适合：

- 任务根本不能取消，却仍放一个“取消”按钮；这会制造错误承诺；
- 长任务直接堵塞 GUI 线程。对话框无法让被阻塞的事件循环重新活过来；
- 常驻的低干扰进度展示。此时主窗口状态栏中的 `QProgressBar` 往往更自然。

## 2. 它由哪些部分组成

从使用者角度，`QProgressDialog` 是一组已经排好版的子控件：

```text
QProgressDialog
  ├─ QLabel          说明当前在做什么
  ├─ QProgressBar    显示范围与当前进度
  └─ QPushButton     取消操作（可以隐藏或替换）
```

通常只设置 `labelText`、范围和 `value` 即可。确有品牌样式、额外状态提示或特殊进度条时，再用 `setLabel()`、`setBar()`、`setCancelButton()` 替换其中的子控件。

这三个替换函数有一个很重要的共同点：**对话框会取得传入控件的所有权**。因此必须传入堆对象，例如 `new QLabel`，绝不能把栈对象地址传进去。

```cpp
auto *label = new QLabel("正在校验文件...");
progress.setLabel(label);       // 此后由 progress 负责删除 label

// QLabel label("正在校验文件...");
// progress.setLabel(&label);   // 错误：析构时可能删除栈对象
```

## 3. 最常见场景：模态地完成一小批前台工作

下面的例子适合“处理 300 个文件”这类可以分步执行、单步时间不长的前台任务。

```cpp
QProgressDialog progress("正在导入文件...", "取消导入", 0, files.size(), this);
progress.setWindowModality(Qt::WindowModal);
progress.setMinimumDuration(800);

for (qsizetype i = 0; i < files.size(); ++i) {
    if (progress.wasCanceled()) {
        rollbackImport();
        return;
    }

    importOneFile(files.at(i));
    progress.setValue(i + 1);
}

progress.setValue(files.size());
```

这里的进度单位是“已导入的文件数”，不必强行换算为百分比。关键约定是：

1. 开始前将值置为 `minimum()`，构造函数中的范围已经把它设为 `0`。
2. 每处理一个可感知的工作单元，调用一次 `setValue()`。
3. 成功结束时必须把值推进到 `maximum()`；默认 `autoReset` 会随即调用 `reset()`。
4. 每一步或每个安全中断点检查 `wasCanceled()`；取消只能由你的业务代码真正停止。

### 3.1 模态 `setValue()` 的重入风险

当对话框是模态的，`setValue()` 会调用 `QCoreApplication::processEvents()`，使界面能刷新、取消按钮能响应。但这也意味着：调用栈尚未返回时，其他排队的事件、信号和用户操作可能执行。

所以不要在 `paintEvent()` 中使用模态 `QProgressDialog`，也不要假定 `setValue()` 前后的状态绝不会被别处修改。若循环中有非可重入的共享状态、临时对象或删除自身的可能，应改为工作线程、`QTimer` 分步执行，或明确设计可重入边界。

## 4. 延迟显示、完成与重置：理解它的状态机

`minimumDuration` 是这类对话框区别于普通 `QDialog` 的核心。默认值为 4000 ms：

```text
开始任务
  ├─ 预计很快结束：对话框始终不显示
  └─ 预计超过 minimumDuration：显示进度对话框
         ├─ value 到达 maximum：autoReset 时 reset()
         │     └─ autoClose 为 true 时隐藏
         └─ 用户取消：cancel()，标记 wasCanceled 并隐藏
```

`setMinimumDuration(0)` 表示一旦设置了进度就显示。它适合明确希望立即看到反馈的操作，但不适合频繁发生的小任务。

`autoReset` 和 `autoClose` 的默认值都为 `true`，但它们控制的是不同阶段：

| 设置 | 控制什么 | 默认行为 |
| --- | --- | --- |
| `autoReset` | `value == maximum` 时是否自动调用 `reset()` | 是 |
| `autoClose` | 调用 `reset()` 时是否隐藏对话框 | 是 |

如果在当前 `value` 恰好等于新 `maximum` 时才调用 `setMaximum()` 或 `setRange()`，Qt 文档特别说明：对话框不会因此自动关闭。不要依赖“改范围”来伪造一次完成事件；在正确的任务完成点调用 `setValue(maximum())`。

## 5. 取消不是终止：把 UI 意图接到业务取消

点击取消按钮时，`canceled()` 信号会发出，并默认连接到 `cancel()`。`cancel()` 会重置对话框、将 `wasCanceled()` 置为 `true`（直到下一次 `reset()`），并隐藏窗口；它**不会**自动终止你的文件操作、网络请求或工作线程。

对于模态循环，轮询 `wasCanceled()` 就足够。对于非模态任务，应把信号接到真正的取消入口：

```cpp
connect(progress, &QProgressDialog::canceled,
        worker, &ImportWorker::requestCancel);

connect(worker, &ImportWorker::progressChanged,
        progress, &QProgressDialog::setValue);

connect(worker, &ImportWorker::finished, this,
        [progress](bool ok) {
            progress->setValue(progress->maximum());
            progress->deleteLater();
            showImportResult(ok);
        });
```

工作对象应在自己的线程安全点检查取消标志并自行清理资源。不要从工作线程直接调用 `progress->setValue()`、`hide()` 或 `deleteLater()`；控件属于 GUI 线程。

`open(receiver, member)` 也会显示对话框并临时将 `canceled()` 连接到指定槽，关闭时自动断开。这是旧式字符串槽接口；新代码通常将对话框的生命周期和连接显式写出来，可读性与类型检查都更好。

## 6. 范围、文本与自定义部件

### 6.1 `minimum`、`maximum`、`value`

默认范围是 `0..100`，但范围的单位由业务定义：

```cpp
progress.setRange(0, totalBytes);
progress.setLabelText("正在下载更新...");
progress.setValue(receivedBytes);
```

`setRange(minimum, maximum)` 中如果 `maximum < minimum`，`minimum` 会成为唯一合法值；若当前值落在新范围之外，进度对话框会被 `reset()`。因此不要在任务中随意重设范围，特别是不要让范围变化抹掉用户的取消状态。

`setLabelText()` 改变的是默认标签中的文字。`setCancelButtonText(QString())` 则会隐藏并删除取消按钮；这适合确实不可取消的阶段，但更清楚的设计通常是在整个任务开始前就决定是否允许取消。

### 6.2 自定义时的所有权与行为边界

```cpp
auto *dialog = new QProgressDialog(this);
dialog->setLabel(new QLabel("正在同步账户数据"));
dialog->setBar(new QProgressBar);
dialog->setCancelButton(new QPushButton("停止同步"));
```

- `setLabel()`、`setBar()`、`setCancelButton()` 都会接管对应对象；替换和销毁时由对话框删除。
- `setCancelButton(nullptr)` 不显示取消按钮。
- `setCancelButtonText(QString())` 也会隐藏并删除当前取消按钮。
- 传入自定义 `QProgressBar` 后，对话框会重新调整尺寸；不要把它当作独立、长生命周期的控件继续由外部管理。

## 7. 选择 QProgressDialog 还是 QProgressBar

| 需求 | 更合适的选择 | 原因 |
| --- | --- | --- |
| 用户当前必须等待，且可中断 | `QProgressDialog` | 有延迟显示和取消入口 |
| 后台同步，用户仍可继续操作主窗口 | 非模态 `QProgressDialog` 或状态栏 `QProgressBar` | 不阻断主界面 |
| 常驻下载、索引、后台任务 | `QProgressBar` | 信息密度更低，不频繁弹窗 |
| 总量未知 | `QProgressBar` 的 `setRange(0, 0)`，或对话框内的同类进度条 | 呈现忙碌而非虚假的百分比 |
| 单步可能卡数秒且无法分割 | 工作线程加信号更新 | 对话框本身不能修复 GUI 线程阻塞 |

## API 速查表
以下是 `QProgressDialog` 在 Qt 6.11.1 类文档中直接列出的 API；从 `QDialog`、`QWidget` 继承的大量通用窗口 API 不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QProgressDialog(QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 用默认标签、默认“取消”按钮及 `0..100` 范围创建对话框。 | `parent` 管理窗口生命周期；默认最短显示时间为 4000 ms。 |
| 构造 | `QProgressDialog(const QString &labelText, const QString &cancelButtonText, int minimum, int maximum, QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 一次设置说明、取消文字和进度范围。 | `cancelButtonText` 传空 `QString` 时不显示取消按钮。 |
| 析构 | `~QProgressDialog()` | 销毁对话框及其拥有的子控件。 | 通过 `setLabel()` 等交出的控件也会由它删除。 |
| 属性 | `autoClose()` | 读取 `reset()` 时是否自动隐藏对话框。 | 默认 `true`；它不决定是否执行重置。 |
| 属性 | `setAutoClose(bool close)` | 设置重置后的自动隐藏行为。 | 想在完成后保留结果窗口时可设为 `false`。 |
| 属性 | `autoReset()` | 读取值达到最大值时是否自动重置。 | 默认 `true`。 |
| 属性 | `setAutoReset(bool reset)` | 设置到达最大值后的自动 `reset()` 行为。 | 与 `autoClose` 是两个独立开关。 |
| 属性 | `labelText()` | 读取默认标签的当前文字。 | 自定义标签时应以自定义控件的状态为准。 |
| 槽、属性 | `setLabelText(const QString &text)` | 修改默认标签显示的任务说明。 | 用具体动作描述，不要把进度百分比手工拼在这里。 |
| 属性 | `maximum()` | 读取进度范围上界。 | 到达它才表示该轮进度完成。 |
| 槽、属性 | `setMaximum(int maximum)` | 修改进度上界。 | 当前值等于新上界时，不会据此自动关闭对话框。 |
| 属性 | `minimum()` | 读取进度范围下界。 | 默认是 `0`，范围单位由业务决定。 |
| 槽、属性 | `setMinimum(int minimum)` | 修改进度下界。 | 与上界一起变化时优先用 `setRange()`。 |
| 属性 | `minimumDuration()` | 读取显示前所需的最短估计时长，单位为毫秒。 | 默认 4000 ms。 |
| 槽、属性 | `setMinimumDuration(int ms)` | 设置显示延迟阈值。 | `0` 表示首次设置进度时立即显示。 |
| 属性 | `value()` | 读取当前进度值。 | 初始值应为下界，完成时应显式推进到上界。 |
| 槽、属性 | `setValue(int progress)` | 更新当前进度，并驱动显示和自动完成逻辑。 | 模态窗口会处理事件，代码必须能承受重入。 |
| 只读属性 | `wasCanceled()` | 查询本轮任务是否被取消。 | 调用 `reset()` 后会清除该状态；它不负责停止业务工作。 |
| 槽 | `cancel()` | 重置、标记取消并隐藏对话框。 | 可由业务主动调用；不要误以为它会杀掉线程或请求。 |
| 信号 | `canceled()` | 用户点取消按钮时发出。 | 默认连接到 `cancel()`；还应连接到实际任务的取消逻辑。 |
| 函数 | `open(QObject *receiver, const char *member)` | 显示对话框，并把 `canceled()` 临时连接到指定槽。 | 对话框关闭时自动断开；新代码更推荐类型安全的 `connect()`。 |
| 槽 | `reset()` | 恢复进度对话框的初始状态，按 `autoClose` 决定是否隐藏。 | 取消状态也会被清除。 |
| 函数 | `setBar(QProgressBar *bar)` | 用自定义进度条替换内部进度条。 | 对话框取得所有权，传堆对象，不要传栈地址。 |
| 函数 | `setCancelButton(QPushButton *cancelButton)` | 用自定义取消按钮替换内部按钮。 | 取得所有权；传 `nullptr` 则不显示取消按钮。 |
| 槽 | `setCancelButtonText(const QString &cancelButtonText)` | 设置默认取消按钮文字。 | 空 `QString` 会隐藏并删除该按钮。 |
| 函数 | `setLabel(QLabel *label)` | 用自定义标签替换内部标签。 | 对话框取得所有权，并按内容重新调整大小。 |
| 槽 | `setRange(int minimum, int maximum)` | 同时设置上下界。 | 上界小于下界时下界是唯一合法值；当前值越界会触发 `reset()`。 |
| 重写函数 | `sizeHint() const` | 返回适合当前子控件内容的建议尺寸。 | 对话框会自行随内容调整，普通代码不必调用。 |
| 受保护槽 | `forceShow()` | 在算法开始且超过 `minimumDuration` 后，强制显示仍隐藏的对话框。 | Qt 内部延迟显示机制使用；子类才可能需要调用。 |
| 受保护重写 | `changeEvent(QEvent *event)` | 处理语言、样式、启用状态等变化事件。 | 子类重写后通常先或后调用基类，取决于自己的处理顺序。 |
| 受保护重写 | `closeEvent(QCloseEvent *event)` | 处理用户关闭窗口的事件。 | 若重写取消逻辑，要让关闭和取消遵循同一条业务路径。 |
| 受保护重写 | `resizeEvent(QResizeEvent *event)` | 响应窗口尺寸变化并更新内部布局。 | 普通使用无需调用；自定义时避免破坏内部布局。 |
| 受保护重写 | `showEvent(QShowEvent *event)` | 响应对话框即将显示的事件。 | 延迟显示与内部状态相关，子类重写时要保留基类行为。 |

## 9. 一句话总结

`QProgressDialog` 的价值不只是显示百分比，而是在耗时不确定的前台操作中，自动避免短任务弹窗，并把“任务仍在进行”和“用户请求取消”这两件事清晰地交给应用处理。
