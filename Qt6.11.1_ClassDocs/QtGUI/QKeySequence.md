# QKeySequence

> Qt 6.11.1 · Qt GUI · 来自 `QKeySequence`

## 1. 先建立直觉

`QKeySequence` 是“一个或多个按键组合构成的命令序列”。`Ctrl+S` 是一个组合键序列，`Ctrl+K, Ctrl+C` 则是两段式序列。Qt 最多支持四个组合键组成一个 sequence。

它不负责监听键盘；监听由 `QAction`、`QShortcut`、菜单或控件事件处理完成。`QKeySequence` 只负责可靠表达、解析、比较、显示和匹配这些快捷键规则。

## 2. 类说明

`QKeySequence` 是值类型。它可以来自 `StandardKey`、`QKeyCombination`、文本表示或旧式 `Qt::Key | Qt::KeyboardModifier` 整数值。

类说明只用于表明这些 API 来自 `QKeySequence`：命令触发状态由 `QAction` / `QShortcut` 管理，单个按键事件由 `QKeyEvent` 表达，菜单助记符从文本中提取可使用 `mnemonic()`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QKeySequence()` | 构造空序列。 |
| `QKeySequence(StandardKey)` | 构造平台标准命令快捷键，如 Copy、Save、Quit。 |
| `QKeySequence(QKeyCombination...)` | 用最多四段组合键构造序列。 |
| `QKeySequence(int k1, ...)` | 用旧式整型组合键构造，现代代码优先 `QKeyCombination`。 |
| `QKeySequence(text, format)` | 从本地化或可移植文本解析快捷键。 |
| `count()` | 返回序列包含的组合键数量，最多 4。 |
| `isEmpty()` | 判断是否为空序列。 |
| `operator[](index)` | 读取某一段 `QKeyCombination`。 |
| `matches(other)` | 判断两个序列是精确匹配、前缀匹配还是不匹配。 |
| `toString(format)` | 格式化为 NativeText 或 PortableText。 |
| `fromString(text, format)` | 从文本解析一个序列。 |
| `keyBindings(StandardKey)` | 返回当前平台某个标准命令的全部推荐绑定。 |
| `listFromString()` / `listToString()` | 解析或序列化多个快捷键列表。 |
| `mnemonic(text)` | 从包含 `&` 助记符的文本提取 Alt 组合键。 |
| `qHash(sequence)` | 用作 `QHash` / `QSet` 键。 |
| `StandardKey` | 预定义 Copy、Paste、Undo、Save、Open、Quit、Find 等跨平台命令。 |
| `SequenceFormat` | 选择 NativeText（给用户看）或 PortableText（存储/配置）。 |
| `SequenceMatch` | `NoMatch`、`PartialMatch`、`ExactMatch`。 |

## 4. 关键用法

### 标准命令使用 `StandardKey`

```cpp
auto *copyAction = new QAction(tr("Copy"), this);
copyAction->setShortcuts(QKeySequence::keyBindings(QKeySequence::Copy));
```

不要把复制硬编码为 `Ctrl+C`。不同平台的主修饰键习惯不同，`StandardKey` 和 `keyBindings()` 让菜单显示、实际触发和用户预期更一致。

构造单一默认绑定时也可以：

```cpp
copyAction->setShortcut(QKeySequence(QKeySequence::Copy));
```

### 配置文件使用 PortableText

```cpp
settings.setValue("shortcut/open",
                  QKeySequence(Qt::CTRL | Qt::Key_O)
                      .toString(QKeySequence::PortableText));

const QKeySequence shortcut = QKeySequence::fromString(
    settings.value("shortcut/open").toString(),
    QKeySequence::PortableText);
```

`NativeText` 用于面向用户显示，可能随平台、本地化和符号习惯变化；跨机器配置与持久化应使用 `PortableText`。

### 多段快捷键使用匹配状态

```cpp
const QKeySequence prefix(Qt::CTRL | Qt::Key_K);
const QKeySequence command(Qt::CTRL | Qt::Key_K,
                           Qt::CTRL | Qt::Key_C);

if (command.matches(prefix) == QKeySequence::PartialMatch)
    showChordHint();
```

编辑器类应用可用 PartialMatch 实现 chord 快捷键等待状态。注意超时、取消键和与单段快捷键冲突的优先级需要由上层输入路由定义。

### 从菜单文本提取助记符

```cpp
const QKeySequence key = QKeySequence::mnemonic(tr("E&xit"));
// 通常得到 Alt+X
```

助记符用于菜单键盘导航，不等同于全局快捷键。翻译时 `&` 的位置需要检查冲突和语言可读性。

## 5. 使用场景

`QKeySequence` 适合菜单动作、工具栏、命令面板、编辑器 chord、用户可配置快捷键、命令冲突检测、设置序列化和菜单助记符。

它特别适合把“命令含义”与“具体键位”分离：内部把动作声明为 Save / Copy / Find，平台和用户偏好决定实际按键。

## 6. 常见坑与经验

不要用 NativeText 保存设置。它用于显示，跨平台/语言解析不如 PortableText 稳定。

不要把 `QKeySequence` 当作按键事件过滤器。多段匹配、焦点上下文、动作优先级和实际触发仍由 `QShortcut` / `QAction` 或自定义事件逻辑处理。

不要假设一个 `StandardKey` 只有一个绑定。`keyBindings()` 可能返回多种等价组合。

不要把 `matches()` 的方向弄反。它表达当前序列与目标序列的关系；多段 chord 逻辑应针对具体调用方向写测试。

不要用 `operator<` 的排序结果表示用户可读优先级。它只提供容器排序所需的稳定关系，不是快捷键重要性。

不要把 `&` 助记符和 `&&` 字面字符混淆。翻译与菜单文本中需要正确转义。

## 7. 知识点覆盖

学习 `QKeySequence` 应覆盖标准命令、跨平台快捷键、单段与多段 chord、NativeText、PortableText、持久化、部分匹配、助记符、QAction/QShortcut 协作、用户自定义绑定和冲突处理。
