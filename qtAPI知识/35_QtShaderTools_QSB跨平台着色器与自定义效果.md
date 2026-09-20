# Qt Shader Tools：QSB 跨平台着色器与自定义效果

Qt 6 的渲染栈可能运行在 Vulkan、Metal、Direct3D 或 OpenGL 上。应用若只发布一份原始 GLSL，无法保证每个后端都能直接使用。Qt Shader Tools 通过 `qsb` 把 Vulkan 风格 GLSL 预编译成包含多个目标变体和反射信息的 `.qsb` 包，Qt Quick、Quick 3D 和 RHI 在运行时选择合适变体。

核心原则是：尽量在构建阶段烘焙着色器，只有用户动态提供源码等特殊场景才考虑运行时 `QShaderBaker`。

## 1. `.qsb` 中包含什么

```text
Vulkan 风格 GLSL 源码
          │ glslang
          ▼
        SPIR-V
          │ SPIRV-Cross / 平台编译器
          ├─ GLSL / GLSL ES
          ├─ HLSL / DXBC
          ├─ MSL / MetalLib
          └─ SPIR-V
               │
               ▼
         一个序列化的 .qsb 包
```

`.qsb` 还保存 uniform、采样器、顶点输入等反射信息。它不是单一 GPU 后端的二进制，也不是普通文本文件。

## 2. CMake 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick ShaderTools)

target_link_libraries(mytarget PRIVATE
    Qt6::Quick
    Qt6::ShaderTools
)

qt_add_shaders(mytarget "app_shaders"
    PREFIX "/shaders"
    FILES
        shaders/tint.vert
        shaders/tint.frag
)
```

构建时，CMake 会调用 `qsb`，把输出隐式加入资源系统。运行时路径为 `qrc:/shaders/shaders/tint.frag.qsb` 或对应的 `:/` 形式，具体还受 `BASE` 和文件相对路径影响。路径不确定时检查构建产物的资源映射，而不要猜测。

## 3. 最小 Qt Quick `ShaderEffect`

### 3.1 顶点着色器

```glsl
#version 440

layout(location = 0) in vec4 qt_Vertex;
layout(location = 1) in vec2 qt_MultiTexCoord0;

layout(location = 0) out vec2 texCoord;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
};

void main()
{
    texCoord = qt_MultiTexCoord0;
    gl_Position = qt_Matrix * qt_Vertex;
}
```

### 3.2 片元着色器

```glsl
#version 440

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    vec4 tintColor;
};

layout(binding = 1) uniform sampler2D source;

void main()
{
    fragColor = texture(source, texCoord) * tintColor * qt_Opacity;
}
```

### 3.3 QML 使用

```qml
ShaderEffect {
    width: 320
    height: 180

    property variant source: imageSource
    property color tintColor: "#80ffffff"

    vertexShader: "qrc:/shaders/shaders/tint.vert.qsb"
    fragmentShader: "qrc:/shaders/shaders/tint.frag.qsb"
}
```

QML 属性名需要和 uniform block 或 sampler 名匹配。类型也必须兼容，例如 QML `color` 对应 `vec4`，`real` 对应标量浮点值。新增属性后要重新构建 `.qsb`。

## 4. Vulkan 风格 GLSL 的约束

Qt 6 着色器通常使用 `#version 440` 等 Vulkan 风格 GLSL：

- 顶点输入和阶段输出显式声明 `layout(location = n)`。
- uniform 放入显式 `layout(std140, binding = 0)` 块。
- 纹理采样器使用独立且连续的 `binding`。
- 片元输出显式声明 location，而不是使用旧式 `gl_FragColor`。
- 不依赖 OpenGL 专有状态或隐式内建变量。

严格声明布局是跨 HLSL、MSL 和 GLSL 翻译的基础。

## 5. uniform 对齐与 `std140`

CPU 与 GPU 必须对同一 uniform block 得出相同偏移。`std140` 的常见规律：

- 标量通常按 4 字节对齐。
- `vec2` 按 8 字节对齐。
- `vec3` 和 `vec4` 通常按 16 字节对齐。
- 矩阵按列向量数组布局，常占多个 16 字节槽。
- 数组元素的步长通常至少为 16 字节。

在自定义 RHI 或场景图材质中，不要凭 C++ 结构体自然布局直接上传。使用反射信息、显式偏移或已验证的打包函数，并在多个编译器上加 `static_assert`。

## 6. `qt_add_shaders` 常用选项

### 6.1 Qt Quick 批处理顶点变体

用于 `ShaderEffect` 或 `QSGMaterialShader` 的顶点着色器通常需要批处理变体：

```cmake
qt_add_shaders(mytarget "quick_shaders"
    PREFIX "/shaders"
    BATCHABLE
    FILES shaders/item.vert shaders/item.frag
)
```

`BATCHABLE` 只影响顶点着色器，它允许 Qt Quick 把多个兼容节点合并批次。着色器若使用无法批处理的自定义语义，仍可能退回单独绘制。

### 6.2 指定目标语言版本

```cmake
qt_add_shaders(mytarget "compute_shaders"
    PREFIX "/shaders"
    GLSL "310 es,430"
    HLSL 50
    MSL 12
    FILES shaders/process.comp
)
```

计算着色器不能使用适合普通顶点/片元着色器的旧 GLSL 默认版本。目标版本应覆盖实际部署后端，同时避免把不需要的变体全部打包造成体积增长。

