# QIconDragEvent

> Qt 6.11.1 · Qt GUI · 来自 `QIconDragEvent`

## 1. 先建立直觉

`QIconDragEvent` 是 Qt 图标系统发出的拖拽启动请求。它不等同于 `QDragEnterEvent`、`QDropEvent` 那类“拖放正在经过目标”的事件；它发生在图标对象希望宿主开始一次拖拽时。

这个类本身没有位置、MIME 数据或目标动作信息，因为那些内容尚未由它决定。收到事件的一方需要知道当前图标代表什么资源，然后创建 `QDrag` 和 `QMimeData`，再执行真正的拖放流程。

## 2. 类说明

`QIconDragEvent` 继承自 `QEvent`，默认未接受。它主要与 `QIcon`、图标引擎以及支持图标拖出的控件协作，普通拖放目标处理仍使用 `QDragEnterEvent`、`QDragMoveEvent`、`QDropEvent`。

类说明只用于表明这个 API 来自 `QIconDragEvent`。事件不携带图标资源内容，应用需要通过上下文、模型索引或图标引擎关联信息决定如何构造拖拽。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QIconDragEvent()` | 构造图标拖拽请求事件，初始接受状态为 false。 |
| `accept()` | 表示宿主已接管并会启动图标拖拽。 |
| `ignore()` | 表示宿主不支持或不处理此次图标拖拽。 |
| `isAccepted()` | 查询请求是否已被接管。 |
| `type()` | 来自 `QEvent`，通常为 `QEvent::IconDrag`。 |

## 4. 关键用法

### 接到请求后创建真正的 `QDrag`

```cpp
void FileIconView::startIconDrag(const QModelIndex &index)
{
    auto *drag = new QDrag(this);
    auto *mime = model()->mimeData({index});

    drag->setMimeData(mime);
    drag->setPixmap(iconPixmap(index));
    drag->exec(Qt::CopyAction | Qt::MoveAction);
}
```

`QIconDragEvent` 只负责“应该开始”的通知。真正的拖放协议从 `QDrag`、`QMimeData` 和 `exec()` 开始。

### 只在确实支持时 accept

如果当前图标只是装饰、没有可导出的资源，或正在编辑状态不允许拖拽，应 `ignore()`，让上层保留默认行为或放弃本次请求。

## 5. 使用场景

`QIconDragEvent` 适合文件浏览器、资源管理器、图片素材库、插件面板、应用启动器和自定义 `QIconEngine` 相关集成。

多数应用不会直接遇到它。直接实现列表、树、表格拖放时，更常用的是 model/view 的 drag flags、`mimeData()` 与 `QDrag`。

## 6. 常见坑与经验

不要期待从事件对象获取拖放数据。它没有 `mimeData()`、位置或动作信息。

不要把它和目标端的 `QDropEvent` 混淆。它是源端开始阶段，drop 事件是目标端结束阶段。

不要在拖拽中使用临时裸指针数据。`QMimeData` 应明确拥有或复制传输内容，拖拽结束后仍需保证资源生命周期正确。

不要默认允许移动操作。支持 Copy、Move、Link 中哪些动作应由业务语义和目标能力决定。

## 7. 知识点覆盖

学习 `QIconDragEvent` 应覆盖图标拖拽请求、源端与目标端区别、`QDrag`、`QMimeData`、拖放动作、模型/视图 drag flags、拖拽视觉预览和资源生命周期。
