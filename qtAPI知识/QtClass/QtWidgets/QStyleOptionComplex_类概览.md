# Qt QStyleOptionComplex 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionComplex>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex`  
> 定位：复杂控件 style option 的公共基类

## 1. 什么叫复杂控件

Qt 的复杂控件并非一整块只能一起绘制的表面，而是由多个能独立计算几何、独立绘制、独立命中的子控件构成。

```text
QComboBox
┌──────────────────────────┐
│ 当前文本             ▼   │
└──────────────────────────┘
                         ^
                    SC_ComboBoxArrow

QSpinBox
┌──────────────────────────┐
│  12                   ▲  │
│                       ▼  │
└──────────────────────────┘

QSlider
─────────────────●──────────
                 ^
            SC_SliderHandle
```

复杂控件至少需要回答三件事：

1. 哪些子控件要画出来？
2. 哪些子控件当前处于悬停、按下或活动状态？
3. 每个子控件在当前 style 下到底位于哪里？

`QStyleOptionComplex` 提供前两件事的公共参数：

- `subControls`：这次要绘制哪些子控件；
- `activeSubControls`：哪些子控件当前处于活动反馈状态。

第三件事由 `QStyle::subControlRect()` 根据具体控件类型和 option 计算。

它解决的是：

> 给所有由多个子区域组成的控件，提供统一的子控件绘制范围和活动状态协议。

## 2. 它通常不单独使用

Qt 文档明确说明，`QStyleOptionComplex` 通常是具体复杂控件 option 的中间基类，而不是单独使用的完整 option：

```text
QStyleOptionComplex
  ├─ QStyleOptionComboBox
  ├─ QStyleOptionGroupBox
  ├─ QStyleOptionSizeGrip
  ├─ QStyleOptionSlider
  ├─ QStyleOptionSpinBox
  ├─ QStyleOptionTitleBar
  └─ QStyleOptionToolButton
```

实际绘制时要选与控件匹配的派生类：

```cpp
QStyleOptionComboBox option;
comboBox->initStyleOption(&option);

comboBox->style()->drawComplexControl(
    QStyle::CC_ComboBox,
    &option,
    &painter,
    comboBox);
```

不要为了“通用”而只创建 `QStyleOptionComplex`。它没有 combo box 的当前文本、没有 slider 的位置和范围、没有 spin box 的上下按钮状态，不能代替具体 option。

## 3. 两个核心字段分别做什么

### 3.1 `subControls`：要绘制哪些部分

`subControls` 的类型是 `QStyle::SubControls`，即 `QStyle::SubControl` 的 flags 组合。

默认值是：

```cpp
QStyle::SC_All
```

这表示当前复杂控件所有适用的子控件都可以由 style 绘制。

例如，手工构造 combo box option 时可以控制绘制范围：

```cpp
option.subControls =
    QStyle::SC_ComboBoxFrame |
    QStyle::SC_ComboBoxArrow;
```

它是“本次绘制包括哪些区域”的提示，不是：

- 子控件对象指针列表；
- 子控件所有权集合；
- 鼠标事件订阅列表；
- 自动创建子控件的配置 API。

### 3.2 `activeSubControls`：哪些部分当前活跃

`activeSubControls` 也是 `QStyle::SubControls` flags，默认值是：

```cpp
QStyle::SC_None
```

当鼠标停在 combo box 箭头、spin box 向上按钮或标题栏关闭按钮上时，控件可设置对应 sub-control，让 style 绘制悬停或按下反馈：

```cpp
if (option.activeSubControls.testFlag(QStyle::SC_ComboBoxArrow)) {
    // style 可以高亮箭头区域。
}
```

它与继承的 `state` 分工不同：

| 字段 | 回答的问题 |
| --- | --- |
| `QStyleOption::state` | 整个控件是否启用、获得焦点、按下、悬停、选中等。 |
| `activeSubControls` | 复杂控件内部具体哪一个区域是活动目标。 |

例如：

```text
state = State_Enabled | State_MouseOver
activeSubControls = SC_ComboBoxArrow
```

含义是：整个 combo box 可用且鼠标位于控件上，箭头区域是当前应显示重点反馈的子控件。

