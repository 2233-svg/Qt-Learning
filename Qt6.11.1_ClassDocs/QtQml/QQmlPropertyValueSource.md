# QQmlPropertyValueSource
> Qt 6.11.1 · Qt QML · 来自 `QQmlPropertyValueSource`

## 作用定位

`QQmlPropertyValueSource` 是“给某个属性提供值”的接口。实现它的对象在 QML 中被用作属性值源时，QML 引擎会调用 `setTarget()`，把目标 `QQmlProperty` 交给它。典型例子是动画、绑定辅助器、状态驱动器这类对象。

## 类说明

- 头文件：`#include <QQmlPropertyValueSource>`
- CMake：链接 `Qt6::Qml`
- 继承：接口类，无公开 QObject 继承要求；实际类型通常也继承 QObject
- 必须实现：`setTarget(const QQmlProperty &property)`

## API 速查

| API | 说明 |
| --- | --- |
| `QQmlPropertyValueSource()` | 构造接口基类。 |
| `~QQmlPropertyValueSource()` | 虚析构，允许通过接口销毁派生对象。 |
| `setTarget(property)` | QML 引擎告诉 value source 它要驱动哪个属性。 |

## 使用场景

- 编写类似动画、行为、动态值源的 QML 类型。
- 属性值不是一次性赋值，而是由一个对象持续更新。
- 需要在 C++ 中接收目标属性并自己控制写入时机。

## 常见坑与经验

- `setTarget()` 里要检查 `property.isValid()` 和 `property.isWritable()`。
- value source 持有目标属性时，要考虑目标对象销毁后的失效问题。
- 更新属性要避免自触发循环：写入属性可能触发绑定、信号，再反过来调用自身逻辑。
- 如果只是普通赋值，不需要这个接口；它面向持续驱动或延迟驱动属性的对象。

## 知识点覆盖

- QML 属性值源协议
- `QQmlProperty` 作为目标句柄
- 持续驱动属性
- 自定义动画/行为类基础
