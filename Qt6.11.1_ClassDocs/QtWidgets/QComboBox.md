# QComboBox

> Qt 6.11.1 · Qt Widgets · 来自 `QComboBox`

## 1. 先建立直觉

### 这是什么

`QComboBox` 是把一组选项压缩到一个控件里的选择器。关闭时它像一个按钮或字段，只显示当前项；打开时它用一个 item view 展示候选项。它可以直接用 `addItem()` 管理小列表，也可以连接 `QAbstractItemModel` 使用模型/视图数据。

组合框有三个经常被混淆的概念：`currentIndex` 是当前行号，`currentText` 是当前显示文本，`currentData` 是当前项在某个 role 下的业务数据。可靠的业务代码通常用 data 存 id，而不是用显示文本当唯一标识。

### 适合使用的场景

- 候选项有限，用户一次只能选一个。
- 窗口空间有限，不适合把所有选项都铺开成 radio button。
- 每个选项需要携带稳定业务 id、图标或额外 role 数据。
- 候选项来自模型，或者要和 view/delegate 共享显示逻辑。
- 可编辑组合框：允许用户从历史项中选，也允许输入新值。

### 不适合的场景

- 选项只有两三个且需要全部可见时，`QRadioButton` 更直观。
- 允许多选时，使用列表、树或带 check state 的模型视图。
- 选项成千上万且需要搜索、分组、分页时，单个 combo 弹窗会变笨重。
- 需要输入任意文本但候选只是辅助提示时，`QLineEdit + QCompleter` 可能更清楚。

### 最小示例

```cpp
auto *combo = new QComboBox(this);
combo->addItem(tr("Draft"), QVariant::fromValue(Status::Draft));
combo->addItem(tr("Published"), QVariant::fromValue(Status::Published));
combo->addItem(tr("Archived"), QVariant::fromValue(Status::Archived));

connect(combo, &QComboBox::currentIndexChanged, this, [combo] {
    const auto status = combo->currentData().value<Status>();
    applyStatus(status);
});
```

显示文本可以翻译、调整、加图标；业务值放在 `Qt::UserRole`，这样不会被文案变化影响。

## 2. 依赖与对象关系

- 头文件：`#include <QComboBox>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：`QFontComboBox`

### 模型/视图结构

普通 `addItem()` 背后也有模型，默认通常是内部 `QStandardItemModel`。弹出列表由 `QAbstractItemView` 显示，绘制由 delegate 负责。你可以替换 model、view、delegate，也可以只使用便利 API。

### 可编辑模式

`setEditable(true)` 后，组合框内部会有一个 `QLineEdit`。此时 `currentText` 可能是用户正在输入的文本，不一定对应某个已有 index。validator、completer、insert policy 都只在可编辑模式下真正有意义。

### 信号语义

`activated()` 表示用户激活了某项，即使选项没变也会发出；`currentIndexChanged()` 表示当前索引实际变化；`highlighted()` 表示弹出列表中高亮项变化。程序设置当前项会触发 changed，但不会等同于用户 activated。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum InsertPolicy` | 可编辑组合框中新文本如何插入列表。 |
| `enum class LabelDrawingMode` | Qt 6.9 起，关闭状态标签由 style 还是 delegate 绘制。 |
| `enum SizeAdjustPolicy` | 内容变化时 size hint 如何调整。 |
| `count : int` | 项目数量。 |
| `currentIndex : int` | 当前行号，空或无效为 `-1`。 |
| `currentText : QString` | 当前显示/编辑文本。 |
| `currentData : QVariant` | 当前项指定 role 的数据，默认 `Qt::UserRole`。 |
| `editable : bool` | 是否允许用户输入文本。 |
| `duplicatesEnabled : bool` | 用户输入新项时是否允许重复。 |
| `insertPolicy : InsertPolicy` | 用户输入新项后的插入位置策略。 |
| `placeholderText : QString` | 无有效索引时显示的提示；可编辑时交给 line edit。 |
| `modelColumn : int` | 从模型哪一列取显示内容。 |
| `maxCount : int` | 最大项目数。 |
| `maxVisibleItems : int` | 弹出列表最多显示多少项。 |
| `minimumContentsLength : int` | size hint 至少按多少字符宽度估算。 |
| `sizeAdjustPolicy : SizeAdjustPolicy` | 尺寸随内容调整策略。 |
| `iconSize : QSize` | 项目图标最大尺寸。 |
| `frame : bool` | 是否绘制边框。 |
| `QComboBox(QWidget *parent)` | 创建组合框。 |
| `addItem()` / `addItems()` | 追加文本、图标和 user data。 |
| `insertItem()` / `insertItems()` / `insertSeparator()` | 在指定位置插入项目或分隔符。 |
| `removeItem(int)` / `clear()` | 移除项目或清空列表。 |
| `itemText()` / `setItemText()` | 读取或设置某项显示文本。 |
| `itemIcon()` / `setItemIcon()` | 读取或设置某项图标。 |
| `itemData()` / `setItemData()` | 读取或设置某项指定 role 数据。 |
| `findText()` / `findData()` | 按文本或 role 数据查找项目。 |
| `setCurrentIndex()` / `setCurrentText()` | 设置当前项或当前文本。 |
| `setEditText()` / `clearEditText()` | 设置或清空可编辑组合框的编辑文本。 |
| `setEditable()` / `lineEdit()` / `setLineEdit()` | 开启编辑并管理内部 `QLineEdit`。 |
| `setValidator()` / `validator()` | 给可编辑文本设置校验器。 |
| `setCompleter()` / `completer()` | 给可编辑文本设置补全器。 |
| `setModel()` / `model()` | 替换或读取底层模型。 |
| `setView()` / `view()` | 替换或读取弹出视图。 |
| `setItemDelegate()` / `itemDelegate()` | 设置或读取项目委托。 |
| `setRootModelIndex()` / `rootModelIndex()` | 让 combo 显示模型的某个子树。 |
| `showPopup()` / `hidePopup()` | 打开或关闭下拉弹窗，可重写自定义弹窗。 |
| `activated(int)` / `textActivated(QString)` | 用户激活某项时发出。 |
| `currentIndexChanged(int)` / `currentTextChanged(QString)` | 当前索引或文本实际变化时发出。 |
| `highlighted(int)` / `textHighlighted(QString)` | 弹出列表高亮项变化时发出。 |
| `editTextChanged(QString)` | 可编辑文本变化时发出。 |
| `sizeHint()` / `minimumSizeHint()` | 推荐尺寸。 |
| `initStyleOption(QStyleOptionComboBox *)` | 为绘制准备 style option。 |
| 输入、鼠标、键盘、滚轮、焦点、绘制事件 | 支撑弹窗、编辑、选择和平台交互。 |