## 4. QStyle::SubControls 是 flags，不是 index

`QStyle::SubControls` 是 `QFlags<QStyle::SubControl>`。一个 option 可以同时包含多个子控件：

```cpp
option.subControls =
    QStyle::SC_SliderGroove |
    QStyle::SC_SliderHandle |
    QStyle::SC_SliderTickmarks;
```

正确操作方式：

```cpp
const bool hasArrow =
    option.subControls.testFlag(QStyle::SC_ComboBoxArrow);

option.subControls |= QStyle::SC_ComboBoxArrow;
option.subControls &= ~QStyle::SC_ComboBoxArrow;
```

不要使用 `==` 判断“是否包含”某个 flag：

```cpp
// 不推荐：只要还有其他子控件，比较就失败。
if (option.subControls == QStyle::SC_ComboBoxArrow) {
}

// 推荐：
if (option.subControls.testFlag(QStyle::SC_ComboBoxArrow)) {
}
```

常见 sub-control 的语义如下：

| 子控件 | 作用 |
| --- | --- |
| `SC_ComboBoxFrame` | combo box 外框。 |
| `SC_ComboBoxEditField` | combo box 的编辑/文本区域。 |
| `SC_ComboBoxArrow` | combo box 的下拉箭头区域。 |
| `SC_SliderGroove` | slider 的滑槽。 |
| `SC_SliderHandle` | slider 的手柄。 |
| `SC_SliderTickmarks` | slider 的刻度区域。 |
| `SC_SpinBoxUp` | spin box 的向上按钮。 |
| `SC_SpinBoxDown` | spin box 的向下按钮。 |
| `SC_SpinBoxEditField` | spin box 的编辑区。 |
| `SC_TitleBarCloseButton` | 标题栏关闭按钮。 |
| `SC_TitleBarMinButton` | 标题栏最小化按钮。 |
| `SC_TitleBarMaxButton` | 标题栏最大化按钮。 |
| `SC_TitleBarLabel` | 标题栏图标和标题文字区域。 |

不同复杂控件使用不同的 sub-control 集合。不能把 title bar 的关闭按钮 flag 当成 slider 的手柄状态。

## 5. 复杂控件的三步协作链路

### 5.1 `drawComplexControl()`：画整体

`QStyle::drawComplexControl()` 接收一个 `ComplexControl` 和 `QStyleOptionComplex`：

```cpp
QStyleOptionSpinBox option;
spinBox->initStyleOption(&option);

spinBox->style()->drawComplexControl(
    QStyle::CC_SpinBox,
    &option,
    &painter,
    spinBox);
```

当前 style 会据此绘制 spin box 的 frame、编辑区、向上/向下按钮等多个部分。

Qt 6.11.1 中常见映射是：

| `ComplexControl` | 需要的具体 option |
| --- | --- |
| `CC_ComboBox` | `QStyleOptionComboBox` |
| `CC_SpinBox` | `QStyleOptionSpinBox` |
| `CC_Slider` | `QStyleOptionSlider` |
| `CC_ScrollBar` | `QStyleOptionSlider` |
| `CC_Dial` | `QStyleOptionSlider` |
| `CC_ToolButton` | `QStyleOptionToolButton` |
| `CC_TitleBar` | `QStyleOptionTitleBar` |

### 5.2 `subControlRect()`：问 style 某部分在哪里

不要按照控件宽度猜“最后 24 像素是箭头”：

```cpp
const QRect arrowRect = comboBox->style()->subControlRect(
    QStyle::CC_ComboBox,
    &option,
    QStyle::SC_ComboBoxArrow,
    comboBox);
```

style 会综合 option 的 `rect`、布局方向、DPI、当前主题和 widget 上下文计算正确区域。

### 5.3 `hitTestComplexControl()`：问 style 鼠标击中了谁

复杂控件的命中测试也应与 style 的几何规则一致：

```cpp
const QStyle::SubControl hit =
    comboBox->style()->hitTestComplexControl(
        QStyle::CC_ComboBox,
        &option,
        event->globalPosition().toPoint(),
        comboBox);

if (hit == QStyle::SC_ComboBoxArrow) {
    // 命中下拉箭头区域。
}
```

