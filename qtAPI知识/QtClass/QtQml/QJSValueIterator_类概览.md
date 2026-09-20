# QJSValueIterator：枚举 QJSValue 自身的属性

> Qt 6.11.1 · `#include <QJSValueIterator>` · 模块：`Qt6::Qml`

`QJSValueIterator` 是 Java 风格迭代器，用于遍历 `QJSValue` 对象的**自身属性**。它适合读取脚本插件返回的配置对象、输出调试信息、把显式字段复制到 C++ 数据结构；它不是遍历原型链的反射工具，也不是可修改的 STL 迭代器。

## 正确的遍历顺序

构造后迭代器位于第一个属性之前。每轮先判断 `hasNext()`，再调用 `next()`，最后读取 `name()` 和 `value()`：

```cpp
#include <QJSEngine>
#include <QJSValueIterator>
#include <QDebug>

QJSEngine engine;
QJSValue settings = engine.evaluate(u"({ theme: 'dark', retries: 3 })"_s);

QJSValueIterator it(settings);
while (it.hasNext()) {
    it.next();
    qDebug() << it.name() << it.value().toVariant();
}
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## 它遍历什么，不遍历什么

迭代器只枚举对象自身的属性，**不会沿原型链继续枚举**。这与 `QJSValue::hasProperty()` 的原型链查找语义不同。

若确实需要检查整条原型链，只能自己分层：

```cpp
for (QJSValue current = object; current.isObject(); current = current.prototype()) {
    QJSValueIterator it(current);
    while (it.hasNext()) {
        it.next();
        // 这里只处理 current 自己的属性
    }
}
```

这种做法还要自行处理同名字段遮蔽和潜在原型问题；业务数据一般只应关注自身字段。

## 使用边界

- 先确认目标是对象；非对象不会被“展开”为属性集合。
- `value()` 返回 `QJSValue`，字段 getter 仍可能执行脚本，枚举不是绝对无副作用的导出。
- 不要把属性枚举顺序当作业务顺序。需要稳定顺序时，传数组或收集键后自行排序。
- 遍历期间修改同一个对象会使枚举结果难以推断。需删除/改写时，先收集名称，再第二阶段修改。
- `operator=(QJSValue &object)` 是重新绑定并复位，不是复制当前迭代进度。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QJSValueIterator(const QJSValue &object)` | 绑定待遍历对象 | 初始位置在首项前，只遍历自身属性。 |
| `hasNext()` | 判断是否有下一项 | 应在 `next()` 前调用。 |
| `next()` | 前进到下一项 | 成功后才可读取当前名称和值。 |
| `name()` | 取当前属性名 | 仅在成功 `next()` 后调用。 |
| `value()` | 取当前属性值 | 返回 `QJSValue`；getter 可能执行脚本。 |
| `operator=(QJSValue &object)` | 重新绑定目标 | 清除旧进度，从新对象开头枚举。 |
| `~QJSValueIterator()` | 销毁迭代器 | 不拥有目标对象，也不延长其 engine 生命周期。 |

当需求是读取脚本对象显式写出的字段时，`QJSValueIterator` 很合适；当需求转为理解继承、描述符或行为，应回到 `QJSValue` 的属性与原型 API。
