# Qt QSurfaceFormat：图形 surface 与 OpenGL context 的请求格式

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSurfaceFormat>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 类型定位：描述绘制表面和 OpenGL context 属性的值类型

## 1. 它解决什么问题

`QSurfaceFormat` 用一个值对象表达图形 surface 或 OpenGL context 的格式请求，包括：

- 深度、模板和 RGBA 颜色缓冲位数；
- 多重采样数量；
- OpenGL 版本和 profile；
- 可渲染 API 类型；
- swap behavior 和 swap interval；
- stereo、debug、deprecated functions、reset notification、protected content 等选项；
- Qt 6 起的 `QColorSpace`。

它常用于 `QWindow::setFormat()`、`QOpenGLContext::setFormat()`、`QOffscreenSurface::setFormat()` 和全局默认格式。

它不是实际 GPU framebuffer，也不是 context 创建成功的结果。`QSurfaceFormat` 只是请求/描述；平台可能降级、忽略不支持的字段或给出与请求不同的实际格式。

## 2. 构建与典型流程

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

请求格式：

```cpp
QSurfaceFormat requested;
requested.setRenderableType(QSurfaceFormat::OpenGL);
requested.setVersion(4, 5);
requested.setProfile(QSurfaceFormat::CoreProfile);
requested.setDepthBufferSize(24);
requested.setStencilBufferSize(8);
requested.setSamples(4);
requested.setOption(QSurfaceFormat::DebugContext);

window.setFormat(requested);
window.create();
```

创建 context 后应读取实际格式：

```cpp
QOpenGLContext context;
context.setFormat(requested);
if (!context.create())
    return;

const QSurfaceFormat actual = context.format();
qDebug() << actual.majorVersion()
         << actual.minorVersion()
         << actual.samples();
```

## 3. 请求格式和实际格式

Qt 会尽量满足请求，但最终结果受以下因素影响：

- 操作系统窗口系统；
- 图形驱动；
- 可用 OpenGL/OpenGL ES 版本；
- surface 类型；
- context sharing；
- multisample、stereo、protected content 等扩展能力。

因此：

- `setVersion()` 不是强制创建某版本的保证；
- `setSamples(4)` 不保证一定得到 4x MSAA；
- `setOption(DebugContext)` 不保证 debug context 一定建立；
- `setColorSpace()` 不保证后端具备完整色彩管理；
- 创建后要从 context/surface 读取实际格式并按能力分支。

## 4. 枚举和 flags

### 4.1 `FormatOption` / `FormatOptions`

```cpp
enum FormatOption {
    StereoBuffers = 0x0001,
    DebugContext = 0x0002,
    DeprecatedFunctions = 0x0004,
    ResetNotification = 0x0008,
    ProtectedContent = 0x0010
};
```

- `StereoBuffers`：请求立体缓冲；
- `DebugContext`：请求 OpenGL debug context；
- `DeprecatedFunctions`：允许使用 deprecated OpenGL functions；
- `ResetNotification`：请求 context reset notification；
- `ProtectedContent`：请求受保护内容能力。

这是 flags 类型：

```cpp
format.setOption(QSurfaceFormat::DebugContext);
format.setOption(QSurfaceFormat::DeprecatedFunctions, false);
```

`setOptions()` 会整体替换 flags，`setOption()` 只修改一个位。选项不适用于所有 renderable type，最终是否支持要看实际格式和 context。

### 4.2 `RenderableType`

| 值 | 含义 |
| --- | --- |
| `DefaultRenderableType` | 由平台/Qt 选择 |
| `OpenGL` | 桌面 OpenGL 请求 |
| `OpenGLES` | OpenGL ES 请求 |
| `OpenVG` | OpenVG 请求 |

`RenderableType` 不是 `QSurface::SurfaceType` 的直接替代。它表示格式请求面向哪个渲染 API；surface 的实际类别还由 surface 对象表示。

### 4.3 `OpenGLContextProfile`

| 值 | 含义 |
| --- | --- |
| `NoProfile` | 不指定 profile |
| `CoreProfile` | 请求 core profile |
| `CompatibilityProfile` | 请求 compatibility profile |

profile 主要对桌面 OpenGL 3.2+ 有意义。对 OpenGL ES 不要把桌面 profile 逻辑直接套用。

### 4.4 `SwapBehavior`

| 值 | 含义 |
| --- | --- |
| `DefaultSwapBehavior` | 平台默认 |
| `SingleBuffer` | 单缓冲请求 |
| `DoubleBuffer` | 双缓冲请求 |
| `TripleBuffer` | 三缓冲请求 |

它是请求，不是所有平台都会实现。窗口系统和合成器可能决定最终交换方式。

### 4.5 旧的 `ColorSpace`

