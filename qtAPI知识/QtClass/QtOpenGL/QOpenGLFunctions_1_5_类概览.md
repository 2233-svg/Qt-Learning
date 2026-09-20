# QOpenGLFunctions_1_5 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_1_5>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 1.5 compatibility API；Qt 以 OpenGL ES 2 构建时不可用，也不适用于只提供 Core profile 的 context

## 它解决什么问题

`QOpenGLFunctions_1_5` 将 OpenGL 1.5 及之前版本的函数入口变成 Qt 可初始化的成员函数。它让旧桌面 OpenGL 程序在 Qt 的 `QOpenGLContext` 生命周期内获取 buffer object、query object 和前代 compatibility API，而不需要自己解析平台函数指针。

OpenGL 1.5 是从纯 client-side vertex arrays 迈向现代资源模型的重要版本：它引入 buffer object，把顶点、索引等数据放入 GL 管理的对象；同时引入 query object，典型用途是 occlusion query。这个类仍然继承了大量 fixed-function 和 deprecated 接口，但 1.5 新增的 buffer/query 是迁移旧代码时很实用的过渡点。

现代 Qt OpenGL 项目通常会使用 `QOpenGLBuffer`、`QOpenGLVertexArrayObject`、`QOpenGLShaderProgram` 或更高版本 Core functions。直接使用本类适合需要精确贴合旧 C/OpenGL 代码、或逐步替换旧渲染路径的场景。

## 实际使用场景

- 将使用 `glVertexPointer()` 指向 CPU 内存的老代码迁移为 VBO/EBO；
- 用 occlusion query 判断某批物体是否通过深度测试，以减少后续昂贵绘制；
- 在 Qt 插件中承接一段明确要求 OpenGL 1.5 compatibility context 的第三方渲染代码；
- 分析旧程序里 buffer target、offset 和 client pointer 混用造成的崩溃或画面错乱。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_1_5>

QOpenGLFunctions_1_5 gl;

