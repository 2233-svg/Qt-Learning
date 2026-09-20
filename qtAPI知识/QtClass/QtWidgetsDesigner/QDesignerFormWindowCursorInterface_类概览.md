# QDesignerFormWindowCursorInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerFormWindowCursorInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerFormWindowCursorInterface` 是 Qt Widgets Designer 对当前窗体“选择、焦点链位置和属性编辑命令”的操作入口。它借用了 cursor 的概念，但不是编辑文本字符的 `QTextCursor`：它在 Designer 的 widget 顺序和选区中移动，并能通过 Designer 的命令系统修改属性。

它主要解决三类问题：

- 查询当前 form 中有哪些 widget、当前选中了哪些 widget；
- 在 Designer 的焦点链/选择序列中移动或扩大选区；
- 修改、重置 widget 属性，并让操作进入 Designer 的撤销体系。

通常从一个 form window 取得 cursor：

```cpp
auto *formWindow = QDesignerFormWindowInterface::findFormWindow(widget);
if (!formWindow)
    return;

auto *cursor = formWindow->cursor();
cursor->setWidgetProperty(widget, "title", "Report");
```

插件要修改 `.ui` 中已有 widget 属性时，优先经由这个 cursor，而不是直接 `widget->setProperty()` 或 `QDesignerPropertySheetExtension::setProperty()`。这样 Designer 才能正确跟踪修改、刷新属性编辑器并支持撤销。

## 选择和位置

cursor 维护当前位置与 anchor：

- `MoveAnchor`：移动当前位置时同时移动锚点，结果是单一选择；
- `KeepAnchor`：保留旧锚点，移动后形成或扩展选择范围。

`MoveOperation` 以 form 的焦点链和空间方向为基准移动，如 `Start`、`End`、`Next`、`Prev`、`Left`、`Right`、`Up`、`Down`。这些行为服务于 Designer 的选择导航，不应用来推断 QWidget 在 layout 中的实际索引。

```cpp
cursor->movePosition(
    QDesignerFormWindowCursorInterface::Next,
    QDesignerFormWindowCursorInterface::KeepAnchor);
```

上例在焦点链中向后移动，同时保留旧锚点，使选区扩展。

## 查询当前选择

`current()` 返回当前选中的主 widget，`selectedWidgetCount()` 与 `selectedWidget(index)` 返回多选集合，`hasSelection()` 判断是否存在选区，`isWidgetSelected(widget)` 判断某个具体 widget 是否被选中。

多选时不要假设 `current()` 等于 `selectedWidget(0)` 的业务含义；前者表示 cursor 的当前点，后者是选区集合中的某个位置。批量处理应遍历 `selectedWidgetCount()`。

## 属性编辑入口

- `setProperty(name, value)`：修改当前选中 widget 的属性；
- `setWidgetProperty(widget, name, value)`：修改指定 widget 的属性；
- `resetWidgetProperty(widget, name)`：恢复指定 widget 的属性默认值。

