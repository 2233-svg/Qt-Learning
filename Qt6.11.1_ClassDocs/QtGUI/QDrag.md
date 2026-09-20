# QDrag

> Qt 6.11.1 · Qt GUI · 来自 `QDrag`

## 1. 先建立直觉

`QDrag` 表示一次正在启动的拖拽操作。源控件创建它，放入 `QMimeData`，设置可选拖拽图像，然后调用 `exec()` 交给 Qt 和操作系统完成拖放协商。

它是拖拽“源端”的对象；目标端接收的是 drag enter/move/drop 事件。

## 2. 类说明

`QDrag` 继承自 `QObject`。构造时传入 drag source，`setMimeData()` 后由 `QDrag` 接管 MIME 数据所有权。`exec()` 会启动拖拽循环，并返回最终执行的 `Qt::DropAction`。

拖拽动作不是源端单方面决定的。源端声明支持 Copy/Move/Link，目标端选择接受哪个动作，用户修饰键也可能影响结果。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QDrag(QObject *dragSource)` | 创建拖拽对象并指定源对象。 |
| `setMimeData(QMimeData *)` / `mimeData()` | 设置或读取拖拽携带数据。 |
| `setPixmap()` / `pixmap()` | 设置拖拽时跟随鼠标的图像。 |
| `setHotSpot()` / `hotSpot()` | 设置 pixmap 中对准光标的热点。 |
| `setDragCursor()` / `dragCursor()` | 为不同 drop action 设置光标图像。 |
| `exec(supportedActions)` | 启动拖拽并返回最终 action。 |
| `exec(supportedActions, defaultAction)` | 指定支持动作和默认动作。 |
| `supportedActions()` | 返回本次拖拽支持的动作。 |
| `defaultAction()` | 返回默认动作。 |
| `source()` | 返回拖拽源对象。 |
| `target()` | 返回当前目标对象。 |
| `cancel()` | 静态函数，尝试取消当前拖拽。 |
| `actionChanged()` | 当前 drop action 改变时发出。 |
| `targetChanged()` | 当前目标改变时发出。 |

## 4. 关键用法

```cpp
auto *drag = new QDrag(this);
auto *mime = new QMimeData;
mime->setText(selectedText);
drag->setMimeData(mime);
drag->setPixmap(renderDragPreview());
drag->setHotSpot(QPoint(8, 8));

const Qt::DropAction result = drag->exec(Qt::CopyAction | Qt::MoveAction,
                                         Qt::CopyAction);
if (result == Qt::MoveAction)
    removeOriginalSelection();
```

## 5. 使用场景

适合列表/树项拖拽、文件拖出、画布对象拖放、跨应用文本/图片/URL 拖动、素材库拖到编辑区。

如果只是控件内部移动对象，不需要跨目标协商数据，普通 mouse move 也可能更简单。

## 6. 常见坑与经验

`setMimeData()` 后不要删除 mime 对象，`QDrag` 会接管。

Move 动作通常要等 `exec()` 返回后再删除源数据，不能一开始拖就删。

拖拽预览 pixmap 应小而清楚。大图会拖慢拖动，也会遮挡目标。
