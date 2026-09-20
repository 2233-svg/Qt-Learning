# Qt QStyleOption 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOption>`  
> 所属模块：`Qt6::Widgets`  
> 继承：无  
> 定位：所有 `QStyleOption` 子类共同遵守的绘制参数协议

## 1. 先建立正确认识：它不是控件，而是绘制上下文

`QStyleOption` 是 Qt Widgets 样式系统的基础数据结构。

它的职责不是显示界面，也不是保存某个控件的长期属性，而是把一次绘制、尺寸计算或命中测试需要的信息交给 `QStyle`：

```text
真实 QWidget
    |
    | initFrom() 或控件自己的 initStyleOption()
    v
QStyleOption 及其派生类
    |
    | drawControl()
    | drawPrimitive()
    | drawComplexControl()
    | sizeFromContents()
    | subControlRect()
    v
当前 QStyle
```

例如：

- `QStyleOptionButton` 描述按钮的文字、图标和按钮状态；
- `QStyleOptionSlider` 描述滑块的方向、范围、位置和刻度；
- `QStyleOptionTab` 描述单个 tab 的形状、标题和相邻关系；
- `QStyleOptionFrame` 描述边框形状、线宽和 frame 特征；
- `QStyleOptionTitleBar` 描述 MDI 子窗口标题栏的标题、图标和窗口状态。

这些派生类最终都可以被当作 `const QStyleOption *` 传给样式接口。`QStyle` 再依据具体绘制入口把它安全转换回对应的派生类型。

因此，`QStyleOption` 要解决的核心问题是：

> 控件的业务状态和样式的像素绘制之间，需要一个轻量、可复制、可扩展的参数边界。

## 2. 它不负责什么

`QStyleOption` 很容易被误解成“控件的样式配置对象”，但它实际上不负责：

- 创建或销毁 QWidget；
- 保存控件的长期状态；
- 修改控件的文字、尺寸、调色板或布局；
- 处理鼠标、键盘和焦点事件；
- 自动调用 `QStyle`；
- 保证一份 option 永远跟随某个控件同步更新。

例如，下面的代码只改变当前 option 的绘制矩形，不会改变按钮本身的几何：

```cpp
QStyleOption option;
option.rect = QRect(0, 0, 200, 40);
```

要改变真实控件的尺寸，应使用 `resize()`、布局或控件自身的尺寸 API；要改变样式，应设置 style、palette、style sheet 或实现自定义 style。

## 3. 最常见的使用方式：在 paintEvent 中组装 option

Qt 文档给出的典型模式是：在绘制函数中创建一个具体的 style option，先从当前控件初始化通用状态，再填充派生类专属字段，最后交给 style。

```cpp
#include <QPainter>
#include <QPushButton>
#include <QStyleOptionButton>

class IconButton final : public QPushButton
{
public:
    using QPushButton::QPushButton;

protected:
    void paintEvent(QPaintEvent *) override
    {
        QStyleOptionButton option;
        option.initFrom(this);
        option.rect = rect();
        option.text = text();
        option.icon = icon();
        option.iconSize = iconSize();

        option.state |= isDown()
            ? QStyle::State_Sunken
            : QStyle::State_Raised;

        QPainter painter(this);
        style()->drawControl(
            QStyle::CE_PushButton,
            &option,
            &painter,
            this);
    }
};
```

这里的分工是：

| 代码部分 | 解决什么问题 |
| --- | --- |
| `QStyleOptionButton option` | 选择与按钮绘制入口匹配的参数类型。 |
| `option.initFrom(this)` | 填充方向、矩形、调色板、字体、状态和 style object 等通用信息。 |
| `option.text/icon` | 填充按钮自己的内容数据。 |
| `option.state` | 告诉 style 当前按钮是按下、抬起、禁用、获得焦点等状态。 |
| `style()->drawControl()` | 让当前平台 style 决定最终颜色、边框、阴影和布局。 |

