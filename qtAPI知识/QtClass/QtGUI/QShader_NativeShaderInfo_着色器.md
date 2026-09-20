# Qt QShader::NativeShaderInfo：后端附加 shader 信息

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshader.h>`  
> 所属模块：`Qt6::Gui` / RHI  
> 归属类型：`QShader::NativeShaderInfo`  
> 继承：无  
> 类型定位：按 shader key 保存的后端附加值类型

## 1. 它解决什么问题

`QShader::NativeShaderInfo` 是 `QShader` 内部按 `QShaderKey` 保存的一小组后端附加信息。它不保存 shader 源码，也不保存完整反射描述，而是为某个语言、版本和变体的 shader 提供：

- `flags`：后端或生成器约定的附加标志；
- `extraBufferBindings`：额外 buffer 绑定映射。

它解决的是“同一个 shader package 的某个后端代码还需要少量原生补充信息”的问题。应用通常通过 `QShader::nativeShaderInfo(key)` 读取，通过 `QShader::setNativeShaderInfo(key, info)` 写入；很少需要单独构造它来替代 `QShaderBaker` 的生成结果。

这个结构体不是 GPU shader module，不会编译代码、创建 pipeline、申请 GPU 内存，也不会自动修改 `QShaderDescription`。字段的具体数值由 Qt 的 RHI 生成器和后端约定，Qt 6.11.1 文档没有为 `flags` 公开一组可供普通应用组合的常量。

## 2. 构建与包含

`NativeShaderInfo` 定义在 `QShader` 的 RHI 头文件中：

```cpp
#include <rhi/qshader.h>
```

Qt 文档对 `QShader`、`QShaderDescription` 和其他 QRhi 类型给出的兼容性警告同样适用于本结构体：

- RHI API 没有源代码兼容性保证；
- RHI API 没有二进制兼容性保证；
- CMake 通常需要链接 `Qt::GuiPrivate`；
- 不应把它暴露为跨 Qt 小版本的公共 ABI。

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::GuiPrivate)
```

## 3. 最小使用方式

### 3.1 通过 `QShader` 按 key 查询

```cpp
#include <rhi/qshader.h>

QShader::NativeShaderInfo infoFor(const QShader &shader,
                                  const QShaderKey &key)
{
    return shader.nativeShaderInfo(key);
}
```

如果该 key 没有附加信息，或者该语言、阶段和后端不需要这类信息，返回的是默认构造的空对象：

```cpp
QShader::NativeShaderInfo info = shader.nativeShaderInfo(key);
if (info.flags == 0 && info.extraBufferBindings.isEmpty()) {
    // 可能确实没有附加信息。
}
```

不要把“字段全为默认值”当作跨版本的正式有效性判定；具体是否需要附加信息应由生成器和后端使用约定决定。

### 3.2 写入并挂到指定 key

```cpp
QShader::NativeShaderInfo info;
info.flags = backendFlags;
info.extraBufferBindings.insert(genericBinding, nativeBinding);

shader.setNativeShaderInfo(key, info);
```

`setNativeShaderInfo()` 会把值与精确的 `QShaderKey` 关联。换一个 source、version 或 variant 就是另一条记录，不能依靠“看起来是同一个 shader”自动复用。

## 4. 核心使用模型

### 4.1 这是附加元数据，不是 shader 代码

`NativeShaderInfo` 不包含：

- GLSL、HLSL、SPIR-V 等源代码；
- 入口点名称；
- pipeline stage；
- uniform block 完整描述；
- texture 和 sampler 的完整资源布局。

这些信息分别由 `QShaderCode`、`QShader::stage()`、`QShaderDescription` 和其他按 key 的映射提供。不要把 `NativeShaderInfo` 当成一个可以独立提交给 `QRhiGraphicsPipeline` 的对象。

### 4.2 信息按 `QShaderKey` 隔离

`QShaderKey` 包含 source、source version 和 source variant。`NativeShaderInfo` 是附着在这组三元组上的，不是整个 `QShader` 的单一全局配置：

```text
QShaderKey(GLSL, 450, StandardShader)
    -> NativeShaderInfo A

QShaderKey(MSL, 20, StandardShader)
    -> NativeShaderInfo B
```

查询时必须传入与目标代码完全一致的 key。使用邻近版本的 info 可能导致 binding 或后端标志与实际代码不匹配。

### 4.3 `flags` 没有公开通用解释

头文件只声明：

```cpp
int flags = 0;
```

没有为普通应用公开 `Flag` 枚举或常量。不要猜测某个 bit 的意义，也不要把它当成 `QFlags` 使用。若生成工具输出了非零值，应原样保存和传递给使用它的 Qt RHI 代码。

