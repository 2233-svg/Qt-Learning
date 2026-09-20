# Qt QKeyCombination 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QKeyCombination>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 引入版本：Qt 6.0  
> 类型性质：可比较、可哈希、可串流的轻量值类型

## 1. 它解决什么问题

`QKeyCombination` 表示“一个按键 + 零个或多个键盘修饰键”的组合，例如 `Ctrl+S`、`Shift+F5` 或 `Meta+Alt+P`。它把原本容易混淆的整数快捷键编码封装成一个明确的值类型，适合在快捷键描述、事件匹配、哈希容器和持久化代码中传递。

它保存的是组合本身，不负责：

- 判断某个按键事件是否已经发生；
- 处理平台键盘布局；
- 展示本地化快捷键文本；
- 管理 `QShortcut` 或 `QKeySequence`。

需要把组合绑定到 UI 动作时，通常还会与 Qt GUI 模块的 `QKeySequence`、`QKeyEvent` 或 `QShortcut` 配合。

## 2. 实际使用场景

### 2.1 创建快捷键组合

```cpp
const QKeyCombination save = Qt::CTRL | Qt::Key_S;
const QKeyCombination run = Qt::ControlModifier | Qt::Key_F5;
```

`operator|` 支持单个修饰键、修饰键标志集合，以及两套 Qt 修饰键枚举。

### 2.2 从键盘事件中提取组合

在 GUI 事件代码中，可把 `QKeyEvent::key()` 与 `QKeyEvent::modifiers()` 组合为一个 `QKeyCombination`，再和预设值比较：

```cpp
const QKeyCombination pressed(event->modifiers(), event->key());
if (pressed == (Qt::CTRL | Qt::Key_S))
    saveDocument();
```

### 2.3 作为哈希表键

```cpp
QHash<QKeyCombination, QString> commands;
commands.insert(Qt::CTRL | Qt::Key_S, u"save"_qs);
```

`qHash()` 与相等比较语义一致，适合 `QHash`、`QSet` 等哈希容器。

### 2.4 序列化快捷键配置

```cpp
QDataStream stream(device);
stream << (Qt::CTRL | Qt::Key_S);
```

对应的 `operator>>` 可以读回组合值。具体持久化兼容性仍取决于 `QDataStream` 的版本和字节序设置。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QKeyCombination>
```

qmake 工程：

```qmake
QT += core
```

## 4. 最小可用示例

```cpp
constexpr QKeyCombination shortcut(Qt::KeyboardModifiers(Qt::ControlModifier),
                                   Qt::Key_S);

Q_ASSERT(shortcut.key() == Qt::Key_S);
Q_ASSERT(shortcut.keyboardModifiers() == Qt::ControlModifier);

const int encoded = shortcut.toCombined();
const QKeyCombination restored = QKeyCombination::fromCombined(encoded);
Q_ASSERT(restored == shortcut);
```

`QKeyCombination` 的构造、访问和编码转换都是 `constexpr noexcept`，可以用于编译期常量和不抛异常的值传递。

## 5. 核心使用模型

### 5.1 一个组合由 `Qt::Key` 和 modifiers 两部分构成

内部用一个 `int` 保存组合：

- `key()` 返回低位按键部分；
- `keyboardModifiers()` 返回由 `Qt::KeyboardModifierMask` 掩码提取出的修饰键部分；
- `toCombined()` 返回两者按位或后的整数。

Qt 的 `Qt::Key` 值空间为修饰键保留了高位区域，因此不能把任意整数都当作合法组合。`fromCombined()` 的输入契约是：它应当来自一个 `Qt::Key` 值和一个 `Qt::KeyboardModifiers` 值的按位或，最稳妥的来源就是 `toCombined()`。

### 5.2 `Qt::KeyboardModifiers` 与 `Qt::Modifiers`

Qt 提供两套修饰键类型：

| 类型 | 本质 | 常见取值 | 适合场景 |
| --- | --- | --- | --- |
| `Qt::KeyboardModifiers` | `QFlags<Qt::KeyboardModifier>` | `ShiftModifier`、`ControlModifier`、`AltModifier`、`MetaModifier`、`KeypadModifier`、`GroupSwitchModifier` | 键盘事件和完整修饰键状态 |
| `Qt::Modifiers` | `QFlags<Qt::Modifier>` | `SHIFT`、`CTRL`、`ALT`、`META` | 快捷键书写的短名称 |

`Qt::Modifiers` 是面向快捷键的简写集合，不包含 `KeypadModifier`。两者都可以传给 `QKeyCombination`，但如果代码表达的是实际键盘事件状态，优先保留 `Qt::KeyboardModifiers`。

### 5.3 `operator|` 是当前组合运算入口

以下形式都有效：

```cpp
Qt::Key key = Qt::Key_S;
const QKeyCombination a = key | Qt::CTRL;
const QKeyCombination b = Qt::CTRL | key;
const QKeyCombination c = key | Qt::ControlModifier;
const QKeyCombination d = Qt::KeyboardModifiers(Qt::ShiftModifier | Qt::AltModifier)
                         | Qt::Key_F5;
