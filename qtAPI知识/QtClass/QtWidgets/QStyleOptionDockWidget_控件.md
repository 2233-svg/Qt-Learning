# Qt QStyleOptionDockWidget 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionDockWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionDockWidget`  
> 常见协作者：`QDockWidget`、`QMainWindow`、`QStyle`

## 1. 它解决什么问题

`QDockWidget` 是主窗口中的工具面板容器，例如 IDE 的“项目”“输出”“属性”区域。用户能否关闭、拖动、浮动它，以及标题栏是横向还是竖向，都会影响标题栏应显示哪些按钮、文字应放在哪里。

`QStyleOptionDockWidget` 是 `QDockWidget` 交给 `QStyle` 的绘制数据包，用于画 dock 标题栏等图形元素。它不是 dock 控件本身，不继承 `QWidget`，不能 `show()`，也不管理停靠布局、拖动或关闭行为。

```text
QMainWindow
  └─ QDockWidget
       ├─ features：允许关闭、移动、浮动、竖向标题栏
       ├─ windowTitle：标题文字
       └─ initStyleOption()
            └─ QStyleOptionDockWidget
                 └─ QStyle::CE_DockWidgetTitle
```

这种分层让一个 style 能根据当前主题、文字方向与 dock 功能集，统一决定标题栏、浮动按钮和关闭按钮的外观。

## 2. 它不解决什么

下列需求都应操作 `QDockWidget` 或 `QMainWindow`，而不是手写 option 字段：

| 需求 | 正确入口 | 原因 |
| --- | --- | --- |
| 添加工具面板 | `QMainWindow::addDockWidget()` | 由主窗口负责停靠区域布局。 |
| 是否允许关闭/拖动/浮动 | `QDockWidget::setFeatures()` | option 只反映本次绘制状态。 |
| 设置工具面板内容 | `QDockWidget::setWidget()` | 内容控件由 dock 管理。 |
| 设置标题 | `QDockWidget::setWindowTitle()` | option 的 `title` 是绘制快照。 |
| 使用自定义标题栏控件 | `QDockWidget::setTitleBarWidget()` | 会改变标准标题栏绘制路径。 |

普通项目很少直接构造 `QStyleOptionDockWidget`；它主要用于自定义 `QDockWidget` 子类或实现 `QStyle` / `QProxyStyle`。

## 3. 构建与协作流程

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 正常创建一个可停靠面板

业务代码操作的是 `QDockWidget`，而非 style option：

```cpp
#include <QDockWidget>
#include <QListWidget>
#include <QMainWindow>

auto *dock = new QDockWidget("项目", mainWindow);
dock->setObjectName("projectDock");
dock->setWidget(new QListWidget(dock));
dock->setFeatures(QDockWidget::DockWidgetClosable
                  | QDockWidget::DockWidgetMovable
                  | QDockWidget::DockWidgetFloatable);

mainWindow->addDockWidget(Qt::LeftDockWidgetArea, dock);
```

`QDockWidget` 会在需要时初始化 `QStyleOptionDockWidget`。给内容控件调用 `setLayout()` 或在构造中建立布局后再传入 `setWidget()`；不要在 dock 外壳上强行设置固定尺寸，因为停靠和浮动时 frame、标题栏和可用尺寸都会变化。

### 3.3 在 style 中读取标题栏状态

`QStyle::CE_DockWidgetTitle` 的 option 是 `QStyleOptionDockWidget`。代理 style 应安全转换，并尽量保留基础 style 绘制：

