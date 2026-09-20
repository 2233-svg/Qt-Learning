# QOpenGLVertexArrayObject 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLVertexArrayObject>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QObject`  
> 定位：包装 OpenGL Vertex Array Object，保存顶点输入状态

## 它解决什么问题

`QOpenGLVertexArrayObject` 包装 OpenGL VAO。VAO 是一个保存“顶点属性如何从 buffer 读入管线”的容器对象：attribute 是否启用、attribute format、stride、offset、绑定的顶点/索引 buffer、attribute divisor 等状态都可以被记录。渲染不同 mesh 时，绑定对应 VAO 就能恢复这组顶点输入状态。

它解决的是现代 OpenGL 中“每次绘制前重复设置一大堆 vertex attribute 状态”的问题。初始化阶段把某个对象的顶点布局写进 VAO，渲染阶段只需 bind VAO、bind program、draw，就能减少状态设置和驱动验证成本。

## 实际使用场景

- 每个 mesh 一个 VAO，保存位置/法线/UV/tangent 等 attribute 布局；
- 同一个 VBO 数据用不同 shader layout 建多个 VAO；
- 使用 instancing 时把 attribute divisor 一并记录在 VAO；
- 在 core profile 中满足“绘制前必须有合适 VAO”的要求；
- 在不支持 VAO 的旧 OpenGL/ES2 平台上降级为每次手动设置 attribute。

## 使用模型

```cpp
#include <QOpenGLVertexArrayObject>
#include <QOpenGLBuffer>

void setup(QOpenGLVertexArrayObject &vao, QOpenGLBuffer &vbo)
{
    vao.create();
    vao.bind();

    vbo.bind();
    // glVertexAttribPointer / QOpenGLShaderProgram::setAttributeBuffer
    // glEnableVertexAttribArray / program.enableAttributeArray

    vao.release();
}
```

`create()` 必须在支持 VAO 的 current context 中调用。若返回 `false`，应用不应直接崩溃，而应准备 VAO-less 路径：每次绘制时手动重新设置 vertex attribute 状态。

## 核心语义

### VAO 保存的是顶点输入状态

绑定 VAO 后设置 attribute pointer、enable state、element array buffer 等，状态会进入这个 VAO。之后重新绑定该 VAO，就恢复这套顶点输入配置。它不保存 shader program、texture、uniform、blend/depth 状态。

### VAO 不跨 context share group 共享

Qt 文档特别强调：VAO 和其他 OpenGL container object 一样，是创建它的 context 专属对象，不能在 context group 之间共享。即使 buffer/texture 可以共享，VAO 自身也要按 context 单独创建。

### 支持情况要检查

桌面 OpenGL 3.0+ 原生支持 VAO；旧桌面可通过 `GL_ARB_vertex_array_object`；OpenGL ES 2 需要可选 `GL_OES_vertex_array_object` 扩展。`create()` 返回 `false` 是可预期的兼容性结果。

### 生命周期依赖 context

`destroy()` 需要一个有效且支持 VAO 的 current OpenGL context。析构时自动清理不一定总是发生在你期望的 context 下，复杂资源系统中显式清理更可控。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `class Binder` | RAII 帮助类，作用域内绑定 VAO，析构时释放。 | 适合避免异常/早退导致忘记 `release()`。 |
| `QOpenGLVertexArrayObject(QObject *parent = nullptr)` | 创建 Qt 包装对象。 | 还没有底层 VAO；使用前调用 `create()`。 |
| `~QOpenGLVertexArrayObject()` | 销毁对象和底层资源。 | 底层资源清理依赖当前 context；必要时显式 `destroy()`。 |
| `create()` | 创建底层 OpenGL VAO。 | 需要 current context；不支持 VAO 时返回 `false`。 |
| `destroy()` | 销毁底层 VAO。 | 调用时需要合适 current context。 |
| `isCreated() const` | 查询底层 VAO 是否已创建。 | 渲染时可用它决定走 VAO 或手动 attribute 路径。 |
| `objectId() const` | 返回底层 OpenGL VAO id。 | 需要原生 OpenGL API 时使用。 |
| `bind()` | 绑定 VAO；之后顶点数组状态修改会记录到它。 | 绑定期间设置 attribute/buffer 布局；不保存 program/uniform/texture。 |
| `release()` | 解绑当前 VAO，绑定默认 VAO 0。 | 在 core profile 中默认 VAO 0 未必可用于实际绘制；只是释放绑定。 |

## 常见误区

### 以为 VAO 保存所有渲染状态

VAO 只保存顶点输入相关状态。shader program、uniform、texture unit、blend/depth/scissor 都要另外设置。

### 在一个 context 创建，在另一个 context 使用

VAO 不可跨 share group 共享。多 context 渲染时，每个 context 都要创建自己的 VAO，哪怕它们引用的是共享 buffer。

### 忽略 `create()` 返回值

旧平台或 OpenGL ES 2 没有 VAO 支持时，`create()` 可能失败。代码应有手动设置 attribute 的 fallback。

## 一句话总结

`QOpenGLVertexArrayObject` 是顶点输入状态的快照容器；它能让 mesh 切换更干净高效，但只管 attribute/buffer 布局，而且强依赖创建它的 OpenGL context。
