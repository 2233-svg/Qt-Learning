# QtTaskTree::GroupItem：任务树 recipe 的通用值元素

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree`

`GroupItem` 是 QtTaskTree recipe 中所有可放进 `Group { ... }` 的元素基类和值包装。真正运行时，它可能代表一个异步任务、一个嵌套组、一个 `Storage`、一个执行模式控制项，或组级 setup/done 处理器。

## 它解决的问题

QtTaskTree 希望用初始化列表描述异步流程：

```cpp
const Group recipe {
    sequential,
    storage,
    downloadTask,
    processTask
};
```

初始化列表必须有统一元素类型，这就是 `GroupItem` 的角色。它是共享内部数据的值类型，可以安全复制；通过派生类构造出的元素放进列表后，仍保留原本的语义。

## 语义边界

`GroupItem` 本身通常不是用户直接执行的任务。只有派生自 `ExecutableItem` 的元素才表示“父组眼中的一个异步步骤”。控制项如 `sequential`、`continueOnError`、`onGroupSetup()`、`Storage<T>` 会影响所在组的行为或生命周期。

把 `GroupItems` 列表作为一个 `GroupItem` 插入时，会包装成一个列表元素；需要注意它与显式 `Group { ... }` 的区别：显式组会作为单个异步任务参与父组执行和结果传播。

## API 速查表

| API | 语义与边界 |
|---|---|
| `GroupItem(const GroupItems &children)` | 将一组元素包装为一个列表型元素。 |
| `GroupItem(std::initializer_list<GroupItem>)` | 用初始化列表构造列表型元素。 |
| `GroupItem(const Storage<T> &storage)` | 把存储声明放入组；运行到该组时创建/销毁实际存储对象。 |
| 复制/移动/赋值 | 值类型操作，共享内部语义；复制不代表克隆运行中任务。 |
| `GroupItem::GroupSetupHandler` | 组进入后调用的处理器，可返回 `SetupResult` 控制是否继续。 |
| `GroupItem::GroupDoneHandler` | 组结束前调用的处理器，可返回 `DoneResult` 调整组结果。 |
| `GroupItems` | `QList<GroupItem>` 别名，用于批量构造 recipe 片段。 |
