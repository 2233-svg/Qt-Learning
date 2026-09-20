# Qt QStyleOptionToolButton 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStyleOptionToolButton>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex -> QStyleOptionToolButton`  
> 定位：把工具栏按钮的图标、文字、箭头、菜单提示和子控件状态交给 `QStyle` 的绘制数据

## 1. 它解决的是工具按钮的复杂外观

`QStyleOptionToolButton` 不是 `QToolButton`。它不保存 `QAction`，不弹出 `QMenu`，也没有点击信号；它只是一帧绘制时提供给样式系统的参数。

工具按钮之所以需要专用的 option，是因为它比普通按钮多出几种复杂结构：

```text
普通工具按钮        [图标]
带文字工具按钮      [图标] 保存
箭头工具按钮        [向下箭头]
带菜单提示按钮      [图标][v]
分离菜单按钮        [主操作区域][v]
```

`QStyleOptionToolButton` 继承自 `QStyleOptionComplex`，除了自身字段，还继承了 `subControls`、`activeSubControls` 等复杂控件状态。它们让 style 区分主按钮区域和菜单箭头区域，正确处理悬停、按下、命中测试与分隔线。

使用它的典型场景：

- 重写 `QToolButton` 子类的绘制，仍保留平台工具栏风格；
- 在 `QProxyStyle` 中只改变工具按钮的菜单箭头、图标间距或文本布局；
- 通过 `subControlRect()` 取得 `SC_ToolButton`、`SC_ToolButtonMenu` 的准确区域。

## 2. `popupMode` 和 option feature 的分工

真实的菜单行为由 `QToolButton` 的 `menu` 与 `popupMode` 决定；option 的 `features` 则把结果翻译成绘制提示。

| `QToolButton::popupMode` | 用户操作 | style 需要表现的重点 |
| --- | --- | --- |
| `DelayedPopup` | 短按执行主操作，长按后显示菜单 | 菜单存在，并体现延迟弹出语义 |
| `MenuButtonPopup` | 点主区域执行主操作，点箭头区域显示菜单 | 主区域和菜单子控件需明显分离 |
| `InstantPopup` | 按下立即显示菜单，主操作不触发 | 把按钮呈现为菜单入口 |

`features` 中的 `Menu`、`MenuButtonPopup`、`PopupDelay`、`HasMenu` 是样式提示，并不是一组让业务代码直接选择行为的“popup mode 枚举”。配置行为时调用 `QToolButton::setMenu()` 和 `setPopupMode()`；绘制时从 `initStyleOption()` 取得已计算好的 feature。

另一个容易混淆点是所有权：`QToolButton::setMenu()` 不转移菜单所有权。这个事实不存储在 option 中；option 只告诉 style 现在应不应该画菜单提示。

## 3. 标准用法：让 style 负责几何与基础绘制

工具栏中按钮尺寸会随 style、DPI、文字模式和主窗口设置改变。不要假设最右侧固定 16 像素永远是菜单箭头。

```cpp
void HistoryToolButton::paintEvent(QPaintEvent *)
{
    QStyleOptionToolButton option;
    initStyleOption(&option);

    QStylePainter painter(this);
    painter.drawComplexControl(QStyle::CC_ToolButton, option);

    const QRect menuRect = style()->subControlRect(
        QStyle::CC_ToolButton,
        &option,
        QStyle::SC_ToolButtonMenu,
        this);

    if (menuRect.isValid())
        drawMenuAccent(painter, menuRect);
}
```

`initStyleOption()` 会把实际 `QToolButton` 的 `QAction` 文本、图标、箭头类型、菜单模式、字体、显示方式及继承的调色板/状态填到 option。手工只填 `icon` 与 `text`，很容易漏掉 RTL 下菜单箭头的位置、auto-raise 悬停反馈、禁用图标模式和当前按下的子区域。

## 4. `ToolButtonFeature` 如何读

### 4.1 箭头、菜单和延迟不是一回事

| feature | 表示什么 | 使用时的边界 |
| --- | --- | --- |
| `Arrow` | 按钮内容是一个方向箭头 | 只有设置了它，`arrowType` 才参与绘制 |
| `Menu` | 按钮具备菜单相关特性 | `MenuButtonPopup` 是它的别名，用于表达分离式菜单按钮 |
| `PopupDelay` | 菜单不是立刻弹出，而有 style 决定的延迟 | 它不负责启动定时器 |
| `HasMenu` | 当前按钮应显示弹出菜单提示 | 真实菜单对象仍由 `QToolButton` 管理 |

