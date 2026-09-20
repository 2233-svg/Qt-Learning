# QExtensionManager 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QExtensionManager>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QObject`、`QAbstractExtensionManager`

## 它解决什么问题

`QExtensionManager` 是 Qt Widgets Designer 扩展系统的具体管理器。它保存“扩展 IID -> factory”的注册关系，并在 Designer 需要某个扩展时，让已注册的 factory 按需创建扩展实例。

它解决的是插件扩展的发现和调度问题。你写的自定义 widget 插件如果想在 Designer 里加入任务菜单、容器页管理、属性表扩展等能力，就需要把对应 factory 注册到 extension manager。

Qt 文档说明它通常不由插件直接创建。插件初始化时会从 `QDesignerFormEditorInterface::extensionManager()` 取得当前 Designer 的管理器，然后注册自己的 `QExtensionFactory`。

## 典型注册位置

```cpp
void MyPlugin::initialize(QDesignerFormEditorInterface *formEditor)
{
    if (initialized)
        return;

    auto *manager = formEditor->extensionManager();
    Q_ASSERT(manager);

    manager->registerExtensions(
        new MyExtensionFactory(manager),
        Q_TYPEID(QDesignerTaskMenuExtension));

    initialized = true;
}
```

这里注册的是 factory，不是扩展实例。Designer 后续真正需要任务菜单扩展时，才会通过 manager 查询。

## 查询扩展

可以直接调用 `extension(object, iid)`，但更常见的是使用 `qt_extension<T>()` 模板辅助函数，它会帮你按类型取扩展并转换结果：

```cpp
auto *manager = formEditor->extensionManager();
auto *sheet = qt_extension<QDesignerPropertySheetExtension *>(manager, widget);
if (sheet)
    qDebug() << sheet->count();
```

如果目标 widget 没有对应扩展，结果是空指针。不要假设所有自定义 widget 都实现了所有 Designer 扩展。

## IID 和接口声明

内建扩展接口通常用 `Q_TYPEID(QDesignerTaskMenuExtension)`、`Q_TYPEID(QDesignerContainerExtension)` 等取得 IID。自定义扩展接口需要使用：

```cpp
Q_DECLARE_EXTENSION_INTERFACE(MyExtension, "com.mycompany.myproduct.myextension")
```

这个标识符必须唯一。推荐包含公司、产品和扩展名，避免插件之间冲突。没有正确声明时，`qt_extension<T>()` 无法按接口类型可靠查询。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QExtensionManager(QObject *parent = nullptr)` | 创建扩展管理器对象。 | Designer 通常已有当前 manager；插件一般从 `formEditor->extensionManager()` 获取。 |
| 析构 | `virtual ~QExtensionManager()` | 销毁扩展管理器。 | 以 manager 为父对象的 factory 会随 QObject 父子关系释放。 |
| 查询 | `extension(QObject *object, const QString &iid) const` | 查询指定对象的指定扩展。 | 找不到返回 `nullptr`；结果是 `QObject *`，需要转换到目标扩展接口。 |
| 注册 | `registerExtensions(QAbstractExtensionFactory *factory, const QString &iid = {})` | 注册一个 factory，让它响应指定 IID 的扩展请求。 | 通常在插件 `initialize()` 中调用；`iid` 应与 factory 支持的扩展接口匹配。 |
| 注销 | `unregisterExtensions(QAbstractExtensionFactory *factory, const QString &iid = {})` | 取消 factory 对指定 IID 的注册。 | 注销参数要与注册时一致；插件卸载或撤销扩展时使用。 |
| 辅助函数 | `qt_extension<T>(QAbstractExtensionManager *manager, QObject *object)` | 按模板类型从 manager 取得对象扩展并转换。 | 自定义扩展接口必须先用 `Q_DECLARE_EXTENSION_INTERFACE` 声明唯一 IID。 |
| 宏 | `Q_DECLARE_EXTENSION_INTERFACE(ExtensionName, Identifier)` | 将扩展接口类型和唯一字符串标识符关联。 | 通常放在扩展接口类定义后；标识符要全局唯一。 |

## 易错点

1. `QExtensionManager` 不会自动知道你的插件扩展；必须在初始化时注册 factory。
2. 注册的是“能创建扩展的 factory”，不是“已经创建好的扩展对象”。
3. `extension()` 返回空指针是正常结果，表示没有对应扩展。
4. 自定义 IID 不唯一会造成扩展查询冲突，最好使用反向域名或公司产品前缀。
5. factory 生命周期建议交给 QObject parent 管理，常见写法是 `new MyExtensionFactory(manager)`。

### 一句话总结

`QExtensionManager` 是 Designer 扩展系统的注册表和调度器：插件把 factory 按 IID 注册进去，Designer 需要扩展时再按对象和接口类型查询。
