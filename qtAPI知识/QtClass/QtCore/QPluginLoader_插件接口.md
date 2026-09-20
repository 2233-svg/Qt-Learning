# QPluginLoader：运行时装入 Qt 插件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPluginLoader>`  
> 模块：`Qt6::Core`  
> 继承：`QObject`  
> 相关类型：`QLibrary`、`QStaticPlugin`、`QJsonObject`、`QCoreApplication`

`QPluginLoader` 是 Qt 插件的运行时加载器。它面向的不是任意 DLL / `.so`，而是由 Qt 插件机制构建、带有 Qt 元数据和根 `QObject` 的共享库。它负责检查 Qt 版本兼容性、读取插件元数据、创建插件根对象，以及在条件允许时卸载插件。

## 它解决什么问题

应用需要把某项能力做成可替换、可扩展的模块时，通常不希望主程序在编译期依赖每个实现。例如：

- 图像编辑器按需发现导入/导出格式插件；
- 工业软件从指定目录加载设备驱动适配器；
- 公司内部工具按产品版本部署不同的数据源、报表或算法实现；
- 宿主程序先读取插件声明的能力、版本或协议，再决定是否创建它。

若只需从动态库解析一个 C 函数，使用 `QLibrary` 更直接。`QPluginLoader` 的额外价值在于：它加载的是 Qt 插件，能取得插件导出的根 `QObject`，并通过 `qobject_cast()` 转成双方约定好的 C++ 接口。

## 使用前提与范围

动态加载这一组成员仅在 Qt 构建时启用了 `library` 特性时可用。若应用**静态链接 Qt**，不能用 `QPluginLoader` 加载动态 Qt 插件；插件也应静态链接，并通过 `Q_IMPORT_PLUGIN` / `staticInstances()` 等静态插件接口接入。静态 Qt 程序若确实要加载普通动态库，可以考虑 `QLibrary`，但那不是动态 Qt 插件机制。

一个插件必须由 Qt 插件宏导出元数据和工厂。宿主与插件还必须共享同一份稳定的接口声明；不要把仅在某一方可见的普通 C++ 基类强转为插件接口。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(host PRIVATE Qt6::Core)
```

## 最小使用模型

先在宿主和插件共同使用的头文件中声明接口。`Q_DECLARE_INTERFACE` 提供给 `qobject_cast()` 用来确认接口身份；接口 ID 是跨版本契约，发布后不应随意改动。

```cpp
// textconverterinterface.h
#pragma once

#include <QString>
#include <QtPlugin>

class TextConverterInterface
{
public:
    virtual ~TextConverterInterface() = default;
    virtual QString name() const = 0;
    virtual QString convert(const QString &input) = 0;
};

#define TextConverterInterface_iid "org.example.TextConverterInterface/1.0"
Q_DECLARE_INTERFACE(TextConverterInterface, TextConverterInterface_iid)
```

插件实现以 `QObject` 为根对象，并用 `Q_PLUGIN_METADATA` 写入 IID 和可选 JSON 文件：

```cpp
class UppercaseConverter final : public QObject, public TextConverterInterface
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID TextConverterInterface_iid FILE "uppercase.json")
    Q_INTERFACES(TextConverterInterface)

public:
    QString name() const override { return "uppercase"; }
    QString convert(const QString &input) override { return input.toUpper(); }
};
```

宿主装入并取得接口的典型写法如下。`instance()` 已经会隐式调用 `load()`，所以这里不必先调用 `load()`。

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QPluginLoader>

QPluginLoader loader(
    QCoreApplication::applicationDirPath() + "/plugins/uppercase");

QObject *root = loader.instance();
if (!root) {
    qWarning() << "Cannot load plugin:" << loader.errorString();
    return;
}

auto *converter = qobject_cast<TextConverterInterface *>(root);
if (!converter) {
    qWarning() << "Plugin does not implement TextConverterInterface";
    loader.unload();
    return;
}

qDebug() << converter->name() << converter->convert("Qt Plugin");
// converter/root 的指针只在插件保持加载时有效。
// 不再使用时不手动 delete root；需要尽早释放则调用 unload()。
loader.unload();
```

这里的调用顺序是：指定文件 -> 可选读取元数据 -> `instance()` / `load()` -> `qobject_cast()` 校验接口 -> 使用接口 -> 停止持有接口指针 -> 可选 `unload()`。失败时查看 `errorString()`，不要只凭空指针猜测原因。

## 文件名、搜索路径与部署

`fileName` 是插件文件名，而不是插件 IID。

- 推荐省略库后缀，例如 Windows 使用 `".../myplugin"` 而非手写 `.dll`；Qt 会按平台补全可加载库的后缀。
- 若名称不是绝对路径，加载器会在 `QCoreApplication::libraryPaths()` 的各目录中搜索。
- 绝对路径绕过这套搜索；用于只允许加载安装目录下某个确定插件的场景。
- 成功加载后，`fileName()` 返回解析后的完整文件名；给出的文件不存在时，属性保持空字符串。
- `libraryPaths()` 应在构造 `QCoreApplication` 后再依赖。应用可执行文件目录、Qt 插件目录、`qt.conf` 与 `QT_PLUGIN_PATH` 都可能影响它。

