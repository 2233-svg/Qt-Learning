# QKeySequence：跨平台的快捷键序列值

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QKeySequence>`  
> 模块：`Qt6::Gui`  
> 相关类型：`QAction`、`QShortcut`、`QKeyCombination`、`QKeyEvent`、`QSettings`

`QKeySequence` 表示一个快捷键序列，而不是一次键盘事件。一个序列由一到四个“按键组合”构成；例如 `Ctrl+S` 是一个组合，`Ctrl+K, Ctrl+C` 是两个组合组成的多段快捷键。它负责表达、比较、显示和序列化快捷键，实际把快捷键绑定到命令的是 `QAction`、`QShortcut` 等类型。

## 它解决的问题

桌面程序里的“保存”“复制”“查找”看起来都有固定快捷键，但不同平台、键盘布局和用户语言下并不相同。例如，macOS 菜单通常把 Qt 语义中的 `Ctrl` 显示并映射为 Command 键；同一个标准动作还可能有多个平台惯用的替代快捷键。

`QKeySequence` 将这件事拆成两层：

1. 用 `StandardKey` 描述“保存”“关闭”“撤销”这类动作语义，让 Qt 选择当前平台的默认快捷键。
2. 用按键组合或文本描述自定义快捷键，并提供可显示和可持久化的两种文本格式。

它常见于：

- 给 `QAction` 设置菜单项、工具栏按钮的默认快捷键。
- 用 `QShortcut` 给一个窗口或控件注册自定义命令。
- 在快捷键设置页保存用户改过的绑定。
- 实现类似编辑器的两段快捷键，例如 `Ctrl+K, Ctrl+C`。
- 从带 `&` 的菜单文本提取助记键，例如 `E&xit` 对应 `Alt+X`。

## 构建与基本模型

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(my_app PRIVATE Qt6::Gui Qt6::Widgets)
```

`QKeySequence` 是无父对象、无事件循环依赖的值类型，不是 `QObject`。可以按值保存、返回和传递；Qt 对它使用隐式共享实现，复制通常很轻量。它不拥有窗口、动作或快捷键注册，离开作用域只会销毁这个值本身。

一个序列最多四段，超过四段不是可表达的 `QKeySequence`。每一段应是一个 `QKeyCombination`，即一个 `Qt::Key` 加零个或多个修饰键。不要把“同时按的键”与“依次按的多段快捷键”混为一谈：

```cpp
#include <QKeyCombination>
#include <QKeySequence>

const QKeySequence save(Qt::CTRL | Qt::Key_S); // 一段：同时按 Ctrl 和 S

const QKeySequence comment(
    QKeyCombination(Qt::CTRL, Qt::Key_K),
    QKeyCombination(Qt::CTRL, Qt::Key_C));     // 两段：先 Ctrl+K，再 Ctrl+C
```

旧的 `int` 构造函数仍可用，但新代码更适合使用 `QKeyCombination`，类型边界更清楚。

## 首选：用标准动作而非硬编码按键

给常见命令设默认快捷键时，优先写动作语义：

```cpp
#include <QAction>
#include <QKeySequence>

auto *saveAction = new QAction(tr("&Save"), this);
saveAction->setShortcut(QKeySequence::Save);

auto *closeAction = new QAction(tr("&Close"), this);
closeAction->setShortcuts(QKeySequence::keyBindings(QKeySequence::Close));
```

`QKeySequence(QKeySequence::Save)` 选取当前平台 `Save` 绑定列表的第一个元素，也就是主快捷键。`keyBindings()` 则返回完整列表：第一个仍是主快捷键，后续元素可作为同一平台上的替代快捷键。需要支持所有平台惯用组合时，传整个列表给 `QAction::setShortcuts()`。

`StandardKey` 是跨平台“动作语义”的最佳入口，但不是任意业务操作的枚举。诸如 `ExportReport`、`ToggleSidebar` 之类的程序专用命令，需要自行定义组合或提供用户设置页。

### 常用 `StandardKey` 分类

