# QOpenGLTextureBlitter 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLTextureBlitter>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：无  
> 定位：用内置 shader 和几何数据把纹理快速绘制成屏幕/目标矩形

## 它解决什么问题

`QOpenGLTextureBlitter` 封装了“画一个带纹理的四边形”这件常见但重复的工作：准备顶点数据、shader、program、坐标变换、纹理采样和 draw call。很多 2D UI、离屏渲染、后处理、FBO 预览最终都只是把一张纹理画到某个矩形上；这个类让你不必为每个项目重写一套 blit shader。

它不是通用 sprite renderer，也不管理 framebuffer、viewport、blend、depth、scissor 或 texture 对象本身。它只负责在当前 OpenGL context 中绑定自己的绘制资源，并把你传入的纹理 id 画出来。

## 实际使用场景

- 把 `QOpenGLFramebufferObject::texture()` 绘制到窗口的某个像素矩形；
- 在多 pass 渲染后，把中间纹理调试显示到屏幕角落；
- 把 `QImage` 上传得到的纹理画出来，并处理上下翻转或 BGRA/RGBA 通道差异；
- 在 Qt 内部/应用框架中以很薄的 OpenGL 路径完成纹理拷贝式呈现；
- 处理 `GL_TEXTURE_RECTANGLE` 或 `GL_TEXTURE_EXTERNAL_OES` 目标前先做支持查询。

## 基本流程

```cpp
#include <QOpenGLTextureBlitter>

void paintTexture(QOpenGLTextureBlitter &blitter,
                  GLuint texture,
                  const QRectF &target,
                  const QRect &viewport)
{
    const QMatrix4x4 transform =
        QOpenGLTextureBlitter::targetTransform(target, viewport);

    blitter.bind(GL_TEXTURE_2D);
    blitter.blit(texture, transform, QOpenGLTextureBlitter::OriginBottomLeft);
    blitter.release();
}
```

`create()` 必须在有效 OpenGL context current 时调用；析构时若没有当初创建资源的 context 或共享 context current，底层资源可能不会被释放，所以推荐在 GL 清理阶段手动调用 `destroy()`。

## 核心语义

### 构造不创建 OpenGL 资源

默认构造只是普通 C++ 对象初始化，不碰 OpenGL。这样可以安全地把它作为类成员。真正的 shader/program/buffer 等图形资源在 `create()` 中创建。

### `bind()` 到 `blit()` 之间保持状态干净

`bind(target)` 会绑定 blitter 内部 program 和相关资源。文档明确建议：`bind()` 和 `blit()` 之间避免改 OpenGL 状态，否则可能和 blitter 内部状态冲突。绘制完调用 `release()`。

### origin 解决上下方向问题

FBO 附件通常按 OpenGL 坐标习惯理解，传 `OriginBottomLeft`；普通未翻转图片数据常是 Y 从上到下，传 `OriginTopLeft`。这比先用 `QImage::flipped()` 在 CPU 上翻图更便宜。

### opacity 不会自动配置 blend

`setOpacity()` 只改变 shader 中使用的不透明度。blitter 不会替你启用或配置混合；如果希望半透明生效，调用方要设置 `glEnable(GL_BLEND)` 和正确的 blend func。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `enum Origin { OriginBottomLeft, OriginTopLeft }` | 描述源纹理 Y 方向。 | FBO 纹理多用 `OriginBottomLeft`；普通图片数据多用 `OriginTopLeft`。 |
| `QOpenGLTextureBlitter()` | 构造 blitter 包装对象。 | 不创建图形资源，可安全作为成员变量。 |
| `~QOpenGLTextureBlitter()` | 析构对象。 | 若当前没有创建时的 context/共享 context，图形资源可能无法释放；优先手动 `destroy()`。 |
| `create()` | 初始化 blitter 需要的 shader/program/buffer 等 OpenGL 资源。 | 必须有 current context；无 context 或 shader 编译失败会返回 `false`。 |
| `isCreated() const` | 查询 `create()` 是否成功。 | 只是资源状态，不代表当前 context 已正确绑定。 |
| `destroy()` | 释放 blitter 持有的图形资源。 | 需要创建时的 context 或共享 context current；未创建时无效果。 |
| `supportsExternalOESTarget() const` | 判断 `bind()` 是否支持 `GL_TEXTURE_EXTERNAL_OES`。 | 常见于移动端相机/视频纹理；使用前先查。 |
| `supportsRectangleTarget() const` | 判断 `bind()` 是否支持 `GL_TEXTURE_RECTANGLE`。 | rectangle texture 坐标规则不同，不是所有平台都有。 |
| `bind(GLenum target = GL_TEXTURE_2D)` | 绑定 blitter 内部绘制资源并指定源纹理 target。 | target 只能是 `GL_TEXTURE_2D`、`GL_TEXTURE_RECTANGLE` 或 `GL_TEXTURE_EXTERNAL_OES`。 |
| `release()` | 解绑 blitter 内部资源。 | 绘制结束后调用，避免影响后续渲染。 |
| `setOpacity(float opacity)` | 设置 blit 输出透明度，默认 1.0。 | 不会自动设置 blend state；调用方负责混合配置。 |
| `setRedBlueSwizzle(bool swizzle)` | 在 shader 中交换红蓝通道。 | 适合小端系统上类似 `QImage::Format_ARGB32` 的 BGRA 数据；FBO/RGBA8888 通常不需要。 |
| `blit(GLuint texture, const QMatrix4x4 &targetTransform, Origin sourceOrigin)` | 绘制整张纹理到目标变换指定的位置。 | 先 `bind()`；用 origin 处理 Y 翻转。 |
| `blit(GLuint texture, const QMatrix4x4 &targetTransform, const QMatrix3x3 &sourceTransform)` | 按源变换绘制纹理子区域。 | `sourceTransform()` 通常负责生成子纹理矩阵。 |
| `static targetTransform(const QRectF &target, const QRect &viewport)` | 生成目标矩形到 viewport 的变换矩阵。 | target/viewport 单位是像素；尺寸相等时是不缩放输出。 |
| `static sourceTransform(const QRectF &subTexture, const QSize &textureSize, Origin origin)` | 生成源子矩形采样变换。 | `subTexture` 用像素坐标；origin 决定 Y 方向。 |

## 常见误区

### 忘记在 GL 清理阶段调用 `destroy()`

析构函数不一定有合适的 OpenGL context。`QOpenGLWidget` 中通常在 `aboutToBeDestroyed` 或显式清理路径里 `makeCurrent()` 后 `destroy()`。

### 以为 `setOpacity()` 自动半透明

opacity 只是 shader 参数。如果 blend 没开，或者 blend func 不对，结果仍可能是不透明覆盖。

### 把 `OriginTopLeft` 和目标矩形翻转混在一起

源纹理 origin 只描述采样方向；目标矩形描述画到哪里。上下颠倒时先判断源数据来自 FBO 还是普通图片，不要同时翻源和翻目标。

### 在 `bind()` 后插入自己的 OpenGL 状态修改

blitter 内部依赖已绑定的 program、buffer 和 texture target。额外修改状态容易让 `blit()` 画错或失败。需要改状态时放在 `bind()` 前或 `release()` 后。

## 一句话总结

`QOpenGLTextureBlitter` 是“把纹理画到矩形上”的轻量工具；它省掉重复 shader 和矩阵代码，但 context 生命周期、blend 状态、源方向和目标资源仍由调用方负责。
