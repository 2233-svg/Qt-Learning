# QQmlFileSelector：让 QML 自动选择平台或渠道版本的资源

> Qt 6.11.1 · `#include <QQmlFileSelector>` · 模块：`Qt6::Qml` · 基类：`QObject`

`QQmlFileSelector` 将 `QFileSelector` 接到 `QQmlEngine` 的 QML 与资源加载路径上。它解决同一份 QML 代码需要因平台、主题、品牌或测试开关而选择不同文件版本的问题。

例如 QML 始终引用 `Component.qml` 和 `asset.png`，Unix 平台可放置 `+unix/Component.qml`，macOS 可放置 `+mac/asset.png`。QML 中不必写平台分支，也不应改写每个相对路径。

## 基本用法

```cpp
#include <QQmlEngine>
#include <QQmlFileSelector>

QQmlEngine engine;
auto *selector = new QQmlFileSelector(&engine);
selector->setExtraSelectors({u"dark"_s, u"enterprise"_s});
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

构造函数会给 selector 配套一个内部 `QFileSelector`，并将这个 `QQmlFileSelector` 安装到 engine。**engine 接管 `QQmlFileSelector` 的所有权**，即便传入了不同的 QObject parent，也要按 engine 生命周期设计，避免之后手动重复删除。

## 资源选择的语义

选择器相当于替换被引用文件，而不是改变它内部的相对路径基准。组件仍可以统一引用 `asset.png`；不同版本的 QML 文件中也继续写同一个相对资源名，选择器会根据活跃 selector 找到对应的 `+selector/` 文件。

选择目录必须以 `+` 开头，所以正常项目目录不会被意外选中。系统默认 selector 来自 `QFileSelector`，可用 `setExtraSelectors()` 增补项目自己的变体，例如渠道、皮肤或受控实验标识。

一台 engine 同时只有一个 `QQmlFileSelector`；创建/安装新的会替换旧的。选择集合应在首次加载 QML 前确定，否则已经解析或缓存的资源与后来选择的版本可能不一致。

## 自定义 QFileSelector 的所有权

`setSelector(custom)` 可以换用自己的 `QFileSelector`，但 `QQmlFileSelector` **不拥有**这个 custom selector。必须让它至少活到 selector 停止使用它。调用 `setSelector(nullptr)` 会恢复内部 selector。

这与 `QQmlEngine` 拥有 `QQmlFileSelector` 本身的规则不同，是这类代码最容易出现重复释放或悬垂指针的地方。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlFileSelector(engine, parent)` | 安装 QML 文件选择器 | engine 取得该 QQmlFileSelector 所有权，并替换旧选择器。 |
| `selector()` | 取当前 QFileSelector | 可能是内部默认实例或外部替换实例。 |
| `setExtraSelectors(strings)` | 添加额外 selector | 适合无需自定义 QFileSelector 的项目变体。 |
| `setSelector(selector)` | 替换 QFileSelector | 不取得新 selector 所有权。 |
| `setSelector(nullptr)` | 恢复内部 selector | 重新使用构造时自带的 QFileSelector。 |
| `~QQmlFileSelector()` | 销毁选择器 | 通常由 engine 生命周期处理，不要重复删除。 |

文件选择适合静态变体资源，不适合承载复杂运行时策略。需要认证、下载或动态映射时，应使用更明确的 URL/网络扩展机制。
