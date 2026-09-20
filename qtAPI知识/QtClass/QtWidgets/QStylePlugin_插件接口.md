# Qt QStylePlugin 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStylePlugin>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QObject -> QStylePlugin`  
> 定位：可动态发现的 QStyle 工厂接口

## 1. 先建立整体认识：它解决什么问题

`QStylePlugin` 让一个自定义 `QStyle` 不必静态编进主程序，而是以 Qt 插件形式放进约定的 style 插件目录，由 `QStyleFactory` 按名称发现并创建。

它解决的是部署和扩展问题：

- 主程序不需要依赖每一种 style 的实现；
- 用户可以通过插件增加新的界面风格；
- style 的创建入口遵循 Qt 的插件元数据和工厂约定。

`QStylePlugin` 自己不负责绘制。真正的绘制、尺寸计算和命中测试仍由 `QStyle` 派生类完成。

## 2. 它和 `QStyleFactory` 的关系

```text
QStyleFactory
    ↓ 按 key 查找插件
QStylePlugin::create(key)
    ↓
自定义 QStyle
```

`QStyleFactory::keys()` 能列出当前可用的 style 名称；`QStyleFactory::create("myStyle")` 会让插件返回对应的 `QStyle` 对象。

## 3. 最小插件骨架

```cpp
#include <QStylePlugin>
#include <QStyle>

class MyStylePlugin final : public QStylePlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QStyleFactoryInterface")

public:
    using QStylePlugin::QStylePlugin;

    QStyle *create(const QString &key) override
    {
        if (key.compare("mystyle", Qt::CaseInsensitive) == 0)
            return new MyStyle;
        return nullptr;
    }
};
```

实际插件还需要在构建系统中生成动态库，并把库部署到 Qt 能扫描到的 style 插件目录。

## 4. `create()` 的契约

`create(const QString &key)` 接收 style 名称。实现应：

1. 对 key 做明确的大小写处理；
2. 只为自己支持的 key 返回 style；
3. 对未知 key 返回 `nullptr`；
4. 返回一个新的 `QStyle` 对象。

不要把“未知 key”当成默认 style 处理，否则多个插件一起存在时可能出现错误匹配。

## 5. 插件元数据和 IID

头文件提供的接口标识是：

```cpp
QStyleFactoryInterface_iid
// "org.qt-project.Qt.QStyleFactoryInterface"
```

通常通过 `Q_PLUGIN_METADATA` 声明。IID 必须和 Qt 约定一致，插件系统才能把它识别为 style factory 插件。

## 6. 什么时候应该用它

- 你要为多个产品或主题提供可独立部署的 style；
- 你在开发 Qt 风格插件本身；
- 你希望用户安装插件后，主程序无需重新编译即可发现新 style。

如果 style 只在一个程序里使用，直接在主程序中创建 `QProxyStyle` 或自定义 `QStyle` 往往更简单。

## 7. 常见误区

- `QStylePlugin` 不是 style 本身，必须和 `QStyle` 派生实现配套；
- 只实现 `create()` 不能自动让插件被发现，还需要正确元数据、插件构建和部署路径；
- 返回的 style 对象不能是栈对象；
- 不支持的 key 要返回 `nullptr`，不要无条件返回同一个 style；
- 插件加载失败时，优先检查 IID、导出元数据、目标目录和 Qt 版本/编译器匹配。

## 8. API 逐项说明

### `QStylePlugin(QObject *parent)`

构造插件对象。它是 `QObject` 的派生类，因此可以有 parent，但插件实例通常由 Qt 插件系统创建和管理。

### `~QStylePlugin()`

虚析构函数，保证通过基类指针销毁具体插件时能正确执行派生类析构。

### `create(const QString &key)`

纯虚函数，也是插件唯一必须实现的 style 创建入口。根据 key 返回对应的 `QStyle`。无法识别 key 时返回 `nullptr`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `explicit QStylePlugin::QStylePlugin(QObject *parent = nullptr)` | 构造 style 插件对象。 | 通常由插件系统实例化，不需要业务代码手动创建。 |
| 析构函数 | `QStylePlugin::~QStylePlugin()` | 以多态方式销毁插件对象。 | 派生插件可以在这里释放自己的资源。 |
| 纯虚函数 | `QStyle *QStylePlugin::create(const QString &key)` | 根据 style 名称创建一个新的 `QStyle`。 | 支持 key 返回新对象，不支持 key 返回 `nullptr`。 |
| 接口标识 | `QStyleFactoryInterface_iid` | 标识这是 Qt style factory 插件接口。 | 应和 `Q_PLUGIN_METADATA(IID ...)` 使用的 IID 保持一致。 |

## 10. 一句话总结

`QStylePlugin` 是把自定义 `QStyle` 接入 Qt 动态插件发现机制的接口，核心任务就是“按 key 返回正确的 style”。
