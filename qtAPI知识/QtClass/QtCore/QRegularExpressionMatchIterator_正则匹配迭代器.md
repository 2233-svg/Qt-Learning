# Qt QRegularExpressionMatchIterator：全局正则匹配迭代器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRegularExpressionMatchIterator>`  
> 所属模块：`Qt6::Core`  
> 类型性质：隐式共享的前向、值语义匹配迭代器  
> 关联类型：`QRegularExpression`、`QRegularExpressionMatch`

## 1. 它解决什么问题

`QRegularExpressionMatchIterator` 用于按顺序读取一次全局正则匹配产生的多个 `QRegularExpressionMatch`。它解决的是：

- 不必先把所有匹配结果装进容器；
- 逐个处理日志、标记、字段或文本片段；
- 在找到目标后停止扫描；
- 在取出下一个结果前先查看它；
- 与 Qt 的 range-based `for` 语法配合。

它不是 STL 的随机访问迭代器，也不是一个保存所有结果的 `QList`。它只支持向前消费：

```cpp
const QRegularExpression re(R"(\b[A-Za-z_]\w*\b)");
const QString source = "first second";

QRegularExpressionMatchIterator it = re.globalMatch(source);
while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    qDebug() << match.capturedView();
}
```

`next()` 会推进位置；`peekNext()` 只查看，不推进。调用这两个函数前都应先检查 `hasNext()`。

## 2. 构建与链接

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QRegularExpression>
#include <QRegularExpressionMatchIterator>
```

类声明位于 `qregularexpression.h`；`<QRegularExpressionMatchIterator>` 是 Qt 提供的类级包含入口。

## 3. 迭代器的创建方式

### 3.1 使用 `globalMatch()`

```cpp
const QRegularExpression re(R"((?<key>[A-Za-z_]\w*)\s*=\s*(?<value>\S+))");
const QString source = "a=1 b=2";

for (QRegularExpressionMatchIterator it = re.globalMatch(source);
     it.hasNext();) {
    const QRegularExpressionMatch match = it.next();
    qDebug() << match.captured("key")
             << match.captured("value");
}
```

`globalMatch()` 面向 `QString`。它适合需要拥有型字符串、或结果要在源字符串之外继续使用的普通代码。

### 3.2 使用 `globalMatchView()`

```cpp
QString source = readLargeText();
QRegularExpressionMatchIterator it =
    re.globalMatchView(QStringView(source));

while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    consumeImmediately(match.capturedView());
}
```

`globalMatchView()` 借用源文本的字符数据，迭代器、返回的匹配结果以及它们产生的 `QStringView` 使用期间，`source` 必须保持有效，且不能进行会使字符存储失效的修改。

### 3.3 range-based `for`

Qt 6 支持直接遍历 `globalMatch()` 或 `globalMatchView()` 的结果：

```cpp
const QRegularExpression re(R"(\w+)");
const QString source = "the quick fox";

