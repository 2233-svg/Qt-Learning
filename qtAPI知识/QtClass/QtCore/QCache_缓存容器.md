# Qt QCache 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCache>`  
> 所属模块：`Qt6::Core`  
> 类型：`template <class Key, class T> class QCache`  
> 核心定位：拥有对象的、按成本限制容量的 LRU 缓存

## 1. 它真正解决什么问题

程序里经常有一类对象：创建很贵、可能会再次使用、又不能无限留在内存中。例如缩略图解码结果、按 ID 加载的资料对象、语法高亮结果或解析后的元数据。

用 `QHash<Key, T *>` 也能建立“键到对象”的映射，但它不会替你回答三个关键问题：

1. 这些指针最后由谁 `delete`。
2. 内存不够时应淘汰哪个对象。
3. 不同对象大小不同，容量该按“对象个数”还是按“近似内存成本”控制。

`QCache<Key, T>` 把这三件事放在一起：

- 以 `Key` 查找 `T *`。
- 插入成功后，缓存取得对象的所有权。
- 每个对象带一个 `cost`；总成本超过 `maxCost` 时，自动淘汰较久未访问的对象。

因此它适合“可丢弃的派生数据”，不适合作为唯一的业务数据仓库。缓存被清空或缩容时，里面的对象是允许消失的。

```text
key -> heap object
       ^
       | QCache owns this pointer and may delete it

recently accessed  [hot] ... [cold]
                             ^
                             | evicted first when space is needed
```

## 2. 先记住所有权规则

`QCache` 存的是 `T *`，但它不是“借用这根指针”：`insert()` 调用后，指针交给缓存管理。无论插入后来是否因为成本过大而失败，传入对象都会由 `QCache` 处理并在需要时删除。

```cpp
QCache<int, QByteArray> cache(1024);

auto *data = new QByteArray(loadPayload());
cache.insert(42, data, data->size());

// 不要 delete data;
// 不要再把 data 交给 std::unique_ptr 或 QSharedPointer。
```

这条规则有三个直接后果：

- `clear()`、`remove()`、析构都会删除仍由缓存拥有的对象。
- `object()` 和 `operator[]` 返回的只是借用指针；缓存任何一次会触发淘汰的操作都可能让它失效。
- 想把对象从缓存中带走，应使用 `take()`；此时所有权才转回调用方。

## 3. 最小可用示例：缓存图片解码结果

下面用文件路径作为键，把近似字节数作为成本。真实项目通常会把成本设计为像素缓冲区大小、条目数权重或其它可比较的资源预算。

```cpp
#include <QCache>
#include <QImage>
#include <QString>

class ThumbnailStore
{
public:
    QImage thumbnail(const QString &path)
    {
        if (const QImage *cached = m_cache.object(path)) {
            return *cached; // 立即复制值，不把借用指针长期保存
        }

        auto *image = new QImage(path);
        if (image->isNull()) {
            delete image;   // 尚未 insert，仍由这里负责释放
            return {};
        }

        const qsizetype cost = qsizetype(image->sizeInBytes());
        if (!m_cache.insert(path, image, cost)) {
            // image 已被 QCache 删除；不能再访问或 delete image。
            return {};
        }

        return *m_cache.object(path);
    }

private:
    QCache<QString, QImage> m_cache { 64 * 1024 * 1024 };
};
```

这个例子刻意返回 `QImage` 值，而不是返回 `QImage *`。`QImage` 是值类型，复制很轻量；更重要的是调用方不会握住一个可能被后续缓存操作删除的指针。

## 4. 淘汰模型：成本上限不是条目上限

构造函数的 `maxCost` 默认是 `100`。它不是字节数的固定单位，只是你的成本单位的上限。若每条都传默认 `cost = 1`，它近似等于最多缓存 100 个对象；若成本代表字节数，则上限应传字节预算。

```cpp
QCache<QString, QByteArray> cache(8 * 1024 * 1024); // 约 8 MiB 预算

cache.insert("small", new QByteArray(1024, '@'), 1024);
cache.insert("large", new QByteArray(4 * 1024 * 1024, '@'),
             4 * 1024 * 1024);
```

