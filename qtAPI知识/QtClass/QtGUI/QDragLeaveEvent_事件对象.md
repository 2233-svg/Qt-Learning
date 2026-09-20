# Qt QDragLeaveEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDragLeaveEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QDragLeaveEvent`  
> 定位：拖动离开当前接收对象时的清理通知

## 1. 它解决什么问题

`QDragLeaveEvent` 告诉拖放目标：此前进入并可能被接受的拖动已经离开当前对象。它没有位置、MIME 数据或动作查询 API，职责非常集中：撤销 `dragEnterEvent()` 或 `dragMoveEvent()` 中建立的临时视觉和命中状态。

典型场景：

- 清除拖动悬停高亮；
- 取消“将在此处插入”的占位线；
- 恢复默认光标或边框；
- 释放仅为预览而创建的临时资源。

它不是 drop 失败的详细报告。用户也可能把拖动移到另一个子控件或窗口，源还可能继续进入别的目标。

## 2. 构建与事件入口

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::Widgets)
```

```cpp
#include <QDragLeaveEvent>

void DropWidget::dragLeaveEvent(QDragLeaveEvent *event)
{
    Q_UNUSED(event);
    clearDropPreview();
}
```

要接收拖放，widget 仍需启用 `setAcceptDrops(true)`。事件对象由 Qt 在事件分发期间管理，不要保存指针，也不要试图从它读取 MIME 数据。

## 3. 事件时序

常见顺序为：

```text
dragEnterEvent -> dragMoveEvent ... -> dragLeaveEvent
                              \-> dropEvent
```

成功 drop 时通常走 `dropEvent()`，而不是把 `dragLeaveEvent` 当成失败回调。代码应让高亮清理既能在离开事件中执行，也能在 drop 完成后执行，避免成功落下后残留预览。

复合控件中，进入父 widget 后可能进入子 widget；不要把“离开父控件”误解为拖动已经离开整个窗口。

## 4. 接受状态与手动构造

`QDragLeaveEvent` 继承 `QEvent`，可以使用 `accept()`、`ignore()`、`isAccepted()`。多数清理处理不需要修改接受状态；如果事件过滤器或父对象依赖传播状态，再明确选择。

```cpp
QDragLeaveEvent event;
event.accept();
```

手动构造主要用于单元测试。正常拖放流程由 Qt 平台插件创建并投递；手动发送事件不会模拟真实平台拖动，也不会自动生成后续 `QDropEvent`。

## 5. 常见错误

- 把 `QDragLeaveEvent` 当作 drop 事件并尝试读取 MIME；
- 只在 `dropEvent()` 清理高亮，拖出控件时预览一直存在；
- 在离开事件中删除源模型数据；
- 保存事件指针给异步任务使用；
- 忽略子控件转移导致的正常离开/进入事件。

## 6. 逐项 API 说明

### `QDragLeaveEvent()`

默认构造一个拖动离开事件。它不携带位置、动作或 MIME 数据，初始类型是 `QEvent::DragLeave`。应用通常只在测试中直接创建它。

### 从 `QEvent` 继承的常用成员

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `accept()` | 标记当前对象接受事件。 | 接受不表示拖放成功。 |
| `ignore()` | 标记当前对象未处理事件。 | 只有确实需要传播时才使用。 |
| `isAccepted() const` | 查询接受状态。 | 不要用它判断 drop action。 |
| `type() const` | 查询事件类型。 | 应为 `QEvent::DragLeave`。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDragLeaveEvent()` | 创建离开事件。 | 普通代码很少手动构造。 |
| 清理 | `dragLeaveEvent(QDragLeaveEvent *)` | 清除拖动悬停状态。 | 事件指针只在处理函数内有效。 |
| 状态 | `accept()` / `ignore()` | 控制事件处理状态。 | 不表示拖放成功或失败动作。 |
| 查询 | `isAccepted()` | 查看事件是否已接受。 | 与 `dropAction()` 无关。 |
| 查询 | `type()` | 确认事件类型。 | 运行时类型应为 `DragLeave`。 |

---

### 一句话总结

`QDragLeaveEvent` 不是“放下失败”的数据报告，而是拖动离开接收对象时的清理通知。