Qt 6.11.1 文档说明：`hitTestComplexControl()` 的 position 使用 screen coordinates。因此若事件点来自 widget 局部坐标，必须先正确转换，不能混用坐标系。

三者分工如下：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 绘制 | `drawComplexControl()` | 按 `QStyleOptionComplex` 描述绘制完整复杂控件 | 需要 option 中的状态、rect、方向和 active sub-control 都正确 |
| 几何查询 | `subControlRect()` | 返回某个子控件在复杂控件中的矩形 | 坐标含义依赖 style 和 option；不要手写固定像素替代 |
| 命中测试 | `hitTestComplexControl()` | 判断一个位置命中了哪个子控件 | Qt 6.11.1 文档说明位置使用屏幕坐标；调用前要从 widget 坐标正确转换 |

## 6. 逻辑坐标、视觉坐标与 RTL

`drawComplexControl()` 的文档要求 option 的 `rect` 使用逻辑坐标。

当自定义 style 要画内部区域时，应使用 `visualRect()` 等函数处理布局方向：

```cpp
const QRect visualRectForButton =
    visualRect(option->direction,
               option->rect,
               logicalRectForButton);
```

原因是：

- LTR 下逻辑左通常就是视觉左；
- RTL 下控件内部布局可能镜像；
- 子控件顺序与可见位置受当前 style 影响；
- 用固定的 x 坐标推导按钮位置很容易出错。

因此，应让 `subControlRect()` 计算几何，或在 style 内明确做逻辑到视觉坐标的转换。

## 7. 具体派生类各自补充什么

`QStyleOptionComplex` 只提供子控件公共状态，具体类型还需要增加自己的语义：

| 派生类 | 额外信息 | 常用绘制入口 |
| --- | --- | --- |
| `QStyleOptionComboBox` | 当前文本、图标、是否可编辑、popup 状态、frame。 | `CC_ComboBox` |
| `QStyleOptionSlider` | 方向、范围、position、tick、upsideDown。 | `CC_Slider`、`CC_ScrollBar`、`CC_Dial` |
| `QStyleOptionSpinBox` | button symbols、step 状态、frame。 | `CC_SpinBox` |
| `QStyleOptionToolButton` | 文本、图标、箭头、工具按钮特征。 | `CC_ToolButton` |
| `QStyleOptionTitleBar` | 标题、图标、窗口 flags、窗口状态。 | `CC_TitleBar` |
| `QStyleOptionGroupBox` | 标题、文本对齐、frame 特征。 | `CC_GroupBox` |

所以，`QStyleOptionComplex` 不是“复杂控件完整状态”，而是这些完整状态共享的一层。

## 8. 如何从真实控件初始化

控件已经提供 `initStyleOption()` 时，优先调用它：

```cpp
#include <QComboBox>
#include <QDebug>
#include <QStyleOptionComboBox>

class InspectableComboBox final : public QComboBox
{
public:
    using QComboBox::QComboBox;

    void dumpStyleOption() const
    {
        QStyleOptionComboBox option;
        initStyleOption(&option);

        qDebug() << "sub controls:" << option.subControls;
        qDebug() << "active controls:" << option.activeSubControls;
        qDebug() << "rect:" << option.rect;
    }
};
```

若是完全自定义的复杂控件，可先初始化公共部分：

```cpp
QStyleOptionComplex option;
option.initFrom(this);
option.rect = rect();
option.subControls = QStyle::SC_All;
option.activeSubControls = QStyle::SC_None;
```

但这个对象只包含共同字段。要让标准 style 绘制 `CC_ComboBox`、`CC_Slider` 等控件，仍必须构造与该 control 匹配的具体派生 option。

## 9. 在 QProxyStyle 中安全读取 option

`drawComplexControl()` 的参数类型是 `const QStyleOptionComplex *`，但根据当前 control 仍需转换到具体类型：

