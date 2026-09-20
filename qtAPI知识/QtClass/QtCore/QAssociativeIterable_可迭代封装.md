# QAssociativeIterable 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAssociativeIterable>`  
> 模块：`Qt6::Core`  
> 继承：`QIterable -> QAssociativeIterable`  
> 状态：Qt 6.15 起计划弃用；新代码使用 `QMetaAssociation::Iterable`

## 它解决什么问题

`QAssociativeIterable` 是 Qt 旧版元类型容器反射接口的一部分。它让代码在**不知道关联容器的具体 C++ 类型**时，仍可通过 `QVariant` 用键访问、遍历和修改容器。例如配置系统、属性编辑器、脚本桥接或通用序列化工具拿到的可能是 `QVariantMap`、`QVariantHash`，甚至是注册了可变视图的自定义关联容器；此时不能把它硬编码为某一种 `QMap<K, V>`。

它不是容器本身，也不是容器的拷贝，而是对 `QVariant` 中关联容器的运行时视图：

```text
QVariant
  └─ 关联容器数据
       └─ QAssociativeIterable：运行时按 key/value 访问
```

Qt 文档明确说明：迭代前不会复制底层容器。因此它适合通用反射代码，但也意味着底层 `QVariant` 和容器必须保持有效，且容器变更会影响迭代器。

不过这套 API 已计划在 Qt 6.15 弃用。维护旧项目时可以理解和使用它；新项目应从一开始使用 `QMetaAssociation::Iterable`，避免把即将淘汰的迭代器类型扩散到业务接口中。

## 如何取得视图

当一个 `QVariant` 能转换为 `QVariantMap`、`QVariantHash`，或者自定义容器注册了对应的 mutable view 时，可以从中取得关联迭代视图：

```cpp
#include <QAssociativeIterable>
#include <QVariant>

QVariantMap headers{
    {QStringLiteral("Accept"), QStringLiteral("application/json")},
    {QStringLiteral("Timeout"), QStringLiteral("30")}
};

QVariant variant = headers;
QAssociativeIterable view = variant.value<QAssociativeIterable>();
```

这个例子表达的是“通过元类型拿到通用关联视图”。使用前要确认转换是否成功，并把 `variant` 留在视图和迭代器的整个使用期内。对于你已经知道类型的普通业务代码，直接操作 `QVariantMap` 或 `QMap` 会更清晰，也通常更容易获得编译期类型检查。

## 它最适合什么场景

- 属性编辑器：根据元数据统一展示和修改未知键值容器。
- 通用诊断或日志：遍历 `QVariant` 中的 map/hash，而不写多套类型分派。
- 序列化、脚本绑定、插件接口：容器类型由运行时决定。
- 兼容旧 Qt 反射代码：在迁移到 `QMetaAssociation::Iterable` 前维持已有行为。

不适合的场景：

- 业务代码已知真实容器类型。此时直接使用 `QHash`、`QMap`、`std::map` 等。
- 需要长期保存迭代器、跨线程传递 view 或在并发修改容器时稳定迭代。
- 正在开始的 Qt 6.15 及以后项目。应直接采用替代 API。

## 关键边界：这是借用视图，不复制容器

`QAssociativeIterable` 自身可按值传递，但它指向的仍是 `QVariant` 中的容器。不要让源 `QVariant` 先析构，也不要在仍使用 `find()`、`mutableFind()` 返回值时替换、销毁或重分配底层容器。

```cpp
QAssociativeIterable makeBadView()
{
    QVariantMap map{{QStringLiteral("mode"), QStringLiteral("debug")}};
    QVariant variant = map;
    return variant.value<QAssociativeIterable>(); // 错误：返回后 variant 已销毁
}
```

它不拥有 key、value，也不管理 QObject 生命周期；这里不存在“谁 delete 谁”的问题，真正需要管理的是底层容器和迭代器失效规则。

## 键类型转换：查询安全，写入要格外小心

所有键参数都是 `QVariant`，但底层容器有自己真实的 key 类型。调用 API 时 Qt 会尝试把传入的 `QVariant` 转换为该 key 类型。

### 查询操作

```cpp
if (view.containsKey(QStringLiteral("Timeout"))) {
    QVariant timeout = view.value(QStringLiteral("Timeout"));
}
```

