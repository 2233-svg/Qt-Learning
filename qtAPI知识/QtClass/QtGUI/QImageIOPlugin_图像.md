# QImageIOPlugin：把自定义图像格式接入 Qt 的插件工厂

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QImageIOPlugin>`  
> 继承：`QObject`

## 它解决什么问题

`QImageIOPlugin` 是图像格式插件的工厂接口。它不直接解码或编码图片，而是回答两个问题：

1. 给定设备内容和格式名，这个插件能读、能写，还是能增量读取？
2. Qt 决定使用它后，如何创建并配置一个对应的 `QImageIOHandler`？

借此，`QImageReader` 与 `QImageWriter` 能在运行时发现 Qt 之外的图像格式，而应用仍沿用统一的 reader/writer API。格式探测、插件选择、handler 生命周期由 Qt 的插件系统协调，像素解析放在 `QImageIOHandler` 派生类中。

它不是给“读取一张 PNG”准备的常规类。普通应用应使用 `QImageReader`、`QImageWriter` 或 `QImage`；只有要向 Qt 增加新格式时才实现此类。

## 实际使用场景

- 为内部归档格式、游戏纹理格式、医疗设备帧或科学相机输出提供 Qt 支持。
- 把已有 C/C++ 解码库包装为可由 `QImageReader` 自动识别的插件。
- 将读取和写入拆分到不同插件，例如一个只读动画解码器和一个只写编码器。
- 让桌面工具、图像预览器和第三方 Qt 程序通过标准图像 API 使用新格式。
- 在部署时让 `QImageReader::supportedImageFormats()` 等能力查询包含自定义格式。

## 架构：plugin 做选择，handler 做工作

一份图像格式插件通常包含：

```text
FooImagePlugin (QImageIOPlugin)
  ├─ capabilities(device, format)  // 探测和能力声明
  └─ create(device, format)
       └─ FooImageHandler (QImageIOHandler)
            ├─ canRead()
            ├─ read(QImage *)
            └─ write(const QImage &)  // 若支持写入
```

插件应保持轻量。`capabilities()` 可能在格式列表查询、文件探测或写入前多次调用，不能在其中实际解码整图、缓存指向短命设备的数据，或改变设备读位置。

## 最小插件骨架

`Q_PLUGIN_METADATA` 把类导出为 Qt 插件，`FILE` 指向编译期可见的 JSON 元数据。真实项目还需要按 Qt 的插件目录规则构建和部署动态库；只把 JSON 复制到应用旁边不会使格式自动可用。

```cpp
#include <QImageIOPlugin>

class FooImagePlugin final : public QImageIOPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QImageIOHandlerFactoryInterface"
                      FILE "fooimage.json")

