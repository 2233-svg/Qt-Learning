# Qt QStyleOptionFocusRect 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionFocusRect>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionFocusRect`

## 1. 它解决什么问题

键盘焦点必须有清晰的视觉提示：用户按 `Tab` 在按钮、输入框、列表项之间移动时，需要知道“接下来按空格或回车会操作谁”。不同平台和主题对此的画法不同，有的使用虚线矩形，有的使用高亮外框或发光边缘。

`QStyleOptionFocusRect` 是把“此处应绘制焦点框”的上下文交给 `QStyle` 的数据包。它本身不管理焦点，也不会显示任何东西；真正绘制的是 style 的 `drawPrimitive()`，使用的 primitive 是 `QStyle::PE_FrameFocusRect`。

```text
QWidget::paintEvent()
  -> QStyleOptionFocusRect option
  -> 填入矩形、状态、调色板、背景色等数据
  -> style()->drawPrimitive(QStyle::PE_FrameFocusRect, &option, painter, this)
  -> 当前平台/主题决定焦点框的最终外观
```

这个分工解决了两个问题：

- 自定义控件不必猜测系统应使用什么颜色、线型和高对比度规则。
- 更换 `QStyle`、切换主题或平台后，焦点提示仍可保持统一。

## 2. 什么时候使用它

它主要出现在两类代码中：

1. **自定义 `QWidget` 的 `paintEvent()`**：控件有键盘焦点时，委托当前 style 绘制焦点提示。
2. **自定义 `QStyle` 或 `QProxyStyle`**：在处理 `PE_FrameFocusRect` 时读取 option 中的状态与 `backgroundColor`，决定怎样画。

普通业务代码通常不需要手工创建它。`QPushButton`、`QLineEdit`、`QAbstractItemView` 等标准控件已完成焦点处理；只有你自己承担绘制工作时才需要接上这一层。

与其相关但职责不同的类型：

| 类型 | 职责 | 适合的场景 |
| --- | --- | --- |
| `QWidget` | 接收键盘焦点、在 `hasFocus()` 中报告状态 | 所有可交互控件 |
| `QStyleOptionFocusRect` | 描述“一次焦点框绘制”所需参数 | 自绘控件与 style |
| `QStyle` | 按当前主题绘制 primitive/control/complex control | 保持平台外观一致 |
| `QFocusFrame` | 独立的辅助控件，可在目标控件外侧显示焦点框 | 焦点框需要延伸到目标控件几何区域外 |

`QFocusFrame::setWidget(target)` 会跟踪目标控件的位置和尺寸；这是“在控件外面套一个焦点框”的现成方案。它不是 `QStyleOptionFocusRect` 的替代品，而是使用 style 焦点绘制能力的更高层封装。

## 3. 构建与最小绘制流程

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 在自定义控件中绘制焦点框

下面的控件绘制自己的边框和文本，并且在获得键盘焦点时请 style 画焦点提示。

```cpp
#include <QPainter>
#include <QStyle>
#include <QStyleOptionFocusRect>
#include <QWidget>

class FocusPreview final : public QWidget
{
public:
    FocusPreview()
    {
        setFocusPolicy(Qt::StrongFocus);
        setMinimumSize(180, 72);
    }

protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter painter(this);

        painter.fillRect(rect(), palette().base());
        painter.setPen(palette().color(QPalette::Mid));
        painter.drawRect(rect().adjusted(0, 0, -1, -1));
        painter.setPen(palette().color(QPalette::Text));
        painter.drawText(rect(), Qt::AlignCenter, "按 Tab 获得焦点");

        if (!hasFocus())
            return;

        QStyleOptionFocusRect option;
        option.initFrom(this);
        option.rect = rect().adjusted(3, 3, -3, -3);
        option.backgroundColor = palette().color(QPalette::Base);
        style()->drawPrimitive(QStyle::PE_FrameFocusRect, &option, &painter, this);
    }
};
```

关键不在于手写一个虚线矩形，而在于把正确的上下文交给当前 style。`initFrom(this)` 会从控件取得通用状态、调色板、布局方向、字体度量和可绘制矩形等基类字段；之后再覆盖本次绘制真正需要的 `rect` 与 `backgroundColor`。

