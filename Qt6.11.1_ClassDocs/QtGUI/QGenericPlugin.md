# QGenericPlugin

> Qt 6.11.1 · Qt GUI · 来自 `QGenericPlugin`

## 1. 先建立直觉

`QGenericPlugin` 是 Qt GUI 通用插件的基类。它用于实现由键名创建 QObject 驱动或辅助组件的插件，例如某些平台输入、设备或图形相关扩展。应用通常不直接创建它，而是由 Qt 插件系统加载并通过 `QGenericPluginFactory` 调用。

这个类的重点是“插件工厂入口”，不是普通业务对象。你实现的 `create()` 必须根据 key 和 specification 返回合适的 QObject，或者在无法处理时返回 `nullptr`。

## 2. 类说明

- 头文件：`#include <QGenericPlugin>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 核心虚函数：`create(const QString &key, const QString &specification)`

构造函数和析构函数一般由插件加载器管理。插件类通常配合 `Q_PLUGIN_METADATA` 和 Qt 插件目录部署。

## 3. API 速查

| API | 用途 |
|---|---|
| `QGenericPlugin(parent)` | 构造插件对象；通常由 Qt 自动调用。 |
| `~QGenericPlugin()` | 插件不再使用时由 Qt 销毁。 |
| `create(key, specification)` | 根据不区分大小写的 key 和附加 specification 创建 QObject。 |

## 4. 关键用法

```cpp
class MyGenericPlugin final : public QGenericPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QGenericPluginFactoryInterface")

public:
    QObject *create(const QString &key,
                    const QString &specification) override
    {
        if (key.compare(u"mydriver"_s, Qt::CaseInsensitive) == 0)
            return new MyDriver(specification);
        return nullptr;
    }
};
```

`key` 不区分大小写，但 `specification` 的语义由插件自己定义。它可能是设备路径、参数串、后端名称或空字符串。实现时不要假定它总是格式正确。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 提供 Qt GUI 可动态发现的底层驱动 | 从 `QGenericPlugin` 派生。 |
| 应用内部普通扩展点 | 使用显式工厂或插件接口，不必使用 Generic Plugin。 |
| 需要多个 key 对应多个 QObject 类型 | 在 `create()` 中分派，不支持的 key 返回 `nullptr`。 |
| 需要复杂配置 | 明确定义 `specification` 格式并做好解析失败处理。 |

## 6. 常见坑与经验

- 不要在插件构造函数里做昂贵初始化；Qt 可能只是探测插件。
- `create()` 返回的 QObject 所有权通常交给调用方/Qt 框架，不要返回栈对象。
- 不支持的 key 必须返回 `nullptr`，不要返回半初始化对象。
- 插件卸载时，已创建对象的生命周期必须清楚，避免对象仍在使用插件代码。
- 元数据 IID、导出宏、插件路径和部署结构错误时，工厂根本找不到插件。

## 7. 知识点覆盖

- Qt 通用插件入口与插件加载器
- key/specification 创建协议
- QObject 返回值所有权和失败处理
- 插件部署、元数据和按需初始化
- `QGenericPlugin` 与普通应用工厂的区别
