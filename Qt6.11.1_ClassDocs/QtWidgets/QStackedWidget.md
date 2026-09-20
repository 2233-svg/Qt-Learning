# QStackedWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QStackedWidget`

## 1. 先建立直觉

### 这是什么

`QStackedWidget` 是“多页面只显示一个”的容器。它内部使用 `QStackedLayout` 思路，把多个 `QWidget` 页面叠在同一块区域里，通过 index 或 widget 指针切换当前页。

它没有标签、侧边栏或导航 UI，只负责页面栈本身。你可以用按钮、列表、树、菜单、状态机或路由逻辑来控制它切换页面。

### 适合使用的场景

- 设置窗口左侧列表 + 右侧页面。
- 向导或流程页面，但不想用 `QWizard`。
- 登录页/主页面/错误页之间切换。
- 空状态、加载中、内容页、错误页等状态页面切换。

### 不适合的场景

- 用户需要看到标签并直接切换，用 `QTabWidget`。
- 只是在一个页面里折叠局部内容，用 hide/show 或布局更轻。
- 大量页面需要懒加载时，不要一次性创建所有重页面。

## 2. 依赖与对象关系

- 头文件：`#include <QStackedWidget>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QFrame`
- 直接派生类：类页未列出

加入的页面会成为 stacked widget 的子控件。`removeWidget()` 只是从页面栈移除，不删除页面；是否复用或删除由调用方决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `count : int` | 页面数量。 |
| `currentIndex : int` | 当前页面索引，空时为 `-1`。 |
| `QStackedWidget(QWidget *parent)` | 创建页面栈容器。 |
| `addWidget(QWidget *widget)` | 追加页面，返回索引。 |
| `insertWidget(int index, QWidget *widget)` | 插入页面，返回实际索引。 |
| `removeWidget(QWidget *widget)` | 从栈中移除页面但不删除。 |
| `widget(int index) const` | 按索引返回页面。 |
| `currentWidget() const` | 返回当前页面。 |
| `indexOf(const QWidget *widget) const` | 查询页面索引。 |
| `setCurrentIndex(int)` | 切换到指定索引。 |
| `setCurrentWidget(QWidget *)` | 切换到指定页面。 |
| `currentChanged(int)` | 当前页面变化时发出。 |
| `widgetAdded(int)` | Qt 6.9 起，页面加入时发出。 |
| `widgetRemoved(int)` | 页面移除时发出。 |
| `event(QEvent *)` | 通用事件处理。 |

## 4. API 逐项说明

### `count` / `currentIndex`

`count()` 返回页面数。`currentIndex()` 返回当前页索引，没有页面时通常为 `-1`。

不要把 index 当长期业务 id。页面插入和移除会改变后续 index；长期引用应保存页面指针或业务枚举映射。

### `addWidget(QWidget *widget)` / `insertWidget(int index, QWidget *widget)`

添加页面并返回索引。页面会成为 `QStackedWidget` 的子对象，显示区域由容器管理。

如果插入位置小于等于当前索引，当前索引可能相应移动以保持当前页面不变。初始化时最好添加完页面后再设置当前页。

### `removeWidget(QWidget *widget)`

从页面栈移除 widget，但不删除它。widget 的 parent 关系可能仍然存在，页面也会被隐藏。

如果不再需要页面，移除后调用 `deleteLater()`；如果要放到别的容器，移除后再重新加入新布局。

### `widget(int index)` / `currentWidget()` / `indexOf(const QWidget *)`

这些函数用于在索引和页面指针之间转换。索引无效时通常返回空指针或 `-1`。

切换前用 `indexOf()` 校验页面是否真的在栈里，能避免把外部 widget 误传给 `setCurrentWidget()`。

### `setCurrentIndex(int)` / `setCurrentWidget(QWidget *)`

切换当前页面。无效索引或不属于栈的 widget 不应作为正常流程。

切换页面只改变可见性，不自动重置页面状态。需要刷新数据时，在 `currentChanged()` 中处理，或给页面定义自己的激活函数。

### `currentChanged(int)` / `widgetAdded(int)` / `widgetRemoved(int)`

`currentChanged()` 是最常用信号。Qt 6.9 起增加 `widgetAdded()`，可以监听动态页面加入；`widgetRemoved()` 在页面移除时发出。

注意移除当前页可能同时导致当前页变化，信号顺序要按实际代码测试。

### `event(QEvent *e)`

通用事件处理。普通应用不需要重写。

如果你要做页面切换动画，通常不是重写 `event()`，而是组合 `QStackedWidget`、`QPropertyAnimation` 或换用自定义容器。

## 5. 深入实践与常见坑

### 它没有导航 UI

`QStackedWidget` 只负责页面栈。左侧列表、顶部按钮、路由逻辑都要你自己提供，并连接到 `setCurrentIndex()`。

### remove 不等于 delete

这是最常见坑。`removeWidget()` 后页面还在内存里；不需要时明确 `deleteLater()`。

### 页面可以懒加载

重页面不必一开始全创建。可以先放占位页，真正切换到某个功能时再创建并插入。