for (const QRegularExpressionMatch &match : re.globalMatch(source)) {
    consume(match.capturedView());
}
```

这里的循环变量是每次匹配的结果引用。若要把文本保存到循环外，应复制为 `QString`；若只是当前循环体内消费，可以使用 `capturedView()`。

## 4. 迭代状态模型

### 4.1 初始位置在第一个结果之前

由 `globalMatch()` 返回的新迭代器并不指向第一个结果，而是位于“第一个结果之前”。因此正确顺序是：

```cpp
while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    // 使用 match
}
```

不要创建后直接调用 `next()`，除非你已经能保证存在下一个结果。

### 4.2 `hasNext()` 与 `isValid()` 是两个维度

- `isValid()`：迭代器是否由有效的全局匹配创建；
- `hasNext()`：当前位置之后是否还有结果。

因此可能出现：

| 状态 | `isValid()` | `hasNext()` |
| --- | ---: | ---: |
| 默认构造的空迭代器 | `true` | `false` |
| 有效正则但没有匹配 | `true` | `false` |
| 有效正则且还有结果 | `true` | `true` |
| 无效正则产生的迭代器 | `false` | 不应当当作正常序列使用 |

检查 `isValid()` 不能代替 `hasNext()`。

### 4.3 到达末尾后不能调用 `next()` 或 `peekNext()`

在结果集末尾调用 `next()` 或 `peekNext()` 会产生未定义结果。即使某些构建中看起来返回了空的 `QRegularExpressionMatch`，也不能依赖这种行为：

```cpp
if (it.hasNext()) {
    const QRegularExpressionMatch next = it.peekNext();
    process(next);
}
```

## 5. `next()` 和 `peekNext()` 的区别

### 5.1 `next()`：取出并推进

```cpp
while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    process(match);
}
```

每次调用返回当前位置之后的下一个结果，并把迭代器推进一个匹配位置。它适合正常消费流式结果。

### 5.2 `peekNext()`：查看但不推进

```cpp
while (it.hasNext()) {
    const QRegularExpressionMatch candidate = it.peekNext();

    if (candidate.captured("key") == "stop")
        break;

    process(it.next());
}
```

`peekNext()` 适合根据下一个结果决定是否消费。反复调用它会得到同一个下一结果；必须随后调用 `next()` 才会推进。

### 5.3 不要把 `peekNext()` 当缓存

`peekNext()` 返回的是一个值类型结果。保存了这个结果不会冻结迭代器，也不会阻止后续 `next()` 推进。若要长期保存捕获文本，复制为 `QString`，不要只保存借用的 `QStringView`。

## 6. 匹配结果、空匹配和部分匹配

### 6.1 每次 `next()` 返回 `QRegularExpressionMatch`

匹配结果包含：

- `hasMatch()` / `hasPartialMatch()`；
- 数字和命名捕获；
- 捕获位置；
- 关联正则；
- 匹配类型和匹配选项。

迭代器本身不提供 `captured()`；需要先取出 `QRegularExpressionMatch`。

### 6.2 空匹配不是“没有结果”

模式如 `.*?`、`^`、`$` 或某些可选结构可能产生长度为 0 的匹配。空匹配仍然是一个结果，调用 `next()` 后迭代器必须继续向前。业务代码不要通过“捕获长度为 0”自行判断迭代结束，应只用 `hasNext()`。

如果业务不接受空匹配，应在处理结果时显式过滤：

```cpp
while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    if (!match.hasMatch() || match.capturedLength(0) == 0)
        continue;
    consume(match.capturedView());
}
```

### 6.3 全局部分匹配

如果 `globalMatch()` 使用部分匹配类型，迭代器可能产生部分匹配结果。调用方必须检查 `hasMatch()` 和 `hasPartialMatch()`，不能只因为 `hasNext()` 为 `true` 就把结果当作完整字段。

## 7. 源文本生命周期与视图边界

### 7.1 `globalMatch()` 的 `QString`

普通 `globalMatch(const QString &)` 适合拥有型主题字符串。即使返回的 `QRegularExpressionMatch` 被保存，也应把 `captured()` 作为长期保存的明确选择。

### 7.2 `globalMatchView()` 的 `QStringView`

`globalMatchView()` 不拥有源文本：

```cpp
QRegularExpressionMatchIterator makeIterator()
{
    return re.globalMatchView(QStringView(loadText()));
    // 错误：loadText() 产生的临时字符串已销毁
}
```

正确方式是让源字符串覆盖整个迭代过程：

```cpp
QString source = loadText();
QRegularExpressionMatchIterator it =
    re.globalMatchView(QStringView(source));

while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    const QStringView token = match.capturedView();
    consumeImmediately(token);
}
```

如果不能严格管理源文本生命周期，使用 `globalMatch()`，或在处理时立即把捕获结果转换为 `QString`。

## 8. 拷贝、移动和交换

### 8.1 拷贝是值语义

迭代器支持复制构造和复制赋值，并且是隐式共享类型。复制不会重新运行正则，也不会把已经处理过的匹配重新计算一遍。

实际代码中应避免让多个副本共同表达一个业务游标。一个函数或一个循环持有一个可推进的迭代器，通常最清晰。

### 8.2 移动后的源对象不可查询

移动构造或移动赋值后，源迭代器只能析构或重新赋值。不要对 moved-from 迭代器调用 `hasNext()`、`isValid()` 或 `next()`。

```cpp
QRegularExpressionMatchIterator first = re.globalMatch(text);
QRegularExpressionMatchIterator second = std::move(first);

