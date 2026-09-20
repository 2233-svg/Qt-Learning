# QSqlDriverPlugin
> Qt 6.11.1 · Qt SQL · 来自 `QSqlDriverPlugin`

## 1. 先建立直觉

`QSqlDriverPlugin` 是 Qt SQL 驱动插件的基类。它让驱动可以作为插件部署，应用只要能找到插件，就能通过 `QSqlDatabase::addDatabase("KEY")` 使用对应数据库后端。

如果 `QSqlDriverCreator` 是“编译进程序的注册”，`QSqlDriverPlugin` 就是“按 Qt 插件机制发现和加载”。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlDriverPlugin`，属于 Qt SQL 模块，用于实现可动态加载的 SQL driver 插件。

派生类要实现 `create(key)`，根据 key 返回对应 `QSqlDriver`。插件还需要 Qt 插件元数据，才能被插件加载器识别。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlDriverPlugin(parent)` | 创建插件对象。 |
| `~QSqlDriverPlugin()` | 虚析构。 |
| `create(const QString &key)` | 根据驱动 key 创建 `QSqlDriver`。 |

## 4. 典型流程

```cpp
class MySqlPlugin : public QSqlDriverPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QSqlDriverFactoryInterface")

public:
    QSqlDriver *create(const QString &key) override
    {
        if (key.compare("MYDRIVER", Qt::CaseInsensitive) == 0)
            return new MyDriver;
        return nullptr;
    }
};
```

## 5. 使用场景

| 场景 | 为什么用插件 |
| --- | --- |
| 驱动依赖可选第三方库 | 用户安装相应插件才启用。 |
| 多数据库后端按需部署 | 减少主程序依赖和体积。 |
| 给 Qt 应用生态提供驱动 | 遵循 Qt 插件搜索路径。 |

## 6. 常见坑与经验

插件能否被发现，取决于目录结构、插件元数据、Qt 版本 ABI、编译器和依赖库。`drivers()` 看不到时，不一定是代码错，可能是部署路径或 DLL 依赖缺失。

`create()` 可能被多次调用，每次都应返回新的 driver 实例。不要返回同一个全局 driver 给多个连接共用。

驱动 key 大小写处理要宽容，但文档和部署中要固定一个正式名称。

## 7. 知识点覆盖

- Qt SQL driver 插件机制。
- 插件元数据、key 和 driver 创建。
- 插件部署、依赖库和 ABI 兼容。
- 插件式驱动与静态注册的取舍。
