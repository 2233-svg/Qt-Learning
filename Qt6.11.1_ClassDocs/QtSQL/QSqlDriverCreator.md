# QSqlDriverCreator
> Qt 6.11.1 · Qt SQL · 来自 `QSqlDriverCreator`

## 1. 先建立直觉

`QSqlDriverCreator<T>` 是 `QSqlDriverCreatorBase` 的模板实现。你把自己的 `QSqlDriver` 子类作为模板参数，它就能在 Qt 需要时创建对应驱动对象。

它是注册内置式自定义驱动的省代码工具，不是插件系统本身。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlDriverCreator`，属于 Qt SQL 模块，用于按模板类型创建 SQL driver。

`T` 必须是 `QSqlDriver` 派生类，并且有适合无参创建的构造方式。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `createObject() const` | 重写基类工厂函数，返回 `new T`。 |

## 4. 典型流程

```cpp
class MyDriver : public QSqlDriver
{
    // 实现 open/close/createResult/hasFeature...
};

QSqlDatabase::registerSqlDriver(
    "MYDRIVER",
    new QSqlDriverCreator<MyDriver>);
```

## 5. 使用场景

| 场景 | 建议 |
| --- | --- |
| 驱动编译进应用 | 用 `registerSqlDriver()` + `QSqlDriverCreator<T>`。 |
| 驱动需要动态加载 | 写 `QSqlDriverPlugin`。 |
| 驱动构造需要复杂参数 | 自己派生 `QSqlDriverCreatorBase`，在 `createObject()` 中处理。 |

## 6. 常见坑与经验

模板 creator 默认只解决“怎么 new driver”。如果你的 driver 依赖连接句柄、license、全局上下文等，仍要设计 driver 自身的初始化流程。

驱动名要避免和 Qt 内置驱动重名。重名会让排查加载路径和实际驱动变得混乱。

## 7. 知识点覆盖

- 模板工厂注册自定义 SQL driver。
- 内置注册和插件注册的区别。
- driver 构造约束和命名策略。