public:
    Capabilities capabilities(QIODevice *device,
                              const QByteArray &format) const override;

    QImageIOHandler *create(QIODevice *device,
                            const QByteArray &format) const override;
};
```

`fooimage.json` 中的 `Keys` 是 Qt 据以查找插件的格式名，必须与 `create()` 可接受的值相符；`MimeTypes` 与 key 一一对应。

```json
{
    "Keys": [ "foo" ],
    "MimeTypes": [ "image/x-foo" ]
}
```

格式名总是小写。不要只在实现里接受 `"FOO"` 或 `"Foo"`，再让 metadata 写成另一套名称；这样会导致 Qt 根本不选择该插件。

## capabilities()：探测必须无副作用

`capabilities(QIODevice *device, const QByteArray &format)` 是插件路由的核心。

- 当 `device == nullptr` 时，只根据 `format` 报告该格式理论上支持哪些读写能力。
- 当 device 非空时，结合格式提示和设备前导字节，判断当前数据能否由插件处理。
- `format` 为空时，插件可探测自己支持的任意格式；非空时，只应接受本插件 metadata `Keys` 中的格式。
- 检查签名时使用 `device->peek()`，或严格保存和恢复位置。绝不能改变 device 的状态。
- 返回 `CanRead`、`CanWrite`、`CanReadIncremental` 的 OR 组合；不确定或不匹配时返回空 flags。

```cpp
QImageIOPlugin::Capabilities FooImagePlugin::capabilities(
    QIODevice *device, const QByteArray &format) const
{
    if (!format.isEmpty() && format != "foo") {
        return {};
    }

    if (!device) {
        return CanRead | CanWrite;
    }

    return device->peek(8) == QByteArray("FOOIMG\0", 7)
        ? Capabilities(CanRead)
        : Capabilities();
}
```

若两个已发现插件都声称能完成同一任务，Qt 可以任意挑选其中之一。因此不要把不确定格式或实际不支持的写入能力报为可用，也不能依赖“插件加载顺序”来抢占某个格式。

## create()：返回已配置的全新 handler

`create(device, format)` 在 Qt 已选择本插件后被调用。它应新建一个 `QImageIOHandler` 派生对象，并对该对象调用 `setDevice(device)` 与 `setFormat(format)`。

`format` 必须是 JSON `Keys` 中的值，或为空；为空意味着 `capabilities()` 已借助 device 内容成功识别了格式。handler 中若需要存储实际探测出的子格式，可以在 `canRead()` 中使用其 const `setFormat()` 重载。

```cpp
QImageIOHandler *FooImagePlugin::create(
    QIODevice *device, const QByteArray &format) const
{
    auto *handler = new FooImageHandler;
    handler->setDevice(device);
    handler->setFormat(format);
    return handler;
}
```

不要返回复用的全局 handler。`QImageIOHandler` 会保存设备、选项和当前帧状态，而 `setDevice()` 只能设置一次；每一次 `create()` 都应返回独立会话对象。

## 能力位的真实含义

| 能力 | 含义 | 不能据此假定的事 |
| --- | --- | --- |
| `CanRead` | 可以从匹配的设备内容解码至少一种图像。 | 不代表支持多帧、随机跳帧、所有 option 或任何尺寸的输入。 |
| `CanWrite` | 可以把 `QImage` 写成对应格式。 | 不代表所有 `QImage::Format` 都无损接受；handler 可能需要转换或拒绝。 |
| `CanReadIncremental` | 可以以增量方式读取，`QImageReader` 会按动画式流程对待。 | 不等于所有动画格式，也不自动实现帧跳转和循环计数。 |

`Capabilities` 是 `QFlags<Capability>`，可用位或组合。对于具体设备返回的能力应保守且准确；对空 device 的能力则描述格式的总体潜力。

## QObject、线程与部署边界

`QImageIOPlugin` 继承 `QObject`，其构造函数可接收 parent；由 `Q_PLUGIN_METADATA` 导出的插件实例通常由 Qt 的插件加载机制创建，应用不应手动销毁它。文档说明 Qt 会在插件不再使用时自动析构。

类成员函数可重入，但实际动态库加载、插件路径、全局解码库初始化和 `QIODevice` 状态都会影响并发设计。避免在 plugin 对象里保存“当前 device”“当前帧”或“上一次格式”之类会话数据，把这些状态放进每个 handler 实例。

部署时必须保证：

- 插件动态库由当前 Qt 运行时和编译器 ABI 构建。
- JSON metadata 已被编进插件，而不是仅作为外部文件存在。
- 动态库位于应用可发现的图像格式插件路径，或由程序以明确的插件路径配置加载。
- 所依赖的第三方解码库也能被运行时找到。

遇到“本机可读、部署后不支持”的问题，先查询运行时支持格式和 Qt 插件路径，再检查动态库依赖与 release/debug 构建是否匹配。

## 常见错误

- 把 `QImageIOPlugin` 当作解码器，把所有解析逻辑塞进 `capabilities()`。
- 探测 magic bytes 时推进 `QIODevice`，破坏随后 handler 的读取位置。
- device 为 `nullptr` 时返回空能力，导致格式枚举时插件不可见。
- 接受不在 metadata `Keys` 内的 `format`，让路由信息与工厂行为不一致。
- 忽略“格式名总是小写”的契约。
- 对同一 handler 反复 `setDevice()`，或让多个 reader 共享一个 handler。
- 宣称 `CanWrite`，但 `create()` 返回的 handler 的 `write()` 仍是基类默认的 `false`。
- 把 `CanReadIncremental` 当作“普通多帧读取”的泛泛标记，却没有实现相应的 handler 状态协议。
- 两个插件都为同一签名返回 `CanRead`，却依赖 Qt 总是选择自己。
- JSON 的 `Keys` 和 `MimeTypes` 数量不匹配，或 metadata 没有被纳入插件二进制。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `Capability` | 单项能力：`CanRead`、`CanWrite`、`CanReadIncremental`。 |
| 类型 | `Capabilities` | `QFlags<Capability>`；返回值可按位组合多个能力。 |
| 构造 | `explicit QImageIOPlugin(QObject *parent = nullptr)` | 创建插件对象；通常由 moc 生成的插件导出代码和 Qt loader 调用。 |
| 析构 | `virtual ~QImageIOPlugin()` | 虚析构；已加载插件不再使用时由 Qt 自动销毁，应用通常不手动调用。 |
| 工厂探测 | `virtual Capabilities capabilities(QIODevice *device, const QByteArray &format) const = 0` | 必须实现。device 为 null 时报告格式总体能力；非空时不改变 device 状态地探测当前数据。格式名总为小写。 |
| 工厂创建 | `virtual QImageIOHandler *create(QIODevice *device, const QByteArray &format = {}) const = 0` | 必须实现。返回新的、已设置 device 与 format 的 handler；format 应来自 metadata `Keys` 或为空且已被探测确认。 |
| 插件导出 | `Q_PLUGIN_METADATA(IID ..., FILE ...)` | 不是成员函数，但实现插件必需。导出 IID 并嵌入含 `Keys`、`MimeTypes` 的 JSON metadata。 |

## 相关类

- `QImageIOHandler`：每次读写会话的真正编解码实现。
- `QImageReader`：读取端发现插件、检查格式并驱动 handler。
- `QImageWriter`：写入端发现插件并驱动 handler。
- `QPluginLoader`：需要手动诊断或加载 Qt 插件时使用。
- `QIODevice`：插件探测和 handler 读写的字节流来源。

`QImageIOPlugin` 的关键职责是做出诚实、无副作用的能力判断，然后交付一个独立的 handler。把路由和会话拆开，插件才会在复杂部署与并发读取中保持可靠。
