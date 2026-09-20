# Qt QStyleOptionTabBarBase 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionTabBarBase>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionTabBarBase`  
> 常见协作者：`QTabBar`、`QTabWidget`、`QStyle`

## 1. 它解决什么问题

tab bar 不只有一排单独的 tab。tab 的底边通常会覆盖一条连续的 base/frame：未选中 tab 贴着这条线，选中 tab 在自己的位置打断或跨过它，视觉上才像“当前页面连在内容区上”。

`QStyleOptionTabBarBase` 描述的正是这条 tab bar base。它把 tab bar 的形状、整排 tab 的矩形、选中 tab 的矩形和文档模式交给 `QStyle`，让当前平台主题决定底线、缺口、重叠和圆角。

```text
独立 QTabBar
  ├─ 逐项 tab：QStyleOptionTab
  │    -> CE_TabBarTab / CE_TabBarTabShape / CE_TabBarTabLabel
  └─ 整体底座：QStyleOptionTabBarBase
       -> PE_FrameTabBarBase
```

它不是 tab bar 控件，不持有 tab，也不会切换当前页。它是绘制“整条底座”的一次性参数对象。

## 2. 最容易混淆的边界：独立 `QTabBar` 与 `QTabWidget`

Qt 文档明确指出，这个 base 仅为**不属于 `QTabWidget` 的独立 `QTabBar`**绘制。`QTabWidget` 自己管理 tab bar 与页面 frame 的连接，相关整体 frame 参数由 `QStyleOptionTabWidgetFrame` 描述。

| 使用场景 | 主要 option | 绘制职责 |
| --- | --- | --- |
| 独立 `QTabBar`，例如编辑器顶部标签栏 | `QStyleOptionTabBarBase` | 绘制 tab bar 下方/旁边的 base。 |
| 单个 tab 的外观 | `QStyleOptionTab` | 绘制标签形状、标题、图标、关闭按钮区域。 |
| `QTabWidget` 的内容区 frame | `QStyleOptionTabWidgetFrame` | 绘制 tab 与页面容器之间的 frame。 |

对普通 `QTabBar`，使用 `setDrawBase(true/false)` 决定是否绘制 base；不要自己创建 `QStyleOptionTabBarBase` 来替代 `QTabWidget` 的 frame 绘制。

## 3. 构建与正常使用

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 创建带 base 的独立 tab bar

```cpp
#include <QTabBar>

auto *tabs = new QTabBar;
tabs->addTab("编辑器");
tabs->addTab("终端");
tabs->addTab("问题");
tabs->setDrawBase(true);
tabs->setDocumentMode(true);
```

这里调用的是 `QTabBar` 的公开 API。Qt 会在绘制过程中计算 base 的矩形、当前选中 tab 的矩形等信息，并构造 `QStyleOptionTabBarBase`。业务代码无需也不应缓存 option。

## 4. 三个矩形分别表示什么

本类同时出现 `rect`、`tabBarRect` 与 `selectedTabRect`，它们的职责不同：

| 矩形 | 来源 | 表示什么 |
| --- | --- | --- |
| 继承的 `rect` | 当前 primitive 的绘制区域。 | style 应在这里画 `PE_FrameTabBarBase`。 |
| `tabBarRect` | tab bar 中所有 tab 所覆盖的区域。 | 用于知道整排 tab 在 base 中占据哪里。 |
| `selectedTabRect` | 当前选中 tab 的区域。 | 必定位于 `tabBarRect` 内，用于在 base 上留出/调整与选中项的连接。 |

```text
rect：            ───────────────────── base 的完整绘制范围 ─────────────────────
tabBarRect：          [ tab 0 ][ tab 1 ][ tab 2 ]  整排标签所在区域
selectedTabRect：              [ tab 1 ]            当前选中标签
```

`selectedTabRect` 默认是空矩形；在没有有效当前 tab、初始化不完整或测试性手工构造 option 时，它可能无效。style 代码在据此切割线条前应先检查 `isNull()` 或有效尺寸。

不要把 `tabBarRect` 当成单个 tab 的几何，也不要用 `selectedTabRect` 推断哪一个 index 被选中。前者是整体范围，后者只提供当前选中区域的几何。

## 5. `shape` 与 `documentMode`

### 5.1 `shape`

`shape` 是 `QTabBar::Shape`，例如 `RoundedNorth`、`RoundedSouth`、左侧或右侧 tab bar 的变体。它告诉 style base 应该位于 tab 的哪一侧，以及如何处理方向。

默认值为 `QTabBar::RoundedNorth`。实际设置应通过：

```cpp
tabs->setShape(QTabBar::RoundedSouth);
```

而不是修改一次性 option。

### 5.2 `documentMode`

`documentMode` 是样式提示，表示 tab bar 应以更适合主窗口文档标签的形式绘制。它与 `QStyleOptionTab::documentMode` 呼应，但本类关心的是**整条 base**的外观和与选中 tab 的衔接。

它不会：

- 自动使 tab 可关闭。
- 处理文件未保存状态。
- 创建页面或实现 tab 拖动。

这些行为仍由 `QTabBar`、`QTabWidget` 和业务代码负责。

## 6. 在自定义 style 中绘制 base

tab bar base 是 primitive，不是 control。使用 `QStyle::PE_FrameTabBarBase`：

