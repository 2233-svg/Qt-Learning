# QBaseIterator
> Qt 6.11.1 · Qt Core · 来自 `QBaseIterator`

## 作用定位
`QBaseIterator` 是 Qt 容器迭代器的内部通用基础，不是通常直接使用的应用级类型。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator++()` / `operator--()` | 前后移动迭代位置。|
| `operator==()` | 比较迭代位置。|

## 使用场景
理解 Qt 容器迭代器设计或模板报错时参考。

## 常见坑与经验
- 应使用 `QList`、`QMap` 等公开 iterator 类型，不应依赖该基础类实现细节。

## 知识点覆盖
迭代器、容器内部实现、公开 API 边界、失效规则。
