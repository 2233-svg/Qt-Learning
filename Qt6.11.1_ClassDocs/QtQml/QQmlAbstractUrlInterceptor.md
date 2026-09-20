# QQmlAbstractUrlInterceptor
> Qt 6.11.1 · Qt QML · 来自 `QQmlAbstractUrlInterceptor`

## 作用定位

`QQmlAbstractUrlInterceptor` 是 QML 资源 URL 重写接口。把实现对象加到 `QQmlEngine` 后，引擎加载 QML、JavaScript、qmldir 或解析 QML 中 URL 属性时，会先调用 `intercept()`，允许你把原 URL 改写成另一个 URL。

它适合资源重定向、主题/平台变体、沙盒路径映射、热更新资源定位等场景。

## 类说明

- 头文件：`#include <QQmlAbstractUrlInterceptor>`
- CMake：链接 `Qt6::Qml`
- 继承：接口类
- 注册入口：`QQmlEngine::addUrlInterceptor()`

## API 速查

| API | 说明 |
| --- | --- |
| `DataType::QmlFile` | 被拦截的是 QML 文件 URL。 |
| `DataType::JavaScriptFile` | 被拦截的是导入的 JS 文件。 |
| `DataType::QmldirFile` | 被拦截的是 qmldir 文件，可用于替换模块子树。 |
| `DataType::UrlString` | 被拦截的是 QML 里普通 URL 属性，不一定会被引擎加载。 |
| `intercept(url, type)` | 返回改写后的 URL；返回原 URL 表示不改写。 |

## 使用场景

- 将磁盘路径重定向到 `qrc:/` 资源或缓存目录。
- 按设备、语言、主题选择不同 QML 文件。
- 记录 QML 资源加载路径，辅助调试。
- 给插件系统做资源命名空间隔离。

## 常见坑与经验

- 拦截器会影响引擎加载路径，必须在加载 QML 前安装。
- `QmlFile` 和 `QmldirFile` 含义不同：前者替换单个文件，后者可能改变整个模块目录。
- 不要在 `intercept()` 里做慢 I/O；它可能处在加载关键路径。
- URL 重写要保持相对路径关系，否则 QML 内部 import 和图片路径可能断掉。
- 多个拦截器同时存在时，顺序会影响最终 URL，要保持规则简单可预测。

## 知识点覆盖

- QML 资源 URL 拦截
- qmldir、QML 文件、JS 文件区别
- 资源重定向和文件选择
- 加载路径调试
