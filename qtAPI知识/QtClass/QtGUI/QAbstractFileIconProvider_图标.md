# Qt QAbstractFileIconProvider 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractFileIconProvider>`  
> 所属模块：`Qt6::Gui`  
> 基类：无；不是 `QObject`  
> 定位：为文件系统视图提供图标与用户可见类型文本的策略接口

## 1. 它解决什么问题

`QAbstractFileIconProvider` 把“某个文件系统对象应该显示什么图标、应该显示什么类型名称”抽象成一个可替换的策略。最常见的使用者是 `QFileSystemModel`：模型负责枚举目录、读取文件信息和提供模型数据，图标提供器负责把 `QFileInfo` 转换成 `QIcon` 与展示文本。

它解决的不是文件访问问题，也不是目录树模型问题：

- 不负责打开、复制、删除或监视文件；
- 不负责枚举目录；
- 不把图标资源写回文件系统；
- 不提供稳定的机器类型判定；
- 只负责显示层使用的图标和类型字符串。

当应用需要统一品牌图标、替换系统默认图标、为特殊扩展名提供业务图标，或者在远程/可移动目录上禁用昂贵的自定义目录图标查找时，可以继承这个类并覆盖虚函数。

## 2. 典型使用场景

### 2.1 给文件系统模型换一套图标

```cpp
class ProjectIconProvider final : public QAbstractFileIconProvider
{
public:
    QIcon icon(const QFileInfo &info) const override
    {
        if (info.isDir())
            return QIcon(":/icons/folder-project.svg");
        if (info.suffix().compare("cpp", Qt::CaseInsensitive) == 0)
            return QIcon(":/icons/file-cpp.svg");
        return QAbstractFileIconProvider::icon(info);
    }

    QString type(const QFileInfo &info) const override
    {
        if (info.suffix().compare("cpp", Qt::CaseInsensitive) == 0)
            return QStringLiteral("C++ 源文件");
        return QAbstractFileIconProvider::type(info);
    }
};
```

如果把 provider 交给 `QFileSystemModel`，应按照 `QFileSystemModel::setIconProvider()` 的所有权规则管理它；独立调用时则由创建者负责其生命周期。provider 自身不拥有传给 `icon(const QFileInfo &)` 或 `type(const QFileInfo &)` 的 `QFileInfo`。

### 2.2 在自定义文件列表中直接使用

```cpp
QAbstractFileIconProvider provider;
QFileInfo info(path);

item->setIcon(provider.icon(info));
item->setText(provider.type(info));
```

这种用法适合已有自己的列表模型、资源管理器或导入面板的应用。需要注意：默认实现的具体图标和文本来自平台风格与 Qt 实现，不能把它们当成跨平台固定输出。

## 3. 设计与生命周期

### 3.1 不可拷贝，也不拥有外部对象

类声明了 `Q_DISABLE_COPY`，不能复制或赋值。它内部有私有实现指针，但这不改变它的策略对象身份。

`QFileInfo` 以 `const` 引用传入，调用期间必须有效；provider 不保存它的引用。返回的 `QIcon` 和 `QString` 是值类型，调用者可以保存返回值。

### 3.2 查询函数可能被高频调用

文件系统模型在刷新目录、滚动视图、排序或重新取数据时可能反复询问图标和类型。覆盖函数时应：

- 避免网络访问、进程启动和长时间磁盘扫描；
- 不要在 `icon()` 中修改模型或触发递归刷新；
- 对昂贵的扩展名判断、主题资源查找和自定义元数据查询做缓存；
- 对无权限、文件已被删除或信息不完整的 `QFileInfo` 给出可接受的回退。

如果图标暂时无法生成，返回默认构造的空 `QIcon` 是合法结果；视图通常会显示空白或使用自己的回退策略。

### 3.3 `type()` 不是类型判定 API

`type()` 返回给用户看的标签，例如“文件夹”“文本文件”或平台本地化文本。它可能受操作系统、文件关联、语言环境和 Qt 平台插件影响。不要用它判断是否为目录、是否为某种扩展名或是否可以执行；机器判断应使用 `QFileInfo::isDir()`、`suffix()`、权限和实际格式检测。

## 4. 成员类型

### `enum IconType`

表示没有具体 `QFileInfo` 时请求的系统对象图标：

| 枚举值 | 典型对象 | 说明 |
| --- | --- | --- |
| `Computer` | “此电脑”或计算机根对象 | 用于文件系统浏览器的计算机入口。 |
| `Desktop` | 桌面目录 | 具体图标由平台决定。 |
| `Trashcan` | 回收站/废纸篓 | 不保证所有平台都提供非空图标。 |
| `Network` | 网络位置 | 可能没有平台对应资源。 |
| `Drive` | 磁盘或卷 | 用于驱动器入口。 |
| `Folder` | 普通文件夹 | 不代表某个具体目录的自定义图标。 |
| `File` | 普通文件 | 最一般的文件回退图标。 |

不要依赖枚举数值，也不要假设每个平台都为每个值提供图标。

### `enum Option`

#### `DontUseCustomDirectoryIcons`

要求 provider 不为目录查找自定义目录图标。它主要用于减少网络盘、可移动介质或包含大量目录的路径上的额外查找成本。该选项只影响目录图标策略，不会禁止所有目录图标，也不影响文件内容访问。

### `using Options = QFlags<Option>`

选项的位标志类型。可以使用 `|` 组合：

```cpp
provider.setOptions(QAbstractFileIconProvider::DontUseCustomDirectoryIcons);
```

