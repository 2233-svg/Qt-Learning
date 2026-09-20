# QStringTokenizer：以惰性范围切分字符串

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringTokenizer>`  
> CMake：`Qt6::Core`  
> 自 Qt 6.0 起提供

`QStringTokenizer` 把一个 haystack 按 needle 切成一系列子串，并以惰性 forward range 的形式
逐个产生结果。它通常不先创建 `QStringList`，因此在只需顺序消费 token、输入很大或需要
`QStringView` 零拷贝子视图时，比 `QString::split()` 更合适。

```cpp
for (QStringView token : QStringTokenizer{line, u','})
    process(token);
```

每个 token 的计算推迟到迭代器递增或解引用时。默认保留空字段；传入
`Qt::SkipEmptyParts` 才会跳过空 token。

## 它解决什么问题

完整 `split()` 会返回容器，适合需要随机访问、跨函数保存或反复遍历的结果。很多解析流程只需
从左到右读取字段，例如日志头、命令参数、简单协议帧和 CSV 的预处理阶段；这时创建完整列表
会增加内存和复制压力。

`QStringTokenizer` 提供：

- O(1) 额外迭代状态，不把所有 token 一次性存下来。
- 只支持 forward iteration，符合它的单向生成模型。
- token 通常是 haystack 的 `QStringView`、`QLatin1StringView` 或 `QChar` 视图。
- 可以把结果显式物化为任意兼容容器。

它不是 CSV、shell 或 URL 解析器，不理解引号、转义和嵌套结构。复杂格式不能只靠分隔符切分。

## 构造与参数顺序

可以直接使用 CTAD：

```cpp
auto tokenizer = QStringTokenizer{line, QStringView{u"::"}};
```

也可以用推荐的工厂：

```cpp
auto tokenizer = qTokenize(line, u',', Qt::SkipEmptyParts,
                           Qt::CaseInsensitive);
```

构造函数支持两种尾部参数顺序：

```cpp
QStringTokenizer{haystack, needle,
                 Qt::CaseInsensitive, Qt::SkipEmptyParts};
QStringTokenizer{haystack, needle,
                 Qt::SkipEmptyParts, Qt::CaseInsensitive};
```

`Qt::CaseSensitivity` 只控制 needle 的匹配；`Qt::SplitBehavior` 控制空 token 是否保留。若
needle 在 haystack 中没有出现，会产生一个包含整个 haystack 的 token。默认
`Qt::KeepEmptyParts`，所以 `"a,,b,"` 按逗号会包含中间和末尾的空字段。

空 needle 是特殊情况。实现会在相邻位置之间推进，避免无限循环；但它通常不是业务上表达
“不切分”的好方式。若分隔符来自用户输入，建议先明确规定空分隔符的含义。

## 惰性迭代和 sentinel

`begin()` / `cbegin()` 返回只读 forward iterator，`end()` / `cend()` 返回单独的
`sentinel` 类型。结束标记不是普通 iterator，因此不能把它当作传统 STL 算法所要求的
`iterator, iterator` 同类型区间。

最自然的用法是范围 for 或 C++20 ranges：

```cpp
std::ranges::for_each(
    QStringTokenizer{line, u','},
    [](QStringView token) { process(token); });
```

tokenizer 没有可变迭代器。迭代器解引用得到的是迭代器内部当前 token 的引用；递增后，该引用
不应继续保存。若要跨递增保存 token，转成 `QString` 或把 view 复制到自己管理的容器中。

## 临时对象与借用生命周期

这是此类最值得记住的设计。

### 传入右值：tokenizer 会固定拥有型字符串

```cpp
auto tokenizer = QStringTokenizer{widget.text(), u','};
```

`widget.text()` 返回的临时 `QString` 会被移动进 tokenizer，确保 tokenizer 自己迭代时数据仍在。
类似的拥有型 `std::basic_string` 右值也会被保存。

### 传入左值：tokenizer 不复制

```cpp
QString text = widget.text();
auto tokenizer = QStringTokenizer{text, u','};
text.clear(); // 错误：tokenizer 中的 token 视图可能悬垂
```

命名对象作为 lvalue 传入时，调用方负责让它的字符存储持续到 tokenizer 使用结束。修改或重新
分配字符串也可能使已有视图失效。

### `toContainer()` 的右值限制

若 tokenizer 内部保存了 haystack，直接在 tokenizer 临时对象上调用右值 `toContainer()` 会被
限制，因为返回容器里的 view 可能指向即将销毁的内部字符串：

```cpp
auto tok = QStringTokenizer{widget.text(), u','};
auto tokens = tok.toContainer(); // 安全：tok 仍活着
```

若需要从临时表达式直接转容器，可以先显式构造并传入 `QStringView`，同时确保底层原对象仍活着；
但不要把这当成绕过生命周期规则的技巧。

## 物化为容器

`toContainer()` 把惰性序列追加到兼容容器。默认容器通常是 `QList<value_type>`：

```cpp
auto tokens = QStringTokenizer{line, u','}.toContainer();
```

也可以传入已有容器，函数会追加 token，并返回该容器的引用；传入临时容器或省略参数时，
返回填充后的容器值。容器的 `value_type` 必须能接收 tokenizer 的 `value_type`。

如果 token 是 `QStringView`，物化得到的容器仍只保存视图，不会自动深拷贝字符。需要脱离源文本
独立保存时，使用 `QList<QString>` 或逐项调用 `toString()`：

```cpp
QList<QString> owned;
for (QStringView token : QStringTokenizer{text, u','})
    owned.append(token.toString());
