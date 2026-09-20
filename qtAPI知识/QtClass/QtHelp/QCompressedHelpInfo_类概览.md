# QCompressedHelpInfo：读取 qch 文件元数据

> 适用版本：Qt 6.11.1
> 头文件：`#include <QCompressedHelpInfo>`
> 所属模块：`Qt6::Help`
> 类型：值类型

## 它解决什么问题

`.qch` 是 Qt Compressed Help 文档包。`QCompressedHelpInfo` 用来读取一个 qch 文件的基本身份信息：namespace、component 和 version。它适合在注册文档前做检查、在插件扫描时显示文档信息，或在安装器中判断文档包是否属于目标组件。

它只提供元数据，不负责把文档注册到 collection file，也不负责读取 HTML 内容。真正的注册和内容访问由 `QHelpEngineCore` 完成。

## 实际使用场景

- 扫描文档目录，列出每个 qch 的 namespace、组件和版本。
- 注册前检查 qch 是否可读、是否为有效压缩帮助文件。
- 选择与当前软件版本匹配的文档包。
- 在诊断日志中显示文档包身份，帮助定位重复 namespace 或版本冲突。

## 创建与有效性

默认构造得到空信息。通常使用静态函数 `fromCompressedHelpFile()` 从文件名创建对象；如果文件不存在、格式不合法或元数据无法读取，返回对象会保持 null 状态，应先调用 `isNull()`。

这是隐式共享的值类型，拷贝和移动成本很低。它没有修改元数据的接口，因此读取同一个对象的多个副本不会改变 qch 文件，也不会把文档注册到帮助引擎。

`namespaceName()`、`component()` 返回空字符串，`version()` 返回无效版本，都可能表示信息缺失。最可靠的整体判断是先检查 `isNull()`，然后再按业务要求检查具体字段。

## 边界与误区

- `fromCompressedHelpFile()` 只读取文件信息，不等于完成 `QHelpEngineCore::registerDocumentation()`。
- 不能通过这个类修改 qch 内的 namespace、组件或版本；这些元数据在生成文档包时确定。
- 相同 namespace 的多个 qch 不能同时注册到同一个 collection，扫描阶段应提前发现冲突。
- 对象保存的是读取结果，不是对文件的持续锁定；原文件之后被删除不会改变已有值，但再次读取会失败。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QCompressedHelpInfo()` | 构造空的 qch 信息对象。 | 构造后通常 `isNull()` 为 `true`。 |
| `QCompressedHelpInfo(const QCompressedHelpInfo &other)` | 拷贝已有信息。 | 值语义；隐式共享，适合按值返回和传递。 |
| `QCompressedHelpInfo(QCompressedHelpInfo &&other)` | 移动构造信息对象。 | 移动后源对象仍可析构和重新赋值，不应继续依赖其旧内容。 |
| `~QCompressedHelpInfo()` | 释放信息对象。 | 不会删除 qch 文件，也不会注销已注册文档。 |
| `operator=(const QCompressedHelpInfo &other)` | 拷贝赋值。 | 只改变当前值对象，不影响源对象或文件。 |
| `operator=(QCompressedHelpInfo &&other)` | 移动赋值。 | 适合接收临时扫描结果。 |
| `void swap(QCompressedHelpInfo &other)` | 交换两个信息对象。 | `noexcept`，不会读取或修改 qch 文件。 |
| `static QCompressedHelpInfo fromCompressedHelpFile(const QString &documentationFileName)` | 从 qch 文件读取元数据。 | 文件无效时返回 null 信息；调用不等于注册文档。 |
| `QString namespaceName() const` | 返回 qch 的 namespace。 | 空值可能表示无效对象或元数据缺失；namespace 是 collection 中的唯一身份。 |
| `QString component() const` | 返回 qch 的组件名。 | 可用于过滤器匹配；不要把它当作 namespace。 |
| `QVersionNumber version() const` | 返回 qch 的版本号。 | 可能是无效版本；过滤器按版本匹配时应先确认有效性。 |
| `bool isNull() const` | 判断对象是否没有有效 qch 信息。 | 读取文件失败时优先检查它，而不是只检查某一个字符串字段。 |

## 一句话总结

`QCompressedHelpInfo` 是 qch 的只读身份卡：先用 `fromCompressedHelpFile()` 扫描，再用 `isNull()` 和三个元数据 getter 判断是否适合注册或展示。
