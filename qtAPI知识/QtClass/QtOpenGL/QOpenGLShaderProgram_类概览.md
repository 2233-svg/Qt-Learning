# QOpenGLShaderProgram 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLShaderProgram>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QObject`  
> 定位：封装 OpenGL shader program 的编译、链接、绑定和参数设置

## 它解决什么问题

`QOpenGLShaderProgram` 把多个 `QOpenGLShader` 或源码片段链接成一个可绑定的 OpenGL program，并提供 attribute、uniform、tessellation 参数和 program 二进制缓存的便捷接口。它把常见的 `glCreateProgram()`、`glAttachShader()`、`glLinkProgram()`、`glUseProgram()`、`glUniform*()`、`glVertexAttribPointer()` 等操作包装成 Qt 风格 API。

它解决的是 shader program 生命周期和参数设置的工程化问题：代码不用手动维护大量 OpenGL 名称和重载函数，也能通过 `log()` 获取编译/链接诊断。但它不是一个完整材质系统，不会替你管理纹理单元、UBO/SSBO、VAO、pipeline state 或多线程同步。

## 实际使用场景

- 在 `initializeGL()` 中把 vertex/fragment shader 源码编译、链接成一个绘制 program；
- 用 `bindAttributeLocation()` 固定 attribute 位置，和 VAO/VBO 布局稳定配合；
- 在每帧绘制前 `bind()`，再用 `setUniformValue()` 传矩阵、颜色、采样器编号；
- 使用 `addCacheableShaderFromSourceCode()` 减少下次启动时的 shader 编译/链接成本；
- 调试 GLSL/GLSL ES 编译和链接失败，把 `log()` 输出到开发日志。

## 基本流程

```cpp
#include <QOpenGLShaderProgram>

bool initProgram(QOpenGLShaderProgram &program)
{
    program.addShaderFromSourceCode(QOpenGLShader::Vertex, R"(
        attribute highp vec3 position;
        uniform highp mat4 mvp;
        void main() { gl_Position = mvp * vec4(position, 1.0); }
    )");

    program.addShaderFromSourceCode(QOpenGLShader::Fragment, R"(
        uniform lowp vec4 color;
        void main() { gl_FragColor = color; }
    )");

    program.bindAttributeLocation("position", 0);
    return program.link();
}
```

正常使用可以不显式调用 `create()`，program id 会按需创建。只有你要把 `programId()` 交给原生 API 或加载 program binary 时，才需要提前 `create()`。

## 核心语义

### add/compile/link/bind 是分层流程

`addShader()` 只把已有 shader 附着到 program；`addShaderFromSourceCode()` / `addShaderFromSourceFile()` 会先创建并编译 shader，再添加到 program；`link()` 才真正检查各阶段接口是否匹配；`bind()` 会把 program 设为当前 context 的活动 program。如果 program 尚未链接或需要重链接，`bind()` 会尝试调用 `link()`。

### 位置查询可能返回 `-1`

`attributeLocation()` 和 `uniformLocation()` 返回 `-1` 表示名称不是有效 attribute/uniform。常见原因包括变量拼写错误、shader 编译出的接口不同、变量被优化掉，或 program 还没成功链接。不要把 `-1` 当作可用位置继续设置。

### attribute 与 uniform 是不同状态层

attribute 描述每个顶点的输入：常量值、客户端数组或当前绑定 VBO 中的布局。uniform 是当前 program 的全局参数：矩阵、颜色、开关、采样器编号等。设置 uniform 前通常要让 program 已链接并处于当前 context；attribute array 还要和 VAO/VBO 状态配合。

### cacheable 变体依赖驱动能力

`addCacheableShaderFromSourceCode()` 和 `addCacheableShaderFromSourceFile()` 在支持 program binary 的环境中会缓存 program 二进制；不可用时行为等价于普通 add 变体。驱动版本变化或 binary format 不兼容时，Qt 会回退到源码编译和链接。

### 源码安全边界

Qt 文档明确要求把传入 shader/program 的数据视为可信内容。源码会交给底层驱动编译器，而驱动编译器是黑盒。不要把任意用户上传的 shader 源码直接编译执行。

## 跨平台 shader 注意点

桌面 GLSL 和 GLSL ES 有差异：GLSL ES 有 `highp`、`mediump`、`lowp` 精度限定符，桌面 GLSL 旧版本没有；桌面 OpenGL 有一些固定管线时代的内置变量，GLSL ES 没有。`QOpenGLShaderProgram` 会在桌面 OpenGL 上为精度限定符加空定义，让很多 GLSL ES 风格 shader 能运行，但这不等于所有语言特性都自动兼容。

