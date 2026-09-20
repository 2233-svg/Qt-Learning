# Qt QHash::TryEmplaceResult 深入笔记

> 适用版本：Qt 6.11.1  
> 所属模块：`Qt6::Core`  
> 类型性质：`QHash` 的嵌套结果结构  
> 引入版本：Qt 6.9  
> 相关 API：`QHash::tryEmplace`、`QHash::tryInsert`、`QHash::insertOrAssign`

## 1. 它解决什么问题

`QHash::TryEmplaceResult` 用一个返回值同时表达两件事：

1. 本次操作最终对应的元素迭代器；
2. 这次操作是否真的创建了新元素。

这比只返回一个 `iterator` 更容易区分“插入成功”和“key 已经存在”。它服务于 Qt 6.9 起的：

- `tryEmplace()`：key 不存在时原地构造 value，存在时保留旧 value；
- `tryInsert()`：key 不存在时插入 value，存在时不覆盖；
- `insertOrAssign()`：key 不存在时插入，存在时赋值覆盖。

## 2. 实际使用场景

### 2.1 判断是否新建

```cpp
QHash<QString, QByteArray> cache;

auto result = cache.tryEmplace("config", 1024, Qt::Uninitialized);
if (result.inserted) {
    qDebug() << "new entry:" << result.iterator.key();
} else {
    qDebug() << "already existed:" << result.iterator.key();
}
```

`result.iterator` 在两种情况下都指向最终对应的元素。`inserted` 才是区分“新建”与“已有”的可靠标志。

### 2.2 避免昂贵的 value 构造

```cpp
auto result = map.tryEmplace(key, expensiveConstructorArgument());
```

如果 key 已经存在，`tryEmplace` 不会为了覆盖旧值而重新构造 mapped value。需要保留旧值时使用 `tryEmplace` 或 `tryInsert`；需要覆盖时使用 `insertOrAssign`。

### 2.3 直接修改返回元素

```cpp
auto result = counts.tryEmplace(id, 0);
if (!result.inserted)
    ++result.iterator.value();
```

返回的是可修改的 `QHash::iterator`。但对 hash 做会触发 detach 或 rehash 的操作后，旧迭代器可能失效，不能跨越这类修改长期保存。

## 3. 三种操作的返回语义

| 操作 | key 不存在 | key 已存在 |
|---|---|---|
| `tryEmplace(key, args...)` | 原地构造，`inserted == true` | 不改 value，`inserted == false` |
| `tryInsert(key, value)` | 插入 value，`inserted == true` | 不覆盖，`inserted == false` |
| `insertOrAssign(key, value)` | 插入 value，`inserted == true` | 覆盖旧 value，`inserted == false` |

三者都返回一个指向相关元素的 iterator。`inserted == false` 并不表示操作失败；对 `insertOrAssign` 而言，它可能表示“已有元素已经被赋新值”。

## 4. 结构字段和迭代器边界

### 4.1 `iterator` 不是结果副本

`iterator` 字段是 `QHash<Key, T>::iterator`，它指向 hash 内部节点。通过它读取或修改的是容器内元素：

```cpp
auto result = hash.tryInsert(key, value);
T &stored = result.iterator.value();
```

它的有效期遵循 QHash 迭代器规则。清空、删除、可能触发 rehash 的插入以及隐式共享 detach 都可能让迭代器失效。

### 4.2 `inserted` 只表示是否新建

`inserted` 为 `true` 表示本次操作创建了新 entry；为 `false` 表示 key 原来已经存在。它不代表 iterator 是否有效，也不表示 `insertOrAssign` 没有修改 value。

### 4.3 不要依赖默认构造结果

结构提供默认构造函数，但业务代码通常只应使用 `tryEmplace`、`tryInsert` 或 `insertOrAssign` 返回的对象。手动默认构造后直接读取 `iterator` 或 `inserted`，没有容器操作为其提供有效语义。

## 5. 和标准库返回值的兼容

Qt 6.9 的实现提供与 `std::pair<key_value_iterator, bool>` 的隐式转换：

- 可以从标准库 `try_emplace` 风格结果转换到 `TryEmplaceResult`；
- 也可以把 Qt 结果转换为 `std::pair`，用于接入部分标准库风格代码；
- Qt 结果中的 `iterator` 是 `QHash::iterator`，转换后会变成 key/value 迭代器，访问方式不同。

如果代码只使用 Qt 容器，直接访问 `.iterator` 和 `.inserted` 可读性最好；只有需要统一 Qt/STL 泛型代码时才依赖转换。

## 6. 逐项 API 说明

### 成员变量

#### `QHash<Key, T>::iterator QHash::TryEmplaceResult::iterator`

保存本次操作最终对应的元素迭代器：

- 新插入时指向新元素；
- key 已存在时指向阻止插入的旧元素；
- `insertOrAssign` 已有 key 时指向被更新的元素。

它是可修改迭代器，可能通过 `iterator.value()` 改变 hash 内部 value。任何会 detach、rehash、删除该元素或清空容器的操作都可能使它失效。

#### `bool QHash::TryEmplaceResult::inserted`

表示本次操作是否创建了新元素：

- `true`：key 之前不存在，本次创建了 entry；
- `false`：key 已存在。

对于 `insertOrAssign`，`false` 不代表 value 没有变化，因为已有 value 可能已经被新值覆盖。

## API 速查表
| 字段/API | 作用 | 关键边界 |
|---|---|---|
| `iterator` | 指向新元素或阻止插入的已有元素 | 受 QHash 迭代器失效规则约束 |
| `inserted` | 表示是否新建 entry | `false` 不代表 `insertOrAssign` 未修改 value |
| `tryEmplace()` | 缺失时原地构造，存在时保留 | Qt 6.9；避免不必要 value 构造 |
| `tryInsert()` | 缺失时插入，存在时不覆盖 | Qt 6.9 |
| `insertOrAssign()` | 缺失时插入，存在时覆盖 | Qt 6.9；已有 key 时 `inserted == false` |
| `std::pair` 转换 | 连接 Qt/STL 风格结果 | 迭代器类型会从 QHash iterator 变为 key/value iterator |

## 8. 选择建议

- 只关心是否插入：检查 `result.inserted`。
- 需要新建时原地构造复杂 value：使用 `tryEmplace`。
- 需要“已有 key 不改变”：使用 `tryInsert`。
- 需要“已有 key 更新”：使用 `insertOrAssign`。
- 需要在结果位置继续操作：立即使用 `result.iterator`，不要跨越可能 rehash 的容器操作保存它。

## 9. 排查顺序

1. 已有 key 的 value 意外改变：检查是否调用了 `insertOrAssign`，而不是 `tryEmplace` 或 `tryInsert`。
2. `inserted == false` 被误判为失败：确认它只表示 key 已存在。
3. 返回 iterator 崩溃：检查是否在取出结果后又对 QHash 做了 detach、rehash、删除或清空。
4. 想避免昂贵构造却仍看到构造发生：确认使用的是 `tryEmplace`，且构造参数没有在调用点提前完成昂贵对象。
5. Qt/STL 迭代器接口混用出错：检查 `iterator` 字段和转换后的 `key_value_iterator` 是否使用了正确的访问 API。
