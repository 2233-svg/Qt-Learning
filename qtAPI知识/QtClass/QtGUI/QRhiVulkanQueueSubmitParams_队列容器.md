# Qt QRhiVulkanQueueSubmitParams：把外部 Vulkan 信号量接入下一次 RHI 提交

> 适用版本：Qt 6.11.1  
> 文档引入版本：Qt 6.9  
> 头文件（文档写法）：`#include <QRhiVulkanQueueSubmitParams>`  
> 实际定义：`rhi/qrhi_platform.h` 中的 Vulkan 条件分支  
> 所属模块：`Qt6::Gui` 文档类型，属于 RHI 扩展接口  
> 基类：`QRhiNativeHandles`

## 1. 它解决什么问题

`QRhiVulkanQueueSubmitParams` 是一个用于 Vulkan 后端的参数结构体。它把应用自己管理的 `VkSemaphore` 列表交给 `QRhi`，让这些信号量参与**下一次**图形队列提交或下一次 present。

典型场景是：应用除了使用 Qt RHI 录制命令，还执行了原生 Vulkan 渲染、计算或资源操作。原生代码和 RHI 代码之间需要通过 Vulkan semaphore 建立 GPU 阶段依赖时，可以把外部 semaphore 交给：

```cpp
rhi->setQueueSubmitParams(&params);
```

这不是普通的“队列容器”或拥有内存的 Qt 容器，而是一个带裸指针的 C 风格参数块：

- 结构体不创建、销毁或复制 Vulkan semaphore。
- `*_Count` 表示对应指针数组中的元素个数。
- 指针必须指向调用方管理的、连续的 `VkSemaphore` 元素。
- 参数只影响下一次相关提交，不能作为持久的队列配置。

RHI API 的兼容性保证有限。Qt 6.11.1 文档明确提醒，使用这套 RHI 接口可能带来未来 Qt 版本的源代码或二进制不兼容；它适合明确接受该约束的底层渲染集成，不适合当作稳定的通用 Qt 抽象层。

## 2. 构建与包含

类页列出的 CMake 形式是：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

类页列出的 qmake 形式是：

```qmake
QT += gui
```

不过 `QRhi` 本身的文档将 RHI 头文件标为 `GuiPrivate`，实际安装的 Qt 6.11.1 头文件把这些类型放在 `QtGui/6.11.1/QtGui/rhi/qrhi_platform.h`，并由 `rhi/qrhi.h` 包含。工程应以本机 Qt 安装的头文件布局和目标配置为准：

```cpp
#include <rhi/qrhi.h>
```

在启用 Vulkan 且能够找到 Vulkan SDK 头文件时，`qrhi_platform.h` 才会暴露 `QRhiVulkanQueueSubmitParams`。如果 Qt 构建没有启用 Vulkan，或者编译器找不到 `<vulkan/vulkan.h>`，该类型不会作为可用的 Vulkan 结构体出现。

## 3. 最小使用方式

下面的示例展示参数块、数组和“下一次提交”的对应关系。`externalWait`、`externalSignal` 必须是由同一个 Vulkan device 体系创建并由应用按 Vulkan 规则管理的 semaphore。

```cpp
#include <rhi/qrhi.h>

void submitWithExternalSemaphores(QRhi *rhi,
                                  QRhiSwapChain *swapChain,
                                  VkSemaphore externalWait,
                                  VkSemaphore externalSignal)
{
    VkSemaphore waits[] = { externalWait };
    VkSemaphore signals[] = { externalSignal };

    QRhiVulkanQueueSubmitParams params{};
    params.waitSemaphoreCount = 1;
    params.waitSemaphores = waits;
    params.signalSemaphoreCount = 1;
    params.signalSemaphores = signals;

    // 只影响后续的下一次队列提交。
    rhi->setQueueSubmitParams(&params);
    const QRhi::FrameOpResult result = rhi->endFrame(swapChain);
    Q_UNUSED(result);
}
```

