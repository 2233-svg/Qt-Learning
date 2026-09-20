# Qt QDropEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDropEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QDropEvent`  
> 定位：拖放目标真正接收数据并完成业务提交的事件

## 1. 它解决什么问题

`QDropEvent` 是拖放流程的提交阶段。用户松开鼠标后，目标从事件中读取 MIME 数据、位置和输入动作，验证内容并更新自己的模型。前面的 `QDragEnterEvent` 和 `QDragMoveEvent` 只负责预览和允许性判断，不能替代这里的实际导入。

常见场景：

- 将 URL 转成文件列表；
- 把文本插入编辑器光标位置；
- 将图片导入画布；
- 把内部对象移动到新的列表、树节点或网格位置。

事件处理完成后应明确 `accept()` 或 `ignore()`。接受表示目标已经处理这次 drop；不接受则让源或平台知道本次提交未完成。

## 2. 最小用法

```cpp
void DropWidget::dropEvent(QDropEvent *event)
{
    const QMimeData *data = event->mimeData();
    if (!data->hasUrls()) {
        event->ignore();
        return;
    }

    const QList<QUrl> urls = data->urls();
    if (!validateUrls(urls)) {
        event->ignore();
        return;
    }

    importUrls(urls, event->position());
    event->setDropAction(Qt::CopyAction);
    event->accept();
}
```

建议顺序是：读取并校验数据、确定位置、执行业务操作、设置实际动作、接受事件。业务操作失败时不要无条件调用 `acceptProposedAction()`。

## 3. 坐标和输入状态

`position()` 是接收对象局部坐标的 `QPointF`。它适合映射到 widget、场景或模型。不要把它直接当成屏幕坐标；需要屏幕级定位时，使用接收对象的坐标映射 API。

`buttons()` 和 `modifiers()` 是 drop 发生瞬间的快照。修饰键可能决定用户意图，例如 Ctrl 倾向复制、Shift 倾向移动，但最终动作仍由源、目标和平台协议共同决定。

Qt 6 推荐使用 `position()`；旧的 `pos()`、`posF()`、`mouseButtons()`、`keyboardModifiers()` 是兼容接口，迁移时应优先替换。

## 4. 动作选择

- `possibleActions()`：源支持的动作集合；
- `proposedAction()`：当前平台建议动作；
- `dropAction()`：事件当前动作；
- `setDropAction(action)`：目标要求某个动作；
- `acceptProposedAction()`：接受建议动作并标记事件已接受。

如果目标实际执行的是复制，应明确设置 Copy；否则目标调用 `acceptProposedAction()` 可能按源或平台建议执行移动：

```cpp
if (event->possibleActions() & Qt::CopyAction) {
    copyData();
    event->setDropAction(Qt::CopyAction);
    event->accept();
}
```

目标不能要求源不支持的动作。跨应用拖动还可能无法得到可靠的 `source()`，因此不要把内部对象指针作为通用协议。

## 5. MIME 数据和所有权

`mimeData()` 返回 `const QMimeData *`，由拖动源管理，目标只借用。目标不能 delete、修改其底层对象或把裸指针保存到异步任务。若需要异步导入，应在事件处理期间复制需要的字符串、URL、图片或字节数组。

外部 MIME 数据是不可信输入。打开 URL、解析 HTML、读取自定义格式前，要检查 scheme、路径、大小和格式版本。不要因为 `hasUrls()` 为真就直接执行 URL。

## 6. 生命周期、性能和线程

drop 事件只在 GUI 线程同步分发。处理函数应尽快返回；大文件复制或复杂解码可以把已复制的数据交给后台任务，但不能把 `QDropEvent *` 或 `mimeData()` 裸指针跨线程传递。

如果业务操作是异步的，接受事件表示“目标已接管提交请求”，不表示后台任务已经成功。应在业务层提供失败反馈和回滚策略。

## 7. 常见错误