| 分类 | 常用值 | 适合绑定的命令 |
| --- | --- | --- |
| 文件与窗口 | `New`、`Open`、`Close`、`Save`、`SaveAs`、`Print`、`Quit`、`FullScreen` | 文档、窗口和应用级命令 |
| 编辑 | `Cut`、`Copy`、`Paste`、`Undo`、`Redo`、`SelectAll`、`Find`、`Replace` | 文本、表格、画布编辑器 |
| 查找与导航 | `FindNext`、`FindPrevious`、`Back`、`Forward`、`NextChild`、`PreviousChild` | 浏览、标签页和结果导航 |
| 文本光标 | `MoveToNextWord`、`SelectEndOfLine`、`DeleteStartOfWord` 等 | 编辑控件或自定义文本组件 |
| 格式与视图 | `Bold`、`Italic`、`Underline`、`ZoomIn`、`ZoomOut` | 富文本、预览和画布 |
| 状态 | `HelpContents`、`WhatsThis`、`Cancel`、`Preferences` | 帮助、取消和设置入口 |

在 Apple 平台，Qt 文档中的 `Ctrl` 语义会对应键盘上的 Command，`Meta` 则对应 Control。因此跨平台代码应继续表达 Qt 语义，不要为了某个平台自行交换 `ControlModifier` 与 `MetaModifier`。

## 自定义快捷键：文本、组合与翻译

固定的程序专用快捷键可以由 `QKeyCombination` 构造：

```cpp
const QKeySequence openCommand(QKeyCombination(Qt::CTRL, Qt::Key_O));
const QKeySequence twoStroke(
    QKeyCombination(Qt::CTRL, Qt::Key_K),
    QKeyCombination(Qt::CTRL, Qt::Key_U));
```

也可以从文本解析。文本可包含最多四段，段与段之间用逗号分隔：

```cpp
const QKeySequence openFromText(
    QStringLiteral("Ctrl+O"),
    QKeySequence::PortableText);

const QKeySequence multiStroke(
    QStringLiteral("Ctrl+K, Ctrl+U"),
    QKeySequence::PortableText);
```

字符串构造函数默认按 `NativeText` 解析，适合与 `tr()` 配合，让翻译人员为当地键盘布局调整可读的快捷键文本：

```cpp
auto *openAction = new QAction(tr("&Open..."), this);
openAction->setShortcut(
    QKeySequence(tr("Ctrl+O", "File menu shortcut")));
```

这不是标准动作的替代品。布局差异较大时，硬编码字符串和硬编码键值都可能不符合用户习惯；只有 `StandardKey` 能让 Qt 按平台惯例选择对应组合。

## `NativeText` 与 `PortableText` 的边界

`SequenceFormat` 不是单纯的显示选项，它决定文本是否适合跨平台保存。

| 格式 | 用途 | 关键边界 |
| --- | --- | --- |
| `NativeText` | 向当前用户显示快捷键 | 名称会翻译；Apple 平台的显示会贴近菜单栏形式；不适合写入配置文件。 |
| `PortableText` | 读写配置、同步设置、测试数据 | 稳定的可移植格式；不承诺符合每个平台的本地展示习惯。 |

用户设置页通常应同时做两件不同的事：显示时调用 `NativeText`，保存时调用 `PortableText`。

```cpp
#include <QSettings>

const QKeySequence shortcut(QKeyCombination(Qt::CTRL, Qt::Key_1));

// UI 标签使用本地化文本。
shortcutLabel->setText(shortcut.toString(QKeySequence::NativeText));

// 配置只保存可移植文本。
settings.setValue(
    "shortcuts/selectFirst",
    shortcut.toString(QKeySequence::PortableText));

const QKeySequence restored = QKeySequence::fromString(
    settings.value("shortcuts/selectFirst").toString(),
    QKeySequence::PortableText);
```

空字符串会得到空序列；解析用户输入后应以 `isEmpty()` 区分“用户清除了快捷键”与“可用绑定”。如果产品需要区分无效输入和有意清空，不能只依赖 `fromString()` 的返回值，应另外保留原始输入、校验规则或设置页状态。

## 多段快捷键与 `matches()`

多段快捷键的匹配顺序容易写反。将“已经输入的前缀”作为接收者，把“完整目标序列”作为参数：

