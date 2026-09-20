# QStaticByteArrayMatcher：为固定字节模式预计算匹配器

> Qt 6.11.1 | `#include <QStaticByteArrayMatcher>` | 模块：`Qt6::Core` | 模板：`QStaticByteArrayMatcher<N>`

`QStaticByteArrayMatcher` 用于在字节数组中反复查找一个**编译期已知**的字节模式。和每次调用 `QByteArray::indexOf()` 相比，它把模式的预处理放到编译期完成，避免运行时重复准备匹配状态。

它适合协议解析、日志切分、固定分隔符扫描、二进制文件标记搜索等场景。若模式由用户输入或配置文件决定，应改用可在运行时 `setPattern()` 的 `QByteArrayMatcher`，而不是硬凑一个静态匹配器。

## 推荐写法

```cpp
#include <QStaticByteArrayMatcher>

static const auto headerMatcher = qMakeStaticByteArrayMatcher("HTTP/");

qsizetype findProtocol(QByteArrayView input)
{
    return headerMatcher.indexIn(input);
}
```

工厂函数从字符串字面量推导模板参数 `N`，比手写 `QStaticByteArrayMatcher<N>` 更可靠。返回对象通常声明为 `static const auto`；模式和预计算表只需构造一次。

## 它与 QByteArray::indexOf() 的区别

`QByteArray::indexOf()` 适合偶发、临时或动态模式搜索。`QStaticByteArrayMatcher` 的优势来自模式固定：内部跳转表可在编译期生成，因此在大输入中重复查找同一个多字节模式时更合适，某些一次性查找也可能受益。

它不是普适的“总是更快”替代品。短输入、单字符搜索、动态模式、或者代码可读性更重要时，普通 `indexOf()` 往往已经足够。

## 字节语义与边界

- 模式是 `char` 字节序列，不做 Unicode 解码、大小写折叠或文本规范化。
- 工厂函数接收 C 字符串字面量；末尾自动添加的终止 `'\0'` 不属于模式内容。
- `indexIn()` 返回首个匹配位置，找不到时返回 `-1`。
- `from` 是开始搜索的字节偏移。外部输入应先验证其范围，尤其不要把负数或不可信长度直接传入。
- `const char *` 重载依赖调用方同时提供正确的 `hlen`。该内存可包含 `'\0'`，但指针必须可读至少 `hlen` 个字节。

Qt 6.11.1 的头文件还提供 `QByteArrayView` 重载；它很适合不想构造 `QByteArray` 的缓冲区切片。

## 生命周期与线程

匹配器按值保存模式与预计算状态，不借用传给构造函数的字面量。`indexIn()` 不修改匹配器或输入，因此静态常量匹配器可被多个线程并发读取；前提仍是每个调用方提供的输入缓冲区在调用期间有效，且没有其他线程同时写它。

## 常见错误

1. **把运行时模式用于静态匹配器。** 配置驱动的模式使用 `QByteArrayMatcher`。
2. **把文本编码问题当成字节匹配问题。** UTF-8、Latin-1 和二进制协议的相同“字符”可能不是相同字节。
3. **遗漏未命中分支。** `-1` 不是位置 0，后续切片或指针运算前必须判断。
4. **错误传递裸指针长度。** `hlen` 比实际可读区域大时会越界读取。
5. **为单字符场景增加复杂度。** 简单查找通常直接用字节数组 API 更清楚。

## API 速查表

| 类别 | API | 语义 | 使用边界 |
| --- | --- | --- | --- |
| 工厂 | `qMakeStaticByteArrayMatcher(const char (&pattern)[N])` | 从字面量推导 `N` 并返回静态匹配器。 | 模式在编译期固定；末尾终止符不参与匹配。 |
| 构造 | `QStaticByteArrayMatcher(const char (&pattern)[N])` | 直接以字面量创建匹配器。 | 通常优先工厂函数，避免手写模板长度。 |
| 搜索 | `indexIn(const QByteArray &haystack, qsizetype from = 0)` | 在 `QByteArray` 内找首个模式。 | 找不到返回 `-1`；偏移按字节计。 |
| 搜索 | `indexIn(QByteArrayView haystack, qsizetype from = 0)` | 在非拥有字节视图内搜索。 | Qt 6.11.1 头文件提供；输入只需在调用期间存活。 |
| 搜索 | `indexIn(const char *haystack, qsizetype hlen, qsizetype from = 0)` | 在显式指针和长度描述的缓冲区内搜索。 | 调用方负责指针有效性与 `hlen` 准确性。 |
| 查询 | `pattern()` | 返回当前固定模式的 `QByteArray` 副本。 | 没有 `setPattern()`；需要换模式就创建另一匹配器。 |

`QStaticByteArrayMatcher` 的关键不是“替代所有搜索”，而是在固定字节标记成为解析热路径时，把模式预处理从运行时挪走。
