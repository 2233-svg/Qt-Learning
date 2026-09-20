# Qt QXmlStreamNotationDeclaration：DTD notation 声明的值对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamNotationDeclaration>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制、可比较的 XML 值类型；函数可重入

## 它解决的问题

DTD 中的 notation 用名称描述某类外部数据或未解析实体的表示方式。例如文档可以声明某个二进制资源采用特定格式。`QXmlStreamNotationDeclaration` 保存一条 notation 的三个字段：

- `name()`：notation 名称；
- `systemId()`：系统标识符；
- `publicId()`：公共标识符。

它是 `QXmlStreamReader::notationDeclarations()` 返回的元素类型，主要服务于 DTD 检查、格式转换、文档诊断和安全审计。它不负责解释 notation，也不负责下载或打开外部资源。

## 真实使用场景

### 记录 DTD 中的外部标识

```cpp
QXmlStreamReader reader(device);

while (!reader.atEnd()) {
    reader.readNext();
    if (!reader.isDTD())
        continue;

    for (const QXmlStreamNotationDeclaration &notation
         : reader.notationDeclarations()) {
        qDebug() << notation.name()
                 << notation.publicId()
                 << notation.systemId();
    }
}
```

这适合把 DTD 元数据转成应用自己的报告。若应用不需要 DTD 或外部资源，应在解析策略中限制它们，而不是把 notation 对象当成安全过滤器。

## 三个字段的含义

### `name()`

notation 的名称，是 DTD 内部引用它时使用的符号。它不是文件名、MIME 类型或 Qt 类型名，除非文档协议明确规定了这样的映射。

### `systemId()`

系统标识符，通常用于描述外部资源的位置或标识。它不保证是本地绝对路径，也不保证资源已被访问。任何文件或网络访问都应经过应用自己的允许列表、路径规范化和权限策略。

### `publicId()`

公共标识符，是另一种外部标识方式。它也不是自动解析出的本地文件路径；空值是合法的常见情况，需结合 DTD 声明形式解释。

## 它是只读快照，不是 builder

Qt 6.11.1 的公开接口只有无参构造和三个访问函数，没有带参数构造函数和 setter。无参构造产生空 notation：

```cpp
QXmlStreamNotationDeclaration notation;
```

如果需要输出 DTD，应使用 `QXmlStreamWriter::writeDTD()` 写出完整 DTD 文本。不能依靠 notation 对象单独生成合法声明，也不能通过它向 reader 注册新的 notation。

## 生命周期和 `QStringView`

`name()`、`systemId()` 和 `publicId()` 都返回 `QStringView`。它们不拥有字符数据，适合在对象仍有效的短代码段内使用。需要跨越 reader、容器或线程生命周期时，显式复制：

```cpp
const QString name = notation.name().toString();
const QString systemId = notation.systemId().toString();
```

类函数可重入，值对象不拥有外部设备或资源。若多个线程共享 notation 列表，仍应避免一个线程修改容器而另一个线程同时遍历。

## 相等比较

`operator==` 比较 `name()`、`systemId()` 和 `publicId()` 三个字段，`operator!=` 为反向判断。它表达的是完整声明值相等，不是“notation 名称相等”。两个同名但外部标识不同的声明不应视为同一个完整声明。

## 与实体声明的关系

未解析实体可以通过 notation 名称引用一条 notation。`QXmlStreamEntityDeclaration::notationName()` 保存的是引用名，而 `QXmlStreamNotationDeclaration::name()` 保存的是 notation 自身名称。两者是协作关系，不是同一个字段的两个别名：

```cpp
if (entity.notationName() == notation.name()) {
    // entity 引用了这条 notation
}
```

实际业务还应考虑空字段和 DTD 解析错误，并决定是否允许外部标识继续参与资源解析。

## API 逐项说明

### `QXmlStreamNotationDeclaration()`

创建空 notation 声明。没有公开的带参数构造或 setter，因此主要用于接收 reader 产生的值。

### `QStringView name() const`

返回 notation 名称。它是非拥有视图；空声明时为空。

### `QStringView publicId() const`

返回公共标识符。空值并不自动表示错误；它可能只是声明采用了 system identifier 的形式。

### `QStringView systemId() const`

返回系统标识符。它是外部标识数据，不保证对应资源可访问，也不应未经检查直接转成路径或 URL 进行访问。

### `QXmlStreamNotationDeclarations`

相关类型别名，等价于 `QList<QXmlStreamNotationDeclaration>`。reader 返回的列表按文档中解析到的顺序保存声明。

### `operator==` 与 `operator!=`

比较 notation 的三个字段。相等比较不只看名称，也不比较它们在 XML 文档中的位置。

## API 速查表

| 类别 | API | 用途 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QXmlStreamNotationDeclaration()` | 创建空 notation 声明 | 没有公开的带参数构造或 setter，主要由 reader 产生。 |
| 读取 | `QStringView name() const` | 获取 notation 名称 | 不是文件名或 MIME 类型；返回非拥有视图。 |
| 读取 | `QStringView publicId() const` | 获取公共标识符 | 可能为空；不等于本地路径。 |
| 读取 | `QStringView systemId() const` | 获取系统标识符 | 不保证已访问资源；使用前需经过安全策略。 |
| 容器别名 | `QXmlStreamNotationDeclarations` | 保存 notation 列表 | 等价于 `QList<QXmlStreamNotationDeclaration>`，保留顺序。 |
| 比较 | `operator==(lhs, rhs)` | 判断完整声明值相等 | 比较名称、systemId、publicId 三个字段。 |
| 比较 | `operator!=(lhs, rhs)` | 判断完整声明值不相等 | 与 `operator==` 互补。 |

### 一句话总结

`QXmlStreamNotationDeclaration` 是 DTD notation 的只读值记录：它保存名称和外部标识，不解释格式、不访问资源，空字段需要结合 DTD 语法判断，长期保存字符串时要复制 `QStringView`。