真实 Qt 控件通常还有自己的 `initStyleOption()`，例如：

```cpp
QStyleOptionButton option;
QPushButton::initStyleOption(&option);
```

当控件已经提供这个函数时，优先使用控件的初始化入口。它比只调用 `QStyleOption::initFrom()` 知道更多控件专属状态。

## 4. `initFrom()` 负责填充哪些公共信息

`QStyleOption::initFrom(const QWidget *widget)` 会根据 widget 初始化这些字段：

- `state`
- `direction`
- `rect`
- `palette`
- `fontMetrics`
- `styleObject`

它是一组通用状态的便利初始化函数，不等于“完整初始化任意派生 option”。

```cpp
QStyleOption option;
option.initFrom(someWidget);
```

这段代码能得到 widget 的通用绘制上下文，但不会知道：

- 按钮文字和按钮专属 flags；
- 滑块的最小值、最大值和 slider position；
- tab 的标题、图标和相邻选中关系；
- combo box 的 editable、下拉箭头和当前文本；
- 标题栏的窗口 flags 和窗口状态。

这些信息要么由调用方补充，要么由具体控件的 `initStyleOption()` 负责填充。

### `initFrom()` 与控件专属初始化的区别

| 初始化方式 | 能提供什么 | 典型场景 |
| --- | --- | --- |
| `option.initFrom(widget)` | 通用 QWidget 样式状态 | 自定义控件、简单 primitive、手工构造基础 option。 |
| `QPushButton::initStyleOption(&option)` | 通用状态 + 按钮专属字段 | 重写按钮绘制或检查按钮 style option。 |
| `QTabWidget::initStyleOption(&option)` | 通用状态 + tab widget 专属几何 | 检查页面 frame、tab bar 和选中 tab 的关系。 |
| `QSlider::initStyleOption(&option)` | 通用状态 + 滑块范围、方向、刻度 | 自定义滑块绘制。 |

## 5. `rect` 不是固定含义，要看绘制入口

`rect` 表示当前 style 操作所使用的区域，但它的具体语义由绘制元素决定。

例如：

| 绘制元素 | `rect` 可能表示 |
| --- | --- |
| `CE_PushButton` | 整个按钮区域。 |
| `CE_PushButtonLabel` | 只包含按钮图标和文字的区域。 |
| `CE_TabBarTab` | 当前单个 tab 的矩形。 |
| `PE_FrameFocusRect` | 焦点框要绘制的区域。 |
| `PE_FrameTabWidget` | tab widget 页面 frame 的整体区域。 |

因此，style 代码不能脱离 `element` 直接假设 `option->rect` 一定是“控件外框”。

默认构造的 `QStyleOption` 中，`rect` 是 null rectangle，也就是宽度和高度都是 0。真实绘制前应由 `initFrom()`、控件专属 `initStyleOption()` 或调用方手工填充。

## 6. `state`：这一帧的交互和可见状态

`state` 的类型是 `QStyle::State`，本质上是 `QStyle::StateFlag` 的 flags 组合。

常见状态包括：

| 状态 | 样式通常用它表示 |
| --- | --- |
| `State_Enabled` | 控件可用。 |
| `State_MouseOver` | 鼠标悬停。 |
| `State_Sunken` | 按下、凹陷或被激活的 pressed 外观。 |
| `State_Raised` | 抬起、凸起的外观。 |
| `State_HasFocus` | 控件具有键盘焦点。 |
| `State_Selected` | 当前项目、tab 或条目处于选中状态。 |
| `State_Active` | 所属窗口处于活动状态。 |
| `State_Horizontal` | 方向是水平的。 |

查询 flags 时使用 `testFlag()` 或按位与：

```cpp
if (option.state.testFlag(QStyle::State_MouseOver)) {
    // 当前绘制对象处于悬停状态。
}
```

