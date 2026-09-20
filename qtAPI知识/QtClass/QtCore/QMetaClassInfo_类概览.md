# Qt QMetaClassInfo 类级静态元数据笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaClassInfo>`  
> 所属模块：`Qt6::Core`  
> 类型性质：引用 `QMetaObject` 中一条类信息键值的轻量句柄  
> 相关类型：`QMetaObject`、`QObject`、`Q_GADGET`、`Q_CLASSINFO`

## 1. 它解决什么问题

`QMetaClassInfo` 表示 Qt 元对象中的一条类级别信息：

```text
name  ->  value
```

信息由 `Q_CLASSINFO(Name, Value)` 宏在类的元对象中声明，之后通过 `QMetaObject` 按索引读取：

```cpp
class Plugin : public QObject
{
    Q_OBJECT
    Q_CLASSINFO("author", "Example Team")
    Q_CLASSINFO("protocol", "v2")
};

const QMetaObject &meta = Plugin::staticMetaObject;
const int index = meta.indexOfClassInfo("protocol");
if (index >= 0) {
    const QMetaClassInfo info = meta.classInfo(index);
    qDebug() << info.name() << info.value();
}
```

它适合把不会频繁变化、需要随类型一起编译进元对象的描述信息暴露给：

- 插件发现和工具链；
- Qt Designer、QML 或其他反射工具；
- RPC、序列化、脚本桥接的静态约定；
- 测试和诊断代码；
- 自定义框架读取类级别标签。

### 1.1 它不是什么

`QMetaClassInfo` 不是：

- 可修改的运行时字典；
- `QVariantMap` 或 `QHash<QString, QString>`；
- QObject 实例属性，实例属性应使用 `QMetaProperty`；
- 方法、信号或槽的描述，方法信息应使用 `QMetaMethod`；
- 独立拥有字符串存储的对象；
- 自动把任意 C++ 注释、变量或配置文件变成元数据的工具。

## 2. 实际使用场景

### 2.1 读取插件的静态描述

```cpp
const QMetaObject &meta = plugin->metaObject();
const int index = meta.indexOfClassInfo("protocol");

if (index >= 0) {
    const QByteArray protocol =
        meta.classInfo(index).value();
    if (protocol == "v2")
        useV2Protocol(plugin);
}
```

`QMetaClassInfo` 只提供信息条目的读取；查找名称、判断是否存在、处理索引都由 `QMetaObject` 负责。

### 2.2 读取全部类信息

```cpp
const QMetaObject &meta = Plugin::staticMetaObject;
for (int i = 0; i < meta.classInfoCount(); ++i) {
    const QMetaClassInfo info = meta.classInfo(i);
    qDebug().noquote()
        << info.name() << '=' << info.value();
}
```

`classInfoCount()` 和 `classInfo(i)` 的索引范围必须配套。越界索引不应被当作有效信息读取。

### 2.3 处理继承层级中的类信息

```cpp
const QMetaObject *meta = object->metaObject();
for (const QMetaObject *current = meta;
     current; current = current->superClass()) {
    for (int i = current->classInfoOffset();
         i < current->classInfoCount(); ++i) {
        const QMetaClassInfo info = current->classInfo(i);
        consume(current->className(), info);
    }
}
```

`QMetaObject` 的总索引空间可能包含继承类的信息；`classInfoOffset()` 用于取得当前类自己新增条目的起点。具体遍历策略要明确是“所有继承层级”还是“只看当前类”。

### 2.4 读取框架约定的键

```cpp
const int index = meta.indexOfClassInfo("factory");
if (index >= 0) {
    const QByteArray factoryName =
        meta.classInfo(index).value();
    createFactory(factoryName);
}
```

