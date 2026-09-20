# Qt QGraphicsWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QGraphicsWidget>`
> 所属模块：`Qt6::Widgets`
> 继承：`QGraphicsObject -> QGraphicsWidget`
> 常见搭档：`QGraphicsLayout`、`QGraphicsScene`

## 1. QGraphicsWidget 解决什么问题

`QGraphicsWidget` 是图形视图架构里的“控件型 item”。它有 `QWidget` 一样的很多感觉：大小、布局、焦点、窗口标题、样式、动作、窗口边框，但它本质上仍然是一个 `QGraphicsItem`，不是桌面窗口部件。

它适合：

- 在 `QGraphicsScene` 里做控件化 UI；
- 需要 item 级布局协作；
- 需要窗口样式的场景内面板；
- 想把 layout 和 graphics item 结合起来。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QGraphicsWidget>
#include <QGraphicsLinearLayout>
#include <QGraphicsProxyWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    auto *scene = new QGraphicsScene;
    auto *widget = new QGraphicsWidget;
    auto *layout = new QGraphicsLinearLayout(Qt::Vertical);
    layout->addItem(new QGraphicsWidget);
    widget->setLayout(layout);
    scene->addItem(widget);

    QGraphicsView view(scene);
    view.show();
    return app.exec();
}
```

`QGraphicsWidget` 自己不显示成系统窗口，它只是在场景里表现得像“有边框、有布局、有焦点的控件”。

## 3. 和 QWidget 的差别

| 项 | `QWidget` | `QGraphicsWidget` |
| --- | --- | --- |
| 所属体系 | Widgets 窗口体系 | Graphics View item 体系 |
| 布局 | `QLayout` | `QGraphicsLayout` |
| 坐标 | 像素窗口坐标 | 场景/item 坐标 |
| 事件 | QWidget 事件 | scene event / item change |
| 常见用途 | 桌面界面控件 | 场景内控件、面板、仪表盘 |

## 4. 布局和尺寸

```cpp
widget->setLayout(layout);
widget->adjustSize();
widget->resize(200, 120);
widget->setContentsMargins(8, 8, 8, 8);
```

`QGraphicsWidget` 通过 `QGraphicsLayout` 组织子项。  
`layoutChanged()` 和 `geometryChanged()` 是你判断布局变动的关键信号。

`sizeHint()`、`minimumSize()`、`preferredSize()`、`maximumSize()`、`sizePolicy()` 都是它和普通 item 之间的接口。

## 5. 窗口化和边框

```cpp
widget->setWindowTitle("Panel");
widget->setWindowFlags(Qt::Window);
widget->setWindowFrameMargins(4, 4, 4, 4);
```

`QGraphicsWidget` 可以表现为场景中的“窗口”。  
`windowFrameGeometry()`、`windowFrameRect()`、`windowFrameSectionAt()` 这些函数就是给这种窗口化边框服务的。

如果你只是想做普通区域，不必开窗口 flags。

## 6. 焦点、动作和 tab 顺序

```cpp
widget->setFocusPolicy(Qt::StrongFocus);
QGraphicsWidget::setTabOrder(a, b);
widget->addAction(action);
widget->removeAction(action);
```

它支持动作列表和键盘焦点链，和 `QWidget` 很像，但对象还是场景里的 item。

## 7. 样式和绘制

```cpp
widget->setStyle(QApplication::style());
widget->setPalette(palette);
widget->setFont(font);
widget->setAutoFillBackground(true);
```

`paint()`、`paintWindowFrame()`、`initStyleOption()` 是主要绘制入口。  
如果要定制控件外观，优先改样式和布局，再考虑重写绘制。

## API 速查表
### 8.1 创建、布局和尺寸

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = {})` | 创建一个场景中的控件型 item。 | 它属于 graphics view 体系，不是普通 `QWidget`；父对象是 `QGraphicsItem` 父子关系。 |
| 析构 | `~QGraphicsWidget()` | 销毁图形控件及其 item 子树关系。 | 如果已经加入场景，通常由场景或 item 父对象负责最终销毁。 |
| 布局 | `layout()` / `setLayout(QGraphicsLayout *)` | 读取或设置管理子 item 的图形布局。 | 只能使用 `QGraphicsLayout`，不能把 `QVBoxLayout` 或 `QLayout` 直接塞进来。 |
| 布局 | `adjustSize()` | 按 size hint 和布局约束重新计算自身尺寸。 | 内容变化后常用；它不会把普通 QWidget 转成图形控件。 |
| 尺寸 | `size()` / `resize(...)` | 读取或设置 item 的宽高。 | 只改尺寸，不自动改变位置；最终尺寸仍可能受布局约束影响。 |
| 几何 | `geometry()` / `setGeometry(...)` | 读取或设置 item 在父 item 坐标中的矩形。 | 由布局管理的控件不应频繁手动改 geometry，否则会与布局协商冲突。 |
| 矩形 | `rect()` | 返回以 item 原点为左上角、大小等于 `size()` 的本地矩形。 | 它不是场景坐标矩形；需要场景坐标时要结合 item 的变换映射。 |
| 边距 | `setContentsMargins(...)` / `getContentsMargins(...)` | 设置或读取布局内容与控件边界之间的内边距。 | 影响布局区域，不等于窗口外框边距。 |
| 尺寸协商 | `sizeHint(Qt::SizeHint, const QSizeF &constraint)` | 为布局提供最小、首选或最大尺寸建议。 | 自定义图形控件时应让返回值和内容真实需求一致。 |
| 尺寸协商 | `updateGeometry()` | 通知父布局重新询问自身尺寸提示。 | 内容、字体或边框变化后调用；不是直接调整尺寸的函数。 |

