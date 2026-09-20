# QAbstractExtensionManager 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractExtensionManager>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QAbstractExtensionManager` 定义了 Qt Widgets Designer 扩展管理器的抽象契约。它负责把“扩展工厂”按 IID 注册起来，并在 Designer 需要某个扩展时，从已注册工厂中找出能为指定对象提供扩展的那一个。

这个接口解决的是扩展系统的中心调度问题：

- 插件在初始化时注册 factory；
- Designer 在需要能力时按对象和 IID 查询；
- manager 调用 factory 创建或返回对应扩展；
- 插件卸载或不再需要时注销 factory。

它本身不应直接实例化。普通插件代码通常通过 `QDesignerFormEditorInterface::extensionManager()` 取得 Designer 当前的扩展管理器接口；Qt 提供的具体实现是 `QExtensionManager`。

## 典型链路

```cpp
void MyPlugin::initialize(QDesignerFormEditorInterface *formEditor)
{
    auto *manager = formEditor->extensionManager();
    Q_ASSERT(manager);

    manager->registerExtensions(
        new MyExtensionFactory(manager),
        Q_TYPEID(QDesignerTaskMenuExtension));
}
```

这里 `registerExtensions()` 把一个 factory 挂到指定扩展接口 IID 下。稍后 Designer 需要任务菜单扩展时，会通过 `extension(object, iid)` 触发查找。

## IID 的意义

`iid` 是扩展接口的字符串标识，用来区分“我要任务菜单扩展”还是“我要容器扩展”。通常通过 `Q_TYPEID(QDesignerTaskMenuExtension)` 取得，而不是手写字符串。自定义扩展接口还需要配合 `Q_DECLARE_EXTENSION_INTERFACE()` 声明唯一标识符。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QAbstractExtensionManager()` | 销毁扩展管理器接口对象。 | 通过基类指针销毁具体 manager 时依赖虚析构。 |
| 查询 | `QObject *extension(QObject *object, const QString &iid) const` | 查询指定对象的指定扩展接口。 | 找不到时返回 `nullptr`；调用方应把返回值转换为目标扩展接口并检查。 |
| 注册 | `registerExtensions(QAbstractExtensionFactory *factory, const QString &iid)` | 将 factory 注册到指定扩展 IID。 | factory 通常以 manager 为父对象；同一 factory 可按实现支持多个 IID。 |
| 注销 | `unregisterExtensions(QAbstractExtensionFactory *factory, const QString &iid)` | 取消 factory 与指定扩展 IID 的注册关系。 | 插件卸载或撤销扩展时使用；确保注销的 factory 和 IID 与注册时一致。 |

## 易错点

1. `QAbstractExtensionManager` 是契约，不是插件里最常手写的实现类。大多数代码拿 Designer 提供的 manager 指针使用即可。
2. 注册的是 factory，不是扩展实例。扩展实例通常在真正被请求时才创建。
3. `extension()` 返回 `QObject *`，调用方必须检查空指针，并转换成正确的扩展接口。
4. IID 要和 factory 能创建的扩展类型一致；注册错 IID 会导致 Designer 找不到扩展或拿到不匹配对象。

### 一句话总结

`QAbstractExtensionManager` 是 Designer 扩展系统的调度契约：注册 factory，按对象和 IID 查询扩展，并在不需要时注销对应关系。
