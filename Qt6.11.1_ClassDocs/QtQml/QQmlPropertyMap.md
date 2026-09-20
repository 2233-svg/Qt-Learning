# QQmlPropertyMap
> Qt 6.11.1 · Qt QML · 来自 `QQmlPropertyMap`

## 作用定位

`QQmlPropertyMap` 把字符串 key 到 QVariant value 的映射暴露成 QML 可访问的动态属性。QML 可以像访问普通属性一样读 `map.someKey`，C++ 可以动态插入、更新、清除 key。

它适合少量动态配置或状态，不适合大型数据模型；数据规模和结构复杂后应使用 model。

## 类说明

- 头文件：`#include <QQmlPropertyMap>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 可继承并重写 `updateValue()` 过滤 QML 写入

## API 速查

| API | 说明 |
| --- | --- |
| `create(parent)` | 创建可直接使用的 property map。 |
| `insert(key, value)` / `insert(QVariantHash)` | 新增或更新动态属性。 |
| `value(key)` / `operator[]` | 读取属性值。 |
| `clear(key)` | 清除某个 key。 |
| `contains()` / `keys()` | 查询 key。 |
| `count()` / `size()` / `isEmpty()` | 查询数量。 |
| `freeze()` | Qt 6.1 起冻结 key 集合，优化属性查找并禁止新增 key。 |
| `valueChanged(key, value)` | 值变化时发出。 |
| `updateValue(key, input)` | QML 写入时的过滤/转换钩子。 |

## 使用场景

- 动态配置项暴露给 QML。
- 小型 key/value 状态面板。
- 需要让 QML 读写一组运行期才知道名字的属性。
- 对 QML 写入做校验或归一化。

## 常见坑与经验

- `QQmlPropertyMap` 的动态属性不等于强类型 Q_PROPERTY；大型 API 更推荐显式属性。
- 如果 key 集合稳定，调用 `freeze()` 可以减少运行期开销，也避免拼错 key 悄悄新增。
- QML 写入会走 `updateValue()`，C++ `insert()` 不一定等价于 QML 写入路径。
- 不要把它当表格或列表模型；没有角色、索引和高效批量通知。
- key 命名应遵守 QML 属性名习惯，避免空格、特殊字符和保留词。

## 知识点覆盖

- 动态 QML 属性
- QVariantHash 暴露
- QML 写入过滤
- key 冻结与性能
- property map 与 model 的边界
