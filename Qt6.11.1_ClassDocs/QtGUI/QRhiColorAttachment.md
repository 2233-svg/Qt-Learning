# QRhiColorAttachment

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiColorAttachment`

## 1. 先建立直觉

`QRhiColorAttachment` 描述一次 texture render target 中的一个颜色输出附件。片段着色器输出的颜色最终写到哪里，可能是 `QRhiTexture` 的某个 mip level / array layer，也可能是 `QRhiRenderBuffer`。如果使用 MSAA，它还可以指定一个非多采样 resolve texture，让渲染结束时自动解析。

它本身不是 GPU 资源，而是 render target description 中的小型描述对象。真正的资源是被它引用的 texture 或 render buffer。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- API 层级：Qt GUI 私有 API
- 常见宿主：`QRhiTextureRenderTargetDescription`
- 可引用对象：`QRhiTexture` 或 `QRhiRenderBuffer`，二者不能同时设置

颜色附件的 layer/level 只在 texture 场景下有意义。render buffer 通常用于不可采样的渲染附件，尤其是 MSAA 临时颜色缓冲。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QRhiColorAttachment()` | 创建空附件描述。 |
| `QRhiColorAttachment(QRhiTexture*)` | 指定纹理作为颜色附件。 |
| `QRhiColorAttachment(QRhiRenderBuffer*)` | 指定渲染缓冲作为颜色附件。 |
| `setTexture()` / `texture()` | 设置/读取颜色附件纹理。 |
| `setRenderBuffer()` / `renderBuffer()` | 设置/读取颜色附件 render buffer。 |
| `setLevel()` / `level()` | 指定渲染到纹理的哪个 mip level。 |
| `setLayer()` / `layer()` | 指定纹理数组层、cubemap face 或 3D slice。 |
| `setResolveTexture()` / `resolveTexture()` | 设置 MSAA 自动解析目标纹理。 |
| `setResolveLevel()` / `resolveLevel()` | 指定 resolve 目标 mip level。 |
| `setResolveLayer()` / `resolveLayer()` | 指定 resolve 目标 layer。 |
| `setMultiViewCount()` / `multiViewCount()` | Qt 6.7 起设置多视图渲染的视图数。 |

## 4. 关键用法

### 渲染到纹理

```cpp
QRhiTexture *colorTex = rhi->newTexture(QRhiTexture::RGBA8, size, 1,
                                        QRhiTexture::RenderTarget);
colorTex->create();

QRhiColorAttachment color(colorTex);
QRhiTextureRenderTargetDescription desc(color);
```

如果渲染后需要采样这张纹理，颜色附件应使用 `QRhiTexture`，并保证创建纹理时带有合适的 render target 使用标志。

### MSAA render buffer + resolve texture

```cpp
QRhiColorAttachment color(msaaRenderBuffer);
color.setResolveTexture(resolvedTexture);
```

这种结构适合先渲染到多采样 render buffer，再自动解析到普通纹理，后续 shader 只需要采样普通 `sampler2D`。

### 多视图渲染

```cpp
QRhiColorAttachment color(textureArray);
color.setLayer(0);
color.setMultiViewCount(2);
```

多视图要求后端支持 `QRhi::MultiView`，并且附件通常是二维纹理数组。它不是“同时渲染到两个普通纹理”，而是渲染到数组层范围。

## 5. 使用场景

- 离屏渲染到纹理。
- G-buffer / MRT 多颜色附件输出。
- MSAA 自动 resolve。
- cubemap face、texture array layer、mip level 渲染。
- VR/XR 或多视图渲染目标。

## 6. 常见坑与经验

- **texture 和 render buffer 二选一。** 同一个 color attachment 不能同时设置两者。
- **resolve texture 必须匹配尺寸和语义。** 通常是非多采样二维纹理或纹理数组。
- **layer 和 level 要与纹理类型匹配。** 2D 普通纹理通常都为 0；数组/cubemap/mipmap 才需要改。
- **多视图不是普通数组渲染循环。** 一次 pass 的 view count 会影响 render target 和 pipeline 的设置。
- **render buffer 不能被采样。** 如果渲染结果要在 shader 中读取，使用 resolve texture 或直接渲染到 texture。
- **附件资源重建后 render target 可能也要更新。** `beginPass()` 对 texture render target 有一定自动检查，但显式管理更容易推理。

## 7. 知识点覆盖

- 颜色附件、render target 和 fragment shader 输出
- texture attachment 与 render buffer attachment 的取舍
- MSAA resolve 目标、mip level、array layer
- MRT、cubemap、纹理数组和 multiview
- RHI render target description 的组成方式
