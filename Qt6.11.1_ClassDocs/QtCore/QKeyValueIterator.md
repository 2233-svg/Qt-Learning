# QKeyValueIterator
> Qt 6.11.1 · Qt Core · 来自 `QKeyValueIterator`

## 作用定位
`QKeyValueIterator` 把关联容器的普通迭代器包装成可结构化绑定的键值迭代器，让 range-for 中可同时得到 key 与 value。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键。|
| `value()` | 读取或修改当前值。|
| `operator*()` | 返回可解构的键值引用。|
| `operator++()` | 前进到下一项。|
| `asKeyValueRange()` | 从支持的关联容器创建键值范围。|

## 使用场景
```cpp
for (auto [name, setting] : settings.asKeyValueRange())
    validate(name, setting);
```

## 常见坑与经验
- key 一般不能经迭代器修改，否则会破坏容器哈希/排序不变量。
- 遍历期间对容器做结构修改仍会导致迭代器失效。

## 知识点覆盖
关联容器、结构化绑定、键值范围、迭代器、容器不变量。
