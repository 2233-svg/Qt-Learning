# QOpenGLContextGroup：观察共享 OpenGL 资源的上下文集合

> 头文件：`#include <QOpenGLContextGroup>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QOpenGLContext`

## 它解决什么问题

多个 `QOpenGLContext` 成功建立共享关系后，可以共享纹理、buffer、shader 等 OpenGL 资源。`QOpenGLContextGroup` 是 Qt 自动维护的关系对象，用于识别“哪些上下文属于同一个资源共享组”。

它主要用于诊断、资源缓存或框架级资源管理，例如：

- 确认后台上传上下文是否真的和主渲染上下文共享；
- 让共享资源缓存按 share group 分组，而不是按单个 context 重复创建；
- 从当前线程的 current context 找到其资源组。

应用不能自行构造、删除或向其中添加上下文。共享组由 `QOpenGLContext` 在 `setShareContext()` 后成功 `create()` 时自动创建和维护。

## 如何理解共享组

一个共享组包含所有成功初始化、并且与该组已有上下文共享资源的 `QOpenGLContext`。不与其它上下文共享的 context 也有自己的 share group，只是其中只有它自己。

共享组表达的是资源可共享关系，不表示：

- 这些上下文可在同一线程同时 current；
- 对同一纹理或 buffer 的并发读写自动安全；
- 成员上下文拥有相同的 format、surface 或原生后端；
- 返回的列表可由调用方修改来改变共享关系。

共享是否实际建立，既可用 `QOpenGLContext::areSharing()` 判断两个特定上下文，也可通过 `context->shareGroup()` 再看成员集合。

## 使用示例

```cpp
QOpenGLContextGroup *group = workerContext->shareGroup();
if (!group)
    return;

for (QOpenGLContext *context : group->shares()) {
    if (context == mainContext) {
        // workerContext 与 mainContext 位于同一个实际共享组。
        break;
    }
}
```

上例中的 `QOpenGLContext *` 均为 Qt 管理的借用指针。列表只是当前状态的返回值，不会延长其中对象的生命周期；上下文销毁、重建或共享创建失败后，之前保存的指针和判断都可能不再适用。

## `currentContextGroup()` 的线程语义

```cpp
QOpenGLContextGroup *group =
    QOpenGLContextGroup::currentContextGroup();
```

它返回**调用线程当前 OpenGL 上下文**所属的组。若当前线程没有 `QOpenGLContext::currentContext()`，结果应视为不可用。不要从 GUI 线程查询后，把结果当成工作线程 current context 的组；OpenGL current 状态是线程局部的。

如果只是想检查某个已知上下文的组，直接调用 `context->shareGroup()` 更明确，也不依赖调用线程当前状态。

## 生命周期与资源管理

共享组本身由 Qt 管理，不能 `delete`。它也不替代资源所有权模型：纹理等 GL 资源仍应在合适的 current context 中创建和删除，并在 `QOpenGLContext::aboutToBeDestroyed()` 期间处理外部持有的资源。

多线程共享时，先确保平台支持线程化 OpenGL，并显式同步生产者/消费者。共享组只让资源名字可见，不会在两个上下文之间插入 GPU fence、内存屏障或 CPU 锁。

## 常见错误

### 手工创建或销毁 QOpenGLContextGroup

构造函数不是应用 API，Qt 会随上下文关系自动管理对象。调用方只观察，不拥有。

### 把 `shares()` 当作稳定容器

它返回的是当下成员列表。成员可以因上下文销毁或重建而变化，不能长期缓存列表或其指针来规避生命周期管理。

### 看到同组就忽略同步

共享只解决资源可见性，不解决并发写入、帧间依赖和线程安全。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 静态查询 | `static QOpenGLContextGroup *currentContextGroup()` | 返回调用线程当前 OpenGL 上下文所属的共享组。 | 没有 current context 时不可用；结果由 Qt 管理且只对当前线程状态有意义。 |
| 成员函数 | `QList<QOpenGLContext *> shares() const` | 返回该共享组中的全部 Qt 上下文对象。 | 列表和指针均为观察结果，不转移所有权；成员变化后需重新查询。 |

## 一句话总结

`QOpenGLContextGroup` 是 Qt 自动维护的“谁能共享 GL 资源”的关系对象；可用来检查和组织缓存，但不拥有上下文，也不替代线程同步和资源生命周期管理。
