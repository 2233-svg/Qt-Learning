# QtTaskTree::GroupItem
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::GroupItem`

## 作用定位

`GroupItem` 是 TaskTree 配方里的基础“积木”。一个任务树不是立即执行的代码块，而是一份由 `GroupItem` 组成的 recipe：里面可以放任务、子组、执行模式、存储对象、条件节点、循环节点等。运行时由 `QTaskTree` 解释这份 recipe。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：无公开基类
- 派生：`ExecutableItem`、`ExecutionMode`

## API 速查

| API | 说明 |
| --- | --- |
| `GroupItem(const GroupItems &children)` | 把一组子项包装成组项。 |
| `GroupItem(std::initializer_list<GroupItem>)` | 用初始化列表写 TaskTree DSL。 |
| `GroupItem(const Storage<StorageStruct> &storage)` | 把运行时存储对象放进 recipe，供任务 setup/done 共享状态。 |
| `GroupSetupHandler` | 组开始执行前的回调类型。 |
| `GroupDoneHandler` | 组结束时的回调类型。 |

## 使用场景

- 构造 `Group{ sequential, task1, task2 }` 这类任务配方。
- 在配方里插入 `Storage<T>`，让一组任务共享上下文。
- 编写库级封装，把多个任务节点包装成一个可复用片段。

## 常见坑与经验

- `GroupItem` 本身只是描述，不代表任务已经开始；真正执行由 `QTaskTree::start()` 或 `runBlocking()` 触发。
- recipe 中捕获的对象要活到任务树运行完成，尤其是 lambda 捕获引用。
- 存储对象是 TaskTree 的状态入口，优先用它传递跨任务状态，不要到处用全局变量。

## 知识点覆盖

- TaskTree recipe 模型
- 任务项与执行项的分层
- 组 setup/done 生命周期
- 存储对象注入
