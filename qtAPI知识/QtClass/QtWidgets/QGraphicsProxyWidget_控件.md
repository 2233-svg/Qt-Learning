# Qt QGraphicsProxyWidget 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGraphicsProxyWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QGraphicsObject -> QGraphicsWidget -> QGraphicsProxyWidget`  
> 定位：把 QWidget 嵌入 Graphics View 场景

## 1. QGraphicsProxyWidget 解决什么问题

`QGraphicsProxyWidget` 是 QWidget 和 Graphics View 之间的桥。它把一个普通的 `QWidget` 嵌入 `QGraphicsScene`，让这个控件可以和场景里的图形项一起移动、缩放、旋转、裁剪和参与场景事件分发。

例如，一个场景里既有流程图节点、连线和缩放画布，又需要在节点上放一个 `QLineEdit`、`QComboBox` 或按钮，这时就可以用代理控件。

```text
QWidget
   │ setWidget()
   ▼
QGraphicsProxyWidget
   │
   ▼
QGraphicsScene -> QGraphicsView
```

它解决的不是“把 QWidget 画成一张图片”，而是尽量保留 QWidget 的输入、焦点、编辑和子控件行为，并把这些行为映射到场景坐标系里。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 把一个 QLineEdit 放进场景

```cpp
#include <QApplication>
#include <QGraphicsProxyWidget>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QLineEdit>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QGraphicsScene scene;

    auto *edit = new QLineEdit;
    edit->setPlaceholderText("输入节点名称");

    QGraphicsProxyWidget *proxy = scene.addWidget(edit);
    proxy->setPos(40, 40);

    QGraphicsView view(&scene);
    view.resize(640, 420);
    view.show();

    return app.exec();
}
```

`QGraphicsScene::addWidget()` 会创建代理并把控件放进去，是最常用的入口。代理和控件的生命周期由 Graphics View 的所有权关系管理，不能再把同一个控件随意交给另一个代理。

## 3. 核心使用模型

### 3.1 场景坐标和控件坐标是两套坐标

`QWidget` 仍然以自己的局部坐标工作，代理负责把它映射到场景坐标。代理的 `pos()`、变换和 `setGeometry()` 影响场景中的位置和尺寸；控件自己的 `geometry()` 仍然是 QWidget 坐标。

```cpp
proxy->setPos(100, 80);
proxy->setRotation(8);
proxy->setScale(1.2);
```

如果需要知道嵌入控件某个子控件在代理中的位置，可以使用 `subWidgetRect()`。

### 3.2 焦点、鼠标和键盘事件会被转发

代理会把场景中的鼠标、键盘、焦点、拖放、悬停和输入法事件转给被嵌入的 QWidget。这样 `QLineEdit` 的光标、选择和输入法通常仍能正常工作。

但焦点链会同时经过 `QGraphicsScene` 和 QWidget。遇到 Tab 顺序、弹出菜单或组合框焦点异常时，要同时检查：

- 代理是否可聚焦；
- 场景视图是否拥有键盘焦点；
- 被嵌入控件的 focus policy；
- 是否在事件重写里错误地吞掉了事件。

### 3.3 子控件可能生成子代理

被嵌入的 QWidget 如果还有子控件，代理可以为子控件创建对应的代理对象。`createProxyForChildWidget()` 和 `newProxyWidget()` 就是这条机制的扩展点。

一般情况下不需要手动创建子代理。只有在定制代理层级或特殊嵌套控件行为时，才需要理解这两个函数。

### 3.4 所有权必须提前想清楚

通过 `setWidget()` 或 `QGraphicsScene::addWidget()` 嵌入后，代理会管理被嵌入的 QWidget。销毁代理时，不要再手动删除同一个 QWidget。

场景、代理、控件之间可以理解成：

```text
QGraphicsScene 管理 QGraphicsProxyWidget
QGraphicsProxyWidget 管理被嵌入 QWidget
```

如果要把控件从代理中取出，应先设计清楚移除和重新归属流程，不要在代理仍然持有它时直接 `delete`。

## 4. 适合用在哪里

- 图形化流程编辑器中的内嵌输入框；
- 节点编辑器中的下拉框、按钮和复选框；
- 可缩放的设计画布中放置少量标准控件；
- 需要把传统 QWidget 逐步迁移到 Graphics View 场景的过渡方案。

它不适合把大量复杂 QWidget 当成场景里的普通图元。每个代理都要维护 QWidget 的事件、布局和绘制，数量过多时会增加内存和重绘成本。大量重复元素更适合直接实现 `QGraphicsItem` 或使用模型/视图控件。

## 5. 常见误区

### 5.1 把代理当成 QWidget

