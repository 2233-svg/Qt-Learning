# QQmlFileSelector
> Qt 6.11.1 · Qt QML · 来自 `QQmlFileSelector`

## 作用定位

`QQmlFileSelector` 把 `QFileSelector` 集成到 `QQmlEngine`，让 QML 文件加载自动选择带 selector 的变体文件。例如按平台、语言、主题、屏幕密度加载不同版本资源。

它本质上是一个预置 URL 选择/拦截机制。

## 类说明

- 头文件：`#include <QQmlFileSelector>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 构造时绑定 `QQmlEngine`

## API 速查

| API | 说明 |
| --- | --- |
| `QQmlFileSelector(engine, parent)` | 给指定 QML 引擎安装文件选择能力。 |
| `selector()` | 返回内部或当前使用的 `QFileSelector`。 |
| `setSelector()` | 替换选择器对象。 |
| `setExtraSelectors()` | 增加额外 selector，如 `"dark"`、`"tablet"`。 |

## 使用场景

- 按平台加载 `+android`、`+windows` 等 QML 变体。
- 按主题加载 `+dark`、`+light` 资源。
- 产品线或客户定制版本共享一套 QML 入口。

## 常见坑与经验

- 要在加载 QML 前创建并配置 selector；加载后已缓存组件不会自动换文件。
- selector 规则会影响 QML、图片、JS 等资源路径，目录结构要统一规划。
- 额外 selector 顺序和 QFileSelector 规则会影响命中结果。
- 如果只想替换少量 URL，URL interceptor 可能比全局 file selector 更直观。

## 知识点覆盖

- QFileSelector 与 QML 集成
- 资源变体目录
- 主题/平台文件选择
- 加载前配置的重要性
