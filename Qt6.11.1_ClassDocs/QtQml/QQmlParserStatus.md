# QQmlParserStatus
> Qt 6.11.1 · Qt QML · 来自 `QQmlParserStatus`

## 作用定位

`QQmlParserStatus` 是自定义 QML 类型感知创建阶段的接口。对象由 QML 创建时，引擎会先调用 `classBegin()`，等所有属性、子对象和绑定初始化到合适阶段后再调用 `componentComplete()`。

它解决的问题是：构造函数太早，很多 QML 属性还没赋值；你需要等 QML 组件完整后再启动逻辑。

## 类说明

- 头文件：`#include <QQmlParserStatus>`
- CMake：链接 `Qt6::Qml`
- 继承：接口类；实际类型通常也继承 QObject
- 必须实现：`classBegin()`、`componentComplete()`
- 使用：类声明中通常需要 `Q_INTERFACES(QQmlParserStatus)`

## API 速查

| API | 说明 |
| --- | --- |
| `classBegin()` | QML 开始创建对象时调用，适合暂停自动启动或初始化内部标志。 |
| `componentComplete()` | QML 组件完成后调用，适合读取最终属性并开始工作。 |

## 使用场景

- 自定义 QML 类型需要等属性赋值后再连接资源。
- 组件内有子对象列表，必须等子对象全部构建后布局或计算。
- 避免构造函数里读取仍为默认值的 QML 属性。

## 常见坑与经验

- 构造函数只做 C++ 基础初始化，不要假设 QML 属性已经可用。
- `componentComplete()` 可能在对象树复杂时较晚执行，启动外部操作要考虑取消和析构。
- C++ 手动 new 这个类型时，QML 引擎不会自动调用这两个函数；不要把唯一初始化放在接口回调里。
- `QQuickItem` 已经实现/使用该机制，自定义 Item 要理解父类生命周期。

## 知识点覆盖

- QML 对象创建生命周期
- 构造函数与属性赋值顺序
- 组件完成回调
- 自定义 QML 类型初始化策略
