# QAssociativeIterable
> Qt 6.11.1 · Qt Core · 来自 `QAssociativeIterable`

## 作用定位
`QAssociativeIterable` 是经 `QVariant` 暴露的关联容器运行时迭代接口，可统一遍历不同键值容器。

## API 速查
| API | 是做什么的 |
|---|---|
| `begin()` / `end()` | 取得通用迭代器。|
| `find()` | 按键查找。|
| `containsKey()` | 判断键存在。|
| `value()` | 读取指定键的值。|
| `mutableIterator()` | 获取可修改迭代器。|

## 使用场景
反射式编辑器、序列化工具或通用调试器需要处理未知具体类型的 map。

## 常见坑与经验
- QVariant 访问有类型擦除和转换成本，不是热路径容器算法的首选。
- 修改迭代时仍遵守底层容器失效规则。

## 知识点覆盖
类型擦除、QVariant、关联容器、运行时反射、迭代器。
