# QtTaskTree::Storage：任务树运行期共享数据槽

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree`

`Storage<T>` 是 QtTaskTree 中跨任务传递数据的机制。recipe 中放入的是一个存储声明；运行到包含它的组时，任务树动态创建一个 `T` 实例，并在该组及其嵌套 handler 运行时激活它。

## 它解决的问题

异步任务通常需要把前一步结果交给后一步。直接捕获局部变量容易遇到生命周期、并发或多次运行复用问题；`Storage<T>` 把数据生命周期绑定到组执行期：

```cpp
Storage<QString> text;

Group {
    sequential,
    text,
    firstTask,
    QSyncTask([text] { qDebug() << *text; })
};
```

所有 `Storage` 副本共享同一个存储声明。handler 中捕获副本并不复制数据槽，而是让它访问当前运行树激活的实例。

## 生命周期与 shadowing

Storage 对象放在哪个组里，实例就在哪个组开始时创建，在该组 done handler 之后销毁。嵌套组中再次放入同一个 Storage 的副本，会创建新的内部实例并遮蔽外层实例，类似 C++ 作用域变量遮蔽。

同一个组内不能放入同一 Storage 的多个副本，运行时会触发断言。若在 handler 中访问一个不可达 Storage，例如忘记把它放进祖先组，文档说明会先输出错误信息，然后可能因空指针而崩溃。

## API 速查表

| API | 语义与边界 |
|---|---|
| `Storage()` | 使用 `T` 的默认构造函数创建运行期实例。 |
| `Storage(args...)` | 保存构造参数，运行时用它们创建 `T` 实例。 |
| `activeStorage()` | 返回当前激活的 `T *`；只能在可达组的运行期 handler 内调用。 |
| `operator*()` | 返回当前激活的 `T &`；生命周期到创建它的组结束。 |
| `operator->()` | 返回当前激活的 `T *`。 |
| `QTaskTree::onStorageSetup(storage, handler)` | 在树启动前向 Storage 写入初始数据。 |
| `QTaskTree::onStorageDone(storage, handler)` | 在树结束前读取最终数据。 |
| Storage 副本 | 共享同一声明；捕获副本是推荐用法。 |
| 嵌套 shadowing | 同一 Storage 放入嵌套组会产生内层实例，遮蔽外层。 |
