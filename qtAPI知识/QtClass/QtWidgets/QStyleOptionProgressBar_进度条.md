# Qt QStyleOptionProgressBar 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 和安装头文件整理）  
> 头文件：`#include <QStyleOptionProgressBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionProgressBar`  
> 定位：把进度条的绘制状态传递给 `QStyle` 的轻量数据对象

## 1. 它不是进度条控件

`QStyleOptionProgressBar` 名字里有 ProgressBar，但它既不会显示在界面上，也没有 `setValue()`、信号或父对象。它只是一次绘制所需状态的快照，交给样式系统决定“进度条应该画成什么样”。

```text
QProgressBar
  └─ initStyleOption(&option)
       └─ QStyleOptionProgressBar
            └─ QStyle::drawControl(CE_ProgressBar, ...)
                 └─ QPainter 画到控件上
```

它主要出现在两种代码里：

- 自定义 `QProgressBar` 子类的 `paintEvent()`，但仍希望复用当前平台样式；
- 自定义 `QStyle` 或 `QProxyStyle`，需要读取进度条状态并决定怎样绘制。

普通业务代码只需使用 `QProgressBar`。只有你正在改变控件外观、实现主题或调试样式时，才直接接触本类。

## 2. 为什么它的成员全是公开变量

`QStyleOption` 家族刻意做成接近 C++ 结构体的形式：没有大量 setter/getter，而是直接读写字段。

```cpp
QStyleOptionProgressBar option;
option.minimum = 0;
option.maximum = 100;
option.progress = 42;
option.text = "42%";
option.textVisible = true;
```

这样做不是鼓励在业务层随意修改控件状态，而是为了降低每次绘制创建和读取样式参数的成本。这个对象没有所有权关系、没有事件循环依赖，也没有 QObject 生命周期；它通常在栈上创建，绘制调用结束便销毁。

要分清两个方向：

```text
QProgressBar 的属性  ->  initStyleOption()  ->  option 的字段
option 的字段         ->  QStyle 绘制决策
```

第二行不是反向绑定。改掉 `option.progress` 只影响这一次传给 `QStyle` 的绘制数据，不会修改真实 `QProgressBar::value()`。

## 3. 标准用法：复用平台样式，只改变绘制时机

如果你写了 `QProgressBar` 子类，最稳妥的起点是让基类把所有状态填入 option，再把它交还给样式：

```cpp
void MeterBar::paintEvent(QPaintEvent *)
{
    QStyleOptionProgressBar option;
    initStyleOption(&option);

    QPainter painter(this);
    style()->drawControl(QStyle::CE_ProgressBar, &option, &painter, this);
}
```

`initStyleOption()` 是 `QProgressBar` 的受保护函数，会同步范围、当前值、方向、文本可见性、调色板、启用状态和 `rect` 等信息。手动只填 `minimum`、`maximum`、`progress` 往往会漏掉继承自 `QStyleOption` 的 `state`、`palette`、`direction`、`fontMetrics` 等字段，结果是禁用态、深色主题、RTL 布局或高 DPI 下的样式不正确。

若只想在基础绘制上叠加内容，应先让样式画进度条，再画自己的装饰，而不是手工复刻所有平台样式细节。

## 4. 自定义样式时：安全识别 option 类型

`QStyle::drawControl()` 接收的是基类指针 `const QStyleOption *`。在自定义 style 中，应当先判断元素，再用 `qstyleoption_cast()` 安全转换：

```cpp
void AccentStyle::drawControl(QStyle::ControlElement element,
                              const QStyleOption *option,
                              QPainter *painter,
                              const QWidget *widget) const
{
    if (element == QStyle::CE_ProgressBar) {
        const auto *bar =
            qstyleoption_cast<const QStyleOptionProgressBar *>(option);

        if (bar && bar->maximum > bar->minimum) {
            drawAccentChunk(*bar, painter);
            return;
        }
    }

    QProxyStyle::drawControl(element, option, painter, widget);
}
```

不要把 `const QStyleOption *` 直接 `static_cast` 为 `QStyleOptionProgressBar *`。样式函数处理很多控件和子控件，元素与 option 类型不匹配时，错误转换会造成未定义行为。`qstyleoption_cast()` 会依据 `Type` 和版本信息完成检查。

## 5. 进度相关字段的语义

### 5.1 `minimum`、`maximum`、`progress`

这三个字段是对 `QProgressBar` 范围和值的绘制快照：

```cpp
const int span = option.maximum - option.minimum;
const double ratio = span > 0
    ? double(option.progress - option.minimum) / span
    : 0.0;
```

上面的比例只是常见思路；真正的样式还需要处理倒置方向、忙碌状态、像素取整和布局方向。

一个容易漏掉的约定是：`progress == minimum - 1` 表示“尚未开始”。此时通常应把 `text` 视为未开始状态，而不是显示 `0%`。默认构造后 `minimum` 和 `progress` 都是 `0`，因此需要由控件的 `initStyleOption()` 或你的代码填入一份自洽的状态。

### 5.2 文本与方向不是同一件事

