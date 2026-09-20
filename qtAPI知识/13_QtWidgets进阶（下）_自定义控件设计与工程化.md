# Qt Widgets 进阶（下）：自定义控件设计与工程化

> 适用版本：Qt 6.11.1  
> 核心类型：`QWidget`、`QPainter`、`QStyle`、`QStyleOption`、`QSizePolicy`、`Q_PROPERTY`、`QAccessible`

自定义 Widget 不只是“在 `paintEvent()` 里画点东西”。一个可复用控件还要正确参与对象所有权、布局协商、样式、焦点、键鼠输入、属性系统、可访问性和测试。

本篇从选择实现方式开始，再用一个完整的 `LevelControl` 串起这些契约。

## 1. 三种自定义方式怎么选

### 1.1 复合控件：组合现有 Widget

```cpp
class SearchBox : public QWidget
{
public:
    explicit SearchBox(QWidget *parent = nullptr)
        : QWidget(parent)
    {
        auto *edit = new QLineEdit(this);
        auto *button = new QPushButton(QStringLiteral("搜索"), this);
        auto *layout = new QHBoxLayout(this);
        layout->addWidget(edit);
        layout->addWidget(button);
    }
};
```

适合表单片段、带标签的输入区、工具条式组件。优点是现有控件已经处理主题、键盘、输入法和可访问性。

### 1.2 继承现有控件

只需要给标准控件增加少量行为时，直接继承最接近的类：

```cpp
class PathEdit : public QLineEdit
{
public:
    using QLineEdit::QLineEdit;

protected:
    void dragEnterEvent(QDragEnterEvent *event) override;
    void dropEvent(QDropEvent *event) override;
};
```

不要为了改颜色就重写整个 `QLineEdit`。样式、palette 或 Delegate 往往足够。

### 1.3 完全自绘控件

适合仪表、波形、画布、时间轴、特殊选择器等没有合适标准控件的场景。需要自己实现：

- 绘制和尺寸建议；
- 鼠标、键盘、焦点；
- 状态与通知信号；
- 高 DPI、主题和 RTL；
- 可访问性；
- 边界测试。

优先级通常是：组合现有控件 > 扩展现有控件 > 从 `QWidget` 完全自绘。

## 2. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

后文若使用 `QSignalSpy` 和 GUI 测试：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets Test)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::Test)
```

## 3. 先设计控件的公共契约

在写绘制前，先回答：

```text
状态：value、minimum、maximum
命令：setValue、setRange
通知：valueChanged
输入：鼠标拖动、方向键、Home/End
展示：进度条形状和焦点框
布局：首选尺寸、最小尺寸、伸缩策略
辅助技术：名称、角色、当前值
```

好的控件把业务状态暴露成属性和信号，而不是要求外部直接改成员并调用 `update()`。

## 4. 完整示例：LevelControl 声明

```cpp
#include <QColor>
#include <QWidget>

class LevelControl : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)
    Q_PROPERTY(int minimum READ minimum WRITE setMinimum)
    Q_PROPERTY(int maximum READ maximum WRITE setMaximum)
    Q_PROPERTY(QColor accentColor READ accentColor
               WRITE setAccentColor NOTIFY accentColorChanged)

public:
    explicit LevelControl(QWidget *parent = nullptr);

    int value() const { return m_value; }
    int minimum() const { return m_minimum; }
    int maximum() const { return m_maximum; }
    QColor accentColor() const { return m_accentColor; }

    QSize sizeHint() const override;
    QSize minimumSizeHint() const override;

public slots:
    void setValue(int value);
    void setMinimum(int minimum);
    void setMaximum(int maximum);
    void setRange(int minimum, int maximum);
    void setAccentColor(const QColor &color);

signals:
    void valueChanged(int value);
    void accentColorChanged(const QColor &color);

protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;