它们服务于 Designer 编辑操作。调用前要确保属性名正确、`QVariant` 类型与目标属性兼容，并且 widget 属于当前 form window。对动态属性或特殊 property sheet 属性，也要保持与 Designer 的持久化规则一致。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `enum MoveMode` | 控制移动 cursor 时 anchor 如何变化。 | 用来改变选择范围，不是文本编辑格式选项。 |
| 枚举值 | `MoveAnchor` | 移动当前位置并同步移动 anchor。 | 适合只保留单个当前选择。 |
| 枚举值 | `KeepAnchor` | 移动当前位置但保留旧 anchor。 | 适合扩展当前选择范围。 |
| 成员类型 | `enum MoveOperation` | 指定 cursor 在窗体选择序列中的移动方式。 | 基于 Designer 的焦点链或方向，不等价于 layout item 索引。 |
| 枚举值 | `NoMove` | 不移动 cursor。 | 一般用于显式保持位置的调用路径。 |
| 枚举值 | `Start` | 移到焦点链起点。 | 可能改变当前选择，结合 MoveMode 使用。 |
| 枚举值 | `End` | 移到焦点链终点。 | 可能改变当前选择，结合 MoveMode 使用。 |
| 枚举值 | `Next` | 移到焦点链下一个 widget。 | 用于顺序导航。 |
| 枚举值 | `Prev` | 移到焦点链前一个 widget。 | 用于反向顺序导航。 |
| 枚举值 | `Left` | 向左移动 cursor。 | 依据 Designer 空间导航语义，不保证等同于前一个 child。 |
| 枚举值 | `Right` | 向右移动 cursor。 | 同样依赖当前 Designer 窗体布局和导航规则。 |
| 枚举值 | `Up` | 向上移动 cursor。 | 空间导航可能因布局不同而有不同结果。 |
| 枚举值 | `Down` | 向下移动 cursor。 | 空间导航可能因布局不同而有不同结果。 |
| 析构 | `virtual ~QDesignerFormWindowCursorInterface()` | 销毁 cursor 接口。 | 不应直接构造或长期持有脱离 form window 生命周期的 cursor。 |
| 当前选择 | `current() const` | 返回当前选中的主 widget。 | 没有有效当前选择时检查空指针；多选时不要把它当成全部选区。 |
| 所属窗体 | `formWindow() const` | 返回关联的 form window。 | 用于确认 cursor 操作作用于哪个 `.ui` 窗体。 |
| 选区状态 | `hasSelection() const` | 判断当前窗体是否存在选择。 | 批量编辑前先检查，避免对空选择调用 `setProperty()`。 |
| 选中判断 | `isWidgetSelected(QWidget *widget) const` | 判断指定 widget 是否在当前选区。 | widget 应属于关联 form window。 |
| 导航 | `movePosition(MoveOperation operation, MoveMode mode = MoveAnchor)` | 按指定操作移动 cursor，成功返回 `true`。 | 失败时保持或部分改变选择的具体行为要按调用结果处理；不要忽略返回值。 |
| 位置 | `position() const` | 返回 cursor 当前的位置索引。 | 这是 Designer 选择/焦点链位置，不是 widget 的 geometry 或 layout index。 |
| 重置属性 | `resetWidgetProperty(QWidget *widget, const QString &name)` | 将指定 widget 属性恢复默认值。 | 属性必须有可用默认/重置语义；操作会影响 `.ui` 保存状态。 |
| 选中 widget | `selectedWidget(int index) const` | 返回选区中指定位置的 widget。 | 索引范围是 `0` 到 `selectedWidgetCount() - 1`。 |
| 选中数量 | `selectedWidgetCount() const` | 返回当前选中 widget 数量。 | 批量操作前记录或遍历此数量；选择变化后索引集合可能改变。 |
| 设置位置 | `setPosition(int position, MoveMode mode = MoveAnchor)` | 将 cursor 移到给定位置。 | position 必须属于当前窗体可导航范围；`KeepAnchor` 会扩展选择。 |
| 设置当前属性 | `setProperty(const QString &name, const QVariant &value)` | 修改当前选中 widget 的指定属性。 | 无选区时无目标；用于可撤销 Designer 编辑，不是普通 QObject 直接赋值替代。 |
| 设置指定属性 | `setWidgetProperty(QWidget *widget, const QString &name, const QVariant &value)` | 修改指定 widget 的属性。 | 优先用于插件修改 form 中的 widget，保持 Designer 的撤销和刷新语义。 |
| 枚举 form widget | `widget(int index) const` | 返回窗体 widget 列表中的指定 widget。 | 索引范围是 `0` 到 `widgetCount() - 1`，不代表 widget 层级或 tab order。 |
| widget 数量 | `widgetCount() const` | 返回 form window 中可枚举 widget 数量。 | 窗体结构改变后数量和索引可能变化。 |

## 易错点

1. 这是 Designer 的 form cursor，不是 `QTextCursor`，位置对应焦点链/选择序列。
2. 需要让属性改动进入撤销栈时，应使用 `setProperty()` 或 `setWidgetProperty()`，不要绕过 Designer 直接改 widget。
3. `setProperty()` 只作用于当前选择；精确目标修改使用 `setWidgetProperty()`。
4. `KeepAnchor` 会扩大选择范围，批量修改前要确认你不是无意选中了多个 widget。
5. `widget(index)` 和 `selectedWidget(index)` 的索引属于不同集合，不能混用。

### 一句话总结

`QDesignerFormWindowCursorInterface` 是 Designer 窗体的选择与属性编辑 cursor：它遍历选区、查询 form 中 widget，并用可追踪的方式修改或重置 widget 属性。