类信息常用于框架约定，但它只是静态字符串。读取后仍应校验值是否属于允许集合，不能把元数据直接当作可信配置或权限信息。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMetaClassInfo>
#include <QMetaObject>
#include <QObject>
#include <QDebug>
```

直接使用 `QMetaClassInfo` 的公共头即可；实际声明 `Q_CLASSINFO` 的类还必须使用 `Q_OBJECT` 或适用的元对象宏，并经过 `moc` 处理。

## 4. `Q_CLASSINFO` 如何生成条目

### 4.1 宏声明静态键值

```cpp
class Worker : public QObject
{
    Q_OBJECT
    Q_CLASSINFO("role", "worker")
    Q_CLASSINFO("threading", "dedicated")
};
```

`Q_CLASSINFO(Name, Value)` 的参数是编译期元数据文本。它们会被 `moc` 收集并放入该类的 `QMetaObject` 数据中。

这意味着：

- 修改类信息通常需要重新运行 `moc` 和重新编译；
- 运行时不能通过 `QMetaClassInfo` 的 setter 改名或改值；
- 值不是从对象实例成员读取的；
- 同一类可以声明多条信息；
- 名称是否重复、重复时由框架如何解释，应由项目约定明确。

### 4.2 `Q_GADGET` 也可以提供类信息

类级元对象不一定必须继承 `QObject`。使用 `Q_GADGET` 的值类型也可以暴露适用的元对象信息：

```cpp
class ValueType
{
    Q_GADGET
    Q_CLASSINFO("kind", "value")
};
```

读取时使用 `ValueType::staticMetaObject`。是否能使用实例相关 API 取决于该类型是否是 QObject，而 `QMetaClassInfo` 本身只读取静态类信息。

### 4.3 元数据值是文本

`name()` 和 `value()` 返回 `const char *`。如果业务需要数字、布尔或结构化配置，应把文本解析成目标类型并检查解析结果：

```cpp
bool ok = false;
const int version =
    QByteArray(info.value()).toInt(&ok);
if (!ok)
    rejectMetadata();
```

解析失败不能静默当成 0 或空值继续执行。

## 5. 句柄、所有权和生命周期

### 5.1 默认构造表示无效句柄

```cpp
const QMetaClassInfo invalid;
```

默认构造对象内部没有关联的 `QMetaObject` 条目。调用 `name()` 或 `value()` 得到的结果不应当被当作有效信息；先通过 `QMetaObject` 的合法索引取得 `QMetaClassInfo`。

### 5.2 对象不拥有字符串

`name()` 和 `value()` 返回指向元对象静态数据的指针。调用方不应释放，也不需要释放：

```cpp
const char *name = info.name();
const char *value = info.value();
```

这些指针通常可以在对应模块和程序生命周期内使用，但把它们保存为跨插件卸载边界的长期指针仍然不安全。若插件或动态库可能卸载，应复制为 `QByteArray` 或 `QString`。

### 5.3 它不是实例快照

```cpp
const QMetaClassInfo info = object->metaObject()->classInfo(index);
```

`info` 描述的是 `object` 的动态类型元对象中的静态条目，不保存 `object` 指针，也不会随对象属性变化。多个实例共享同一个类元对象时，读取到的类信息通常相同。

### 5.4 可拷贝的是句柄，不是元数据

`QMetaClassInfo` 是轻量的元对象句柄，可以作为值返回和保存；复制它不会复制一份字符串或创建一份独立元数据。其有效性仍依赖关联元对象以及动态库生命周期。

## 6. `QMetaObject` 中的索引语义

### 6.1 `classInfoCount()`

`QMetaObject::classInfoCount()` 返回当前元对象可访问的类信息总数，具体是否包含继承层级要结合 Qt 元对象的 offset 语义理解。调用 `classInfo(index)` 时，合法索引应满足：

```cpp
0 <= index && index < meta.classInfoCount()
```

### 6.2 `classInfoOffset()`

`classInfoOffset()` 标记当前类自己新增信息在元对象总表中的起始位置。遍历当前类直接声明的信息时常用：

```cpp
for (int i = meta.classInfoOffset();
     i < meta.classInfoCount(); ++i) {
    // 当前类新增的条目
}
```

如果要包含基类信息，应沿着 `superClass()` 分层遍历，而不是只依赖一个 offset。

### 6.3 `indexOfClassInfo(const char *)`

```cpp
const int index = meta.indexOfClassInfo("role");
```

找到时返回非负索引，找不到时返回负值。不要把返回值直接传给 `classInfo()`：

```cpp
const int index = meta.indexOfClassInfo(name);
if (index < 0)
    return;