`state` 只描述本次样式调用的输入。直接修改 `option.state` 不会改变真实控件是否获得焦点，也不会触发 mouse move 或 pressed 事件。

## 7. `direction`：文字和布局的方向

`direction` 的类型是 `Qt::LayoutDirection`，默认是 `Qt::LeftToRight`。

它主要影响：

- 文字排列方向；
- 图标和文字的相对位置；
- 左右按钮的视觉顺序；
- tab、标题栏和复杂控件的镜像布局。

不要用 `QApplication::isRightToLeft()` 代替 option 中已经准备好的方向，也不要只通过 `rect.left()` / `rect.right()` 手工推断视觉左右。

```cpp
const bool rtl =
    option.direction == Qt::RightToLeft;
```

样式代码通常会使用 `QStyle::visualRect()`、`QStyle::visualPos()` 等帮助函数，把逻辑坐标转换成当前方向下的视觉坐标。

这也是为什么自定义 style 不应把按钮永远画在几何矩形的右侧：在 RTL 界面中，右侧和逻辑上的末端不一定是同一个概念。

## 8. `palette`：绘制颜色和角色

`palette` 保存当前绘制对象应使用的 `QPalette`。

它提供的不是“某个固定颜色”，而是按角色区分的颜色集合，例如：

- `QPalette::Window`
- `QPalette::Base`
- `QPalette::Button`
- `QPalette::Text`
- `QPalette::ButtonText`
- `QPalette::Highlight`
- `QPalette::HighlightedText`

style 应尽量从 option 的 palette 读取颜色，而不是直接使用固定的 `Qt::white`、`Qt::black`：

```cpp
const QColor textColor =
    option.palette.color(QPalette::ButtonText);
```

这样才能适配：

- 深色和浅色主题；
- 禁用态调色板；
- 高对比度主题；
- 当前 widget 覆盖的 palette；
- 平台 style 对角色的重新解释。

`QPalette` 是隐式共享类型，复制一份 option 不等于深拷贝一整套昂贵资源。

## 9. `fontMetrics`：不要自己猜文字尺寸

`fontMetrics` 保存当前绘制对象使用的 `QFontMetrics`。

样式在计算文字宽度、行高、基线和省略文本时，应优先使用这个字段：

```cpp
const int textWidth =
    option.fontMetrics.horizontalAdvance(optionText);
```

不要在 style 中无条件创建 `QFontMetrics(QApplication::font())`，因为当前控件可能具有：

- 局部字体；
- 平台特定字体；
- 高 DPI 下的不同字体度量；
- 主题或状态变化后的字体。

`fontMetrics` 的默认值使用应用默认字体；如果 option 来自某个 widget，`initFrom()` 会把它更新为对应 widget 的度量。

## 10. `styleObject`：被样式化的对象，不是所有权指针

`styleObject` 的类型是 `QObject *`，表示当前正在被样式化的对象。

Qt 内置 style 支持的对象类型包括：

- `QWidget`
- `QGraphicsObject`
- `QQuickItem`

它的用途是让 style 在必要时读取对象的动态属性、类型或额外上下文：

```cpp
if (auto *object = option.styleObject) {
    // 这里只读取上下文，不取得所有权。
}
```

这个指针有几个边界：

- `QStyleOption` 不拥有它；
- 复制 option 不复制对象；
- 不能因为 option 中保存了指针，就延长对象生命周期；
- 如果手工构造 option，应明确是否需要设置它；
- 只有在指针仍然有效的当前调用期间读取它。

不要把 `styleObject` 当成 `QPointer`。如果 style option 被保存到绘制调用之外，指针可能失效。

## 11. `type` 与 `version`：给 style option 做运行时识别

### 11.1 `type`

`type` 表示 option 的类型。基类默认值是：

```cpp
QStyleOption::SO_Default
```

派生类会定义自己的类型常量，例如：

