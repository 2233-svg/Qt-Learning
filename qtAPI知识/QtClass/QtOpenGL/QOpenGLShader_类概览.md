# QOpenGLShader 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLShader>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QObject`  
> 定位：封装单个 OpenGL shader 对象的创建、源码保存和编译

## 它解决什么问题

`QOpenGLShader` 把 OpenGL shader 对象包装成 Qt 的 `QObject`，负责创建指定阶段的 shader、设置源码、调用驱动编译器、保存编译日志，并在销毁时处理底层 shader 对象。它不负责把多个 shader 链接成可用 program；这一步由 `QOpenGLShaderProgram` 完成。

它解决的是 OpenGL shader 编译流程中最重复、最容易漏错误处理的部分：根据当前 context 创建 shader，传入源码，编译，检查成功状态，读取 info log。你仍然需要理解 GLSL/GLSL ES 版本、profile、扩展和驱动差异，因为 Qt 只是转交源码给底层 OpenGL 编译器。

## 实际使用场景

- 在 `initializeGL()` 中编译 vertex/fragment shader，再交给 `QOpenGLShaderProgram` 链接；
- 对 geometry、tessellation、compute 等阶段做能力检查后再创建对应 shader；
- 在资源系统中单独编译 shader，并把编译日志展示给开发者；
- 需要取得底层 `shaderId()`，和少量原生 OpenGL shader API 配合。

## 基本流程

```cpp
#include <QOpenGLShader>
#include <QOpenGLShaderProgram>

bool buildProgram(QOpenGLShaderProgram &program, const QByteArray &vs, const QByteArray &fs)
{
    QOpenGLShader vertex(QOpenGLShader::Vertex);
    if (!vertex.compileSourceCode(vs))
        return false;

    QOpenGLShader fragment(QOpenGLShader::Fragment);
    if (!fragment.compileSourceCode(fs))
        return false;

    program.addShader(&vertex);
    program.addShader(&fragment);
    return program.link();
}
```

构造、编译和销毁都和当前 `QOpenGLContext` 相关。通常把它放在 context 已 current 的初始化阶段，例如 `QOpenGLWidget::initializeGL()`。

## Shader 类型边界

`ShaderTypeBit` 指定 shader 阶段：

- `Vertex`：顶点 shader，OpenGL/ES shader pipeline 的基础阶段；
- `Fragment`：片元 shader，和 vertex shader 一起构成最常见的可绘制 program；
- `Geometry`：需要 OpenGL 3.2+ 或 OpenGL ES 3.2+；
- `TessellationControl` / `TessellationEvaluation`：需要 OpenGL 4.0+ 或 OpenGL ES 3.2+；
- `Compute`：需要 OpenGL 4.3+ 或 OpenGL ES 3.1+。

`ShaderType` 是 `QFlags<ShaderTypeBit>`。构造单个 `QOpenGLShader` 时通常只传一个阶段；能力查询可以组合或分别查询。

## 关键 API 语义与边界

### 编译只验证单个阶段

`compileSourceCode()` 和 `compileSourceFile()` 只做 shader 编译。attribute/uniform 是否匹配、varying/interface block 是否兼容、多个阶段能否一起工作，要到 program link 时才知道。

### `log()` 是主要诊断入口

返回 `false` 后应立即读取 `log()`。驱动日志可能包含 warning，也可能在成功编译时仍有提示。不要只依赖 `glGetError()`。

### 源码应视为可信内容

Qt 文档明确提醒：shader 源码会经过最小处理后交给底层 OpenGL 编译器，而驱动编译器对 Qt 来说是黑盒。不要把未约束的用户输入直接传给 `compileSourceFile()` 或 `compileSourceCode()`。

### 销毁和 program 附着的关系

如果 shader 已附着到 `QOpenGLShaderProgram`，销毁 `QOpenGLShader` 对象并不一定马上让底层 shader 消失；OpenGL 会让它在 program 不再需要后释放。尽管如此，应用层仍应避免在 context 已销毁后才依赖析构清理。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `enum ShaderTypeBit` / `ShaderType` | 表示 shader 阶段：vertex、fragment、geometry、tessellation、compute。 | 后三个/四个阶段依赖更高 OpenGL 或 OpenGL ES 版本；先用 `hasOpenGLShaders()` 判断。 |
| `QOpenGLShader(ShaderType type, QObject *parent = nullptr)` | 创建指定类型的 shader 对象，并关联当前 context。 | 构造后通常立刻编译；需要 current `QOpenGLContext`。 |
| `~QOpenGLShader()` | 销毁 Qt shader 对象，并按 OpenGL 规则释放底层 shader。 | 已附着到 program 的底层 shader 可能延后到 program 销毁后释放。 |
| `compileSourceCode(const char *source)` | 从 C 字符串设置源码并编译。 | 字符串生命周期只需覆盖调用；失败看 `log()`。 |
| `compileSourceCode(const QByteArray &source)` | 从字节数组设置源码并编译。 | 适合从资源文件或缓存读取的 GLSL/GLSL ES 源码。 |
| `compileSourceCode(const QString &source)` | 从 `QString` 设置源码并编译。 | 注意编码和换行；驱动最终处理的是源码文本。 |
| `compileSourceFile(const QString &fileName)` | 读取文件内容作为源码并编译。 | 文件打开失败和编译失败都会返回 `false`；不要直接编译不可信路径。 |
| `isCompiled() const` | 查询最近编译是否成功。 | 只代表单个 shader 阶段，不代表 program 可链接。 |
| `log() const` | 返回最近编译产生的错误和警告。 | 成功时也可能有 warning；失败时这是首要排查信息。 |
| `sourceCode() const` | 返回当前保存的源码。 | 可用于调试输出，但不等于驱动最终内部表示。 |
| `shaderType() const` | 返回 shader 阶段类型。 | 用于资源系统断言和调试。 |
| `shaderId() const` | 返回底层 OpenGL shader 名称。 | 只有在需要原生 API 时使用；不能跨不共享的 context 使用。 |
| `static hasOpenGLShaders(ShaderType type, QOpenGLContext *context = nullptr)` | 查询指定 shader 类型是否受支持。 | `context == nullptr` 时使用当前 context；非基础阶段必须先查。 |

## 常见误区

### 编译成功就以为能渲染

一个 shader 编译成功只说明这一阶段语法和单阶段约束通过。真正可用还要 program link 成功、uniform/attribute 设置正确、OpenGL 状态匹配。

### 在没有 current context 的地方编译

`QOpenGLShader` 底层是 OpenGL 对象，不能脱离当前 context 创建和编译。把编译放进普通 C++ 构造函数很容易太早。

### 忽略驱动和 GLSL 方言差异

桌面 GLSL 与 GLSL ES 在精度限定符、内置变量、版本声明上不同。需要跨平台时，尽量写 GLSL ES 兼容源码，或者按 context 生成不同源码。

## 一句话总结

`QOpenGLShader` 是单个 shader 阶段的 Qt 封装；它让编译和日志处理更顺手，但 shader 版本、阶段支持、安全输入和 program link 仍需要调用方认真管理。
