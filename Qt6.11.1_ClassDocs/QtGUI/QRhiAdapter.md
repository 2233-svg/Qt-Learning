# QRhiAdapter

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiAdapter`

## 1. 先建立直觉

`QRhiAdapter` 表示某个 RHI 后端可用的图形适配器，也就是可被选择来创建 `QRhi` 的 GPU/软件设备抽象。它本身不渲染，也不创建资源；它的主要价值是携带驱动/设备信息，让你在创建 RHI 前做选择。

Qt 6.10 起可以通过 `QRhi::enumerateAdapters()` 获取 adapter 列表，再把选中的 adapter 传给 `QRhi::create()`。这对多 GPU 笔记本、外接 GPU、软件渲染 fallback、诊断工具特别有用。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- API 层级：Qt GUI 私有 API
- 获取方式：`QRhi::enumerateAdapters(...)`
- 主要输出：`QRhiDriverInfo`

`QRhiAdapter` 的生命周期通常由枚举结果管理。不要把它当作长期 GPU 资源，也不要在对应枚举上下文失效后继续依赖裸指针。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `info() const` | 返回该适配器的 `QRhiDriverInfo`，用于查看设备、驱动、厂商、软件/硬件等信息。 |
| `QRhi::enumerateAdapters()` | 获取当前后端可用 adapter 列表。 |
| `QRhi::create(..., adapter)` | 用指定 adapter 创建 RHI。 |

## 4. 关键用法

```cpp
auto adapters = QRhi::enumerateAdapters(QRhi::Vulkan, params);
for (QRhiAdapter *adapter : adapters) {
    QRhiDriverInfo info = adapter->info();
    qDebug() << info.deviceName << info.vendorName;
}

QRhi *rhi = QRhi::create(QRhi::Vulkan, params, {}, nullptr, adapters.first());
```

实际选择策略可以很简单：优先硬件 GPU，失败再尝试软件；或者提供设置项让用户选择。不要只按列表顺序假设“一定是最佳显卡”。

## 5. 使用场景

- 多 GPU 环境中选择独显、集显或软件设备。
- 图形设置页展示设备名称、驱动信息、厂商信息。
- 渲染初始化失败时做 fallback。
- 自动测试中固定使用软件 renderer。
- 诊断后端能力差异和用户环境问题。

## 6. 常见坑与经验

- **adapter 不是 `QRhi`。** 选中 adapter 之后仍需要调用 `QRhi::create()`。
- **列表顺序不等于性能排序。** 后端和平台可能有自己的枚举顺序。
- **设备信息只用于决策和展示。** 真正可用功能仍要在 `QRhi` 创建后用 `isFeatureSupported()` 查询。
- **私有 API 要关注版本。** Qt 升级后 adapter 枚举和 driver info 字段都应重新验证。
- **软件渲染不是错误。** 在 CI、远程桌面、无 GPU 机器上它可能是合理 fallback。

## 7. 知识点覆盖

- RHI 后端与图形适配器的关系
- adapter 枚举、驱动信息和 RHI 创建
- 多 GPU、软件渲染、fallback 策略
- 设备展示信息与实际功能查询的区别
