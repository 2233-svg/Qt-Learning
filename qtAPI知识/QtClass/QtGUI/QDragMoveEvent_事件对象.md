# Qt QDragMoveEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDragMoveEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QDropEvent -> QDragMoveEvent`  
> 定位：拖动指针在接收对象内移动时的连续判断事件

## 1. 它解决什么问题

`QDragMoveEvent` 让目标在拖动过程中持续决定“这里能不能放、放下会执行什么动作”。它用于树节点插入定位、表格行列高亮、画布网格命中，以及在不同区域间切换 Copy、Move、Link 动作。

它不是最终提交事件。真正修改模型应放在 `dropEvent()`，否则用户只是移动指针就可能重复写入。

## 2. 基本处理方式

```cpp
void DropWidget::dragMoveEvent(QDragMoveEvent *event)
{
    if (!event->mimeData()->hasUrls()) {
        event->ignore();
        return;
    }

    const QRect allowedArea = rect().adjusted(8, 8, -8, -8);
    if (allowedArea.contains(event->position().toPoint())) {
        event->setDropAction(Qt::CopyAction);
        event->accept();
    } else {
        event->ignore();
    }
}
```

先判断格式，再做位置命中和动作选择。`position()` 是目标局部浮点坐标；需要和整数控件矩形比较时应明确取整策略。

## 3. `accept()` 与 `ignore()` 的矩形重载

除了无参数版本，本类提供：

```cpp
event->accept(rectangle);
event->ignore(rectangle);
```

矩形表示“当拖动位置离开这个区域时，才需要再次通知我”。它用于减少高频事件处理，不是自动替代业务命中测试。应用仍需在收到事件时根据当前位置决定是否允许放置。

`answerRect()` 返回最近一次设置的回答矩形。若没有显式设置，通常是空矩形；不要把空矩形解释成整个控件都不可放。

## 4. 动作和 MIME 数据

`possibleActions()` 是源声明的能力集合，`proposedAction()` 是平台和修饰键计算出的建议值，`dropAction()` 是事件当前动作。目标可调用 `setDropAction()` 后再 `accept()`，但动作必须属于 `possibleActions()`。

```cpp
const auto possible = event->possibleActions();
if (possible & Qt::MoveAction) {
    event->setDropAction(Qt::MoveAction);
    event->accept();
}
```

`acceptProposedAction()` 适合目标直接接受建议动作；如果业务只支持复制，不要盲目调用它。

## 5. 高频事件与性能

移动事件可能每秒到达很多次。避免在每个事件中读取大文件、解析复杂 HTML 或重建整个视图。可以只更新变化的高亮区域、对昂贵预览做节流，并使用回答矩形减少无意义通知。实际导入放到 `dropEvent()`。

## 6. 常见错误

- 把 `accept(rectangle)` 当成“只允许矩形内 drop”的完整实现；
- 忘记在离开区域时清理高亮；
- 把建议动作当成最终动作；
- 在移动事件中修改模型；
- 保存事件指针到异步回调；
- 只处理已弃用的整数位置 API，造成坐标精度损失。

## 7. 逐项 API 说明

### `QDragMoveEvent(...)`

```cpp
QDragMoveEvent(const QPoint &pos,
               Qt::DropActions actions,
               const QMimeData *data,
               Qt::MouseButtons buttons,
               Qt::KeyboardModifiers modifiers,
               QEvent::Type type = QEvent::DragMove)
```

用于测试或平台事件注入。`pos` 是局部整数坐标；`actions`、`data`、输入状态与 `QDropEvent` 语义相同。`type` 正常应为 `DragMove`，派生的 `QDragEnterEvent` 使用自己的类型。

### 移动事件专有 API

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QRect answerRect() const` | 取得当前回答矩形。 | 不是业务可放区域。 |
| `void accept()` | 接受当前点。 | 不自动选择动作。 |
| `void accept(const QRect &rectangle)` | 接受当前点并设置反馈矩形。 | 用于减少后续事件，不替代命中判断。 |
| `void ignore()` | 拒绝当前点。 | 可能让 Qt 继续寻找其他目标。 |
| `void ignore(const QRect &rectangle)` | 拒绝当前点并设置反馈矩形。 | 下一次仍需重新判断。 |

### 从 `QDropEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `position()` | 读取局部浮点位置。 | Qt 6 推荐。 |
| `mimeData()` | 读取拖动数据。 | 借用只读指针。 |
| `possibleActions()` | 读取源支持动作。 | 用位测试判断集合。 |
| `proposedAction()` | 读取建议动作。 | 不代表目标必须接受。 |
| `setDropAction()` | 指定目标动作。 | 选项应属于源支持集合。 |
| `dropAction()` | 查询当前动作。 | 只有接受后才对最终行为有意义。 |
| `acceptProposedAction()` | 接受建议动作。 | 目标无需改写动作时使用。 |
| `source()` | 查询源对象。 | 外部拖动可能为空。 |
| `buttons()` / `modifiers()` | 读取拖动时输入状态。 | 是事件快照。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 位置 | `position()` | 判断当前拖动点。 | Qt 6 优先使用浮点坐标。 |
| 内容 | `mimeData()` | 判断当前点是否支持数据格式。 | 只读；不要保存事件内指针。 |
| 动作 | `possibleActions()` | 了解源支持的动作。 | 这是位集合。 |
| 动作 | `proposedAction()` | 获取平台建议动作。 | 可以被目标改写。 |
| 动作 | `setDropAction()` | 选择 Copy/Move/Link。 | 必须兼容源能力。 |
| 接受 | `accept()` / `ignore()` | 接受或拒绝当前点。 | 不等于已经执行 drop。 |
| 优化 | `accept(rect)` / `ignore(rect)` | 降低无意义移动事件频率。 | 不是可放区域声明。 |
| 查询 | `answerRect()` | 查看反馈矩形。 | 由矩形重载设置。 |
| 继承 | `acceptProposedAction()` | 直接接受建议动作。 | 目标确实支持时再调用。 |

---

### 一句话总结

`QDragMoveEvent` 负责拖动过程中的“当前位置能否放置”判断；用它更新反馈，用 `QDropEvent` 完成真正的数据变更。
