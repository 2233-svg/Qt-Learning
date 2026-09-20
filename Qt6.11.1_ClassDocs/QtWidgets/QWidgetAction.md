# QWidgetAction

> Qt 6.11.1 · Qt Widgets · 来自 `QWidgetAction`

## 1. 先建立直觉

`QWidgetAction` 是一种特殊 `QAction`，它用 QWidget 作为 action 的可视表现。普通 action 在菜单里显示文本，在工具栏里显示按钮；`QWidgetAction` 可以显示搜索框、滑块、颜色选择器、缩放下拉等真实控件。

它适合把少量轻量控件嵌进菜单或工具栏。复杂交互仍应使用 dock、弹出面板或对话框，因为菜单天然是短生命周期的命令界面。

## 2. 类说明

- 头文件：`#include <QWidgetAction>`
- 模块：`Qt6::Widgets`
- 继承自：`QAction`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它本身不是 QWidget，而是能为不同容器请求/创建 QWidget 的 action。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QWidgetAction(parent)` | 创建 widget action。 |
| `setDefaultWidget()` / `defaultWidget()` | 设置单个默认控件，所有权转给 action。 |
| `requestWidget(parent)` | 容器请求该 action 的可视 widget。 |
| `releaseWidget(widget)` | 容器释放该 action 的 widget。 |
| `createWidget(parent)` | 子类化时为每个容器创建新 widget。 |
| `deleteWidget(widget)` | 子类化控制 widget 释放策略。 |
| `createdWidgets()` | 返回当前由 `createWidget()` 创建并在使用的 widgets。 |

## 4. 关键用法

### 默认 widget 只适合单一容器

`setDefaultWidget()` 最简单，但一个 QWidget 不能同时出现在多个父容器里。如果同一个 action 可能同时加入菜单和工具栏，或同一菜单多处使用，应重写 `createWidget()`，每次返回一个新控件。

### 子类化更可控

重写 `createWidget(parent)` 可以创建并初始化控件，连接信号到 action 或业务槽。容器移除 action 时会调用 `releaseWidget()`，最终走 `deleteWidget()`。默认删除策略是隐藏并 `deleteLater()`。

### 和 QAction 状态同步

既然它继承 `QAction`，enabled、visible、text、tooltip 等状态仍然有意义。自定义 widget 应响应 action 的 enabled 状态，避免 action 禁用但内部控件还能操作。

### 菜单里的控件要轻

菜单可能因为失焦而关闭，嵌入文本框或 slider 时要测试焦点、键盘和关闭行为。长时间编辑、复杂验证不适合放菜单里。

## 5. 常见坑与经验

- 一个 QWidget 不能被多个容器同时显示。
- `setDefaultWidget()` 后 action 接管 widget 所有权。
- 放入菜单的控件可能不会像普通 action 那样自动触发 `triggered()`。
- 在工具栏中嵌入控件时要给它稳定尺寸，避免工具栏跳动。
- 复杂设置请用 dock 或对话框，不要把菜单变成小表单。