当新条目会使总成本超过上限，`QCache` 会从较久未访问的对象开始删除，直到预算足够。成功查找 `object(key)` 或 `operator[](key)` 会把该条目视作最近使用，因此会影响以后谁先被淘汰。

不要把这个机制理解成精确的内存统计器：

- `cost` 由你提供，Qt 不会测量 `T` 的真实堆内存。
- `totalCost()` 正常情况下不高于 `maxCost()`，但 Qt 文档说明：缓存对象若涉及隐式共享数据，实际情况可能出现例外。
- `setMaxCost()` 缩小预算会立即删除一些对象；它不是只修改一个数字。

## 5. `insert()` 的失败路径尤其重要

`insert(key, object, cost)` 返回 `false` 的常见原因是 `cost > maxCost()`。此时对象根本放不进缓存，Qt 会马上删除传入的对象。

```cpp
QCache<int, QByteArray> cache(10);
auto *tooLarge = new QByteArray("this does not fit");

const bool stored = cache.insert(1, tooLarge, 20);
Q_ASSERT(!stored);

// tooLarge 已不再可用。此处不能 delete tooLarge，也不能读取它。
```

同一键再次插入时，旧对象会被移除并删除，然后缓存拥有新对象。若你的新旧对象实际上指向同一块堆内存，第二次插入会造成所有权混乱；每个插入指针必须只交给一个所有者。

## 6. 查询、借用与取回的区别

这三个 API 名字很像，所有权语义却不同：

| 调用 | 缓存是否继续拥有对象 | 返回后谁负责释放 | 适合什么情况 |
| --- | --- | --- | --- |
| `object(key)` | 是 | `QCache` | 短暂读取、复制出值 |
| `operator[](key)` | 是 | `QCache` | 与 `object()` 相同的简写 |
| `take(key)` | 否 | 调用方 | 要永久移出缓存并继续使用 |

```cpp
if (QByteArray *borrowed = cache.object("token")) {
    useImmediately(*borrowed);
}

std::unique_ptr<QByteArray> owned(cache.take("token"));
if (owned) {
    modifyAndKeep(*owned);
} // unique_ptr 在这里删除对象
```

`object()` 是 `const` 成员函数并不表示它没有副作用：查找命中会更新内部的“最近使用”顺序。这也说明不能把“const 缓存可在多个线程同时读”当成默认前提；`QCache` 自身不提供并发同步，同一个实例被多线程访问时，调用方应通过 `QMutex` 等方式保护它。

## 7. 选择 `QCache`、`QHash` 还是智能指针容器

选择的核心是“对象是否允许被自动淘汰”以及“谁拥有对象”：

| 需求 | 更合适的选择 | 原因 | 判断方式 |
| --- | --- | --- | --- |
| 有限内存里的临时可重建对象 | `QCache<Key, T>` | 有成本预算、自动所有权和 LRU 淘汰。 | 对象被删后仍能按源数据重新构建。 |
| 所有条目都必须一直保留 | `QHash<Key, T>` | 直接保存值，不会自动删业务数据。 | 数据的完整性比节约缓存空间优先。 |
| 需要共享生命周期、多个持有者 | `QHash<Key, QSharedPointer<T>>` | 生命周期与缓存策略可分开表达。 | 外部对象也必须安全持有同一实例。 |
| 需要值对象且希望缓存按容量淘汰 | `QCache<Key, T>` 配合堆对象 | `QCache` 的接口就是拥有 `T *`。 | 接受由缓存独占指针并随时淘汰。 |

`QCache` 在 Qt 6.11 的头文件中禁用了复制。把它作为成员保存或通过引用传递；需要共享同一个缓存时，明确设计其拥有者和同步策略，而不是假设复制会产生独立缓存。

## 8. 常见错误与排查

### 8.1 把 `object()` 的结果长期保存

```cpp
QByteArray *p = cache.object("a");
cache.insert("b", new QByteArray, 1000); // 可能淘汰 a
use(*p);                                 // p 可能悬空
```