### 4.4 `extraBufferBindings` 是整数映射

头文件声明：

```cpp
QMap<int, int> extraBufferBindings;
```

它表达某种额外 buffer 绑定关系，但“键”和“值”具体代表哪一侧的 binding、是否与特定 shader 语言或后端相关，取决于生成器和 RHI 后端约定。结构体页面没有为普通应用定义一套独立的编号协议。

因此，应用应优先把它当作生成的 opaque metadata 保存和传递，而不是自行重新编号：

```cpp
for (auto it = info.extraBufferBindings.cbegin();
     it != info.extraBufferBindings.cend(); ++it) {
    // 只有在明确掌握目标后端约定时才解释 it.key() 和 it.value()。
}
```

## 5. 实际使用场景

### 5.1 保存 `qsb` 生成的后端附加数据

最常见的场景是 `qsb` 或其他 shader 工具生成 `QShader` package 时写入该信息，应用通过序列化和反序列化保留它。普通应用通常不需要手工生成字段。

### 5.2 QRhi 后端创建管线

QRhi 在选择具体 shader key 后，可能读取该 key 对应的原生附加信息，用于处理特定后端的 buffer 绑定或代码特性。应用只需要把完整 `QShader` package 传给 RHI，不应在每个后端重复实现同一套解析逻辑。

### 5.3 shader 工具和诊断工具

材质编辑器、shader package 检查器或构建诊断工具可以读取 `flags` 和 `extraBufferBindings`，但显示时应注明“后端相关元数据”，不要把整数直接展示成跨平台通用语义。

### 5.4 自定义生成流水线

如果应用确实有自己的 shader 生成器，可以在掌握目标 Qt 版本和后端实现约定的前提下设置这些字段。生成器和运行时必须锁定同一 Qt/RHI 版本，并为每个目标 key 做一致性测试。

## 6. 生命周期、所有权和线程

### 6.1 普通值类型

`NativeShaderInfo` 是一个无 QObject、无父对象的结构体。它只包含一个整数和一个 `QMap<int, int>`，可以按值复制、返回和放入 Qt 容器。它不拥有 GPU 资源，也不拥有外部内存。

### 6.2 与 `QShader` 的隐式共享边界

结构体本身按值保存；当它通过 `QShader::nativeShaderInfo()` 返回时，调用方得到的是自己的值对象。把它修改后不会自动修改原 `QShader` 中的记录，必须显式调用 `setNativeShaderInfo()` 写回：

```cpp
auto info = shader.nativeShaderInfo(key);
info.extraBufferBindings.insert(1, 3);
shader.setNativeShaderInfo(key, info);
```

`QShader` setter 会按其隐式共享规则修改 package，可能触发 detach。

### 6.3 线程边界来自使用者

结构体值本身可以复制到工作线程，但如果工作线程正在修改一个与渲染线程共享的 `QShader`，仍需外部同步。更稳妥的方式是在线程之间传递完整、不可变的 shader package，生成新版本后在渲染线程按 QRhi 生命周期替换 pipeline。

## 7. 与相关类型的边界

### 7.1 与 `QShaderDescription`

`QShaderDescription` 描述 shader 的输入、输出和资源反射；`NativeShaderInfo` 是特定 key 的后端附加信息。前者不能简单替代后者，后者也不提供完整反射。

### 7.2 与 `NativeResourceBindingMap`

`NativeResourceBindingMap` 主要表达通用资源 binding 到后端原生 binding 的映射；`extraBufferBindings` 只表达 `NativeShaderInfo` 中的额外 buffer 关系。二者可能同时存在，不能因为其中一个 map 为空就删除另一个。

### 7.3 与 `SeparateToCombinedImageSamplerMapping`

独立 texture/sampler 合并需要另一组按 key 保存的映射列表。`extraBufferBindings` 不描述 combined image sampler，不应交叉解释。

### 7.4 与 `QShaderKey`

`QShaderKey` 决定查找哪一份 `NativeShaderInfo`。key 不同，即使都属于同一个 `QShader`，也可能对应完全不同的后端附加数据。

## 8. 常见误区与排查顺序

### 8.1 自行猜测 `flags` bit

Qt 没有在该结构体页面公开 flags 常量。猜测 bit 含义会使代码绑定某个未承诺的实现细节。优先使用生成器产生的值并原样传递。

### 8.2 把 `extraBufferBindings` 当作完整资源布局

它只是一张额外整数映射表，不能替代 `QShaderDescription`、`QRhiShaderResourceBinding` 或完整 binding map。

### 8.3 用错 key