当前 Qt 版本只有一个公开选项，但代码应按 flags 语义编写，不要把它当作布尔值或依赖具体整数值。

## 5. 逐项 API 说明

### `QAbstractFileIconProvider()`

构造一个默认 provider。默认实现使用 Qt 平台相关的图标和类型策略。构造本身不会扫描目录，也不会绑定模型或资源管理器。

### `virtual ~QAbstractFileIconProvider()`

虚析构函数，允许通过 `QAbstractFileIconProvider *` 安全销毁派生类。它不负责销毁传入过的 `QFileInfo`，也不负责清理应用资源系统中的图标资源。

### `virtual QIcon icon(IconType type) const`

根据抽象系统对象类型返回图标。适合请求 `Folder`、`Drive`、`Trashcan` 等没有具体路径的对象。

边界：

- 返回空 `QIcon` 是允许的；
- 不同平台的图标外观、尺寸和是否支持某个类型都可能不同；
- 该重载不读取某个具体路径，也不能反映目录是否存在；
- 派生类只需要覆盖自己关心的类型，其他类型可调用基类实现。

### `virtual QIcon icon(const QFileInfo &info) const`

根据具体文件系统信息返回图标。默认实现通常会区分文件与目录，并尝试使用平台或文件关联信息。

`QFileInfo` 只在调用期间借用。`info` 可能代表已经不存在的路径、权限不足的路径、符号链接或尚未刷新完整元数据的对象；覆盖实现应定义合理回退，不要假设 `exists()` 永远为真。

对符号链接、目录自定义图标和特殊文件的具体表现属于平台实现细节。若业务必须稳定区分它们，应先使用 `QFileInfo` 自己判断，再选择资源。

### `virtual QString type(const QFileInfo &info) const`

返回适合显示给用户的文件类型名称。结果可能本地化，可能由扩展名关联或平台 shell 规则决定。

不要把返回值用于协议字段、持久化格式或逻辑分支。若需要固定标签，应在派生类中明确返回自己的字符串；若需要机器判定，应直接检查 `QFileInfo` 和文件内容。

### `virtual void setOptions(Options options)`

设置 provider 的行为选项。默认实现至少支持 `DontUseCustomDirectoryIcons`。

这是 provider 状态的修改操作。应在把 provider 交给模型前完成设置，避免模型已经开始查询时改变显示策略。该类不是 `QObject`，没有信号通知选项变化；更改后通常需要由使用者刷新模型或视图。

### `virtual Options options() const`

返回当前设置的选项 flags。可以用 `testFlag()` 查询：

```cpp
if (provider.options().testFlag(
        QAbstractFileIconProvider::DontUseCustomDirectoryIcons)) {
    // 当前不查找目录自定义图标
}
```

## 6. 覆盖函数时的实践边界

### 6.1 先处理业务特例，再回退到基类

基类实现包含平台集成和默认本地化策略。派生类不必重写所有函数：

```cpp
QIcon ProjectIconProvider::icon(const QFileInfo &info) const
{
    const QString suffix = info.suffix().toCaseFolded();
    if (suffix == u"project")
        return QIcon(":/icons/project-file.svg");
    return QAbstractFileIconProvider::icon(info);
}
```

### 6.2 不要把展示策略和文件格式解析混在一起

如果要根据文件内容选择图标，最多读取已经缓存的元数据；不要在每次 `icon()` 查询中打开并解析整个文件。更适合在模型层预先计算角色数据，或者在后台任务完成后通知模型刷新。

### 6.3 线程与 GUI 资源

provider 本身不是 `QObject`，但 `QIcon` 可能引用平台主题、插件或 GUI 资源。通常应在 GUI 线程中配合视图使用；不要把一个可变 provider 同时交给多个线程调用并修改。若确实要后台预计算，缓存稳定的资源标识或值对象，并在 GUI 线程完成视图更新。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 类型 | `IconType` | 表示计算机、桌面、驱动器、文件夹等抽象对象。 | 不依赖枚举数值；平台可能返回空图标。 |
| 类型 | `Option` | 表示 provider 的行为选项。 | 当前公开选项是目录自定义图标开关。 |
| 类型 | `Options` | `QFlags<Option>` 位标志容器。 | 用 `testFlag()` 和 flags 运算。 |
| 生命周期 | `QAbstractFileIconProvider()` | 创建默认图标 provider。 | 不绑定模型，不扫描目录。 |
| 生命周期 | `~QAbstractFileIconProvider()` | 虚析构派生 provider。 | 不拥有外部 `QFileInfo`。 |
| 图标 | `icon(IconType)` | 返回抽象系统对象图标。 | 具体平台可能不支持某项。 |
| 图标 | `icon(const QFileInfo &)` | 返回具体路径对象图标。 | 输入只借用；可能文件不存在或权限不足。 |
| 文本 | `type(const QFileInfo &)` | 返回用户可见类型名称。 | 不能用于机器判断，可能本地化。 |
| 配置 | `setOptions(Options)` | 设置显示策略选项。 | 设置后没有信号；模型可能需要刷新。 |
| 配置 | `options()` | 查询当前选项。 | 返回 flags，不是单个布尔值。 |

### 一句话总结

`QAbstractFileIconProvider` 是文件系统视图的显示策略接口：用 `icon()` 提供图像、用 `type()` 提供人类可读标签、用 `Options` 控制目录图标查找成本；它不访问文件内容，也不替代 `QFileInfo` 的机器判定能力。
