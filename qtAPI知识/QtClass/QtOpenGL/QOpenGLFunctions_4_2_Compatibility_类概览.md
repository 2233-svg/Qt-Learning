# QOpenGLFunctions_4_2_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_2_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.2 Compatibility profile；包含 4.2 Core API 与旧 fixed-function/legacy 接口

## 它解决什么问题

`QOpenGLFunctions_4_2_Compatibility` 让 Qt 程序在 OpenGL 4.2 Compatibility context 中同时访问 image load/store、memory barrier、immutable texture storage、base-instance draw 等现代能力，以及旧 fixed-function 和 deprecated API。它适合遗留 renderer 的渐进迁移，而不是新代码继续使用旧状态机的许可。

4.2 的现代能力会显著改变资源流转方式：shader 可以写 texture/image，后续 pass 可以读取这些结果，多个实例批次可以共享同一实例数据 buffer。Compatibility profile 允许这些新能力与旧 overlay、display list 或固定管线模块共存，但也扩大了状态污染和同步错误的范围。

## 实际使用场景

- 旧渲染器保留部分 fixed-function overlay，新后处理 pass 使用 image store；
- 在迁移过程中先用 `glTexStorage*()` 规范化纹理资源系统；
- 将大量实例数据集中管理，用 base-instance draw 替代多次小 draw；
- 为旧项目加入 GPU 侧统计或计数，但仍保留传统可视化代码。

## 初始化与隔离建议

```cpp
#include <QOpenGLFunctions_4_2_Compatibility>

QOpenGLFunctions_4_2_Compatibility gl;

bool initializeImagePath(GLuint texture)
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    gl.glBindImageTexture(0, texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA8);
    return true;
}
```

建议把 image load/store、barrier、FBO 和 shader pass 放入现代渲染模块；旧 fixed-function 模块只通过明确输入/输出资源与它交接。不要让旧模块随意改 texture binding、pixel store、FBO 或 barrier 相关资源状态。

## 现代 4.2 能力如何进入旧项目

### Immutable texture storage

`glTexStorage1D/2D/3D()` 可以让旧资源系统从“任意地方重新定义 texture level”变成“创建期固定格式，更新期只上传内容”。这一步常常是迁移到 FBO、image 和后处理链的基础。

### Image load/store 与 memory barrier

`glBindImageTexture()` 给 shader image uniform 绑定可读写资源；`glMemoryBarrier()` 描述 shader 写入何时对后续阶段可见。Compatibility context 不会替旧模块处理这些可见性问题；如果旧代码随后采样或复制该纹理，同样需要正确 barrier。

### Base-instance 绘制

`glDraw*BaseInstance()` 让实例数据 buffer 可以按批次偏移读取，有助于把旧的对象循环绘制改造成批处理。它适合替换大量重复 draw call，但需要实例 attribute divisor、VAO 和 buffer layout 一起设计。

## Compatibility 边界

### 旧像素路径和 image 路径不要混成一团

`glDrawPixels()`、`glCopyPixels()`、color table、histogram 等旧像素路径依赖大量 pixel store/transfer 状态；image load/store 又依赖 memory barrier 和 image format。混用时请明确阶段边界，必要时重设 pixel store 和 texture/image binding。

### Memory barrier 不是可选优化

只要 shader 写入的结果被后续 pass 读取，barrier 就是正确性需求。Compatibility profile 中旧模块读写同一资源时更应谨慎。

### Legacy API 仍是迁移对象

4.2 Compatibility 提供的固定管线接口不能移植到 Core/ES。新功能应建立在 Core 子集上，旧功能逐步替换。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 4.2 Compatibility profile 函数。 | profile 必须匹配；失败后不能调用成员。 |
| 4.2 texture/image：`glTexStorage1D`, `glTexStorage2D`, `glTexStorage3D`, `glBindImageTexture`, `glMemoryBarrier` | 不可变纹理存储、image unit 绑定和内存可见性控制。 | image format/access 要匹配 shader；barrier 是正确性需求。 |
| 4.2 query/format：`glGetActiveAtomicCounterBufferiv`, `glGetInternalformativ` | 查询 atomic counter buffer 与 internal format 能力。 | 初始化/反射阶段使用；避免热路径频繁查询。 |
| 4.2 draw：`glDrawArraysInstancedBaseInstance`, `glDrawElementsInstancedBaseInstance`, `glDrawElementsInstancedBaseVertexBaseInstance`, `glDrawTransformFeedbackInstanced`, `glDrawTransformFeedbackStreamInstanced` | 带 base-instance 或 transform-feedback 结果的实例化绘制。 | 需要 VAO、实例 attribute、buffer layout 和捕获状态配合。 |
| 继承的现代 Core 子集：`glGenProgramPipelines`, `glProgramUniform*`, `glViewportArrayv`, `glPatchParameter*`, `glDraw*Indirect`, `glGenSamplers`, `glVertexAttribDivisor`, `glFenceSync`, `glUniformBlockBinding`, `glBindVertexArray`, `glBindFramebuffer`, `glCreateShader`, `glUseProgram` | program pipeline、tessellation、indirect draw、sampler、instancing、sync、UBO、VAO/FBO 和 GLSL。 | 新模块优先使用这些能力，保持可迁移到 Core。 |
| legacy 几何/矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式与固定矩阵栈。 | 只保留在旧模块；新代码用 VAO/VBO 与 shader。 |
| legacy 光照/像素/反馈：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glVertexPointer`, `glEnableClientState`, `glDrawPixels`, `glColorTable*`, `glConvolution*`, `glNewList`, `glCallList*`, `glSelectBuffer`, `glFeedbackBuffer` | 固定管线、client arrays、传统像素、display list 与反馈模式。 | 不适用于 Core/ES；与 image/barrier 路径混用时状态风险更高。 |

## 常见误区

### image 写入后让旧 fixed-function 纹理路径直接读取

旧路径能读纹理不代表内存可见。仍需根据下一步访问类型调用合适的 `glMemoryBarrier()`。

### 旧资源系统继续重定义 immutable texture

一旦改用 `glTexStorage*()`，资源生命周期要随之改变。重新定义格式/层级的旧代码必须迁移为重建 texture 或仅更新内容。

### 把 base-instance 当成立即模式循环的简单替代

它要求实例数据、attribute divisor、VAO 和 shader 一起配套。没有现代顶点输入布局，base-instance 本身无法发挥作用。

## 一句话总结

`QOpenGLFunctions_4_2_Compatibility` 让旧 Qt OpenGL 项目能接入 image load/store、不可变纹理和 base-instance 绘制；但这些能力必须在隔离良好的现代子路径中使用，不能任由 legacy 状态机继续蔓延。
