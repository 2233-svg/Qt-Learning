# QProgressDialog

> Qt 6.11.1 · Qt Widgets · 来自 `QProgressDialog`

## 1. 先建立直觉

### 这是什么

`QProgressDialog` 是带进度条、说明文字和可选取消按钮的对话框。它用于“操作可能需要一段时间，用户需要看到进度，也可能需要取消”的场景。

它比自己拼 `QDialog + QProgressBar + QPushButton` 多了几个关键策略：`minimumDuration` 防止短任务一闪而过，`autoClose` / `autoReset` 控制完成后是否自动收起和复位，`wasCanceled()` 和 `canceled()` 给任务取消提供 UI 入口。

### 适合使用的场景

- 批量处理文件、导入导出、扫描、压缩、复制等长任务。
- 任务有明确步骤数，能持续调用 `setValue()`。
- 需要给用户取消入口。
- 短任务不想弹窗打扰，长任务才显示进度。

### 不适合的场景

- 后台长期任务更适合状态栏进度、任务面板或通知中心。
- 不要在 `paintEvent()` 或复杂重入敏感代码里使用模态 progress dialog。
- 取消按钮不会自动终止线程；任务本身必须配合检查取消标志。

## 2. 依赖与对象关系

- 头文件：`#include <QProgressDialog>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QDialog`
- 直接派生类：类页未列出

内部通常包含 `QLabel`、`QProgressBar` 和 `QPushButton`。可以通过 `setLabel()`、`setBar()`、`setCancelButton()` 替换这些部件；传入后所有权交给对话框，不要传栈对象地址。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `autoClose : bool` | reset 时是否隐藏对话框，默认真。 |
| `autoReset : bool` | value 到 maximum 时是否自动 reset，默认真。 |
| `labelText : QString` | 说明文字。 |
| `minimum : int` / `maximum : int` | 进度范围。 |
| `value : int` | 当前进度。 |
| `minimumDuration : int` | 显示前等待时间，避免短任务闪现。 |
| `wasCanceled : bool` | 是否被用户取消。 |
| `QProgressDialog(...)` | 创建空进度对话框或一次指定文字、取消按钮和范围。 |
| `open(receiver, member)` | 异步打开并临时连接 canceled 到槽。 |
| `setValue(int)` | 更新进度；模态对话框下可能处理事件。 |
| `setRange(min, max)` / `setMinimum()` / `setMaximum()` | 设置进度范围。 |
| `setLabelText()` / `labelText()` | 设置或读取说明文字。 |
| `setCancelButtonText()` | 设置取消按钮文字；空字符串可隐藏取消按钮。 |
| `setBar(QProgressBar *)` | 替换进度条，对话框取得所有权。 |
| `setLabel(QLabel *)` | 替换标签，对话框取得所有权。 |
| `setCancelButton(QPushButton *)` | 替换取消按钮，对话框取得所有权。 |
| `cancel()` | 标记取消并隐藏/重置。 |
| `reset()` | 重置进度，对话框可按 autoClose 隐藏。 |
| `canceled()` | 用户取消时发出。 |
| `sizeHint()` | 返回适合内部部件的建议尺寸。 |
| `changeEvent()` / `closeEvent()` / `resizeEvent()` / `showEvent()` | 处理语言、关闭、尺寸和显示事件。 |

## 4. API 逐项说明

### `autoClose`

控制 `reset()` 时是否隐藏对话框。默认开启。

完成后想保留结果状态给用户看，可以关闭它；普通进度对话框通常保持默认。

### `autoReset`

当 `value()` 达到 `maximum()` 时是否自动 reset。默认开启。

如果你希望完成后先改 label 为“完成”，再由用户关闭，就关闭 auto reset 和 auto close，手动控制生命周期。

### `labelText`

描述当前任务或阶段。它应该告诉用户正在做什么，而不仅是“请稍候”。

长任务阶段变化时可以更新 label，例如“正在扫描文件”“正在写入索引”。

