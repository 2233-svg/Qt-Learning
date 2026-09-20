# Qt QModelRoleDataSpan 多角色槽位视图笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QModelRoleDataSpan>`  
> 所属模块：`Qt6::Core`  
> 类型性质：指向连续 `QModelRoleData` 存储的非拥有 span  
> 相关类型：`QModelRoleData`、`QModelIndex`、`QAbstractItemModel::multiData()`

## 1. 它解决什么问题

`QModelRoleDataSpan` 是 Qt 模型批量角色读取 API 使用的轻量范围视图。它把一段连续的 `QModelRoleData` 存储描述成：

```text
起始 QModelRoleData *
        +
元素数量
        |
        v
QModelRoleDataSpan
```

`QModelIndex::multiData()` 和 `QAbstractItemModel::multiData()` 用它一次处理多个 role：

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::DecorationRole),
    QModelRoleData(Qt::CheckStateRole)
};

QModelRoleDataSpan span(roles);
index.multiData(span);
```

模型随后遍历 span，按每个槽位的 `role()` 填写对应 `data()`。

它解决的是：

- 不为每个 role 单独设计参数；
- 让模型以统一的 range 方式遍历待填充槽位；
- 让 `QModelIndex` 和自定义模型共享连续角色数据协议；
- 在不复制 `QModelRoleData` 数组的情况下传递批量请求。

## 2. 它不是什么

`QModelRoleDataSpan` 不是：

- `QVector<QModelRoleData>` 或 `QList<QModelRoleData>` 的拥有者；
- 自动分配 role 槽位的容器；
- 只读 span；
- 自动检查每个 role 是否存在的查找器；
- 可以脱离源数组长期保存的对象；
- 对 `operator[]` 或指针范围做边界保护的安全数组。

它只保存一个指针和一个长度。复制 span 只复制这两个描述值，不复制底层 `QModelRoleData`。

## 3. 最小使用场景

### 3.1 从数组构造

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::EditRole)
};

QModelRoleDataSpan span(roles);
index.multiData(span);

qDebug() << roles[0].data()
         << roles[1].data();
```

模板构造会从容器的 `std::data()` 和 `std::size()` 取得指针和长度。数组必须在 `multiData()` 调用期间保持有效。

### 3.2 直接从单个槽位构造

```cpp
QModelRoleData display(Qt::DisplayRole);
QModelRoleDataSpan one(display);
index.multiData(one);
```

它表示长度为 1 的 span。这个形式适合需要复用批量 API、但当前只请求一个 role 的代码。

### 3.3 在模型实现中遍历

```cpp
void MyModel::multiData(const QModelIndex &index,
                        QModelRoleDataSpan span) const
{
    for (QModelRoleData &roleData : span) {
        switch (roleData.role()) {
        case Qt::DisplayRole:
            roleData.setData(displayText(index));
            break;
        default:
            roleData.clearData();
            break;
        }
    }
}
```

`begin()` 和 `end()` 提供了 range-for 所需的指针范围。模型不应按固定下标解释 role，而应读取每个 `QModelRoleData::role()`。

## 4. 生命周期和所有权

### 4.1 span 不拥有底层数组

```cpp
QModelRoleDataSpan makeBadSpan()
{
    QModelRoleData local(Qt::DisplayRole);
    return QModelRoleDataSpan(local);
} // local 销毁，返回的 span 悬空
```

安全写法是让数组覆盖 span 的完整使用期：

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole)
};
QModelRoleDataSpan span(roles);
index.multiData(span);
```

### 4.2 复制 span 不复制槽位

```cpp
QModelRoleDataSpan first(roles);
QModelRoleDataSpan second = first;