改为立刻使用，或者复制为值；需要拿走则改用 `take()`。

### 8.2 插入后仍手工释放

```cpp
auto *value = new QByteArray("x");
cache.insert("x", value);
delete value; // 错误：QCache 之后还会再次 delete
```

只有在调用 `insert()` 前决定不交给缓存，或者通过 `take()` 拿回对象后，才由你的代码释放它。

### 8.3 忽略 `insert()` 返回值

成本超过上限时，插入失败且对象已被删除。返回值不只是“缓存命中率统计”，它决定后续能否继续使用该指针。

### 8.4 用它缓存不可重建的主数据

`QCache` 的职责就是删除旧对象。订单、编辑中的文档模型、未保存的用户输入等数据不应只存在于 `QCache` 中；最多在旁边缓存可重新生成的投影或派生结果。

## API 速查表
### 构造与生命周期

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QCache(qsizetype maxCost = 100) noexcept` | 创建空缓存，并设置允许的总成本上限。 | 上限是调用方定义的成本单位；默认值为 100。 |
| 生命周期 | `~QCache()` | 销毁缓存并删除其中仍被它拥有的全部对象。 | 析构前不要让外部智能指针或手工 `delete` 同时拥有已插入的对象。 |

### 成本与状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成本 | `qsizetype maxCost() const noexcept` | 返回允许的总成本上限。 | 这是预算值，不是 Qt 实测的内存字节数。 |
| 成本 | `void setMaxCost(qsizetype cost)` | 修改成本上限；当前总成本过高时立即淘汰对象。 | 缩小上限会使先前从 `object()` 借出的指针失效。 |
| 成本 | `qsizetype totalCost() const noexcept` | 返回当前缓存条目的成本总和。 | 通常不超过上限；不要把它当作精确的进程内存占用。 |
| 状态 | `qsizetype size() const noexcept` | 返回缓存中的对象数量。 | 不等于总成本；一个条目可有很大的 `cost`。 |
| 状态 | `qsizetype count() const noexcept` | `size()` 的同义 API。 | 新代码通常统一使用 `size()`，避免两种名称混用。 |
| 状态 | `bool isEmpty() const noexcept` | 判断缓存中是否没有对象。 | 仅检查条目数，不涉及成本预算。 |
| 枚举 | `QList<Key> keys() const` | 返回当前所有键组成的列表。 | 返回的是一份键列表；不应用它推断 LRU 顺序。 |

### 插入、查询与移除

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 清空 | `void clear()` | 删除缓存拥有的所有对象，并把缓存置空。 | 所有借用指针随即失效。 |
| 查询 | `bool contains(const Key &key) const noexcept` | 判断某个键是否存在。 | 只查存在性，不取得对象，也不会代替空指针检查以外的同步需求。 |
| 插入 | `bool insert(const Key &key, T *object, qsizetype cost = 1)` | 以键和成本加入一个堆对象；同键旧对象会被删除。 | 调用后缓存取得 `object` 所有权；即使返回 `false`，也不能再使用该指针。 |
| 查询 | `T *object(const Key &key) const noexcept` | 取到键对应对象的借用指针；找不到返回 `nullptr`。 | 命中会更新最近使用顺序；返回指针随缓存后续淘汰而可能失效。 |
| 查询 | `T *operator[](const Key &key) const noexcept` | `object(key)` 的等价简写。 | 它不会像某些映射容器那样在键不存在时插入默认值。 |
| 删除 | `bool remove(const Key &key)` | 删除指定键及其对象；找到并删除时返回 `true`。 | 这是销毁对象，不是转移对象；想保留对象用 `take()`。 |
| 取出 | `T *take(const Key &key)` | 从缓存移除对象但不删除，并把所有权交给调用方。 | 找不到返回 `nullptr`；拿到后立即交给智能指针或负责 `delete`。 |

---

### 一句话总结

`QCache` 是“带 LRU 淘汰策略的原始指针所有者”：成本要由你合理估算，插入后对象属于缓存，查询得到的指针只能短暂借用。
