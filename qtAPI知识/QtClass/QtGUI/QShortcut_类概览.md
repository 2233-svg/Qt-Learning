# Qt QShortcut：窗口内快捷键的注册、作用域与激活信号

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QShortcut>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`  
> 类型定位：把 `QKeySequence` 绑定到激活信号的非可视对象

## 1. 它解决什么问题

`QShortcut` 用来把一个或多个键盘快捷键注册到 Qt 对象层，并在用户按下匹配的 `QKeySequence` 时发出：

- `activated()`：快捷键明确匹配；
- `activatedAmbiguously()`：当前按键与多个快捷键匹配，无法唯一决定目标。

它适合菜单命令、编辑器操作、工具窗口快捷操作、全局应用命令和自定义键盘交互。`QShortcut` 本身不是按钮，也不绘制任何界面；它依赖 Qt 的键盘事件分发和快捷键上下文来判断何时有效。

## 2. 构建与最小用法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QShortcut>
#include <QWidget>

auto *shortcut = new QShortcut(
    QKeySequence(Qt::CTRL | Qt::Key_S),
    window);

QObject::connect(shortcut, &QShortcut::activated,
                 window, &QWidget::close);
```

实际项目通常把它绑定到一个明确的命令对象或 lambda：

```cpp
auto *shortcut = new QShortcut(QKeySequence::StandardKey::Save,
                               window,
                               window,
                               [window] {
                                   window->update();
                               });
```

第二种写法使用 context 对象管理回调连接的生命周期。若 `window` 被销毁，连接会自动断开。

## 3. 父对象、作用域和激活条件

`QShortcut` 是 `QObject`，构造时必须提供 `parent`。在 widget 应用中，parent 通常是拥有该快捷键作用域的 `QWidget`。它不需要另建一个可见控件。

`context` 属性决定快捷键在哪个范围内有效：

| 上下文 | 典型含义 |
| --- | --- |
| `Qt::WidgetShortcut` | parent widget 自身处于活动状态时有效 |
| `Qt::WidgetWithChildrenShortcut` | parent widget 或其子控件处于活动范围时有效 |
| `Qt::WindowShortcut` | parent 所属窗口处于活动窗口时有效，默认值 |
| `Qt::ApplicationShortcut` | 应用范围内有效，不限于某个活动窗口 |

具体激活仍受窗口激活状态、键盘焦点、平台快捷键和其他快捷键冲突影响。`ApplicationShortcut` 也不是绕过操作系统保留快捷键的保证。

## 4. 属性

### 4.1 `key : QKeySequence`

单个快捷键序列属性。`setKey()` 是旧的单键序列入口；设置空序列或整数 0 可用于清空该键。Qt 6 的多序列场景应优先使用 `setKeys()` 和 `keys()`。

### 4.2 `enabled : bool`

通过 `setEnabled()` 和 `isEnabled()` 控制快捷键是否参与匹配。禁用 shortcut 不会删除对象、清除键序列或断开激活信号。

### 4.3 `autoRepeat : bool`

控制按住按键时是否允许自动重复激活。若命令不适合重复执行，例如“提交一次表单”或“打开一次对话框”，应显式关闭：

```cpp
shortcut->setAutoRepeat(false);
```

它只影响快捷键激活，不会改变底层键盘设备的系统重复设置。

### 4.4 `context : Qt::ShortcutContext`

设置快捷键作用域。修改 context 不会修改 key sequence，但会立刻改变之后的匹配范围。

## 5. 单键、多键序列和多个替代序列

`QKeySequence` 可以是多步序列，例如 `Ctrl+K, Ctrl+C`。这不是同时按下四个键，而是按顺序输入两个 chord。Qt 会在事件序列中等待后续按键，因此应用要考虑用户输入被其他快捷键或焦点控件接管的情况。

Qt 6 提供多个快捷键序列：

```cpp
shortcut->setKeys({
    QKeySequence(Qt::CTRL | Qt::Key_S),
    QKeySequence(Qt::CTRL | Qt::SHIFT | Qt::Key_S)
});
```

`keys()` 返回当前所有序列；`setKeys(QKeySequence::StandardKey)` 则使用 Qt 对标准命令的平台映射。多个序列是同一个 `QShortcut` 的替代触发方式，不是创建多个独立 shortcut。

`setKey()` 只设置单个序列，适合简单场景。调用它会替换当前键，而不是追加到 `keys()`。

## 6. 激活和歧义

```cpp
connect(shortcut, &QShortcut::activated,
        this, &Editor::save);

connect(shortcut, &QShortcut::activatedAmbiguously,
        this, &Editor::showShortcutConflict);
```

### `activated()`

当 Qt 能够唯一确定某个快捷键时发出。它不携带按下的是哪个替代序列，因此如果业务需要区分具体序列，可以为不同序列创建不同 `QShortcut`，或在命令层设计统一语义。

### `activatedAmbiguously()`

当多个 shortcut 或多个匹配路径造成歧义时发出。它不是普通激活的第二次通知，也不表示快捷键一定会随后发出 `activated()`。应用应检查重复注册、上下文重叠和多步序列前缀。