second[0].setData(QStringLiteral("changed"));
Q_ASSERT(first[0].data().toString() == QStringLiteral("changed"));
```

两个 span 指向同一组 `QModelRoleData`。复制它不会建立独立结果。

### 4.3 const span 仍能修改底层槽位

头文件中的：

```cpp
QModelRoleData &operator[](qsizetype index) const;
```

返回的是非 const 引用。span 对象本身可以是 const，但它仍然可以通过 `data()`、`begin()` 或 `operator[]` 修改底层 `QModelRoleData`。这是“span 描述器 const”和“底层元素 const”之间的区别。

## 5. 构造形式和兼容容器

### 5.1 默认构造

```cpp
QModelRoleDataSpan empty;
```

得到长度为 0、数据指针为空的空 span。它可以作为“没有请求 role”的状态，但不应对它执行 `operator[]` 或假设 `data()` 指向可写元素。

### 5.2 `QModelRoleData &`

```cpp
QModelRoleDataSpan span(roleData);
```

构造一个只包含单个槽位的 span：

```text
data() == &roleData
size() == 1
```

### 5.3 `QModelRoleData *` 和长度

```cpp
QModelRoleDataSpan span(pointer, length);
```

这是最低层构造形式。Qt 不替调用方验证：

- `pointer` 是否指向至少 `length` 个连续对象；
- `length` 是否非负；
- 对象是否已经构造；
- 对象在 span 使用期间是否存活。

调用方必须自行保证这些条件。传入空指针和正长度会产生无效 span。

### 5.4 兼容容器模板

```cpp
template <typename Container,
          if_compatible_container<Container> = true>
QModelRoleDataSpan(Container &container);
```

Qt 通过编译期检测接受满足这些条件的容器：

- `std::data(container)` 可转换为 `QModelRoleData *`；
- `std::size(container)` 可转换为 `qsizetype`；
- 支持可迭代访问；
- 元素类型可转换为 `QModelRoleData`；
- 不是 `QModelRoleDataSpan` 自身。

由于需要可写的 `QModelRoleData *`，这个构造通常要求可写容器，而不是 `const` 容器。常见可用形状包括 `std::array<QModelRoleData, N>`、内置数组或提供合适 contiguous data 的容器；具体是否满足约束应以编译器实例化结果为准。

## 6. 逐项 API 语义

### 6.1 `QModelRoleDataSpan()`

```cpp
constexpr QModelRoleDataSpan() noexcept;
```

构造空 span。内部指针为空，长度为 0。

它适合表示没有 role 请求的状态，但不能因为 `size() == 0` 就对 `data()`、`begin()` 或 `operator[]` 返回的地址做解引用。

### 6.2 `QModelRoleDataSpan(QModelRoleData &modelRoleData)`

```cpp
constexpr QModelRoleDataSpan(
    QModelRoleData &modelRoleData) noexcept;
```

把一个槽位包装成长度为 1 的 span。span 不复制 `modelRoleData`，并且通过它写入的结果会直接改变原对象。

### 6.3 `QModelRoleDataSpan(QModelRoleData *modelRoleData,
qsizetype len)`

```cpp
constexpr QModelRoleDataSpan(
    QModelRoleData *modelRoleData,
    qsizetype len);
```

使用裸指针和长度描述连续槽位。这个 API 不拥有内存，也不做运行时长度检查。

安全前提：

- `len >= 0`；
- `modelRoleData` 指向至少 `len` 个连续的已构造 `QModelRoleData`；
- 这些对象在 span 使用期间保持存活；
- 不发生让底层存储搬家的容器操作。

### 6.4 `QModelRoleDataSpan(Container &c)`

```cpp
template <typename Container,
          if_compatible_container<Container> = true>
constexpr QModelRoleDataSpan(Container &c);
```

从兼容容器的 `data()` 和 `size()` 构造非拥有 view。`Container` 必须提供适合模型 role 数据的可写连续存储。

这个构造不是“把任意 range 变成 span”的通用机制。只支持能提供连续可写 `QModelRoleData` 地址的容器。

### 6.5 `size() const`

```cpp
constexpr qsizetype size() const noexcept;
```

返回 span 描述的元素数量。空 span 返回 `0`。

它只返回构造时保存的长度，不重新查询底层容器。若底层容器后来改变大小，span 的长度不会自动更新，指针也可能失效。

### 6.6 `length() const`

```cpp
constexpr qsizetype length() const noexcept;
```

返回与 `size()` 相同的长度。它适合与“字符/范围长度”风格的泛型代码配合，语义上没有额外的存储信息。

### 6.7 `data() const`

```cpp
constexpr QModelRoleData *data() const noexcept;
```

返回第一个 `QModelRoleData` 的指针。返回值可能为 `nullptr`：

```cpp
if (span.data() && span.size() > 0) {
    // 才能按数组访问
}
```

`data()` 返回的是可写指针，即使 span 对象本身是 const。指针的有效性取决于底层数组和生命周期，不由 span 延长。

### 6.8 `begin() const`

```cpp
constexpr QModelRoleData *begin() const noexcept;
```

返回第一个槽位的指针。它与 `end()` 一起提供 range-for：

```cpp
for (QModelRoleData &roleData : span) {
    roleData.clearData();
}
```

空 span 可以有空 begin；不要解引用 `begin()`，除非 `begin() != end()`。

### 6.9 `end() const`

```cpp
constexpr QModelRoleData *end() const noexcept;
```

返回 one-past-the-end 指针。它只能用于比较和计算范围，不能解引用：

```cpp
for (auto *it = span.begin(); it != span.end(); ++it)
    inspect(*it);
