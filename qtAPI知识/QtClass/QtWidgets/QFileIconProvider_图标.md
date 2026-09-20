# Qt QFileIconProvider 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QFileIconProvider>`
> 所属模块：`Qt6::Widgets`
> 继承：`QAbstractFileIconProvider`

## 它解决什么问题

`QFileIconProvider` 根据文件系统对象的类别或 `QFileInfo` 返回适合当前平台的 `QIcon`。它解决的是“文件浏览界面应该显示什么图标”的问题，而不是让应用自己根据扩展名硬编码图标。

在 Windows 上，返回结果可能来自 shell 图标；在其他桌面环境中，可能来自图标主题或平台实现。这样自定义文件列表、附件面板、最近文件菜单和资源管理器式界面就能更接近用户熟悉的系统外观。

`QFileSystemModel` 已经内置文件图标处理。只有在你自建模型、脱离 model/view 单独查询图标，或需要定制 provider 行为时，才通常直接使用 `QFileIconProvider`。

## 实际使用场景

- 自定义文件树或文件表格，需要给每行路径显示系统图标。
- 附件列表只保存了路径，但希望区分文件、目录、磁盘等对象。
- “打开最近文件”菜单中想给不同文件类型显示平台一致的图标。
- 大型文件浏览器中想禁用目录自定义图标以降低网络路径开销。

## 两个图标查询入口

`icon(QAbstractFileIconProvider::IconType type)` 按抽象类别返回图标，例如 `Folder`、`File`、`Drive`、`Trashcan`。它不需要实际路径，适合固定入口或虚拟节点。

`icon(const QFileInfo &info)` 按真实文件信息返回图标。平台实现可以根据目录属性、扩展名、系统关联、图标主题等信息决定结果。文件不存在时，也可能根据路径后缀返回一个通用图标，但不要把它当成文件存在性检查。

## 性能与边界

文件图标查询在某些平台和路径上并不便宜。网络目录、慢速磁盘、带自定义图标的目录都可能造成额外开销。对于大量文件列表，建议复用 provider，并把结果缓存到模型数据或图标缓存中。

从 `QAbstractFileIconProvider` 继承的 `DontUseCustomDirectoryIcons` 选项可以跳过目录自定义图标查询。目录很多或路径在网络上时，这通常更稳。

`QFileIconProvider` 不读取文件内容，不判断文件是否能打开，不负责 MIME 嗅探，也不保证每种扩展名都有独立图标。它是平台图标查询器，不是文件类型数据库。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFileIconProvider::QFileIconProvider()` | 创建文件系统图标 provider。 | 可以复用一个实例查询多个文件，避免高频重复创建。 |
| 析构 | `QFileIconProvider::~QFileIconProvider()` | 销毁 provider。 | 不拥有传入的 `QFileInfo`；已返回的 `QIcon` 按值类型使用。 |
| 图标查询 | `QIcon icon(QAbstractFileIconProvider::IconType type) const` | 按通用类别返回系统图标。 | 适合 `Folder`、`File`、`Drive` 等没有具体路径的节点。 |
| 图标查询 | `QIcon icon(const QFileInfo &info) const` | 按文件或目录信息返回平台图标。 | 结果依赖平台、路径和扩展名；网络路径可能有额外成本。 |
| 继承选项 | `void setOptions(QAbstractFileIconProvider::Options options)` | 设置 provider 查询策略。 | `DontUseCustomDirectoryIcons` 可减少目录图标查询开销。 |
| 继承查询 | `QAbstractFileIconProvider::Options options() const` | 返回当前查询选项。 | 用于确认是否启用了性能相关限制。 |
| 继承枚举 | `QAbstractFileIconProvider::IconType` | 描述通用文件系统对象类别。 | 常用值包括 `Computer`、`Desktop`、`Trashcan`、`Network`、`Drive`、`Folder`、`File`。 |
| 继承标志 | `QAbstractFileIconProvider::Option` | 控制图标提供策略。 | 当前最常见的是跳过目录自定义图标。 |

## 一句话总结

`QFileIconProvider` 是系统文件图标的查询入口：给它文件信息或文件系统类别，它返回适合当前平台文件界面的 `QIcon`。
