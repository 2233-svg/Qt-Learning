# QGenericPluginFactory

`QGenericPluginFactory` 是 Qt 通用驱动插件的运行时发现入口。它枚举已找到的插件 key，并要求匹配插件创建相应 `QObject` 驱动实例。

- 头文件：`#include <QGenericPluginFactory>`
- 模块：`Qt6::Gui`
- 类型特性：纯静态工具类，没有对象状态
- 关联类型：`QGenericPlugin`、`Q_PLUGIN_METADATA`

## 它解决的问题

调用方无需了解插件库名称或派生类类型，只需要一个逻辑 key 和规格字符串。工厂负责让 Qt 的插件系统寻找支持该 key 的动态插件并请求它创建对象。这使平台相关驱动能够按部署环境出现或缺失。

```cpp
const QStringList available = QGenericPluginFactory::keys();
if (!available.contains(u"myinput"_s, Qt::CaseInsensitive))
    return;

QObject *driver = QGenericPluginFactory::create(u"myinput"_s, u"device=/dev/input0"_s);
if (!driver)
    return;
```

## 使用边界

keys 与创建都依赖插件搜索路径、动态库可加载性、插件元数据和二进制 ABI 兼容性。`keys()` 看到某 key 不保证 `create()` 必然成功：规格字符串可能无效，驱动初始化可能失败，或插件可发现但依赖加载失败。

返回值是裸 `QObject *`。创建成功后，调用方应立即按实际插件接口建立所有权，例如提供合适 parent 或交由约定的拥有者管理；失败返回 `nullptr`。key 不区分大小写。

这个工厂面向 Qt 通用驱动插件机制，不应当被当作任意业务模块服务定位器。普通应用功能更适合显式依赖注入或领域专用 Qt 插件 API。

## API 速查表

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `static QStringList keys()` | 返回当前可用通用插件声明的有效 key 列表。 | 列表来自插件发现与元数据；不保证创建一定成功。 |
| `static QObject *create(const QString &key, const QString &specification)` | 查找能处理 key 的插件，并用规格字符串创建驱动。 | key 不区分大小写；失败返回 `nullptr`；调用方需明确返回对象的所有权。 |

## 易错点

1. 只因 `keys()` 包含 key 就跳过空指针检查。
2. 忽略插件搜索路径、调试/发布构建或 Qt 版本不一致造成的加载失败。
3. 将返回对象泄漏，或在插件/对象仍活跃时尝试卸载插件库。