### 8.2 布局方向、样式和外观

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 布局方向 | `layoutDirection()` / `setLayoutDirection(...)` | 读取或设置布局的从左到右或从右到左方向。 | RTL 界面应配合文字、图标和实际阅读方向一起测试。 |
| 布局方向 | `unsetLayoutDirection()` | 清除控件自身的方向设置，使其回到继承或默认状态。 | 适合主题或语言切换后恢复统一继承链。 |
| 样式 | `style()` / `setStyle(QStyle *)` | 读取或设置图形控件使用的 Qt 样式。 | 样式对象通常由应用或场景提供；不要随意删除仍在使用的共享 style。 |
| 字体 | `font()` / `setFont(...)` | 读取或设置控件及其子项可继承的字体。 | 字体变化可能改变 size hint，必要时配合 `updateGeometry()`。 |
| 调色板 | `palette()` / `setPalette(...)` | 读取或设置控件的颜色角色。 | 适合主题同步；自定义 `paint()` 时仍需主动使用 palette。 |
| 背景 | `autoFillBackground()` / `setAutoFillBackground(bool)` | 控制是否按调色板填充控件背景。 | 只影响图形控件自身的背景填充，不会替代复杂的自定义绘制。 |
| 绘制 | `paint(...)` | 绘制控件本体。 | 重写时要遵守 `QStyleOptionGraphicsItem` 和 painter 状态约定。 |
| 绘制 | `paintWindowFrame(...)` | 绘制窗口型图形控件的外框。 | 只有设置窗口标志并需要自定义框架时才值得重写。 |
| 样式准备 | `initStyleOption(QStyleOption *) const` | 为样式绘制准备包含状态、矩形等信息的选项对象。 | 自定义绘制时应先正确初始化 option，再交给 style 使用。 |

