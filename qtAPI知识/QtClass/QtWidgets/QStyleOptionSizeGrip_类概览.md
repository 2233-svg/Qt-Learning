# Qt QStyleOptionSizeGrip 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStyleOptionSizeGrip>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex -> QStyleOptionSizeGrip`  
> 定位：把窗口缩放手柄所在的角传给 `QStyle`，用于绘制正确朝向的 resize grip

## 1. 它不是可拖动手柄，真正处理鼠标的是 QSizeGrip

`QStyleOptionSizeGrip` 只是绘制数据，唯一新增字段是 `corner`。它不会捕获鼠标、计算新窗口尺寸或改变任何 widget 的大小。

真正的交互控件是 `QSizeGrip`：

```text
QSizeGrip
  ├─ mousePressEvent()：开始一次缩放操作
  ├─ mouseMoveEvent()：调整顶级窗口或 Qt::SubWindow
  └─ paintEvent()
       └─ QStyleOptionSizeGrip
            └─ QStyle::drawControl(CE_SizeGrip, ...)
```

也就是说：

- `QSizeGrip` 解决“用户拖拽角落调整窗口大小”；
- `QStyleOptionSizeGrip` 解决“当前 style 应把这个 grip 画成朝哪个角的纹理”。

普通应用通常不必直接使用它。`QStatusBar` 已经内置 size grip；`QDialog` 可直接调用 `setSizeGripEnabled(true)`。只有自定义 `QSizeGrip` 或 style 时才需要创建本类。

## 2. 真实使用场景：哪些窗口会被它调整

Qt 6.11.1 文档说明，`QSizeGrip` 可以放在任意 widget 树中，用户拖它时会缩放：

- 包含它的顶级窗口；
- 或具有 `Qt::SubWindow` 标志的窗口。

最常见的布局是右下角：

```cpp
auto *dialog = new QDialog(this);
dialog->setSizeGripEnabled(true);
```

或手工将 `QSizeGrip` 放入底部布局：

```cpp
auto *layout = new QHBoxLayout(bottomBar);
layout->addStretch();
layout->addWidget(new QSizeGrip(bottomBar));
```

第二段代码的前提是父层级最终能找到可调整大小的顶级窗口或子窗口；把 size grip 放在一个不可缩放窗口中，不会 magically 赋予它缩放能力。

平台也会影响可见性：部分平台上，当窗口最大化或全屏时，`QSizeGrip` 会自动隐藏；macOS 上主窗口的 size grip 通常不显示，`QMdiSubWindow` 是重要例外。这是控件和平台 style 的行为，不是 `corner` 字段能强行绕开的规则。

## 3. 为什么 `corner` 是唯一新增字段

缩放手柄的经典视觉是斜向点阵或短线。它在不同角落应有不同朝向：

```text
右下角： \\\
左下角： ///
右上角： ///
左上角： \\\
```

`corner` 的类型是 `Qt::Corner`：

| 取值 | 表示的角 |
| --- | --- |
| `Qt::TopLeftCorner` | 左上角 |
| `Qt::TopRightCorner` | 右上角 |
| `Qt::BottomLeftCorner` | 左下角 |
| `Qt::BottomRightCorner` | 右下角 |

它是绘制方向与位置语义的输入，而不是“把控件自动移动到这个角”的命令。控件实际放在哪，由布局、父 widget 和 geometry 决定；`corner` 需要与实际位置一致，否则用户看到的纹理方向会与可拖动边缘相反，体验很别扭。

## 4. 标准绘制方法：用 CE_SizeGrip，而不是自己画几条线

```cpp
void CustomSizeGrip::paintEvent(QPaintEvent *)
{
    QStyleOptionSizeGrip option;
    option.initFrom(this);
    option.corner = Qt::BottomRightCorner;

    QStylePainter painter(this);
    painter.drawControl(QStyle::CE_SizeGrip, option);
}
```

这会将纹理、调色板、启用状态、高 DPI 与当前 style 交给 Qt 处理。若自定义 `QSizeGrip` 子类，优先参考/保留基类的事件处理逻辑；仅替换绘制时，也应让 style 画基础握柄后再叠加装饰。

`option.initFrom(this)` 来自 `QStyleOption`，用于填充 palette、rect、state、direction 等通用绘制上下文。仅创建对象然后设 `corner`，通常会得到缺少正确尺寸、主题或禁用态信息的 option。