private:
    void setValueFromPosition(qreal x);

    int m_value = 25;
    int m_minimum = 0;
    int m_maximum = 100;
    QColor m_accentColor = QColor("#1677c8");
};
```

`Q_OBJECT` 是必要的，因为类声明了自己的 signal 和 `Q_PROPERTY`。CMake 应启用 AUTOMOC；`qt_add_executable()` / `qt_add_library()` 的标准 Qt 配置通常会接入它。

### 4.1 为什么属性要有 NOTIFY

`NOTIFY` 使外部能观察值变化，属性绑定、Designer 和测试工具也更容易使用它。通知信号应只在值真正变化后发送一次。

## 5. 构造和尺寸策略

```cpp
LevelControl::LevelControl(QWidget *parent)
    : QWidget(parent)
{
    setFocusPolicy(Qt::StrongFocus);
    setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
    setAccessibleName(QStringLiteral("级别"));
}

QSize LevelControl::sizeHint() const
{
    return QSize(240, qMax(32, fontMetrics().height() + 14));
}

QSize LevelControl::minimumSizeHint() const
{
    return QSize(80, qMax(24, fontMetrics().height() + 8));
}
```

这里的含义是：水平方向愿意吸收额外空间，垂直方向希望保持首选高度。

### 5.1 sizeHint、minimumSizeHint、sizePolicy 的分工

| 项目 | 回答的问题 |
|---|---|
| `sizeHint()` | 控件舒服地显示需要多大 |
| `minimumSizeHint()` | 再小就很难使用的建议尺寸 |
| `minimumSize` | 不允许低于的硬限制 |
| `maximumSize` | 不允许超过的硬限制 |
| `sizePolicy` | 有多余/不足空间时是否愿意伸缩 |

不要把 `setFixedSize()` 当作实现尺寸建议的捷径。固定尺寸会破坏布局、字体缩放、翻译长度和高 DPI 适配。

### 5.2 何时调用 `updateGeometry()`

当会影响 `sizeHint()` 的状态变化时：

```cpp
updateGeometry(); // 通知父布局重新协商
update();         // 请求重新绘制
```

`value` 变化只影响图形填充，不影响首选尺寸，因此只需 `update()`。字体变化会影响 `fontMetrics()`，应在 `changeEvent()` 中调用 `updateGeometry()`。

## 6. Setter：维护不变量并只通知一次

```cpp
#include <algorithm>

void LevelControl::setValue(int value)
{
    const int bounded = qBound(m_minimum, value, m_maximum);
    if (bounded == m_value)
        return;

    m_value = bounded;
    update();
    emit valueChanged(m_value);
}

void LevelControl::setRange(int minimum, int maximum)
{
    if (minimum > maximum)
        std::swap(minimum, maximum);

    const bool rangeChanged = minimum != m_minimum
                           || maximum != m_maximum;
    if (!rangeChanged)
        return;

    m_minimum = minimum;
    m_maximum = maximum;
    setValue(m_value); // 必要时钳制，并只发一次 valueChanged
    update();
}

void LevelControl::setMinimum(int minimum)
{
    setRange(minimum, qMax(minimum, m_maximum));
}

void LevelControl::setMaximum(int maximum)
{
    setRange(qMin(m_minimum, maximum), maximum);
}

void LevelControl::setAccentColor(const QColor &color)
{
    if (!color.isValid() || color == m_accentColor)
        return;
    m_accentColor = color;
    update();
    emit accentColorChanged(m_accentColor);
}
```

这里集中维护 `minimum <= maximum` 和 `value` 位于区间内两个不变量。所有写入路径都走 setter，避免键盘、鼠标和外部调用各自实现一套边界逻辑。

### 6.1 信号描述“已经发生的事实”

先更新成员，再发送 `valueChanged(newValue)`。槽执行时若调用 `value()`，必须读到新状态。

不要在值没有变化时发送通知，否则双向绑定和业务槽可能发生无意义循环。

## 7. 绘制：只从当前状态生成画面

```cpp
#include <QPainter>
#include <QStyle>
#include <QStyleOption>