```cpp
#include <QProxyStyle>
#include <QStyleOptionComboBox>

class ComboAccentStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawComplexControl(
        ComplexControl control,
        const QStyleOptionComplex *option,
        QPainter *painter,
        const QWidget *widget = nullptr) const override
    {
        if (control == CC_ComboBox) {
            if (const auto *combo =
                    qstyleoption_cast<const QStyleOptionComboBox *>(option)) {
                const bool arrowIsActive =
                    combo->activeSubControls.testFlag(
                        SC_ComboBoxArrow);
                Q_UNUSED(arrowIsActive);
            }
        }

        QProxyStyle::drawComplexControl(
            control,
            option,
            painter,
            widget);
    }
};
```

不要直接 `static_cast<const QStyleOptionComboBox *>(option)`。`option` 也可能实际是 slider、spin box、title bar 或其他复杂 option；`qstyleoption_cast()` 会检查 type/version，失败时返回 `nullptr`。

## 10. `subControls` 不等于“允许用户点击”

以下层次需要分开：

```text
subControls            -> 这次 style 应画哪些区域
activeSubControls      -> 哪些区域当前显示活动反馈
hitTestComplexControl  -> 指针落在哪个 style 子区域
真实控件事件处理       -> 点击后实际执行什么操作
```

例如，`SC_TitleBarCloseButton` 出现在 `subControls` 中，不代表点击后一定会关闭窗口。真正的关闭行为仍由 `QMdiSubWindow`、窗口事件和业务逻辑执行。

同样，把 `SC_ComboBoxArrow` 从 `subControls` 移除通常只影响绘制，不会自动禁用 combo box 的下拉行为。行为层应通过控件 API 或事件处理调整。

## 11. 生命周期、所有权和构造

`QStyleOptionComplex` 是值类型：

- 不继承 `QObject`；
- 没有 parent；
- 不拥有复杂控件、painter 或 style；
- 适合在栈上创建；
- 复制构造和赋值只复制字段；
- style 调用结束后不能保存传入的 option 指针。

Qt 6.11.1 头文件声明：

```cpp
enum StyleOptionType { Type = SO_Complex };
enum StyleOptionVersion { Version = 1 };

QStyleOptionComplex(
    int version = QStyleOptionComplex::Version,
    int type = SO_Complex);
```

带 version/type 参数的构造函数主要供派生类传入自己的类型和版本：

```cpp
class MyComplexOption : public QStyleOptionComplex
{
public:
    enum StyleOptionType {
        Type = QStyleOption::SO_ComplexCustomBase + 1
    };
    enum StyleOptionVersion {
        Version = 1
    };

    MyComplexOption()
        : QStyleOptionComplex(Version, Type)
    {
    }
};
```

普通应用不需要自行伪造 type。创建 `QStyleOptionComboBox`、`QStyleOptionSlider` 等具体对象即可。

## 12. 常见误区与排查

### 12.1 “只创建 QStyleOptionComplex，为什么 combo box 没有完整外观”

它没有 combo box 专属字段。请使用 `QStyleOptionComboBox`。

### 12.2 “我设置 activeSubControls 后，控件还是没有 hover”

这只是 style 输入。鼠标追踪、事件处理和 `update()` 仍由真实控件负责。

### 12.3 “只删掉 subControls 的箭头 flag，就能禁用下拉”

通常只会影响绘制。控件行为必须通过真实 API 或事件层处理。

### 12.4 “用 == 判断是否包含一个子控件”

`SubControls` 是 flags。使用 `testFlag()`。

### 12.5 “手工算子控件矩形，在 RTL 或高 DPI 下错位”

优先调用 `subControlRect()`；自定义 style 中遵守逻辑坐标到视觉坐标的转换规则。

### 12.6 “把复杂 option 直接强转成 combo box option”

只有实际 option 类型匹配时才合法。使用 `qstyleoption_cast()`。