代理是 `QGraphicsWidget`，真正的按钮、输入框仍然是 `proxy->widget()` 返回的 QWidget。场景几何和控件属性要分开设置。

### 5.2 以为缩放场景等于改变控件字体

`QGraphicsView` 的缩放会改变代理在场景中的视觉大小，但不会自动修改 QWidget 的字体、字号或逻辑尺寸。

### 5.3 让一个 QWidget 同时属于多个代理

一个 QWidget 不能同时被多个代理安全托管。需要多个场景副本时，应创建多个控件实例。

### 5.4 把所有控件都塞进 Graphics View

代理适合少量、确实需要和图形项一起变换的控件。普通表单、工具栏和设置页直接用 QWidget 布局通常更合适。

### 5.5 忽略原生窗口或特殊渲染控件限制

依赖原生窗口句柄、独立渲染表面或平台特性的控件，嵌入代理后的表现可能和普通 QWidget 不同。遇到黑屏、无法输入或弹出窗口位置异常时，要先确认该控件是否适合被嵌入。

## 6. 关键 API 怎么理解

### `setWidget()` / `widget()`

这是一对核心接口：前者建立 QWidget 和代理的关联，后者取回被嵌入控件。设置成功后，控件的显示、尺寸和事件会由代理协同管理。

### `setGeometry()` / `sizeHint()`

代理继承了图形布局项的几何接口。`setGeometry()` 改的是代理在场景中的几何；`sizeHint()` 则把被嵌入 QWidget 的尺寸建议转换成图形布局可以使用的尺寸。

### `subWidgetRect()`

它解决“场景里某个 QWidget 子控件到底对应代理中的哪个矩形”这个问题，适合做高亮、定位和自定义命中测试。

### `paint()`