```

## 与 split、tokenize 的选择

- 需要完整 `QStringList`：`QString::split()`。
- 需要完整 `QList<QStringView>`：`QStringView::split()`。
- 只顺序消费：`QStringTokenizer` / `qTokenize()`。
- 已有 `QStringView`：`view.tokenize(separator)`，返回类型用 `auto` 接收。

`QStringView::tokenize()` 的返回类型依赖具体 haystack 与 needle 类型，不能手写模板参数猜测；
C++17 直接用 CTAD，旧标准使用 `auto`。

## 线程与可重入性

官方将该类的函数标为可重入。tokenizer 本身不使用全局可变状态，但它借用或保存输入数据：
不同线程各自使用独立 tokenizer 没问题；同一个 tokenizer 及其底层 lvalue 字符串不能在一个线程
修改、另一个线程同时迭代，必须由调用方同步。

它不是 `QObject`，没有事件循环、父对象或信号通知。

## 常见错误

### 把 tokenizer 当成 QStringList

它是一次性、单向、惰性范围，不提供随机访问和长度查询。需要索引或多次遍历时先物化。

### 把 sentinel 当普通 end iterator

`begin()` 的 iterator 和 `end()` 的 sentinel 类型不同；优先使用范围 for 或 C++20 ranges。

### 左值源字符串提前销毁或修改

tokenizer 不会为 lvalue 自动保存副本。让源文本活到迭代完成，或把结果转换为拥有型字符串。

### 保存迭代器解引用结果跨过递增

当前 token 的引用属于迭代器内部状态，递增后会被替换。需要长期保存就拷贝。

### `toContainer()` 后以为 token 已拥有字符

`QList<QStringView>` 仍是视图容器。源文本销毁后，里面的 view 全部失效。

### 用它解析带引号转义的格式

分隔符切分无法处理 CSV 引号、反斜杠转义或嵌套结构。应使用对应格式解析器。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `value_type` | token 的值类型 | 通常是 haystack 对应的 view 类型，不一定是传入参数的原类型。 |
| `difference_type` | 迭代距离类型 | 为 `qsizetype`；tokenizer 不提供随机访问。 |
| `size_type` | 容器大小类型别名 | 为 `std::size_t`；不等于 tokenizer 能直接报告 token 数。 |
| `reference` / `const_reference` | 只读 token 引用别名 | 不支持可变 token；引用不应跨迭代器递增长期保存。 |
| `pointer` / `const_pointer` | 只读 token 指针别名 | 指向迭代器当前值，随递增而改变。 |
| `iterator` / `const_iterator` | 只读 forward iterator | 只能向前；没有随机访问和写操作。 |
| `sentinel` | 结束标记类型 | 与 iterator 不同类型，适合范围 for/C++20 ranges。 |
| `QStringTokenizer(haystack, needle, cs, sb)` | 构造惰性切分范围 | `cs` 控制分隔符匹配，`sb` 控制空项；支持 CTAD。 |
| `QStringTokenizer(haystack, needle, sb, cs)` | 另一种参数顺序的构造 | 默认 `KeepEmptyParts` 和 `CaseSensitive`。 |
| `begin() const` | 获取第一个 token 的迭代器 | 首次调用可能立即计算第一个 token。 |
| `cbegin() const` | `begin()` 的只读别名 | 返回同样的 forward iterator。 |
| `end() const` | 获取结束 sentinel | 不是 iterator/iterator 区间的普通 end。 |
| `cend() const` | `end()` 的只读别名 | 返回空 sentinel。 |
| `toContainer(LContainer &&) const &` | 把 token 追加到容器 | 容器元素类型必须兼容；lvalue 容器返回引用，临时容器返回值。 |
| `toContainer(RContainer &&) const &&` | 在 tokenizer 右值上物化 | 仅在不会产生指向 tokenizer 内部存储的悬垂 view 时可用；有 pinning 时会被禁用。 |
| `qTokenize(haystack, needle, flags...)` | 工厂函数创建 tokenizer | Qt 6.0 起；flags 可传 `Qt::SplitBehavior` 和 `Qt::CaseSensitivity`。 |

一句话总结：`QStringTokenizer` 的核心是“边走边切、边用边算”；它把内存效率交给惰性 range，
也把源文本生命周期责任交给调用方。
