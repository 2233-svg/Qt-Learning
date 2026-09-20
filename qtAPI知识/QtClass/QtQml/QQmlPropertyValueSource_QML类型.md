# QQmlPropertyValueSource：让一个 QML 对象持续为另一个属性供值

> Qt 6.11.1 | `#include <QQmlPropertyValueSource>` | CMake: `Qt6::Qml`

`QQmlPropertyValueSource` 是“属性值来源”接口。动画、绑定一类 QML 对象并不是只把一个普通值赋给目标属性，它们会接管该属性并在后续持续提供值；此接口让自定义 C++ 类型也能参与这套机制。

它解决的不是“怎样写一次属性”，而是“引擎把某个对象赋给属性时，怎样让这个对象知道它服务的目标属性是谁”。QML 引擎分配 value source 时会调用 `setTarget(const QQmlProperty &)`.

## 适合的业务场景

例如一个传感器值源需要持续把最新读数写到 QML 项目的 `opacity`；或者一个时间源按时钟更新 `rotation`。把定时器和目标属性的反射细节封进 value source 后，QML 使用者只描述关系：

```qml
Gauge {
    opacity: SensorValue {
        channel: "ambient-light"
    }
}
```

它适合确实“占有目标属性更新权”的对象。若只是一次转换或按钮事件中写属性，普通方法、绑定或 `PropertyChanges` 更直白，也更容易推断。

## 最小实现结构

实现类型必须同时是 QObject 派生类和 `QQmlPropertyValueSource`，并用 `Q_INTERFACES()` 宣告接口：

```cpp
class SensorValue final : public QObject, public QQmlPropertyValueSource
{
    Q_OBJECT
    Q_INTERFACES(QQmlPropertyValueSource)
    QML_ELEMENT

public:
    void setTarget(const QQmlProperty &property) override
    {
        m_target = property;
        applyLatestReading();
    }

private:
    void applyLatestReading()
    {
        if (m_target.isValid() && m_target.isWritable())
            m_target.write(m_latestValue);
    }

    QQmlProperty m_target;
    QVariant m_latestValue;
};
```

`setTarget()` 由 QML 引擎调用，而不是业务代码随意选择时机调用。实现应立即保存或验证 property，建立所需连接，并在对象销毁时停止定时器、断开外部源或释放订阅。

## target 不是一个裸字段

传入的是 `QQmlProperty`，它可能无效、只读、类型不匹配，甚至在错误使用中代表 signal property。因此 value source 至少应检查 `isValid()`、`isProperty()` 和 `isWritable()`，每次 `write()` 都处理 false 返回。

源对象与目标对象的生命周期也不必相同。保存 `QQmlProperty` 不会让目标 QObject 继续存活；目标被销毁后，继续写入没有业务意义。若源会比 target 活得久，额外跟踪 `m_target.object()` 的 `destroyed` 信号，或在每次更新前验证有效性。

## 避免和其它写入者拉扯

value source、动画、QML binding 和 C++ setter 若同时争夺同一个属性，最终值与更新顺序会难以维护。设计时应明确：

- 目标属性由谁持续控制；
- value source 何时停止；
- 外部手工写入是否应取消 source，还是被下一次 source 更新覆盖；
- 目标属性类型、量纲和异常值如何处理。

对于跨线程外部数据，不能从工作线程直接对 `QQmlProperty::write()` 操作 UI 对象。把数据排队回 target 所在线程，再写入。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQmlPropertyValueSource` | 属性值来源的抽象接口 | 不能单独实例化或直接作为 QObject 使用 |
| `Q_INTERFACES(QQmlPropertyValueSource)` | 向元对象系统声明实现接口 | 缺失时 QML 引擎不能将对象识别为 value source |
| `setTarget(const QQmlProperty &)` | 引擎在分配 value source 时交付目标属性 | 由引擎调用；实现应校验、保存并建立更新机制 |
| `QQmlProperty::isValid()` | 判断目标仍可解析 | 不代表该属性一定可写 |
| `QQmlProperty::isWritable()` | 判断目标接受写入 | 类型转换和 setter 仍可能令 `write()` 失败 |
| `QQmlProperty::write()` | 向目标推送新值 | 遵守 target QObject 的线程亲和性 |
| `QQmlPropertyValueSource` 析构 | 结束 value source 的资源和连接 | 停止异步回调，避免目标消失后继续写入 |

## 相关类型

- `QQmlProperty`：value source 接收的目标属性封装。
- `QQmlPropertyValueInterceptor`：用于拦截而非作为值来源的另一类扩展接口。
- `QPropertyAnimation`、QML binding：Qt 内置的持续供值机制。
