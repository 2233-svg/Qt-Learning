# QVariant
> Qt 6.11.1 · Qt Core · 来自 `QVariant`
## 作用定位
`QVariant` 是 Qt 的类型擦除值容器，可保存注册到元类型系统的值，广泛用于模型角色、属性系统、信号参数和设置存储。
## API 速查
| API | 是做什么的 |
|---|---|
| `fromValue()` | 保存任意已注册类型。 |
| `value<T>()` / `qvariant_cast` | 取回指定类型。 |
| `canConvert()` / `convert()` | 检查和执行类型转换。 |
| `metaType()` / `typeId()` | 查询真实元类型。 |
| `isValid()` / `isNull()` | 区分无值和空值。 |
| `toString/toInt/...` | 常用转换快捷方式。 |
| `emplace()` | 原位构造保存值。 |
## 使用场景
模型 `data()` 返回不同角色的文本、颜色、图标或业务 id。
## 常见坑与经验
- `isValid()` false 表示没有值；空字符串、0、null 指针是另一回事。
- 转换失败可能给默认值，关键路径先 `canConvert()`。
- 自定义类型跨 queued signal 或 QVariant 前需注册元类型。
- 不要把 `QVariant` 当长期逃避类型设计的万能容器。
## 知识点覆盖
元类型、类型擦除、模型角色、属性、转换失败、自定义类型注册。