void LevelControl::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    // 让当前 QStyle 先绘制 Widget 背景，样式表才能正常参与。
    QStyleOption option;
    option.initFrom(this);
    style()->drawPrimitive(QStyle::PE_Widget, &option, &painter, this);

    const QRectF track = QRectF(contentsRect()).adjusted(8, 8, -8, -8);
    painter.setPen(Qt::NoPen);
    painter.setBrush(palette().color(QPalette::Midlight));
    painter.drawRoundedRect(track, 4, 4);

    const qreal span = m_maximum - m_minimum;
    const qreal ratio = span > 0
        ? qreal(m_value - m_minimum) / span
        : 0.0;

    QRectF logicalFill = track;
    logicalFill.setWidth(track.width() * ratio);
    const QRect fill = QStyle::visualRect(
        layoutDirection(), track.toRect(), logicalFill.toRect());

    painter.setBrush(isEnabled()
        ? m_accentColor
        : palette().color(QPalette::Disabled, QPalette::Mid));
    painter.drawRoundedRect(fill, 4, 4);

    painter.setPen(palette().color(QPalette::Text));
    painter.drawText(track, Qt::AlignCenter,
                     QString::number(m_value));

    if (hasFocus()) {
        QStyleOptionFocusRect focus;
        focus.initFrom(this);
        focus.rect = contentsRect().adjusted(2, 2, -2, -2);
        focus.backgroundColor = palette().color(QPalette::Window);
        style()->drawPrimitive(QStyle::PE_FrameFocusRect,
                               &focus, &painter, this);
    }
}
```

绘制函数应是状态到像素的纯粹投影：不要在 `paintEvent()` 修改 value、发业务信号、访问网络或启动定时器。

### 7.1 为什么使用 palette 和 QStyle

硬编码所有颜色会破坏深色主题、禁用状态和平台风格。自定义强调色可以是属性，其余结构色、文本色、焦点框尽量来自 palette/Style。

### 7.2 RTL

`QStyle::visualRect()` 把逻辑上的“从起点填充”映射为左到右或右到左方向。支持 RTL 不能只翻转文字，水平交互和图形也要保持语义一致。

### 7.3 高 DPI

用设备无关坐标绘制，避免把预先按物理像素生成的位图直接拉伸。缓存 `QPixmap` 时关注 `devicePixelRatio()`，资源图标优先准备高分辨率版本或 SVG。

## 8. 鼠标和键盘输入统一走 Setter

```cpp
void LevelControl::setValueFromPosition(qreal x)
{
    const QRect track = contentsRect().adjusted(8, 8, -8, -8);
    if (track.width() <= 0)
        return;

    qreal ratio = qBound(0.0,
        (x - track.left()) / track.width(), 1.0);
    if (layoutDirection() == Qt::RightToLeft)
        ratio = 1.0 - ratio;

    const int value = qRound(m_minimum
                           + ratio * (m_maximum - m_minimum));
    setValue(value);
}

void LevelControl::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        setFocus(Qt::MouseFocusReason);
        setValueFromPosition(event->position().x());
        event->accept();
        return;
    }
    QWidget::mousePressEvent(event);
}

void LevelControl::mouseMoveEvent(QMouseEvent *event)
{
    if (event->buttons() & Qt::LeftButton) {
        setValueFromPosition(event->position().x());
        event->accept();
        return;
    }
    QWidget::mouseMoveEvent(event);
}

void LevelControl::keyPressEvent(QKeyEvent *event)
{
    const bool rtl = layoutDirection() == Qt::RightToLeft;

    switch (event->key()) {
    case Qt::Key_Left:
        setValue(m_value + (rtl ? 1 : -1));
        break;
    case Qt::Key_Right:
        setValue(m_value + (rtl ? -1 : 1));
        break;
    case Qt::Key_Home:
        setValue(m_minimum);
        break;
    case Qt::Key_End:
        setValue(m_maximum);
        break;
    default:
        QWidget::keyPressEvent(event);
        return;
    }
    event->accept();
}
```

所有路径最终只调用 `setValue()`，不变量、刷新和通知因此天然一致。

## 9. 属性系统深入

### 9.1 常见 Q_PROPERTY 属性项

```cpp
Q_PROPERTY(Type name
           READ getter
           WRITE setter
           RESET resetter
           NOTIFY changedSignal
           DESIGNABLE true
           STORED true
           USER true)
