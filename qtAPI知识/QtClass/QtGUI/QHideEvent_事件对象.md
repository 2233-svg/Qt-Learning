# Qt QHideEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHideEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QHideEvent`  
> 定位：widget 被隐藏时的生命周期通知

## 1. 它解决什么问题

`QHideEvent` 表示 widget 已经变为不可见。它常由调用 `hide()`、隐藏父对象、切换页面、关闭窗口或界面状态变化触发。控件可以在 `hideEvent()` 中停止仅为显示服务的活动，例如闪烁动画、预览更新、临时悬停状态或昂贵刷新。

隐藏不是销毁。对象、模型、连接和大部分状态仍然可能继续存在，之后还可能收到 `QShowEvent`。因此 `hideEvent()` 适合暂停和清理临时呈现状态，不适合无条件释放仍会复用的业务数据。

## 2. 事件入口

```cpp
#include <QHideEvent>
#include <QWidget>

class PreviewWidget : public QWidget
{
protected:
    void hideEvent(QHideEvent *event) override
    {
        stopPreviewTimer();
        QWidget::hideEvent(event);
    }
};
```

一般让基类继续处理。若计时器或后台任务仍要运行，是否暂停取决于任务是否只服务于当前可见 UI，而不是由“收到 hide 事件”机械决定。

## 3. 与关闭、禁用和销毁的区别

- `hide()`：改变可见性，widget 可以稍后 `show()`；
- `close()`：触发 `QCloseEvent`，可被忽略或接受，随后窗口通常隐藏，是否删除取决于属性和代码；
- `setEnabled(false)`：控件不可交互，但不一定隐藏；
- 析构：对象生命周期结束，不保证能把 `hideEvent()` 当作唯一清理出口。

不要把 `hideEvent()` 当作关闭确认点或资源释放的唯一位置。必须在析构中释放的资源仍要由 RAII、父子对象关系或析构函数管理。

## 4. 事件传播与可见性层级

父 widget 隐藏时，子 widget 也可能接收隐藏相关通知。复合控件内若每个子项都暂停同一共享任务，可能出现重复操作；共享资源应由明确的所有者统一管理。

隐藏过程中不要假设 `isVisible()` 的每个中间状态都适合作为业务状态机输入。对“当前页面是否活动”等概念，优先维护明确的业务状态，而不是只监听一个 UI 事件。

## 5. 常见错误

- 在 `hideEvent()` 中删除对象，导致以后 `show()` 访问悬空状态；
- 把隐藏当成用户关闭或取消操作；
- 不调用基类实现，影响父类的显示状态维护；
- 子控件各自停止/启动同一个共享服务；
- 只依赖 `hideEvent()` 清理资源，忽略析构路径；
- 在 GUI 线程外直接调用 widget 可见性 API。

## 6. 逐项 API 说明

### `QHideEvent()`

构造隐藏事件。正常由 Qt 在可见性变化时发送，应用仅在测试中直接构造。它不携带隐藏原因、位置或关闭结果。

### 从 `QEvent` 继承的常用成员

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `type()` | 查询事件类型。 | 正常为 `QEvent::Hide`。 |
| `accept()` / `ignore()` | 设置事件处理状态。 | 不能阻止 widget 已经隐藏。 |
| `isAccepted()` | 查询处理状态。 | 不表示 widget 仍可见。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QHideEvent()` | 创建隐藏事件。 | 一般只用于测试。 |
| 入口 | `QWidget::hideEvent()` | 暂停可见性相关工作。 | 隐藏不等于销毁。 |
| 查询 | `type()` | 确认事件类型。 | 正常是 `QEvent::Hide`。 |
| 状态 | `accept()` / `ignore()` | 设置处理状态。 | 不能撤销隐藏。 |
| 协作 | `QShowEvent` | 恢复可见性相关工作。 | 停止和恢复应成对设计。 |
| 协作 | `QCloseEvent` | 处理可取消的关闭请求。 | 不要将二者混为一谈。 |

---

### 一句话总结

`QHideEvent` 是“暂时不显示”的通知：暂停只为 UI 服务的工作即可，永久资源和业务状态仍要按对象生命周期管理。