对于自有插件目录，通常应显式使用绝对路径或在应用启动后调用 `QCoreApplication::addLibraryPath()`。不要把可被低权限用户写入的目录加入插件搜索路径；加载插件等同于在进程内执行该库代码。

## 元数据先筛选，加载后执行

`metaData()` 返回插件在编译时由 `Q_PLUGIN_METADATA` 嵌入的 JSON 对象。它无需装入 DLL / `.so`，适合扫描目录时按 IID、能力集、协议版本、厂商 ID 等字段筛选候选项。

```cpp
QPluginLoader candidate(pluginPath);
const QJsonObject meta = candidate.metaData();

if (meta.value("IID").toString() != TextConverterInterface_iid)
    return;

const QJsonObject data = meta.value("MetaData").toObject();
if (data.value("apiVersion").toInt() != 1)
    return;

QObject *root = candidate.instance(); // 仅对通过筛选的候选项加载
```

元数据是优化加载决策的声明，不是安全验证。攻击者若能替换插件文件，也能伪造 JSON；真正的安全边界是可信安装位置、文件权限、签名/包完整性校验和最小化搜索路径。

## 装载、根对象与卸载的生命周期

`QPluginLoader` 对象、插件根对象和共享库的寿命彼此相关但不相同：

1. `load()` 只装入库；它不要求立即创建根对象。
2. `instance()` 会在必要时装入库并创建插件根 `QObject`。
3. 根对象由插件加载机制管理。**不要对 `instance()` 返回值调用 `delete`**。
4. 销毁某个 `QPluginLoader` 不会自动把插件库从内存卸掉；若未显式 `unload()`，通常会留到进程结束。
5. 最后一次实际卸载之前，Qt 会删除根对象。之后从该插件取得的接口指针、`QObject *`、函数指针都不可再访问。

同一个物理插件可被多个 `QPluginLoader` 对象引用。一个 loader 调用 `unload()` 时，若还有其他 loader 正在使用同一库，调用会失败；只有全部 loader 都请求卸载后，才可能真正卸载。因此插件返回给宿主的对象、线程、定时器或全局回调应当能在卸载前彻底停止，否则运行时库可能仍有活动引用。

`instance()` 若发现此前的根对象已经被销毁，会创建新的根对象。不要把“同一插件只会有一个永久单例”作为设计前提。

## `loadHints`：默认不会真正卸载

`loadHints` 使用 `QLibrary::LoadHints`。从 Qt 5.7 起，`QPluginLoader` 默认设置 `QLibrary::PreventUnloadHint`，它阻止库在调用 close / `unload()` 后离开进程地址空间；此时库的静态变量也不会在后续再加载时重新初始化。

这带来一个容易忽略的边界：

- `unload()` 仍负责释放根组件、解除该 loader 的使用关系，并返回是否成功；
- 但带着 `PreventUnloadHint` 时，不应把它理解成“DLL 一定已经从进程移除”；
- 需要可重复的真卸载/重载语义时，在首次 `load()` 前清除该 hint，并设计好所有跨库对象、线程和回调的收尾；
- `setLoadHints()` 应在加载前调用。库已加载后再修改不会影响本次加载；同一底层库的 loader 会共享装载提示，不应让不同使用方对 hints 做互相矛盾的设置。

各 hint 的意义来自 `QLibrary`：`ResolveAllSymbolsHint` 要求加载时解析全部符号；`ExportExternalSymbolsHint` 让后续加载的库可解析其外部符号；`LoadArchiveMemberHint` 支持指向归档库内对象；`DeepBindHint` 仅 Linux 支持，优先使用被加载库自己的符号定义。它们属于平台链接器策略，不是普通插件功能开关。

## 线程与错误处理

Qt 文档将 `QPluginLoader` 标为可重入（reentrant）：不同 loader 实例可在不同线程中并发使用。它不表示同一个 `QPluginLoader` 可由多线程同时读写；将一个 loader 及其根对象限制在明确的所有者线程，跨线程时用同步策略或队列调用。

插件根对象是 `QObject`，仍遵循 QObject 的线程亲和性。若插件启动了工作线程，卸载前应让它们退出并等待结束；尤其不要让其他线程在 `unload()` 后继续调用接口或投递事件给根对象。

`errorString()` 返回最近一次错误的文本描述。它适合记录日志和排查，不适合作为稳定的程序分支协议；程序逻辑应依赖 `load()` / `unload()` 的布尔结果、`instance()` 是否为空，以及接口投射是否成功。

## 动态插件与静态插件

| 模式 | 发现与装入方式 | 适用情形 |
| --- | --- | --- |
| 动态 Qt 插件 | `QPluginLoader(fileName)`、`metaData()`、`instance()` | 可在部署后增减插件；需要谨慎控制搜索路径与 ABI/接口版本。 |
| 静态 Qt 插件 | 链接插件目标，使用 `Q_IMPORT_PLUGIN` 注册，再查 `staticInstances()` / `staticPlugins()` | 静态 Qt、嵌入式或希望将所有代码随主程序部署。 |
| 普通动态库 | `QLibrary` + `resolve()` | 库不是 Qt 插件，或只需导出 C/C++ 符号。 |