```cpp
#include <QProxyStyle>
#include <QStyleOptionDockWidget>

class DockTitleStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_DockWidgetTitle) {
            if (const auto *dock =
                    qstyleoption_cast<const QStyleOptionDockWidget *>(option)) {
                if (dock->verticalTitleBar) {
                    // 竖向标题栏需要按其方向处理附加装饰的几何。
                }
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

不要在 `drawControl()` 内调用 `setFeatures()`、`close()` 或 `setFloating()`。绘制函数应读取快照并画图，不能承担 dock 的状态迁移。

## 4. 标题与三种能力状态

### 4.1 `title`

`title` 是本次绘制的 dock 标题，通常来自 `QDockWidget::windowTitle()`。默认值为空字符串。

它不是可编辑的业务源。若要改标题，调用：

```cpp
dock->setWindowTitle("调试输出");
```

而不是在 option 上修改 `title`；下次重绘时 `QDockWidget` 会再次用自身状态重建 option。

### 4.2 `closable`、`movable`、`floatable`

这三个布尔值分别反映 `QDockWidget::features()` 中的功能位：

| option 字段 | 对应 `QDockWidget` feature | 对 style 的含义 |
| --- | --- | --- |
| `closable` | `DockWidgetClosable` | 是否应显示/启用关闭相关 UI。 |
| `movable` | `DockWidgetMovable` | 用户是否可在 dock 区域中拖动、重新停靠。 |
| `floatable` | `DockWidgetFloatable` | 用户是否可将其脱离主窗口成为浮动窗口。 |

它们描述的是**允许的交互能力**，不是当前已经发生的状态。例如 `floatable == true` 表示允许浮动，不表示这个 dock 此刻已经浮动；当前是否浮动应通过 `QDockWidget::isFloating()` 查询。

请注意默认值层次不同：

- 一个新 `QDockWidget` 的 `features` 默认组合包含 closable、movable、floatable。
- 单独默认构造的 `QStyleOptionDockWidget` 用于绘制测试时，`closable` 和 `floatable` 默认是 `true`，`movable` 默认是 `false`。

因此不要把一个未由 `QDockWidget::initStyleOption()` 初始化的 option 当作真实 dock 的状态来源。

## 5. `verticalTitleBar`：方向会改变绘制几何

Qt 6.11.1 头文件中还公开了：

```cpp
bool verticalTitleBar;
```

它表示标题栏是否为竖向。通常对应 `QDockWidget::DockWidgetVerticalTitleBar` feature，竖向标题栏位于 dock 左侧，可为主窗口中的内容保留更多纵向空间。

```cpp
dock->setFeatures(dock->features()
                  | QDockWidget::DockWidgetVerticalTitleBar);
```

对 style 来说，`verticalTitleBar` 不是单纯的“旋转文字”开关。它会影响标题文本、浮动/关闭按钮和自定义装饰的可用矩形、方向与布局。自定义标题栏控件在 `resizeEvent()` 中也应检查父 `QDockWidget` 是否启用这一 feature，并提供适配两种方向的 `sizeHint()` 与 `minimumSizeHint()`。

`QStyleOptionDockWidget` 的 Qt 6.11.1 类文档页没有在“Public Variables”摘要中列出 `verticalTitleBar`，但安装头文件确实将它作为 public field 声明；写自定义 style 时应以头文件接口为准。

## 6. `QDockWidget::initStyleOption()`：子类的正确入口

若你继承 `QDockWidget` 并且确实需要拿到完整绘制参数，使用它提供的受保护函数：

```cpp
class CustomDockWidget final : public QDockWidget
{
public:
    using QDockWidget::QDockWidget;

protected:
    void inspectTitleBarState() const
    {
        QStyleOptionDockWidget option;
        initStyleOption(&option);

        // option.title、option.closable、option.verticalTitleBar
        // 均来自当前 QDockWidget 的真实状态。
    }
};
```

不要只调用 `option.initFrom(this)` 就认为信息完整。基类 `QStyleOption::initFrom()` 只填通用 widget 绘制上下文；`QDockWidget::initStyleOption()` 还会填本类专属的标题与 feature 派生字段。

## 7. 类型、版本、生命周期与文档勘误

| 常量 | Qt 6.11.1 头文件值 | 用途 |
| --- | --- | --- |
| `QStyleOptionDockWidget::Type` | `QStyleOption::SO_DockWidget` | 标识这是 dock widget option。 |
| `QStyleOptionDockWidget::Version` | `1` | 标识本数据布局版本。 |

离线类文档的 version 表格存在前后不一致：值列写 `1`，说明列却写 `2`。Qt 6.11.1 安装头文件明确声明 `enum StyleOptionVersion { Version = 1 };`，本页按头文件记录。

该类是值类型：

- 通常在当前绘制调用栈上创建并立即传给 style。
- 不继承 `QObject`，没有父对象，也不拥有 `QDockWidget`、`QMainWindow` 或 `QPainter`。
- 复制构造只复制绘制数据。
- style 从基类指针读取它时应使用 `qstyleoption_cast()`。

## 8. 常见误区与排查

### 8.1 “我对 `QStyleOptionDockWidget` 调 `show()`”

不能。它不是 `QWidget`，只是一份数据。应对真正的 `QDockWidget` 调 `show()`，或由 `QMainWindow` 管理可见性。

### 8.2 “我把 `closable` 设为 false，关闭按钮仍在”

option 的字段不会改 dock 的 feature。使用：

```cpp
dock->setFeatures(dock->features()
                  & ~QDockWidget::DockWidgetClosable);
