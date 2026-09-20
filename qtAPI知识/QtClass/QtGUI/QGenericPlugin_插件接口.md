# QGenericPlugin

`QGenericPlugin` 是 Qt 通用驱动插件的抽象基类，历史上主要用于鼠标等输入驱动的插件入口。派生类通过插件元数据公布支持的 key，并重写 `create()` 按 key 和规格字符串创建实际驱动对象。

- 头文件：`#include <QGenericPlugin>`
- 模块：`Qt6::Gui`
- 继承：`QObject`
- 设计：抽象插件入口，不是普通业务对象工厂

## 它解决的问题

程序在编译时不必链接每一种平台驱动实现。Qt 可在运行时扫描插件元数据，知道插件支持哪些 key，再通过统一的 `create(key, specification)` 请求正确的驱动。这样平台或硬件特有实现能以动态插件形式部署。

```cpp
class MyInputPlugin final : public QGenericPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QGenericPluginFactoryInterface_iid FILE "myinput.json")
public:
    QObject *create(const QString &key, const QString &specification) override
    {
        if (key.compare(u"myinput"_s, Qt::CaseInsensitive) != 0)
            return nullptr;
        return new MyInputDriver(specification);
    }
};
```

元数据 JSON 必须列出插件支持的 keys；`create()` 的 `key` 不区分大小写。

## 实现边界

这不是为一般桌面应用扩展功能而设计的首选插件接口。对于图片格式、SQL、QML 扩展、样式或自定义业务插件，应使用其领域对应的 Qt 插件接口。`QGenericPlugin` 的典型消费者是 Qt 的通用驱动加载路径。

由 `Q_PLUGIN_METADATA` 导出的插件实例通常由 Qt/moc 生成的加载流程创建。不要手动调用析构函数，也不要假定能在仍有创建对象活动时卸载插件库。`create()` 返回的 `QObject *` 所有权需要遵循调用方接口的约定；实现不能返回栈对象，也应对未知 key 返回 `nullptr`。

插件对象与其创建的对象通常必须在相同线程和仍已加载的插件代码生命周期内使用。避免让异步任务在插件被卸载后继续调用插件实现。

## API 速查表

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `QGenericPlugin(QObject *parent = nullptr)` | 构造插件入口并可指定 `QObject` 父对象。 | 常由 Qt 插件导出机制自动调用，业务代码无需显式构造。 |
| `~QGenericPlugin()` | 虚析构函数。 | Qt 在插件不再使用时管理销毁；不要手动析构动态加载插件实例。 |
| `create(const QString &key, const QString &specification)` | 纯虚工厂函数，根据 key 和规格字符串创建驱动对象。 | 必须重写；key 不区分大小写；不支持时返回 `nullptr`；返回对象不能是栈对象。 |

## 易错点

1. 忘记让 JSON 元数据列出 key，导致工厂发现不到插件。
2. 对未知 key 创建“默认驱动”，掩盖配置错误；应返回 `nullptr`。
3. 用此接口承载普通应用功能模块；选择领域专用插件接口或显式业务扩展点。
4. 卸载插件后仍持有其创建对象或回调，造成代码段已失效的生命周期问题。