`MenuButtonPopup = Menu` 是同一个位值的别名。代码里若想表达“分离菜单按钮”这个语义，使用 `MenuButtonPopup` 可读性更好；它不会额外增加一个独立 bit。

### 4.2 `Arrow` 与图标的优先关系

当 `features` 包含 `Arrow` 时，style 根据 `arrowType` 绘制方向箭头，默认方向是 `Qt::DownArrow`。它与 `icon` 是两条不同的内容输入，不应指望“给 icon 画一个箭头”自动等价于设置 `Arrow`：平台 style 可能会为真正的箭头按钮采用不同的尺寸、留白和按下效果。

### 4.3 `toolButtonStyle` 决定文字字段是否生效

`toolButtonStyle` 常见取值如下：

| 显示方式 | `text` 和 `font` 是否参与绘制 |
| --- | --- |
| `Qt::ToolButtonIconOnly` | 通常不使用 |
| `Qt::ToolButtonTextOnly` | 使用 |
| `Qt::ToolButtonTextBesideIcon` | 使用 |
| `Qt::ToolButtonTextUnderIcon` | 使用 |

这也是 `font` 不直接复用基类 `fontMetrics` 的原因：它是工具按钮文字排版的明确输入，而基类的字体度量还服务通用 style 计算。

## 5. 每个公开字段的真实职责

### 5.1 内容与尺寸

- `icon`：当前绘制的图标；空图标表示没有图标。
- `iconSize`：图标目标尺寸；默认 `QSize(-1, -1)` 是无效尺寸，允许 style 选择大小。
- `text`：工具按钮标签；仅在文字相关 `toolButtonStyle` 下有实际意义。
- `font`：用于文字相关显示方式；默认使用应用默认字体。

修改这些字段只改变随后传给 `drawComplexControl()` 的本次绘制，不会反向调用真实控件的 `setIcon()`、`setText()` 或 `setFont()`。

### 5.2 位置和显示方式

- `pos`：工具按钮位置数据，默认是 `(0, 0)`。
- `toolButtonStyle`：图标和文字怎样组合，默认 `Qt::ToolButtonIconOnly`。

不要拿 `pos` 替代 `option.rect` 做内部布局。控件尺寸与可绘制区域来自继承的 `rect`，菜单箭头和主区域位置应由 `subControlRect()` 计算；`pos` 是 option 的附加位置数据，不是通用的子控件几何 API。

## 6. QProxyStyle 中安全处理菜单区域

`drawComplexControl()` 接收基类指针，必须先确认 complex control，再进行安全转换：

```cpp
void ToolbarStyle::drawComplexControl(
    QStyle::ComplexControl control,
    const QStyleOptionComplex *option,
    QPainter *painter,
    const QWidget *widget) const
{
    if (control == QStyle::CC_ToolButton) {
        const auto *toolButton =
            qstyleoption_cast<const QStyleOptionToolButton *>(option);

        if (toolButton && toolButton->features.testFlag(
                              QStyleOptionToolButton::MenuButtonPopup)) {
            const QRect menuRect = subControlRect(
                QStyle::CC_ToolButton, toolButton,
                QStyle::SC_ToolButtonMenu, widget);
            drawSplitLine(menuRect, painter);
        }
    }

    QProxyStyle::drawComplexControl(control, option, painter, widget);
}
```

`Type = SO_ToolButton` 与 `Version = 1` 是 `qstyleoption_cast()` 判断数据布局的标签。不要将 `QStyleOptionComplex *` 直接 `static_cast` 成工具按钮 option；样式函数也会收到组合框、滚动条、滑块等其他复杂控件。

## 7. 常见错误

### 7.1 把 `HasMenu` 当作真的有可弹出菜单

症状：手工设置 `features |= HasMenu` 后，界面有箭头但点击没有菜单。

原因：option 仅负责画面，既不创建 `QMenu` 也不连接触发逻辑。

处理：给真实 `QToolButton` 设置 `QMenu` 与 `popupMode`，再让 `initStyleOption()` 生成绘制提示。

### 7.2 用固定坐标判断是否点击菜单箭头

症状：切换 style、高 DPI 或 RTL 后，点击区域错位。

