# QSequentialIterable
> Qt 6.11.1 · Qt Core · 来自 `QSequentialIterable`

## 作用定位
`QSequentialIterable` 是 `QVariant` 中顺序容器的类型擦除遍历接口，便于在不知道具体 `QList<T>`、`QVector<T>` 类型时读取元素。
## API 速查
| API | 是做什么的 |
|---|---|
| `begin/end` | 遍历元素，解引用得到 `QVariant`。 |
| `constBegin/constEnd` | 只读遍历。 |
| `size()` / `at()` | 查询元素数量或随机访问。 |
| `valueMetaType()` | 查询元素类型。 |
## 使用场景
从插件、元对象或通用序列化代码获取 `QVariant` 容器后统一读取。
## 常见坑与经验
- 元素以 `QVariant` 暴露，频繁转换会有成本和失败可能。
- 只适用于顺序容器，键值容器使用 `QAssociativeIterable`。
- 不要在遍历期间修改底层容器。
## 知识点覆盖
类型擦除、QVariant、元类型、泛型遍历、容器边界。
