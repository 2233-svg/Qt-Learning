# QToolBox

> Qt 6.11.1 · Qt Widgets · 来自 `QToolBox`

## 1. 先建立直觉

`QToolBox` 是一组折叠式页面容器，一次显示一个页面，页面标题像竖向工具分组。它适合工具面板、属性分类、设置分组、向导式但非线性的选项集合。

它和 `QTabWidget` 都是一页多面板，但气质不同：tab 更适合平级页面快速切换，toolbox 更适合垂直工具分类，特别是在窄侧栏里。

## 2. 类说明

- 头文件：`#include <QToolBox>`
- 模块：`Qt6::Widgets`
- 继承自：`QFrame`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

加入的页面 widget 会由 toolbox 管理父子关系。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QToolBox(parent, flags)` | 创建工具箱。 |
| `addItem(widget, text)` / `addItem(widget, icon, text)` | 添加页面并返回索引。 |
| `insertItem(index, widget, text/icon)` | 插入页面。 |
| `removeItem(index)` | 移除页面；页面 widget 不一定被删除，应确认所有权。 |
| `count()` | 页面数量。 |
| `currentIndex()` / `setCurrentIndex()` | 当前页面索引。 |
| `currentWidget()` / `setCurrentWidget()` | 当前页面 widget。 |
| `widget(index)` / `indexOf(widget)` | 索引和页面互查。 |
| `setItemText()` / `itemText()` | 设置或读取页面标题。 |
| `setItemIcon()` / `itemIcon()` | 设置或读取页面图标。 |
| `setItemToolTip()` / `itemToolTip()` | 设置或读取页面提示。 |
| `setItemEnabled()` / `isItemEnabled()` | 启用或禁用某页入口。 |
| `currentChanged(index)` | 当前页面变化信号。 |
| `itemInserted()` / `itemRemoved()` | 子类化时响应页面增删。 |

## 4. 关键用法

### 适合窄侧栏分组

画图工具、属性编辑器、资源面板里，`QToolBox` 可以把多个工具组压在一个窄区域中。每页内部仍然应使用布局，不要固定坐标。

### 页面数量不要太多

toolbox 的入口是竖向堆叠，超过几个分组后扫描成本会上升。很多页面、需要重排或关闭时，`QTabWidget`、树导航加 `QStackedWidget` 会更清楚。

### 禁用页面传达不可用状态

`setItemEnabled(index, false)` 适合当前上下文下暂不可用的工具组。禁用比隐藏更能告诉用户功能存在但当前条件不满足；永久不相关的页面则可以移除或不添加。

## 5. 常见坑与经验

- `removeItem()` 从 toolbox 移除页面，但不要默认以为业务对象也销毁了。
- 当前索引为空时为 `-1`，访问前检查。
- 页面标题要短，toolbox 入口空间有限。
- 嵌套太深会让用户迷路，页面内部保持简单。
- 需要可关闭或可重排页面时用 tab/dock 更合适。