```cpp
QStyleOptionButton::Type == QStyleOption::SO_Button
QStyleOptionTab::Type == QStyleOption::SO_Tab
QStyleOptionFrame::Type == QStyleOption::SO_Frame
```

### 11.2 `version`

`version` 表示当前 option 数据布局的版本。

对 `QStyleOption` 基类来说，默认值是 `1`。派生类可以使用不同版本来扩展数据布局，避免旧 style 读取新结构时越界。

普通使用者不需要手工维护 version；创建具体派生类时，构造函数会设置正确的 type/version。

### 11.3 不要直接猜类型，使用 qstyleoption_cast

style 函数通常接收基类指针：

```cpp
void drawControl(ControlElement element,
                 const QStyleOption *option,
                 QPainter *painter,
                 const QWidget *widget) const override;
```

如果当前元素要求某个派生 option，应这样转换：

```cpp
const auto *button =
    qstyleoption_cast<const QStyleOptionButton *>(option);

if (!button)
    return;
```

`qstyleoption_cast()` 会根据目标类型的 `Type` 和 `Version` 检查传入对象。失败时返回 `nullptr`。

无条件 `static_cast` 的问题在于：传入的基类指针可能来自另一个 style element，强转成功并不代表对象内存真的具有目标布局。

## 12. `OptionType` 不是让业务代码随便选择的枚举

`QStyleOption::OptionType` 包含 Qt 内置 style option 的类型标识，例如：

| 常量 | 对应 option |
| --- | --- |
| `SO_Default` | `QStyleOption` |
| `SO_FocusRect` | `QStyleOptionFocusRect` |
| `SO_Button` | `QStyleOptionButton` |
| `SO_Tab` | `QStyleOptionTab` |
| `SO_MenuItem` | `QStyleOptionMenuItem` |
| `SO_Frame` | `QStyleOptionFrame` |
| `SO_ProgressBar` | `QStyleOptionProgressBar` |
| `SO_ToolBox` | `QStyleOptionToolBox` |
| `SO_Header` | `QStyleOptionHeader` |
| `SO_DockWidget` | `QStyleOptionDockWidget` |
| `SO_ViewItem` | `QStyleOptionViewItem` |
| `SO_TabWidgetFrame` | `QStyleOptionTabWidgetFrame` |
| `SO_TabBarBase` | `QStyleOptionTabBarBase` |
| `SO_RubberBand` | `QStyleOptionRubberBand` |
| `SO_ToolBar` | `QStyleOptionToolBar` |
| `SO_GraphicsItem` | `QStyleOptionGraphicsItem` |
| `SO_Complex` | `QStyleOptionComplex` |
| `SO_Slider` | `QStyleOptionSlider` |
| `SO_SpinBox` | `QStyleOptionSpinBox` |
| `SO_ToolButton` | `QStyleOptionToolButton` |
| `SO_ComboBox` | `QStyleOptionComboBox` |
| `SO_TitleBar` | `QStyleOptionTitleBar` |
| `SO_GroupBox` | `QStyleOptionGroupBox` |
| `SO_SizeGrip` | `QStyleOptionSizeGrip` |

`SO_CustomBase` 和 `SO_ComplexCustomBase` 是为自定义 style option 预留的范围：

- 自定义普通 option 的 type 应高于 `SO_CustomBase`；
- 自定义 complex option 的 type 应高于 `SO_ComplexCustomBase`；
- 不要占用 Qt 已有的内置值。

## 13. 普通 option、complex option 和具体派生 option

可以按继承层级理解：

```text
QStyleOption
├─ QStyleOptionButton
├─ QStyleOptionFrame
├─ QStyleOptionTab
├─ QStyleOptionViewItem
├─ ...
└─ QStyleOptionComplex
   ├─ QStyleOptionComboBox
   ├─ QStyleOptionSlider
   ├─ QStyleOptionSpinBox
   ├─ QStyleOptionTitleBar
   └─ ...
```

