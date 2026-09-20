# Qt QXmlStreamEntityDeclaration：DTD 实体声明的值对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamEntityDeclaration>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制、可比较的 XML 值类型；函数可重入

## 它解决的问题

DTD 可以声明实体，把一个名称映射到替换文本，或者映射到外部资源。`QXmlStreamEntityDeclaration` 把一条实体声明的组成部分放在同一个值对象中：

- `name()`：实体名称；
- `notationName()`：未解析实体关联的 notation 名称；
- `systemId()`：系统标识符；
- `publicId()`：公共标识符；
- `value()`：实体的替换文本。

它主要用于读取 DTD 信息，而不是用来构造或注册实体。`QXmlStreamReader::entityDeclarations()` 会在读取 DTD 时返回 `QXmlStreamEntityDeclarations`，也就是此类型的 `QList`。

## 真实使用场景

### 审计 DTD 中声明了什么

```cpp
QXmlStreamReader reader(device);

while (!reader.atEnd()) {
    reader.readNext();
    if (!reader.isDTD())
        continue;

    for (const QXmlStreamEntityDeclaration &entity
         : reader.entityDeclarations()) {
        qDebug() << "entity =" << entity.name()
                 << "value =" << entity.value()
                 << "systemId =" << entity.systemId();
    }
}

if (reader.hasError())
    qWarning() << reader.errorString();
```

这适合配置文件审计、格式转换和诊断工具。若应用本身不需要 DTD，通常应在 reader 层面采用更严格的安全策略，而不是把实体声明解析出来后再试图“猜测”它是否可信。

### 区分内部实体和外部实体信息

`value()` 有内容时，通常可以看到内部实体的替换文本；`systemId()` 或 `publicId()` 则提供外部标识信息。具体字段是否为空取决于 DTD 中采用的声明形式，因此不要把“某字段为空”直接当成解析失败。

`notationName()` 主要与未解析实体有关。普通文本实体通常没有 notation 名称。处理业务协议时，应根据实体类型和 DTD 语法共同判断，而不是只检查这个字段。

## 它不是实体构造器

Qt 6.11.1 的公开接口只有无参构造和五个读取函数，没有接受名称、值或标识符的公开构造函数，也没有 setter。无参构造只创建一个空声明：

```cpp
QXmlStreamEntityDeclaration empty;
Q_ASSERT(empty.name().isEmpty());
```

因此它适合保存 reader 返回的声明快照，不适合直接创建一条自定义 DTD 声明。若需要生成 DTD 文本，应使用 `QXmlStreamWriter::writeDTD()` 写出完整 DTD 内容，并自行承担 DTD 语法和安全约束。

## 字段语义和空值边界

### `name()`

返回实体名称，不包含实体引用两侧的 `&` 和 `;`。例如 `&company;` 对应的实体名是 `company`。

### `notationName()`

返回实体关联的 notation 名称。对于没有 notation 的实体，该视图为空。它不是实体替换文本，也不是实体引用在文档中的出现位置。

### `systemId()` 与 `publicId()`

这两个字段是 DTD 外部标识符的组成部分。它们描述标识信息，不等于已经打开的本地文件路径，也不保证资源已经被访问。不要把未经策略检查的 system identifier 直接当作可读文件名或 URL 使用。

### `value()`

返回实体替换文本。外部实体或没有内部替换文本的声明可能返回空视图。空值必须结合其他字段和 DTD 语法解释，不能单独据此断言实体不存在。

## 生命周期、复制和线程

所有读取函数返回 `QStringView`。视图不拥有字符存储，适合在当前声明对象有效期间短暂读取；要放入长期缓存、异步任务或跨线程消息，立即转换为 `QString`：

```cpp
const QString entityName = entity.name().toString();
const QString replacement = entity.value().toString();
```

这个类的函数是可重入的，值对象本身没有设备句柄或父对象关系。可重入不代表同一个对象可以被多个线程无同步地同时修改；通常做法是先复制声明或复制需要的字符串，再交给其他线程。