```cpp
const QKeySequence target(
    QKeyCombination(Qt::CTRL, Qt::Key_K),
    QKeyCombination(Qt::CTRL, Qt::Key_C));

const QKeySequence firstStroke(QKeyCombination(Qt::CTRL, Qt::Key_K));

switch (firstStroke.matches(target)) {
case QKeySequence::PartialMatch:
    // 已命中 Ctrl+K；继续等待下一段。
    break;
case QKeySequence::ExactMatch:
    // 完整命中；执行命令。
    break;
case QKeySequence::NoMatch:
    // 取消当前前缀或交给普通按键处理。
    break;
}
```

`ExactMatch` 表示两个序列相同；`PartialMatch` 表示接收者是目标序列的有效前缀。一个重要边界是：若传入参数 `seq` 比接收者更短，`matches()` 返回 `NoMatch`。因此上述调用写成 `target.matches(firstStroke)` 不会得到“继续等待”的结果。

实际控件一般无需手写这套状态机，使用 `QShortcut` 或 `QAction` 就能交给 Qt 的快捷键映射处理。只有实现自定义命令分发器、快捷键录制器或输入状态机时，才需要直接使用 `matches()`。

## 助记键不是普通快捷键

菜单文本中的单个 `&` 指定助记键：

```cpp
const QKeySequence exitMnemonic = QKeySequence::mnemonic(QStringLiteral("E&xit"));
// exitMnemonic 等价于 Alt+X。
```

`mnemonic("&Quit")` 得到 `Alt+Q`；没有 `&` 则返回空序列。它服务于菜单、标签等 UI 文本中的访问键，不应当用来实现用户自定义的全局快捷键。

平台可能关闭自动助记键。尤其 macOS 默认不启用；在该特性关闭时，`mnemonic()` 返回空序列。存在一个未在 Qt 公共头文件中声明的 `qt_set_sequence_auto_mnemonic(bool)` 辅助函数，但它属于不便携的低层入口，普通应用不应通过手工声明原型来依赖它。

## 生命周期、线程与容器

- `QKeySequence` 没有所有权关系，也没有 parent 参数。把它交给 `QAction::setShortcut()` 后，`QAction` 保存的是自己的值；原局部变量可立即销毁。
- 可在容器、`QVariant` 和 `QDataStream` 中传递。`QHash<QKeySequence, T>` 使用 Qt 提供的 `qHash()`；`QMap` 可使用比较运算符。
- 它不操作 GUI 资源，本身无需 GUI 事件循环。但和任何普通 C++ 值一样，不能让多个线程无同步地同时读写同一个对象实例；跨线程传递副本，或在外部加同步。
- `operator<` 提供的是用于有序容器的任意稳定比较，不是按用户可见文本或按键语义排序。不要拿它做“快捷键显示顺序”或业务优先级。

## 常见错误

