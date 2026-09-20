# Qt QStyleOptionSlider 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStyleOptionSlider>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex -> QStyleOptionSlider`  
> 定位：为滑块、滚动条和拨盘提供绘制与子控件几何计算所需的状态快照

## 1. 它解决的不是“保存滑块值”

`QStyleOptionSlider` 是样式系统的数据载体，不是可交互控件。`QSlider`、`QScrollBar` 和 `QDial` 在绘制自己、计算手柄矩形或判断鼠标点到哪一部分时，把自身状态装进这个对象，传给 `QStyle`。

```text
QSlider / QScrollBar / QDial
  └─ initStyleOption(&option)
       ├─ 范围、值、手柄位置、方向、步长
       ├─ QStyleOptionComplex 的 subControls / activeSubControls
       └─ QStyle 的 drawComplexControl()、subControlRect()、hitTestComplexControl()
```

因此它在这些场景中出现：

- 重写控件 `paintEvent()`，但依然使用当前平台 style 来画沟槽、手柄、箭头和刻度；
- 实现 `QProxyStyle`，只改变特定子控件的几何或外观；
- 用 `QStyle::subControlRect()` 精确取得滑块手柄、滚动条滑块等区域，进行叠加绘制或命中判断。

业务代码不应通过它修改真实值。要改变真实控件，仍然调用 `QAbstractSlider::setValue()`、`setSliderPosition()` 等 API。

## 2. 三个控件为何共用一个 option

它们外观不同，底层却都遵循“在一个范围内移动位置”的模型：

| 控件 | 这个 option 中特别重要的字段 |
| --- | --- |
| `QSlider` | `sliderPosition`、`sliderValue`、`tickPosition`、`tickInterval` |
| `QScrollBar` | `pageStep`、`singleStep`、`sliderPosition`、`upsideDown` |
| `QDial` | `dialWrapping`、`notchTarget`、`sliderPosition` |

`QStyleOptionSlider` 继承自 `QStyleOptionComplex`。这比普通 `QStyleOption` 多出“复杂控件由哪些子部件组成、哪个子部件正被操作”的信息，例如 `subControls` 与 `activeSubControls`。它们是样式画出滚动条箭头、滑块手柄、槽沟并处理悬停态的基础。

本类自身也没有所有权语义：通常在栈上创建，绘制调用结束后销毁。

## 3. 标准用法：让 style 计算手柄区域

写滑块子类时，手工猜测手柄宽度是脆弱的。不同 style、系统主题、缩放比例下，手柄尺寸都可能不同。应让当前 style 计算：

```cpp
void VolumeSlider::paintEvent(QPaintEvent *)
{
    QStyleOptionSlider option;
    initStyleOption(&option);

    const QRect handleRect = style()->subControlRect(
        QStyle::CC_Slider,
        &option,
        QStyle::SC_SliderHandle,
        this);

    QStylePainter painter(this);
    painter.drawComplexControl(QStyle::CC_Slider, option);

    painter.setPen(Qt::white);
    painter.drawText(handleRect, Qt::AlignCenter, QString::number(value()));
}
```

这里 `initStyleOption()` 比手工填字段更可靠，因为它还会填写基类的 `rect`、`palette`、`state`、`direction`、`fontMetrics` 以及复杂控件的子控件状态。第一帧看起来正常、深色主题或禁用状态却错乱，常常就是因为手工 option 缺少这些上下文。

对 `QScrollBar` 应配套使用 `QStyle::CC_ScrollBar` 与对应的 `SC_ScrollBar...` 子控件，而不是把它当成 `CC_Slider`。

## 4. 最关键的区别：`sliderPosition` 不一定等于 `sliderValue`

这两个字段在大多数时候相同，因此很容易被混淆。差异在用户拖动、且 `QAbstractSlider::tracking` 为 `false` 时出现：

```text
初始值：sliderValue = 30，sliderPosition = 30
拖动手柄到 70，tracking = false：
  sliderPosition = 70    视觉上的手柄已经移动
  sliderValue    = 30    业务值尚未提交
松开鼠标后：
  sliderPosition = 70
  sliderValue    = 70
```

它让 style 能在“预览位置”和“已提交值”不一致时正确画出手柄。

- `sliderPosition`：当前手柄的可见位置。
- `sliderValue`：控件已经确认的值；无 tracking 时是拖动前的值。
- `tracking == true`：每次拖动都提交，两个字段相等。

自定义外观时，手柄几何应以 `sliderPosition` 为依据；把业务数值显示在标签或浮层时，则要有意识地选择展示预览位置还是已提交值。

## 5. 方向：`orientation`、`upsideDown` 与控制反转

`orientation` 只有横向和纵向，决定轨道主要沿哪个轴布置。`upsideDown` 决定“数值增长”对应哪一个空间方向：

```text
upsideDown = false：通常向右或向上，数值变大
upsideDown = true ：通常向左或向下，数值变大
```

`upsideDown` 是**视觉映射**，会影响 `QStyle::sliderPositionFromValue()`、`sliderValueFromPosition()` 等换算。不要将它与 `QAbstractSlider::invertedControls` 混为一谈：

- `invertedAppearance` 最终影响 option 中的 `upsideDown`，改变画面和鼠标位置对应的数值方向；
- `invertedControls` 改的是键盘、滚轮等输入动作的增减语义，不等于镜像外观。