// second 可以使用；first 只能析构或重新赋值
```

### 8.3 `swap()` 不改变匹配逻辑

`swap()` 只交换两个迭代器对象的内部状态，不重新匹配，也不改变正则模式本身。

## 9. 元数据 API

迭代器可以查询创建它时使用的匹配参数：

```cpp
qDebug() << it.regularExpression().pattern();
qDebug() << it.matchType();
qDebug() << it.matchOptions();
```

- `regularExpression()` 返回产生该迭代器的正则对象值；
- `matchType()` 返回 `globalMatch()` 调用时使用的匹配类型；
- `matchOptions()` 返回调用时使用的匹配选项。

这些 API 适合调试通用扫描器，不能用来判断当前是否还有结果；结果数量仍由 `hasNext()` 决定。

## 10. 典型使用场景

### 10.1 提取所有字段

```cpp
const QRegularExpression re(R"((?<name>\w+)\s*=\s*(?<value>\S+))");
QRegularExpressionMatchIterator it = re.globalMatch(line);

while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    fields.insert(match.captured("name"),
                  match.captured("value"));
}
```

### 10.2 找到目标后停止

```cpp
QRegularExpressionMatchIterator it = re.globalMatch(text);
while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    if (match.capturedView() == u"target") {
        handleTarget(match);
        break;
    }
}
```

全局匹配是按顺序推进的；不需要全部结果时，找到目标后可以直接结束循环。

### 10.3 大文本短期扫描

```cpp
const QString source = readLargeText();
QRegularExpressionMatchIterator it =
    re.globalMatchView(QStringView(source));