## API 速查表
### 13.1 本类直接 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `QStyleOptionComplex::StyleOptionType` | 表示复杂 option 基类类型的枚举。 | `Type` 的值是 `SO_Complex`；具体派生类会定义自己的 type。 |
| 类型值 | `QStyleOptionComplex::Type` | 复杂 option 基类用于运行时识别的类型常量。 | 只用于 option 识别，不代表具体是 combo box、slider 还是 spin box。 |
| 类型 | `QStyleOptionComplex::StyleOptionVersion` | 表示复杂 option 数据布局版本的枚举。 | Qt 6.11.1 中基类版本为 `1`。 |
| 类型值 | `QStyleOptionComplex::Version` | 复杂 option 基类的数据布局版本常量。 | 供 `qstyleoption_cast()` 做兼容识别。 |
| 构造 | `QStyleOptionComplex(int version = Version, int type = SO_Complex)` | 按指定版本和类型创建复杂 option。 | 主要供具体复杂 option 派生类调用，普通代码优先直接构造具体派生类。 |
| 构造 | `QStyleOptionComplex(const QStyleOptionComplex &other)` | 创建另一个复杂 option 的副本。 | 只复制字段，不拥有控件、painter 或 style。 |
| 赋值 | `operator=(const QStyleOptionComplex &other)` | 把另一个复杂 option 的字段复制到当前对象。 | 不会复制任何外部对象的所有权。 |
| 字段 | `QStyle::SubControls subControls` | 指定本次 style 绘制应包含哪些子控件。 | 默认是 `QStyle::SC_All`；这是绘制提示，不是子控件对象列表。 |
| 字段 | `QStyle::SubControls activeSubControls` | 指定当前显示悬停、按下等活动反馈的子控件。 | 默认是 `QStyle::SC_None`；它不会自动开启真实点击行为。 |

### 13.2 继承字段和协作 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| 继承字段 | `QStyleOption::state` | 描述整个复杂控件是否启用、悬停、按下、聚焦等通用状态。 | 它描述整体状态，和 `activeSubControls` 的具体子区状态分工不同。 |
| 继承字段 | `QStyleOption::direction` | 描述控件的逻辑布局方向。 | RTL 下不要把逻辑左右直接当成视觉左右。 |
| 继承字段 | `QStyleOption::rect` | 描述复杂控件的逻辑绘制区域。 | `drawComplexControl()` 接收到的是逻辑坐标；视觉转换交给 style 辅助函数。 |
| 继承字段 | `QStyleOption::palette` | 提供绘制使用的颜色角色。 | 优先读取 palette，才能适配主题和禁用态。 |
| 继承字段 | `QStyleOption::fontMetrics` | 提供当前控件的字体度量。 | 用于文字尺寸和布局，不要另建错误字体度量。 |
| 初始化 | `QStyleOption::initFrom(const QWidget *)` | 从 QWidget 填充共同绘制状态。 | 只填充基础字段，不会知道 combo box、slider 等专属数据。 |
| 绘制 | `QStyle::drawComplexControl()` | 根据 complex control 类型绘制完整控件。 | option 的真实派生类型必须与 control 匹配。 |
| 几何 | `QStyle::subControlRect()` | 计算指定子控件在当前 style 下的矩形。 | 不要手工猜主题、DPI 和 RTL 下的箭头或按钮位置。 |
| 命中 | `QStyle::hitTestComplexControl()` | 判断一个位置命中了哪个复杂控件子区。 | position 按接口使用 screen coordinates，调用前要转换正确。 |
| 转换 | `qstyleoption_cast<const QStyleOptionComboBox *>(option)` | 安全识别 combo box 具体 option。 | 先确认当前 `ComplexControl` 是 `CC_ComboBox`。 |
| 转换 | `qstyleoption_cast<const QStyleOptionSlider *>(option)` | 安全识别 slider、scrollbar 或 dial 使用的 slider option。 | 同一 option 类型服务多个 complex control，但仍要核对 control 语义。 |
| 配置 | `QStyle::SC_All` | 表示所有适用的子控件集合。 | 通常是 `subControls` 的默认值；它不代表一定存在每一种子区。 |
| 配置 | `QStyle::SC_None` | 表示不包含任何子控件。 | 通常是 `activeSubControls` 的默认值。 |

---

### 一句话总结

`QStyleOptionComplex` 是复杂控件的共同绘制上下文：`subControls` 决定本次画哪些子控件，`activeSubControls` 决定哪些子控件显示活动反馈，`subControlRect()` 负责几何，`hitTestComplexControl()` 负责命中；真实的 combo box、slider、spin box 等仍要使用各自的具体派生 option。