## 4. 焦点状态：两个容易混淆的标志

焦点框是否以及画在哪里，通常由 `QStyleOption::state` 里的状态位表达。

| 状态位 | 表示什么 | 常见用法 |
| --- | --- | --- |
| `QStyle::State_HasFocus` | 控件当前拥有键盘焦点 | 作为是否绘制焦点提示的依据 |
| `QStyle::State_FocusAtBorder` | 焦点提示应在控件边框处，而不是内部内容区域 | 让 style 决定焦点框的内外位置 |

二者不是同一个概念。`State_HasFocus` 回答“有没有焦点”，`State_FocusAtBorder` 回答“如果画焦点提示，位置更接近边框还是内容内部”。不要用第二个标志替代 `hasFocus()` 判断，也不要为了“显示焦点”随意伪造 state；优先使用 `option.initFrom(this)` 取得真实状态。

如果自定义控件希望能通过键盘获得焦点，先设定合适的 `focusPolicy`，例如 `Qt::StrongFocus`。仅仅绘制 focus rect 不会让控件变成可聚焦控件。

## 5. `backgroundColor` 到底是什么

`backgroundColor` 表示**焦点框下方的背景色**。style 可以借此选择可见、对比度合适的焦点框画法。

```cpp
option.backgroundColor = palette().color(QPalette::Base);
```

它不是“设置焦点框颜色”的 API，也不会改变控件背景。若你的控件在某一区域上绘制焦点框，应填写那一区域实际已画出的底色：

| 焦点框所在区域 | 更合理的背景色来源 |
| --- | --- |
| 普通输入区域 | `palette().color(QPalette::Base)` |
| 按钮式表面 | `palette().color(QPalette::Button)` |
| 选中列表项 | 该项实际使用的高亮底色 |
| 自绘渐变或图片背景 | 与焦点框重叠处的近似/实际底色 |

默认构造后的 `backgroundColor` 是无效 `QColor`（其 RGB 分量为 `(0, 0, 0)`）。无效色不是可靠的黑色背景；若 style 需要背景信息，应在绘制前明确赋值。

## 6. 生命周期、拷贝与版本字段

`QStyleOptionFocusRect` 是值类型的短生命周期对象，典型做法是在 `paintEvent()` 栈上创建，填好字段后立刻传给 `drawPrimitive()`。它不拥有控件、画家或 style，也不会保存指向这些对象的引用。

```cpp
QStyleOptionFocusRect option;
option.initFrom(this);
style()->drawPrimitive(QStyle::PE_FrameFocusRect, &option, &painter, this);
```

复制构造函数会复制 option 的数据，适合 style 代理在改动个别字段前保留原始上下文。没有 `QObject` 父子关系，也不需要 `new` 或 `delete`。

`Type` 和 `Version` 是 `QStyleOption` 运行时类型识别协议的一部分：

- `Type == QStyleOption::SO_FocusRect`，用于标识它是焦点框 option。
- `Version == 1`，用于兼容后续可能扩展的数据布局。
- style 接收基类指针时，可用 `qstyleoption_cast<const QStyleOptionFocusRect *>(option)` 安全识别。

常规自绘控件只需构造它，不必手动检查这两个值。

## 7. 在自定义 style 中读取它

下面展示 `QProxyStyle` 拦截焦点框绘制的典型位置。实际项目应尽量保持系统 style 的行为，仅在确有品牌或可访问性需求时做局部修改。

```cpp
#include <QProxyStyle>
#include <QStyleOptionFocusRect>

class FocusStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawPrimitive(PrimitiveElement element,
                       const QStyleOption *option,
                       QPainter *painter,
                       const QWidget *widget = nullptr) const override
    {
        if (element == PE_FrameFocusRect) {
            if (const auto *focus =
                    qstyleoption_cast<const QStyleOptionFocusRect *>(option)) {
                // focus->rect、focus->state、focus->backgroundColor
                // 是本次绘制的输入，而不是可长期保存的数据。
            }
        }

        QProxyStyle::drawPrimitive(element, option, painter, widget);
    }
};
```