## 4. API 逐项说明

### `enum QComboBox::InsertPolicy`

只影响可编辑组合框：用户输入一个列表中不存在的新文本后，应该不插入、插到顶部、替换当前项、插到底部、插到当前项前后，还是按字母顺序插入。

历史记录类输入常用 `InsertAtTop` 或 `InsertAtBottom`；固定枚举选择应使用 `NoInsert`，避免用户随手把非法项加入列表。

### `enum class QComboBox::LabelDrawingMode`

Qt 6.9 起控制关闭状态下的当前项标签如何绘制。`UseStyle` 交给 style，最符合平台；`UseDelegate` 用 item delegate 绘制，适合弹出列表和关闭状态需要完全一致的复杂项。

使用 `UseDelegate` 时要确保 delegate 能在 combo 标签区域也画得合理，不要只按列表项高度和背景假设绘制。

### `enum QComboBox::SizeAdjustPolicy`

控制内容变化时组合框推荐尺寸如何调整。`AdjustToContents` 最准确但可能在大模型上昂贵；`AdjustToContentsOnFirstShow` 是常见折中；`AdjustToMinimumContentsLengthWithIcon` 适合大模型，用固定字符长度估算。

大型数据模型不要让 combo 每次内容变化都扫描所有项计算宽度。

### 当前项属性：`count` / `currentIndex` / `currentText` / `currentData`

`count()` 是项目数。`currentIndex()` 是当前行，空列表或无有效选择时为 `-1`。`currentText()` 是显示文本；可编辑时可能是 line edit 内容。`currentData(role)` 读取当前项 role 数据。

业务逻辑优先读 `currentData(Qt::UserRole)`。显示文本会被翻译、重命名或重复，拿它当数据库 key 迟早会痛。

### 可编辑属性：`editable` / `duplicatesEnabled` / `insertPolicy`

`editable` 开启后用户可以输入文本；关闭时 validator 和 completer 会被移除。`duplicatesEnabled` 只限制用户输入造成的重复，程序仍可插入重复项。`insertPolicy` 决定新文本如何进入列表。

如果你需要“用户可以输入，但不自动污染候选列表”，组合是 `setEditable(true)` 加 `setInsertPolicy(QComboBox::NoInsert)`。

### 外观属性：`frame` / `iconSize` / `placeholderText`

`frame` 控制边框；`iconSize` 控制项目图标最大尺寸；`placeholderText` 在无有效索引时显示。不可编辑 combo 若先添加了项目，想显示 placeholder 通常还要 `setCurrentIndex(-1)`。

可编辑 combo 的 placeholder 实际由内部 `QLineEdit` 处理。

### 容量与尺寸属性：`maxCount` / `maxVisibleItems` / `minimumContentsLength` / `sizeAdjustPolicy`

`maxCount` 限制项目数量，设置得小于当前数量会截断额外项。`maxVisibleItems` 控制弹窗可见项数，但某些平台 style 可能忽略。`minimumContentsLength` 和 `sizeAdjustPolicy` 共同影响尺寸提示。

选项多时，不要只提高 `maxVisibleItems`。用户仍然需要搜索、分组或补全。

### 模型属性：`modelColumn`

指定显示模型的哪一列。可编辑 combo 中，这一列也会影响补全使用的列。

多列模型中，如果显示列和业务数据列不同，应把业务 id 放在 role 里，而不是依赖隐藏列文本。

