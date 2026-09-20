# QSqlDriverPlugin 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlDriverPlugin>`  
> 所属模块：`Qt6::Sql`  
> 继承：`QObject`

## 它解决什么问题

`QSqlDriverPlugin` 是动态 SQL driver 插件的抽象基类。它让 Qt 在运行时从插件目录加载数据库驱动，而应用不必在启动代码中手工调用 `QSqlDatabase::registerSqlDriver()`。

一个 SQL driver 插件需要三部分：

1. 一个 `QSqlDriver` 子类，完成数据库协议实现；
2. 一个 `QSqlDriverPlugin` 子类，按 key 创建对应 driver；
3. `Q_PLUGIN_METADATA` 导出的 JSON 元数据，列出支持的 driver key。

```cpp
class MySqlPlugin final : public QSqlDriverPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QSqlDriverFactoryInterface"
                      FILE "mysqldriver.json")

public:
    QSqlDriver *create(const QString &key) override
    {
        if (key == "MYDB")
            return new MyDriver;
        return nullptr;
    }
};
```

## key 是插件发现契约

`create(key)` 的 key 通常是所需 driver 的类名或注册名，并且大小写敏感。JSON 元数据中的 key、`create()` 中接受的 key，以及应用调用 `QSqlDatabase::addDatabase()` 时传入的 driver 名必须一致。

若元数据声明支持某 key，但 `create()` 返回空指针，应用会在创建连接时失败。反过来，`create()` 支持但元数据没有声明的 key，也不会被插件加载器正确发现。

## 生命周期与所有权

插件对象通常由 Qt 的插件加载系统实例化和销毁，应用不应手工构造或删除它。`create()` 返回的 `QSqlDriver *` 由 Qt SQL 连接体系接管；每次创建连接应返回独立 driver。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlDriverPlugin(QObject *parent = nullptr)` | 构造 SQL driver 插件对象。 | 通常由 Qt 插件加载机制和 moc 生成代码调用，应用不直接实例化。 |
| 析构 | `~QSqlDriverPlugin()` | 销毁插件对象。 | Qt 在插件不再使用时管理销毁，不能由应用手工释放。 |
| 创建 driver | `create(const QString &key)` | 根据大小写敏感的 key 创建并返回对应 `QSqlDriver`。 | 纯虚函数；未支持的 key 返回 `nullptr`，支持 key 时每次返回新实例。 |

## 易错点

1. JSON 元数据 key、`create()` 判断和 `addDatabase()` 名称必须完全一致且区分大小写。
2. 插件类不是 driver，真正执行数据库操作的是返回的 `QSqlDriver`。
3. `create()` 应创建新对象，不要返回共享 driver。
4. 静态注册与动态插件是两条路径：前者用 `QSqlDriverCreator`，后者用本类。

### 一句话总结

`QSqlDriverPlugin` 是 Qt 动态发现 SQL driver 的入口：它通过插件元数据声明支持的 key，并按 key 创建新的 `QSqlDriver`。
