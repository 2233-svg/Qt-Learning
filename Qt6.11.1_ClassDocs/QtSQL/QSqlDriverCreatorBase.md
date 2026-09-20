# QSqlDriverCreatorBase
> Qt 6.11.1 · Qt SQL · 来自 `QSqlDriverCreatorBase`

## 1. 先建立直觉

`QSqlDriverCreatorBase` 是自定义 SQL 驱动创建器的抽象基类。`QSqlDatabase::registerSqlDriver()` 需要的就是这种创建器：Qt 根据驱动名请求它 new 出一个 `QSqlDriver` 实例。

普通数据库应用几乎不会用它；只有你要注册自定义驱动，或把非标准数据库后端接入 Qt SQL 时才需要。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlDriverCreatorBase`，属于 Qt SQL 模块，用于抽象 SQL driver 工厂。

它只有一个核心纯虚函数 `createObject()`。模板类 `QSqlDriverCreator<T>` 是它最常用的实现。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `~QSqlDriverCreatorBase()` | 虚析构，允许通过基类指针销毁创建器。 |
| `createObject() const` | 创建一个新的 `QSqlDriver` 实例。 |

## 4. 典型流程

```cpp
QSqlDatabase::registerSqlDriver(
    "MYDRIVER",
    new QSqlDriverCreator<MyDriver>);

QSqlDatabase db = QSqlDatabase::addDatabase("MYDRIVER");
```

Qt 会接管传给 `registerSqlDriver()` 的 creator 指针。

## 5. 常见坑与经验

创建器负责创建 driver，不负责打开连接。连接参数仍由 `QSqlDatabase` 传给 driver 的 `open()`。

如果 driver 需要外部库初始化，要明确初始化时机和线程规则。不要把昂贵初始化藏在每次 `createObject()` 中反复执行。

## 6. 知识点覆盖

- 自定义 SQL 驱动注册机制。
- driver 工厂对象和 `QSqlDatabase::addDatabase()` 的关系。
- 基类工厂与模板工厂的分工。