```

如果底层数组已失效，`end()` 的指针也不能再用于比较。

### 6.10 `operator[](qsizetype index) const`

```cpp
constexpr QModelRoleData &operator[](
    qsizetype index) const;
```

按偏移返回槽位引用。这个操作不做边界检查，`index` 必须满足：

```text
0 <= index < size()
```

越界访问是未定义行为。即使 span 自身是 const，返回仍是可写引用，因为 span 只保存非 const 元素指针。

### 6.11 `dataForRole(int role) const`

```cpp
constexpr QVariant *dataForRole(int role) const;
```

在 span 中线性查找 `role()` 等于指定值的第一个槽位，并返回该槽位的 `data()` 地址：

```cpp
if (QVariant *display = span.dataForRole(Qt::DisplayRole))
    display->setValue(QStringLiteral("ready"));
```

但这个示例隐含一个重要边界：Qt 6.11.1 头文件实现使用：

```cpp
Q_ASSERT(result != end());
return &result->data();
```

因此 `dataForRole()` 不是“找不到就返回 nullptr”的安全查询 API。调用方必须保证 role 存在；找不到时在 debug 构建会触发断言，在关闭断言的构建中继续解引用 end 位置也不受支持。

它的复杂度是 O(n)，重复查询很多 role 时应考虑先建立自己的 role 到数组位置映射。

## 7. 与 `multiData()` 的协作规则

### 7.1 调用方拥有槽位，模型只借用

```cpp
QModelRoleData requested[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::UserRole + 1)
};

QModelRoleDataSpan span(requested);
index.multiData(span);
```

`multiData()` 返回后，`requested` 仍然由调用方拥有。span 不负责销毁或清理其中的 `QModelRoleData`。

### 7.2 role 顺序不固定

模型实现必须写：

```cpp
for (QModelRoleData &roleData : span) {
    switch (roleData.role()) {
    case Qt::DisplayRole:
        roleData.setData(...);
        break;
    }
}
```

不能写成：

```cpp
span[0].setData(display);
span[1].setData(edit);
```

除非调用方和模型之间明确约定数组顺序。公共模型 API 不应依赖这种隐含顺序。

### 7.3 未支持 role 要清理

如果 role 数组被复用，模型对未知 role 应调用：

```cpp
roleData.clearData();
```

否则旧结果可能残留，让调用方误以为本次请求成功返回了新数据。

### 7.4 span 不会复制结果

模型在 span 中写入的所有结果直接落到调用方的 `QModelRoleData` 数组。复制 span、把 span 按值传给函数或作为参数返回，都不会复制这些 `QVariant` 结果。

## 8. 常见使用模式

### 8.1 连续数组

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::EditRole),
    QModelRoleData(Qt::ToolTipRole)
};

QModelRoleDataSpan span(roles);
index.multiData(span);
```

### 8.2 单个 role 复用批量接口

```cpp
QModelRoleData display(Qt::DisplayRole);
index.multiData(QModelRoleDataSpan(display));
qDebug() << display.data();
```

临时 span 在调用结束后销毁没有问题，因为 `display` 仍由外层拥有。

### 8.3 按 role 查询结果

如果代码确实保证 role 存在，可以使用：

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::EditRole)
};

QModelRoleDataSpan span(roles);
index.multiData(span);

QVariant *edit = span.dataForRole(Qt::EditRole);
```

如果 role 可能不存在，不要直接调用 `dataForRole()`。应自己遍历：

```cpp
QVariant *result = nullptr;
for (QModelRoleData &roleData : span) {
    if (roleData.role() == requestedRole) {
        result = &roleData.data();
        break;
    }
}
```

## 9. 生命周期、移动和容器失效

### 9.1 span 可以移动和复制，但指针语义不变

它是轻量可复制值对象。移动或复制只转移/复制指针和长度，不会让底层数组获得新的所有者。

### 9.2 不要在 span 存活期间让容器搬家

```cpp
QVector<QModelRoleData> roles;
QModelRoleDataSpan span(roles);