```

| 项 | 含义 |
|---|---|
| `READ` | 读取函数 |
| `WRITE` | 写入函数 |
| `RESET` | 恢复默认值 |
| `NOTIFY` | 值改变通知信号 |
| `DESIGNABLE` | 是否显示在 Designer 属性编辑器 |
| `STORED` | 是否保存到 `.ui` 等持久表示 |
| `USER` | 是否为类的主要用户属性 |
| `BINDABLE` | 提供 `QBindable<T>`，支持 Qt 6 属性绑定 |

普通 Widgets 项目并不要求所有属性都改写成 bindable。只有确实采用 Qt 6 C++ 属性绑定时，再引入 `QProperty` / `QBindable`，并遵守它们的通知约束。

### 9.2 动态属性

```cpp
widget->setProperty("severity", "warning");
```

动态属性适合少量元数据和样式选择器，不提供编译期类型检查，也不会自动形成强类型业务 API。核心状态仍应使用正式 `Q_PROPERTY`。

## 10. 让自定义 Widget 支持样式表

从 `QWidget` 直接派生并完全自绘时，可在 `paintEvent()` 开头用：

```cpp
QStyleOption option;
option.initFrom(this);
style()->drawPrimitive(QStyle::PE_Widget, &option, &painter, this);
```

然后样式表背景和边框才能由 Style 正常绘制：

```css
LevelControl {
    background: palette(base);
    border: 1px solid palette(mid);
}
LevelControl:disabled {
    background: palette(window);
}
```

自定义 Qt 属性可通过 `qproperty-属性名` 设置：

```css
LevelControl {
    qproperty-accentColor: #1677c8;
}
```

样式表不是业务状态系统。不要通过反复替换整段样式表表达 value，否则会触发昂贵的重新 polish；value 的绘制仍应由属性和 `update()` 驱动。

## 11. 复合控件的封装边界

一个复合控件不应把内部所有 Widget 都公开出去：

```cpp
class RangeEditor : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(int minimum READ minimum WRITE setMinimum)

public:
    explicit RangeEditor(QWidget *parent = nullptr);
    int minimum() const;

public slots:
    void setMinimum(int value);

signals:
    void minimumChanged(int value);

private:
    QSpinBox *m_spinBox;
};
```

外部依赖 `minimum` 语义，不依赖内部恰好是 `QSpinBox`。将来换成滑块或带单位编辑器时，公共 API 不变。

### 11.1 内部对象的 parent 和布局

给布局传入 `this`，或调用 `setLayout()`，可让布局成为控件的顶层布局；通过 layout 添加的 Widget 会被重新设为正确父 Widget。仍建议构造时明确传 parent，使生命周期一眼可见。

### 11.2 焦点代理与 buddy

```cpp
label->setBuddy(editor);
setFocusProxy(editor);
```

Label 的助记键可把焦点送到 editor，外部把焦点设给复合控件时也会落到真正的输入控件。

## 12. 可访问性

最低要求：

```cpp
control->setAccessibleName(QStringLiteral("音量"));
control->setAccessibleDescription(
    QStringLiteral("使用左右方向键调整"));
