# Qt QContextMenuEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QContextMenuEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QInputEvent -> QContextMenuEvent`  
> 定位：请求打开上下文菜单时携带的位置与触发来源

## 1. 它解决什么问题

`QContextMenuEvent` 表示用户请求“针对当前位置或当前选择显示操作菜单”。鼠标右键只是最常见的触发方式；键盘的菜单键、平台定义的快捷键，以及其他系统方式也可能生成同一种事件。

事件对象提供三类信息：

- **触发来源**：鼠标、键盘或其他方式；
- **局部位置**：接收事件的 widget 内应针对哪个内容建立菜单；
- **全局位置**：菜单应在屏幕哪个位置弹出。

真实场景包括：

1. 在 `QTreeView`、画布、表格或文本编辑器中根据点击项显示不同菜单；
2. 键盘用户按菜单键时，为当前焦点项或当前选择打开同一套操作；
3. 支持“右键按下/拖动用于选择，释放后再显示菜单”的 Windows 交互习惯；
4. 自定义 widget 在局部坐标中做命中测试，在全局坐标中调用 `QMenu::exec()` 或 `popup()`。

它是短生命周期的事件参数，不是菜单对象。菜单内容由 `QMenu`、`QAction` 或 Qt Quick 的 `ContextMenu` 创建。

## 2. 构建与事件入口

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::Widgets)
```

```cpp
#include <QContextMenuEvent>
#include <QMenu>
#include <QWidget>
```

在 Widgets 中，通常重写 `QWidget::contextMenuEvent()`：

```cpp
class Canvas : public QWidget
{
protected:
    void contextMenuEvent(QContextMenuEvent *event) override;
};
```

不要长期保存 `event` 指针。Qt 在同步事件分发完成后拥有并销毁事件；若之后还要使用位置或触发原因，应在处理函数中复制 `pos()`、`globalPos()` 和 `reason()` 的值。

## 3. 最小可用代码

```cpp
#include <QContextMenuEvent>
#include <QMenu>
#include <QWidget>

class Canvas : public QWidget
{
protected:
    void contextMenuEvent(QContextMenuEvent *event) override
    {
        QMenu menu(this);
        menu.addAction(tr("Add marker"));
        menu.addAction(tr("Clear"));

        menu.exec(event->globalPos());
        event->accept();
    }
};
```

`QMenu::exec()` 需要屏幕全局坐标，因此使用 `globalPos()`。若根据用户点击的图元决定动作，应先使用 `pos()` 在 widget 的局部坐标中命中测试。

## 4. 事件时机与平台行为

### 4.1 右键事件即使已处理也可能继续到来

与某些由未接受输入事件衍生的合成事件不同，`QContextMenuEvent` 会在原始鼠标或键盘事件已经被接受后仍然发送。原因是它需要支持平台习惯：例如用户可以用右键点击或拖动来改变当前选择，然后让菜单动作作用于新的选择。

因此，下面的想法并不可靠：

```text
我已经在 mousePressEvent() 接受右键事件，所以不会再收到 contextMenuEvent()。
```

如果你已经自行在 `mousePressEvent()` 中实现“按下后打开菜单、拖到菜单项再释放选择”的交互，那么在 `contextMenuEvent()` 中应当对 `Mouse` 原因调用 `ignore()`，避免重复弹出菜单；但仍要处理 `Keyboard` 原因，保证键盘可访问性。

### 4.2 Windows 与其他平台的发送时机不同

Qt 默认遵循平台约定：

- Windows 常在右键**释放**时发送上下文菜单事件；
- 其他平台常在右键**按下**时发送；
- 键盘触发不一定有可用的鼠标局部位置。

不要把菜单打开逻辑写死为“右键按下必然立刻显示”。若需要统一的自定义按下-拖动-释放交互，应该直接处理 `QMouseEvent`，并明确去重后续的 `QContextMenuEvent`。

## 5. 坐标语义与空位置

### 5.1 `pos()` 是接收 widget 的局部坐标

`pos()` 指向接收事件的 widget 内位置。它适合：

- 调用 `childAt()`、命中测试或查找表格单元格；
- 将局部点映射到画布、场景或模型索引；
- 判断是否点击在当前选择、空白区域或某个图元上。

### 5.2 `globalPos()` 是屏幕坐标

`globalPos()` 是事件发生时的鼠标全局位置，适合传给菜单的弹出接口：

```cpp
menu.popup(event->globalPos());
```

不要把 `pos()` 直接交给 `QMenu::popup()`，否则嵌套 widget、窗口移动或多屏幕环境中，菜单通常会出现在错误位置。

### 5.3 键盘触发时位置可能为空

若事件并非由右键产生，`pos()` 可能是空点 `(0, 0)`。这不是“用户一定在左上角打开菜单”，而是位置不可靠的信号。

键盘路径应使用当前焦点、当前选择或控件定义的默认锚点。例如表格可在当前索引的视觉矩形中心显示菜单，文本控件可在光标矩形附近显示；不要仅用 `pos().isNull()` 判断后仍然在 `(0, 0)` 弹菜单。

## 6. `Reason` 与可访问性

`reason()` 告诉你事件为何被发送：

- `Mouse`：鼠标导致，通常是右键，但仍受平台约定影响；
- `Keyboard`：键盘菜单键或平台快捷键导致；
- `Other`：非鼠标、非键盘的其它方式。

大多数应用无需为了 `Mouse` 和 `Keyboard` 使用完全不同菜单；差异通常在于**上下文的定位方式**。鼠标事件使用 `pos()` 找目标，键盘事件使用当前焦点或选择找目标。

不要只在 `reason() == Mouse` 时显示菜单。这样会让键盘用户失去同一操作入口，也与 Qt 发送键盘上下文菜单事件的目的相悖。

## 7. 接受、忽略与继续传播

### 7.1 菜单由当前对象处理

当当前 widget 已经完成处理，通常调用 `event->accept()`。许多事件处理路径默认也会处于接受状态，但显式表达能让“此处截获菜单请求”的意图清楚。

### 7.2 当前对象不处理

若不应由当前对象提供菜单，调用：

```cpp
event->ignore();
```

Qt 会尝试把事件传递给该位置下的其他 widget 或 Qt Quick Item。这个机制对复合控件很有用：外层容器可以让内部子控件优先响应其专属菜单。

不要在已经打开菜单后再调用 `ignore()`，否则可能造成重复菜单或不可预测的后续路由。

## 8. 手动构造与测试边界

一般程序不需要手动构造 `QContextMenuEvent`；Qt 会从原始平台输入创建并投递它。测试、事件过滤器验证或自定义事件注入时可以使用构造函数：

```cpp
QContextMenuEvent event(
    QContextMenuEvent::Mouse,
    QPoint(12, 8),
    widget.mapToGlobal(QPoint(12, 8)),
    Qt::ControlModifier);
