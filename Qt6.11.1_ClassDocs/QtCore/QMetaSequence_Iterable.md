# QMetaSequence::Iterable
> Qt 6.11.1 · Qt Core · 来自 `QMetaSequence::Iterable`

## 作用定位
`QMetaSequence::Iterable` 将未知具体类型的顺序容器实例包装为可运行时遍历的范围。

## API 速查
| API | 是做什么的 |
|---|---|
| `begin()` / `end()` | 获取可写迭代范围。|
| `constBegin()` / `constEnd()` | 获取只读范围。|
| `metaSequence()` | 查询底层顺序容器描述。|
| `container()` | 获取被包装实例的运行时地址。|

## 使用场景
属性浏览器读取 QVariant 中的列表并动态生成项目，或通用序列化框架遍历任意注册顺序容器。

## 常见坑与经验
- 它不拥有容器；容器销毁、移动或 QVariant 重置后 iterable 即失效。
- 修改元素或结构时，要遵循底层容器的容量、detach 与迭代器规则。

## 知识点覆盖
运行时范围、顺序容器、元类型、生命周期、类型擦除、动态表单。