真实程序必须先处于符合 `QRhi` 帧流程的状态，例如已经成功调用对应的 `beginFrame()`。示例的重点是生命周期：`params` 和两个数组至少要活到触发提交的 RHI 调用返回。

如果只需要 present 前等待 semaphore：

```cpp
QRhiVulkanQueueSubmitParams params{};
params.presentWaitSemaphoreCount = 1;
params.presentWaitSemaphores = &presentWait;

rhi->setQueueSubmitParams(&params);
// 下一次包含 present 的 endFrame() 会使用 presentWait。
```

`presentWaitSemaphores` 不等同于 `waitSemaphores`：前者给下一次 `vkQueuePresentKHR()`，后者给下一次 `vkQueueSubmit()`。

## 4. 六个字段如何配对

### 4.1 submit 阶段的等待 semaphore

`waitSemaphoreCount` 与 `waitSemaphores` 成对使用。它们描述下一次 `vkQueueSubmit()` 需要等待的 semaphore。

```cpp
params.waitSemaphoreCount = static_cast<uint32_t>(waits.size());
params.waitSemaphores = waits.data();
```

当数量为零时，通常可以把指针设为 `nullptr`。当数量大于零时，指针必须有效，并且数组至少包含指定数量的 `VkSemaphore`。

该结构只暴露 semaphore 句柄和数量，不提供每个等待 semaphore 的 pipeline stage mask，也不提供 timeline semaphore 的 wait value。需要这些更细粒度同步参数时，不能假定此结构能完整表达原生 `VkSubmitInfo`/`VkTimelineSemaphoreSubmitInfo` 语义。

### 4.2 submit 阶段的 signal semaphore

`signalSemaphoreCount` 与 `signalSemaphores` 成对使用。它们描述下一次 `vkQueueSubmit()` 完成相关工作后要 signal 的 semaphore。

调用方仍负责确保：

- semaphore 的生命周期覆盖 GPU 使用期，而不只是覆盖 `endFrame()` 的 CPU 调用。
- semaphore 的状态符合 Vulkan 对 binary/timeline semaphore 的要求。
- 不把仍处于 pending 状态、或不属于当前 device 的 semaphore 错误地交给 RHI。

`QRhiVulkanQueueSubmitParams` 不会替调用方等待 GPU 或销毁 semaphore。

### 4.3 present 阶段的等待 semaphore

`presentWaitSemaphoreCount` 与 `presentWaitSemaphores` 描述下一次 `vkQueuePresentKHR()` 需要等待的 semaphore。Qt 文档特别指出，当该 count 非零时，它作用于下一次 present。

因此：

- 它通常只在有 swapchain present 的 `endFrame()` 中有意义。
- `endOffscreenFrame()` 或 `finish()` 若没有 present，不能把它们当作 present 等待点。
- 不要把 present wait 列表误放入 `waitSemaphores`，两者作用于 Vulkan 的不同操作。

## 5. 与 `QRhi::setQueueSubmitParams()` 的时间关系

### 5.1 只消费一次

`QRhi::setQueueSubmitParams()` 的语义是给**下一次**队列提交提供附加参数。Qt 文档列出的实际消费点包括：

- `endFrame()`。
- `endOffscreenFrame()`。
- `finish()`。

调用完成后，不应假设同一参数仍会自动应用到下一帧。如果下一次提交还需要外部 semaphore，应再次设置。

### 5.2 参数指针不是长期配置

函数参数类型是 `QRhiNativeHandles *`，而不是按值传入的 `QRhiVulkanQueueSubmitParams`。这意味着应用必须把对象和内部数组保持有效到 RHI 消费它们的时机。

推荐把参数与数组放在同一作用域，并紧接着调用触发提交的函数：

```cpp
VkSemaphore waits[] = { waitSemaphore };
QRhiVulkanQueueSubmitParams params{};
params.waitSemaphoreCount = 1;
params.waitSemaphores = waits;

rhi->setQueueSubmitParams(&params);
const auto result = rhi->finish();
```

