# QOpenGLContextGroup

> Qt 6.11.1 · Qt GUI · 来自 `QOpenGLContextGroup`

## 1. 先建立直觉

`QOpenGLContextGroup` 表示一组彼此共享 OpenGL 资源的 `QOpenGLContext`。如果两个上下文在同一个共享组中，它们通常可以共享纹理、缓冲、着色器等 GL 对象。

它不是你手工创建的资源池，而是 Qt 根据上下文的共享关系维护的对象。多数应用只会在调试、资源管理或后台上传架构中查询它。

## 2. 类说明

- 头文件：`#include <QOpenGLContextGroup>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 获取方式：通过 `QOpenGLContext::shareGroup()` 或 `currentContextGroup()`。

共享组只说明上下文之间具有资源共享关系，不代表所有 OpenGL 状态都共享。

## 3. API 速查

| API | 用途 |
|---|---|
| `currentContextGroup()` | 返回当前线程 current 上下文所属的共享组；没有 current 上下文时通常为空。 |
| `shares()` | 返回该共享组内所有 `QOpenGLContext *`。 |

## 4. 关键用法

```cpp
QOpenGLContextGroup *group = QOpenGLContextGroup::currentContextGroup();
if (group) {
    const QList<QOpenGLContext *> contexts = group->shares();
    qDebug() << "sharing contexts:" << contexts.size();
}
```

这段代码适合调试“我的后台 context 是否真的和 GUI context 共享”。生产代码若只想判断两个 context 是否共享，`QOpenGLContext::areSharing(a, b)` 通常更直接。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 调试纹理在另一个 context 中不可见 | 查询双方 `shareGroup()` 或用 `areSharing()`。 |
| 后台资源上传系统 | 用共享组理解哪些 context 能复用资源。 |
| 清理共享资源 | 在 context 销毁前通过 `aboutToBeDestroyed()` 管理资源，而不是遍历组强删。 |
| 判断当前线程 GL 环境 | 使用 `currentContextGroup()` 前先确保有 current context。 |

## 6. 常见坑与经验

- `shares()` 返回的 context 指针由各自对象生命周期管理，不要删除。
- 共享资源不等于共享状态。绑定点、当前 program、VAO、viewport 等仍属于当前 context 状态。
- 共享关系通常要在 context `create()` 前通过 `setShareContext()` 建立；创建后不能补救。
- context 销毁、重建或丢失会改变共享组实际内容，旧查询结果不能长期缓存。
- 平台可能拒绝共享请求，应以 `shareContext()`、`shareGroup()` 或 `areSharing()` 的结果为准。

## 7. 知识点覆盖

- OpenGL context 共享组的意义
- 资源共享与状态共享的区别
- 当前上下文、共享组和后台资源上传
- context 生命周期和共享关系验证
- `shares()`、`shareGroup()`、`areSharing()` 的使用边界
