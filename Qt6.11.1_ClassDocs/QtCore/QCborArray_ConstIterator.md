# QCborArray::ConstIterator
> Qt 6.11.1 · Qt Core · 来自 `QCborArray::ConstIterator`

## 作用定位
`QCborArray::ConstIterator` 是只读遍历 `QCborArray` 的随机访问迭代器。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` / `operator->()` | 读取当前 `QCborValue`。|
| `operator++()` / `operator--()` | 前后移动。|
| `operator+()` / `operator-()` | 按偏移移动。|
| `operator==()` | 比较位置。|

## 使用场景
解析 CBOR 数组但不允许修改原始文档时使用。

## 常见坑与经验
- 在数组结构变化后，旧迭代器不再可靠。

## 知识点覆盖
const iterator、随机访问、CBOR、迭代器失效。
