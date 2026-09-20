# Qt QChildEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QChildEvent>`  
> 所属模块：`Qt6::Core`  
> 继承：`QEvent`  
> 核心定位：通知 `QObject` 的直接子对象关系正在增加、移除或完成 polish

## 1. 它解决什么问题

`QObject` 的父子关系既决定对象树，也通常决定对象的生命周期。一个对象通过 `setParent()`、构造时传入 parent，或析构时脱离父对象，会使父对象的直接 children 列表发生变化。

`QChildEvent` 是 Qt 在这些变化发生时立即发送给父对象的事件参数。正常代码不手工创建它，而是在重写 `QObject::childEvent(QChildEvent *event)` 时读取它。

```text
QObject parent
  |
  | a direct child is attached / detached
  v
QObject::childEvent(QChildEvent *)
  |
  +-- ChildAdded
  +-- ChildRemoved
  +-- ChildPolished
```

它适用于对象树观察、延迟初始化、通用容器类或框架级调试。普通业务代码若知道自己创建了哪些子对象，通常直接保存指针或连接信号槽更清楚，不应靠 child event 做常规控制流。

## 2. 最重要的规则：对象状态尚不稳定

子事件到达的时机决定了你能对 `event->child()` 做什么：

| 事件类型 | 到达时的状态 | 可以可靠假设什么 | 不应假设什么 |
| --- | --- | --- | --- |
| `QEvent::ChildAdded` | 子对象已加入父对象，但其派生类构造可能未结束。 | 它至少是 `QObject`；若 `isWidgetType()` 为真，可视为 `QWidget`。 | 不要依赖派生类成员、虚函数行为、完整 meta-object 状态或已建立的连接。 |
| `QEvent::ChildRemoved` | 子对象已从父对象脱离；析构路径中它可能已经部分销毁。 | 只应把指针当作离开通知的附带值。 | 不要解引用、调用方法、转换到具体派生类或保存后继续使用。 |
| `QEvent::ChildPolished` | 子对象有机会在构造完成后被 polish。 | 适合补充延迟配置或观察更稳定的 widget 状态。 | 不能假设只会收到一次；Qt 文档明确说明它可能重复。 |

这也是 `childEvent()` 与普通“对象已就绪”信号不同的地方：`ChildAdded` 发生得很早，`ChildRemoved` 发生得很晚。把它们当作“安全可用”和“对象仍有效”的通知，很容易写出偶现崩溃。

## 3. 最小使用示例

下面的类只记录对象树变化，不在 `ChildRemoved` 分支解引用子对象：

```cpp
#include <QChildEvent>
#include <QObject>
#include <QDebug>

class ObjectTreeObserver : public QObject
{
protected:
    void childEvent(QChildEvent *event) override
    {
        if (event->added()) {
            qDebug() << "child attached:" << event->child();
        } else if (event->polished()) {
            qDebug() << "child polished:" << event->child();
        } else if (event->removed()) {
            qDebug() << "child detached:" << event->child();
            // 不要在这里使用 event->child()->objectName() 等成员调用。
        }

        QObject::childEvent(event);
    }
};
```

若父类的 `childEvent()` 有实际行为，保留基类调用。`QObject::childEvent()` 默认实现通常不需要业务处理，但继承层级较深时，省略它可能破坏父类自己依赖的对象树逻辑。

## 4. `ChildPolished` 是什么

对 widget 或依赖 widget polish 的对象，Qt 会在构造过程更靠后的阶段发送 `ChildPolished`。它常被误解为“对象仅在完全初始化后通知一次”，但 Qt 明确允许同一子对象收到多次 polish 事件。

因此这类代码需要幂等：

```cpp
if (event->polished()) {
    auto *widget = qobject_cast<QWidget *>(event->child());
    if (widget && !m_configured.contains(widget)) {
        configureWidget(widget);
        m_configured.insert(widget);
    }
}
```

更常见也更稳妥的方案，是在你创建子对象的位置完成配置，或把初始化放进该对象自己的构造、`showEvent()`、`polishEvent()` 等更贴近职责的生命周期点。`ChildPolished` 比较适合不知道具体子类、但需要观察整个对象树的通用基础设施。

## 5. 与对象所有权和线程的关系