如果设置参数后还要经过多个异步步骤，不能把局部变量销毁后再等待 Qt 将来使用它。

### 5.3 后端匹配

只有 Vulkan 后端对这些字段有对应语义。`QRhi` 文档说明，许多其他后端对 `setQueueSubmitParams()` 是 no-op。

调用前应确认：

```cpp
if (rhi->backend() == QRhi::Vulkan) {
    // 才使用 QRhiVulkanQueueSubmitParams。
}
```

即使当前工程只使用 Vulkan，也不要把这个结构传给 D3D、Metal、OpenGL ES 或 Null 后端并期待相同效果。

## 6. 实际使用场景

### 6.1 原生 Vulkan 计算与 Qt RHI 交接

应用可能用自己的 Vulkan command buffer 做计算，将结果写入共享 image/buffer，然后让 Qt RHI 的下一次提交等待一个外部 signal semaphore：

```text
原生 Vulkan submit signal S
             |
             v
Qt RHI next submit wait S
```

反向地，也可以让 Qt RHI signal 一个 semaphore，原生 Vulkan 提交等待它。

### 6.2 自定义 present 同步

当应用在 RHI 帧外执行了与 swapchain 相关的原生 Vulkan 工作，需要让下一次 present 等待额外 semaphore，可以使用 `presentWaitSemaphores`。

### 6.3 与外部 Vulkan 组件互操作

视频解码器、计算库、采集组件或引擎插件可能暴露 Vulkan semaphore。该结构提供了把这些同步对象接入 Qt RHI 下一次提交的窄接口，但资源所有权和设备兼容性仍由集成方负责。

## 7. 生命周期、所有权和线程

### 7.1 结构体不拥有任何对象

`QRhiVulkanQueueSubmitParams` 只是一个继承自空 `QRhiNativeHandles` 的数据结构。六个字段中的两个指针类型都只是借用地址：

- 不会复制 semaphore 数组。
- 不会释放数组。
- 不会销毁 `VkSemaphore`。
- 不会延长 semaphore 的 GPU 生命周期。

`count` 与数组内容由调用方维护，结构体本身不会检查一致性。

### 7.2 semaphore 的 GPU 生命周期长于 CPU 调用

即使 `endFrame()` 已经返回，GPU 可能仍在执行对应提交。应用不能只因为参数结构可以离开作用域，就立即销毁 signal/wait semaphore。应按 Vulkan fence、队列空闲或资源回收策略决定实际销毁时间。

### 7.3 与 QRhi 所在线程一致

`QRhi` 文档说明，RHI 操作发生在 QRhi 初始化所在的线程。`setQueueSubmitParams()` 应在执行相关 RHI 帧操作的线程调用；不要从另一个线程同时修改参数结构或 semaphore 数组。

如果渲染器在专用线程，先在该线程准备并设置参数，或通过线程安全的消息机制把值和同步对象的使用请求传递给渲染线程。

### 7.4 结构体的默认初始化

头文件没有给六个字段提供默认成员初始化。应使用值初始化：

```cpp
QRhiVulkanQueueSubmitParams params{};
```

这样 count 为零、指针为 null。若写成普通局部变量 `QRhiVulkanQueueSubmitParams params;`，不要读取未初始化字段。

## 8. Vulkan 和 RHI 的边界

### 8.1 它不是完整的 `VkSubmitInfo`

这个结构只描述三组 semaphore 数组，没有暴露：

- wait semaphore 的 stage mask。
- submit command buffer。
- fence。
- timeline semaphore 的具体值。
- Vulkan submit 的 pNext 链。

Qt RHI 会把这些字段组合进自己的 backend 提交流程。需要完全控制 Vulkan 提交结构时，应使用原生 Vulkan 队列提交，并自行规划它与 QRhi 的互操作边界。

### 8.2 binary semaphore 与重复使用

Vulkan semaphore 的可用状态由 GPU 操作决定。不要在前一轮 GPU 仍可能使用 semaphore 时，把同一个 semaphore 又作为下一轮不兼容的 wait 或 signal 对象。Qt 结构体不会跟踪这些状态。

