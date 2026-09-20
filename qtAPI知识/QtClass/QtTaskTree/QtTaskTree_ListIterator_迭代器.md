# QtTaskTree::ListIterator：按 QList 元素循环

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`Iterator`

`ListIterator<T>` 让 `For` 对 `QList<T>` 的每个元素执行一次 body，并在 body handler 内暴露当前元素。

## 使用方式

```cpp
const QList<QUrl> urls = ...;
ListIterator<QUrl> it(urls);

const Group recipe {
    For(it) >> Do {
        QSyncTask([it] {
            qDebug() << *it;
        })
    }
};
```

迭代器会捕获传入列表的副本，因此 recipe 可以安全晚些执行；但当前元素只能在对应 `Do` body 的运行期 handler 内访问。

## 并行语义

并行 body 中，每个 handler 看到的 `*it` 与自己的迭代对应，但 done handler 完成顺序不保证和列表顺序一致。需要按原顺序合并结果时，结合 `iteration()` 存储到对应位置。

## API 速查表

| API | 语义与边界 |
|---|---|
| `ListIterator(const QList<T> &list)` | 构造按列表元素循环的迭代器；内部捕获列表副本。 |
| `operator*()` | 返回当前元素引用；只能在 body handler 内调用。 |
| `operator->()` | 返回当前元素指针；只能在 body handler 内调用。 |
| 继承的 `iteration()` | 当前元素索引，可用于保存结果位置。 |
| 非运行期访问 | 没有活跃元素，可能崩溃。 |
