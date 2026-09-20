# QMetaSequence::Iterable::ConstIterator
> Qt 6.11.1 · Qt Core · 来自 `QMetaSequence::Iterable::ConstIterator`

## 作用定位
`QMetaSequence::Iterable::ConstIterator` 是通用顺序容器的运行时只读迭代器，不需要在编译期知道元素模板类型。

## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 读取当前位置元素到运行时缓冲。|
| `operator++()` | 推进至下一元素。|
| `operator==()` | 判断是否到达结束。|

## 使用场景
在调试面板、通用格式转换器中只读枚举某个 QVariant 携带的容器元素。

## 常见坑与经验
- 读取的元素类型由 `QMetaSequence::valueMetaType()` 决定；使用前必须知道如何构造和销毁输出存储。
- 容器发生结构改变后，旧运行时迭代器不能继续使用。

## 知识点覆盖
运行时迭代、顺序容器、QMetaType、只读访问、生命周期。