`Q_IMPORT_PLUGIN(PluginName)` 是静态插件的常用入口。`qRegisterStaticPluginFunction(QStaticPlugin)` 是它使用的底层注册函数；应用代码通常不直接调用。`staticPlugins()` 返回含元数据的 `QStaticPlugin` 列表，`staticInstances()` 则返回已经持有的静态插件根对象列表。

## 常见错误

### 把 `QPluginLoader` 当作任意动态库加载器

库若没有 Qt 插件元数据和根对象，`instance()` 不能提供所需对象。解析普通导出符号请改用 `QLibrary`。

### 只检查 `instance()`，不检查接口

拿到根 `QObject` 只说明插件根对象创建成功，不说明它实现了当前业务接口。必须用 `qobject_cast<ExpectedInterface *>()`；返回空指针时不要继续强转调用。

### 手动删除根对象

这会破坏 loader 对根组件的生命周期管理，且可能使其他仍持有接口指针的代码悬空。停止使用后调用 `unload()`，或让进程退出时由 Qt 清理。

### 以为析构 loader 就会卸载库

析构默认不会主动卸载插件。需要提前释放根对象和关联资源时显式调用 `unload()`，并接受同一库仍被其他 loader 使用时会失败。

### 在加载后再改 `loadHints`

已打开的动态库不会按新提示重新装载。所有需要影响链接行为的 hints 都应在 `load()` 或 `instance()` 之前设置。

### 从不可信目录自动扫描并加载

扫描目录和加载是两件事：可先读 metadata 做功能筛选，但不要把 metadata 当成信任证明。插件库拥有与宿主相同的进程权限。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QPluginLoader(QObject *parent = nullptr)` | 创建尚未指定插件的 loader。 | 之后以 `setFileName()` 指定文件；`parent` 只管理 loader 本身，不等于管理插件根对象。 |
| `QPluginLoader(const QString &fileName, QObject *parent = nullptr)` | 创建并指定插件文件名。 | 不代表已加载；后缀可省略。相对路径按 `libraryPaths()` 搜索，绝对路径直接定位。 |
| `~QPluginLoader()` | 销毁 loader 对象。 | 若未显式 `unload()`，插件通常继续留在内存至进程结束。不要据此判断根对象或库已释放。 |
| `setFileName(const QString &fileName)` | 设置插件文件名。 | 文件不存在时文件名不会被设置，属性会是空字符串；应在加载前设置。 |
| `fileName() const` | 取得当前插件文件名。 | 成功加载后返回完整解析路径；默认和无效文件名情形为 `QString()`。 |
| `setLoadHints(QLibrary::LoadHints hints)` | 设置动态库装载提示。 | 必须在第一次 `load()` / `instance()` 前设置；同一物理库的 loader 会共享 hints。 |
| `loadHints() const` | 读取当前装载提示。 | 默认含 `QLibrary::PreventUnloadHint`；它影响是否真正从地址空间卸载。 |
| `bool load()` | 显式装入插件库。 | 成功返回 `true`；不需要根对象时可预加载。调用 `instance()` 已会隐式执行此步骤。 |
| `bool isLoaded() const` | 查询库是否已加载。 | 只反映加载状态，不保证接口匹配，也不表示已取得或仍持有业务对象。 |
| `QObject *instance()` | 获取插件根对象。 | 必要时隐式加载；失败返回 `nullptr`。根对象被销毁后再次调用可创建新对象；返回值不可手动删除。 |
| `QJsonObject metaData() const` | 获取嵌入的插件 JSON 元数据。 | 不加载库即可读取，适合预筛选；数据来自 `Q_PLUGIN_METADATA`，不能作为安全信任依据。 |
| `bool unload()` | 请求解除 loader 对插件的使用并卸载。 | 最后一个 loader 才可能真正卸载；卸载前 Qt 删除根对象。默认 `PreventUnloadHint` 下库未必离开地址空间。 |
| `QString errorString() const` | 读取最近一次错误描述。 | 用于日志与诊断；以返回值、空指针和接口投射结果决定控制流。 |
| `static QObjectList staticInstances()` | 返回静态插件的根对象列表。 | 用于静态链接场景；通常先由 `Q_IMPORT_PLUGIN` 使插件被注册。 |
| `static QList<QStaticPlugin> staticPlugins()` | 返回静态插件描述列表。 | 相比 `staticInstances()` 还可取得 `QStaticPlugin` 中的元数据。 |
| `void qRegisterStaticPluginFunction(QStaticPlugin plugin)` | 向 loader 注册一个静态插件。 | `Q_IMPORT_PLUGIN` 所用的底层函数；通常不在业务代码里直接调用。 |

## 一句话总结

`QPluginLoader` 是“取得 Qt 插件根对象”的运行时入口：用 `metaData()` 先筛选，用 `instance()` 加载并以 `qobject_cast()` 验证接口，把接口指针的寿命严格限制在插件保持加载的期间。