`QStyleOptionComplex` 只增加所有复杂控件都需要的子控件状态：

- `subControls`：要绘制哪些子控件；
- `activeSubControls`：哪些子控件当前处于悬停、按下或活动状态。

它本身通常不单独使用，而是作为 combo box、slider、spin box、title bar 等具体 option 的中间基类。

复杂控件的 style API 也与普通 control 不同：

```cpp
style()->drawComplexControl(
    QStyle::CC_ComboBox,
    &comboOption,
    &painter,
    this);
```

这里 `comboOption` 的静态类型可以是 `QStyleOptionComboBox`，但 style 接口按 `const QStyleOptionComplex *` 接收。

## 14. 坐标、生命周期和所有权

### 14.1 option 通常在栈上创建

Qt 文档建议 style option 通常在调用栈上创建：

```cpp
void MyWidget::paintEvent(QPaintEvent *)
{
    QStyleOption option;
    option.initFrom(this);

    QPainter painter(this);
    style()->drawPrimitive(
        QStyle::PE_Widget,
        &option,
        &painter,
        this);
}
```

这样做的原因是：

- option 很小；
- 不需要堆分配；
- `QString`、`QPalette`、`QIcon` 等 Qt 类型通常使用隐式共享；
- option 只服务当前绘制调用；
- 不会产生“旧 option 与控件当前状态脱节”的缓存问题。

### 14.2 不拥有 widget、painter 或 style

`QStyleOption` 是值类型，不继承 `QObject`：

- 没有 parent；
- 不负责删除 `styleObject`；
- 不拥有 `QPainter`；
- 不拥有 `QStyle`；
- 不持有控件的生命周期。

style 接口返回后，调用者可以销毁栈上的 option，style 不应保存它的指针。

### 14.3 坐标要服从调用契约

不同 style API 对坐标的要求不同。`drawComplexControl()` 文档明确要求 option 的 `rect` 使用逻辑坐标，style 在需要时使用 `visualRect()` 转换为屏幕视觉坐标。

因此不要在 option 还表示逻辑坐标时，就按当前屏幕左右方向手工重排所有矩形。

## 15. 自定义控件的完整示例

下面的示例展示一个自定义控件如何：

1. 继承 `QStyleOption` 的派生类；
2. 从当前 widget 初始化通用状态；
3. 填充控件专属字段；
4. 交给当前 style 绘制；
5. 使用 style 的标准布局能力。

```cpp
#include <QPainter>
#include <QStyleOptionButton>
#include <QWidget>

class ActionSurface final : public QWidget
{
public:
    using QWidget::QWidget;

protected:
    void paintEvent(QPaintEvent *) override
    {
        QStyleOptionButton option;
        option.initFrom(this);
        option.rect = rect();
        option.text = "执行";
        option.state |= QStyle::State_Enabled;

        if (underMouse())
            option.state |= QStyle::State_MouseOver;

        QPainter painter(this);
        style()->drawControl(
            QStyle::CE_PushButton,
            &option,
            &painter,
            this);
    }
};
```

这个例子仍然只是一个绘制示例。若要实现点击行为，还需要重写鼠标事件、发出信号或使用 `QAbstractButton`。style option 不会替代控件行为层。

## 16. 自定义 style 中如何使用

### 16.1 普通绘制入口

`QStyle::drawPrimitive()`、`drawControl()`、`sizeFromContents()` 等接口接收 `const QStyleOption *`。

