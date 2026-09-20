# QJSValueIterator
> Qt 6.11.1 · Qt QML · 来自 `QJSValueIterator`

## 作用定位

`QJSValueIterator` 用来枚举一个 JS 对象的属性。它面向调试、桥接和对象转储场景：你有一个 `QJSValue` 对象，但不知道它有哪些可枚举属性，就用迭代器逐项读取属性名和值。

## 类说明

- 头文件：`#include <QJSValueIterator>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 迭代对象：`QJSValue` 中的 JS object

## API 速查

| API | 说明 |
| --- | --- |
| `QJSValueIterator(object)` | 为指定 JS 对象创建迭代器。 |
| `hasNext()` | 是否还有下一个属性。 |
| `next()` | 前进到下一个属性；成功后才能读 `name()` 和 `value()`。 |
| `name()` | 当前属性名。 |
| `value()` | 当前属性值。 |
| `operator=(object)` | 重设迭代目标。 |

## 典型用法

```cpp
QJSValue obj = engine.globalObject().property("config");
QJSValueIterator it(obj);
while (it.hasNext()) {
    it.next();
    qDebug() << it.name() << it.value().toString();
}
```

## 使用场景

- 把 JS 对象转成日志或调试视图。
- 动态读取用户脚本返回的配置对象。
- 桥接 JS object 到 C++ map-like 结构。

## 常见坑与经验

- 只能枚举可枚举属性；不可枚举属性和某些原型链属性未必出现。
- `next()` 之前读 `name()`/`value()` 没有意义。
- 迭代期间修改对象属性会让结果难以预测；先收集再修改更稳。
- 迭代器不解决深层递归转换，嵌套对象需要手动判断 `value().isObject()` 后继续处理。

## 知识点覆盖

- JS 对象属性枚举
- 可枚举属性与原型链
- 动态对象转 Qt 数据
- `QJSValue` 调试技巧