## 7. 构造函数族

### 7.1 仅提供 parent

```cpp
explicit QShortcut(QObject *parent);
```

创建没有键序列的 shortcut 对象，之后可通过 `setKey()` 或 `setKeys()` 设置。parent 负责对象所有权。

### 7.2 `QKeySequence` 构造

```cpp
explicit QShortcut(const QKeySequence &key,
                   QObject *parent,
                   const char *member = nullptr,
                   const char *ambiguousMember = nullptr,
                   Qt::ShortcutContext context = Qt::WindowShortcut);
```

这是兼容旧式字符串槽连接的构造函数。`member` 和 `ambiguousMember` 是旧的 `SIGNAL`/`SLOT` 字符串接口；新代码更适合使用 functor 或显式连接 `activated()`、`activatedAmbiguously()`。

### 7.3 `QKeySequence::StandardKey` 构造

```cpp
explicit QShortcut(QKeySequence::StandardKey key,
                   QObject *parent,
                   const char *member = nullptr,
                   const char *ambiguousMember = nullptr,
                   Qt::ShortcutContext context = Qt::WindowShortcut);
```

标准键由 Qt 根据平台和键盘布局解析，例如保存、复制、粘贴等命令。使用标准键比硬编码 `Ctrl` 组合更适合跨平台命令，但具体序列仍可能因平台而不同。

### 7.4 functor 构造

头文件提供以 functor 为回调的模板重载，分别支持：

- 只连接明确激活回调；
- 指定一个 context 对象后连接明确激活回调；
- 同时连接明确激活和歧义激活回调；
- 为两个回调分别指定 context 对象。

示例：

```cpp
new QShortcut(QKeySequence(Qt::CTRL | Qt::Key_Z),
              window,
              window,
              [window] { window->update(); });

new QShortcut(QKeySequence(Qt::CTRL | Qt::Key_F),
              window,
              window,
              [window] { window->show(); },
              window,
              [window] { window->statusBar()->showMessage(
                  QStringLiteral("快捷键冲突")); });
```

把 context 对象传给 functor 重载，可以让 Qt 在 context 被销毁时自动断开回调。无 context 的 contextless connect 受 `QT_NO_CONTEXTLESS_CONNECT` 配置影响，并且不适合捕获可能先于 shortcut 销毁的对象。

## 8. API 语义

### `void setKey(const QKeySequence &key)` / `QKeySequence key() const`

设置或读取单个键序列。设置空序列会让该 shortcut 没有可匹配的单键；它不会销毁对象。若应用使用多个替代序列，应使用 `setKeys()`，不要反复调用 `setKey()` 试图追加。

### `void setKeys(QKeySequence::StandardKey key)`

按标准命令设置快捷键集合。标准命令可能映射为多个平台相关 `QKeySequence`，因此应通过 `keys()` 查看实际结果。

### `void setKeys(const QList<QKeySequence> &keys)` / `QList<QKeySequence> keys() const`

设置或读取多个替代序列。传入空列表表示没有快捷键。列表项为空序列时不应依赖其产生激活；应在设置前清理无效序列。

### `void setEnabled(bool enable)` / `bool isEnabled() const`

启用或禁用 shortcut。禁用状态下不会响应快捷键，但对象仍保留原有 key、context、WhatsThis 和信号连接。

### `void setContext(Qt::ShortcutContext context)` / `Qt::ShortcutContext context() const`

设置或读取快捷键作用域。context 是匹配范围，不是焦点策略；窗口和 widget 的激活状态仍由 Qt 和平台事件系统决定。

### `void setAutoRepeat(bool on)` / `bool autoRepeat() const`

设置或读取按键自动重复行为。命令若不可幂等或执行成本高，应考虑关闭。

### `void setWhatsThis(const QString &text)` / `QString whatsThis() const`

设置和读取用于 WhatsThis 帮助的文本。它是辅助说明，不会改变快捷键的显示文本、匹配逻辑或菜单标题。

### `QWidget *parentWidget() const`

Qt 6.0 起弃用。旧接口用于把 QObject parent 转为 QWidget。新代码应使用 `parent()` 配合 `qobject_cast<QWidget *>`，并处理 parent 不是 widget 的情况。

### `int id() const`

Qt 6.0 起弃用。旧代码可用它识别 shortcut，但新代码应直接连接 `activated()` 信号或在命令层管理对象引用。不要把这个内部注册 ID 当作稳定持久化标识。

### `bool event(QEvent *e)`

受保护的事件入口。`QShortcut` 用它参与 Qt 对象事件分发。一般不需要重写；若子类重写，必须理解 shortcut 事件处理并妥善调用基类实现，否则可能破坏激活行为。

### `QShortcut::~QShortcut()`

销毁 shortcut。带 parent 时通常由 QObject 父对象自动销毁；销毁会移除快捷键注册并断开以该对象为 sender 的连接。

## 9. 生命周期、线程与事件循环

`QShortcut` 的匹配依赖 GUI 线程的键盘事件分发。它通常应在 GUI 线程创建和使用，并由 widget 或窗口对象作为 parent。不要在工作线程中直接创建一个期待接收 GUI 键盘事件的 shortcut。

