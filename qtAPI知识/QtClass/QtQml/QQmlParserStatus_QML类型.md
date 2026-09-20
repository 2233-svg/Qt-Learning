# QQmlParserStatus：知道 QML 何时把一个对象真正配置完成

> Qt 6.11.1 | `#include <QQmlParserStatus>` | CMake: `Qt6::Qml`

`QQmlParserStatus` 给由 `QQmlEngine` 创建的 C++ QML 类型两个生命周期回调：对象构造后、属性赋值前的 `classBegin()`，以及造成该实例的根组件构造完成后的 `componentComplete()`。它解决的是初始化期间属性多次写入导致昂贵计算反复执行的问题。

典型例子是文本布局：`text`、`font`、`width` 在组件创建时陆续赋值。每个 setter 都立即布局，会得到多次无用工作；等 `componentComplete()` 再布局，则只做一次。

## 正确的多重继承方式

该接口必须和 `QObject` 派生类一起使用，并用 `Q_INTERFACES()` 让元对象系统识别接口：

```cpp
class PlotItem : public QQuickItem, public QQmlParserStatus
{
    Q_OBJECT
    Q_INTERFACES(QQmlParserStatus)

public:
    void classBegin() override
    {
        m_constructingFromQml = true;
    }

    void componentComplete() override
    {
        m_constructingFromQml = false;
        rebuildGeometry();
    }

private:
    bool m_constructingFromQml = false;
};
```

setter 中据此只记录脏状态，或者在 `m_constructingFromQml` 为 false 时立即更新：

```cpp
void PlotItem::setSamples(const QList<QPointF> &samples)
{
    if (m_samples == samples)
        return;

    m_samples = samples;
    if (!m_constructingFromQml)
        rebuildGeometry();
}
```

实际类型还应在 `componentComplete()` 中处理 `m_dirty`，以保证 QML 初始化结束时必定应用初始化期间的改动。

## 两个回调的时序

`classBegin()` 在类对象创建之后、任何属性被设定之前调用。这里适合开始“延迟模式”，不要依赖 QML 属性值。

`componentComplete()` 在触发该对象实例化的根组件完成构造之后调用。静态赋值和绑定初值都已经写入，因此适合依赖多个属性一致组合的初始化。它并不表示未来绑定不再改变；后续属性变化仍会走常规 setter 和通知。

尤其要注意：不是每创建一个嵌套对象就立即完成回调，而是相关根组件的构造整体完成后才进入 `componentComplete()`。所以不要把它当作子对象逐个可用的唯一同步点。

## C++ 直接创建不会得到回调

只有 `QQmlEngine` 实例化类型时才自动调用这些函数：

```cpp
auto *item = new PlotItem; // 不会自动调用 classBegin/componentComplete
```

因此不应该从构造函数开始永久压制更新，再单纯依赖 `componentComplete()` 解锁；C++ 创建路径会永远停在延迟状态。推荐策略是只在 `classBegin()` 开启延迟。这样 QML 创建会合并初始化期的多次变更，而 C++ 直接 `new` 后 setter 仍正常即时生效。

接口本身没有提供“对象已完成”的查询 API；需要这个状态时，在派生类维护自己的布尔值并明确其业务含义。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQmlParserStatus` | 供元对象系统识别的生命周期接口 | 不能单独作为 QML 对象使用 |
| `Q_INTERFACES(QQmlParserStatus)` | 声明 QObject 实现了该接口 | 缺失时引擎无法按接口发现回调 |
| `classBegin()` | 对象创建后、任何 QML 属性赋值前调用 | 不要读取尚未赋值的配置；在这里开始延迟工作 |
| `componentComplete()` | 根组件构造完成、静态值和绑定初值写入后调用 | 后续绑定仍可能变化，不能把它当作唯一更新机会 |
| 直接 C++ 构造 | 不触发接口回调 | 不要把 C++ 路径设计成必须等待 `componentComplete()` |
| 属性 setter | 初始化期先记录脏状态，完成后统一处理 | 仍要正确处理组件完成后的普通属性变更 |

## 相关类型

- `QQmlEngine`：只有它创建对象时，接口回调才自动发生。
- `QObject`、`Q_INTERFACES`：让运行时元对象系统识别多重继承接口。
- `QQuickItem`：自定义视觉 QML 类型常用的 QObject 基类。