```

还要保证：

- 不依赖颜色作为唯一状态信息；
- 支持键盘访问并显示焦点；
- tooltip 不能作为唯一标签；
- 随字体和系统缩放正确布局；
- 文本有足够对比度。

### 12.1 完全自绘控件的角色和值接口

`accessibleName` 只能提供名称。屏幕阅读器若需要识别它是滑块并读取/修改当前值，应实现或注册 `QAccessibleInterface`，通常基于 `QAccessibleWidget`，并按需要提供 `QAccessibleValueInterface`。

值改变后还应通知辅助技术：

```cpp
QAccessibleValueChangeEvent event(this, m_value);
QAccessible::updateAccessibility(&event);
```

只有应用实际启用可访问性时，这类通知才有意义，但控件库应从设计阶段保留正确语义。

## 13. 动画和定时状态

属性值动画可使用 `QPropertyAnimation`：

```cpp
auto *animation = new QPropertyAnimation(control, "value", control);
animation->setDuration(180);
animation->setStartValue(control->value());
animation->setEndValue(80);
animation->start(QAbstractAnimation::DeleteWhenStopped);
```

每个动画帧会调用 `setValue()`，因此 setter 必须轻量。不要在 value setter 中写文件、查询数据库或做大规模布局。

频繁新建动画前应停止或复用旧动画，否则多个动画会竞争写同一属性。

## 14. 绘制性能与缓存

先测量，再缓存。常见原则：

- 静态复杂背景可缓存为 `QPixmap`；
- 尺寸、DPI、palette、Style 或字体变化时失效缓存；
- 高频值变化只更新受影响区域；
- 不在 paint 中构造昂贵路径和加载图片；
- 透明叠层会增加合成成本；
- 不要为了“性能”关闭所有更新后忘记重新启用。

缓存键至少可能包含：

```text
widget size + devicePixelRatio + palette/style + relevant properties
```

仅按 width/height 缓存，在切换屏幕 DPI 或深色主题后会得到错误图像。

## 15. Designer 中使用自定义控件

### 15.1 Promote：日常项目优先

在 `.ui` 中先放一个 `QWidget` 占位，然后 Promote 为 `LevelControl`，配置类名和头文件。`uic` 生成代码时会实例化真实类型。

适合：

- 控件只在当前项目或少数项目中使用；
- 不需要在 Designer 画布里实时呈现专用属性；
- 希望避免额外插件部署。

### 15.2 Designer 插件

需要控件出现在 Widget Box、在属性编辑器展示元属性、提供默认图标和容器扩展时，实现 `QDesignerCustomWidgetInterface` 插件。

构建依赖轮廓：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Gui UiPlugin Widgets)
qt_add_plugin(customwidgetplugin)
target_link_libraries(customwidgetplugin PUBLIC
    Qt6::Core Qt6::Gui Qt6::UiPlugin Qt6::Widgets)
```

插件必须与 Designer 的 Qt 版本、编译器架构和 Debug/Release 兼容，并安装到 Qt 插件路径的 `designer` 子目录。控件实现最好放在独立库中，由应用和 Designer 插件共同链接，避免应用依赖 Designer 库。

## 16. 测试自定义控件

### 16.1 属性和信号

```cpp
void TestLevelControl::valueIsClamped()
{
    LevelControl control;
    QSignalSpy spy(&control, &LevelControl::valueChanged);

    control.setRange(0, 100);
    control.setValue(150);

    QCOMPARE(control.value(), 100);
    QCOMPARE(spy.count(), 1);

    control.setValue(100);
    QCOMPARE(spy.count(), 1); // 相同值不重复通知
}
```

### 16.2 键盘交互

```cpp
void TestLevelControl::keyboardChangesValue()
{
    LevelControl control;
    control.setValue(50);
    control.show();
    control.setFocus();

    QTest::keyClick(&control, Qt::Key_Right);
    QCOMPARE(control.value(), 51);

    QTest::keyClick(&control, Qt::Key_Home);
    QCOMPARE(control.value(), control.minimum());
}
```

### 16.3 还应覆盖

```text
空区间 minimum == maximum
minimum > maximum 的输入策略
鼠标点在左右边界和控件外
Left/Right 在 RTL 下的行为
disabled 时是否拒绝用户输入
字体、Style、palette 变化后的尺寸和重绘
高 DPI 截图和焦点框
屏幕阅读器能否读出名称、角色和值
```

绘制结果可用固定 palette、字体和尺寸做图像对比，但跨平台像素可能不同。优先测试状态和交互；视觉回归测试按平台维护基线。

## 17. 发布为控件库

公共控件应明确：

- 类的命名空间和导出宏；
- 二进制兼容策略；
- 属性默认值与信号保证；
- 是否允许子类化；
- 资源如何打包；
- 最低 Qt 版本；
- 线程限制：Widget 只能在 GUI 线程创建和使用；
- 主题、RTL、DPI 和可访问性支持范围。

大规模库可用 d-pointer 隐藏实现细节，减少私有成员变化对 ABI 的影响。应用内部控件不必为了形式套用全部库级设计。

## 18. 常见错误

### 18.1 在 paintEvent 中改变状态

可能触发 `update()` → paint → 改状态 → update 的循环。绘制只读状态。

### 18.2 值变化却不发信号

外部标签、属性绑定和测试无法同步。所有写入路径应汇总到一个 setter。

### 18.3 每次 setter 都发信号

相同值也通知会造成冗余重绘和绑定循环。先比较，再修改，再通知。

### 18.4 只实现鼠标，不实现键盘和焦点

