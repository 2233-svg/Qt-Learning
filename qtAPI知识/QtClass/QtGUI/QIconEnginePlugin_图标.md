# QIconEnginePlugin：按文件后缀动态提供图标引擎

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QIconEnginePlugin>`  
> 继承：`QObject`

## 它解决什么问题

`QIconEnginePlugin` 把自定义 `QIconEngine` 接入 Qt 的动态插件系统。应用只需创建 `QIcon("logo.myicon")` 或 `icon.addFile(":/assets/logo.myicon")`，Qt 根据文件或资源名的后缀找到相应插件，再由插件创建处理该资源的图标引擎。

它把“如何发现某种图标格式”与“如何绘制该格式”分开：

- `QIconEnginePlugin`：声明支持哪些后缀，并创建引擎；
- `QIconEngine`：保存资源状态、选择尺寸/状态并进行实际绘制；
- `QIcon`：对控件和应用提供统一值类型接口。

普通应用不应继承它。只有要为第三方图标格式或专有后缀提供系统级可发现性时，才需要写插件。

## 实际使用场景

- 为企业专有 `.brandicon` 文件提供图标加载和渲染。
- 将压缩、加密或包内图标格式暴露给 `QIcon`。
- 为程序化矢量格式提供按尺寸、DPR、状态生成图标的后端。
- 将自定义引擎随应用部署，避免在业务代码中手工判断后缀。

不适合处理单个应用内部的一组固定资源。资源路径、SVG 或直接构造 `QIconEngine` 往往更简单；插件会引入部署、加载路径、ABI 和版本兼容成本。

## 插件结构

插件类需要继承 `QIconEnginePlugin`、实现 `create()`，并用 `Q_PLUGIN_METADATA` 导出元数据：

```cpp
#include <QIconEnginePlugin>

class BrandIconPlugin final : public QIconEnginePlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QIconEngineFactoryInterface_iid
                      FILE "brandicon.json")

