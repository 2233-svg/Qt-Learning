# QProperty
> Qt 6.11.1 · Qt Core · 来自 `QProperty`

## 作用定位
`QProperty<T>` 是 Qt C++ 响应式属性的存储类型。它可保存普通值、安装计算绑定、通知订阅者，并在依赖属性变化时自动重算。

## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 读取当前值，必要时触发绑定求值。|
| `setValue()` | 设置显式值并移除绑定。|
| `setBinding()` | 安装派生计算绑定。|
| `binding()` | 查询当前绑定。|
| `takeBinding()` | 移除并取回绑定。|
| `hasBinding()` | 判断是否由绑定驱动。|
| `onValueChanged()` | 注册变化处理器。|
| `bindable()` | 返回 `QBindable<T>` 句柄。|

## 使用场景
在纯 C++ 领域对象中建立 `total = price * quantity` 这类自动更新关系，或作为 QObject/QML 属性的内部存储。

## 常见坑与经验
- `setValue()` 会打破现有 binding；UI 或业务层不应有多个无协调的写入来源。
- 绑定函数应避免网络访问、写数据库、修改其他属性等副作用。
- 依赖关系过深或形成循环时很难调试，应把计算分层并保持单向数据流。

## 知识点覆盖
响应式属性、绑定、依赖图、订阅、单向数据流、绑定覆盖、C++/QML 集成。
