# Qt QDrag 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDrag>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject -> QDrag`  
> 定位：启动一次 MIME 数据拖放操作，并跟踪源、目标与最终动作

## 1. 它解决什么问题

`QDrag` 把“用户按住对象移动到另一个位置”的交互转换为 Qt 的 MIME 拖放协议。拖动源负责准备 `QMimeData`、声明允许的 `Qt::DropAction`，然后调用 `exec()`；目标窗口通过 `QDragEnterEvent`、`QDragMoveEvent` 和 `QDropEvent` 决定是否接受，以及最终执行复制、移动或链接。

常见场景：

- 文件管理器把本地文件拖到另一个目录或应用；
- 编辑器拖动文本、图片或自定义对象；
- 列表、树、表格内部重新排序；
- 自定义画布把一个图元拖到另一个容器。

`QDrag` 只描述一次拖动会话，不负责决定何时开始拖动。通常在鼠标按下后记录起点，移动距离超过 `QApplication::startDragDistance()` 时才创建它。

## 2. 生命周期与最小用法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::Widgets)
```

```cpp
#include <QDrag>
#include <QMimeData>
#include <QMouseEvent>
#include <QWidget>

void startDrag(QWidget *source)
{
    auto *drag = new QDrag(source);
    auto *mime = new QMimeData;
    mime->setText(QStringLiteral("item-42"));
    drag->setMimeData(mime); // 所有权转移给 drag
    drag->exec(Qt::CopyAction | Qt::MoveAction, Qt::CopyAction);
}
```

`QDrag` 是 `QObject`，构造时应传入稳定的 `dragSource`，通常直接传发起拖动的 widget。`setMimeData()` 会接管传入 `QMimeData` 的所有权；不要在调用后继续手动删除它，也不要把栈对象地址传入。

拖动返回后，再根据结果更新源模型：

```cpp
const Qt::DropAction result =
    drag->exec(Qt::CopyAction | Qt::MoveAction, Qt::MoveAction);