public:
    QIconEngine *create(const QString &fileName) override
    {
        return new BrandIconEngine(fileName);
    }
};
```

`brandicon.json` 的关键字段是 `Keys`：

```json
{
  "Keys": [ "brandicon" ]
}
```

键就是支持的文件或资源名后缀，大小写不敏感；不要带点，例如写 `"brandicon"` 而不是 `".brandicon"`。

`QIconEngineFactoryInterface_iid` 由 Qt 头文件提供，避免手写 IID 字符串发生拼写或版本错误。

## 创建流程

当 `QIcon` 首次以某个文件或资源名创建或添加资源时，Qt 使用后缀查询图标引擎插件。找到匹配插件后，插件加载器构造插件对象并调用：

```cpp
QIconEngine *create(const QString &filename = QString()) override;
```

`filename` 是触发引擎创建的文件或资源名。`create()` 应返回一个全新的、可用的堆分配引擎；后续由 `QIcon` 管理该引擎的所有权。

引擎创建失败时可返回 `nullptr`，但应让调用路径安全地得到空或不可用图标，而不是返回半初始化对象后在 `paint()` 时崩溃。若格式支持只取决于后缀，解析和 I/O 可延迟到引擎第一次被请求绘制时；若在 `create()` 立即验证文件，必须处理文件不存在和资源路径等失败情况。

## 后缀匹配与元数据边界

`Keys` 只是一种**格式发现声明**，不是文件内容校验。比如声明 `"brandicon"` 后，任何同后缀路径都有机会进入 `create()`，引擎仍必须检查文件头、版本、长度、校验和或解密结果。

同一个后缀与多个插件发生冲突时，应用不应依赖“某个插件恰好先被加载”的顺序。专有格式应使用足够特异的后缀，并在部署时避免并存冲突插件。

图标引擎插件对应 Qt 的 `iconengines` 插件类别，插件动态库必须位于 Qt 能发现的插件搜索路径中，或被作为静态插件显式导入。仅仅编译出一个 DLL、SO 或 dylib 并不等于运行时一定能找到它。

## 插件与引擎的所有权

插件对象由 Qt 插件加载器构造，构造函数的 `parent` 通常由加载器提供。应用代码一般不手工 `new`、`delete` 或调用插件析构函数；Qt 在插件不再使用时负责销毁和卸载。

而 `create()` 返回的 `QIconEngine *` 是不同的所有权层次：它将被 `QIcon` 接管。不要给引擎设置插件对象作为 `QObject` 父对象，因为 `QIconEngine` 不是 `QObject`，也不要让插件持有会在图标仍在使用时销毁的独占引擎指针。

引擎内部若引用插件库中的代码或静态数据，必须确保 Qt 不会在引擎仍活着时卸载插件。遵守 Qt 的插件加载路径和 `QIcon` 所有权模型，避免用外部 `QLibrary` 强制提前卸载模块。

## 线程与 GUI 资源

插件发现和引擎创建最终服务于 `QIcon`。如果引擎使用 `QPixmap`、`QPainter`、主题图标或平台资源，实际渲染应遵守 GUI 线程边界。后台解析可以先产生纯数据或 `QImage`，随后在 GUI 线程生成 `QPixmap`。

插件对象继承 `QObject`，但不意味着所有引擎操作可以任意跨线程调用。应把插件的线程归属、引擎的资源缓存和 `QIcon` 的使用线程设计为一致的模型。

## 部署与兼容性

图标引擎插件是二进制扩展。发布时应验证：

- 插件与宿主使用相同兼容的 Qt 主版本、编译器和构建模式；
- 依赖的第三方库随插件一同部署；
- 插件目录位于运行时搜索路径；
- 资源后缀和 JSON `Keys` 完全匹配；
- 在干净机器上通过实际 `QIcon` 路径测试，而不只加载 `QLibrary`。

插件中不要把业务 UI、长期网络请求或阻塞解码塞进 `create()`。`QIcon` 可能在控件首次绘制时被频繁请求，耗时策略应放在可缓存、可取消或可延迟的引擎实现中。

## 常见错误

- 忘记 `Q_PLUGIN_METADATA`，导致 Qt 无法发现插件。
- JSON 中漏掉 `Keys`，写成带点后缀，或与实际文件后缀不一致。
- 认为 `Keys` 会验证文件内容，未在引擎中解析和校验格式。
- 从 `create()` 返回栈对象、共享的同一引擎指针或半初始化引擎。
- 手工销毁由插件加载器管理的插件实例。
- 忘记部署到 `iconengines` 类别的可发现路径。
- 让不同插件声明相同通用后缀，依赖加载顺序。
- 在 `create()` 中做阻塞网络 I/O 或创建 GUI pixmap 的工作线程调用。
- 假定运行时插件可在仍有 `QIcon` 使用其引擎时安全卸载。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 宏常量 | `QIconEngineFactoryInterface_iid` | 图标引擎工厂插件的 IID；传给 `Q_PLUGIN_METADATA`，不要手写替代字符串。 |
| 构造 | `QIconEnginePlugin(QObject *parent = nullptr)` | 构造插件对象；通常由 Qt 插件加载器自动调用。 |
| 析构 | `virtual ~QIconEnginePlugin()` | 虚析构；通常由 Qt 在插件不再使用时管理，应用无需显式调用。 |
| 工厂 | `virtual QIconEngine *create(const QString &filename = QString()) = 0` | 必须实现；为给定文件或资源名创建新的引擎，返回指针的所有权转给 `QIcon` 使用路径。 |
| 元数据 | `Q_PLUGIN_METADATA(IID ... FILE "...json")` | 导出插件并嵌入 JSON 元数据；没有它，动态发现不会发生。 |
| 元数据 | `Keys` | JSON 后缀列表，大小写不敏感；使用不带点的后缀字符串。 |
| 继承 | `QObject` | 插件对象可有 parent，但不等于其创建的 `QIconEngine` 使用 QObject 所有权。 |

## 相关类

- `QIconEngine`：插件要创建的实际渲染后端。
- `QIcon`：按文件或资源后缀触发引擎发现和使用。
- `QPluginLoader`：通用 Qt 动态插件加载机制。
- `QIconEngine::ScaledPixmapArgument`：自定义引擎处理高 DPI 请求的兼容参数。

`QIconEnginePlugin` 的职责很集中：用可靠元数据把一个后缀路由到一个新引擎。资源解析、绘制质量、缓存与高 DPI 支持仍应在 `QIconEngine` 中完成。
