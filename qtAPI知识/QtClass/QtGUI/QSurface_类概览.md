# Qt QSurface：窗口与离屏表面的抽象契约

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSurface>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 类型定位：为 `QWindow`、`QOffscreenSurface` 等提供的抽象 surface 接口

## 1. 它解决什么问题

图形上下文需要一个“绘制目标表面”，但表面可能是：

- 有平台窗口的可见 surface；
- 没有屏幕显示的离屏 surface；
- Raster、OpenGL、Vulkan、Metal 或 Direct3D 类型的表面。

`QSurface` 用统一接口描述这些对象的类别、格式、大小和平台 surface handle，让 `QOpenGLContext`、图形后端和窗口系统可以协作。

它不是一个可直接显示的窗口，也不是 GPU framebuffer。应用通常使用 `QWindow` 或 `QOffscreenSurface`，而不是直接派生 `QSurface`。

## 2. 抽象性和派生类型

`QSurface` 的构造函数是 protected，`format()`、`surfaceHandle()`、`surfaceType()` 和 `size()` 是 pure virtual：

```text
QSurface
  -> QWindow
  -> QOffscreenSurface
```

不能直接：

```cpp
QSurface surface; // 错误：抽象类
```

## 3. 成员类型

### 3.1 `SurfaceClass`

| 枚举值 | 含义 |
| --- | --- |
| `Window` | 有窗口语义的 surface |
| `Offscreen` | 离屏 surface |

它描述 surface 的类别，不描述具体图形 API。

### 3.2 `SurfaceType`

| 枚举值 | 含义 |
| --- | --- |
| `RasterSurface` | Qt raster 绘制表面 |
| `OpenGLSurface` | OpenGL/OpenGL ES 表面 |
| `RasterGLSurface` | 旧的 raster-GL 混合类型，Qt 6.11 起处于弃用迁移路径 |
| `OpenVGSurface` | OpenVG 表面 |
| `VulkanSurface` | Vulkan 表面 |
| `MetalSurface` | Metal 表面 |
| `Direct3DSurface` | Direct3D 表面 |

`SurfaceType` 是图形 API/绘制路径类型，不是 `SurfaceClass` 的替代品。一个 window surface 也可能是 OpenGL 或 Vulkan 类型。

## 4. 纯虚接口

### `QSurfaceFormat format() const`

返回 surface 使用或请求的格式。具体是 requested format 还是实际获得格式，取决于派生类和平台生命周期。对于 OpenGL，实际 context format 还可能受平台降级、共享 context 和驱动能力影响。

### `QPlatformSurface *surfaceHandle() const`

返回 QPA 平台表面句柄。`QPlatformSurface` 是 Qt 平台抽象的内部类型，普通应用不应依赖其具体实现或强转为平台私有对象。

句柄可能在 surface 尚未创建、即将销毁或离屏对象没有对应平台资源时不可用。不要把它当作稳定的 native window handle。

### `SurfaceType surfaceType() const`

返回绘制表面类型。调用它只能识别 Qt 表示的 surface 类别，不会证明相应图形上下文已经创建成功。

### `QSize size() const`

返回 surface 尺寸。窗口尺寸通常是逻辑像素，具体与窗口系统、DPR 和派生类语义有关；创建 framebuffer 或 swapchain 时应结合实际像素尺寸和后端 API。

## 5. 其他成员函数

### `SurfaceClass surfaceClass() const`

返回构造时记录的 surface 类别。它是 `Window` 或 `Offscreen`，不会随着窗口是否当前可见而动态变成另一类。

### `bool supportsOpenGL() const`

查询 surface 是否适合 OpenGL 使用。它是能力提示，不等价于：

- 当前机器一定有可用 OpenGL 驱动；
- 一个 `QOpenGLContext` 一定能成功创建；
- surface 已经创建了 native handle；
- requested `QSurfaceFormat` 一定会被满足。

## 6. 构造和析构

### `protected QSurface(SurfaceClass type)`

供派生类记录 surface 类别。自定义派生类必须同时实现所有 pure virtual 接口，并正确维护平台资源生命周期。

### `virtual ~QSurface()`

虚析构保证通过 `QSurface *` 删除派生对象时行为正确。析构本身不替派生类管理外部 native surface，资源释放由具体派生类负责。

## 7. 实际使用场景

### 7.1 OpenGL context 与 window surface

```cpp
QWindow window;
window.setSurfaceType(QSurface::OpenGLSurface);
window.create();

QOpenGLContext context;
context.setFormat(window.requestedFormat());
if (context.create())
    context.makeCurrent(&window);
```

