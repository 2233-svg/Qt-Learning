# QPalette：用语义化颜色角色维持界面主题一致性

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPalette>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`

`QPalette` 保存控件绘制所需的颜色和画刷，但它不以“红、蓝、灰”这样的具体颜色组织，而是以 `Window`、`Text`、`Base`、`Highlight` 等**颜色角色**组织，并为活动、非活动和禁用状态分别保存一组值。这样自定义控件能随当前平台主题、深浅模式和应用配色变化，而不是把视觉假设写死在代码里。

它是隐式共享的值类型：复制便宜，修改副本时才分离数据。`QPalette` 可以安全地按值保存和传递；但它不是动态主题订阅对象，系统或应用调色板发生变化后，之前保存的副本不会自动神奇地更新。

## 它解决的问题

自绘控件经常需要按钮背景、输入区域背景、普通文字、选中行和禁用文字。若每个控件各自硬编码 `#ffffff`、`#222222`，深色主题、辅助功能主题和平台风格一变，视觉就会断裂。

```cpp
void StatusBadge::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    const QPalette &pal = palette();

    painter.fillRect(rect(), pal.brush(QPalette::Window));
    painter.setPen(pal.color(QPalette::WindowText));
    painter.drawText(rect(), Qt::AlignCenter, text());
}
```

这里控件没有猜测“窗口背景一定是白色”，而是取当前控件继承并解析后的 `Window` 与 `WindowText`。对普通 Widgets 自绘，这通常是最稳妥的起点。

## 两个维度：颜色组与颜色角色

`QPalette` 的值由 `(ColorGroup, ColorRole)` 这一对键决定。

### 颜色组：同一角色在什么状态下使用

| 颜色组 | 使用时机 |
| --- | --- |
| `Active` | 有键盘焦点的窗口。 |
| `Inactive` | 其他未激活窗口；多数样式下外观可能与 `Active` 相同。 |
| `Disabled` | 已禁用的控件，不是“失去焦点的窗口”。活动或非活动窗口都可包含禁用控件。 |
| `Normal` | `Active` 的别名。 |
| `Current` | 访问时采用 `currentColorGroup()`；主要是 API 内部/兼容性便利值。 |
| `All` | 设置时表示所有颜色组；不应当作实际绘制状态。 |

`palette.color(QPalette::Text)` 和 `palette.brush(QPalette::Base)` 都读取当前颜色组。自绘控件通常直接从 `QWidget::palette()` 获取已经为该控件解析好的调色板，而不是自行切换 `currentColorGroup()`。

### 颜色角色：这个颜色在界面中扮演什么角色

常用角色的含义如下：

| 角色 | 正确的使用位置 |
| --- | --- |
| `Window` / `WindowText` | 普通窗口或面板背景，以及其前景文字。 |
| `Base` / `Text` | 文本输入、项目视图等内容区域背景及其文字。`Base` 不等于通用窗口背景。 |
| `AlternateBase` | 交替行视图的另一种背景。 |
| `Button` / `ButtonText` | 按钮类控件的背景与文字。 |
| `Highlight` / `HighlightedText` | 当前选中项背景与其文字，必须成对考虑对比度。 |
| `ToolTipBase` / `ToolTipText` | 工具提示和 What's This 的背景与文字；工具提示通常使用 `Inactive` 组。 |
| `PlaceholderText` | 输入框占位文字；Qt 6 中是独立角色，不能再简单假定为半透明 `Text`。 |
| `Accent` | 与 `Base`、`Window`、`Button` 对比或互补的强调色，常用于交互元素；Qt 6.6 起提供，未显式设置时通常回退为 `Highlight`。 |
| `Link` / `LinkVisited` | 未访问与已访问链接文字。 |
| `Light`、`Midlight`、`Mid`、`Dark`、`Shadow` | 用于立体边缘、阴影和层次；让当前样式决定具体关系。 |
| `BrightText` | 需要在较深背景上突出显示的文字。 |
| `NoRole` | 表示未指定角色，不应用来取正常绘制颜色。 |

优先选语义正确的角色，而不是“看起来现在比较像”的角色。例如输入框背景应是 `Base`，不是 `Window`；选中条上的文字应是 `HighlightedText`，不要固定为白色。

## 从当前主题派生，而不是从空调色板重建

默认构造的 `QPalette` 是一个没有显式设置颜色角色的空调色板。当它作为 `QWidget` 的 palette 使用时，控件系统会按继承规则解析未设置项；它不是一套完整的“默认主题”。

需要微调控件时，先从已有调色板复制，再覆盖少数角色：

```cpp
QPalette pal = button.palette();
pal.setColor(QPalette::Active, QPalette::Accent, QColor("#00695c"));
pal.setColor(QPalette::Inactive, QPalette::Accent, QColor("#00695c"));
button.setPalette(pal);
```