bool createVertexBuffer(const void *data, qsizetype bytes)
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint vbo = 0;
    gl.glGenBuffers(1, &vbo);
    gl.glBindBuffer(GL_ARRAY_BUFFER, vbo);
    gl.glBufferData(GL_ARRAY_BUFFER, GLsizeiptr(bytes), data, GL_STATIC_DRAW);
    return true;
}
```

调用初始化和任意 `gl*` 成员时，目标 `QOpenGLContext` 必须在当前线程 current。buffer/query ID 属于 context 共享组；没有共享关系的 context 不能直接使用这些对象。

## 1.5 新增能力如何使用

### Buffer object

`glGenBuffers()` 创建 buffer 名称，`glBindBuffer()` 将其绑定到 `GL_ARRAY_BUFFER`、`GL_ELEMENT_ARRAY_BUFFER` 等 target，`glBufferData()` 分配并可选上传整块数据，`glBufferSubData()` 更新子范围。绑定 buffer 后，旧的 `glVertexPointer()`、`glColorPointer()`、`glTexCoordPointer()` 等函数里的 `pointer` 参数不再表示 CPU 地址，而是 buffer 内字节偏移。

这是 1.5 最重要的边界：同一段旧代码在是否绑定 `GL_ARRAY_BUFFER` 时语义完全不同。迁移时应把 offset 写成 `reinterpret_cast<const void *>(quintptr(offset))` 这类明确形式，并用 VAO 或局部封装固定每个 attribute 的布局。

### 映射与读回

`glMapBuffer()` 将 buffer 映射到进程地址空间，`glUnmapBuffer()` 解除映射并返回数据是否仍有效。`glGetBufferSubData()` 可把 buffer 某段读回 CPU，`glGetBufferPointerv()` 和 `glGetBufferParameteriv()` 查询映射指针与大小/用法等状态。

映射期间不要继续让 GPU 使用同一存储范围，也不要忘记 unmap。读回与映射都可能造成同步等待；高频更新应使用 orphaning、环形 buffer 或更高版本的 map-range/persistent mapping 策略，而不是每帧 map/unmap 同一块数据。

### Query object

`glGenQueries()`、`glBeginQuery()`、`glEndQuery()` 和 `glGetQueryObject*()` 管理异步查询。1.5 典型目标是 `GL_SAMPLES_PASSED`：在查询范围内绘制 bounding proxy 后，稍后读取通过深度/模板测试的样本数。

查询结果不是立即免费的。刚结束查询就读取 `GL_QUERY_RESULT` 往往会阻塞 CPU 等 GPU 完成；应先用 `GL_QUERY_RESULT_AVAILABLE` 轮询，或延迟几帧消费结果。查询对象不能嵌套同一 target，begin/end 必须成对。

## 关键边界

### 本类仍是 compatibility 版本函数类

虽然 buffer object 是现代资源模型的基础，本类继承的矩阵栈、立即模式、client state、fixed-function lighting/fog 等仍是 deprecated。Core profile 代码应选择匹配的 Core 版本类，并用 vertex attribute API、shader 与 VAO 管理布局。

### `indices` 和 attribute pointer 的解释依赖 buffer binding

`glDrawElements()`、`glMultiDrawElements()`、`glVertexPointer()` 等函数的指针参数在 1.5 之后经常被当作 buffer offset。绑定状态错误时，最常见结果是把一个小 offset 当成非法 CPU 地址，或把 CPU 地址当成巨大的 buffer offset。

### `GL_ELEMENT_ARRAY_BUFFER` 的绑定语义特殊

索引 buffer 的绑定会影响后续 indexed draw。在更现代的 VAO 模型里，它还会被 VAO 记录。维护混合年代代码时，应明确在哪个初始化阶段绑定 EBO，避免 draw 时隐式状态串扰。

### Query 适合延迟决策，不适合立刻分支

Occlusion query 的价值在于跨帧或批量决策。如果每个对象刚画完 proxy 就立刻读取结果，CPU/GPU 并行性会被破坏，甚至比不做查询更慢。

## API 速查表

下表列出 1.5 新增接口，并按用途归纳继承的 1.0--1.4 能力。数值重载和历史变体按操作族合并说明。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop compatibility context 解析 1.5 与继承函数。 | 初始化失败后不得调用；context 必须在当前线程 current。 |
| `glGenBuffers`, `glDeleteBuffers`, `glBindBuffer`, `glIsBuffer` | 创建、删除、绑定和检查 buffer object。 | ID 属 context 共享组；绑定 target 决定后续 pointer/offset 语义。 |
| `glBufferData` | 为当前 target 的 buffer 分配存储并可选上传整块数据。 | `usage` 是性能提示；传 `nullptr` 可 orphan/重新分配存储。 |
| `glBufferSubData` | 更新当前 buffer 的一段字节范围。 | `offset + size` 不可越界；更新 GPU 正在使用的范围可能同步。 |
| `glGetBufferSubData` | 从当前 buffer 读回一段数据。 | 可能强制等待 GPU；输出缓冲区必须足够大。 |
| `glMapBuffer`, `glUnmapBuffer` | 将当前 buffer 映射到 CPU 地址并解除映射。 | 映射指针只在 unmap 前有效；`glUnmapBuffer` 返回 false 表示数据可能损坏。 |
| `glGetBufferParameteriv`, `glGetBufferPointerv` | 查询 buffer 大小、用法、映射状态或映射指针。 | 查询当前绑定 target；调试有用，热路径谨慎。 |
| `glGenQueries`, `glDeleteQueries`, `glIsQuery` | 创建、删除和检查 query object。 | query ID 也属于 context 共享组；删除前确认不再使用。 |
| `glBeginQuery`, `glEndQuery` | 开始/结束某个 target 的异步查询。 | 同一 target 不可嵌套；begin/end 必须配对。 |
| `glGetQueryiv`, `glGetQueryObjectiv`, `glGetQueryObjectuiv` | 查询 query target 能力与某个 query 的可用状态/结果。 | 读取 `GL_QUERY_RESULT` 可能阻塞；优先先查 `GL_QUERY_RESULT_AVAILABLE`。 |
| 继承的 1.4 功能：`glPointParameter*`, `glMultiDrawArrays`, `glMultiDrawElements`, `glBlendFuncSeparate`, `glWindowPos*`, `glSecondaryColor*`, `glFogCoord*` | 点参数、多批绘制、分离混合及 fixed-function 辅助属性。 | `glMultiDrawElements` 的 indices 受 EBO binding 影响；legacy 属性 Core 不可用。 |
| 继承的 1.3 功能：`glActiveTexture`, `glCompressedTexImage*`, `glCompressedTexSubImage*`, `glGetCompressedTexImage`, `glSampleCoverage`, `glClientActiveTexture`, `glMultiTexCoord*` | 多纹理单元、压缩纹理、sample coverage 和 fixed-function 多纹理坐标。 | compressed 数据须匹配块格式；client active texture 只影响旧 client arrays。 |
| 继承的 1.2 功能：`glTexImage3D`, `glTexSubImage3D`, `glDrawRangeElements`, `glBlendColor`, `glBlendEquation`, `glColorTable*`, `glConvolution*`, `glHistogram*`, `glMinmax*` | 3D texture、范围索引绘制、混合方程和 imaging subset。 | imaging subset 已废弃；上传/读回依赖 pixel-store state。 |
| 继承的 1.1/1.0 绘制与纹理：`glGenTextures`, `glBindTexture`, `glTexImage1D`, `glTexImage2D`, `glTexSubImage*`, `glDrawArrays`, `glDrawElements`, `glVertexPointer`, `glColorPointer`, `glNormalPointer`, `glTexCoordPointer`, `glEnableClientState` | 旧纹理对象、client arrays 与基础绘制。 | 绑定 VBO 后 pointer 是 offset；未绑定时是 CPU 地址。 |
| 继承的状态、查询和 fixed pipeline：`glViewport`, `glEnable`, `glDisable`, `glClear*`, `glDepth*`, `glStencil*`, `glBlendFunc`, `glGet*`, `glReadPixels`, `glMatrixMode`, `glBegin`, `glEnd`, `glLight*`, `glMaterial*`, `glTexEnv*`, `glNewList`, `glCallList*` | 基础 render state、读回、固定管线和其他 legacy 功能。 | Core/ES 不适用；查询和读回避免进入每帧热路径。 |

## 常见误区

### 创建了 VBO，却继续把真实 CPU 指针传给 `glVertexPointer()`

只要 `GL_ARRAY_BUFFER` 非零绑定，`pointer` 就会被解释为 buffer 内偏移。若想传 offset 0，应传空指针或明确的 0 offset，而不是某个数组地址。

### 每帧 map 同一块正在使用的 buffer

这会制造同步点。频繁流式更新应使用多 buffer、orphaning 或更高版本的映射策略；1.5 的 `glMapBuffer()` 粒度较粗，尤其要谨慎。

### 查询后立刻读取结果

Occlusion query 的读回应该延迟。立刻取 `GL_QUERY_RESULT` 等价于要求 GPU 现在完成前面命令，容易让优化适得其反。

## 一句话总结

`QOpenGLFunctions_1_5` 是旧桌面 OpenGL 迈向现代资源管理的关键过渡包装：buffer object 和 query object 很有迁移价值，但它仍处在 compatibility 语境里，必须清楚区分 CPU 指针、buffer offset、异步查询和 legacy 状态机。
