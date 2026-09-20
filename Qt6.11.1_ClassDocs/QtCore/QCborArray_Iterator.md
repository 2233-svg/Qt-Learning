# QCborArray::Iterator
> Qt 6.11.1 · Qt Core · 来自 `QCborArray::Iterator`

## 作用定位
`QCborArray::Iterator` 是可写的 CBOR 数组迭代器，可就地访问或替换元素。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 访问当前元素。|
| `operator++()` / `operator--()` | 移动迭代位置。|
| `operator[]` | 按相对偏移访问。|
| `erase()` | 通过容器 API 删除当前位置元素。|

## 使用场景
清洗协议数组、将特定 tag 或旧字段值迁移为新值。

## 常见坑与经验
- 遍历时删除元素要使用容器返回的新迭代位置，不能简单递增旧迭代器。

## 知识点覆盖
可写迭代器、就地更新、删除遍历、CBOR 迁移。