更常见的是对角色在所有颜色组使用同一种覆盖：

```cpp
QPalette pal = widget.palette();
pal.setColor(QPalette::PlaceholderText, QColor(80, 80, 80));
widget.setPalette(pal);
```

不带 `ColorGroup` 的 `setColor(role, color)` 与 `setBrush(role, brush)` 会设置**所有**颜色组。要保留禁用态与活动态的不同效果，使用带颜色组的重载逐组设置。

应用级主题应从 `QGuiApplication::palette()` 或 Widgets 程序中当前 `QApplication` 的调色板派生，再使用相应的 `setPalette()` API。不要只靠 `QPalette(QColor)` 构造器做完整主题：它会基于给定按钮色推导一批颜色，却无法表达平台样式的全部设计意图。

## 颜色与画刷：何时用 `color()`，何时用 `brush()`

每个角色保存的是 `QBrush`，因此不仅可以是纯色，还可以是渐变、纹理或图案。`color()` 返回该画刷的 `QColor`；自绘时若要保留纹理或渐变，应使用 `brush()`。

```cpp
QPainter painter(this);
const QPalette &pal = palette();

painter.fillRect(rect(), pal.brush(QPalette::Window));
painter.setPen(pal.color(QPalette::WindowText));
```

`const QBrush &` 和 `const QColor &` 返回的是调色板内部引用。不要在调色板可能被修改、销毁或重新赋值后继续保存这些引用；需要跨作用域保存就按值拷贝。

## 局部覆盖如何与父级/样式合并

`resolve(other)` 返回一张新调色板：调用者自身**已经显式设置**的角色优先，未设置的角色从 `other` 补齐。这个行为依赖 resolve mask，而不只是“颜色是否刚好相等”。

```cpp
QPalette overridePalette;
overridePalette.setColor(QPalette::Highlight, QColor("#1565c0"));

const QPalette effective =
    overridePalette.resolve(QGuiApplication::palette());
```

在此例中 `Highlight` 来自 `overridePalette`，其他未设置的角色来自应用调色板。`resolveMask()` 和 `setResolveMask()` 是处理这种显式覆盖集合的低层接口；业务代码一般通过 `setColor()` / `setBrush()` 让 Qt 维护掩码，手工篡改掩码很容易让继承结果难以推断。

`isBrushSet(group, role)` 检查的是某角色是否**在这张 palette 上显式设置过**，不是它最终解析后是否有可用颜色。它适合调试和实现合并逻辑，不是绘制前的“颜色存在性”测试。

## 平台样式和样式表的边界

`QPalette` 是 Qt Widgets 的主题契约，但并不保证所有平台原生样式都使用其中每一项。使用原生主题引擎的样式，特别是 Windows Vista 风格与 macOS 风格，可能对部分控件或部分角色采用系统绘制。

Qt Style Sheets 又是一套更具体的控件外观规则。为同一控件同时设置 palette 和 `background-color`、`color` 等 QSS 属性时，最终呈现取决于样式表与当前 style 的绘制路径，不能把 palette 当成强制覆盖。若设计要求逐像素一致，使用一致的样式策略并在目标平台验证；若目标是遵从系统主题，自绘时读取 palette 通常更好。

## 比较、缓存与序列化

`operator==` 比较调色板值是否相等；`isCopyOf()` 更严格，只在二者共享同一未修改数据副本时为真。两个独立构造但颜色相同的调色板可以相等，却不是彼此的 copy。

`cacheKey()` 标识当前内容，修改调色板后会改变。它可用于进程内缓存失效判断，不能当作跨进程、跨版本或持久化的稳定 ID。

`QDataStream` 读写可用于 Qt 侧的二进制传输；读取外部数据时检查流状态，并且不要把它当成长期公开文件格式协议。

## API 速查表

### 构造、值语义与合并