从控件取得 option 时，让 `initStyleOption()` 处理这些组合规则。自己创建 option 做独立绘制时，必须根据目标控件和 RTL 布局明确设置方向，不能只填范围和值。

## 6. 步长、刻度和拨盘专用字段

### 6.1 `singleStep` 与 `pageStep`

它们描述两个动作粒度：

- `singleStep`：方向键、滚轮或小箭头的一小格移动量；
- `pageStep`：点击滚动条槽沟等“大步”移动量。

对 style 来说，它们不仅是业务数据，也可能影响滚动条滑块长度、槽沟点击后的反馈及可访问性呈现。

### 6.2 `tickInterval` 与 `tickPosition`

这组字段主要服务 `QSlider`：

- `tickInterval`：相邻刻度对应的数值间隔；
- `tickPosition`：刻度在滑块上方、下方、两侧或不显示。

`tickInterval == 0` 不代表“自动画每一格”；它表示 option 中没有指定显式间隔。真实 `QSlider` 的自动间隔与 style/控件规则有关，重写绘制时不要擅自把零理解为 1。

### 6.3 `dialWrapping` 与 `notchTarget`

它们主要服务 `QDial`：

- `dialWrapping`：最大值后是否可绕回最小值；
- `notchTarget`：期望的刻度间像素距离，类型是 `qreal`。

这不是业务精度设置。`notchTarget` 是绘制密度的目标，style 或 `QDial` 会按可用圆弧、范围和缩放决定实际画出多少刻度。

## 7. 自定义 QProxyStyle：先识别类型，再改一个点

`drawComplexControl()` 收到的是基类 `QStyleOptionComplex *`。安全的自定义方式是先筛选 complex control，再通过 `qstyleoption_cast()` 取得这个子类：

```cpp
void CompactStyle::drawComplexControl(
    QStyle::ComplexControl control,
    const QStyleOptionComplex *option,
    QPainter *painter,
    const QWidget *widget) const
{
    if (control == QStyle::CC_Slider) {
        const auto *slider =
            qstyleoption_cast<const QStyleOptionSlider *>(option);

        if (slider) {
            // 读取 sliderPosition、orientation、state 等数据。
        }
    }

    QProxyStyle::drawComplexControl(control, option, painter, widget);
}
```

不要将 `option` 强制转换后马上解引用。`QStyleOptionSlider::Type = SO_Slider` 和 `Version = 1` 是 `qstyleoption_cast()` 识别布局的依据。大多数 style 代码不需要手工比较它们。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionSlider` 自己声明的类型、构造函数与公开字段。`QStyleOptionComplex` 继承来的 `subControls`、`activeSubControls` 等通用复杂控件状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_Slider` | 标识这是滑块类 style option。 | 供样式系统和 `qstyleoption_cast()` 做运行时识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构的版本。 | 普通代码无需手工比较版本，安全转换会处理兼容性。 |
| 构造 | `QStyleOptionSlider()` | 创建并以默认值初始化一份 option。 | 从真实控件绘制时，随后调用其 `initStyleOption()`。 |
| 构造 | `QStyleOptionSlider(const QStyleOptionSlider &other)` | 复制另一份 option。 | 是值复制，不复制控件和 QObject 生命周期。 |
| 公开字段 | `bool dialWrapping` | 指定拨盘是否从最大值绕回最小值。 | 默认 `false`；主要由 `QDial` 使用。 |
| 公开字段 | `int maximum` | 滑块范围上界。 | 默认 `0`；必须和 `minimum`、位置和值保持一致。 |
| 公开字段 | `int minimum` | 滑块范围下界。 | 默认 `0`；不要假定下界永远是零。 |
| 公开字段 | `qreal notchTarget` | 设置拨盘相邻刻度的目标像素间隔。 | 默认 `0.0`；是绘制密度目标，不是刻度数。 |
| 公开字段 | `Qt::Orientation orientation` | 指定横向或纵向布局。 | 默认 `Qt::Horizontal`；影响几何换算的主轴。 |
| 公开字段 | `int pageStep` | 指定大步移动的数值间隔。 | 默认 `0`；滚动条槽沟点击等操作会用到它。 |
| 公开字段 | `int singleStep` | 指定小步移动的数值间隔。 | 默认 `0`；对应方向键、滚轮或小箭头等细粒度动作。 |
| 公开字段 | `int sliderPosition` | 表示手柄当前可见位置。 | `tracking == false` 时可不同于 `sliderValue`。 |
| 公开字段 | `int sliderValue` | 表示控件已经确认的值。 | 无 tracking 拖动期间仍是拖动前的值。 |
| 公开字段 | `int tickInterval` | 指定相邻刻度对应的数值间隔。 | 默认 `0`；不要简单把零解释为一格一刻度。 |
| 公开字段 | `QSlider::TickPosition tickPosition` | 指定刻度显示在哪一侧，或不显示。 | 默认 `QSlider::NoTicks`；主要由 `QSlider` 使用。 |
| 公开字段 | `bool upsideDown` | 指定值增大时视觉上是向反方向还是正常方向移动。 | 默认 `false`；不要与 `invertedControls` 混淆。 |

## 9. 一句话总结

`QStyleOptionSlider` 是滑块类复杂控件的一帧绘制状态；最重要的是让 `initStyleOption()` 填好它，并在自定义绘制中尊重 `sliderPosition` 与 `sliderValue`、`upsideDown` 和子控件几何之间各自不同的职责。
