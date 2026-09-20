# QIconEnginePlugin

> Qt 6.11.1 · Qt GUI · 来自 `QIconEnginePlugin`

## 1. 先建立直觉

`QIconEnginePlugin` 是 `QIconEngine` 的发现工厂。Qt 根据图标文件的后缀/插件元数据加载它，并调用 `create(filename)` 获得一个能解释该文件的图标引擎。

普通应用无需手动调用这个类；它只服务于扩展 Qt 图标格式的插件作者。若图标来自 SVG、PNG、资源文件或主题，直接构造 `QIcon` 更简单。

## 2. 类说明

- 头文件：`#include <QIconEnginePlugin>`
- CMake：`target_link_libraries(plugin PRIVATE Qt6::Gui)`
- 继承：`QObject` 与 Qt 图标引擎工厂接口。
- 核心职责：由 `create()` 为某个文件创建独立 `QIconEngine`；plugin 自身不负责逐次绘制。
- 通过 `Q_PLUGIN_METADATA` 与 JSON 元数据被 Qt 发现；动态插件路径与依赖部署正确才会生效。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QIconEnginePlugin(parent)` | 创建插件 QObject，通常由 Qt plugin loader 管理 |
| `create(filename)` | 必须实现：根据文件名创建新的 `QIconEngine` |
| `Q_PLUGIN_METADATA` | 声明插件 IID 与 JSON 信息，供 Qt 发现 |
| JSON `Keys` | 声明插件处理的文件后缀/键 |
| `QIconEngine::key()` | engine 返回的稳定类型标识，辅助序列化和诊断 |

## 4. 关键用法

```cpp
class AcmeIconPlugin final : public QIconEnginePlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QIconEngineFactoryInterface"
                      FILE "acmeicon.json")

public:
    QIconEngine *create(const QString &filename) override
    {
        if (filename.isEmpty())
            return new AcmeIconEngine;
        return AcmeIconEngine::fromFile(filename);
    }
};
```

`create()` 每次都应返回一个新的 engine，或在失败时返回空指针。不要让所有 `QIcon` 共用一个会变的 engine：`QIcon` 是值类型，资源、状态、缓存和生命周期都应隔离。

示例元数据：

```json
{
  "Keys": [ "aicon" ]
}
```

键与文件扩展名/格式发现路径匹配。实际 IID、插件目录和部署方式要以当前 Qt 插件接口和构建系统为准。

## 5. 使用场景

- 将专有矢量图标容器接入 `QIcon("file.aicon")`。
- 向设计资产管线提供可参数化、可多状态生成的图标格式。
- 让插件在不改应用业务代码的前提下扩展图标加载能力。

## 6. 常见坑与经验

- **不要用 plugin 承担图标渲染。** 渲染、DPR、Mode/State 选择都应在返回的 `QIconEngine` 内完成。
- **plugin JSON 与二进制部署缺一不可。** 开发环境可用、发布版失效通常是插件目录、依赖库或元数据 key 的问题。
- **QObject 不代表自动线程安全。** 避免 plugin 实例里持有未同步的可变全局缓存；engine 也应按 GUI 资源规则使用。
- **`filename` 不能盲信。** 私有图标格式也应验证头部、尺寸和输入范围，不能只按后缀解析。
- **不要直接析构 Qt 创建/管理的 plugin。** 交给 plugin loader 的生命周期机制；你的责任是正确返回 engine。

## 7. 知识点覆盖

Qt 动态插件、工厂模式、QObject 生命周期、图标格式发现、JSON 元数据、QIconEngine 分层、发布部署、输入验证。