```cpp
class AccentStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_PushButton) {
            if (const auto *button =
                    qstyleoption_cast<const QStyleOptionButton *>(option)) {
                if (button->state.testFlag(State_MouseOver)) {
                    // 可在基础 style 之前或之后增加悬停装饰。
                }
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

### 16.2 复杂控件入口

复杂控件使用 `QStyleOptionComplex` 或其派生类：

```cpp
void AccentStyle::drawComplexControl(
    ComplexControl control,
    const QStyleOptionComplex *option,
    QPainter *painter,
    const QWidget *widget) const
{
    if (control == CC_TitleBar) {
        if (const auto *titleBar =
                qstyleoption_cast<const QStyleOptionTitleBar *>(option)) {
            const auto active =
                titleBar->state.testFlag(State_Active);
            Q_UNUSED(active);
        }
    }

    QProxyStyle::drawComplexControl(control, option, painter, widget);
}
```

### 16.3 不要把 style option 当成业务对象

不要在 style 中把 option 保存为成员变量：

```cpp
// 不建议：option 指针只在当前 style 调用期间有效
// cachedOption = option;
```

如果需要动画或延迟绘制，应复制真正需要的轻量值，并自己处理对象失效、DPI 变化和主题变化。

## 17. `qstyleoption_cast()` 与自定义 option

如果要定义自定义 style option，需要：

1. 选择不与 Qt 冲突的 type 值；
2. 定义 `StyleOptionType::Type`；
3. 定义 `StyleOptionVersion::Version`；
4. 正确调用基类构造函数；
5. 在 style 入口使用 `qstyleoption_cast()`；
6. 保证传入对象的生命周期覆盖当前调用。

概念示例：

```cpp
class MyOption : public QStyleOption
{
public:
    enum StyleOptionType { Type = QStyleOption::SO_CustomBase + 1 };
    enum StyleOptionVersion { Version = 1 };

    int emphasis = 0;

