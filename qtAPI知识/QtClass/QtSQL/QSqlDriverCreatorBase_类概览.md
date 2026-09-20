# QSqlDriverCreatorBase 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlDriverCreatorBase>`  
> 所属模块：`Qt6::Sql`  
> 继承：无

## 它解决什么问题

`QSqlDriverCreatorBase` 是为 `QSqlDatabase` 注册自定义 SQL driver 时使用的抽象工厂接口。`QSqlDatabase` 需要在创建连接时得到一个新的 `QSqlDriver` 实例，而这个类把“如何创建具体 driver”抽象成 `createObject()`。

它适用于没有以动态插件方式发布 driver、而是由应用在启动时显式注册 driver 的场景：

```cpp
QSqlDatabase::registerSqlDriver(
    "MYDB",
    new QSqlDriverCreator<MyDriver>);
```

大多数情况直接使用模板类 `QSqlDriverCreator<T>`，不需要手写派生类。只有 driver 构造需要额外策略、配置或依赖注入时，才继承 `QSqlDriverCreatorBase` 自己实现工厂。

## 创建责任与生命周期

`createObject()` 必须每次返回一个新的 `QSqlDriver` 实例，不能返回同一个共享 driver。数据库连接各自维护状态，例如事务、最后错误、结果集和连接参数；复用一个 driver 会让不同连接彼此污染。

创建出的 driver 所有权交给 Qt SQL 连接体系。工厂本身则是在 `registerSqlDriver()` 时传给 Qt 的对象，不要在注册后同时由别的智能指针或手工 `delete` 管理。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QSqlDriverCreatorBase()` | 销毁 SQL driver 工厂接口。 | 已注册给 Qt 的 creator 不应再由调用方重复释放。 |
| 创建 driver | `createObject() const` | 创建并返回一个新的 `QSqlDriver` 子类实例。 | 纯虚函数；每次调用都应返回独立、可用的 driver，所有权交给 Qt SQL。 |

## 易错点

1. 这是 driver 工厂，不是数据库连接本身。
2. `createObject()` 不能缓存并返回同一个 driver 实例。
3. 常规 driver 直接用 `QSqlDriverCreator<T>` 更简单。
4. 动态插件 driver 应继承 `QSqlDriverPlugin`，不是这个工厂基类。

### 一句话总结

`QSqlDriverCreatorBase` 是 `QSqlDatabase` 注册自定义 driver 的抽象工厂：它负责为每个连接创建新的 `QSqlDriver` 实例。