### 构造和析构

`QComboBox(QWidget *parent)` 创建组合框，默认有内部模型。析构时清理控件自身；外部传入的 model、view、delegate 的生命周期要按 Qt 对象父子关系或你的持有策略确认。

替换外部模型时，不要让 combo 指向即将销毁的模型。

### 添加和插入项目

`addItem()` / `insertItem()` 可加入文本、图标和 user data；`addItems()` / `insertItems()` 批量加入文本；`insertSeparator()` 插入分隔符。

批量填充前可以暂时 `blockSignals(true)`，填完再设置当前索引并恢复信号，避免中间状态触发业务逻辑。

### 删除和清空

`removeItem(index)` 删除单项；`clear()` 清空所有项。删除当前项会改变当前索引，并可能触发 changed 信号。

如果 combo 绑定外部模型，删除行为会作用到模型数据；不要把它当成只清 UI 缓存。

### 单项读写：text、icon、data

`itemText()`、`itemIcon()`、`itemData()` 读取某项；`setItemText()`、`setItemIcon()`、`setItemData()` 修改某项。

`itemData()` 默认 role 是 `Qt::UserRole`，非常适合保存枚举、数据库 id、路径、配置 key。

### 查找：`findText()` / `findData()`

按显示文本或 role 数据查找项目，找不到返回 `-1`。可传 `Qt::MatchFlags` 控制精确、大小写、包含等匹配方式。

查业务对象时用 `findData()`。查显示文本时要考虑翻译和重复项。

### 当前项设置：`setCurrentIndex()` / `setCurrentText()` / `setEditText()` / `clearEditText()`

`setCurrentIndex()` 直接选行。不可编辑 combo 的 `setCurrentText()` 会查找匹配文本并选中；可编辑 combo 的 `setCurrentText()` 类似设置编辑文本。`setEditText()` 专门设置内部 line edit 文本；`clearEditText()` 清空编辑文本但不一定清列表。

初始化时先填项目，再设置当前索引；需要显示 placeholder 时设置 `-1`。

### line edit、validator、completer

`setEditable(true)` 后可通过 `lineEdit()` 取得内部编辑器，或用 `setLineEdit()` 替换。`setValidator()` 和 `setCompleter()` 作用在可编辑文本上。

关闭 editable 会移除 validator 和 completer。若之后再开启，需要重新设置。

### 模型、视图、委托

`setModel()` 替换数据源；`setView()` 替换弹出视图；`setItemDelegate()` 定制项目绘制；`setRootModelIndex()` 让 combo 只显示模型某个子树。

这套 API 让 combo 可以显示真实模型数据，而不是复制一份字符串列表。模型较复杂时，优先走 model/view，而不是反复 `clear()` + `addItem()`。

### 弹窗控制：`showPopup()` / `hidePopup()`

打开或关闭下拉弹窗。可重写以提供自定义弹窗，但重写后要维护内部状态，关闭自定义弹窗时应调用基类 `hidePopup()` 复位。

普通业务代码很少需要主动调用，除非做自动展开或特殊交互。

### 信号：activated、changed、highlighted、edited

`activated()` / `textActivated()` 表示用户激活某项，即使当前项没变也会发。`currentIndexChanged()` / `currentTextChanged()` 表示状态变化，程序设置也会触发。`highlighted()` / `textHighlighted()` 是弹窗里高亮项变化。`editTextChanged()` 只在可编辑文本变化时有意义。

要响应用户选择，用 `activated()`；要同步当前状态，用 `currentIndexChanged()`；要预览弹窗高亮，用 `highlighted()`。

### 绘制、输入和事件

`initStyleOption()` 准备绘制状态；`paintEvent()` 绘制关闭状态；键盘、鼠标、滚轮、焦点和输入法事件共同支持打开弹窗、选择项目、编辑文本。`wheelEvent()` 尤其容易导致鼠标滚轮无意改变选择。

在滚动区域或表单中，若用户滚轮经过 combo 导致值变化，可以考虑在子类中过滤 wheel，或要求获得焦点后才响应。

## 5. 深入实践与常见坑

### 不要把显示文本当业务 id

显示文本会翻译、重复、调整文案。把稳定值放进 `Qt::UserRole`，用 `currentData()` 读取。

### 区分用户选择和程序同步

`currentIndexChanged()` 会被程序设置触发。初始化和刷新列表时若连接了业务逻辑，要么调整连接时机，要么临时阻塞信号。

### 可编辑组合框不是万能输入框

如果用户主要是自由输入，只是偶尔参考候选，用 `QLineEdit + QCompleter` 更轻。combo 更适合“输入值也可能进入候选集合”的场景。

### 大模型要控制尺寸策略

`AdjustToContents` 在内容多时可能昂贵。大数据列表使用 `AdjustToMinimumContentsLengthWithIcon`，并设置合理 `minimumContentsLength`。

### 弹出视图可以定制，但成本不低

换 view/delegate 可以做图标、分组、富显示，但也要处理键盘、hover、尺寸和关闭行为。简单列表不要过度定制。