| API | 语义与使用边界 |
| --- | --- |
| `QPalette()` | 创建未显式设置角色的空调色板；作为控件 palette 时由控件继承规则解析。 |
| `QPalette(QColor/Qt::GlobalColor button)` | 由按钮色推导颜色，`Window` 也使用该按钮色；适合简单场景，不是完整平台主题。 |
| `QPalette(button, window)` | 由按钮色和窗口色推导其他颜色。 |
| 九个 `QBrush` 或七个 `QColor` 的构造器 | 直接初始化一组传统核心角色；新增角色仍应按需要单独设置。 |
| 拷贝/移动构造、赋值、`swap()` | 值语义且隐式共享；写入副本时分离。 |
| `operator QVariant()` | 转换为 `QVariant`，可用于属性和通用数据接口。 |
| `resolve(const QPalette &other)` | 返回合并结果：本对象显式设置的角色优先，未设置角色取自 `other`。 |
| `resolveMask()` / `setResolveMask()` | 读取或直接设定显式角色掩码；低层接口，通常由 `setColor()` / `setBrush()` 维护。 |
| `cacheKey()` | 返回当前内容标识，修改后变化；仅适合临时缓存键。 |
| `operator==` / `operator!=` | 比较调色板值。 |
| `isCopyOf(const QPalette &)` | 判断是否共享同一且未修改的数据副本，比值相等严格。 |
| `QDataStream <<` / `>>` | 写入/读取 Qt 二进制流；外部输入必须检查流错误。 |
| `QDebug <<` | 输出调试表示；仅在启用调试流时可用。 |

### 颜色组与角色访问

| API | 语义与使用边界 |
| --- | --- |
| `currentColorGroup()` | 返回“无组参数”读取所使用的当前颜色组。 |
| `setCurrentColorGroup(ColorGroup)` | 设置无组参数读取的颜色组；普通控件绘制通常无需手动切换。 |
| `color(group, role)` | 返回指定状态和角色的纯色引用。 |
| `color(role)` | 返回当前颜色组中角色的纯色引用。 |
| `brush(group, role)` | 返回指定状态和角色的完整画刷，能保留纹理或渐变。 |
| `brush(role)` | 返回当前颜色组中的完整画刷。 |
| `isBrushSet(group, role)` | 判断该条目是否由此调色板显式设置；不是最终解析有效性的判断。 |
| `isEqual(group1, group2)` | 比较本 palette 内两个颜色组是否相同。 |

### 写入颜色与画刷

| API | 语义与使用边界 |
| --- | --- |
| `setColor(group, role, color)` | 设置一个颜色组中的纯色角色。 |
| `setColor(role, color)` | 为所有颜色组设置该角色；会抹平 Active、Inactive、Disabled 的差异。 |
| `setBrush(group, role, brush)` | 设置一个颜色组中的完整画刷。 |
| `setBrush(role, brush)` | 为所有颜色组设置该画刷。 |
| `setColorGroup(group, windowText, button, light, dark, mid, text, brightText, base, window)` | 一次设定传统核心角色；其他角色仍需按需求单独设置。 |

### 角色便利访问器

| API | 对应角色 |
| --- | --- |
| `windowText()` / `window()` | `WindowText` / `Window`。 |
| `base()` / `alternateBase()` | `Base` / `AlternateBase`。 |
| `text()` / `placeholderText()` | `Text` / `PlaceholderText`。 |
| `button()` / `buttonText()` | `Button` / `ButtonText`。 |
| `light()` / `midlight()` / `mid()` / `dark()` / `shadow()` | 层次与边缘的五个角色。 |
| `brightText()` | `BrightText`。 |
| `highlight()` / `highlightedText()` | `Highlight` / `HighlightedText`。 |
| `link()` / `linkVisited()` | `Link` / `LinkVisited`。 |
| `toolTipBase()` / `toolTipText()` | `ToolTipBase` / `ToolTipText`。 |
| `accent()` | `Accent`；Qt 6.6 起提供。 |

### `ColorGroup`

| 枚举值 | 含义 |
| --- | --- |
| `Active` | 有键盘焦点窗口的颜色组。 |
| `Disabled` | 禁用控件的颜色组。 |
| `Inactive` | 未激活窗口的颜色组。 |
| `Normal` | `Active` 的别名。 |
| `Current` | 当前颜色组的占位值。 |
| `All` | 全部颜色组的设置占位值。 |
| `NColorGroups` | 颜色组数量边界，不是可绘制状态。 |

### `ColorRole`

| 枚举值 | 含义 |
| --- | --- |
| `WindowText`、`Window` | 通用窗口前景、背景。 |
| `Button`、`ButtonText` | 按钮背景、前景。 |
| `Light`、`Midlight`、`Mid`、`Dark`、`Shadow` | 立体层次和阴影。 |
| `Text`、`Base` | 内容/输入区域前景、背景。 |
| `BrightText` | 强对比文字。 |
| `Highlight`、`HighlightedText` | 选择高亮背景、前景。 |
| `Link`、`LinkVisited` | 未访问、已访问链接。 |
| `AlternateBase` | 交替行背景。 |
| `ToolTipBase`、`ToolTipText` | 工具提示背景、前景。 |
| `PlaceholderText` | 占位文字。 |
| `Accent` | 主题强调色，Qt 6.6 起。 |
| `NoRole` | 未指定角色。 |
| `NColorRoles` | 角色数量边界，不是实际颜色角色。 |