- 在 `dragMoveEvent()` 中修改模型，导致没有 drop 也产生数据；
- `acceptProposedAction()` 前没有验证 MIME；
- 复制动作实际执行成移动动作；
- 把 `position()` 当成全局屏幕坐标；
- 事件返回后继续使用 `mimeData()` 指针；
- drop 业务失败仍调用 `accept()`；
- 用 `source()` 强转为自家 widget，忽略外部拖动时它可能为空。

## 8. 逐项 API 说明

### `QDropEvent(...)`

```cpp
QDropEvent(const QPointF &pos,
           Qt::DropActions actions,
           const QMimeData *data,
           Qt::MouseButtons buttons,
           Qt::KeyboardModifiers modifiers,
           QEvent::Type type = QEvent::Drop)
```

构造一个 drop 事件。普通应用通常由 Qt 平台创建，手动构造只适合测试。`data` 不转移所有权；`actions` 是源支持的动作集合；`type` 通常使用 `Drop`。

### 数据、位置与输入

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QPointF position() const` | 返回目标局部位置。 | Qt 6 推荐；不是全局坐标。 |
| `const QMimeData *mimeData() const` | 取得拖动数据。 | 借用只读指针，不要删除或跨线程保存。 |
| `Qt::MouseButtons buttons() const` | 返回 drop 时鼠标按钮状态。 | 事件快照，不能替代实时状态。 |
| `Qt::KeyboardModifiers modifiers() const` | 返回 drop 时修饰键。 | 用于解释用户动作意图。 |
| `QObject *source() const` | 返回拖动源对象。 | 外部拖动可能为 `nullptr`。 |

### 动作

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `Qt::DropActions possibleActions() const` | 查询源支持动作集合。 | 用位运算检查单个动作。 |
| `Qt::DropAction proposedAction() const` | 查询平台建议动作。 | 不是目标必须执行的动作。 |
| `Qt::DropAction dropAction() const` | 查询当前动作。 | 目标可通过 `setDropAction()` 修改。 |
| `void setDropAction(Qt::DropAction action)` | 设置目标选择的动作。 | 应属于 `possibleActions()`。 |
| `void acceptProposedAction()` | 接受建议动作并接受事件。 | 只适用于建议动作符合业务规则的情况。 |

### 从 `QEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `accept()` | 标记 drop 已处理。 | 业务成功或已接管请求后调用。 |
| `ignore()` | 标记 drop 未处理。 | 业务校验失败时使用。 |
| `isAccepted()` | 查看接受状态。 | 不等于动作是 Copy 或 Move。 |
| `type()` | 获取事件类型。 | 正常应为 `QEvent::Drop`。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 位置 | `position()` | 确定数据放入的位置。 | 局部浮点坐标，必要时映射。 |
| 数据 | `mimeData()` | 读取拖入内容。 | 只读借用；先校验再使用。 |
| 来源 | `source()` | 识别内部拖动源。 | 外部拖动可能为空。 |
| 能力 | `possibleActions()` | 了解源能执行哪些动作。 | 是集合，不是最终结果。 |
| 建议 | `proposedAction()` | 查看平台建议动作。 | 不能无条件信任。 |
| 选择 | `setDropAction()` | 指定实际 Copy/Move/Link。 | 必须与源能力兼容。 |
| 接受 | `acceptProposedAction()` | 直接接受建议动作。 | 先完成格式和业务校验。 |
| 接受 | `accept()` | 确认目标处理完成。 | 业务失败不要调用。 |
| 拒绝 | `ignore()` | 让源知道本次未处理。 | 适用于格式或业务校验失败。 |
| 输入 | `buttons()` / `modifiers()` | 读取 drop 时输入状态。 | 是事件快照。 |

---

### 一句话总结

`QDropEvent` 是拖放提交点：复制需要的数据、校验外部输入、选择真实动作，成功后再接受事件并更新模型。