手柄大小也不是固定像素。style 可通过 `QStyle::pixelMetric(QStyle::PM_SizeGripSize, ...)` 提供当前主题下的推荐尺寸。

## 5. `corner` 与 RTL、布局位置的关系

`corner` 是物理角：左上、右上、左下、右下。它不是“末尾角”的抽象概念。

如果界面需要在 RTL 下将 grip 从右下移到左下，那么布局和 geometry 应实际移动它，同时 option 也应同步改为：

```cpp
option.corner = Qt::BottomLeftCorner;
```

只让布局移动却不改 `corner`，会导致 style 仍按右下角方向绘制。反过来，只改 `corner` 也不会移动控件。

## 6. 自定义 style 时的安全读取

`CE_SizeGrip` 的 option 参数类型是 `QStyleOption *`。自定义 style 仍应使用 `qstyleoption_cast()`：

```cpp
void GripStyle::drawControl(QStyle::ControlElement element,
                            const QStyleOption *option,
                            QPainter *painter,
                            const QWidget *widget) const
{
    if (element == QStyle::CE_SizeGrip) {
        const auto *grip =
            qstyleoption_cast<const QStyleOptionSizeGrip *>(option);

        if (grip && grip->corner == Qt::BottomLeftCorner) {
            drawLeftHandGrip(*grip, painter);
            return;
        }
    }

    QProxyStyle::drawControl(element, option, painter, widget);
}
```

`Type = SO_SizeGrip` 与 `Version = 1` 是 `qstyleoption_cast()` 的识别依据。不要将所有 `QStyleOption *` 强制转换成 size grip option。

### 6.1 Qt 6.11.1 离线文档的笔误

该类页的详细说明错误地写成了 `QStyleOptionButton contains...`，枚举说明的描述中也错误提到 `SO_TabBarBase`。实际类型是 `QStyleOptionSizeGrip`，安装头文件定义 `Type = SO_SizeGrip`、`Version = 1`；代码应以头文件为准。

## 7. 常见错误

### 7.1 以为设置 `corner` 就会移动控件

症状：纹理方向变了，但 grip 仍在原位置。

原因：`corner` 是 style 输入，不是布局命令。

处理：使用 layout 或 `setGeometry()` 放置 `QSizeGrip`，再使 option 的 `corner` 与实际角一致。

### 7.2 主窗口已有状态栏又额外塞一个 grip

症状：底部出现两个缩放手柄，或布局有冗余空隙。

原因：`QStatusBar` 已经使用 size grip。

处理：先确认状态栏是否已提供它；需要关闭时使用状态栏相应配置，而不是叠加一个控件。

### 7.3 最大化时强行依赖 grip 作为唯一缩放入口

症状：最大化或全屏后 grip 自动隐藏，交互逻辑没有替代路径。

原因：平台上这是正常行为，窗口本身也通常不应直接缩放。

处理：把 grip 视为普通窗口状态下的辅助交互，不要把核心命令绑定在它的可见性上。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionSizeGrip` 直接声明的类型、构造函数和公开字段。继承自 `QStyleOptionComplex` 与 `QStyleOption` 的通用绘制状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_SizeGrip` | 标识这是 size grip 的 style option。 | 供 `qstyleoption_cast()` 与样式系统识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构版本。 | 普通 style 代码不需手动检查版本。 |
| 构造 | `QStyleOptionSizeGrip()` | 创建一份 size grip 绘制数据。 | 随后应初始化通用绘制上下文并设定实际 `corner`。 |
| 构造 | `QStyleOptionSizeGrip(const QStyleOptionSizeGrip &other)` | 复制另一份 size grip 绘制状态。 | 是值复制，不拥有或创建 `QSizeGrip`。 |
| 公开字段 | `Qt::Corner corner` | 表示 size grip 所在的物理角。 | 影响 style 绘制朝向；不会移动控件或执行缩放。 |

## 9. 一句话总结

`QStyleOptionSizeGrip` 只告诉 style “这个缩放握柄在哪个角”，真正的拖动缩放由 `QSizeGrip` 处理；让布局、实际 geometry 和 `corner` 保持一致，再通过 `CE_SizeGrip` 交给当前 style 绘制，才能在不同主题和布局方向下保持正确。