    MyOption()
        : QStyleOption(Version, Type)
    {
    }
};
```

自定义 option 的 type 值应遵循 Qt 预留范围规则。不要复用 `SO_Button`、`SO_Frame` 或其他内置值，否则 style 端可能把你的对象误识别成不兼容的 Qt option。

## 18. 常见误区与排查顺序

### 18.1 “创建了 QStyleOption，控件为什么没有变化”

创建 option 不会自动绘制，也不会自动修改控件。

必须明确调用：

```cpp
style()->drawControl(...);
```

或者把 option 交给其他需要它的 style API。

### 18.2 “我修改 option.text，真实按钮文字为什么没变”

`option.text` 只是当前绘制快照。要修改真实按钮，应调用：

```cpp
button->setText("新的标题");
```

### 18.3 “我把所有 option 都 static_cast 成 QStyleOptionButton”

style 会收到不同元素、不同派生类的 option。应该用：

```cpp
qstyleoption_cast<const QStyleOptionButton *>(option)
```

### 18.4 “我把 `rect` 当成永远是整个控件”

`rect` 的含义由具体 style element 决定。按钮整体和按钮 label 就可能使用不同区域。

### 18.5 “我缓存了 option 指针，之后重绘时继续用”

option 通常是调用者栈上的临时对象。绘制函数返回后，指针可能立即失效。

### 18.6 “只调用 initFrom 就能得到派生类全部状态”

`initFrom()` 只填充公共 QWidget 状态。派生字段要由控件的 `initStyleOption()` 或调用方自己补齐。

### 18.7 “直接画固定颜色和固定左右位置更简单”

这样通常会丢失 RTL、深色主题、禁用态、DPI 和平台 style 的行为。优先使用 option 中的 palette、fontMetrics、direction 和 state，并让当前 style 计算几何。

## API 速查表
### 19.1 公开类型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QStyleOption::OptionType` | 表示 style option 运行时类型的编号集合。 | 主要供 Qt 和 `qstyleoption_cast()` 识别，不是业务状态枚举。 |
| 枚举值 | `SO_Default` | 基础 `QStyleOption` 的类型编号。 | 默认基础类型；不要拿它伪装成具体派生 option。 |
| 枚举值 | `SO_FocusRect` | `QStyleOptionFocusRect` 的类型编号。 | 对应焦点框绘制上下文。 |
| 枚举值 | `SO_Button` | `QStyleOptionButton` 的类型编号。 | 对应按钮绘制上下文。 |
| 枚举值 | `SO_Tab` | `QStyleOptionTab` 的类型编号。 | 对应单个 tab 绘制上下文。 |
| 枚举值 | `SO_MenuItem` | `QStyleOptionMenuItem` 的类型编号。 | 对应菜单项绘制上下文。 |
| 枚举值 | `SO_Frame` | `QStyleOptionFrame` 的类型编号。 | 对应普通 frame 绘制上下文。 |
| 枚举值 | `SO_ProgressBar` | `QStyleOptionProgressBar` 的类型编号。 | 对应进度条绘制上下文。 |
| 枚举值 | `SO_ToolBox` | `QStyleOptionToolBox` 的类型编号。 | 对应 toolbox 页签绘制上下文。 |
| 枚举值 | `SO_Header` | `QStyleOptionHeader` 的类型编号。 | 对应 header section 绘制上下文。 |
| 枚举值 | `SO_DockWidget` | `QStyleOptionDockWidget` 的类型编号。 | 对应 dock 标题栏等绘制上下文。 |
| 枚举值 | `SO_ViewItem` | `QStyleOptionViewItem` 的类型编号。 | 对应 item view 中一个项目的绘制上下文。 |
| 枚举值 | `SO_TabWidgetFrame` | `QStyleOptionTabWidgetFrame` 的类型编号。 | 对应 `QTabWidget` 页面 frame。 |
| 枚举值 | `SO_TabBarBase` | `QStyleOptionTabBarBase` 的类型编号。 | 对应独立 `QTabBar` 的底座区域。 |
| 枚举值 | `SO_RubberBand` | `QStyleOptionRubberBand` 的类型编号。 | 对应橡皮筋选择框。 |
| 枚举值 | `SO_ToolBar` | `QStyleOptionToolBar` 的类型编号。 | 对应工具栏绘制上下文。 |
| 枚举值 | `SO_GraphicsItem` | `QStyleOptionGraphicsItem` 的类型编号。 | 对应 graphics view item 绘制上下文。 |
| 枚举值 | `SO_Complex` | `QStyleOptionComplex` 的类型编号。 | 复杂控件 option 的公共基类类型。 |
| 枚举值 | `SO_Slider` | `QStyleOptionSlider` 的类型编号。 | 也用于 scrollbar 和 dial 的 complex option。 |
| 枚举值 | `SO_SpinBox` | `QStyleOptionSpinBox` 的类型编号。 | 对应 spin box 绘制上下文。 |
| 枚举值 | `SO_ToolButton` | `QStyleOptionToolButton` 的类型编号。 | 对应 tool button 绘制上下文。 |
| 枚举值 | `SO_ComboBox` | `QStyleOptionComboBox` 的类型编号。 | 对应 combo box 绘制上下文。 |
| 枚举值 | `SO_TitleBar` | `QStyleOptionTitleBar` 的类型编号。 | 对应标题栏绘制上下文。 |
| 枚举值 | `SO_GroupBox` | `QStyleOptionGroupBox` 的类型编号。 | 对应 group box 绘制上下文。 |
| 枚举值 | `SO_SizeGrip` | `QStyleOptionSizeGrip` 的类型编号。 | 对应 size grip 绘制上下文。 |
| 枚举值 | `SO_CustomBase` | 自定义普通 style option 的保留起点。 | 自定义普通 option 应选择高于该值且不冲突的 type。 |
| 枚举值 | `SO_ComplexCustomBase` | 自定义复杂 style option 的保留起点。 | 自定义 complex option 应选择高于该值且不冲突的 type。 |
| 枚举 | `StyleOptionType` | 表示当前具体 `QStyleOption` 类的 type 常量。 | 基类的 `Type` 是 `SO_Default`，派生类会定义自己的同名枚举。 |
| 枚举值 | `StyleOptionType::Type` | 当前类用于运行时识别的具体类型值。 | 通常由 Qt 类定义，不要在普通代码中手动改写。 |
| 枚举 | `StyleOptionVersion` | 表示当前 option 数据布局的版本。 | 版本用于安全识别布局扩展，不是 Qt 或应用的版本号。 |
| 枚举值 | `StyleOptionVersion::Version` | 当前类默认使用的数据版本值。 | 基类 Qt 6.11.1 中为 `1`；具体派生类也可能定义自己的版本。 |

