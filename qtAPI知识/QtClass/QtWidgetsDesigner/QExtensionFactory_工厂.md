# QExtensionFactory 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QExtensionFactory>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QObject`、`QAbstractExtensionFactory`

## 它解决什么问题

`QExtensionFactory` 是 Qt Widgets Designer 中创建自定义扩展实例的基类。Designer 不会在插件加载时立刻创建所有扩展，而是在需要某种能力时才向扩展管理器请求；扩展管理器再询问已注册的 factory。`QExtensionFactory` 就负责在这个时候根据对象和 IID 创建合适的扩展对象。

它解决的典型问题是：你的自定义 widget 在 Designer 里需要额外能力，而这个能力不能靠 widget 本身的普通属性完成。例如：

- 自定义多页容器需要 Designer 支持添加、删除、切换页面；
- 自定义 widget 需要右键任务菜单；
- 需要给属性编辑器暴露一组特殊属性；
- 需要控制 Designer 中成员函数或槽的显示。

这些能力分别由 Designer 扩展接口表达，factory 负责把“某个 widget 对象”与“某个扩展接口 IID”连接起来。

## 使用模型

插件初始化时把 factory 注册给 `QExtensionManager`。之后 Designer 需要扩展时，manager 调用 factory 的 `extension(object, iid)`；`QExtensionFactory::extension()` 内部会调用你重写的 `createExtension(object, iid, parent)`。

```cpp
class MyExtensionFactory : public QExtensionFactory
{
public:
    using QExtensionFactory::QExtensionFactory;

protected:
    QObject *createExtension(QObject *object,
                             const QString &iid,
                             QObject *parent) const override
    {
        if (iid != Q_TYPEID(QDesignerTaskMenuExtension))
            return nullptr;

        auto *widget = qobject_cast<MyWidget *>(object);
        if (!widget)
            return nullptr;

        return new MyTaskMenuExtension(widget, parent);
    }
};
```

这个函数里有两个判断必须写清楚：`iid` 判断扩展类型，`qobject_cast` 判断当前对象是不是你的 widget。任一不匹配都返回 `nullptr`，这不是错误，而是让 manager 继续尝试其它 factory 的正常路径。

## parent 参数为什么重要

`createExtension()` 的第三个参数 `parent` 是扩展对象的 QObject 父对象。返回扩展实例时应把它作为 parent 传进去，让 Designer 的扩展系统接管生命周期。

不要把扩展对象交给智能指针再同时设置 QObject parent；这会让所有权变得混乱。Designer 扩展对象通常按 QObject 父子关系释放。

## 与 QExtensionManager 的关系

`QExtensionFactory` 自己不负责保存全局注册表，也不会主动被 Designer 扫描。它必须注册到 `QExtensionManager`，通常在 `QDesignerCustomWidgetInterface::initialize()` 中完成：

```cpp
auto *manager = formEditor->extensionManager();
manager->registerExtensions(
    new MyExtensionFactory(manager),
    Q_TYPEID(QDesignerTaskMenuExtension));
```

如果一个 factory 同时支持多个扩展类型，可以在 `createExtension()` 中分别判断多个 IID。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QExtensionFactory(QExtensionManager *parent = nullptr)` | 创建扩展工厂对象。 | 常以 `QExtensionManager` 为父对象，跟随 Designer 扩展管理器释放。 |
| 查询 | `extension(QObject *object, const QString &iid) const` | 返回指定对象的指定扩展。 | 通常由 manager 调用；内部会走 `createExtension()`。 |
| 管理器访问 | `extensionManager() const` | 返回该 factory 关联的扩展管理器。 | 可用于需要访问注册环境的实现；为空时说明构造时未传 manager。 |
| 派生扩展点 | `createExtension(QObject *object, const QString &iid, QObject *parent) const` | 派生类重写，用来真正创建扩展实例。 | 不支持时返回 `nullptr`；支持时返回以 `parent` 为父对象的扩展 QObject。 |

## 易错点

1. 重写点是 `createExtension()`，不是直接把所有逻辑塞进外部注册代码。
2. `iid` 判断和 `object` 类型判断都要做。只判断其中一个容易把扩展挂到错误对象上。
3. 返回 `nullptr` 是正常的“不匹配”信号，不应弹错误或断言。
4. 扩展对象要使用传入的 `parent` 管理生命周期。

### 一句话总结

`QExtensionFactory` 是 Designer 延迟创建扩展对象的工厂基类：注册给 manager 后，通过重写 `createExtension()` 按对象和 IID 生成正确的扩展实例。