控件对键盘用户不可用，自动化测试也更脆弱。交互语义要有键盘等价操作。

### 18.5 硬编码尺寸和颜色

在翻译、字体缩放、深色主题和高 DPI 下失效。尺寸参考 font metrics/Style，颜色参考 palette。

### 18.6 混淆 `update()` 与 `updateGeometry()`

画面改变用 `update()`；首选/最小尺寸改变再加 `updateGeometry()`。后者不是重绘函数。

### 18.7 用控件内部类型作为公共 API

暴露内部 `QSpinBox *` 会让调用方依赖实现。应暴露领域属性、命令和信号。

## 19. API 速查

| API | 作用 |
|---|---|
| `Q_PROPERTY` | 把状态纳入 Qt 元对象属性系统 |
| `sizeHint()` | 建议首选尺寸 |
| `minimumSizeHint()` | 建议最小可用尺寸 |
| `setSizePolicy()` | 声明布局伸缩意愿 |
| `update()` | 安排重绘 |
| `updateGeometry()` | 通知布局尺寸建议变化 |
| `contentsRect()` | 排除 contents margins 后的绘制区域 |
| `QStyleOption::initFrom()` | 从 Widget 初始化 Style 状态 |
| `QStyle::drawPrimitive()` | 让当前 Style 绘制标准元素 |
| `QStyle::visualRect()` | 将逻辑矩形映射到 LTR/RTL |
| `setAccessibleName()` | 提供可访问名称 |
| `QAccessible::updateAccessibility()` | 通知辅助技术状态变化 |
| `setFocusProxy()` | 把复合控件焦点转给内部编辑器 |
| Designer Promote | 在 `.ui` 中使用项目内自定义类 |

## 20. 自测题

1. 哪类自定义界面优先做成复合控件？
2. 为什么 `LevelControl` 需要 `Q_OBJECT`？
3. `sizeHint()` 与 `QSizePolicy` 各自解决什么问题？
4. 哪类状态变化需要调用 `updateGeometry()`？
5. Setter 为什么应先比较旧值和新值？
6. `paintEvent()` 为什么不应发送业务信号？
7. 如何让水平控件适应 RTL？
8. `accessibleName` 是否足以完整描述一个自绘滑块？
9. Promote 和 Designer 插件分别适合什么情况？
10. 为什么外部不应直接依赖复合控件内部的 `QSpinBox *`？

## 21. 参考答案

1. 由现有输入框、按钮、标签等标准控件组成的界面片段，优先组合以复用成熟行为。
2. 它声明了自己的信号和 Qt 属性，需要 moc 生成相应元对象代码。
3. `sizeHint()` 给出首选尺寸；SizePolicy 描述布局有多余或不足空间时控件如何伸缩。
4. 会改变 sizeHint/minimumSizeHint 的变化，例如字体、内容或显示模式变化。
5. 避免重复通知、冗余重绘和属性绑定循环。
6. 绘制可能因遮挡、缩放和系统请求多次发生，不代表业务状态变化；副作用会造成不稳定循环。
7. 使用 `layoutDirection()` 配合 `QStyle::visualRect()`，并同时调整键盘和鼠标方向语义。
8. 不足。复杂自绘控件还需要正确角色、状态和值接口，通常要实现/注册 QAccessible 接口。
9. 项目内使用、无需实时设计支持时用 Promote；要进入 Widget Box 并提供完整设计期能力时写插件。
10. 那会泄漏实现细节，使以后更换内部控件时破坏调用方；应公开稳定的业务属性和信号。

## 22. 本篇结论

一个成熟自定义 Widget 的状态链应该始终清晰：

```text
鼠标 / 键盘 / 外部调用
          ↓
统一 Setter 校验并维护不变量
          ↓
更新内部状态
      ↙          ↘
   update()     change signal
      ↓              ↓
 paintEvent()    外部观察者同步
```

若首选尺寸也变化，再调用 `updateGeometry()`；若辅助技术需要知道状态变化，再发送相应可访问事件。优先组合标准控件，完全自绘时主动承担样式、键盘、RTL、高 DPI 和可访问性契约，这才是从“能显示”走到“可复用”的关键。