原因：菜单子控件宽度和位置由当前 style 决定。

处理：使用 `hitTestComplexControl()` 或 `subControlRect(QStyle::SC_ToolButtonMenu)`。

### 7.3 把工具按钮按普通按钮绘制

症状：分离菜单按钮没有分隔线，按钮文字模式不正确。

原因：使用了 `CE_PushButton` 或 `QStyleOptionButton`，丢失复杂控件的子区域和 `ToolButtonFeature`。

处理：使用 `QStyle::CC_ToolButton` 与 `QStyleOptionToolButton`。

## API 速查表
以下是 Qt 6.11.1 类文档中 `QStyleOptionToolButton` 直接声明的类型、构造函数和公开字段。`QStyleOptionComplex` 继承来的 `subControls`、`activeSubControls` 与 `QStyleOption` 通用状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_ToolButton` | 标识这是工具按钮的 style option。 | 供 style 系统和 `qstyleoption_cast()` 进行类型识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识该数据结构版本。 | 普通自定义 style 不必手动比较。 |
| 枚举值 | `ToolButtonFeature::None = 0x00` | 表示普通工具按钮，没有额外 feature。 | 是默认值。 |
| 枚举值 | `ToolButtonFeature::Arrow = 0x01` | 表示按钮内容是方向箭头。 | 只有包含此位时才使用 `arrowType`。 |
| 枚举值 | `ToolButtonFeature::Menu = 0x04` | 表示按钮有菜单相关特性。 | `MenuButtonPopup` 是该值的语义别名。 |
| 枚举值 | `ToolButtonFeature::MenuButtonPopup = Menu` | 表示分离主操作与菜单箭头区域的菜单按钮。 | 是 `Menu` 的别名，不是额外独立 bit。 |
| 枚举值 | `ToolButtonFeature::PopupDelay = 0x08` | 表示菜单显示有延迟。 | 真实延迟时长由 `QStyle::SH_ToolButton_PopupDelay` 决定。 |
| 枚举值 | `ToolButtonFeature::HasMenu = 0x10` | 表示按钮带弹出菜单提示。 | 仅说明绘制状态，不能替代设置真实 `QMenu`。 |
| 标志类型 | `ToolButtonFeatures` | 保存多个 `ToolButtonFeature` 的按位组合。 | 用 `testFlag()` 查询特性，不要把组合值当作单一枚举。 |
| 构造 | `QStyleOptionToolButton()` | 创建并以默认值初始化 option。 | 默认无 feature、向下箭头、仅显示图标。 |
| 构造 | `QStyleOptionToolButton(const QStyleOptionToolButton &other)` | 复制一份工具按钮绘制状态。 | 是值复制，不拥有 `QAction`、`QMenu` 或控件。 |
| 公开字段 | `Qt::ArrowType arrowType` | 指定箭头工具按钮的方向。 | 默认 `Qt::DownArrow`；仅 `Arrow` feature 时使用。 |
| 公开字段 | `ToolButtonFeatures features` | 保存菜单、箭头、延迟等绘制特性。 | 应由 `initStyleOption()` 从真实控件生成。 |
| 公开字段 | `QFont font` | 保存工具按钮文字所用字体。 | 仅文字相关显示模式下使用。 |
| 公开字段 | `QIcon icon` | 保存当前绘制图标。 | 默认空图标；修改不改变真实控件图标。 |
| 公开字段 | `QSize iconSize` | 保存图标目标尺寸。 | 默认无效尺寸，style 可自行选取合适尺寸。 |
| 公开字段 | `QPoint pos` | 保存工具按钮位置数据。 | 默认 `(0, 0)`；子控件几何应使用 `subControlRect()`。 |
| 公开字段 | `QString text` | 保存工具按钮文本。 | 仅文字相关 `toolButtonStyle` 下使用。 |
| 公开字段 | `Qt::ToolButtonStyle toolButtonStyle` | 指定图标与文字的组合方式。 | 默认 `Qt::ToolButtonIconOnly`。 |

## 9. 一句话总结

`QStyleOptionToolButton` 描述的是工具按钮这一帧的复杂外观，而不管理菜单行为本身：让 `QToolButton` 配置真实动作和菜单，让 `initStyleOption()` 填状态，再让 `QStyle` 根据 feature 和子控件区域完成平台一致的绘制。
