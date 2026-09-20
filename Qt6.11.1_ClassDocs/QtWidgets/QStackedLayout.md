# QStackedLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QStackedLayout`

## 1. 先建立直觉

`QStackedLayout` 是一次显示一个页面的布局。它不像 `QStackedWidget` 自带外壳控件，而是直接作为 layout 放进某个 QWidget，适合你想完全控制外层 UI，但内部需要页面切换的场景。

典型用途包括设置页右侧内容、向导页面、自定义导航+内容区、登录/注册切换、空状态/加载中/内容视图切换。

## 2. 类说明

- 头文件：`#include <QStackedLayout>`
- 模块：`Qt6::Widgets`
- 继承自：`QLayout`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

如果你需要一个现成 QWidget 容器，用 `QStackedWidget`；如果你正在设计自己的复合控件，用 `QStackedLayout` 更轻。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStackedLayout()` / `QStackedLayout(parent)` | 创建堆叠布局。 |
| `addWidget()` / `insertWidget()` | 添加或插入页面并返回索引。 |
| `setCurrentIndex()` / `currentIndex()` | 切换或读取当前页面索引。 |
| `setCurrentWidget()` / `currentWidget()` | 按 widget 切换或读取当前页面。 |
| `widget(index)` | 获取某页 widget。 |
| `count()` | 页面数量。 |
| `setStackingMode()` / `stackingMode()` | `StackOne` 只显示当前页；`StackAll` 所有页可见但当前页置顶。 |
| `currentChanged(index)` | 当前页面变化。 |
| `widgetAdded(index)` | Qt 6.9 起页面加入信号。 |
| `widgetRemoved(index)` | 页面移除信号。 |
| `itemAt()` / `takeAt()` | 作为布局访问内部 item。 |

## 4. 关键用法

`StackOne` 是默认模式，适合普通页面切换。`StackAll` 适合叠加层，例如内容页上叠一个透明提示层或浮动编辑层，但要自己处理鼠标事件穿透、透明背景和层级关系。

页面导航通常由外部控件驱动：列表、树、按钮组、tab bar 都可以连接到 `setCurrentIndex()`。这比把导航和页面强绑在一个控件里更灵活。

## 5. 常见坑与经验

- 空布局时 current index 为 `-1`，访问页面前检查。
- 页面 widget 加入后由布局/父控件体系管理，不要再放入其他布局。
- `StackAll` 下不可见假设不成立，所有页面都可能参与绘制和事件。
- 移除页面后索引会变化，保存长期索引用业务 id 更稳。