Qt 6 中保留了旧的：

```cpp
enum ColorSpace {
    DefaultColorSpace,
    sRGBColorSpace
};
```

这个 enum overload 属于弃用迁移路径。新代码使用 `QColorSpace`：

```cpp
format.setColorSpace(QColorSpace::SRgb);
```

## 5. 缓冲、采样和 alpha

### `setDepthBufferSize()` / `depthBufferSize()`

请求 depth buffer 位数。`0` 通常表示不提出特定深度位数偏好，而不是强制“没有 depth buffer”；实际结果要在创建后确认。

### `setStencilBufferSize()` / `stencilBufferSize()`

请求 stencil buffer 位数。深度和模板缓冲可能由平台以组合格式提供，实际结果不能只按请求值推断。

### RGBA buffer size

`setRedBufferSize()`、`setGreenBufferSize()`、`setBlueBufferSize()`、`setAlphaBufferSize()` 设置各颜色通道位数；对应 getter 读取格式对象中的值。

`hasAlpha()` 用于快速判断是否请求/描述了 alpha 通道。它不等价于窗口一定支持透明合成，也不等价于内容最终会以透明方式显示。

### `setSamples()` / `samples()`

请求 multisample 数量。`0` 通常表示不请求多重采样；正数表示期望的 sample count。平台可能选择其他支持值，创建后应读取实际 `samples()`。

## 6. OpenGL 版本、profile 和渲染类型

### `setMajorVersion()` / `setMinorVersion()` / `setVersion()`

设置 OpenGL 版本请求。`version()` 返回 `std::pair<int, int>`；`majorVersion()` 和 `minorVersion()` 提供单独查询。

```cpp
format.setVersion(3, 3);
const auto [major, minor] = format.version();
```

版本字段只在相关 renderable type 上有明确意义。它不会验证驱动支持，也不会自动回退。

### `setProfile()` / `profile()`

设置/读取 OpenGL context profile。使用 core profile 时，旧版固定管线函数和兼容性对象不可用；应用应让 shader、VAO 和 pipeline 代码与 profile 一致。

### `setRenderableType()` / `renderableType()`

设置/读取 OpenGL、OpenGL ES、OpenVG 或 default 请求。不要把它当成运行时已选择的后端证明，实际 context 创建后仍要检查。

## 7. swap interval 和默认格式

### `swapInterval()` / `setSwapInterval(int)`

设置/读取交换间隔请求，通常用于垂直同步节奏：

- `0` 常用于请求不等待垂直同步；
- `1` 常用于每次刷新等待一次；
- 更大值可表示更低频率；
- 具体支持和实际行为取决于平台。

它不是渲染帧率上限的绝对保证，也不适用于所有非 OpenGL 后端。

### `defaultFormat()` / `setDefaultFormat()`

全局默认格式：

```cpp
QSurfaceFormat format;
format.setDepthBufferSize(24);
QSurfaceFormat::setDefaultFormat(format);
```

应在创建依赖默认格式的 window/context 之前设置。它不会 retroactively 修改已经创建的对象，也不应在多线程中随意动态切换。

全局默认格式会影响同一进程中后续使用默认值的图形对象，因此库代码不应无条件覆盖宿主应用的全局默认值。

## 8. 颜色空间

Qt 6 起使用 `QColorSpace`：

```cpp
format.setColorSpace(QColorSpace::SRgb);
const QColorSpace cs = format.colorSpace();
```

颜色空间描述内容的编码/显示色彩语义，但是否由窗口系统、OpenGL surface、交换链或后端实际执行色彩转换，取决于平台能力。不能只设置 `QColorSpace` 就假设所有显示输出自动完成正确转换。

## 9. 值语义和生命周期

`QSurfaceFormat` 是可复制的值类型，不拥有窗口、context 或 GPU buffer。复制和赋值只复制请求/描述字段。

修改一个格式对象不会修改已经使用它创建的 window/context。要改变已经创建的图形对象，通常需要按平台和 API 重新创建对象。

## 10. 常见误区与排查顺序

### 10.1 把请求格式当作实际格式

创建 context/surface 后读取实际 format，并根据结果检查版本、samples、alpha、depth/stencil 和 options。

### 10.2 用 `setDefaultFormat()` 影响已有对象

全局默认只影响之后使用默认格式的对象；已有对象不会自动重建。

### 10.3 把 0 位数理解成强制禁用

对很多 buffer size 字段，0 更接近“无偏好”。如果业务要求无 depth 或固定 alpha，需要在实际创建后验证。

### 10.4 把 samples 请求当成 MSAA 保证

平台可能降级、拒绝或选择其他 sample count。实际绘制还要让 render target 和 pipeline 与样本数匹配。

### 10.5 混用 OpenGL profile 和 OpenGL ES

