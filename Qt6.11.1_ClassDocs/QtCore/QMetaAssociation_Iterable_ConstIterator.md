# QMetaAssociation::Iterable::ConstIterator
> Qt 6.11.1 · Qt Core · 来自 `QMetaAssociation::Iterable::ConstIterator`

## 作用定位
`QMetaAssociation::Iterable::ConstIterator` 是在不知道关联容器具体模板类型时，只读遍历运行时键值对的迭代器。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 以运行时数据读取当前键。|
| `value()` | 以运行时数据读取当前值。|
| `operator++()` | 前进到下一项。|
| `operator==()` | 判断是否到达结束。|

## 使用场景
元对象浏览器、动态序列化工具、调试面板输出任意关联容器。

## 常见坑与经验
- 键和值的解释依赖 `QMetaAssociation` 给出的元类型；读取后再转换为具体 C++ 类型。
- 它不是类型安全的模板 iterator，错误的 `void*` 缓冲可能破坏内存。

## 知识点覆盖
运行时迭代、键值容器、QMetaType、类型擦除、内存安全。