if (result == Qt::MoveAction) {
    // 只有目标真正完成移动时，才从源模型移除原项。
}
```

## 3. `exec()` 的动作语义

第一个重载只接收支持动作，默认动作由 Qt 按 `MoveAction`、`CopyAction`、`LinkAction` 的顺序从支持集合中选择。第二个重载允许显式给出默认动作：

```cpp
drag->exec(Qt::CopyAction | Qt::MoveAction, Qt::CopyAction);
```

第二个参数必须是第一参数所支持的动作之一；若传入 `IgnoreAction` 或不在支持集合中的动作，不应把它当作可执行的默认动作。最终返回值是目标实际接受的动作，未完成或被取消时通常为 `Qt::IgnoreAction`。

`exec()` 会启动平台拖放会话。Linux 和 macOS 上拖动期间 Qt 事件循环通常不会被阻塞；Windows 上 Qt 会以不同方式处理事件，嵌套事件循环和重入代码可能影响拖动期间的状态。不要在 `exec()` 尚未返回时假定源模型已经完成最终移动，也不要把大量不可重入的同步逻辑塞进拖动启动路径。

## 4. MIME 数据、图像与热点

### 4.1 MIME 数据

`QMimeData` 可以同时提供文本、URL、图片或自定义 MIME 类型。目标应先用 `hasFormat()` 判断，再读取对应数据。自定义二进制格式必须定义稳定的编码和版本，不要依赖进程内指针或对象地址。

`mimeData()` 返回当前数据对象。它通常只在拖动会话期间有效；`QDrag` 析构时会销毁由它拥有的 MIME 数据。目标事件中的 `mimeData()` 是只读指针，目标不应删除。

### 4.2 拖动图像

`setPixmap()` 和 `setHotSpot()` 必须在 `exec()` 前设置。热点是相对于拖动 pixmap 左上角的像素坐标，表示鼠标指针落在图像的哪一点：

```cpp
drag->setPixmap(icon.pixmap(32, 32));
drag->setHotSpot(QPoint(16, 16));
```

热点可以在图像矩形外，但这通常会导致视觉位置和命中位置不直观；应用层应自行限制到合理区域。没有设置 pixmap 时由平台显示默认拖动反馈。

### 4.3 自定义拖动光标

`setDragCursor()` 为某个 drop action 指定拖动期间的光标。传入空 `QPixmap` 可以恢复平台原生光标。`IgnoreAction` 在 Windows 上不支持自定义光标；跨平台代码应为 `CopyAction`、`MoveAction` 和 `LinkAction` 分别准备资源，并允许平台回退。

## 5. 源、目标与信号

`source()` 返回构造时的拖动源，通常是一个 widget，但类型是 `QObject *`，因此也可以由其他 QObject 发起。`target()` 返回当前拖动目标；没有目标时为 `nullptr`，外部拖动或平台尚未报告目标时也可能为空。

- `actionChanged(Qt::DropAction)`：当前拖动动作变化，例如目标或修饰键改变；
- `targetChanged(QObject *)`：鼠标进入或离开新的目标对象。

信号只反映拖动会话中的状态，不保证目标已经完成业务操作。真正决定源模型是否删除、文件是否移动，应以 `exec()` 返回结果和目标处理结果为准。

## 6. 何时开始拖动

`QDrag` 不会自动监听鼠标。Widgets 中通常采用以下逻辑：

1. 在 `mousePressEvent()` 保存按下位置和当前项；
2. 在 `mouseMoveEvent()` 判断移动距离是否达到 `QApplication::startDragDistance()`；
3. 创建 `QDrag`，准备 MIME 数据；
4. 设置 pixmap 和热点；
5. 调用 `exec()`；
6. 根据返回动作更新模型。

不要在每次鼠标移动时都创建 `QDrag`，否则会产生意外的拖动会话。也不要在 `exec()` 返回前删除拖动源所依赖的临时数据。

## 7. 线程、平台和取消

拖放是 GUI 平台交互，`QDrag` 应在 GUI 线程创建和执行。不要从工作线程直接启动它；后台数据准备完成后，通过 queued signal 把结果交给 GUI 线程。

`cancel()` 请求取消当前拖动。Qt 当前主要在 Windows 和 X11 平台实现该静态操作；其他平台可能没有等价效果。取消不是跨平台的业务回滚通知，源模型仍应检查 `exec()` 返回值。

## 8. 常见错误

- `setMimeData()` 后又 `delete mime`：造成悬空指针或双重释放；
- 在 `exec()` 后才设置 pixmap 或热点：本次拖动不会按预期显示；
- 用 `source()` 判断目标是否接受：它只表示发起源，目标用 `target()` 或 drop 事件判断；
- 不检查返回动作就从列表删除源项：复制、取消和拒绝都会导致数据丢失；
- 把 `Qt::DropAction` 当作位标志使用：支持动作是 `Qt::DropActions`，最终动作是单个枚举值；
- 在拖动对象栈上创建并让其超出作用域：拖动会话仍在运行时对象已经失效。

## 9. 逐项 API 说明

### 构造与析构

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `explicit QDrag(QObject *dragSource)` | 创建一次拖动会话。 | `dragSource` 通常是发起拖动的对象；`QDrag` 不可复制。 |
| `~QDrag()` | 结束并销毁拖动对象。 | 由 QObject 父对象或调用者负责；已交给它的 MIME 数据随之释放。 |

### MIME、图像与热点

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `void setMimeData(QMimeData *data)` | 设置拖动携带的数据。 | 所有权转移给 `QDrag`；不要传栈对象或再次删除。 |
| `QMimeData *mimeData() const` | 取得当前 MIME 数据。 | 返回对象由 `QDrag` 管理；不要删除。 |
| `void setPixmap(const QPixmap &)` | 设置拖动反馈图像。 | 应在 `exec()` 前调用。 |
| `QPixmap pixmap() const` | 读取拖动反馈图像。 | 未设置时可能是空 pixmap。 |
| `void setHotSpot(const QPoint &hotspot)` | 设置鼠标相对于 pixmap 的热点。 | 坐标以 pixmap 左上角为原点。 |
| `QPoint hotSpot() const` | 读取热点。 | 仅影响拖动反馈定位，不改变 drop 坐标。 |

### 会话与动作

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `Qt::DropAction exec(Qt::DropActions supportedActions = Qt::MoveAction)` | 启动拖动并返回最终动作。 | 可能运行平台拖放循环；返回 `IgnoreAction` 表示未完成有效动作。 |
| `Qt::DropAction exec(Qt::DropActions supportedActions, Qt::DropAction defaultAction)` | 启动拖动并指定默认动作。 | `defaultAction` 应属于 `supportedActions`。 |
| `Qt::DropActions supportedActions() const` | 查询声明支持的动作集合。 | 只表示源愿意支持什么，不表示目标一定接受。 |
| `Qt::DropAction defaultAction() const` | 查询默认动作。 | 最终结果仍以 `exec()` 返回值为准。 |
| `static void cancel()` | 请求取消当前拖动。 | 主要支持 Windows 和 X11；不要依赖其在所有平台等效。 |

### 目标、光标与信号

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QObject *source() const` | 查询拖动源。 | 通常非空；返回的是构造时的 QObject，不是 MIME 数据。 |
| `QObject *target() const` | 查询当前目标。 | 目标可能为空，且会随指针移动变化。 |
| `void setDragCursor(const QPixmap &cursor, Qt::DropAction action)` | 为动作设置拖动光标。 | 空 pixmap 恢复原生光标；Windows 不支持 `IgnoreAction`。 |
| `QPixmap dragCursor(Qt::DropAction action) const` | 查询动作对应的拖动光标。 | 没有自定义光标时可能为空。 |
| `actionChanged(Qt::DropAction)` | 通知当前动作变化。 | 不等价于目标已经完成 drop。 |
| `targetChanged(QObject *newTarget)` | 通知当前目标变化。 | `newTarget == nullptr` 表示暂时没有目标。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDrag(QObject *dragSource)` | 创建拖动会话。 | 在 GUI 线程创建，源对象要保持有效。 |
| 数据 | `setMimeData()` / `mimeData()` | 携带文本、URL、图片或自定义数据。 | `setMimeData()` 转移所有权。 |
| 反馈 | `setPixmap()` / `pixmap()` | 设置拖动预览图像。 | 在 `exec()` 前设置。 |
| 反馈 | `setHotSpot()` / `hotSpot()` | 调整指针与预览图的相对位置。 | 相对于 pixmap 左上角。 |
| 会话 | `exec(actions)` | 启动拖放并得到最终动作。 | 可能进入平台拖动循环；检查返回值。 |
| 会话 | `exec(actions, defaultAction)` | 启动拖放并指定默认动作。 | 默认动作应属于支持集合。 |
| 状态 | `source()` / `target()` | 查询拖动源和当前目标。 | 目标可为空且会变化。 |
| 状态 | `supportedActions()` / `defaultAction()` | 查询动作策略。 | 支持集合不代表目标必然接受。 |
| 光标 | `setDragCursor()` / `dragCursor()` | 自定义不同动作的拖动光标。 | 空 pixmap 恢复原生光标；注意平台差异。 |
| 控制 | `cancel()` | 请求取消拖动。 | 主要是 Windows、X11 能力。 |
| 信号 | `actionChanged()` | 观察当前动作变化。 | 不替代 `exec()` 返回值。 |
| 信号 | `targetChanged()` | 观察目标变化。 | `nullptr` 表示没有当前目标。 |

---

### 一句话总结

`QDrag` 负责一次拖放会话：用 `QMimeData` 描述内容、用 `DropActions` 描述意图、用事件让目标决定结果，最后以 `exec()` 的返回值更新源模型。