桌面 core/compatibility profile 不能直接套在 OpenGL ES 上。先确认 renderable type。

### 10.6 频繁修改全局默认格式

它是进程级配置，可能影响其他模块。应用应在图形对象创建前集中设置一次。

### 10.7 把 swap interval 当成准确 FPS

它是交换同步请求，实际刷新、合成器和驱动可能改变最终节奏。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 枚举 | `FormatOption` | 定义 debug、stereo 等选项 | 是 flags 位，支持组合 |
| 枚举 | `SwapBehavior` | 定义交换缓冲策略 | 平台可能不满足请求 |
| 枚举 | `RenderableType` | 指定渲染 API 类型 | 不等于实际 context 成功 |
| 枚举 | `OpenGLContextProfile` | 指定桌面 OpenGL profile | 对 OpenGL ES 不直接适用 |
| 枚举 | `ColorSpace` | 旧颜色空间 enum | 弃用；新代码用 `QColorSpace` |
| 构造 | `QSurfaceFormat()` | 创建默认格式对象 | 未指定字段交给平台选择 |
| 构造 | `QSurfaceFormat(FormatOptions)` | 创建带 flags 的格式 | 不验证平台能力 |
| 构造 | `QSurfaceFormat(const QSurfaceFormat &)` | 复制格式对象 | 只复制值，不复制图形资源 |
| 赋值 | `operator=(const QSurfaceFormat &)` | 复制格式 | 不影响已创建 surface/context |
| 析构 | `~QSurfaceFormat()` | 销毁值对象 | 不释放 GPU 资源 |
| 深度 | `setDepthBufferSize()` / `depthBufferSize()` | 设置/读取 depth 位数 | 0 通常是无偏好 |
| 模板 | `setStencilBufferSize()` / `stencilBufferSize()` | 设置/读取 stencil 位数 | 实际值需创建后确认 |
| 颜色 | `setRedBufferSize()` / `redBufferSize()` | 设置/读取 R 位数 | 是请求/描述字段 |
| 颜色 | `setGreenBufferSize()` / `greenBufferSize()` | 设置/读取 G 位数 | 是请求/描述字段 |
| 颜色 | `setBlueBufferSize()` / `blueBufferSize()` | 设置/读取 B 位数 | 是请求/描述字段 |
| 颜色 | `setAlphaBufferSize()` / `alphaBufferSize()` | 设置/读取 A 位数 | 不等于窗口透明合成 |
| 颜色 | `hasAlpha()` | 判断是否有 alpha 请求/描述 | 不是透明窗口保证 |
| 采样 | `setSamples()` / `samples()` | 设置/读取 MSAA sample count | 可能被平台降级 |
| 版本 | `setMajorVersion()` / `majorVersion()` | 设置/读取主版本 | 不验证驱动 |
| 版本 | `setMinorVersion()` / `minorVersion()` | 设置/读取次版本 | 不自动回退 |
| 版本 | `setVersion()` / `version()` | 成对设置/读取版本 | 返回 pair |
| profile | `setProfile()` / `profile()` | 设置/读取 OpenGL profile | 主要用于桌面 OpenGL |
| API | `setRenderableType()` / `renderableType()` | 设置/读取 OpenGL/ES/OpenVG | 仍需检查实际结果 |
| option | `setOptions()` / `options()` | 整体替换 flags | 会清除未包含的位 |
| option | `setOption()` / `testOption()` | 设置/查询单个位 | 选项可能不被平台支持 |
| stereo | `setStereo()` / `stereo()` | 设置/读取立体缓冲 | 是 `StereoBuffers` 便捷接口 |
| 交换 | `setSwapBehavior()` / `swapBehavior()` | 设置/读取交换策略 | 平台可能忽略 |
| 交换 | `setSwapInterval()` / `swapInterval()` | 设置/读取同步间隔 | 不是准确 FPS 限制 |
| 颜色空间 | `setColorSpace(const QColorSpace &)` / `colorSpace()` | 设置/读取 Qt 颜色空间 | 后端是否实际转换需验证 |
| 兼容 | `setColorSpace(ColorSpace)` | 设置旧颜色空间 | 弃用 |
| 全局 | `setDefaultFormat()` / `defaultFormat()` | 设置/读取进程默认格式 | 必须在创建对象前设置 |
| 比较 | `operator==` / `operator!=` | 比较格式值 | 不表示实际资源相同 |

---

### 一句话总结

`QSurfaceFormat` 是图形 surface/context 的格式请求值：先设置，再创建 window/context，最后读取实际格式验证；buffer 位数、samples、profile、options、swap interval 和颜色空间都可能被平台调整，`setDefaultFormat()` 还是进程级配置，必须在创建相关对象前谨慎设置。
