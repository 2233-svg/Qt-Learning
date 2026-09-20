# QQmlError
> Qt 6.11.1 · Qt QML · 来自 `QQmlError`

## 作用定位

`QQmlError` 是 QML 加载、编译、绑定求值和运行时警告的定位信息容器。它不仅有描述文本，还包含 URL、行、列、关联对象和消息级别，因此比普通字符串更适合错误面板、日志和 IDE 集成。

## 类说明

- 头文件：`#include <QQmlError>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 常见来源：`QQmlComponent::errors()`、`QQmlExpression::error()`、`QQmlEngine::warnings()`

## API 速查

| API | 说明 |
| --- | --- |
| `isValid()` | 是否包含有效错误。 |
| `description()` / `setDescription()` | 错误文字。 |
| `url()` / `setUrl()` | 出错 QML 文件或资源 URL。 |
| `line()` / `setLine()` | 行号。 |
| `column()` / `setColumn()` | 列号。 |
| `object()` / `setObject()` | 关联 QObject，常用于运行时绑定错误。 |
| `messageType()` / `setMessageType()` | `QtMsgType` 级别，如 warning、critical。 |
| `toString()` | 生成可直接打印的错误文本。 |
| `operator<<` | 用 `QDebug` 输出错误。 |

## 使用场景

- 打印 QML 组件加载失败原因。
- 在自定义编辑器中跳转到错误行列。
- 收集 `QQmlEngine::warnings()` 做统一日志。
- 把运行期绑定错误关联回对象和源文件。

## 常见坑与经验

- 多个错误要逐条输出，不能只看第一条；一个 import 失败常伴随多个下游错误。
- URL 可能是 `qrc:/`、本地文件、网络 URL 或内存数据 URL，错误展示要支持多种来源。
- 行列号可能为 `-1` 或 0，表示无法定位，不要直接当数组索引用。
- `description()` 是给人看的文本，不适合做程序分支条件。
- 自己构造错误时，把 URL/line/column 填上，后续排查成本会低很多。

## 知识点覆盖

- QML 错误定位
- 编译错误、运行时警告、绑定错误
- `QtMsgType` 与日志级别
- 错误对象到字符串输出