```

构造出的事件初始为未接受状态。构造函数的 `reason` 约定为 `Mouse` 或 `Keyboard`；`Other` 是 Qt 用于描述其它来源的原因值，不应被作为常规手动构造参数滥用。

传入的 `pos` 和 `globalPos` 必须相互对应。特别是在多屏幕、HiDPI、子 widget 或嵌套窗口场景，使用 `widget.mapToGlobal(pos)` 得到全局位置比手写屏幕坐标可靠。

## 9. 常见误区与排查顺序

### 9.1 菜单位置偏移

确认传给 `QMenu::exec()` / `popup()` 的是 `globalPos()`，不是 `pos()`。若仍偏移，再检查目标 widget 是否是接收者、是否经过 `mapToGlobal()`，以及是否有自定义坐标变换。

### 9.2 右键一次出现两个菜单

检查是否同时在 `mousePressEvent()` 或 `mouseReleaseEvent()` 中手动弹菜单，又在 `contextMenuEvent()` 中弹菜单。若自定义鼠标模式已经处理了 `Mouse` 原因，应对该原因忽略上下文菜单事件。

### 9.3 键盘打开菜单出现在左上角

检查 `reason()`。键盘触发时 `pos()` 可能为空，应该从焦点项、当前选择或光标位置计算一个合适的全局锚点。

### 9.4 子控件菜单不出现

父 widget 若无条件接受了事件，子控件或底层目标可能没有机会处理。对不属于父对象的区域或输入来源调用 `ignore()`，让 Qt 继续投递。

### 9.5 保存事件指针异步使用

`QContextMenuEvent *` 只在调用栈内有效。异步回调中使用它会成为悬空指针；请复制需要的数据值。

## 10. 与相关类型的协作

- `QWidget::contextMenuEvent()`：Widgets 的主要重写入口。
- `QMenu`：承载并显示菜单项；使用 `globalPos()` 定位。
- `QAction`：定义菜单可执行操作。
- `QInputEvent`：提供 `modifiers()`、`timestamp()` 等输入事件共性数据。
- `QMouseEvent`：需要自定义按下-拖动-释放菜单交互时直接处理它。
- Qt Quick `ContextMenu`：Qt Quick 中的对应处理方式。

## 11. 逐项 API 说明

### `QContextMenuEvent::Reason`

```cpp
enum Reason { Mouse, Keyboard, Other };
```

| 枚举值 | 含义 | 处理建议 |
| --- | --- | --- |
| `Mouse` | 鼠标导致事件，通常是右键，具体触发方式依平台而定。 | 用 `pos()` 命中测试；避免与手工鼠标菜单重复。 |
| `Keyboard` | 键盘菜单键或平台快捷键导致。 | 从焦点、选择或光标确定上下文，不要假定鼠标位置有效。 |
| `Other` | 不是鼠标或键盘的其它来源。 | 作为可处理的上下文请求处理，避免假定具体输入设备。 |

### `QContextMenuEvent` 构造函数

```cpp
QContextMenuEvent(Reason reason,
                  const QPoint &pos,
                  const QPoint &globalPos,
                  Qt::KeyboardModifiers modifiers = Qt::NoModifier)