### `minimum` / `maximum` / `value`

范围和当前进度。典型流程是先设置范围，把 value 设为 minimum，然后每完成一步递增，最后设到 maximum。

如果无法知道总量，考虑用范围 0 到 0 的忙碌进度条，或换成非确定进度提示。

### `minimumDuration`

默认约 4000 ms。任务预期很快完成时，对话框不会出现，避免界面闪一下。

如果你希望立即显示，设为 0；如果你只想提示真正耗时的任务，保留默认或调大。

### `wasCanceled`

表示对话框是否被取消。任务循环应定期检查它，或者把 `canceled()` 连接到取消标志。

注意：取消只是用户请求，Qt 不会自动停止你的计算或线程。

### 构造函数

默认构造创建可配置对话框。带参数构造可一次设置说明文字、取消按钮文字、范围和父窗口。`cancelButtonText` 传空字符串时不显示取消按钮。

父窗口很重要，它决定模态关系、居中和任务栏归属。

### `open(QObject *receiver, const char *member)`

异步打开，并把 `canceled()` 临时连接到指定槽；对话框关闭后会断开。它比 `exec()` 更适合不阻塞调用栈的长任务 UI。

现代代码中，优先用 `open()` 加信号槽或 lambda 管理任务取消。

### `setValue(int progress)`

更新进度。一个关键细节：如果进度对话框是模态的，`setValue()` 可能调用 `QCoreApplication::processEvents()`，这会带来重入风险。

因此不要在 `paintEvent()` 中使用它，也不要在状态不允许重入的循环里假设 `setValue()` 只是简单赋值。

### `setRange()` / `setMinimum()` / `setMaximum()`

设置进度范围。当前值超出新范围时，对话框可能 reset。

动态发现总量时可以先显示忙碌状态，拿到总量后再设成明确范围。

### `setLabelText()` / `setCancelButtonText()`

更新说明文字和取消按钮文字。取消按钮文字为空可隐藏并删除取消按钮。

取消按钮文案要准确：有些任务只能“停止后续处理”，不能撤销已完成步骤，此时写“停止”比“取消”更诚实。

### `setBar()` / `setLabel()` / `setCancelButton()`

替换内部部件。对话框取得传入对象所有权，必要时会删除它们，所以必须传堆上创建且不再由其他对象独占管理的控件。

这适合统一应用风格或给 label/bar/button 加额外行为。

### `cancel()` / `reset()`

`cancel()` 标记取消并隐藏/重置；`reset()` 清空进度并按 `autoClose` 决定是否隐藏。

调用 `cancel()` 不会自动终止后台任务。你的任务必须响应该状态。

### `canceled()`

用户按取消按钮时发出，默认连接到 `cancel()`。你应该把它连接到任务取消标志、worker 的取消槽或控制器逻辑。

不要在槽里直接强杀线程；更好的做法是请求取消，让 worker 在安全点退出。

### 事件和尺寸函数

`sizeHint()` 根据内部 label、bar、button 计算建议尺寸；show/resize/change/close 事件维护对话框行为和翻译、布局、关闭语义。

普通使用不需要重写这些函数；多数需求通过替换内部部件和属性即可完成。

## 5. 深入实践与常见坑

### 取消是协作协议

`wasCanceled()` 只告诉你用户想取消。循环任务要定期检查；线程任务要有原子标志或线程安全取消接口。

### 模态 setValue 可能重入

模态 `QProgressDialog::setValue()` 可能处理事件。事件处理期间用户可能点击按钮、窗口可能关闭、对象状态可能变化。复杂任务更推荐异步 worker + 非阻塞 `open()`。

### minimumDuration 是体验细节

短任务弹窗一闪会显得粗糙。让 `minimumDuration` 过滤掉短任务，界面会安静很多。

### autoClose/autoReset 影响完成后读取状态

默认完成即 reset/close 很方便，但如果完成后还要读取 value、展示总结或等待用户确认，要显式关闭自动行为。