```

随后由 `QDockWidget` 在下一次绘制时反映正确状态。

### 8.3 “内容控件设置最小尺寸后，浮动时大小不对”

尺寸约束应主要放在 `setWidget()` 传入的内容控件上。`QDockWidget` 在停靠和浮动间切换时会计算不同的 frame 与标题栏开销；直接固定 dock 外壳常导致约束不自然。

### 8.4 “自定义标题栏在竖向 dock 中被挤压或方向错误”

检查 `DockWidgetVerticalTitleBar` 和 `verticalTitleBar`，让标题栏控件的 size hint 同时适配横向、竖向。未处理的鼠标事件应 `ignore()`，使事件能继续交给 `QDockWidget` 处理拖动和停靠。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionDockWidget()` | 创建并以默认值初始化 dock 标题栏绘制数据。 | 单独构造不等于真实 dock 状态；自定义 `QDockWidget` 中优先调用 `initStyleOption()`。 |
| 构造 | `QStyleOptionDockWidget(const QStyleOptionDockWidget &other)` | 创建另一个 dock option 的值副本。 | 复制绘制字段，不转移 `QDockWidget`、`QMainWindow` 或 `QPainter` 的所有权。 |
| 类型常量 | `StyleOptionType::Type` | 返回值为 `SO_DockWidget` 的运行时类型标识。 | style 接收基类指针时用 `qstyleoption_cast()` 识别，不要只按 `element` 猜类型。 |
| 类型常量 | `StyleOptionVersion::Version` | 表示当前 dock option 数据布局版本，Qt 6.11.1 头文件中为 `1`。 | 以安装头文件为准；版本字段用于兼容识别，不是 Qt 版本号。 |
| 公共字段 | `QString title` | 提供本次绘制要显示的 dock 标题文字。 | 通常由 `QDockWidget::windowTitle()` 填入；修改真实标题应调用 `setWindowTitle()`。 |
| 公共字段 | `bool closable` | 表示 dock 是否具备关闭能力，供 style 决定是否绘制关闭入口。 | 反映 `DockWidgetClosable`，直接修改它只影响当前绘制快照，不会改变 dock feature。 |
| 公共字段 | `bool movable` | 表示 dock 是否允许用户移动和重新停靠。 | 反映 `DockWidgetMovable`；它不表示当前正在拖动。 |
| 公共字段 | `bool floatable` | 表示 dock 是否允许脱离主窗口成为浮动窗口。 | 反映 `DockWidgetFloatable`；当前是否浮动应查询 `QDockWidget::isFloating()`。 |
| 公共字段 | `bool verticalTitleBar` | 表示标题栏是否按竖向标题栏几何绘制。 | 通常对应 `DockWidgetVerticalTitleBar`；自定义标题栏必须同时适配横向和竖向布局。 |
| 继承字段 | `QStyleOption::rect` | 指定本次 dock 标题栏 style 操作使用的绘制矩形。 | 它不是整个主窗口矩形，也不是内容 widget 的矩形，具体范围由 dock 绘制流程提供。 |
| 继承字段 | `QStyleOption::state` | 提供启用、活动、焦点等通用绘制状态。 | 它和 closable/movable/floatable 这类“允许做什么”的 feature 状态不是同一维度。 |
| 初始化 | `QDockWidget::initStyleOption(QStyleOptionDockWidget *)` | 从真实 dock 组装完整标题栏绘制 option。 | 这是 `QDockWidget` 子类获取当前标题、feature 和方向状态的正确入口。 |
| 行为配置 | `QDockWidget::setFeatures(...)` | 设置 dock 是否可关闭、移动、浮动以及标题栏方向等能力。 | 业务代码应改真实 dock 的 features，不要把 option 字段当成行为控制器。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_DockWidgetTitle, ...)` | 让当前 style 按主题绘制 dock 标题栏。 | 自定义 style 中应保留基础 style，并根据 `verticalTitleBar` 和功能位调整局部外观。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionDockWidget *>(option)` | 从 `QStyleOption *` 安全识别 dock option。 | 失败时返回空指针；只在当前绘制调用期间读取，不要缓存 option 指针。 |

---

### 一句话总结

`QStyleOptionDockWidget` 是 dock 标题栏的一次性绘制说明：`title` 提供标题，`closable/movable/floatable` 反映允许的交互能力，`verticalTitleBar` 指导方向相关几何；真正改变 dock 行为要调用 `QDockWidget` API，自定义 style 才读取这个 option 来保持主题一致的外观。