`qstyleoption_cast()` 会同时核对 option 的类型和版本。不要对所有 `QStyleOption *` 直接 `static_cast` 为 `QStyleOptionFocusRect *`；primitive 的调用方可能传入的是其他 option。

## 8. 常见误区与排查

### 8.1 “我设置了 `backgroundColor`，焦点框却没有变色”

这是预期行为。该字段向 style 描述底色，不是强制指定焦点框颜色。焦点颜色、边框粗细和虚线/实线由当前 `QStyle` 决定。

### 8.2 “调用了 `drawPrimitive()`，但什么都看不见”

依次检查：

1. 控件是否真的有焦点，且 `focusPolicy` 允许它获得焦点。
2. `option.initFrom(this)` 是否在绘制前调用，使 `State_HasFocus` 等状态正确同步。
3. `option.rect` 是否在控件可见区域内，且宽高为正数。
4. 当前 style 是否选择不在此状态下绘制可见焦点提示；高对比度、平台主题和控件类别都可能影响外观。

### 8.3 “我直接用 `QPainter` 画虚线不是更简单吗”

临时调试可以，但正式控件优先调用 `PE_FrameFocusRect`。手绘虚线通常会与深色主题、系统高对比度模式和原生控件风格不协调，也可能降低键盘导航的可发现性。

### 8.4 “焦点框需要显示在控件外侧”

若只是当前控件内部的一次绘制，调整 `option.rect` 即可；若焦点框需要越过控件自身裁剪区，使用 `QFocusFrame` 并通过 `setWidget()` 绑定目标控件更合适。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型常量 | `StyleOptionType::Type` | 提供值为 `SO_FocusRect` 的运行时类型标识。 | 自定义 style 中优先让 `qstyleoption_cast()` 使用，普通代码无需手工比较。 |
| 类型常量 | `StyleOptionVersion::Version` | 表示焦点框 option 的数据布局版本，Qt 6.11.1 中为 `1`。 | 用于兼容性检查，不要把它理解成 Qt 版本或控件状态。 |
| 构造 | `QStyleOptionFocusRect()` | 创建并初始化一份焦点框绘制参数。 | 通常随后调用 `initFrom(widget)`，再填写本次绘制的 `rect` 和 `backgroundColor`。 |
| 构造 | `QStyleOptionFocusRect(const QStyleOptionFocusRect &other)` | 创建另一个焦点框 option 的值副本。 | 只复制字段，不转移 widget、painter 或 style 的所有权。 |
| 公共字段 | `QColor backgroundColor` | 告诉 style 焦点框下面实际使用的背景色。 | 不是设置焦点框颜色；无效颜色不能可靠地表示黑色背景，应按实际底色明确赋值。 |
| 继承字段 | `QStyleOption::rect` | 指定 style 应绘制焦点框的矩形区域。 | 默认可能为空；根据控件内容边距调整时要确保宽高仍为正数。 |
| 继承字段 | `QStyleOption::state` | 提供 `State_HasFocus`、`State_FocusAtBorder` 等通用状态。 | 用 `initFrom()` 同步真实控件状态，不要靠伪造 state 让控件获得焦点。 |
| 继承函数 | `QStyleOption::initFrom(const QWidget *widget)` | 从 widget 填充方向、矩形、调色板、字体和状态等公共绘制上下文。 | 它不会替你决定焦点框具体区域，也不会填充本类的 `backgroundColor`。 |
| 绘制 | `QStyle::drawPrimitive(QStyle::PE_FrameFocusRect, ...)` | 让当前 style 绘制符合平台主题的焦点框。 | 需要同时传入正确的 option、`QPainter` 和目标 widget；调用它不会改变真实焦点状态。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionFocusRect *>(option)` | 从基类 option 安全识别焦点框 option。 | 失败返回空指针；style 不应对所有 primitive option 无条件 `static_cast`。 |

---

### 一句话总结

`QStyleOptionFocusRect` 是“焦点框应如何被当前主题绘制”的一次性数据包：在自绘控件中用 `initFrom()` 取得真实状态，填入绘制区域和底色，再交给 `QStyle::PE_FrameFocusRect`，让键盘焦点提示既可见又符合平台风格。