### 6.3 优化、预编译与宏

```cmake
qt_add_shaders(mytarget "production_shaders"
    PREFIX "/shaders"
    OPTIMIZED
    PRECOMPILE
    DEFINES "USE_FOG=1;MAX_LIGHTS=4"
    FILES shaders/scene.frag
)
```

`OPTIMIZED` 可能依赖外部 SPIR-V 优化工具；`PRECOMPILE` 在支持的平台调用原生编译器。CI 应使用和发布构建一致的 SDK，否则本地成功、发布机失败。

## 7. 直接使用 `qsb`

```text
qsb --glsl "100 es,120,150" --hlsl 50 --msl 12 \
    shader.frag -o shader.frag.qsb
```

查看包内容：

```text
qsb -d shader.frag.qsb
```

调试时重点检查各目标变体、资源绑定、uniform 偏移和阶段输入输出。项目构建仍应由 CMake 调用工具，手动命令只适合定位问题。

## 8. 着色器接口匹配

顶点着色器的输出 location 必须与片元着色器输入匹配：

```glsl
// vertex
layout(location = 0) out vec2 uv;
layout(location = 1) out vec3 normal;

// fragment
layout(location = 0) in vec2 uv;
layout(location = 1) in vec3 normal;
```

名称可以不同，但 location 和类型必须兼容。跨阶段接口不一致通常在 `qsb` 或管线创建时报错，而不是自动转换。

## 9. 多重采样、多视图和变体

XR 或立体渲染可能需要多视图变体：

```cmake
qt_add_shaders(mytarget "xr_shaders"
    MULTIVIEW
    FILES shaders/xr.vert shaders/xr.frag
)
```

`VIEW_COUNT` 会改变顶点着色器生成规则，不应对普通单视图着色器无条件启用。变体数量越多，构建时间和资源体积越大；按实际管线功能划分着色器包。

## 10. Qt Quick 3D 自定义材质

Quick 3D 的 `CustomMaterial` 使用框架约定的入口、内建变量和材质属性。概念示例：

```qml
CustomMaterial {
    property color edgeColor: "#00bcd4"
    property real edgeWidth: 0.2

    vertexShader: "shaders/outline.vert"
    fragmentShader: "shaders/outline.frag"
}
```

Quick 3D 自定义材质源码与普通 `ShaderEffect` 的完整 GLSL 接口不同，框架会注入场景、光照和材质相关代码。应按 `CustomMaterial` 文档使用其宏和入口，不能直接把 Qt Quick 2D 着色器复制过去。

## 11. 运行时 `QShaderBaker`

特殊场景可以在运行时烘焙：

```cpp
#include <rhi/qshaderbaker.h>

QShaderBaker baker;
baker.setSourceFileName("user.frag", QShader::FragmentStage);
baker.setGeneratedShaderVariants({QShader::StandardShader});

const QShader shader = baker.bake();
if (!shader.isValid())
    qWarning() << baker.errorMessage();
```

这需要链接私有目标 `Qt6::ShaderToolsPrivate`，而且 `QShaderBaker`、`QShader` 和 QRhi 系列没有常规 Qt 公共 API 的源码/二进制兼容保证。除非运行时源码不可避免，否则不要把它放入稳定产品接口。

## 12. 安全边界

用户提供的着色器不是普通文本配置。编译可能消耗大量 CPU/内存，驱动编译器也可能存在缺陷。处理不可信源码时：

- 限制源码大小、include 深度和宏数量。
- 在隔离进程中编译并设置超时。
- 只允许预定义资源绑定和阶段。
- 缓存结果前校验来源和目标 Qt 版本。
- 编译失败只返回必要诊断，避免泄露本地路径。

## 13. 常见错误

### `ShaderEffect` 完全透明

检查片元输出是否乘了 `qt_Opacity`、采样器属性是否有效、资源路径是否指向 `.qsb`，以及 uniform 名是否与 QML 属性一致。

### OpenGL 正常但 D3D/Metal 失败

通常是隐式类型转换、未初始化变量、接口 location、uniform 对齐或超出目标着色语言能力。以最严格后端为基准修复源码，而不是只保留 OpenGL 变体。

### 修改源码但效果不变

确认 CMake 追踪了 shader 文件、`.qsb` 重新生成、运行的是新可执行文件，并清理了错误的外部资源副本。使用 `qsb -d` 对比构建时间和内容。

## 14. 测试与发布

1. CI 在所有目标平台运行 `qt_add_shaders`，把编译警告视为错误。
2. 对关键效果做离屏截图和像素容差比较。
3. 在 Direct3D、Metal、Vulkan、OpenGL/ES 实机验证。
4. 测试不同 DPR、颜色空间、MSAA 和纹理格式。
5. 发布包只携带需要的 `.qsb` 资源，不依赖开发机上的原始 shader 路径。

## 15. 速查表

| 目标 | 工具/API |
| --- | --- |
| 构建阶段烘焙 | `qt_add_shaders()` |
| 手动烘焙 | `qsb` |
| 检查着色器包 | `qsb -d` |
| Qt Quick 2D 效果 | `ShaderEffect` |
| Quick 3D 材质 | `CustomMaterial` |
| 运行时烘焙 | `QShaderBaker`（私有兼容等级） |

正确使用 Shader Tools 的关键不是写出某个后端能运行的 GLSL，而是把资源布局、变体生成和后端能力在构建期固定下来，让同一个效果可预测地跨平台运行。