while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    inspect(match.capturedView());
}
```

这里不把每个捕获字段复制出来，适合同步、短生命周期的扫描路径。若 `inspect()` 会异步保存参数，应改用 `captured()`。

## 11. 常见错误

### 11.1 不检查 `hasNext()` 就调用 `next()`

到达末尾后调用 `next()` 是未定义行为。把 `next()` 放在 `while (hasNext())` 或等价保护中。

### 11.2 用 `isValid()` 判断还有结果

有效迭代器可能已经为空，也可能一开始就没有匹配。是否还有下一个结果只看 `hasNext()`。

### 11.3 误以为它可以回退

它是前向、单向消费模型，没有 `previous()` 或随机访问。需要回看时保存 `QRegularExpressionMatch` 或把必要字段复制到容器。

### 11.4 把它当作 STL 迭代器做 `++` 和解引用

公共 API 没有让调用方直接使用 `operator++`、`operator*` 的 STL 风格接口。Qt 支持 range-based `for`，但普通手动遍历应使用 `hasNext()` / `next()`。

### 11.5 `globalMatchView()` 返回后源字符串已经销毁

这会让迭代器或结果中的视图指向失效字符数据。临时 `QString`、局部返回值和异步任务是高风险场景。

### 11.6 用捕获长度判断迭代结束

空匹配的长度可以是 0，但它仍是合法结果。迭代结束只由 `hasNext()` 决定。

### 11.7 复制多个迭代器并假设它们共享一个业务游标

迭代器是值类型。不要依赖多个副本之间的推进关系；需要共享扫描状态时，应由一个明确的拥有者负责推进。

## 12. 逐项 API 语义

### `QRegularExpressionMatchIterator()`

构造有效的空迭代器。它关联默认构造的正则、`NoMatch` 匹配类型和 `NoMatchOption` 选项，但不遍历任何结果，因此 `hasNext()` 返回 `false`。

### `QRegularExpressionMatchIterator(const QRegularExpressionMatchIterator &iterator)`

复制迭代器的值状态。它不会重新执行全局匹配。

### `QRegularExpressionMatchIterator(QRegularExpressionMatchIterator &&iterator)`

移动构造迭代器。Qt 6.1 起提供。移动后的源对象只能析构或赋值，不能继续查询或推进。

### `~QRegularExpressionMatchIterator()`

销毁迭代器并释放共享状态。使用 `globalMatchView()` 时，析构后不能再从该对象取得结果或视图。

### `operator=(const QRegularExpressionMatchIterator &iterator)`

复制赋值，把另一个迭代器的状态赋给当前对象。当前对象原有的遍历状态被覆盖。

### `operator=(QRegularExpressionMatchIterator &&iterator)`

移动赋值并接管另一个迭代器的内部状态。Qt 6.1 起提供；源对象移动后只能析构或重新赋值。

### `swap(QRegularExpressionMatchIterator &other)`

交换两个迭代器的内部状态。操作快速且不会重新执行正则。

### `isValid() const`

判断迭代器是否来自有效的 `QRegularExpression` 全局匹配。它不表示存在结果；默认空迭代器也没有可供 `next()` 读取的结果。

### `hasNext() const`

判断当前迭代位置之后是否至少还有一个匹配结果。调用 `next()` 或 `peekNext()` 前应先调用它。

### `next()`

返回下一个 `QRegularExpressionMatch`，并推进迭代器。到达末尾时调用是未定义行为。

### `peekNext() const`

返回下一个 `QRegularExpressionMatch`，但不推进迭代器。到达末尾时调用是未定义行为。

### `regularExpression() const`

返回创建该迭代器的 `QRegularExpression` 值对象。它适合诊断当前扫描器使用的模式。

### `matchType() const`

返回创建迭代器时传给 `globalMatch()` 或 `globalMatchView()` 的匹配类型。它描述配置，不代表每个结果都是完整或部分匹配。

### `matchOptions() const`

返回创建迭代器时使用的匹配选项。它不改变当前游标位置。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QRegularExpressionMatchIterator()` | 创建有效的空迭代器。 | `hasNext()` 为 `false`；有效不等于有结果。 |
| 构造 | `QRegularExpressionMatchIterator(const QRegularExpressionMatchIterator &)` | 复制迭代器状态。 | 不重新匹配；不要把多个副本当成一个共享游标。 |
| 构造 | `QRegularExpressionMatchIterator(QRegularExpressionMatchIterator &&)` | 移动构造迭代器。 | Qt 6.1 起；源对象移动后只能析构或赋值。 |
| 生命周期 | `~QRegularExpressionMatchIterator()` | 销毁迭代器。 | 视图匹配的源字符串仍应由外层正确管理。 |
| 赋值 | `operator=(const QRegularExpressionMatchIterator &)` | 复制赋值。 | 覆盖当前游标状态。 |
| 赋值 | `operator=(QRegularExpressionMatchIterator &&)` | 移动赋值。 | 源对象之后不可查询。 |
| 交换 | `swap()` | 交换两个游标状态。 | 不重新执行正则。 |
| 状态 | `isValid()` | 判断是否来自有效正则的全局匹配。 | 不代表还有结果。 |
| 状态 | `hasNext()` | 判断后方是否还有匹配。 | `next()` / `peekNext()` 的前置检查。 |
| 消费 | `next()` | 取出下一个结果并推进。 | 末尾调用是未定义行为。 |
| 预览 | `peekNext()` | 查看下一个结果但不推进。 | 反复调用会得到同一个结果；末尾调用是未定义行为。 |
| 元数据 | `regularExpression()` | 返回关联正则对象。 | 返回值对象，适合诊断模式。 |
| 元数据 | `matchType()` | 返回创建时使用的匹配类型。 | 不等于每个结果的实际状态。 |
| 元数据 | `matchOptions()` | 返回创建时使用的匹配选项。 | 不表示当前还有多少结果。 |

## 14. 一句话总结

`QRegularExpressionMatchIterator` 是全局匹配结果的单向消费器：创建后先用 `hasNext()`，再用 `next()` 取出并推进；需要预判时用 `peekNext()`；使用 `globalMatchView()` 时，源文本必须覆盖整个迭代和所有捕获视图的使用期。