### 19.2 构造、析构和操作

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOption(int version = QStyleOption::Version, int type = SO_Default)` | 按指定 version/type 创建基础 style option。 | `state` 初始为空；具体派生类通常通过这个构造函数写入自己的版本和类型。 |
| 构造 | `QStyleOption(const QStyleOption &other)` | 创建另一个基础 option 的副本。 | 复制的是字段值，不复制或拥有 `styleObject` 指向的对象。 |
| 析构 | `~QStyleOption()` | 销毁 style option 值对象。 | 不会删除 `styleObject`，通常在当前绘制函数栈上自然销毁。 |
| 初始化 | `initFrom(const QWidget *widget)` | 从 widget 填充通用绘制状态。 | 不会自动填充按钮、滑块、tab 等派生类专属字段。 |
| 赋值 | `operator=(const QStyleOption &other)` | 把另一个基础 option 的字段复制到当前对象。 | 仍然是值复制；派生类应使用与自身类型匹配的赋值操作。 |

### 19.3 公共字段

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 字段 | `int version` | 记录当前 option 数据布局版本。 | 通常由构造函数设置，供 `qstyleoption_cast()` 判断兼容性。 |
| 字段 | `int type` | 记录当前 option 的运行时类型编号。 | 应与具体派生类的 `Type` 匹配，不要把它当成业务状态开关。 |
| 字段 | `QStyle::State state` | 描述启用、悬停、按下、焦点、选中等这一帧的交互状态。 | 是 flags 组合；修改它只影响当前 style 调用，不会改变真实 widget 状态。 |
| 字段 | `Qt::LayoutDirection direction` | 描述逻辑文字和布局方向。 | RTL 绘制时应使用 style 的视觉坐标辅助函数。 |
| 字段 | `QRect rect` | 提供当前 style 操作使用的绘制或计算区域。 | 具体含义由 element 决定，默认是空矩形，不一定代表整个 widget。 |
| 字段 | `QFontMetrics fontMetrics` | 提供当前绘制对象的字体度量。 | 用它计算文字尺寸，避免使用错误的应用默认字体。 |
| 字段 | `QPalette palette` | 提供当前绘制对象的颜色角色集合。 | 优先读取 palette 角色，才能适配主题、禁用态和高对比度。 |
| 字段 | `QObject *styleObject` | 指向当前正在被样式化的对象。 | option 不拥有它；只在当前调用期间读取，不能把它当成延长生命周期的指针。 |

### 19.4 相关非成员

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型转换 | `qstyleoption_cast<T>(QStyleOption *option)` | 根据 type/version 把可写基础 option 安全转换为目标派生 option。 | 失败返回 `nullptr`；目标类型必须和真实 option 布局匹配。 |
| 类型转换 | `qstyleoption_cast<T>(const QStyleOption *option)` | 根据 type/version 把只读基础 option 安全转换为目标派生 option。 | 自定义 style 中优先使用它，不要无条件 `static_cast`。 |

---

### 一句话总结

`QStyleOption` 是 Qt 样式系统的公共绘制协议：它用 `rect` 描述当前区域，用 `state` 描述交互状态，用 `direction`、`palette` 和 `fontMetrics` 提供平台相关绘制上下文，用 `type/version` 支持安全识别；普通代码在当前绘制调用中创建它，具体控件再通过派生 option 补充自己的信息。
