# QQuick3DTextureData
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3DTextureData`

## 1. 先建立直觉

`QQuick3DTextureData` 让 C++ 直接提供纹理原始数据给 Quick 3D。它不负责从图片文件解码，而是描述“这块字节是什么尺寸、什么格式、有没有透明、深度多少”。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3DTextureData`，属于 Qt Quick 3D 模块，用于向 Quick 3D 提供自定义纹理数据。

它适合程序生成纹理、外部解码器输出、压缩纹理数据接入等场景。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `setTextureData()` / `textureData()` | 设置或读取纹理字节。 |
| `setSize()` / `size()` | 设置宽高。 |
| `setDepth()` / `depth()` | 设置 3D/数组类纹理深度。 |
| `setFormat()` / `format()` | 设置数据格式，如 RGBA8、RGBA16F、BC/ETC/ASTC。 |
| `setHasTransparency()` / `hasTransparency()` | 声明是否含透明信息，影响渲染路径。 |
| `Format` | 未压缩、HDR、单通道、块压缩格式枚举。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 程序生成贴图 | 噪声、热力图、动态 UI 贴图。 |
| 接入外部图像解码 | 解码后直接喂给 Quick 3D。 |
| 压缩纹理资源 | 使用 BC/ETC/ASTC 等 GPU 压缩格式。 |

## 5. 常见坑与经验

格式、尺寸和字节长度必须匹配。压缩格式尤其要按块大小计算数据长度，否则不同图形后端表现会不一致。

`hasTransparency` 是渲染提示，不会扫描你的像素。设置错会造成透明排序不正确或走错渲染路径。

纹理数据变化后要走 Quick 3D 的同步路径，不要在渲染线程外直接改底层 GPU 资源。

## 6. 知识点覆盖

- 自定义纹理数据输入。
- 像素格式、压缩格式、尺寸和透明性。
- 动态纹理和渲染同步边界。