```cpp
#include <QProxyStyle>
#include <QStyleOptionTabBarBase>

class TabBaseStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawPrimitive(PrimitiveElement element,
                       const QStyleOption *option,
                       QPainter *painter,
                       const QWidget *widget = nullptr) const override
    {
        if (element == PE_FrameTabBarBase) {
            if (const auto *base =
                    qstyleoption_cast<const QStyleOptionTabBarBase *>(option)) {
                if (!base->selectedTabRect.isNull()) {
                    // 可依据 selectedTabRect 调整底线在选中 tab 附近的绘制。
                }
            }
        }

        QProxyStyle::drawPrimitive(element, option, painter, widget);
    }
};
```

不要手工在每个 tab 的 `paintEvent()` 里画整条 base。base 是整个 tab bar 的共享元素；把它混入单项 tab 绘制会导致重叠、边线加粗或无法正确在选中项处留缺口。

## 7. 生命周期、类型与版本勘误

`QStyleOptionTabBarBase` 是值类型：

- 不继承 `QObject`，没有父对象。
- 不拥有 `QTabBar`、`QTabWidget`、`QPainter` 或 tab。
- 在一次绘制中创建/传递，不能把它的指针保存到事件循环之后。
- 复制构造只复制绘制数据。

| 常量 | Qt 6.11.1 头文件值 | 作用 |
| --- | --- | --- |
| `QStyleOptionTabBarBase::Type` | `QStyleOption::SO_TabBarBase` | 标识这是 tab bar base option。 |
| `QStyleOptionTabBarBase::Version` | `1` | 标识本数据布局版本。 |

离线类文档的 version 表中，值列为 `1`，说明列却误写为 `2`；安装头文件声明 `Version = 1`，本页以头文件为准。

## 8. 常见误区与排查

### 8.1 “我关掉 `drawBase` 后，为什么内容区边框也变了”

`drawBase` 控制独立 tab bar 的 base；视觉上它可能与相邻内容区 frame 连在一起。若使用 `QTabWidget`，应同时检查其 frame/样式设置，而不是只根据 tab bar 这一层判断。

### 8.2 “选中 tab 下方仍然有一条线”

自定义 style 只画了 `rect` 的整条直线，没有依据 `selectedTabRect` 处理与选中 tab 的衔接。应让基础 style 绘制，或按 `shape` 和选中矩形正确裁剪。

### 8.3 “我用 `tabBarRect` 来画单个 tab，按钮和标题错位”

`tabBarRect` 覆盖整排 tab。单个 tab 的内容、按钮尺寸和相邻状态属于 `QStyleOptionTab`。

### 8.4 “我在 QTabWidget 里没看到 `PE_FrameTabBarBase`”

这是预期行为。该 primitive 主要服务独立 `QTabBar`；`QTabWidget` 的页面 frame 使用不同 option 与绘制路径。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionTabBarBase()` | 创建并以默认值初始化独立 tab bar 底座的绘制参数。 | 默认矩形可能无效；真实数据通常由 `QTabBar` 的绘制流程填充。 |
| 构造 | `QStyleOptionTabBarBase(const QStyleOptionTabBarBase &other)` | 创建另一个 tab bar base option 的值副本。 | 复制绘制字段，不拥有 tab bar、tab 或 painter。 |
| 类型常量 | `StyleOptionType::Type` | 提供值为 `SO_TabBarBase` 的运行时类型标识。 | style 接收基类指针时使用 `qstyleoption_cast()`。 |
| 类型常量 | `StyleOptionVersion::Version` | 表示底座 option 的数据布局版本，Qt 6.11.1 中为 `1`。 | 以安装头文件为准；版本用于兼容识别。 |
| 公共字段 | `QTabBar::Shape shape` | 提供 tab bar 的方向和轮廓形状。 | 决定底座位于 tab 的哪一侧；真实配置通过 `QTabBar::setShape()` 完成。 |
| 公共字段 | `QRect tabBarRect` | 提供整排 tab 覆盖的整体矩形。 | 它不是某个单独 tab 的矩形，也不是 base 的完整绘制区域。 |
| 公共字段 | `QRect selectedTabRect` | 提供当前选中 tab 的矩形。 | style 可据此处理底座线条的连接或缺口；无有效当前 tab 时可能为空。 |
| 公共字段 | `bool documentMode` | 提供 tab bar 是否采用文档式外观的样式提示。 | 只影响 base 的绘制风格，不会让 tab 可关闭或实现文档行为。 |
| 继承字段 | `QStyleOption::rect` | 指定 `PE_FrameTabBarBase` 当前应绘制的完整区域。 | 与 `tabBarRect` 的“整排 tab 区域”语义不同。 |
| 行为配置 | `QTabBar::setDrawBase(bool)` | 控制独立 `QTabBar` 是否绘制共享 base。 | 普通业务代码应配置它，不应通过手工 option 替代控件绘制流程。 |
| 绘制 | `QStyle::drawPrimitive(QStyle::PE_FrameTabBarBase, ...)` | 使用当前 style 绘制整条 tab bar 底座。 | 这是 primitive 绘制入口，不是单个 tab 的 `CE_TabBarTab`。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionTabBarBase *>(option)` | 从基类 option 安全识别 tab bar base option。 | 失败返回空指针；应保留基础 style 的降级绘制路径。 |

---

### 一句话总结

`QStyleOptionTabBarBase` 描述的是独立 `QTabBar` 的共享底座，而非一项 tab：`rect` 是 base 的画布，`tabBarRect` 表示整排标签，`selectedTabRect` 告诉 style 选中项在哪里打断或连接底线；普通代码用 `setDrawBase()`，自定义 style 才处理 `PE_FrameTabBarBase`。