- `containsKey()`：键不能转换时返回 `false`。
- `find()`、`mutableFind()`：键不存在或不能转换时返回 end 迭代器。
- `value()`：键不存在时返回 mapped 类型的默认构造 `QVariant`；键不能转换时，查询的是**默认构造的 key**所对应的值。

因此，`value()` 的返回值“看起来为空”不一定能区分键不存在、键转换失败或真实 value 恰好是默认值。需要精确判断时先调用 `containsKey()`，并确保传入的 `QVariant` 类型正确。

### 写入操作

`insertKey()`、`removeKey()`、`setValue()` 的转换失败语义更危险：

- `insertKey(key)`：不能转换时，会插入默认构造的 key；若 key 已存在，则把 value 重置为 mapped 类型默认值。
- `removeKey(key)`：不能转换时，尝试删除默认构造的 key。
- `setValue(key, mapped)`：不能转换时，写入默认构造的 key；不存在则创建。

因此，通用编辑器在调用写 API 前应先从元类型信息验证 key 的类型，或至少显式转换并检查结果。不要把用户输入的任意 `QVariant` 直接传给这些写操作。

## 查找与迭代

`find()` 返回只读迭代器，`mutableFind()` 返回可写迭代器；未找到时都返回 end：

```cpp
auto it = view.mutableFind(QStringLiteral("Timeout"));
if (it == view.mutableEnd())
    return;

// 用 iterator 的 key()/value() 等能力读取或修改，
// 具体接口来自 QIterable 的迭代器体系。
```

迭代器类型只能由 `QAssociativeIterable` 实例创建，使用方式接近 STL 风格。它们及 `QIterable` 提供的 `begin()`、`end()`、`mutableBegin()`、`mutableEnd()` 都随该类在 Qt 6.15 的弃用计划一起面临迁移，应避免把这些旧类型作为长期公开 API。

容器插入、删除、detach 或重分配后，已有迭代器是否失效取决于底层容器的规则。通用代码不能假设所有关联容器的迭代器稳定；修改前先结束当前遍历或重新取得迭代器最稳妥。

## 迁移到 `QMetaAssociation::Iterable`

Qt 文档指定 `QMetaAssociation::Iterable` 作为替代品。迁移时关注三件事：

1. 用新的 `QMetaAssociation::Iterable` 及其 `Iterator` / `ConstIterator` 代替旧的 `QAssociativeIterable`、`iterator`、`const_iterator`。
2. 不再围绕“`QVariant` 可转换为旧 iterable”设计新接口，而是通过新的元容器关联 API 获取视图。
3. 在库的公共头文件中避免暴露旧类型，防止 Qt 6.15 后调用方被弃用告警和兼容性问题牵制。

这不是简单的名称替换。旧类把“关联容器在 QVariant 中”的模型直接暴露出来；新 API 的职责更贴近 `QMetaAssociation` 的元类型容器反射体系。迁移时应重新确认 view 从何处取得、可写性如何获得，以及迭代器的生命周期。

## 迭代器别名怎么理解

`iterator` 与 `const_iterator` 是旧式别名，并计划在 Qt 6.15 弃用。其余 `Input`、`Forward`、`Bidirectional`、`RandomAccess` 别名把相同底层迭代器以对应的标准迭代器分类暴露出来，便于泛型算法表达所需能力。

这些别名不是说所有关联容器都真的支持随机访问；它们用于满足不同算法的迭代器类型接口。编写通用算法时，只依赖自己声明需要的最小能力，不能因为拿到了 `RandomAccessIterator` 这个别名就盲目对未知容器假设高效随机访问。

## 常见误区

