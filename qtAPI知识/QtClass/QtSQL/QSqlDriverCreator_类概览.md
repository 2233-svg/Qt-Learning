# QSqlDriverCreator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlDriverCreator>`  
> 所属模块：`Qt6::Sql`  
> 继承：`QSqlDriverCreatorBase`

## 它解决什么问题

`QSqlDriverCreator<T>` 是 `QSqlDriverCreatorBase` 的模板实现，用最少代码为特定 `QSqlDriver` 子类提供工厂。它默认在 `createObject()` 中执行 `new T`，避免每个自定义 driver 都重复写一个只会构造对象的 factory。

```cpp
class MyDriver final : public QSqlDriver
{
    // 实现 QSqlDriver 的连接、执行、事务等接口。
};

QSqlDatabase::registerSqlDriver(
    "MYDB",
    new QSqlDriverCreator<MyDriver>);
```

当之后调用 `QSqlDatabase::addDatabase("MYDB")` 时，Qt SQL 通过这个 creator 建立一个新的 `MyDriver`。

## 适用条件

模板参数 `T` 必须是 `QSqlDriver` 的可默认构造子类。若 driver 需要构造参数，例如配置对象、凭据提供者或连接池句柄，`QSqlDriverCreator<T>` 不适合；应派生 `QSqlDriverCreatorBase`，在 `createObject()` 中按自己的规则构造。

它解决的是 **静态注册**。若希望 driver 作为共享库被 Qt 自动发现和加载，应实现 `QSqlDriverPlugin` 并导出插件元数据。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 创建 driver | `createObject() const` | 创建并返回一个新的模板参数 `T` 实例。 | `T` 必须可默认构造且继承 `QSqlDriver`；每个连接会得到独立 driver。 |

## 易错点

1. `QSqlDriverCreator<T>` 不是 SQL driver 本身，它只负责构造 driver。
2. `T` 若需要构造参数，就应改用自定义 `QSqlDriverCreatorBase`。
3. 注册 key 必须与 `QSqlDatabase::addDatabase()` 使用的 driver 名匹配。
4. 动态发现的 driver 用 `QSqlDriverPlugin`，不是注册 creator。

### 一句话总结

`QSqlDriverCreator<T>` 是默认构造型 SQL driver 的简洁工厂模板，专门配合 `QSqlDatabase::registerSqlDriver()` 使用。