如果目标是跨桌面和 ES，最好主动避免依赖只在某一端存在的内置变量，并按 context/profile 控制 `#version`、输入输出语法和扩展。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| 构造/销毁：`QOpenGLShaderProgram(QObject *parent = nullptr)`, `~QOpenGLShaderProgram()` | 创建/销毁 program 包装对象。 | OpenGL 资源依赖 context；不要把清理拖到 context 已失效之后。 |
| 资源创建：`create()`, `programId()` | 提前创建并取得底层 OpenGL program 名称。 | 普通使用可按需创建；需要原生 binary/API 时才显式创建。 |
| 添加 shader：`addShader(QOpenGLShader *)`, `removeShader()`, `removeAllShaders()`, `shaders()` | 管理附着到 program 的 shader 列表。 | `addShader()` 不取得 QObject 所有权；移除后若已链接，重新链接才会反映变化。 |
| 源码添加：`addShaderFromSourceCode()`, `addShaderFromSourceFile()` | 从源码或文件创建、编译并添加 shader。 | 返回 `false` 时读取 `log()`；文件/源码应来自可信来源。 |
| 可缓存源码添加：`addCacheableShaderFromSourceCode()`, `addCacheableShaderFromSourceFile()` | 允许 Qt 缓存 program binary，后续加速 link。 | 不支持 binary 时等价普通 add；驱动变化会触发回退编译。 |
| 链接与日志：`link()`, `isLinked()`, `log()` | 链接 program、查询链接状态和错误/警告信息。 | `link()` 可重入并强制重链接；失败首看 `log()`。 |
| 绑定：`bind()`, `release()` | 调用等价 `glUseProgram(programId())` / `glUseProgram(0)`。 | `bind()` 可能隐式 link；绑定只影响当前 context。 |
| 能力查询：`static hasOpenGLShaderPrograms(QOpenGLContext *context = nullptr)` | 判断当前或指定 context 是否支持 GLSL shader program。 | `nullptr` 使用当前 context；初始化前查询可能没有意义。 |
| Attribute 位置：`bindAttributeLocation()`, `attributeLocation()` | 固定或查询 attribute 位置。 | `bindAttributeLocation()` 在 link 前生效最清楚；link 后调用需要重新 link。 |
| Attribute 常量：`setAttributeValue()` | 设置某个 attribute 的常量值。 | 只有对应 attribute array 未启用时才作为顶点输入。 |
| Attribute 数组：`setAttributeArray()`, `setAttributeBuffer()`, `enableAttributeArray()`, `disableAttributeArray()` | 描述并启用顶点数组输入。 | `setAttributeBuffer()` 使用当前绑定 VBO；Qt 版本会启用 normalization，不想归一化时用底层 `glVertexAttribPointer()`。 |
| Uniform 位置：`uniformLocation()` | 查询 uniform location。 | `-1` 代表无效或被优化掉；不要继续设置。 |
| Uniform 单值：`setUniformValue()` | 设置 float/int/uint、向量、颜色、点、尺寸、矩阵、transform 等 uniform。 | program 应已链接并在当前 context 中使用；sampler 传的是纹理单元编号。 |
| Uniform 数组：`setUniformValueArray()` | 设置 uniform 数组或矩阵数组。 | `count` 是元素个数；裸 `GLfloat *` 的 `tupleSize` 必须是 1 到 4。 |
| Geometry 查询：`maxGeometryOutputVertices()` | 查询 geometry shader 最大输出顶点数。 | 只有 geometry shader 可用平台才有实际意义。 |
| Tessellation：`setPatchVertexCount()`, `patchVertexCount()`, `setDefaultOuterTessellationLevels()`, `defaultOuterTessellationLevels()`, `setDefaultInnerTessellationLevels()`, `defaultInnerTessellationLevels()` | 设置/查询 patch 顶点数和默认 tessellation level。 | 修改的是全局 OpenGL 状态，不属于某个 program；OpenGL 4.0+，且 ES 3.2 有限制。 |

## 常见误区

### 忘记 attribute 位置要在 link 前固定

`bindAttributeLocation()` 可以在 link 后调用，但必须重新 link 才生效。可维护的做法是：添加 shader 后、link 前统一绑定 attribute 位置。

### 看到 `bind()` 返回 false 却不看 `log()`

`bind()` 可能触发隐式 `link()`。失败时日志仍然在 `log()`，而不是 OpenGL error code 里。

### 把 uniform 设置和纹理绑定混为一谈

sampler uniform 存的是纹理单元索引，例如 `0` 表示 `GL_TEXTURE0`。实际 texture 仍要用 OpenGL/Qt texture API 绑定到相应单元。

### 以为 tessellation 相关函数是对象状态

`setPatchVertexCount()` 和默认 tessellation levels 是全局 OpenGL 状态的便捷包装，切换 program 时不会由 Qt 自动恢复。需要在渲染函数中按 pass 设置。

## 一句话总结

`QOpenGLShaderProgram` 是 Qt OpenGL 里管理 shader program 的主入口；它把编译、链接、绑定和参数设置做得顺手，但 OpenGL context、GLSL 兼容性、位置有效性和全局渲染状态仍必须由调用方掌控。
