# QOpenGLFunctions_2_1 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_2_1>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 2.1 compatibility API；Qt 以 OpenGL ES 2 构建时不可用，且继承的 legacy 成员不适用于 Core-only context

## 它解决什么问题

`QOpenGLFunctions_2_1` 在 Qt 中提供 OpenGL 2.1 及此前规范的版本化函数入口。它的新增 API 很集中：六个 `glUniformMatrix*fv()` 非方阵变体，使 shader 可以直接接收 2x3、3x2、2x4、4x2、3x4、4x3 的 float 矩阵数组。

这看似很小，却解决了早期 GLSL 里“为了上传 affine transform、骨骼调色板的压缩表示、2D/3D 坐标变换而把数据硬塞进 4x4 矩阵”的问题。它不改变 shader/program/attribute 的基本模型，也不提供新资源对象；它是 2.0 programmable pipeline 的细化版本。

若项目只需要方阵 `mat2/mat3/mat4`，使用 `QOpenGLFunctions_2_0` 即足够。若 shader 真实声明了 GLSL 非方阵矩阵类型，或必须兼容一套 OpenGL 2.1 desktop renderer，本类才有明确价值。

## 实际使用场景

- 给 GLSL `mat3x2`、`mat4x3` 等非方阵 uniform 上传数组；
- 将二维仿射变换、紧凑 3D frame 或预计算权重以非 4x4 格式交给 shader；
- 维护以 OpenGL 2.1 为最低桌面能力的旧渲染后端；
- 在升级到更现代 Core profile 前，保持一个明确的桌面兼容函数集。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_2_1>

QOpenGLFunctions_2_1 gl;

