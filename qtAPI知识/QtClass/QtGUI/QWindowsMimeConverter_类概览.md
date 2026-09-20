# QWindowsMimeConverter：Windows MIME 与剪贴板格式桥接

> 适用版本：Qt 6.11.1
> 头文件：`#include <QtGui/private/qwindowsmimeconverter_p.h>`
> 所属模块：`Qt6::Gui`
> 类型：Windows 平台内部扩展基类

## 它解决什么问题

Windows 剪贴板和拖放使用 COM `IDataObject`、`FORMATETC`、`STGMEDIUM` 等数据结构，而 Qt 对外使用 `QMimeData` 和 MIME 类型字符串。`QWindowsMimeConverter` 是 Windows 平台插件用于连接这两套数据模型的转换器基类。

它允许一个转换器声明：“这个 Qt MIME 类型可以转换成某种 Windows 原生格式”，也允许反方向声明：“这个 Windows 原生格式可以暴露成某种 Qt MIME 类型”。例如文本、HTML、文件列表和应用自定义 clipboard format 都可以通过不同转换器接入 Qt 的复制粘贴与拖放流程。

该类位于 Qt 的 Windows 平台实现边界，不是普通业务代码优先使用的公共跨平台 API。只有需要编写 Windows MIME converter、接入自定义 `IDataObject` 格式或维护 Qt Windows 平台插件时，才应直接继承它。

## 实际使用场景

- 为应用自定义的 Windows clipboard format 增加 Qt MIME 表示。
- 让外部 Windows 程序提供的数据进入 `QMimeData`。
- 为拖放对象同时提供 Qt MIME 和 Windows 原生格式。
- 在 Qt Windows 平台插件中添加 Office、Shell 或专用设备数据的转换支持。

## 注册与所有权

转换器应在 `QGuiApplication` 建立后创建。构造函数会把对象注册到 Qt Windows MIME converter 列表，析构函数会自动注销。Qt 负责在 GUI 应用关闭阶段清理已注册的转换器，因此通常不应把同一个对象同时交给其他所有者删除。

头文件明确禁止拷贝。虽然可以在堆上创建派生对象，但一旦注册成功，就要把它看成由 Qt 平台层管理的全局转换器。创建时机过早、在 `QGuiApplication` 销毁后仍使用，都会造成注册表或 COM 环境失效。

## 两个转换方向

从 Qt 到 Windows 时，Qt 依次询问 `canConvertFromMime()`、`formatsForMime()` 和 `convertFromMime()`。前者判断某个 `FORMATETC` 是否可由给定 `QMimeData` 提供，后者列出一个 MIME 类型能导出的 Windows 格式，最终转换函数把数据写入调用方提供的 `STGMEDIUM`。

从 Windows 到 Qt 时，Qt 以目标 MIME 类型询问 `canConvertToMime()`，用 `mimeForFormat()` 把原生格式映射为 MIME 名称，再由 `convertToMime()` 从 `IDataObject` 读取并返回 `QVariant`。`preferredType` 是调用方对返回值类型的偏好，不代表转换器可以忽略真实数据格式。

一个 converter 不必支持所有方向，也不必为所有 MIME 类型返回结果。对于不认识的格式应返回 `false`、空列表或空字符串，让其他 converter 有机会处理。

## COM 数据与内存边界

`FORMATETC` 描述数据格式、介质类型和目标设备；判断时不能只比较 `cfFormat`，还要考虑 `tymed`、`dwAspect` 等字段。`STGMEDIUM` 的填充和释放遵循 COM 所有权规则，尤其是 `HGLOBAL`、`IStream`、`IStorage` 以及 `pUnkForRelease` 的处理。错误地使用栈内存、重复释放或把 Qt 容器指针直接塞进 medium，都可能导致跨边界崩溃。

转换函数通常运行在剪贴板或拖放请求的同步调用链中。不要在里面启动依赖当前转换结果的嵌套事件循环，也不要保存 `IDataObject *`、`STGMEDIUM *` 或 `FORMATETC` 指针供异步使用。需要延迟处理时应复制数据，并明确 COM 接口的引用计数。

## MIME 类型注册