### 8.3 device 和 queue 必须匹配

外部 semaphore 必须由与 QRhi Vulkan device 兼容的设备体系创建，并用于允许互操作的队列。仅仅因为 C++ 类型都是 `VkSemaphore`，并不代表任意 Vulkan instance/device 创建的句柄都能交给当前 QRhi。

## 9. 常见误区与排查顺序

### 9.1 调用 `setQueueSubmitParams()` 后立刻销毁参数

错误原因：QRhi 接收的是指针，且提交发生在后续的帧结束或 finish 阶段。  
排查方式：让 params、数组和其中的句柄引用至少活到触发提交的调用返回，并让 Vulkan semaphore 本身活到 GPU 使用完毕。

### 9.2 count 与指针不匹配

常见错误包括：

```cpp
params.waitSemaphoreCount = 2;
params.waitSemaphores = &oneSemaphore;
```

这会让 RHI/Vulkan 读取数组边界之外的数据。count 应等于有效连续数组元素数；count 为零时把对应指针设为 `nullptr` 最清晰。

### 9.3 把 present wait 填到 submit wait

`waitSemaphores` 影响 `vkQueueSubmit()`，`presentWaitSemaphores` 影响下一次 `vkQueuePresentKHR()`。两者不是同一个等待点，也不保证可以互换。

### 9.4 认为参数会持续到下一帧

文档语义是 next submission only。每次需要外部同步时，都要为对应的下一次提交重新设置。

### 9.5 在非 Vulkan 后端使用并期待效果

其他后端可能直接忽略这组参数。使用前检查 `rhi->backend()`，并为非 Vulkan 路径设计独立同步方案。

### 9.6 把这个接口当成稳定公共 ABI

RHI 有限兼容性意味着 Qt 升级可能影响源代码和二进制兼容。需要长期维护的产品应把该适配代码隔离在后端模块中，并固定 Qt 版本或做好升级验证。

### 9.7 试图通过它传递 timeline semaphore values

结构体只提供 `VkSemaphore *` 和 count，没有每个 semaphore 的 value 数组。不要从字段名称推断它能表达完整 timeline submit 语义。

## 10. 逐项 API 说明

### 基类和结构体

#### `struct QRhiVulkanQueueSubmitParams : public QRhiNativeHandles`

Vulkan 专用的 RHI 原生句柄参数结构。它没有成员函数、构造函数或析构函数逻辑，默认是一个可聚合初始化的数据块。

它继承 `QRhiNativeHandles` 只是为了能传给 `QRhi::setQueueSubmitParams(QRhiNativeHandles *)`。基类不提供资源所有权或运行时校验。

### submit 等待字段

#### `uint32_t QRhiVulkanQueueSubmitParams::waitSemaphoreCount`

指定 `waitSemaphores` 中用于下一次 `vkQueueSubmit()` 的 semaphore 数量。为零表示没有附加 submit wait semaphore。

count 必须与有效数组长度一致。结构体不会检查负数问题，因为类型是无符号整数；把过大的值传入会导致 Vulkan 读取无效内存或产生验证层错误。

#### `VkSemaphore *QRhiVulkanQueueSubmitParams::waitSemaphores`

指向 submit wait semaphore 数组。数组由调用方拥有，元素数量由 `waitSemaphoreCount` 指定。

当 count 大于零时，指针和数组必须有效；当 count 为零时应设为 `nullptr` 或遵守当前集成层的明确约定。它只传 semaphore 句柄，不携带 wait stage mask。

### submit signal 字段

#### `uint32_t QRhiVulkanQueueSubmitParams::signalSemaphoreCount`

指定 `signalSemaphores` 中用于下一次 `vkQueueSubmit()` 的 semaphore 数量。为零表示没有附加 signal semaphore。

调用方必须确认这些 semaphore 的状态、设备归属和 GPU 生命周期符合 Vulkan 约束。

