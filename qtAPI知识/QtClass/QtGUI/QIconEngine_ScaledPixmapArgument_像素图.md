# QIconEngine::ScaledPixmapArgument：高 DPI 图标请求的输入输出包

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 声明位置：`#include <QIconEngine>`

## 它解决什么问题

`QIconEngine::ScaledPixmapArgument` 是 `QIconEngine::virtual_hook()` 在 `ScaledPixmapHook` 场景下使用的参数结构。它把一次高 DPI 图标请求的输入和输出放在同一对象中：

- 输入：逻辑尺寸、Mode、State、缩放因子；
- 输出：引擎选出的最佳 `QPixmap`。

它存在的原因是 Qt 需要在不新增虚函数、保持二进制兼容的前提下，向旧版 `QIconEngine` 扩展“按设备像素比取图”的能力。它不是面向普通 `QIcon` 使用者的公共配置对象。

## 什么时候会用到

只有在实现自定义 `QIconEngine`，并重写 `virtual_hook()` 支持 `QIconEngine::ScaledPixmapHook` 时，才通常直接操作该结构体。

典型场景：

- Freedesktop 图标主题针对 1x、2x、3x 目录提供不同资源；
- 自定义引擎希望为 1.25x、1.5x 等目标 DPR 返回最佳 pixmap；
- 图标资源是远程、程序化或专有格式，需要按缩放因子主动选择版本。

普通应用调用 `QIcon::pixmap(size, devicePixelRatio, mode, state)` 即可，Qt 会在内部走引擎路径。应用代码不应直接调用 `virtual_hook()` 来绕过 `QIcon` 的选择与缓存逻辑。

## 输入与输出方向

| 字段 | 方向 | 含义 |
| --- | --- | --- |
| `size` | 输入 | 请求的**设备无关**尺寸 |
| `mode` | 输入 | `QIcon::Normal`、`Disabled`、`Active` 或 `Selected` |
| `state` | 输入 | `QIcon::On` 或 `Off` |
| `scale` | 输入 | 请求缩放因子，通常等于目标绘制设备的 DPR |
| `pixmap` | 输出 | 引擎写回的最佳匹配图像 |

这里最容易混淆的是 `size` 与 `scale`：`size` 不是物理像素大小。对于 24x24 的逻辑图标和 `scale == 2.0`，引擎通常需要准备约 48x48 的像素内容，并为返回的 `QPixmap` 正确设置 DPR，使其在布局中仍表现为 24x24。

## 引擎中的正确用法

```cpp
void ThemeEngine::virtual_hook(int id, void *data)
{
    if (id == QIconEngine::ScaledPixmapHook) {
        auto *argument =
            static_cast<QIconEngine::ScaledPixmapArgument *>(data);

        QPixmap result = loadBestPixmap(
            argument->size, argument->scale,
            argument->mode, argument->state);

        if (!result.isNull())
            result.setDevicePixelRatio(argument->scale);

        argument->pixmap = result;
        return;
    }

    QIconEngine::virtual_hook(id, data);
}
```

`loadBestPixmap()` 应按逻辑尺寸和 scale 选择资源，而不是把 `size` 先乘 scale 后再把结果当作逻辑尺寸传给布局 API。返回的 `pixmap` 是输出参数；如果引擎无法满足请求，应保持空 pixmap 或使用其明确的回退策略。

## 与 `scaledPixmap()` 的关系

`QIconEngine::scaledPixmap()` 是面向引擎的显式虚函数，`ScaledPixmapArgument` 则是兼容 hook 使用的参数格式。两者表达的是同一类请求：按逻辑尺寸、Mode、State 和缩放因子取得 pixmap。

实现引擎时可按 Qt 版本和兼容需求选择支持方式，但应确保结果一致：

- 相同输入应得到同等语义的图标；
- 输出 pixmap 的 DPR 应与实际像素内容匹配；
- 不应为不同入口套用互相矛盾的 Mode/State 回退规则。

`scale` 常等于 DPR，但并非所有引擎都精确支持任意分数值。有些实现会转成整数，因此 125%、150% 等缩放环境需要单独测试。

## 与主题图标的关系

该结构体主要让 `QIcon::fromTheme()` 创建的主题图标利用 Freedesktop `index.theme` 中目录的 `Scale` 信息，选择适合当前 DPR 的资源。

通过文件、资源或普通 `addFile()` 建立的图标通常沿用 `QIcon::pixmap()` 的常规结果，并可继续使用 Qt 的 `@2x`、`@3x` 文件命名支持。不要把主题目录的 `Scale` 规则和应用私有文件的 `@nx` 规则混为同一套元数据格式。

## 初始化与生命周期

此结构体没有构造函数，作为调用方创建时应值初始化并明确填写所有输入字段：

```cpp
QIconEngine::ScaledPixmapArgument argument{};
argument.size = QSize(24, 24);
argument.mode = QIcon::Normal;
argument.state = QIcon::Off;
argument.scale = 2.0;
```

通常 Qt 在调用 `virtual_hook()` 时构造并管理它，引擎只在这次同步调用中读取和写入。不得保存 `ScaledPixmapArgument *`、其字段地址或 `data` 指针到回调返回之后。

`pixmap` 是值对象，赋值后可独立保留；但其背后是 GUI 类型，应遵守 `QPixmap` 的 GUI 线程与应用对象初始化边界。

## 常见错误

- 将 `size` 当成已乘 DPR 的物理像素尺寸。
- 返回了高分辨率像素内容，却未设置 `QPixmap::devicePixelRatio()`。
- 把 `scale` 一律四舍五入为整数，导致分数缩放模糊或尺寸错误。
- 未检查 `id` 就把任意 `void *` 转为 `ScaledPixmapArgument *`。
- 将该参数指针保存到异步加载回调中。
- 在 worker thread 中构造或操作返回的 `QPixmap`。
- 直接从业务代码调用 `virtual_hook()`，跳过 `QIcon` 的正常协作路径。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 结构体 | `QIconEngine::ScaledPixmapArgument` | 仅用于 `virtual_hook(ScaledPixmapHook, ...)` 的高 DPI 请求参数。 |
| 字段 | `QSize size` | 输入：请求的设备无关图标尺寸。 |
| 字段 | `QIcon::Mode mode` | 输入：请求的交互模式。 |
| 字段 | `QIcon::State state` | 输入：请求的开关状态。 |
| 字段 | `qreal scale` | 输入：请求缩放因子，通常是目标设备 DPR。 |
| 字段 | `QPixmap pixmap` | 输出：引擎写回的最佳匹配图像。 |
| 协作 hook | `QIconEngine::ScaledPixmapHook` | 指明 `virtual_hook()` 的 `data` 必须指向本结构体。 |
| 协作函数 | `QIconEngine::scaledPixmap(...)` | 表达相同类型的高 DPI 请求；实现应与 hook 行为保持一致。 |

## 相关类

- `QIconEngine`：接收并处理此参数结构。
- `QIcon`：普通应用获取高 DPI 图标的入口。
- `QPixmap`：结构体输出的 GUI 图像类型。

这不是一个独立的数据模型；它是一份短生命周期协议，核心规则是“输入以逻辑尺寸表达，输出以正确 DPR 的 pixmap 表达”。