`registerMimeType()` 可把 MIME 字符串注册成 Windows clipboard format ID。返回的 ID 应用于 `FORMATETC::cfFormat`，而不是把 MIME 字符串直接当原生格式名。

Qt 还支持特殊 MIME 形式：

```text
application/x-qt-windows-mime;value="WindowsType"
```

其中 `WindowsType` 是 Windows 格式名称或注册后的格式标识语义。解析和生成时必须保持引号、大小写及格式名约定一致；自定义格式最好使用稳定、带厂商或应用前缀的名称，避免与其他程序冲突。

## 常见误区

- 在 `QGuiApplication` 创建前实例化 converter。
- 手动删除已被 Qt 注册并管理的 converter，造成悬空注册项。
- 只按 `cfFormat` 判断，忽略 `tymed` 和 `dwAspect`。
- 忘记为输出 `STGMEDIUM` 选择正确介质，或没有按 COM 规则交接所有权。
- 在 `convertToMime()` 中返回一个与 `preferredType` 完全不相容的类型，却没有记录转换失败。
- 对未知 MIME/Windows 格式“猜测转换”，导致错误的 converter 抢走请求。
- 异步保存 `IDataObject` 或 `STGMEDIUM` 指针，没有复制数据或增加 COM 引用。
- 把此私有头文件当作跨平台稳定公共 API 使用。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QWindowsMimeConverter()` | 构造并注册一个 Windows MIME converter。 | 应在 `QGuiApplication` 创建后调用；注册生命周期由 Qt 平台层接管。 |
| `virtual ~QWindowsMimeConverter()` | 注销并销毁 converter。 | 不要重复删除；析构前确保没有外部代码继续调用该对象。 |
| `Q_DISABLE_COPY(QWindowsMimeConverter)` | 禁止复制和赋值。 | converter 在注册表中有唯一身份，不能通过复制扩散。 |
| `static int registerMimeType(const QString &mimeType)` | 注册 MIME 类型并返回 Windows clipboard format ID。 | 返回值用于 `FORMATETC::cfFormat`；格式名称应稳定且不冲突。 |
| `virtual bool canConvertFromMime(const FORMATETC &, const QMimeData *) const` | 判断 Qt `QMimeData` 能否导出为指定 Windows 格式。 | 应检查完整 `FORMATETC`，不能只看 MIME 名称。 |
| `virtual QList<FORMATETC> formatsForMime(const QString &, const QMimeData *) const` | 列出某 MIME 类型可提供的 Windows 格式描述。 | 列表应只包含当前数据确实能生成的格式。 |
| `virtual bool convertFromMime(const FORMATETC &, const QMimeData *, STGMEDIUM *) const` | 将 Qt 数据写入调用方提供的 COM medium。 | 正确填充 `tymed`、句柄和释放语义；失败时不要留下半初始化数据。 |
| `virtual bool canConvertToMime(const QString &, IDataObject *) const` | 判断 Windows `IDataObject` 是否可转换成目标 MIME 类型。 | 需要查询数据对象可提供的格式和介质。 |
| `virtual QString mimeForFormat(const FORMATETC &) const` | 把 Windows 原生格式映射为 Qt MIME 字符串。 | 不认识的格式返回空字符串，让其他 converter 继续尝试。 |
| `virtual QVariant convertToMime(const QString &, IDataObject *, QMetaType preferredType) const` | 从 Windows 数据对象读取数据并返回 Qt 值。 | 需尊重可用格式和 `preferredType`；失败时返回无效 `QVariant`。 |
| `FORMATETC` | 描述 clipboard format、介质类型、aspect 和目标设备。 | `cfFormat`、`tymed`、`dwAspect` 要整体匹配。 |
| `STGMEDIUM` | 承载 COM 数据及其释放信息。 | 遵循 COM 所有权；不要把临时内存地址交给调用方。 |
| `IDataObject *` | Windows 剪贴板/拖放数据对象接口。 | 仅在当前同步调用链中使用；跨线程或异步需处理 COM 引用和数据复制。 |

## 一句话总结

`QWindowsMimeConverter` 是 Qt Windows 平台的 COM/MIME 适配点：先准确声明格式能力，再按 COM 规则转换和交接数据。
