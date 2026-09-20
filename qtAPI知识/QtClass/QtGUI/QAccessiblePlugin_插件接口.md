# Qt QAccessiblePlugin 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessiblePlugin>`  
> 所属模块：`Qt6::Gui`  
> 基类：`QObject`  
> 定位：把自定义可访问接口作为 Qt 动态插件提供的抽象工厂

## 1. 它解决什么问题

`QAccessiblePlugin` 让应用或第三方库把某类 QObject/QWidget 的 `QAccessibleInterface` 实现编译为可按需加载的 Qt 插件。Qt 在 `QAccessible::queryAccessibleInterface()` 找不到已安装 factory 的实现时，可以加载无障碍插件并请求插件为给定对象创建接口。

它解决的是“把无障碍适配与主程序解耦、仅在需要时加载”的问题：

- 不需要把所有自定义 accessible 实现链接进每个进程；
- 可以给第三方控件库单独发布无障碍支持；
- 插件可以根据类 key 决定是否处理对象；
- Qt plugin loader 管理插件实例生命周期。

它不是屏幕阅读器插件，也不是平台后端桥接。它提供的是**应用内对象到 `QAccessibleInterface` 的工厂**；平台后端仍由 Qt 的 MSAA、macOS Accessibility、AT-SPI 等集成处理。

## 2. 最小插件骨架

```cpp
class MyControlsAccessiblePlugin final : public QAccessiblePlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QAccessibleFactoryInterface_iid)

public:
    QAccessibleInterface *create(const QString &key,
                                 QObject *object) override
    {
        if (key == u"MyControls::Gauge" && object)
            return new GaugeAccessible(
                static_cast<Gauge *>(object));
        return nullptr;
    }
};
```

`Q_PLUGIN_METADATA` 负责把插件元数据导出给 Qt plugin loader。实际工程还需按目标平台把动态库放入 Qt 能发现的插件路径，并保证 ABI、Qt 版本和编译器配置相容。

## 3. `create()` 的契约

Qt 调用 `create(key, object)` 时，插件应：

1. 区分自己是否支持 `key`；
2. 确认 `object` 非空并且实际类型匹配；
3. 创建并返回正确的 `QAccessibleInterface`；
4. 不支持时返回 `nullptr`，让 Qt 继续查找其他实现。

`key` 区分大小写。不要为了方便只做字符串前缀匹配后就对任意 QObject 使用 `static_cast`；类型不匹配会造成未定义行为。需要时用 `qobject_cast` 或 `inherits()` 进行防御性检查。

返回的 interface 会进入 Qt 可访问性缓存，调用方不应在插件代码之外自行 delete。factory 每次调用也不应为同一对象无条件制造多个不受 cache 管理的接口。

## 4. 插件生命周期与边界

插件实例由 plugin loader 自动创建和销毁。`QObject *parent` 由 loader/Qt 对象模型管理，业务代码不需要手动构造或析构插件。

`create()` 可能在辅助技术查询期间被调用，因此必须：

- 不做网络访问、阻塞磁盘扫描或大规模模型初始化；
- 不修改目标控件的业务状态；
- 只创建可立即用于查询的 interface；
- 正确处理对象已销毁、对象无效或运行时类不匹配；
- 将 GUI 对象访问限制在所属线程。

若控件库可以直接在主程序中安装 `QAccessible::installFactory()`，动态插件未必更简单。插件更适合需要独立发布、按需加载或第三方分发的适配层。

## 5. 逐项 API 说明

### `explicit QAccessiblePlugin(QObject *parent = nullptr)`

构造插件对象。通常由 Qt plugin loader 自动调用，`parent` 也由 Qt 管理。应用代码不应为“临时创建一个 accessible interface”而直接实例化插件。

### `virtual ~QAccessiblePlugin()`

虚析构函数。Qt 在插件不再使用时销毁插件；用户不需要显式调用析构，也不应在仍有 interface 使用插件代码时强行卸载动态库。

### `virtual QAccessibleInterface *create(const QString &key, QObject *object) = 0`

为 `key` 和 `object` 创建可访问接口。`key` 区分大小写；不支持时返回 `nullptr`。

返回 interface 后，其生命周期由 Qt 无障碍系统协作管理。实现不能返回栈对象、临时对象地址或已被 QObject parent 自动销毁的对象。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `QAccessiblePlugin(QObject *)` | 构造无障碍插件。 | 通常由 plugin loader 自动调用。 |
| 生命周期 | `~QAccessiblePlugin()` | 销毁插件实例。 | Qt 自动管理；不要在使用期间强制卸载。 |
| 工厂 | `create(const QString &, QObject *)` | 为指定类 key 和对象创建 interface。 | key 区分大小写；不支持返回 `nullptr`；返回值不能是临时对象。 |
| 元数据 | `Q_PLUGIN_METADATA(IID QAccessibleFactoryInterface_iid)` | 导出可发现的 Qt 插件元数据。 | 需要匹配 IID、部署路径与 Qt ABI。 |

### 一句话总结

`QAccessiblePlugin` 是把对象级无障碍适配做成按需加载工厂的入口：用区分大小写的 key 精确匹配控件类型，返回由 Qt cache 管理的 interface，不支持就返回 `nullptr`，并把插件加载和卸载交给 Qt。