void uploadAffineColumns(GLint location, const GLfloat *matrices, GLsizei count)
{
    // 当前 context 已 current，且使用中的 shader program 声明了 mat3x2 uniform。
    gl.glUniformMatrix3x2fv(location, count, GL_FALSE, matrices);
}
```

使用前仍要先检查 `initializeOpenGLFunctions()`。`location` 必须来自当前 program 的 `glGetUniformLocation()`；若 program 切换或 relink，旧 location 不能继续假定有效。

## 非方阵矩阵的语义与内存布局

`glUniformMatrixCxRfv()` 中的 `C` 是列数、`R` 是行数，对应 GLSL 的 `matCxR`。例如 `glUniformMatrix3x2fv()` 对应 `mat3x2`，每个矩阵有 3 列、每列 2 个 float，共 6 个 float；`glUniformMatrix4x3fv()` 对应 `mat4x3`，每个矩阵有 12 个 float。

OpenGL/GLSL 的默认约定是 column-major。传入 `GL_FALSE` 时，内存应按列连续排列；`count > 1` 时，矩阵之间紧密连续。桌面 GL 支持 `transpose = GL_TRUE`，但跨 API 或将代码移植到 OpenGL ES 时不应依赖它，最好在 CPU 侧统一布局、始终上传 `GL_FALSE`。

非方阵矩阵不能随意当作 4x4 的可替代物。它们的乘法维度由 GLSL 类型决定，例如 `mat3x2 * vec3` 的结果是 `vec2`。设计 uniform 数据时先从 shader 中的数学方向和维度出发，而不是只看内存能否塞进去。

## 关键边界

### 仅扩展 uniform 上传，不扩展固定管线

2.1 的六个新函数服务 programmable pipeline。它们不会让固定矩阵栈理解非方阵矩阵，也不会让 `glMatrixMode()`、`glLoadMatrix*()` 获得新能力。旧 fixed-function 路径仍应被视为迁移对象。

### 写入目标始终是当前 program

`glUniformMatrix*()` 不接收 program 参数。若没有有效的 current program，或 `location` 不属于当前 program，会产生错误或无效更新。采用 Qt 的 `QOpenGLShaderProgram` 时，先 `bind()`，再通过其 uniform API 或本类设置值。

### `count` 表示矩阵个数，不是 float 个数

例如上传两个 `mat4x3` 时，`count` 传 `2`，数据数组需有 24 个 float。把元素数量误传给 `count` 会导致 OpenGL 读取越界内存。

### 版本包装仍带有 compatibility 历史包袱

本类继承 2.0 的 shader API，也继承 1.x 的 immediate mode、client array、fixed lighting、display list 等 API。对 Core profile 的新代码，应当选择相应的 Core functions，而不是因“2.1 比 2.0 更新”就把它视为现代完整能力集。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop context 解析 2.1 与继承函数。 | context 必须 current；初始化失败后不得调用成员。 |
| `glUniformMatrix2x3fv` | 上传 GLSL `mat2x3` 数组。 | 每项 6 个 float，默认按两列、每列三项布局。 |
| `glUniformMatrix3x2fv` | 上传 GLSL `mat3x2` 数组。 | 每项 6 个 float，默认按三列、每列两项布局。 |
| `glUniformMatrix2x4fv` | 上传 GLSL `mat2x4` 数组。 | 每项 8 个 float；`count` 是矩阵数。 |
| `glUniformMatrix4x2fv` | 上传 GLSL `mat4x2` 数组。 | 每项 8 个 float；检查 shader 的精确 uniform 类型。 |
| `glUniformMatrix3x4fv` | 上传 GLSL `mat3x4` 数组。 | 每项 12 个 float；通常用 `GL_FALSE` 保持 column-major。 |
| `glUniformMatrix4x3fv` | 上传 GLSL `mat4x3` 数组。 | 每项 12 个 float；不能把 float 数量误作为 `count`。 |
| 继承的 shader/program：`glCreateShader`, `glShaderSource`, `glCompileShader`, `glGetShader*`, `glCreateProgram`, `glAttachShader`, `glLinkProgram`, `glGetProgram*`, `glUseProgram`, `glDeleteShader`, `glDeleteProgram`, `glValidateProgram` | 创建、编译、链接、使用和诊断 GLSL program。 | 分别检查 compile/link 状态和 info log；program 使用受 current context 约束。 |
| 继承的 attribute/uniform：`glBindAttribLocation`, `glGetAttribLocation`, `glVertexAttribPointer`, `glEnableVertexAttribArray`, `glDisableVertexAttribArray`, `glGetVertexAttrib*`, `glGetUniformLocation`, `glGetActiveUniform`, `glUniform*`, `glUniformMatrix2fv`, `glUniformMatrix3fv`, `glUniformMatrix4fv` | 定义顶点输入并设置常规 uniform。 | VBO 绑定时 pointer 是 offset；uniform location 只对对应且未 relink 的 program 有效。 |
| 继承的输出状态：`glDrawBuffers`, `glBlendEquationSeparate`, `glStencilFuncSeparate`, `glStencilMaskSeparate`, `glStencilOpSeparate` | 配置 MRT、独立 RGB/Alpha blend equation 和双面 stencil。 | 输出、attachment、shader 及 FBO 配置必须一致。 |
| 继承的 buffer/query：`glGenBuffers`, `glBindBuffer`, `glBufferData`, `glBufferSubData`, `glMapBuffer`, `glUnmapBuffer`, `glGetBuffer*`, `glGenQueries`, `glBeginQuery`, `glEndQuery`, `glGetQuery*` | 管理 GPU buffer 与异步 query。 | 映射期间正确 unmap；延迟读取 query result 以避免同步。 |
| 继承的纹理：`glActiveTexture`, `glCompressedTexImage*`, `glCompressedTexSubImage*`, `glTexImage3D`, `glTexSubImage3D`, `glGenTextures`, `glBindTexture`, `glTexParameter*` | 多纹理、压缩/3D 纹理和传统纹理对象管理。 | sampler 取逻辑 unit；压缩数据、尺寸和 pixel-store state 要匹配。 |
| 继承的 compatibility API：`glDrawArrays`, `glDrawElements`, `glVertexPointer`, `glEnableClientState`, `glMatrixMode`, `glBegin`, `glEnd`, `glLight*`, `glMaterial*`, `glTexEnv*`, `glMultiTexCoord*`, `glColorTable*`, `glNewList`, `glCallList*` | 旧数组、固定管线和其他 legacy 功能。 | 不适用于 Core/ES；新代码应落在 shader + buffer 路径。 |

## 常见误区

### 将 `mat3x2` 当成 2 行 3 列的 row-major 数组上传

GLSL 名称中的 `3x2` 是 3 列、2 行。若 CPU 数据以 row-major 排列却传 `GL_FALSE`，变换会悄悄错位；应统一 CPU 数学库和上传布局。

### uniform location 来自另一个 program

location 不是全局编号。切换 program、重新 link 或重建 shader 后，都必须按当前 program 重新获取所需 location。

### 为了使用非方阵 uniform 而继续维持 fixed-function 渲染

2.1 的价值正是让数据更自然地进入 GLSL。它应推动矩阵、光照和纹理计算收敛到 shader，而不是给旧矩阵栈再加一层补丁。

## 一句话总结

`QOpenGLFunctions_2_1` 是 OpenGL 2.0 shader 路径的精确补充：它专门解决 GLSL 非方阵矩阵 uniform 的上传问题，可靠使用的关键是读对列/行维度、保持内存布局一致，并始终在当前 program 上写入。
