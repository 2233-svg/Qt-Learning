# Qt QXmlStreamEntityResolver：为 XML 流读取器提供实体替换策略

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamEntityResolver>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可继承的回调接口；函数可重入

## 它解决的问题

XML 文档可能引用未在文档内部声明的实体，例如：

```xml
<message>&companyName;</message>
```

如果 `QXmlStreamReader` 不知道 `companyName` 的替换文本，应用可以通过 `QXmlStreamEntityResolver` 提供一个受控的解析策略。它是一个很小的多态接口，核心职责只有一件事：收到实体名称，返回替换文本。

它适合把“XML 语法解析”和“实体名称如何映射到应用数据”分开。比如配置文件可以只允许一组白名单实体，文档转换器可以从内存字典读取替换值，而安全敏感程序可以对未知实体统一拒绝。

## 真实使用场景

### 使用内存白名单

```cpp
class EntityResolver final : public QXmlStreamEntityResolver
{
public:
    QString resolveUndeclaredEntity(const QString &name) override
    {
        if (name == u"companyName")
            return u"Example Inc."_qs;
        if (name == u"productName")
            return u"Qt Tool"_qs;
        return {};
    }
};

EntityResolver resolver;
QXmlStreamReader reader(device);
reader.setEntityResolver(&resolver);
```

返回空字符串表示解析器没有提供替换文本。默认实现始终返回空字符串，因此仅仅创建一个基类对象不会启用任何自定义实体解析。

### 从受控配置表解析

```cpp
class MapResolver final : public QXmlStreamEntityResolver
{
public:
    explicit MapResolver(QHash<QString, QString> values)
        : values_(std::move(values))
    {
    }

    QString resolveUndeclaredEntity(const QString &name) override
    {
        return values_.value(name);
    }

private:
    QHash<QString, QString> values_;
};
```

解析器应只访问内存或明确允许的资源。不要把 `name` 直接拼接成本地路径、网络地址或脚本命令。

## 返回值语义非常关键

`resolveUndeclaredEntity()` 返回 `QString`：

- 非空字符串：作为该实体的替换文本返回；
- 空字符串：表示 resolver 不认识该实体。

因此，空字符串同时也是“无法解析”的信号，不适合用来表达一个确实需要替换成空文本的实体。若协议必须区分这两种情况，实体命名规则或上层文档格式需要另行设计。

回调收到的是实体名称，不是带 `&` 和 `;` 的完整引用。例如 `&companyName;` 回调参数是 `companyName`。不要在 resolver 中再次把名称包成实体引用返回；返回的是替换文本本身。

## 它只处理“未声明实体”

接口名称是 `resolveUndeclaredEntity`。已知的内置实体或已经由 DTD 声明的实体，不应假设都会经过这个回调。resolver 不是通用的字符转义器，也不是 XML 文本预处理器。

如果目标只是把 `&lt;`、`&amp;` 等写入 XML，应使用 `QXmlStreamWriter::writeCharacters()`，不要手动用 resolver 参与转义。

## 生命周期和所有权

`QXmlStreamReader::setEntityResolver()` 接受一个指针。resolver 通常由调用方在栈上或更长生命周期的对象中持有；reader 不应被理解为接管这个对象的所有权。resolver 必须至少活到 reader 不再需要回调：

```cpp
EntityResolver resolver;
{
    QXmlStreamReader reader(device);
    reader.setEntityResolver(&resolver);
    // 在 reader 生命周期内 resolver 有效
}
```

不要这样做：

```cpp
reader.setEntityResolver(new EntityResolver); // 所有权和释放责任不清晰
```

除非应用明确设计并管理堆对象的销毁，否则优先使用栈对象或拥有者成员。

析构函数是虚函数且 `noexcept`，因此可以通过基类指针安全销毁派生对象。派生类析构也应保持不抛异常。

## 线程和重入

Qt 文档标注本类函数可重入。这个属性表示不同对象可以在多个线程中独立使用，不表示一个 resolver 的回调可以被多个线程同时调用而无需同步。

若 resolver 读取共享 `QHash`、数据库连接或网络客户端，需由应用提供同步或线程隔离。回调应尽量短、确定、无阻塞；不要在 reader 解析过程中执行不可控的网络访问，否则会把外部资源延迟和失败直接引入 XML 解析流程。

## 继承接口的设计建议

派生类只需覆盖 `resolveUndeclaredEntity()`。建议遵循以下约束：

1. 明确允许解析的实体白名单；
2. 对名称做精确匹配，不做模糊替换；
3. 不把名称直接解释为路径或代码；
4. 未知名称返回空字符串；
5. 不在回调中修改 reader 或递归触发另一轮 XML 解析；
6. 若共享状态可能被并发访问，使用锁或不可变快照。

## API 逐项说明

### `virtual ~QXmlStreamEntityResolver()`

虚析构函数，声明为 `noexcept`。它允许通过 `QXmlStreamEntityResolver *` 删除派生 resolver。基类不拥有外部设备或资源；派生类若持有资源，应按普通 C++ RAII 规则管理。

### `virtual QString resolveUndeclaredEntity(const QString &name)`

解析未声明实体并返回替换文本。基类默认实现始终返回空字符串。派生类应覆盖它，根据 `name` 返回受控的替换内容；未知名称返回空字符串。

参数不含 `&` 和 `;`。返回值是拥有型 `QString`，因此派生类可以从局部变量或内部表安全返回；但不要把未验证的外部数据直接当作可信 XML 片段。

## API 速查表

| 类别 | API | 用途 | 关键边界 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QXmlStreamEntityResolver() noexcept` | 通过基类接口安全销毁派生对象 | reader 通常只保存指针引用；resolver 必须先于 reader 或不晚于 reader 需求结束而存在。 |
| 扩展点 | `virtual QString resolveUndeclaredEntity(const QString &name)` | 把未声明实体名称映射为替换文本 | 参数不含 `&`、`;`；空返回表示未知；默认实现始终返回空字符串。 |

### 一句话总结

`QXmlStreamEntityResolver` 是 `QXmlStreamReader` 的实体回调接口：用白名单或受控内存表解析未声明实体，未知名称返回空字符串，resolver 的生命周期必须覆盖 reader 的回调期，并且不能把实体名直接当作路径或代码。