## 相等比较

`operator==` 比较实体声明的全部五个字段，`operator!=` 是其反向判断。比较的是声明值，不是实体在某个 DTD 文档中的位置，也不是“两个实体名称是否相同”。

如果业务只关心名称是否重复，应显式比较 `name()`；如果要判断声明是否完全一致，才使用 `==`。两个同名但值或外部标识不同的声明不会因此被视为相等。

## 与 reader 的协作边界

实体声明列表有意义的上下文是 `QXmlStreamReader` 的 DTD token。reader 的实体展开限制、实体解析器和错误状态影响后续文档读取；`QXmlStreamEntityDeclaration` 本身不负责展开实体、不负责联网、不负责打开外部资源。

读取 DTD 或外部实体时，应把资源访问策略放在 reader 配置和 `QXmlStreamEntityResolver` 中处理。不要把这个值类型误当成安全隔离层。

## API 逐项说明

### `QXmlStreamEntityDeclaration()`

创建空的实体声明。它没有参数，不能通过公开 API 直接填充名称、值或外部标识符。

### `QStringView name() const`

返回实体名称，不包含 `&` 和 `;`。返回非拥有的视图；空声明或没有对应字段时视图为空。

### `QStringView notationName() const`

返回关联的 notation 名称。普通实体通常为空；该字段不能代替实体名称，也不能用来读取替换文本。

### `QStringView publicId() const`

返回 DTD 声明中的公共标识符。它是标识信息，不是 Qt 自动解析出的文件路径；返回 `QStringView`，长期保存请复制。

### `QStringView systemId() const`

返回 DTD 声明中的系统标识符。它描述外部资源标识，不能未经检查直接当作本地路径使用。

### `QStringView value() const`

返回实体替换文本。视图不拥有数据；没有内部值时可能为空，需结合 `systemId()`、`publicId()` 和 DTD 语法判断。

### `QXmlStreamEntityDeclarations`

相关类型别名，等价于 `QList<QXmlStreamEntityDeclaration>`。它保留 reader 返回的声明顺序，列表本身拥有元素值，但元素中的 `QStringView` 仍应按非拥有视图理解。

### `operator==` 与 `operator!=`

比较两个实体声明的全部字段。相等判断不只看 `name()`，也不考虑它们在原 XML 文档中的位置。

## API 速查表

| 类别 | API | 用途 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QXmlStreamEntityDeclaration()` | 创建空实体声明 | 没有公开的带参数构造或 setter，主要作为 reader 返回的值类型使用。 |
| 读取 | `QStringView name() const` | 获取实体名称 | 不包含 `&`、`;`；返回非拥有视图。 |
| 读取 | `QStringView notationName() const` | 获取关联 notation 名称 | 普通实体可能为空；不是替换文本。 |
| 读取 | `QStringView publicId() const` | 获取公共标识符 | 不等于本地路径；外部资源使用前需要策略检查。 |
| 读取 | `QStringView systemId() const` | 获取系统标识符 | 不保证资源已访问；不要直接当作可信路径或 URL。 |
| 读取 | `QStringView value() const` | 获取实体替换文本 | 外部实体可能为空；需要长期保存时转为 `QString`。 |
| 容器别名 | `QXmlStreamEntityDeclarations` | 表示实体声明列表 | 等价于 `QList<QXmlStreamEntityDeclaration>`，保留列表顺序。 |
| 比较 | `operator==(lhs, rhs)` | 判断声明值完全相等 | 比较全部五个字段，不只比较实体名。 |
| 比较 | `operator!=(lhs, rhs)` | 判断声明值不相等 | 与 `operator==` 互补。 |

### 一句话总结

`QXmlStreamEntityDeclaration` 是 DTD 实体声明的只读值对象：它保存名称、notation、外部标识和替换文本，主要由 reader 产生；字段可能为空，外部标识也不等于已访问资源，所有 `QStringView` 都要遵守非拥有生命周期。
