# Qt QXmlStreamNamespaceDeclaration：保存一条 XML 命名空间声明

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamNamespaceDeclaration>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制、可比较的 XML 值类型；函数可重入

## 它解决的问题

XML 命名空间声明把前缀绑定到 URI：

```xml
<svg:svg xmlns:svg="http://www.w3.org/2000/svg">
```

这里的 `svg` 是前缀，`http://www.w3.org/2000/svg` 是命名空间 URI。`QXmlStreamNamespaceDeclaration` 用两个字段保存这条绑定：

- `prefix()`：声明的前缀；
- `namespaceUri()`：前缀绑定到的 URI。

它主要由 `QXmlStreamReader::namespaceDeclarations()` 返回，也可作为 `QXmlStreamReader::addExtraNamespaceDeclaration()` 的参数，为增量解析补充命名空间信息。它不是全局注册表，声明只在对应 XML 作用域中有意义。

## 真实使用场景

### 检查当前元素声明了哪些前缀

```cpp
QXmlStreamReader reader(device);

while (!reader.atEnd()) {
    reader.readNext();
    if (!reader.isStartElement())
        continue;

    for (const QXmlStreamNamespaceDeclaration &declaration
         : reader.namespaceDeclarations()) {
        qDebug() << declaration.prefix()
                 << "->" << declaration.namespaceUri();
    }
}
```

### 为片段解析补充外部上下文

当应用分块解析 XML 片段，而片段本身没有携带父元素的命名空间声明时，可以在 reader 上添加额外声明：

```cpp
QXmlStreamReader reader(fragment);
reader.addExtraNamespaceDeclaration(
    QXmlStreamNamespaceDeclaration(
        u"svg"_qs,
        u"http://www.w3.org/2000/svg"_qs));
```

这类声明是解析上下文的一部分。它不等于向输出文档写入 `xmlns`，也不会自动改变 writer 的命名空间状态。

## 前缀和 URI 的边界

前缀是词法别名，不是命名空间的稳定身份。`p` 可以在不同元素作用域中绑定不同 URI；同一个 URI 也可以使用不同前缀。因此：

- 协议判断应比较 URI；
- 只有在保留输入文本或诊断信息时才重点比较前缀；
- 不要在全局表中把 prefix 当作永恒唯一键。

默认命名空间声明的前缀为空：

```xml
<root xmlns="urn:example"/>
```

对应的 `prefix()` 为空，`namespaceUri()` 为 `urn:example`。空前缀并不等于“没有命名空间”。

另一方面，空的 URI 表示解除默认命名空间或一个空声明值的情况，具体是否是合法 XML 语法要结合所在位置和 reader 的错误状态判断。不要仅凭一个字段为空就推断声明对象没有意义。

## 生命周期、复制和线程

两个读取函数都返回 `QStringView`，不拥有字符数据。将声明存入日志、缓存或跨线程任务时，复制成 `QString`：

```cpp
const QString prefix = declaration.prefix().toString();
const QString uri = declaration.namespaceUri().toString();
```

值对象本身不拥有 reader，也没有设备句柄。文档标注函数可重入，但共享声明列表或共享解析上下文仍需按普通容器和线程同步规则处理。

## 相等比较

`operator==` 比较前缀和命名空间 URI 两个字段；`operator!=` 表示不相等。两个声明即使 URI 相同，只要前缀不同，也不一定相等，因为它们表达的词法绑定不同。反过来，业务若只关心命名空间身份，应显式比较 `namespaceUri()`，不要直接把 `==` 当作 URI 等价判断。

## 无参构造与公开能力

无参构造创建空声明。带参数构造按调用方提供的 `prefix` 和 `namespaceUri` 保存一条值记录。类没有 setter，因此构造后不能原地修改字段；需要变更时创建新的声明值。

`QXmlStreamNamespaceDeclarations` 是 `QList<QXmlStreamNamespaceDeclaration>` 的别名，适合保存同一作用域中返回的声明序列。

## API 逐项说明

### `QXmlStreamNamespaceDeclaration()`

创建空的命名空间声明。它不自动表示默认命名空间，也不表示无命名空间元素。

### `QXmlStreamNamespaceDeclaration(const QString &prefix, const QString &namespaceUri)`

按给定前缀和 URI 创建声明。传空前缀可表达默认命名空间绑定；参数不会替调用方建立全局注册，也不会自动写入 XML。

### `QStringView prefix() const`

返回声明的前缀。默认命名空间的前缀为空；返回值是非拥有视图，长期保存请复制。

### `QStringView namespaceUri() const`

返回前缀对应的命名空间 URI。空前缀不代表 URI 为空；需要区分默认命名空间时必须同时读取两个字段。

### `QXmlStreamNamespaceDeclarations`

相关类型别名，等价于 `QList<QXmlStreamNamespaceDeclaration>`。它常用于 reader 返回的当前声明列表，遵守 `QList` 的顺序、复制和迭代语义。

### `operator==` 与 `operator!=`

比较声明的前缀和 URI。相等是完整值相等，不是仅按 URI 判断命名空间身份。

## API 速查表

| 类别 | API | 用途 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QXmlStreamNamespaceDeclaration()` | 创建空声明 | 不等于默认命名空间，也不等于无命名空间。 |
| 构造 | `QXmlStreamNamespaceDeclaration(const QString &prefix, const QString &namespaceUri)` | 创建前缀到 URI 的绑定值 | 空前缀可表示默认命名空间；不会自动注册或写出。 |
| 读取 | `QStringView prefix() const` | 获取词法前缀 | 默认命名空间前缀为空；返回非拥有视图。 |
| 读取 | `QStringView namespaceUri() const` | 获取命名空间身份 | URI 才是稳定语义身份；长期保存需复制。 |
| 容器别名 | `QXmlStreamNamespaceDeclarations` | 保存声明序列 | 等价于 `QList<QXmlStreamNamespaceDeclaration>`，保留列表顺序。 |
| 比较 | `operator==(lhs, rhs)` | 判断前缀和 URI 都相等 | 不只是 URI 相等。 |
| 比较 | `operator!=(lhs, rhs)` | 判断声明不完全相等 | 与 `operator==` 互补。 |

### 一句话总结

`QXmlStreamNamespaceDeclaration` 只是“前缀 -> URI”的值记录：空前缀可以是默认命名空间，前缀不是稳定身份，URI 才适合协议判断；声明对象本身不会自动注册或写出命名空间。