### 8.3 场景内窗口、焦点和动作

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 窗口标志 | `windowFlags()` / `setWindowFlags(...)` | 读取或设置 item 是否按场景内窗口、对话框等方式表现。 | 设置窗口类型可能改变外框、焦点和事件行为；普通面板通常不需要 `Qt::Window`。 |
| 窗口类型 | `windowType()` | 返回当前窗口标志中的窗口类型部分。 | 用于判断当前是否是场景内窗口，而不是普通 item。 |
| 活动窗口 | `isActiveWindow()` | 判断这个图形控件是否是场景中的活动窗口。 | 需要场景处于活动状态；它与普通桌面窗口的激活不是同一层级。 |
| 标题 | `windowTitle()` / `setWindowTitle(...)` | 读取或设置场景内窗口的标题。 | 只有窗口化控件的标题栏或自定义绘制才会显示它。 |
| 边框边距 | `setWindowFrameMargins(...)` / `getWindowFrameMargins(...)` | 设置或读取窗口外框占用的边距。 | 这是窗口框架区域，不要拿它替代内容 `contentsMargins`。 |
| 边框边距 | `unsetWindowFrameMargins()` | 清除手动设置的窗口框边距，回到样式计算。 | 更换 style 后通常应允许样式重新计算。 |
| 边框几何 | `windowFrameGeometry()` / `windowFrameRect()` | 查询包含窗口框架后的外部几何区域或本地矩形。 | 自定义拖动、缩放和边框命中时才需要；普通布局用 `geometry()`。 |
| 焦点 | `focusPolicy()` / `setFocusPolicy(...)` | 读取或设置控件是否能通过鼠标、键盘等方式获得焦点。 | 没有合适的 focus policy，场景内键盘交互不会按预期工作。 |
| 焦点 | `focusWidget()` | 返回当前焦点所在的子 `QGraphicsWidget`。 | 只在控件包含图形子控件时有意义；没有焦点子控件时可能为空。 |
| Tab 顺序 | `setTabOrder(first, second)` | 设置两个图形控件之间的键盘 Tab 导航顺序。 | 这是图形控件自己的焦点链，不是普通 QWidget 的 tab 顺序。 |
| 动作 | `addAction()` / `addActions()` | 把一个或多个 `QAction` 加入控件动作列表。 | 动作提供快捷键、上下文菜单等入口；action 仍是独立 QObject。 |
| 动作 | `insertAction()` / `insertActions()` | 把动作插到指定 action 前面。 | `before` 不属于当前列表时要确认实际插入语义，避免依赖错误顺序。 |
| 动作 | `removeAction()` / `actions()` | 移除动作或读取当前动作列表。 | 移除 action 不等于删除 action；所有权由 action 的 parent 和调用方决定。 |
| 快捷键 | `grabShortcut(...)` / `releaseShortcut(int)` | 注册或释放控件级快捷键。 | 这是比 QAction 更底层的快捷键机制；只在确实需要直接接收 shortcut 时使用。 |
| 快捷键 | `setShortcutEnabled(...)` / `setShortcutAutoRepeat(...)` | 控制已注册快捷键是否启用以及是否自动重复。 | 只对 `grabShortcut()` 得到的 id 生效，id 失效后不要继续操作。 |

### 8.4 属性、关闭和事件接口

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `setAttribute(Qt::WidgetAttribute, bool)` / `testAttribute(...)` | 设置或查询图形控件的 widget 属性。 | 只适合 Qt 明确支持的属性；不能把所有 QWidget 属性都当作在场景中等价可用。 |
| 类型 | `type()` | 返回图形控件的 item 类型编号。 | 主要给 `qgraphicsitem_cast` 或自定义类型判断使用。 |
| 关闭 | `close()` | 请求关闭场景内控件。 | 可能触发关闭事件并被拒绝；返回值应当作为关闭结果判断。 |
| 通知 | `geometryChanged()` | 几何区域发生变化时发出的信号。 | 可用于同步连接线、外部属性面板或重排辅助元素。 |
| 通知 | `layoutChanged()` | 图形布局发生变化时发出的信号。 | 适合在子项增删或尺寸协商后刷新外部状态。 |
| 事件 | `windowFrameEvent(QEvent *)` | 处理场景内窗口框架的特殊事件。 | 只有自定义窗口边框交互时才重写，普通 item 不需要。 |
| 命中 | `windowFrameSectionAt(const QPointF &)` | 判断场景坐标位置命中了窗口框架的哪个区域。 | 可用于识别标题栏、边缘和角点；坐标必须是 item 本地坐标语义。 |

### 一句话总结

`QGraphicsWidget` 就是场景里的“控件”：它把布局、焦点、样式和窗口边框这些 QWidget 的便利感带进了 graphics view 世界。