`QChildEvent` 不转移对象所有权。它只报告关系发生过变化：

- `ChildAdded` 不说明父对象一定会最终删除子对象，但 `QObject` 的标准规则通常是在父对象析构时删除仍在其 children 列表中的对象。
- `ChildRemoved` 不说明子对象已经被 `delete`，也可能只是调用了 `setParent(nullptr)` 或换了另一个父对象。
- 父子关系和 child event 遵循 `QObject` 的线程归属约束；不要跨线程直接改变对象父级。需要迁移对象时先理解 `moveToThread()` 与父子关系限制。

事件对象只在 Qt 的事件分发调用期间有效，不应缓存 `QChildEvent *`。若需要延后处理，保存经过验证的必要信息，例如对象的稳定 ID；对子对象指针使用 `QPointer`，并在真正使用前再次检查。

## 6. 适合与不适合的场景

| 场景 | 是否适合 | 原因 | 更直接的替代方案 |
| --- | --- | --- | --- |
| 调试打印对象树变化 | 适合 | 不需依赖具体子类型或长生命周期。 | 无。 |
| 通用容器为未知子 widget 做延迟配置 | 谨慎适合 | 可利用 `ChildPolished`，但配置必须幂等。 | 创建接口、工厂或专用基类。 |
| 监听某个已知对象销毁 | 不适合 | `ChildRemoved` 时可能不能安全解引用。 | 连接 `QObject::destroyed()`，或用 `QPointer`。 |
| 判断用户界面已经完全构建 | 不适合 | `ChildPolished` 可重复且只反映直接子对象。 | 显式初始化阶段或页面完成信号。 |
| 管理业务数据对象的生命周期 | 不适合 | 父子事件只是旁路观察，时机过早或过晚。 | 清晰的所有权模型和智能指针或 QObject 父级。 |

## 7. 常见错误

### 7.1 在 `ChildAdded` 中 `qobject_cast` 后马上调用派生类 API

构造尚未完成，虚派发与成员状态都可能不是你预期的最终状态。最多把对象登记起来，待 `ChildPolished`、显式初始化或事件循环稍后阶段再做需要完整对象的工作。

### 7.2 在 `ChildRemoved` 中访问 `objectName()`

该对象可能正处于析构，访问任何 QObject 成员都不安全。移除通知只用于更新父对象自己的索引或统计，不用于读取子对象状态。

### 7.3 把 `child()` 指针长期保存为裸指针

父对象不拥有该指针的独占有效性；子对象可以重新设父对象或被删除。长期观察请使用 `QPointer<QObject>`，并连接 `destroyed()` 处理清理。

### 7.4 忽略基类 `childEvent()`

如果当前类的父类也依赖 child event，吞掉事件会破坏它的行为。除非能确认基类不需要，否则调用基类实现。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QChildEvent(QEvent::Type type, QObject *child)` | 构造指定子对象和事件类型的子事件。 | 正常由 Qt 创建并发送；`type` 只应是 `ChildAdded`、`ChildRemoved` 或 `ChildPolished`。 |
| 类型判断 | `bool added() const` | 判断 `type()` 是否为 `QEvent::ChildAdded`。 | 子对象可能尚未完成派生类构造，只做最保守的登记或观察。 |
| 类型判断 | `bool polished() const` | 判断 `type()` 是否为 `QEvent::ChildPolished`。 | 可能对同一对象多次为真；初始化逻辑必须幂等。 |
| 类型判断 | `bool removed() const` | 判断 `type()` 是否为 `QEvent::ChildRemoved`。 | 子对象可能已经部分析构，绝不能依赖或解引用 `child()`。 |
| 访问 | `QObject *child() const` | 返回发生关系变化的直接子对象指针。 | 指针不转移所有权，也不保证跨出当前事件后仍有效。 |
| 处理入口 | `void QObject::childEvent(QChildEvent *event)` | `QObject` 接收并处理子对象事件的虚函数。 | 重写时只做与事件时机相符的操作，必要时调用基类实现。 |

---

### 一句话总结

`QChildEvent` 是对象树变化的低层即时通知：新增时对象可能没构造完，移除时对象可能已在析构，只有把这两个时机当成“不稳定边界”来处理，才能安全使用它。