| 字段 | 决定什么 | 不决定什么 |
| --- | --- | --- |
| `text` | 样式可用的显示文字，例如 `42%` | 是否一定会画出文字 |
| `textVisible` | 是否允许显示文字 | 具体文字内容与位置 |
| `textAlignment` | 文字的位置建议，默认 `Qt::AlignLeft` | 进度块的填充方向 |
| `bottomToTop` | 竖直进度条中文字是否由下向上阅读 | 进度块的填充方向 |
| `invertedAppearance` | 进度块外观是否反转 | 竖直文字的阅读方向 |

不同平台样式对文字的支持并不完全相同，特别是竖直进度条；`textVisible == true` 表示把文字作为输入交给样式，并不等于每个 style 都会以相同方式呈现它。

## 6. `Type` 与 `Version`：给样式系统的运行时标签

每个 `QStyleOption` 子类都有 `Type` 与 `Version`：

- `Type = SO_ProgressBar`：告诉 `qstyleoption_cast()` 这是一份进度条样式数据。
- `Version`：让未来版本可以扩展结构，而旧代码仍能拒绝无法理解的布局。

普通控件子类和普通 style 实现不应手工比较这些常量，使用 `qstyleoption_cast()` 即可。

### 6.1 Qt 6.11.1 文档与头文件的一个不一致

Qt 6.11.1 离线类页的详细说明文字写着 “version 2”，但该安装目录中的 `QtWidgets/qstyleoption.h` 将 `QStyleOptionProgressBar::Version` 定义为 `1`，类页的枚举表也列出常量值 `1`。代码应以当前编译所用头文件为准；不要把说明段中的 `2` 写死到自定义代码。

## 7. 常见错误与排查

### 7.1 直接构造 option 后，画面缺少平台状态

症状：禁用状态不对、RTL 布局错位、文字颜色不符合主题。

原因：只填了进度数字，忽略了从 `QStyleOption` 继承的绘制上下文。

处理：从一个真实 `QProgressBar` 绘制时，优先调用 `initStyleOption(&option)`。

### 7.2 误把 `bottomToTop` 当成填充方向

症状：竖直条的文字方向改了，但进度块仍从原来的方向增长。

原因：`bottomToTop` 只描述文字的阅读方向。

处理：填充方向应读取或设置 `invertedAppearance`，并结合 layout direction 交给当前 style 处理。

### 7.3 用 option “回写”控件状态

症状：修改 `option.progress` 后，下一帧又变回旧进度。

原因：option 是一次绘制快照，并非控件模型。

处理：要改变真实进度，调用 `QProgressBar::setValue()`；要只改变本次外观，在 option 上改字段后立刻调用绘制函数。

## API 速查表
以下列出 `QStyleOptionProgressBar` 在 Qt 6.11.1 类文档中直接声明的类型、构造函数和公开数据成员。继承自 `QStyleOption` 的 `rect`、`state`、`palette` 等通用绘制字段不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_ProgressBar` | 标记本 option 的运行时类型是进度条。 | 主要供 `qstyleoption_cast()` 和样式系统识别；普通代码无需手工判断。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标记该结构的版本。 | 以正在编译的 Qt 头文件为准；Qt 6.11.1 离线页的说明段有“version 2”的不一致文字。 |
| 构造 | `QStyleOptionProgressBar()` | 创建并以默认值初始化一份进度条绘制状态。 | 通常紧接着调用 `QProgressBar::initStyleOption()` 填充真实状态。 |
| 构造 | `QStyleOptionProgressBar(const QStyleOptionProgressBar &other)` | 复制另一份 option。 | 是值复制，没有 QObject 父子关系，也不会复制控件本身。 |
| 公开字段 | `bool bottomToTop` | 指定竖直进度条的文字是否自下而上阅读。 | 默认 `false`；不控制进度块填充方向。 |
| 公开字段 | `bool invertedAppearance` | 指定进度条外观是否反转。 | 默认 `false`；样式还可能结合布局方向决定实际呈现。 |
| 公开字段 | `int maximum` | 进度范围的上界。 | 默认 `0`；应与 `minimum`、`progress` 保持逻辑一致。 |
| 公开字段 | `int minimum` | 进度范围的下界。 | 默认 `0`；不要假定范围一定从零开始。 |
| 公开字段 | `int progress` | 当前绘制进度。 | `minimum - 1` 表示尚未开始；它只是样式快照，不会修改控件值。 |
| 公开字段 | `QString text` | 样式可显示的进度文字。 | 空字符串通常代表尚未开始；实际是否绘制还看 `textVisible` 与 style。 |
| 公开字段 | `Qt::Alignment textAlignment` | 提供文字对齐位置建议。 | 默认 `Qt::AlignLeft`；样式可以选择忽略或调整它。 |
| 公开字段 | `bool textVisible` | 指定是否应显示 `text`。 | 默认 `false`；不同平台 style 的显示效果可能不同。 |

## 9. 一句话总结

`QStyleOptionProgressBar` 是进度条的“绘制说明书”，不是进度条本身；用 `initStyleOption()` 取得可靠快照，用 `QStyle` 或 `QProxyStyle` 解释这份快照，才能既自定义外观又保住 Qt 的平台样式行为。