- 以为 `QAssociativeIterable` 把容器复制出来。它只是 view，源 `QVariant` 销毁后 view 会失效。
- 对已知的 `QVariantMap` 也绕一层 iterable。已知类型时直接操作真实容器更简单安全。
- 把 `value()` 的空结果当成“键绝不存在”。键转换失败和默认 key 都会影响结果。
- 将错误类型的键传给 `setValue()` 或 `removeKey()`，意外修改默认构造 key 的条目。
- 在遍历中修改未知底层容器后继续使用旧迭代器。
- 在新代码中继续扩散该类型。它计划于 Qt 6.15 弃用，应优先使用 `QMetaAssociation::Iterable`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 迭代器别名 | `InputConstIterator` | 将只读迭代器作为 `std::input_iterator_tag` 能力暴露。 | 只依赖单次顺序读取所需的最小能力；该旧体系计划随类一起淘汰。 |
| 迭代器别名 | `InputIterator` | 将可写迭代器作为 `std::input_iterator_tag` 能力暴露。 | 修改容器可能使已有迭代器失效，遵守实际底层容器的规则。 |
| 迭代器别名 | `ForwardConstIterator` | 将只读迭代器作为 `std::forward_iterator_tag` 能力暴露。 | 用于需要可重复前向遍历的泛型接口，不表示容器可随机访问。 |
| 迭代器别名 | `ForwardIterator` | 将可写迭代器作为 `std::forward_iterator_tag` 能力暴露。 | 不要在未知容器上假设插入删除后迭代器仍有效。 |
| 迭代器别名 | `BidirectionalConstIterator` | 将只读迭代器作为 `std::bidirectional_iterator_tag` 能力暴露。 | 仅在算法确实需要反向移动时选用。 |
| 迭代器别名 | `BidirectionalIterator` | 将可写迭代器作为 `std::bidirectional_iterator_tag` 能力暴露。 | 迭代器仍借用 view 与底层容器，不能脱离它们长期保存。 |
| 迭代器别名 | `RandomAccessConstIterator` | 以随机访问迭代器分类暴露只读迭代器。 | 这是泛型分类接口；对未知关联容器不要据此假设操作复杂度。 |
| 迭代器别名 | `RandomAccessIterator` | 以随机访问迭代器分类暴露可写迭代器。 | 仅用于兼容需要该分类的模板代码，优先迁移到新元容器 API。 |
| 旧别名 | `const_iterator` | 旧式只读关联迭代器类型。 | 计划于 Qt 6.15 弃用；改用 `QMetaAssociation::Iterable::ConstIterator`。 |
| 旧别名 | `iterator` | 旧式可写关联迭代器类型。 | Qt 6.0 引入且计划于 Qt 6.15 弃用；改用 `QMetaAssociation::Iterable::Iterator`。 |
| 查询 | `containsKey(const QVariant &key)` | 判断是否存在指定键。 | 键不能转换为真实 key 类型时返回 `false`；适合在 `value()` 前区分不存在。 |
| 查询 | `find(const QVariant &key) const` | 返回指定键的只读迭代器。 | 键不存在或不能转换时返回 `end()`；比较后再解引用。 |
| 查询 | `mutableFind(const QVariant &key)` | 返回指定键的可写迭代器。 | 键不存在或不能转换时返回 `mutableEnd()`；写入前确认底层 view 可写。 |
| 插入或重置 | `insertKey(const QVariant &key)` | 插入键；若键已存在则把其 mapped value 重置为默认值。 | 键转换失败会使用默认构造 key，可能误改非预期条目。 |
| 删除 | `removeKey(const QVariant &key)` | 从容器移除指定键的条目。 | 键转换失败会尝试移除默认构造 key；用户输入应先验证类型。 |
| 读取 | `value(const QVariant &key) const` | 读取键对应的 mapped value。 | 键不存在时返回 mapped 类型默认值；键转换失败时查询默认构造 key。 |
| 写入 | `setValue(const QVariant &key, const QVariant &mapped)` | 设置已有键的值，必要时插入新条目。 | 键不能转换时会写入默认构造 key；同时确认 mapped 能转换为真实 value 类型。 |
| 弃用 | `QAssociativeIterable` | 通过 `QVariant` 反射访问关联容器的旧接口。 | Qt 6.15 起计划弃用；新代码使用 `QMetaAssociation::Iterable`。 |

## 一句话总结

`QAssociativeIterable` 是 `QVariant` 里未知关联容器的借用式反射视图：它不复制容器，却会受底层生命周期、迭代器失效和 `QVariant` 键类型转换影响。维护旧代码时尤其要防止转换失败写入默认 key；新代码直接迁移到 `QMetaAssociation::Iterable`。
