# QAccessiblePlugin

> Qt 6.11.1 · Qt GUI · 来自 `QAccessiblePlugin`

## 1. 先建立直觉

`QAccessiblePlugin` 用于把某些 QObject 类的无障碍接口做成 Qt 插件，让应用在查询可访问接口时按需加载。它主要面向库作者、平台集成或独立控件包；普通应用通常直接调用 `QAccessible::installFactory()` 更简单。

插件解决的是“我不能或不想在主程序里硬编码所有可访问接口工厂”的问题。它不是给控件自动补全语义的工具，真正的 Role、State、Text 和专用接口仍要由你返回的 `QAccessibleInterface` 实现。

## 2. 类说明

- 头文件：`#include <QAccessiblePlugin>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 核心虚函数：`create(const QString &key, QObject *object)`
- 加载方式：由 Qt 插件系统发现和实例化，通常配合 `Q_PLUGIN_METADATA`。

Qt 在 `QAccessible::queryAccessibleInterface()` 无法从已安装工厂获得结果时，可能加载无障碍插件并调用其 `create()`。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessiblePlugin(parent)` | 构造插件对象；通常由插件加载器调用。 |
| `~QAccessiblePlugin()` | 插件卸载或不再使用时由 Qt 管理。 |
| `create(key, object)` | 根据类名键和对象指针创建对应的 `QAccessibleInterface`。 |

`key` 区分大小写，通常是对象类名或 Qt 用于查找接口的类键。无法处理时必须返回 `nullptr`，让其他插件或父类策略继续尝试。

## 4. 关键用法

```cpp
class MyAccessiblePlugin : public QAccessiblePlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QAccessibleFactoryInterface")

public:
    QAccessibleInterface *create(const QString &key,
                                 QObject *object) override
    {
        if (key == u"MyDial"_s)
            return new AccessibleMyDial(static_cast<MyDial *>(object));
        return nullptr;
    }
};
```

`create()` 返回的新接口会交给 Qt 无障碍缓存管理。不要返回栈对象，也不要在插件里保存每个接口的裸指针列表。类型转换前应确保 `key` 与对象真实类型一致；如果对象不是预期类型，返回 `nullptr` 比强转崩溃更好。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 应用内部少量自定义控件 | 使用 `QAccessible::installFactory()`。 |
| 发布一个控件库，希望使用者自动获得无障碍映射 | 可使用 `QAccessiblePlugin`。 |
| 平台或产品级可访问接口包 | 插件方式便于独立部署和按需加载。 |
| 需要运行时热更新业务语义 | 不适合；无障碍接口应与控件代码版本一致。 |

## 6. 常见坑与经验

- 插件加载是按需的，不要把初始化关键业务逻辑放进插件构造函数。
- `create()` 应快速、确定、无副作用；它可能在辅助技术查询时被调用。
- 插件卸载后接口代码不可再被调用。实际部署中应避免手动卸载正在使用的无障碍插件。
- 元数据、IID、导出宏和插件目录必须正确，否则 Qt 永远不会调用你的 `create()`。
- 插件只提供工厂入口；返回的接口仍必须处理对象销毁、虚拟子节点和事件同步。

## 7. 知识点覆盖

- 无障碍接口插件化与工厂机制
- `queryAccessibleInterface()` 的查找链
- 插件生命周期、元数据和按需加载
- `create()` 返回值所有权和类型安全
- 插件方案与 `installFactory()` 的取舍