roles.append(QModelRoleData(Qt::EditRole)); // 可能重新分配
```

扩容后 `span.data()`、`begin()`、`end()` 和 `operator[]` 都可能指向失效存储。应在容器完成尺寸调整后重新构造 span。

### 9.3 线程安全由调用方负责

span 本身没有同步机制。多个线程同时修改同一组 role data 会发生数据竞争；模型也通常必须在所属线程调用。

## 10. 常见错误

### 10.1 返回局部数组的 span

**问题：** 函数返回后继续使用 span。

**原因：** span 不拥有数组。

**处理：** 让数组覆盖整个使用期，或返回真正拥有数据的容器/结果。

### 10.2 用 `operator[]` 试探长度

**问题：** 访问 `span[size()]` 检查是否存在。

**原因：** `operator[]` 没有边界检查。

**处理：** 先判断 `index < size()`。

### 10.3 把 `dataForRole()` 当成可失败查询

**问题：** 请求不存在的 role，希望得到 nullptr。

**原因：** Qt 6.11.1 实现对未找到 role 使用 `Q_ASSERT`，不是返回空指针。

**处理：** 预先保证 role 存在，或自己遍历查找。

### 10.4 用 const 容器构造可写 span

**问题：** 期待模型通过 span 填写 const 数组。

**原因：** 模板约束要求 data 指针可转换为 `QModelRoleData *`。

**处理：** 使用可写的 `QModelRoleData` 存储。若只需要读结果，调用后再以 const 方式读取。

### 10.5 容器扩容后继续使用旧 span

**问题：** 结果写入随机内存或崩溃。

**原因：** 底层 contiguous storage 已重新分配。

**处理：** 完成容器调整后重新构造 span。

### 10.6 以为 span 复制结果

**问题：** 修改复制出的 span，却期待原数组不变。

**原因：** span 是非拥有的指针范围。

**处理：** 复制真正的 `QModelRoleData` 数组，不能只复制 span。

## API 速查表
### 11.1 构造和存储

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QModelRoleDataSpan()` | 构造空 span | 长度为 0；不能解引用 |
| `QModelRoleDataSpan(QModelRoleData &)` | 包装一个 role 槽位 | 不复制对象；长度为 1 |
| `QModelRoleDataSpan(QModelRoleData *, qsizetype)` | 包装裸指针连续范围 | 不检查指针、长度或对象生命周期 |
| `QModelRoleDataSpan(Container &)` | 从兼容 contiguous 容器构造 | 需要可写 `QModelRoleData *`；不拥有容器 |

### 11.2 范围访问

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `size()` | 返回槽位数量 | 返回构造时保存的长度，不跟踪容器变化 |
| `length()` | 返回槽位数量 | 与 `size()` 相同 |
| `data()` | 返回第一个槽位指针 | 可能为空；返回可写指针 |
| `begin()` | 返回起始指针 | 空 span 不可解引用 |
| `end()` | 返回尾后指针 | 只能比较，不能解引用 |
| `operator[](qsizetype)` | 按位置取得可写槽位 | 无边界检查；必须先验证范围 |
| `dataForRole(int)` | 按 role 找到第一个槽位的 data | role 必须存在；未找到会断言/进入未定义路径 |

### 11.3 与模型 API 的协作

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QModelIndex::multiData(QModelRoleDataSpan)` | 批量读取当前索引多个 role | span 和底层数组由调用方持有 |
| `QAbstractItemModel::multiData(const QModelIndex &, QModelRoleDataSpan)` | 模型实现批量填写 role 槽位 | 按 `role()` 分派；未知 role 应清理 |
| `QModelRoleData::setData()` | 写入某个槽位结果 | 只改结果，不改 role，也不通知模型 |
| `QModelRoleData::clearData()` | 清理某个槽位结果 | 复用数组或未知 role 时使用 |

## 12. 一句话总结

`QModelRoleDataSpan` 是一段连续 `QModelRoleData` 的非拥有、可写范围视图：它只保存指针和长度，复制不会复制槽位，`operator[]` 不做边界检查，`dataForRole()` 也不是可失败查询。把它传给 `multiData()` 时，让底层数组保持有效，模型按 `role()` 填写对应槽位，未知 role 明确清空。