const QMetaClassInfo info = meta.classInfo(index);
```

名称比较是元对象字符串比较，不是模糊匹配、大小写不敏感匹配或正则匹配。

### 6.4 同名信息的约定

Qt 元对象可以由类层级或多个宏产生多条条目。若项目允许重复 name，不要默认 `indexOfClassInfo()` 返回的条目就是唯一或最具体的条目。需要确定优先级时，按当前类/基类和索引范围显式实现策略。

## 7. 逐项 API 说明

### 7.1 `QMetaClassInfo()`

```cpp
constexpr QMetaClassInfo();
```

构造无效的默认句柄。它通常只用于：

- 声明稍后赋值的局部变量；
- 表达“没有找到条目”的占位状态；
- 泛型代码中提供默认可构造值。

它不会绑定到任何当前类，也不会读取调用方上下文。

### 7.2 `name() const`

```cpp
const char *name() const;
```

返回当前条目的名称，也就是 `Q_CLASSINFO(Name, Value)` 中的 `Name`：

```cpp
const QByteArray name = info.name();
```

返回值是非拥有的元对象字符串指针。无效句柄上的结果不应当被当作有效名称；通用代码应先确保 `info` 来自合法索引。

### 7.3 `value() const`

```cpp
const char *value() const;
```

返回当前条目的文本值，也就是 `Q_CLASSINFO(Name, Value)` 中的 `Value`：

```cpp
const QString value =
    QString::fromUtf8(info.value());
```

返回值不拥有存储，且始终是文本。需要转整数、布尔、URL 或结构化数据时，调用方必须执行明确解析和错误检查。

### 7.4 `enclosingMetaObject() const`

```cpp
const QMetaObject *enclosingMetaObject() const;
```

返回包含该条目的 `QMetaObject` 指针。它可用于回到所属类：

```cpp
if (const QMetaObject *owner = info.enclosingMetaObject())
    qDebug() << owner->className();