实际代码还要检查 format、线程、窗口可见性和 context 创建结果。`QSurface` 只提供协作接口，不负责 `makeCurrent()`。

### 7.2 离屏资源准备

`QOffscreenSurface` 作为 `QSurface::Offscreen` 使用，适合在没有可见窗口时创建 OpenGL context 进行纹理或资源准备。它仍受 GUI 线程、context 线程归属和平台 surface 支持限制。

### 7.3 统一处理 window/offscreen

需要接收 `QSurface *` 的基础设施代码可以先检查：

```cpp
if (surface->surfaceClass() == QSurface::Offscreen) {
    // 不要假设存在可见窗口
}
```

再根据 `surfaceType()` 和 `format()` 选择图形后端逻辑。

## 8. 与 `QSurfaceFormat` 的关系

`QSurface::format()` 返回 format 描述，`QSurfaceFormat` 负责请求和表达颜色位数、深度/模板、samples、swap behavior、OpenGL profile 等。

请求格式和实际格式可能不同。平台通常会尽量满足请求，但应用应在 context/surface 创建后读取实际结果，而不是只保存创建前的 request。

## 9. 平台句柄和生命周期

`surfaceHandle()` 对应的是 QPA 层平台对象，其有效时间与 surface 的 native 资源生命周期相关。窗口从未 `create()`、正在销毁或平台插件尚未完成初始化时，句柄语义可能不同。

不要跨线程缓存平台句柄，不要在 `QWindow`/`QOffscreenSurface` 销毁后继续使用。

## 10. 常见误区

- 尝试直接实例化 `QSurface`。
- 把 `SurfaceClass::Window` 当成 `SurfaceType::OpenGLSurface`。
- 把 `supportsOpenGL()` 当成 OpenGL context 创建成功保证。
- 把 `surfaceHandle()` 当成稳定的 HWND、NSView 或 X11 Window。
- 忽略逻辑尺寸、物理像素和 DPR 的差异。
- 认为 requested format 等于最终 format。
- 在 surface native 资源创建前获取句柄并长期缓存。
- 把弃用的 `RasterGLSurface` 当成新项目首选。

## API 速查表
| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 枚举 | `SurfaceClass::Window` | 标识窗口 surface | 不代表图形 API 类型 |
| 枚举 | `SurfaceClass::Offscreen` | 标识离屏 surface | 不代表没有平台资源 |
| 枚举 | `SurfaceType::RasterSurface` | raster 表面 | 不等于 OpenGL |
| 枚举 | `SurfaceType::OpenGLSurface` | OpenGL 表面 | 不保证 context 创建成功 |
| 枚举 | `SurfaceType::RasterGLSurface` | 旧 raster-GL 类型 | Qt 6.11 起处于弃用路径 |
| 枚举 | `SurfaceType::OpenVGSurface` | OpenVG 表面 | 受平台支持限制 |
| 枚举 | `SurfaceType::VulkanSurface` | Vulkan 表面 | 需结合 Vulkan 后端 |
| 枚举 | `SurfaceType::MetalSurface` | Metal 表面 | 仅相关平台有意义 |
| 枚举 | `SurfaceType::Direct3DSurface` | Direct3D 表面 | 仅相关平台有意义 |
| 构造 | `protected QSurface(SurfaceClass)` | 初始化派生 surface 类别 | 普通应用不能直接调用 |
| 析构 | `virtual ~QSurface()` | 虚析构 | 派生类负责平台资源 |
| 查询 | `surfaceClass() const` | 查询 Window/Offscreen | 不随可见性动态改变 |
| 查询 | `format() const` | 获取 surface 格式 | requested/actual 语义由派生类决定 |
| 查询 | `surfaceHandle() const` | 获取 QPA 平台句柄 | 私有层，生命周期敏感 |
| 查询 | `surfaceType() const` | 获取绘制 API 类型 | 不证明上下文可用 |
| 查询 | `supportsOpenGL() const` | 查询 OpenGL 适用性 | 不是 context 创建保证 |
| 查询 | `size() const` | 获取 surface 尺寸 | 需考虑逻辑像素与 DPR |

---

### 一句话总结

`QSurface` 是窗口和离屏绘制表面的抽象契约：普通应用使用 `QWindow`/`QOffscreenSurface`，通过 `surfaceClass()`、`surfaceType()`、`format()` 和 `size()` 协作；`surfaceHandle()` 属于 QPA 平台层，`supportsOpenGL()` 也只是能力提示，不能替代实际 context 和资源创建检查。