```

**作用：** 手动创建一个上下文菜单事件，初始接受状态为 `false`。

**参数边界：**

- `reason` 应为 `Mouse` 或 `Keyboard`；
- `pos` 相对接收 widget；
- `globalPos` 使用屏幕全局坐标；
- `modifiers` 保存 Ctrl、Shift、Alt 等键盘修饰状态；
- 手动构造通常仅用于测试或事件注入。

### `globalPos()`、`globalX()`、`globalY()`

```cpp
const QPoint &globalPos() const
int globalX() const
int globalY() const
```

**作用：** 取得事件时鼠标的屏幕全局坐标或单独坐标分量。

**使用重点：**

- 菜单定位优先使用完整的 `globalPos()`；
- `globalX()`、`globalY()` 主要适合遗留代码或简单数值计算；
- 键盘触发时应按控件上下文确认这个位置是否适合作为菜单锚点。

### `pos()`、`x()`、`y()`

```cpp
const QPoint &pos() const
int x() const
int y() const
```

**作用：** 取得相对于接收 widget 的鼠标位置。

**使用重点：**

- 用于局部命中测试；
- 非右键事件时 `pos()` 可能是空点；
- `x()`、`y()` 是 `pos()` 的分量快捷入口。

### `reason()`

```cpp
QContextMenuEvent::Reason reason() const
```

**作用：** 返回事件触发来源。

**使用重点：** 根据来源选择上下文定位策略；不要忽略键盘路径。

### 从 `QInputEvent` 继承的常用成员

| API | 用途 | 注意事项 |
| --- | --- | --- |
| `modifiers()` | 获取触发时的键盘修饰键。 | 与当前实时键盘状态不同，以事件发生瞬间为准。 |
| `accept()` | 声明当前对象已处理事件。 | 菜单已由当前对象处理时使用。 |
| `ignore()` | 放弃当前处理，让 Qt 尝试继续投递。 | 不要在已经显示菜单后调用。 |
| `isAccepted()` | 查询当前接受状态。 | 可用于事件过滤器或复杂路由调试。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum Reason { Mouse, Keyboard, Other }` | 识别上下文菜单请求的来源。 | 键盘触发时不应依赖鼠标局部坐标。 |
| 构造 | `QContextMenuEvent(Reason, const QPoint &, const QPoint &, Qt::KeyboardModifiers)` | 手动创建事件。 | 初始未接受；`reason` 应为 `Mouse` 或 `Keyboard`。 |
| 位置 | `const QPoint &pos() const` | 获得接收 widget 内的局部位置。 | 用于命中测试；非右键事件可能为空点。 |
| 位置 | `int x() const` | 获得局部 x 坐标。 | 等价于 `pos().x()` 的便捷入口。 |
| 位置 | `int y() const` | 获得局部 y 坐标。 | 等价于 `pos().y()` 的便捷入口。 |
| 位置 | `const QPoint &globalPos() const` | 获得屏幕全局位置。 | `QMenu::exec()` / `popup()` 的常用参数。 |
| 位置 | `int globalX() const` | 获得全局 x 坐标。 | 通常优先使用完整 `globalPos()`。 |
| 位置 | `int globalY() const` | 获得全局 y 坐标。 | 通常优先使用完整 `globalPos()`。 |
| 查询 | `Reason reason() const` | 查询事件来源。 | 决定如何寻找上下文，而不是决定是否支持菜单。 |
| 继承 | `Qt::KeyboardModifiers modifiers() const` | 获得触发时的修饰键。 | 表示事件瞬间状态。 |
| 继承 | `accept()` / `ignore()` | 控制当前对象是否处理事件。 | `ignore()` 可让 Qt 尝试把事件交给其它目标。 |

---

### 一句话总结

`QContextMenuEvent` 是一次上下文菜单请求：用 `pos()` 找局部对象、用 `globalPos()` 弹出菜单，并把鼠标与键盘触发都当成一等交互路径。
