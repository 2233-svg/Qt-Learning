# QtTaskTree::Storage
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::Storage`

## 作用定位

`Storage<StorageStruct>` 是 TaskTree 的运行时共享状态容器。它把一份结构体状态绑定到任务树执行过程中，让 setup、任务回调、done handler 能访问同一份上下文。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`StorageBase`

## API 速查

| API | 说明 |
| --- | --- |
| `Storage()` | 默认构造存储描述。 |
| `Storage(args...)` | 用参数构造实际存储结构。 |
| `activeStorage()` | 返回当前运行中的存储指针。 |
| `operator*()` | 访问当前存储引用。 |
| `operator->()` | 访问当前存储成员。 |

## 使用场景

- 在多个任务之间共享结果、临时对象、配置和计数器。
- 避免 lambda 到处捕获一堆外部引用。
- 给 `onStorageSetup()` / `onStorageDone()` 绑定初始化和清理逻辑。

## 常见坑与经验
- 只有任务树运行时才有 active storage；构造 recipe 后立即解引用通常是错的。
- 存储里的 QObject 指针仍要遵守 QObject 生命周期和线程归属。
- 并行组里多个任务同时写存储成员时要自己同步或拆分状态。

## 知识点覆盖

- TaskTree 运行时上下文
- 共享状态与生命周期
- setup/done hooks
- 并行访问风险