parent 销毁后 shortcut 会一起销毁。functor 连接使用 context 时，context 销毁会自动断开回调；lambda 捕获的裸指针不会因为捕获动作本身获得生命周期保护。

## 10. 常见误区与排查顺序

### 10.1 快捷键完全不触发

按以下顺序检查：

1. `keys()` 是否为空；
2. `isEnabled()` 是否为 `true`；
3. parent 是否属于正确的活动 widget/window；
4. `context()` 是否过窄；
5. 是否有其他 shortcut、菜单或平台保留键冲突；
6. 多步 `QKeySequence` 是否被实际按下。

### 10.2 把 `ApplicationShortcut` 当成系统全局快捷键

它是 Qt 应用范围内的快捷键，只在应用获得相关事件时有效，不能监听应用外的系统键盘。

### 10.3 使用旧式字符串槽

字符串接口容易隐藏签名错误，优先使用类型安全的 `connect` 或 functor 构造。旧接口仍可能出现在维护代码中，但不应作为新代码首选。

### 10.4 忽略歧义信号

多个窗口或 widget 上相同快捷键、前缀序列和重叠 context 都可能产生歧义。只监听 `activated()` 会让命令看起来“偶尔失效”。

### 10.5 误解 `autoRepeat`

它不是“按一次只触发一次”的全局保证。关闭后只是禁止按住键时的自动重复激活，用户快速进行多次独立按键仍可能触发多次。

### 10.6 把 `setKey()` 当作追加 API

`setKey()` 会替换单键配置。需要多个候选序列时，使用 `setKeys(QList<QKeySequence>)`。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 属性 | `key : QKeySequence` | 单个快捷键序列 | 多序列场景用 `keys()`/`setKeys()` |
| 属性 | `enabled : bool` | 是否参与匹配 | 禁用不销毁对象和连接 |
| 属性 | `autoRepeat : bool` | 是否允许按住键重复激活 | 不改变系统键盘重复设置 |
| 属性 | `context : Qt::ShortcutContext` | 快捷键作用域 | 不是系统全局快捷键开关 |
| 构造 | `QShortcut(QObject *parent)` | 创建空 shortcut | parent 负责所有权 |
| 构造 | `QShortcut(const QKeySequence &, QObject *, const char *, const char *, ShortcutContext)` | 用序列创建 | 字符串槽为旧式接口 |
| 构造 | `QShortcut(QKeySequence::StandardKey, QObject *, const char *, const char *, ShortcutContext)` | 用平台标准键创建 | 实际序列由平台映射决定 |
| 构造 | functor 重载 | 直接绑定 lambda/成员函数 | 优先提供 context 对象 |
| 析构 | `~QShortcut()` | 移除快捷键并销毁对象 | parent 通常自动管理 |
| 设置 | `setKey(const QKeySequence &)` | 替换单个序列 | 不会追加 |
| 查询 | `key() const` | 读取单个序列 | 空序列表示无单键 |
| 设置 | `setKeys(QKeySequence::StandardKey)` | 设置标准键集合 | 可能得到多个平台序列 |
| 设置 | `setKeys(const QList<QKeySequence> &)` | 设置多个替代序列 | 空列表表示无快捷键 |
| 查询 | `keys() const` | 读取实际序列集合 | 用于诊断平台映射 |
| 设置 | `setEnabled(bool)` | 启用/禁用 | 不清除 key |
| 查询 | `isEnabled() const` | 查询启用状态 | 仍要检查 context 和冲突 |
| 设置 | `setContext(ShortcutContext)` | 设置作用域 | 活动窗口状态仍重要 |
| 查询 | `context() const` | 查询作用域 | `WindowShortcut` 是默认值 |
| 设置 | `setAutoRepeat(bool)` | 设置自动重复 | 不限制独立快速按键 |
| 查询 | `autoRepeat() const` | 查询自动重复 | 适合确认命令策略 |
| 设置 | `setWhatsThis(const QString &)` | 设置帮助文本 | 不改变匹配逻辑 |
| 查询 | `whatsThis() const` | 读取帮助文本 | 仅辅助说明 |
| 查询 | `parentWidget() const` | 获取 widget parent | Qt 6.0 起弃用 |
| 查询 | `id() const` | 获取旧式注册 ID | Qt 6.0 起弃用，不是稳定 ID |
| 信号 | `activated()` | 唯一匹配时通知 | 不说明具体替代序列 |
| 信号 | `activatedAmbiguously()` | 匹配有歧义时通知 | 不是 activated 的补充回调 |
| 事件 | `event(QEvent *)` | 参与 shortcut 事件分发 | protected，重写需谨慎 |

---

### 一句话总结

`QShortcut` 是依赖 GUI 事件分发的快捷键对象：用 parent 管理生命周期，用 `context` 控制作用域，用 `keys()` 支持多个替代序列，用 `activated()`/`activatedAmbiguously()` 区分唯一匹配和冲突；新代码优先使用类型安全的 functor 连接，并把平台标准键和应用内快捷键范围分开理解。