代理的绘制工作是把 QWidget 的视觉内容绘制到场景中。通常不需要重写；如果重写，必须理解 QWidget 的更新、裁剪和场景绘制顺序。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Type` | 返回代理图形项的类型编号所使用的常量。 | 用于 `QGraphicsItem` 类型识别。 |
| 构造 | `QGraphicsProxyWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())` | 创建一个代理图形项。 | 通常随后调用 `setWidget()`，也可以由 `QGraphicsScene::addWidget()` 创建。 |
| 析构 | `~QGraphicsProxyWidget()` | 销毁代理及其托管的嵌入控件关系。 | 不要再手动删除仍由代理管理的 QWidget。 |
| 关联 | `setWidget(QWidget *widget)` | 把一个 QWidget 嵌入当前代理。 | 一个控件不要同时交给多个代理；设置后要遵守代理的所有权关系。 |
| 关联 | `widget() const` | 返回当前代理嵌入的 QWidget。 | 没有关联控件时返回 `nullptr`。 |
| 坐标 | `subWidgetRect(const QWidget *widget) const` | 返回某个嵌入控件或子控件在代理坐标中的矩形。 | 传入的控件必须属于当前嵌入控件树。 |
| 几何 | `setGeometry(const QRectF &rect)` | 设置代理在图形场景中的几何矩形。 | 会影响被嵌入 QWidget 的布局尺寸。 |
| 绘制 | `paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)` | 将嵌入 QWidget 的内容绘制到场景。 | 通常由 Qt 内部调用，不需要手动调用。 |
| 类型查询 | `type() const` | 返回代理的图形项类型编号。 | 可和 `QGraphicsItem::type()` 或类型转换配合。 |
| 子代理 | `createProxyForChildWidget(QWidget *child)` | 为嵌入控件树中的子控件创建代理。 | 一般由框架使用，手动调用前要确认子控件归属。 |
| 状态变化 | `itemChange(GraphicsItemChange change, const QVariant &value)` | 在代理的位置、可见性、父项等图形项状态变化时处理同步。 | 重写时不要破坏 QWidget 与代理之间的同步。 |
| 事件 | `event(QEvent *event)` | 处理代理收到的通用事件。 | 是代理协调 QWidget 事件的总入口之一。 |
| 事件过滤 | `eventFilter(QObject *object, QEvent *event)` | 过滤被嵌入 QWidget 及其子对象的事件。 | 需要拦截时先判断对象和事件类型。 |
| 显示事件 | `showEvent(QShowEvent *event)` | 处理代理显示时的同步工作。 | 通常让基类继续完成默认处理。 |
| 隐藏事件 | `hideEvent(QHideEvent *event)` | 处理代理隐藏时的同步工作。 | 代理隐藏后嵌入控件也不会正常显示。 |
| 菜单事件 | `contextMenuEvent(QGraphicsSceneContextMenuEvent *event)` | 转发或处理场景中的右键菜单事件。 | 是否可用取决于构建配置和被嵌入控件的菜单策略。 |
| 拖放事件 | `dragEnterEvent(QGraphicsSceneDragDropEvent *event)` | 处理拖放进入代理区域的事件。 | 被嵌入控件必须允许相应拖放。 |
| 拖放事件 | `dragLeaveEvent(QGraphicsSceneDragDropEvent *event)` | 处理拖放离开代理区域的事件。 | 和进入、移动、放下事件配套。 |
| 拖放事件 | `dragMoveEvent(QGraphicsSceneDragDropEvent *event)` | 处理拖动经过代理区域的事件。 | 可以影响是否接受最终放下。 |
| 拖放事件 | `dropEvent(QGraphicsSceneDragDropEvent *event)` | 处理拖放放下事件。 | 数据最终通常仍由嵌入 QWidget 消费。 |
| 悬停事件 | `hoverEnterEvent(QGraphicsSceneHoverEvent *event)` | 处理鼠标进入代理区域。 | 影响代理与嵌入控件的悬停状态同步。 |
| 悬停事件 | `hoverLeaveEvent(QGraphicsSceneHoverEvent *event)` | 处理鼠标离开代理区域。 | 和进入事件成对出现。 |
| 悬停事件 | `hoverMoveEvent(QGraphicsSceneHoverEvent *event)` | 处理鼠标在代理区域内移动。 | 频繁触发，不要放重计算。 |
| 鼠标抓取 | `grabMouseEvent(QEvent *event)` | 处理代理开始抓取鼠标时的事件。 | 由场景输入系统调用。 |
| 鼠标抓取 | `ungrabMouseEvent(QEvent *event)` | 处理代理释放鼠标抓取时的事件。 | 适合检查拖拽或按键状态是否需要清理。 |
| 鼠标事件 | `mouseMoveEvent(QGraphicsSceneMouseEvent *event)` | 处理代理中的鼠标移动。 | 通常继续转发给 QWidget。 |
| 鼠标事件 | `mousePressEvent(QGraphicsSceneMouseEvent *event)` | 处理代理中的鼠标按下。 | 影响点击、焦点和拖拽开始。 |
| 鼠标事件 | `mouseReleaseEvent(QGraphicsSceneMouseEvent *event)` | 处理代理中的鼠标释放。 | 与按下事件配套。 |
| 鼠标事件 | `mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)` | 处理代理中的鼠标双击。 | 例如双击嵌入编辑器或按钮区域。 |
| 滚轮事件 | `wheelEvent(QGraphicsSceneWheelEvent *event)` | 处理代理中的滚轮输入。 | 被嵌入控件和场景滚动策略可能共同影响结果。 |
| 键盘事件 | `keyPressEvent(QKeyEvent *event)` | 处理代理中的按键按下。 | 要注意快捷键、编辑器和场景焦点的优先级。 |
| 键盘事件 | `keyReleaseEvent(QKeyEvent *event)` | 处理代理中的按键释放。 | 与按下事件配套。 |
| 焦点事件 | `focusInEvent(QFocusEvent *event)` | 处理代理获得焦点。 | 让 QWidget 和场景焦点保持一致。 |
| 焦点事件 | `focusOutEvent(QFocusEvent *event)` | 处理代理失去焦点。 | 编辑器提交/取消可能在这里发生。 |
| 焦点导航 | `focusNextPrevChild(bool next)` | 在嵌入控件的子控件之间切换焦点。 | 影响 Tab/Shift+Tab 导航。 |
| 输入法 | `inputMethodQuery(Qt::InputMethodQuery query) const` | 查询输入法需要的光标、选区和文本状态。 | 文本编辑控件依赖它正确输入中文等组合文本。 |
| 输入法 | `inputMethodEvent(QInputMethodEvent *event)` | 接收输入法提交和预编辑事件。 | 不要随意吞掉，否则会破坏中文输入。 |
| 尺寸 | `sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const` | 根据 QWidget 的尺寸建议返回代理尺寸。 | `constraint` 会影响有约束布局下的结果。 |
| 尺寸事件 | `resizeEvent(QGraphicsSceneResizeEvent *event)` | 处理代理尺寸变化。 | 需要保持 QWidget 几何和代理几何同步。 |
| 保护槽 | `newProxyWidget(const QWidget *child)` | 为子控件创建新的代理对象。 | 通常由框架在子控件弹出或嵌套时使用。 |

## 8. 一句话总结

`QGraphicsProxyWidget` 把 QWidget 带进 Graphics View 世界，适合少量需要随场景移动和变换的标准控件；使用时最重要的是分清两套坐标、事件焦点和对象所有权。