1. **把 `NativeText` 写进配置。** 在另一平台或另一语言环境读回时可能不符合预期。配置使用 `PortableText`。
2. **把 `QKeySequence` 当事件。** 它没有发生时间、按下/释放状态、重复次数或目标控件；这些信息来自 `QKeyEvent`。
3. **给标准命令硬编码 `Ctrl+...`。** `Save`、`Copy`、`Close` 等应优先使用 `StandardKey`。
4. **忽略替代快捷键。** `QKeySequence(StandardKey)` 只取首选组合；需要完整平台绑定时使用 `keyBindings()`。
5. **误判多段匹配方向。** 用 `currentInput.matches(fullShortcut)`，不是反过来。
6. **把 `&` 文本当成全局快捷键定义。** 它只定义助记键，且可能被平台设置禁用。
7. **超过四段。** `QKeySequence` 的上限固定为四个按键组合；更长的命令前缀需要自行设计交互。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QKeySequence()` | 构造空序列。 | `count()` 为 0，`isEmpty()` 为 `true`，`toString()` 返回空字符串。 |
| `QKeySequence(StandardKey key)` | 由标准动作构造主快捷键。 | 平台相关，等价于取 `keyBindings(key)` 的第一个元素；不包含替代组合。 |
| `QKeySequence(const QString &, SequenceFormat)` | 从文本解析序列。 | 默认格式为 `NativeText`；最多逗号分隔四段；需要持久化文本时显式使用 `PortableText`。 |
| `QKeySequence(QKeyCombination, ... )` | 由一到四个类型安全的按键组合构造。 | 推荐的新代码入口；未提供的后续段为空。 |
| `QKeySequence(int, int, int, int)` | 由组合后的键值构造。 | 可将 `Qt::Key` 与修饰键按位组合；为清晰和类型安全，新代码优先 `QKeyCombination`。 |
| 拷贝构造、析构、复制/移动赋值 | 普通值语义。 | 无对象树、无父对象；隐式共享是实现细节，不要据此推断并发写入安全。 |
| `count()` | 返回序列包含的按键组合数。 | 最大值为 4。 |
| `isEmpty()` | 判断是否没有任何按键组合。 | 适合表示未绑定快捷键；不能单独说明原始文本是否输入错误。 |
| `SequenceFormat` | 选择文本格式。 | `NativeText` 给用户显示；`PortableText` 给文件、配置和跨平台交换。 |
| `SequenceMatch` | 表示序列比较结果。 | 取值为 `NoMatch`、`PartialMatch`、`ExactMatch`；多段录入时要保留 `PartialMatch` 状态。 |
| `StandardKey` | 表示平台惯用的命令语义。 | 覆盖文件、编辑、导航、文本操作、格式等标准行为；优先于硬编码组合。 |
| `toString(SequenceFormat)` | 将单个序列转为文本。 | 默认是 `PortableText`；空序列返回空字符串；多段之间以逗号分隔。 |
| `fromString(const QString &, SequenceFormat)` | 从文本生成单个序列。 | 默认是 `PortableText`，应与写入时的格式配对。 |
| `listToString(const QList<QKeySequence> &, SequenceFormat)` | 将多个候选序列编码为一个字符串。 | 适合保存某命令的多个绑定；读取使用 `listFromString()`。 |
| `listFromString(const QString &, SequenceFormat)` | 从字符串恢复多个候选序列。 | 格式必须与 `listToString()` 一致。 |
| `keyBindings(StandardKey)` | 查询标准动作的全部平台绑定。 | 首项是主快捷键，其他项是替代快捷键；结果依目标平台而变。 |
| `matches(const QKeySequence &seq)` | 比较当前序列与另一序列。 | 使用 `current.matches(target)` 检测前缀；若参数比接收者短，结果为 `NoMatch`。 |
| `mnemonic(const QString &text)` | 从含 `&` 的界面文本提取 `Alt+键`。 | 找不到助记符或平台关闭自动助记符时返回空序列。 |
| `operator[](uint index)` | 读取指定位置的 `QKeyCombination`。 | 只读访问；索引应小于 `count()`，不要以它修改序列。 |
| `operator QVariant()` | 转为 `QVariant`。 | 用于属性系统、模型数据或通用设置值；类型信息仍需由接收端正确处理。 |
| `swap(QKeySequence &other)` | 交换两个序列。 | `noexcept` 且很快；适合实现移动或需要交换值的算法。 |
| `operator==` / `operator!=` | 判断两个序列是否相同。 | 比较实际组合，不是比较本地化显示文本。 |
| `operator<` / `>` / `<=` / `>=` | 为有序容器提供比较。 | 排序关系是任意的；可作 `QMap` 键，不应用作用户可见排序规则。 |
| `qHash(const QKeySequence &, size_t)` | 计算哈希值。 | 供 `QHash`、`QSet` 使用；可传 seed，通常无需直接调用。 |
| `QDataStream <<` / `>>` | 写入或读出二进制流。 | 流两端应协商 `QDataStream` 版本；它不是人可编辑的配置格式。 |
| `QDebug <<` | 输出调试表示。 | 仅在未定义 `QT_NO_DEBUG_STREAM` 时提供。 |
| `isDetached()` | 查询当前隐式共享数据是否独占。 | 头文件可见但并非日常业务 API；不要把它用于功能决策或并发控制。 |
| `DataPtr` / `data_ptr()` | 暴露实现数据指针类型和访问入口。 | 属于隐式共享实现配合接口，不应在应用代码中保存、修改或依赖。 |
| `qt_set_sequence_auto_mnemonic(bool)` | 控制自动助记键是否生效。 | 不在 Qt 公共头文件中声明，平台默认值不同；普通应用避免依赖。 |

## 一句话总结

把 `QKeySequence` 当作“快捷键的跨平台值表示”：标准命令选 `StandardKey`，显示选 `NativeText`，保存选 `PortableText`，多段录入用 `current.matches(target)` 判断前缀。