用 GLSL key 查询 MSL 的附加信息会得到空对象或错误关联。排查时同时打印 source、version、variant 和 `availableShaders()` 返回的 key。

### 8.4 修改查询结果却忘记写回

`nativeShaderInfo()` 返回值对象。修改局部变量不会改变 package，必须调用 `setNativeShaderInfo()`。

### 8.5 把默认空对象当成错误

没有附加信息可能是合法状态，例如该语言或阶段不需要此映射。是否错误取决于目标后端和生成器约定，而不是只看 `flags == 0`。

### 8.6 跨 Qt 小版本持久化内部假设

RHI API 没有源和二进制兼容保证。即使 `QMap<int, int>` 的外形不变，也不能据此假设 `flags` 和绑定编号在不同 Qt 小版本中含义不变。

### 8.7 直接把结构体交给 GPU

该类型是 CPU 侧元数据，不是 `QRhiShaderStage`、shader module 或 pipeline 对象。它需要作为 `QShader` package 的一部分被 RHI 消费。

## 9. 逐项 API 说明

### 数据成员

#### `int QShader::NativeShaderInfo::flags`

保存后端或生成器定义的整数标志。默认构造时为 `0`。Qt 6.11.1 的公共结构体文档没有提供通用 flags 枚举，因此应用不应擅自按位解释或构造业务协议。

它不是 `QFlags`，也不保证非零值在其他后端有意义。使用自定义生成器时，必须和目标 Qt/RHI 版本的消费者实现保持一致。

#### `QMap<int, int> QShader::NativeShaderInfo::extraBufferBindings`

保存额外 buffer 绑定映射。默认构造时为空 `QMap`。它的编号语义由目标 shader 生成器和后端约定，不能单凭字段名称确定键和值的方向。

修改 map 只修改结构体副本；如果该副本来自 `QShader::nativeShaderInfo()`，要调用 `QShader::setNativeShaderInfo()` 才能写回 package。

### 相关 `QShader` API

#### `QShader::NativeShaderInfo QShader::nativeShaderInfo(const QShaderKey &key) const`

按精确 `QShaderKey` 返回原生 shader 附加信息。没有数据、语言不适用或阶段不适用时返回空对象。查询是值返回，不会让调用方直接修改 package。

#### `void QShader::setNativeShaderInfo(const QShaderKey &key, const QShader::NativeShaderInfo &info)`

把附加信息写入指定 key。它会修改 `QShader` 的 package，并在隐式共享需要时触发 detach。调用方要保证 info 与该 key 的 shader code、阶段和其他映射一致。

#### `void QShader::removeNativeShaderInfo(const QShaderKey &key)`

删除指定 key 的原生附加信息。它不删除该 key 的 shader code、反射描述、资源绑定 map 或 combined sampler 映射。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `int flags` | 保存后端附加整数标志 | Qt 没有公开通用 bit 定义；不要自行猜测或按 `QFlags` 使用 |
| 字段 | `QMap<int, int> extraBufferBindings` | 保存额外 buffer 绑定映射 | 键和值的方向由生成器/后端约定，空 map 可能是合法状态 |
| 查询 | `QShader::nativeShaderInfo(const QShaderKey &) const` | 获取某个 key 的附加信息值 | 按精确 key 查找；无数据时返回默认空对象 |
| 写入 | `QShader::setNativeShaderInfo(const QShaderKey &, const NativeShaderInfo &)` | 把附加信息挂到 package 的指定 key | 修改值对象不会自动发生；必须与 shader code 和其他元数据一致 |
| 删除 | `QShader::removeNativeShaderInfo(const QShaderKey &)` | 删除指定 key 的附加信息 | 不影响 code、反射或其他按 key 保存的映射 |
| 相关 | `QShaderKey` | 指定 source、版本和 variant | key 不同就是不同记录，不能跨 key 盲目复用 |
| 相关 | `QShaderDescription` | 提供输入、输出和资源反射 | 不能被 `NativeShaderInfo` 或其 map 完全替代 |
| 相关 | `QShader::NativeResourceBindingMap` | 提供资源 binding 的后端映射 | 与额外 buffer 映射是不同数据层次，可能同时存在 |
| 兼容性 | RHI API | 提供 Qt 的跨后端 shader 资产接口 | 没有源/二进制兼容保证，应锁定 Qt 版本并隔离适配代码 |

---

### 一句话总结

`QShader::NativeShaderInfo` 是按 `QShaderKey` 挂在 shader package 上的后端附加值：`flags` 和 `extraBufferBindings` 都是生成器/RHI 约定的数据，不是通用资源布局；查询结果要修改必须写回 `QShader`，而普通应用应优先保存和传递生成工具产出的完整 package。
