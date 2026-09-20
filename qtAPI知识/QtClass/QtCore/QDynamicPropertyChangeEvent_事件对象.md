# Qt QDynamicPropertyChangeEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDynamicPropertyChangeEvent>`  
> 所属模块：`Qt6::Core`  
> 继承：`QEvent`  
> 定位：动态属性变更通知事件

## 1. 它解决什么问题

`QDynamicPropertyChangeEvent` 用来通知 `QObject`：某个**动态属性**被添加、修改或移除了。

Qt 的属性有两种来源：

- `Q_PROPERTY` 在类编译时声明，是元对象的一部分；
- `QObject::setProperty()` 运行时写入一个未在元对象中声明的名字，形成动态属性。

动态属性很适合给通用控件、Qt Designer 表单、插件对象或不方便修改 C++ 类定义的对象附加少量配置。例如：

```cpp
button->setProperty("role", "primary");
button->setProperty("validationState", "error");
```

当动态属性变化时，Qt 向对象发送 `QEvent::DynamicPropertyChange`，事件对象就是 `QDynamicPropertyChangeEvent`。

它解决的是“属性变化后，接收者如何知道哪个名字变了”的问题，而不是“把新值装进事件里”。事件只携带属性名；处理函数需要回到接收对象上调用 `property()` 读取当前值。

## 2. 最小可用模式

```cpp
#include <QDebug>
#include <QDynamicPropertyChangeEvent>
#include <QEvent>
#include <QObject>
#include <QVariant>

class ConfigObject : public QObject
{
public:
    using QObject::QObject;

protected:
    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::DynamicPropertyChange) {
            auto *change =
                static_cast<QDynamicPropertyChangeEvent *>(event);
            const QByteArray name = change->propertyName();
            const QVariant value = property(name.constData());

            if (value.isValid())
                qDebug() << "property changed:" << name << value;
            else
                qDebug() << "property removed:" << name;

            return true;
        }

        return QObject::event(event);
    }
};
```

使用：

```cpp
ConfigObject object;
object.setProperty("mode", "safe");       // 添加动态属性
object.setProperty("mode", "fast");       // 修改动态属性
object.setProperty("mode", QVariant{});   // 移除动态属性
```

这里 `QVariant{}` 是无效 QVariant。对动态属性设置无效值会移除它；事件中的 `propertyName()` 仍然返回 `"mode"`，所以可以用 `property()` 的有效性判断当前是“有值”还是“已移除”。

## 3. 事件是怎样产生的

### 3.1 由 `QObject::setProperty()` 触发

```cpp
object.setProperty("theme", "dark");
```

如果 `"theme"` 不是类中通过 `Q_PROPERTY` 声明的属性，它会被作为动态属性保存。动态属性添加、值改变或移除时，Qt 会发送动态属性变更事件。

`QObject::setProperty()` 的返回值容易被误读：对静态 `Q_PROPERTY` 成功写入通常返回 `true`；对未声明名字创建或修改动态属性时返回 `false`，这不等于动态属性操作失败。是否为动态属性，应结合元对象和 `dynamicPropertyNames()` 判断，而不能只看这个布尔值。

### 3.2 事件只报告名字，不携带旧值和新值

```cpp
const QByteArray name = change->propertyName();
const QVariant current = property(name.constData());
```

事件没有旧值，也没有独立保存“新值”的字段。需要比较前后差异时，接收者必须自己缓存之前的值，或者在业务层维护一份状态：

```cpp
if (name == "mode") {
    const QVariant next = property("mode");
    if (next != m_lastMode) {
        m_lastMode = next;
        applyMode(next);
    }
}
```

### 3.3 事件处理时读取对象当前状态

事件是发给对象本身的。通常在重写 `event()` 时直接调用 `property(name)`；不要把事件对象保存到成员变量中，等以后再读取。事件由 Qt 的事件分发流程管理，处理返回后其生命周期就不再由业务代码掌控。

## 4. 动态属性的实际使用场景

### 4.1 给通用控件附加样式或业务标签

```cpp
auto *label = new QLabel;
label->setProperty("severity", "warning");
label->setProperty("featureId", 42);
```

样式表可以读取动态属性作为选择条件，业务代码也可以在事件中监听属性变化并刷新展示。动态属性适合低频配置，不适合代替有明确类型约束的领域模型。

### 4.2 让容器对象响应插件配置

