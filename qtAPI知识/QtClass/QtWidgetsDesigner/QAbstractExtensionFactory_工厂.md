# QAbstractExtensionFactory 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractExtensionFactory>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QAbstractExtensionFactory` 定义了 Qt Widgets Designer 扩展工厂的最小契约：给定一个正在设计中的对象和一个扩展接口标识符（IID），返回该对象对应的扩展对象，或者返回空指针表示“不支持”。

它本身不应直接实例化。实际开发自定义 Designer 插件时，通常继承 `QExtensionFactory`，重写其受保护的 `createExtension()`；`QExtensionFactory` 会替你实现本类要求的 `extension()` 调度、缓存和父对象管理。

这个抽象层解决的是“Designer 如何用统一方式向不同 widget 请求不同能力”的问题。典型扩展包括：

- `QDesignerContainerExtension`：让自定义复合控件在 Designer 中像 `QTabWidget` 一样可插入、删除、切换页面；
- `QDesignerPropertySheetExtension`：向属性编辑器提供自定义属性；
- `QDesignerTaskMenuExtension`：向右键任务菜单添加动作；
- `QDesignerMemberSheetExtension`：控制成员信号和槽的可见性。

## 调用链

```text
Designer 需要某个扩展
    -> QExtensionManager 查已注册 factory
    -> 调用 factory.extension(object, iid)
    -> factory 返回扩展对象或 nullptr
```

管理器会依次尝试已注册的工厂，找到第一个能创建请求扩展的工厂后使用其结果。因此 factory 的实现应在“不匹配的 IID”或“不支持的 object 类型”时快速返回 `nullptr`。

## 实现时该怎么判断

`iid` 表示所需接口种类，`object` 是被设计的 widget 或对象。实现通常先判断 IID，再用 `qobject_cast` 判断对象类型：

```cpp
QObject *MyFactory::extension(QObject *object, const QString &iid) const
{
    if (iid != Q_TYPEID(QDesignerTaskMenuExtension))
        return nullptr;

    auto *widget = qobject_cast<MyWidget *>(object);
    if (!widget)
        return nullptr;

    return new MyTaskMenuExtension(widget);
}
```

新代码一般不直接派生本类，而是把以上逻辑放进 `QExtensionFactory::createExtension()`。这样扩展实例会按该 factory 的既有约定创建和管理。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QAbstractExtensionFactory()` | 销毁扩展工厂接口对象。 | 通过基类指针删除派生 factory 时依赖虚析构。 |
| 纯虚接口 | `QObject *extension(QObject *object, const QString &iid) const` | 为指定对象查找或创建指定 IID 的扩展对象。 | 不支持时返回 `nullptr`；返回对象必须真正实现 IID 对应的扩展接口。 |

## 易错点

1. 不要直接实例化或单独使用 `QAbstractExtensionFactory`；普通插件实现应继承 `QExtensionFactory`。
2. IID 和 C++ 类名不是一回事。要使用 `Q_TYPEID(扩展接口类型)`，并确保接口有正确声明。
3. factory 只负责回答“能不能给这个对象提供这种扩展”，不能匹配时返回空指针是正常流程。

### 一句话总结

`QAbstractExtensionFactory` 是 Designer 扩展发现机制的抽象入口：用对象加 IID 请求扩展，不支持就返回空；实际插件通常转而继承 `QExtensionFactory`。