```

修饰键和按键的先后顺序不改变结果。Qt 6.0 起应使用 `operator|`；旧的 `operator+` 已弃用。

### 5.4 组合相等比较的是编码后的 key/modifier 对

`operator==` 判断两个对象的按键和修饰键组合是否相同；`operator!=` 判断是否不同。它不是字符串比较，也不涉及平台上 Command/Ctrl 的显示转换。

## 6. 平台和输入边界

### 6.1 macOS 的 Ctrl/Meta 映射

在 macOS 上，Qt 默认会把 Command 映射为 `Qt::ControlModifier`，把实际 Control 映射为 `Qt::MetaModifier`，以便跨平台快捷键代码中的 `Ctrl+...` 通常符合 macOS 用户预期。`QKeyCombination` 只存储收到的 Qt 修饰键值，不自行做平台映射。

### 6.2 Windows 的 Meta 和键盘布局

在 Windows 键盘上，`Qt::MetaModifier` 通常对应 Windows 键。键盘布局、输入法、AltGr 和平台快捷键抢占都可能影响实际 `QKeyEvent` 产生的组合；`QKeyCombination` 本身只负责保存值。

### 6.3 Keypad 和 GroupSwitch 修饰键

`KeypadModifier` 表示数字键盘按钮状态；在 macOS 上方向键也可能被视作数字键盘的一部分。`GroupSwitchModifier` 主要是 X11 语义，Windows 只有在特定命令行配置下才支持。不要把这类修饰键简单当作 `Ctrl`、`Alt` 等常规快捷键修饰键。

### 6.4 未知按键

默认构造参数是 `Qt::Key_unknown`。这表示组合的按键部分未知，不等于“没有按键”。如果业务需要表示只按修饰键的状态，应明确约定 `Key_unknown` 是否可接受。

## 7. 常见误区与边界

### 7.1 不要直接拼整数

不要手工猜测 `Qt::Key` 与 modifier 的位布局。使用构造函数、`operator|`、`toCombined()` 和 `fromCombined()`，这样代码跟随 Qt 的掩码定义。

### 7.2 `fromCombined()` 不会验证任意整数

```cpp
const QKeyCombination combination = QKeyCombination::fromCombined(rawValue);
```

该函数按位提取并封装 `rawValue`，调用方应保证 `rawValue` 是合法的组合编码。它不是输入校验器，也不会判断按键值是否属于当前平台有效键盘。

### 7.3 不要把 `Qt::Modifiers` 当作完整事件修饰键

`Qt::Modifiers` 只包含短名称对应的修饰键，不包含 `KeypadModifier` 等完整键盘状态。处理 `QKeyEvent::modifiers()` 时应优先使用 `Qt::KeyboardModifiers`。

### 7.4 `QKeyCombination` 不等于 `QKeySequence`

`QKeyCombination` 表示一个组合；`QKeySequence` 可以表示由一个或多个组合构成的序列，例如多步快捷键。需要多步快捷键、文本显示或动作绑定时使用 `QKeySequence`。

### 7.5 比较不等于 Java/业务层“快捷键相同”

两个编码相同的组合才相等。平台别名、显示文本、键盘布局和 `QKeySequence` 的标准化规则需要由更高层 API 处理。

### 7.6 已弃用 API

Qt 6.0 起以下接口不应用于新代码：

- 隐式 `operator int()`：改用 `toCombined()`；
- 各种 `operator+`：改用 `operator|`。

## 8. 与相关类型的协作

- `Qt::Key`：组合中的按键部分。
- `Qt::KeyboardModifier` / `Qt::KeyboardModifiers`：完整键盘事件修饰键及其标志集合。
- `Qt::Modifier` / `Qt::Modifiers`：快捷键书写用的短名称修饰键及其集合。
- `QKeySequence`：表示单个或多个按键组合形成的快捷键序列。
- `QKeyEvent`：提供实际按键事件中的 `key()` 和 `modifiers()`。
- `QHash`、`QSet`：借助 `qHash()` 保存组合键集合或映射。
- `QDataStream`、`QDebug`：提供序列化和调试输出。

## 9. 逐项 API 说明

### 构造

#### `[constexpr noexcept] QKeyCombination::QKeyCombination(Qt::Key key = Qt::Key_unknown)`

创建一个不带修饰键的组合。默认按键为 `Qt::Key_unknown`，表示按键部分未知。

#### `[explicit constexpr noexcept] QKeyCombination::QKeyCombination(Qt::KeyboardModifiers modifiers, Qt::Key key = Qt::Key_unknown)`

创建由完整键盘修饰键集合和一个按键组成的组合。修饰键会与按键值按位或保存。

#### `[explicit constexpr noexcept] QKeyCombination::QKeyCombination(Qt::Modifiers modifiers, Qt::Key key = Qt::Key_unknown)`

创建由快捷键短名称修饰键集合和一个按键组成的组合。`Qt::Modifiers` 会转换为对应的键盘 modifier 位。

### 编码转换与访问

#### `[static constexpr] QKeyCombination QKeyCombination::fromCombined(int combined)`

从组合编码构造对象。`combined` 应是 `Qt::Key` 与 `Qt::KeyboardModifiers` 按位或的结果，通常由 `toCombined()` 生成。函数不承担任意整数的合法性校验。

#### `[constexpr noexcept] Qt::Key QKeyCombination::key() const`

返回组合中的按键部分。实现通过去除 `Qt::KeyboardModifierMask` 得到按键值。

#### `[constexpr noexcept] Qt::KeyboardModifiers QKeyCombination::keyboardModifiers() const`

返回组合中的修饰键标志集合。结果是按 `Qt::KeyboardModifierMask` 提取的 `Qt::KeyboardModifiers`。

#### `[constexpr noexcept] int QKeyCombination::toCombined() const`

返回内部组合编码，即按键值与修饰键值的按位或结果。该值可传回 `fromCombined()`，也可作为兼容旧 API 或序列化格式的整数表示。

### 相关非成员

#### `[constexpr noexcept] size_t qHash(QKeyCombination key, size_t seed = 0)`

返回组合的哈希值，`seed` 用于哈希种子。相等的组合必须得到可用于哈希容器的等价哈希语义。

#### `[constexpr noexcept] bool operator==(const QKeyCombination &lhs, const QKeyCombination &rhs)`

当两个组合的按键和修饰键相同时返回 `true`。

#### `[constexpr noexcept] bool operator!=(const QKeyCombination &lhs, const QKeyCombination &rhs)`

当两个组合不相同时返回 `true`。

#### `QKeyCombination operator|(Qt::Key key, Qt::KeyboardModifier modifier)`

构造一个按键和单个完整键盘修饰键的组合。按键和修饰键顺序可交换。

#### `QKeyCombination operator|(Qt::Key key, Qt::KeyboardModifiers modifiers)`

构造一个按键和完整键盘修饰键集合的组合。集合中的各 modifier 会一起保存。

#### `QKeyCombination operator|(Qt::Key key, Qt::Modifier modifier)`

构造一个按键和单个快捷键短名称修饰键的组合。

#### `QKeyCombination operator|(Qt::Key key, Qt::Modifiers modifiers)`

构造一个按键和快捷键短名称修饰键集合的组合。

#### `QKeyCombination operator|(Qt::KeyboardModifier modifier, Qt::Key key)`

与按键在左侧的单 modifier 重载等价，支持修饰键在左的自然书写方式。

#### `QKeyCombination operator|(Qt::KeyboardModifiers modifiers, Qt::Key key)`

与按键在左侧的完整修饰键集合重载等价。

#### `QKeyCombination operator|(Qt::Modifier modifier, Qt::Key key)`

与按键在左侧的短名称单 modifier 重载等价。

#### `QKeyCombination operator|(Qt::Modifiers modifiers, Qt::Key key)`

与按键在左侧的短名称修饰键集合重载等价。

#### `[deprecated] QKeyCombination::operator int() const`

把组合隐式转换为整数。Qt 6.0 起弃用，新代码使用 `toCombined()`，避免组合值在普通整数运算中失去类型信息。

#### `[deprecated] operator+` 的 8 个重载

`operator+` 支持与 `operator|` 相同的按键/修饰键参数排列，但 Qt 6.0 起已弃用。新代码统一使用 `operator|`，以明确表达位组合语义。

#### `QDataStream &operator<<(QDataStream &out, QKeyCombination combination)`

把组合写入数据流并返回 `out`。流版本、字节序和读写双方的 Qt 数据流约定必须一致。

#### `QDataStream &operator>>(QDataStream &in, QKeyCombination &combination)`

从数据流读取组合并写入 `combination`，返回 `in`。读取失败时应检查数据流状态。

#### `QDebug operator<<(QDebug debug, QKeyCombination combination)`

把组合写入调试输出对象，用于日志和调试，不应把调试格式当作持久化协议。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QKeyCombination(key = Qt::Key_unknown)` | 创建不带修饰键的组合。 | 默认是未知按键，不是无按键状态。 |
| 构造 | `QKeyCombination(Qt::KeyboardModifiers, key)` | 用完整键盘修饰键集合创建组合。 | 适合 `QKeyEvent::modifiers()`。 |
| 构造 | `QKeyCombination(Qt::Modifiers, key)` | 用快捷键短名称集合创建组合。 | 不包含 `KeypadModifier`。 |
| 转换 | `fromCombined(combined)` | 从整数编码恢复组合。 | 输入应来自合法位组合；不做校验。 |
| 访问 | `key()` | 读取 `Qt::Key` 部分。 | 去除 modifier 掩码后的值。 |
| 访问 | `keyboardModifiers()` | 读取完整修饰键集合。 | 返回 `Qt::KeyboardModifiers`。 |
| 转换 | `toCombined()` | 输出整数编码。 | 可无损传给 `fromCombined()`。 |
| 哈希 | `qHash(key, seed)` | 计算哈希值。 | 可用于 `QHash`、`QSet`。 |
| 比较 | `operator==` | 比较按键和修饰键是否都相同。 | 不比较显示文本或平台别名。 |
| 比较 | `operator!=` | 判断组合是否不同。 | 与 `operator==` 相反。 |
| 组合 | `operator|(key, modifier)` | 按键加单个完整 modifier。 | 顺序可交换。 |
| 组合 | `operator|(key, modifiers)` | 按键加完整 modifier 集合。 | 适合事件状态。 |
| 组合 | `operator|(key, Qt::Modifier)` | 按键加单个快捷键短名称 modifier。 | 适合 `Qt::CTRL` 等写法。 |
| 组合 | `operator|(key, Qt::Modifiers)` | 按键加快捷键短名称集合。 | 不含数字键盘 modifier。 |
| 组合 | `operator|(modifier, key)` 四组 | 支持 modifier 在左侧的四种对称写法。 | 结果与 key 在左侧相同。 |
| 序列化 | `operator<<(QDataStream &, combination)` | 写入数据流。 | 检查流版本和状态。 |
| 调试 | `operator<<(QDebug, combination)` | 输出调试信息。 | 调试格式不是持久化协议。 |
| 反序列化 | `operator>>(QDataStream &, combination &)` | 从数据流读回组合。 | 读取后检查流状态。 |
| 弃用 | `operator int()` | 隐式转为编码整数。 | Qt 6.0 起弃用，改用 `toCombined()`。 |
| 弃用 | `operator+` 八个重载 | 旧式创建组合。 | Qt 6.0 起弃用，改用 `operator|`。 |

## 11. 使用判断

- 只保存一个按键和修饰键组合：使用 `QKeyCombination`。
- 需要表示多步快捷键序列或显示文本：使用 `QKeySequence`。
- 从键盘事件构造组合：优先传 `QKeyEvent::modifiers()` 和 `QKeyEvent::key()`。
- 新代码组合按键时使用 `operator|`，编码转换使用 `toCombined()`/`fromCombined()`。
- 需要跨平台快捷键语义时，注意 macOS 的 Ctrl/Meta 映射，不要自行硬编码平台位值。