插件系统可能只知道一个 `QObject *`，无法依赖具体派生类。调用方可以设置约定好的动态属性名，插件对象在事件中读取这些属性并重新配置。

这要求双方共享稳定的属性名、类型和移除语义。属性名建议集中定义，避免在多个模块里散落字符串字面量。

### 4.3 观察 Qt Designer 或运行时表单属性

动态属性是 Qt Designer 支持的常见扩展方式。若控件需要在运行时对动态属性变化作出反应，重写 `event()` 通常比频繁轮询 `dynamicPropertyNames()` 更直接。

## 5. 关键边界

### 5.1 不要把它当成属性信号

`QDynamicPropertyChangeEvent` 是事件，不是 `void propertyChanged(name, value)` 信号。它通过 `QObject::event()` / 事件过滤器到达对象：

```cpp
class PropertyObserver : public QObject
{
protected:
    bool eventFilter(QObject *watched, QEvent *event) override
    {
        if (event->type() == QEvent::DynamicPropertyChange) {
            auto *change =
                static_cast<QDynamicPropertyChangeEvent *>(event);
            qDebug() << watched << change->propertyName();
        }
        return QObject::eventFilter(watched, event);
    }
};
```

如果只是想让业务对象发出强类型通知，直接定义信号通常更清晰；动态属性事件适合通用观察、控件扩展和元对象层集成。

### 5.2 不能用事件名推断属性一定存在

收到事件时属性可能刚被移除，或者业务代码在事件处理前后再次修改了它。应以 `property()` 的当前结果为准，必要时用 `dynamicPropertyNames()` 确认它是否仍是动态属性。

### 5.3 `_q_` 前缀是 Qt 保留空间

Qt 文档明确保留以 `_q_` 开头的动态属性名供内部使用。应用和插件不要使用这类名字，避免与 Qt 内部实现冲突。

### 5.4 事件处理返回值要有明确语义

如果派生类已经完整处理这个动态属性事件，可以返回 `true`；如果只观察但仍希望基类继续处理，应调用并返回 `QObject::event(event)` 的结果。事件过滤器同理，不要无条件吞掉所有事件。

## 6. 与相关 API 的协作

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QObject::setProperty()` | 添加、修改或移除属性 | 动态属性写入时返回值可能仍为 `false` |
| `QObject::property()` | 读取当前属性值 | 属性不存在或已移除时返回无效 `QVariant` |
| `QObject::dynamicPropertyNames()` | 列出当前动态属性名 | 返回的是名称列表，不携带属性值 |
| `QObject::event()` | 接收对象事件 | 重写时保留其它事件的基类处理 |
| `QObject::installEventFilter()` | 在不修改目标类的情况下观察事件 | 过滤器对象必须与被观察对象处于同一线程 |
| `QEvent::DynamicPropertyChange` | 标识动态属性变化事件类型 | 需要先判断 `event->type()` 再进行安全转换 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QDynamicPropertyChangeEvent(const QByteArray &name)` | 创建一个动态属性变化事件，并记录发生变化的属性名 | 通常由 Qt 在 `QObject::setProperty()` 流程中创建；业务代码一般不需要手动发送 |
| 查询 | `QByteArray propertyName() const` | 返回被添加、修改或移除的动态属性名 | 只返回名字，不返回旧值或新值；需要值时回到接收对象调用 `property()` |
| 事件类型 | `QEvent::DynamicPropertyChange` | 标识动态属性发生添加、修改或移除 | 先判断 `event->type()`，再转为 `QDynamicPropertyChangeEvent *` |
| 关联 API | `QObject::setProperty(const char *, const QVariant &)` | 写入静态或动态属性，并触发动态属性变更事件 | 设置无效 QVariant 会移除动态属性；动态属性路径的返回值不要按静态属性成功语义解释 |
| 关联 API | `QObject::property(const char *)` | 查询当前属性值 | 返回无效 QVariant 可能表示属性不存在或已移除 |
| 关联 API | `QObject::dynamicPropertyNames() const` | 返回当前动态属性名 | 需要判断属性是否仍存在时使用；不会告诉你属性类型 |

## 8. 一句话总结

`QDynamicPropertyChangeEvent` 是动态属性变化的事件通知；它只携带属性名，处理时要回到接收对象读取当前值，并区分添加、修改与用无效 `QVariant` 移除的边界。
