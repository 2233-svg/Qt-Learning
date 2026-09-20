# QImageIOPlugin

> Qt 6.11.1 · Qt GUI · 来自 `QImageIOPlugin`

## 1. 先建立直觉

`QImageIOPlugin` 是“让 Qt 发现一种图像格式”的工厂插件。它不直接解码图片；它先判断自己的格式能否读、写或增量读当前输入，再创建对应的 `QImageIOHandler` 去完成实际工作。

应用开发者通常不直接调用它。只要把格式插件随程序正确部署，`QImageReader` 与 `QImageWriter` 会通过 Qt 插件系统发现它。只有新增私有图片格式或维护 imageformats 插件时，才继承此类。

## 2. 类说明

- 头文件：`#include <QImageIOPlugin>`
- CMake：`target_link_libraries(plugin PRIVATE Qt6::Gui)`
- 继承：`QObject` 与 `QImageIOHandlerFactoryInterface`。
- 插件入口：使用 `Q_PLUGIN_METADATA` 声明 IID 和 JSON 元数据；实际 handler 由 `create()` 返回。
- Qt 加载插件后会在格式检测与读写阶段调用 `capabilities()`；它必须快速、可靠，且不破坏输入流状态。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QImageIOPlugin(parent)` | 创建 QObject 插件基类并交给 Qt 管理 |
| `capabilities(device, format)` | 报告当前输入和格式请求下可读、可写、是否增量读 |
| `create(device, format)` | 创建并配置一个新的 `QImageIOHandler` |
| `Capability::CanRead` | 插件能读取当前设备/格式 |
| `Capability::CanWrite` | 插件能写入所请求格式 |
| `Capability::CanReadIncremental` | 插件可在流持续到达时增量读取 |
| `Capabilities` | 多个 capability 的 `QFlags` 组合 |

## 4. 关键用法

### 插件骨架

```cpp
class AcmeImagePlugin final : public QImageIOPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QImageIOHandlerFactoryInterface"
                      FILE "acme.json")

public:
    Capabilities capabilities(QIODevice *device,
                              const QByteArray &format) const override;
    QImageIOHandler *create(QIODevice *device,
                            const QByteArray &format) const override;
};
```

`capabilities()` 决定 Qt 是否应该把这个 plugin 纳入候选；`create()` 只在 Qt 已选择该插件后负责分配 handler。不要在 plugin 层做完整解码，也不要返回多个 handler 共享的可变单例。

### 正确区分读写能力

```cpp
QImageIOPlugin::Capabilities AcmeImagePlugin::capabilities(
    QIODevice *device, const QByteArray &format) const
{
    if (format.compare("acme", Qt::CaseInsensitive) == 0)
        return CanRead | CanWrite;

    if (device && device->peek(8) == "ACMEIMG\0")
        return CanRead;

    return {};
}

QImageIOHandler *AcmeImagePlugin::create(
    QIODevice *device, const QByteArray &format) const
{
    auto *handler = new AcmeHandler;
    handler->setDevice(device);
    handler->setFormat(format.isEmpty() ? "acme" : format);
    return handler;
}
```

格式字符串是显式意图；没有格式字符串时，才用 `peek()` 对内容做快速签名检查。对于写入，device 通常没有数据可探测，必须依据 `format` 作出 `CanWrite` 判断。

### 维护插件元数据与部署

```json
{
  "Keys": [ "acme", "acm" ],
  "MimeTypes": [ "image/x-acme" ]
}
```

键决定文件扩展名或显式 format 如何找到插件。编译成功却读不到图片，最常见原因不是 handler，而是插件 JSON、IID、部署目录或动态库依赖不正确。

## 5. 使用场景

- 增加企业私有的归档图片格式。
- 为专业图像格式实现 Qt 的读写与缩略图支持。
- 将硬件/网络的增量图像流接入 `QImageReader` 生态。
- 为 `QImageWriter` 提供特定压缩、子类型或元数据能力。

## 6. 常见坑与经验

- **`capabilities()` 不能消费输入。** 与 handler 的 `canRead()` 一样，必须用 `peek()` 或恢复 device 位置。
- **不要对所有 device 宣称 `CanRead`。** 这会抢占其他插件，造成格式误判或错误的 reader 选择。
- **`CanWrite` 必须依赖明确格式。** 输出流没有 header 可识别；format 为空时不应随意猜测。
- **每次 `create()` 返回独立 handler。** handler 绑定 device、帧位置、选项和错误状态，不能被多个 reader 并发共享。
- **QObject 线程规则仍然适用。** Qt 管理 plugin 对象，但 handler 的并发访问与内部全局状态仍由实现负责。
- **部署是功能的一部分。** 把库放入正确的 Qt `imageformats` 插件路径，并确认依赖库也能被加载；用 `QImageReader::supportedImageFormats()` 做发布版验证。

## 7. 知识点覆盖

Qt 插件发现、工厂模式、QObject 生命周期、格式嗅探、读写能力协商、增量解码、JSON 元数据、动态库部署、handler 隔离、插件诊断。
