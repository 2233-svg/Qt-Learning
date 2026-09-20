# Qt QUndoView 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUndoView>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QListView -> QUndoView`  
> 定位：撤销历史可视化控件

## 1. QUndoView 解决什么问题

`QUndoView` 把 `QUndoStack` 里的命令历史显示成一个列表。用户不仅可以点击“撤销”和“重做”，还可以直接在历史列表中选择某个状态，让撤销栈一次性回退或重做到那个位置。

它解决的是“如何把撤销历史展示给用户，并允许用户跳转到历史状态”的问题。

```text
QUndoStack / QUndoGroup
          │
          ▼
      QUndoView
          │
          ▼
   选择历史项 -> 改变 stack index
```

它只显示和操纵撤销栈，不负责创建 `QUndoCommand`，也不负责执行具体业务修改。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 绑定 QUndoStack

```cpp
#include <QApplication>
#include <QUndoStack>
#include <QUndoView>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    auto *stack = new QUndoStack;
    stack->setUndoLimit(100);

    QUndoView view(stack);
    view.setWindowTitle("操作历史");
    view.show();

    return app.exec();
}
```

实际项目中，`QUndoStack` 通常属于编辑器或文档控制器；`QUndoView` 只是把它展示出来。

### 2.3 使用 QUndoGroup

```cpp
auto *group = new QUndoGroup;
group->addStack(documentAStack);
group->addStack(documentBStack);

auto *view = new QUndoView(group);
```

使用 group 时，视图展示的是 group 当前激活的 undo stack。切换当前文档或窗口时，要同步切换 `QUndoGroup` 的 active stack。

## 3. 核心使用模型

### 3.1 列表项代表“执行到这里的状态”

每一行通常对应一个 `QUndoCommand`。当前选中位置代表撤销栈的当前 index；点击更早的命令，视图会让 stack undo；点击更晚的命令，视图会让 stack redo。

因此它显示的不是一组静态日志，而是一组可以直接改变文档状态的控制项。

### 3.2 `QUndoView` 不拥有撤销栈

视图只是观察和操作 `QUndoStack`/`QUndoGroup`。撤销栈的生命周期应由文档、编辑器或应用控制器管理。

### 3.3 stack 和 group 是两种连接模式

通常选择其中一种：

- `setStack()`：固定显示一个撤销栈；
- `setGroup()`：跟随 group 的当前激活栈。

不要一边把 view 绑定到 stack，一边又期待它自动跟随 group；连接模式应明确。

### 3.4 cleanIcon 和 emptyLabel 是状态提示

- `cleanIcon`：标记文档处于 clean 状态的位置；
- `emptyLabel`：没有可显示撤销历史时显示的文字。

它们不改变撤销逻辑，只改变用户对历史列表的理解。

## 4. 适合用在哪里

- 文档编辑器的历史面板；
- 图形编辑器的操作历史；
- 多文档应用的撤销栈观察器；
- 调试复杂命令合并和撤销行为。

如果用户不需要查看历史，普通工具栏上的 `undoAction()` / `redoAction()` 就够了，不必额外放一个 `QUndoView`。

## 5. 常见误区

### 5.1 把列表文本当普通日志

点击历史项会真实改变文档状态，不是简单选中一行。

### 5.2 让 view 管理 stack 生命周期

`QUndoView` 不负责销毁外部 stack/group。要由业务层保证它们在 view 使用期间一直有效。

### 5.3 使用 group 却不切换 active stack

视图只会展示 group 当前激活的 stack。多文档场景要正确维护 `QUndoGroup` 的活动栈。

### 5.4 不理解 clean 状态

`cleanIcon` 只是标记 `QUndoStack::cleanIndex()`，它不是“保存按钮状态”的替代品。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `emptyLabel : QString` | 设置没有撤销历史或没有关联栈时显示的文字。 | 这是空状态提示，不是命令内容。 |
| 属性 | `cleanIcon : QIcon` | 设置 clean 状态在历史列表中的图标。 | 对应撤销栈的 clean index。 |
| 构造 | `QUndoView(QWidget *parent = nullptr)` | 创建一个尚未绑定撤销栈的历史视图。 | 后续用 `setStack()` 或 `setGroup()`。 |
| 构造 | `QUndoView(QUndoStack *stack, QWidget *parent = nullptr)` | 创建并绑定到指定撤销栈的历史视图。 | view 不拥有 stack。 |
| 构造 | `QUndoView(QUndoGroup *group, QWidget *parent = nullptr)` | 创建并绑定到撤销组的历史视图。 | 仅在启用 undo group 配置时可用。 |
| 析构 | `~QUndoView()` | 销毁历史视图。 | 不会自动销毁外部 stack 或 group。 |
| 查询 | `stack() const` | 返回当前直接绑定或当前 group 激活的撤销栈。 | 没有可用撤销栈时返回 `nullptr`。 |
| 查询 | `group() const` | 返回当前绑定的撤销组。 | 直接绑定 stack 时通常为空。 |
| 修改 | `setStack(QUndoStack *stack)` | 让视图显示指定撤销栈。 | 会切换视图的数据来源。 |
| 修改 | `setGroup(QUndoGroup *group)` | 让视图跟随撤销组的当前激活栈。 | 多文档场景要维护 group 的 active stack。 |
| 查询 | `emptyLabel() const` | 返回空状态提示文字。 | 和 `setEmptyLabel()` 配对。 |
| 修改 | `setEmptyLabel(const QString &label)` | 设置没有历史时显示的文字。 | 可以用于本地化或说明当前状态。 |
| 查询 | `cleanIcon() const` | 返回 clean 状态图标。 | 和 `setCleanIcon()` 配对。 |
| 修改 | `setCleanIcon(const QIcon &icon)` | 设置 clean 状态图标。 | 只影响显示，不改变 clean index。 |

## 7. 一句话总结

`QUndoView` 是撤销历史的可视化控制器，点击列表项会直接改变 `QUndoStack` 的当前状态；它展示历史，但不拥有撤销栈，也不负责业务命令本身。