```

它返回的是元对象，不是 QObject 实例。默认构造或无效句柄的结果可能为 `nullptr`。

## 8. 读取模式和编码边界

### 8.1 用 `QByteArray` 保留原始 UTF-8/本地字节语义

元对象 API 返回 `const char *`，如果值来自 ASCII 或 UTF-8 约定，可以使用：

```cpp
const QByteArray rawValue(info.value());
```

如果项目约定非 ASCII 文本，明确使用 `QString::fromUtf8()` 或合适编码转换，不要在 Windows 上无条件使用本地 8 位编码。

### 8.2 不要修改返回指针

```cpp
// 错误：元对象字符串不是可写存储
// info.value()[0] = 'X';
```

返回类型虽然是 `const char *`，已经表达了只读契约。需要修改应复制到 `QByteArray` 或 `QString`。

### 8.3 不要把空字符串和缺失条目混为一谈

一个条目可以合法地拥有空值：

```cpp
Q_CLASSINFO("optional", "")
```

`indexOfClassInfo()` 找不到条目时返回负索引；找到条目后 `value()` 可能是空字符串。业务判断应先区分“有没有条目”，再判断“值是否为空”。

### 8.4 类信息不是安全配置

类信息通常来自编译进程，适合描述协议和工具行为，但不应替代签名校验、权限配置或运行时安全策略。插件提供的类信息也可能来自不可信模块，读取后仍需校验。

## 9. 常见错误与排查顺序

### 9.1 直接构造后读取 name/value

**症状：** 得到空指针或无意义值。

**原因：** `QMetaClassInfo()` 是无效句柄，不会自动绑定到当前类。

**修复：** 从 `QMetaObject::classInfo(index)` 取得实例，并检查 index 合法。

### 9.2 把 `Q_CLASSINFO` 当作运行时配置

**症状：** 修改配置文件或对象成员后，`value()` 仍然不变。

**原因：** `Q_CLASSINFO` 是由 `moc` 编译进元对象的静态字符串。

**修复：** 动态配置使用属性、配置对象或其他运行时存储；类信息只用于静态约定。

### 9.3 忽略 `indexOfClassInfo()` 的负返回值

**症状：** 无效索引传给 `classInfo()`，读取到错误条目或触发未定义行为。

**原因：** 查找失败不代表索引 0。

**修复：** 先检查 `index >= 0`，再读取。

### 9.4 把 value 当成整数或布尔

**症状：** `"false"` 被当成 true，或无效数字被当成 0。

**原因：** `value()` 只返回文本，不提供类型转换状态。

**修复：** 用带 `ok` 的解析 API，并明确接受的文本集合。

### 9.5 把返回指针保存过久

**症状：** 动态插件卸载后访问名称或值崩溃。

**原因：** 指针指向元对象所属模块的静态数据。

**修复：** 在模块仍加载时复制为 `QByteArray`/`QString`，再跨卸载边界保存。

### 9.6 只遍历 `classInfoCount()` 的前缀却误解继承关系

**症状：** 子类或基类的类信息漏读，或重复处理。

**原因：** `classInfoOffset()` 和 `superClass()` 决定信息属于哪个元对象层级。

**修复：** 明确只读当前类还是递归遍历继承链，并按 offset 选择范围。

### 9.7 假设名称唯一

**症状：** 多个框架标签同名时只读取到错误优先级的一个值。

**原因：** `QMetaClassInfo` 是条目，不是强制唯一键字典。

**修复：** 项目约定唯一性，或遍历所有匹配条目并定义冲突策略。

## 10. 推荐设计模板

### 10.1 安全读取一个键值

```cpp
std::optional<QByteArray> classInfoValue(
    const QMetaObject &meta,
    const char *name)
{
    const int index = meta.indexOfClassInfo(name);
    if (index < 0)
        return std::nullopt;

    const QMetaClassInfo info = meta.classInfo(index);
    if (!info.value())
        return QByteArray();

    return QByteArray(info.value());
}
```

返回拥有数据的 `QByteArray`，可以避免调用方继续依赖元对象字符串指针。

### 10.2 只遍历当前类新增信息

```cpp
void dumpOwnClassInfo(const QMetaObject &meta)
{
    for (int i = meta.classInfoOffset();
         i < meta.classInfoCount(); ++i) {
        const QMetaClassInfo info = meta.classInfo(i);
        qDebug().noquote()
            << info.name() << '=' << info.value();
    }
}
```

如果工具需要包含基类，沿着 `superClass()` 循环调用该函数，并明确输出类名。

### 10.3 为类信息定义稳定前缀

```cpp
Q_CLASSINFO("app.protocol.version", "2")
Q_CLASSINFO("app.plugin.role", "decoder")
```

使用命名空间式前缀可以降低不同库之间的名称冲突。它仍然只是项目约定，不会由 `QMetaClassInfo` 自动校验。

## API 速查表
### 11.1 `QMetaClassInfo` 本身

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMetaClassInfo()` | 构造无效元数据句柄 | 不会自动绑定当前类 |
| `name() const` | 返回信息名称 | 非拥有 `const char *`；来自元对象静态数据 |
| `value() const` | 返回信息文本值 | 需要调用方自行解析和校验 |
| `enclosingMetaObject() const` | 返回所属元对象 | 是 `QMetaObject`，不是 QObject 实例 |

### 11.2 `QMetaObject` 配套查找

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `classInfoCount() const` | 获取可访问类信息条目数 | 与 `classInfo(index)` 的合法范围配套 |
| `classInfoOffset() const` | 获取当前类自有条目的起点 | 处理继承层级时按 offset 遍历 |
| `classInfo(int index) const` | 按索引取得 `QMetaClassInfo` | 先验证 `0 <= index < count` |
| `indexOfClassInfo(const char *) const` | 按名称查找条目 | 找不到返回负值；不代表唯一业务键 |
| `superClass() const` | 沿继承链读取基类元对象 | 需要自己决定是否包含基类信息 |

### 11.3 声明侧

| 宏或类型 | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Q_CLASSINFO(Name, Value)` | 向类元对象添加静态键值信息 | 需要 `moc`；运行时不可修改 |
| `Q_OBJECT` | 为 QObject 类生成元对象 | 使类信息进入该类的 `staticMetaObject` |
| `Q_GADGET` | 为非 QObject 类型生成元对象能力 | 读取时使用类型的 `staticMetaObject` |

## 12. 一句话总结

`QMetaClassInfo` 是 `QMetaObject` 中一条静态类信息的轻量句柄：由 `Q_CLASSINFO` 和 `moc` 生成，`name()`/`value()` 返回非拥有文本，查找和继承范围由 `QMetaObject` 管理；它适合描述编译期约定，不是可变字典、实例属性或安全配置存储。
