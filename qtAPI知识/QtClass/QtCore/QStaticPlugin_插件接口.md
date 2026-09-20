# QStaticPlugin：静态链接插件的实例入口与元数据

> Qt 6.11.1 | `#include <QStaticPlugin>` | 模块：`Qt6::Core`

`QStaticPlugin` 是一个轻量结构，保存静态插件的实例函数和插件元数据。它服务于“插件代码被链接进最终可执行文件或库”的部署方式：不在运行时扫描和加载独立动态库，而由链接和导入宏把插件登记给 Qt。

应用代码通常不会手工构造 `QStaticPlugin`。更常见的工作是：插件类使用 `Q_PLUGIN_METADATA` 声明元数据，宿主使用 `Q_IMPORT_PLUGIN(PluginClass)` 将其注册，再通过 `QPluginLoader::staticInstances()` 或相应 Qt 工厂机制发现实例。

## 它解决什么问题

动态插件需要在部署目录中找到并加载 DLL、so 或 dylib；静态插件则把实现编入产物。静态方式常用于单文件部署、嵌入式目标、受限运行环境，或希望避免运行时插件搜索路径的场景。

代价也很明确：

- 插件版本随宿主一起发布，不能单独替换。
- 可执行文件通常更大。
- 链接器、CMake 配置和导入宏必须确保插件对象文件没有被裁剪掉。
- 宿主只应链接并导入可信的插件实现；元数据本身不是安全认证。

## 宿主侧的典型用法

```cpp
#include <QtPlugin>

Q_IMPORT_PLUGIN(MyImageFormatPlugin)

// 稍后由对应的 Qt 工厂或：
const QList<QObject *> plugins = QPluginLoader::staticInstances();
```

`Q_IMPORT_PLUGIN()` 会注册由插件的 moc 代码生成的 `QStaticPlugin` 提供者。对 CMake 项目，除了链接插件目标外，还应采用 Qt 为该类插件提供的导入/链接配置方式，确保最终链接产物确实包含插件。

## API 的实际语义

### `instance`

公共字段 `instance` 的类型是 `QtPluginInstanceFunction`，可调用并返回插件 `QObject *`。Qt 生成的静态插件入口通常延迟创建实例，并保留一个 `QPointer`；这是 Qt 的内部注册机制，不是建议业务层到处直接调用的服务定位器。

若确实直接调用，必须遵守插件接口约定，检查对象是否可转换为预期接口，并考虑首次创建对象所在的线程。对一般应用，更稳妥的入口是 Qt 提供的专用工厂或 `QPluginLoader::staticInstances()`。

### `metaData()`

`metaData()` 返回由 `Q_PLUGIN_METADATA` 编入的 `QJsonObject`。典型字段包括 IID、className 和插件自定义元数据。它适合做发现、诊断和接口选择，但不能代替 `qobject_cast` 或其他真正的接口验证。

## 生命周期、线程与平台考虑

- 静态插件实例是 `QObject`，生命周期、线程归属和线程安全性由该插件实现决定。
- 不要因为 `QStaticPlugin` 是值类型就认为插件对象可以跨线程随意使用；首次创建及后续调用仍应符合对象的线程亲和性。
- 静态插件没有运行时卸载过程。需要可热更新、可隔离加载或用户安装插件的产品，通常应使用动态插件机制。
- 注册表来自编译和链接时的已知代码，适合受控部署；它不提供对插件能力、数据格式或安全性的自动校验。

## 常见错误

1. **手工拼装 `QStaticPlugin`。** 应让 moc、`Q_PLUGIN_METADATA` 与 `Q_IMPORT_PLUGIN` 协作生成和注册。
2. **只链接静态插件而未导入。** 代码可能被链接器裁剪，运行时看不到插件。
3. **用元数据判断接口可用。** 元数据只是声明；获取 `QObject *` 后仍要转换并验证接口。
4. **从任意线程首次调用 `instance`。** 插件对象可能因此落在错误线程；按插件的线程模型创建和使用。
5. **期待静态插件可热卸载。** 它随宿主进程存在，不能替代动态加载方案。

## API 速查表

| 类别 | API | 语义 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QStaticPlugin(QtPluginInstanceFunction, QtPluginMetaDataFunction)` | 组合实例入口与原始元数据函数。 | 公共但主要供 Qt 生成的注册代码使用，业务代码通常不手工构造。 |
| 公共字段 | `QtPluginInstanceFunction instance` | 指向取得插件 `QObject *` 的函数。 | 调用前要了解插件接口、对象线程与生命周期；优先走 Qt 工厂。 |
| 元数据 | `QJsonObject metaData() const` | 将嵌入的插件元数据解析为 JSON 对象。 | 数据来自编译期元数据，不等同于接口验证或安全认证。 |
| 注册函数 | `qRegisterStaticPluginFunction(QStaticPlugin)` | 把静态插件登记给 Qt。 | 通常由 `Q_IMPORT_PLUGIN` 生成的代码调用，不应作为普通业务 API。 |
| 导入宏 | `Q_IMPORT_PLUGIN(PLUGIN)` | 让宿主引用并注册指定静态插件。 | 插件类名和链接配置必须匹配；放在适合全局初始化的编译单元。 |
| 发现 | `QPluginLoader::staticPlugins()` | 取得已注册的 `QStaticPlugin` 描述。 | 主要用于检查元数据或框架级发现。 |
| 实例 | `QPluginLoader::staticInstances()` | 取得所有静态插件的 `QObject` 实例。 | 对每个对象做接口转换和能力检查。 |

`QStaticPlugin` 是静态插件体系的连接件：它把“可创建实例”和“该实例宣称的元数据”交给 Qt 的注册机制。宿主代码的重点应放在正确导入、正确链接，以及按照接口和线程规则使用实例。
