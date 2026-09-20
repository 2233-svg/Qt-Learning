# Qt QDragEnterEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDragEnterEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QDropEvent -> QDragMoveEvent -> QDragEnterEvent`  
> 定位：拖动指针首次进入接收对象时的询问事件

## 1. 它解决什么问题

`QDragEnterEvent` 是拖放目标收到的第一道判断。它告诉目标：一个拖动会话刚进入当前 widget，携带哪些 MIME 数据、支持哪些动作、当前位置在哪里。目标在这里接受事件，后续才会继续收到 `QDragMoveEvent` 和最终的 `QDropEvent`。

典型流程是：

1. `dragEnterEvent()` 检查 `mimeData()` 是否包含自己理解的格式；
2. 检查 `possibleActions()` 是否包含可执行动作；
3. 接受或忽略进入事件；
4. 若接受，`dragMoveEvent()` 负责按位置细化反馈，`dropEvent()` 负责真正写入模型。

它只表示“允许拖动进入”，不表示数据已经落下。不要在这里删除文件、插入列表项或执行不可逆操作。

## 2. 构建与事件入口

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::Widgets)
```

```cpp
#include <QDragEnterEvent>
#include <QMimeData>
#include <QWidget>
```

在 Widgets 中重写：

```cpp
void DropWidget::dragEnterEvent(QDragEnterEvent *event)
{
    const QMimeData *data = event->mimeData();
    if (data->hasUrls() &&
        (event->possibleActions() & Qt::CopyAction)) {
        event->acceptProposedAction();
    } else {
        event->ignore();
    }
}
```

接收 widget 还需要启用 drops，例如 `setAcceptDrops(true)`。事件指针只在当前处理调用期间有效，不要保存到异步回调。

## 3. 接受、忽略与动作

`QDragEnterEvent` 继承 `QDragMoveEvent` 和 `QDropEvent` 的操作，因此可以调用：

- `accept()`：接受进入请求，但不主动改变 drop action；
- `acceptProposedAction()`：把当前建议动作设为当前动作并接受；
- `setDropAction(action)` 后 `accept()`：目标明确要求某个动作；
- `ignore()`：拒绝进入，后续通常不会把这次拖动当作当前目标继续处理。

如果目标只能复制，即使源的建议动作是移动，也应明确：

```cpp
if (event->possibleActions() & Qt::CopyAction) {
    event->setDropAction(Qt::CopyAction);
    event->accept();
}
```

传给 `setDropAction()` 的动作必须与源支持的动作兼容；目标不能凭空要求源不支持的动作。源最终还要以 `QDrag::exec()` 返回值为准。

## 4. MIME 数据与安全边界

`mimeData()` 返回只读 `const QMimeData *`。目标可以读取文本、URL、图片、HTML 或自定义 MIME 类型。外部应用拖入的 URL、HTML 或自定义数据都不能直接信任。写文件前要检查路径、权限、文件类型和危险位置；解析自定义二进制数据时要检查长度和版本。

进入事件适合做轻量格式判断，不适合同步读取大文件。需要预览时可以延后到移动事件，真正导入放到 `dropEvent()`。

## 5. 事件时序与 UI 反馈

进入事件通常发生一次，随后可能有很多移动事件。进入事件适合初始化悬停反馈，例如设置高亮；离开事件负责清理。若只接受特定区域，可在 `dragMoveEvent()` 根据位置细化允许性。

成功 drop 时由 `dropEvent()` 完成提交。不要因为进入事件已接受，就假设后续一定会发生 drop；用户可能把指针移出窗口、取消拖动或改用不支持的动作。

## 6. 常见错误

- 忘记 `setAcceptDrops(true)`，导致事件根本不到达；
- 只检查 `mimeData()`，不检查 `possibleActions()`；
- 在 `dragEnterEvent()` 中直接完成 drop；
- 接受进入后没有处理 `dragLeaveEvent()`，高亮状态残留；
- 保存事件指针，稍后异步读取导致悬空；
- 把 `acceptProposedAction()` 当成“必然复制”或“必然移动”。

## 7. 逐项 API 说明

### `QDragEnterEvent(...)`

```cpp
QDragEnterEvent(const QPoint &pos,
                Qt::DropActions actions,
                const QMimeData *data,
                Qt::MouseButtons buttons,
                Qt::KeyboardModifiers modifiers)
```

手动构造进入事件，主要用于测试或事件注入。`pos` 是目标 widget 的整数局部坐标；`actions` 是源支持的动作集合；`data` 由拖动会话管理，事件不取得其所有权；`buttons` 和 `modifiers` 是进入瞬间的输入状态。普通应用不应自行构造平台拖放事件。

### 从 `QDragMoveEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `accept()` | 接受当前进入/移动请求。 | 不自动把动作改成某个具体值。 |
| `accept(const QRect &rectangle)` | 接受并设置下一次需要报告变化的矩形。 | 是事件反馈优化提示，不是最终可 drop 区域。 |
| `ignore()` | 拒绝当前请求。 | 进入阶段忽略通常表示当前对象不接收拖动。 |
| `ignore(const QRect &rectangle)` | 忽略并设置变化矩形。 | 只影响事件反馈节奏。 |
| `answerRect() const` | 查询当前回答矩形。 | 由矩形重载设置。 |

### 从 `QDropEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `position() const` | 获取目标局部浮点坐标。 | Qt 6 推荐；构造函数仍使用 `QPoint`。 |
| `possibleActions() const` | 获取源支持的动作集合。 | 是能力集合，不是最终动作。 |
| `proposedAction() const` | 获取当前建议动作。 | 可被目标通过 `setDropAction()` 改变。 |
| `setDropAction(Qt::DropAction)` | 指定目标希望执行的动作。 | 只应选择源支持的动作。 |
| `dropAction() const` | 查询当前动作。 | 接受前后可能不同。 |
| `acceptProposedAction()` | 接受建议动作。 | 等价于设置建议动作并接受事件。 |
| `mimeData() const` | 读取拖动数据。 | 只读借用指针，不要删除。 |
| `buttons() const` / `modifiers() const` | 获取进入瞬间输入状态。 | 是事件快照。 |
| `source() const` | 获取拖动源对象。 | 外部应用拖动时可能为 `nullptr`。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDragEnterEvent(...)` | 创建进入事件。 | 主要用于测试；事件不拥有 MIME 数据。 |
| 判断 | `mimeData()` | 判断是否理解拖入内容。 | 只读；外部数据需要安全校验。 |
| 判断 | `possibleActions()` | 判断源支持哪些动作。 | 不等于最终 drop action。 |
| 动作 | `proposedAction()` | 查看平台建议动作。 | 可按业务改为 Copy/Move/Link。 |
| 接受 | `accept()` | 允许拖动进入。 | 不自动选择具体动作。 |
| 接受 | `acceptProposedAction()` | 接受当前建议动作。 | 只在目标确实支持该动作时使用。 |
| 接受 | `setDropAction()` + `accept()` | 明确指定目标动作。 | 动作必须与 `possibleActions()` 兼容。 |
| 拒绝 | `ignore()` | 拒绝当前拖动。 | 不代表最终 drop 失败回调。 |
| 位置 | `position()` | 获取进入位置。 | 使用局部坐标。 |
| 优化 | `answerRect()` | 控制移动事件反馈区域。 | 不替代命中测试。 |

---

### 一句话总结

`QDragEnterEvent` 是拖放目标的第一道门：先检查 MIME 和动作能力，再决定是否让这次拖动进入当前对象。