#### `VkSemaphore *QRhiVulkanQueueSubmitParams::signalSemaphores`

指向 submit signal semaphore 数组。RHI 使用这些句柄构造下一次 submit 的 signal 列表，但不拥有或销毁它们。

不要让数组在触发提交前失效，也不要在 GPU 完成前释放其中的 semaphore。

### present 等待字段

#### `uint32_t QRhiVulkanQueueSubmitParams::presentWaitSemaphoreCount`

指定 `presentWaitSemaphores` 中用于下一次 `vkQueuePresentKHR()` 的 semaphore 数量。Qt 文档明确规定，count 非零时它作用于下一次 present。

没有 present 的 offscreen 路径不能提供同样的效果。

#### `VkSemaphore *QRhiVulkanQueueSubmitParams::presentWaitSemaphores`

指向下一次 present 要等待的 semaphore 数组。它与 submit wait 列表独立，数组生命周期和设备兼容性要求相同。

### 配套调用

#### `[since 6.9] void QRhi::setQueueSubmitParams(QRhiNativeHandles *params)`

把后端相关的附加提交参数交给 QRhi。对 Vulkan，`params` 应指向 `QRhiVulkanQueueSubmitParams`；该调用只影响下一次队列提交。实际提交发生在 `endFrame()`、`endOffscreenFrame()` 或 `finish()` 等帧操作中。

其他后端可能 no-op。调用方必须保证 params 及其数组在 QRhi 消费前有效，并在正确的 QRhi 线程调用。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 结构体 | `QRhiVulkanQueueSubmitParams : QRhiNativeHandles` | 携带 Vulkan 外部 semaphore 列表 | RHI 有限兼容性；不拥有句柄或数组 |
| 初始化 | `QRhiVulkanQueueSubmitParams params{}` | 将 count 和指针初始化为零/null | 普通局部默认初始化可能留下未初始化字段 |
| submit wait 数量 | `uint32_t waitSemaphoreCount` | 指定下一次 `vkQueueSubmit()` 的等待数量 | 必须与 `waitSemaphores` 数组长度一致 |
| submit wait 数组 | `VkSemaphore *waitSemaphores` | 提供下一次 submit 等待的 semaphore | 裸指针借用；count>0 时必须有效；不含 stage mask |
| submit signal 数量 | `uint32_t signalSemaphoreCount` | 指定下一次 submit 的 signal 数量 | semaphore 状态和 GPU 生命周期由调用方负责 |
| submit signal 数组 | `VkSemaphore *signalSemaphores` | 提供下一次 submit 要 signal 的 semaphore | 不会创建或销毁 semaphore |
| present wait 数量 | `uint32_t presentWaitSemaphoreCount` | 指定下一次 `vkQueuePresentKHR()` 的等待数量 | 只对应下一次 present，不是 submit wait |
| present wait 数组 | `VkSemaphore *presentWaitSemaphores` | 提供下一次 present 等待的 semaphore | 无 present 的 offscreen 路径不产生相同效果 |
| RHI 入口 | `QRhi::setQueueSubmitParams(QRhiNativeHandles *)` | 将参数安排到下一次队列提交 | Vulkan 才有对应语义；其他后端可能 no-op |
| 消费时机 | `endFrame()` / `endOffscreenFrame()` / `finish()` | 触发 QRhi 可能消费参数的操作 | 触发调用返回前保持 params 和数组有效 |
| 生命周期 | 外部 `VkSemaphore` | 由应用管理 GPU 同步对象 | CPU 调用返回不等于 GPU 已完成，不能过早销毁 |

---

### 一句话总结

`QRhiVulkanQueueSubmitParams` 是把外部 Vulkan semaphore 接到 Qt RHI 下一次提交的窄接口：六个字段必须按 count/数组成对设置，参数内存要活到实际提交，semaphore 要活到 GPU 使用结束，并且只能在 Vulkan 后端和接受 RHI 有限兼容性的前提下使用。
