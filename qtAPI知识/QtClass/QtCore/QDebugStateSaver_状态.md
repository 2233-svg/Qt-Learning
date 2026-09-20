# Qt QDebugStateSaver 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QDebugStateSaver>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QDebug`、`QTextStream`

## 1. 它解决什么问题：自定义输出不能污染调用方的日志格式

`QDebugStateSaver` 是一个很小的 RAII 保护器。它在构造时保存一个 `QDebug` 的格式状态，在离开作用域时自动恢复。

它最典型的用途是实现自定义类型的 `operator<<`。为了把一个对象打印成 `Point(3, 5)`、十六进制 ID 或固定精度浮点数，运算符往往需要改用 `nospace()`、`noquote()`、`Qt::hex`、`Qt::fixed` 等格式。如果没有恢复，调用方在这个对象之后继续 `<<` 的内容就会继承被改动的格式。

```text
没有 QDebugStateSaver：
  qDebug() << "before" << point << "after"
  自定义 point 使用 nospace()
  结果可能变成："before"Point(3,5)"after"

有 QDebugStateSaver：
  point 的局部格式在返回前自动恢复
  结果保持："before" Point(3, 5) "after"
```

它不保存业务对象状态，不会撤销已经写入日志流的文字，也不会过滤、缓存或提交日志消息。它只保护格式状态。

## 2. 最小正确用法

```cpp
#include <QDebug>
#include <QDebugStateSaver>

namespace geometry {

struct Point {
    int x;
    int y;
};

QDebug operator<<(QDebug debug, const Point &point)
{
    QDebugStateSaver saver(debug);
    debug.nospace() << "Point(" << point.x << ", " << point.y << ')';
    return debug;
}

} // namespace geometry
```

使用时：

```cpp
geometry::Point point{3, 5};
qDebug() << "cursor:" << point << "visible:" << true;
```

运算符接收并返回 `QDebug` 值，这是 Qt 的标准模式。`QDebug` 自身内部共享流状态，因此按值传递不会重新创建一条消息；`QDebugStateSaver` 保护的正是这个共享流上的格式。

## 3. 它到底保存和恢复什么

`QDebugStateSaver` 保存当前 `QDebug` 的设置，包括自动插入空格等 QDebug 格式选项；它也会保存内部 `QTextStream` 的格式状态。因此以下写法是安全的：

```cpp
QDebug operator<<(QDebug debug, const quint32 value)
{
    QDebugStateSaver saver(debug);
    debug.nospace() << "0x" << Qt::hex << value;
    return debug;
}
```

在此之后，调用者的 `QDebug` 不会意外永久保持十六进制或 `nospace()` 模式。

| 被保护的内容 | 是否会恢复 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 自动空格与字符串引号 | 会 | 恢复 `space()`、`nospace()`、`quote()`、`noquote()` 相关状态 | 自定义输出中仍应只改自己确实需要的状态 |
| verbosity | 会 | 恢复当前 debug 流希望输出的细节等级 | 不要在子对象输出中擅自永久改变调用方诊断级别 |
| `QTextStream` 格式 | 会 | 恢复进制、字段宽度、精度、对齐等内部文本流格式 | 使用 `Qt::hex`、`Qt::fixed` 后尤其需要它 |
| 已写出的字符 | 不会 | 已输出内容仍属于当前日志消息 | 它不是事务或回滚工具 |
| 日志消息提交 | 不会控制 | 消息仍由 `QDebug` 的生命周期决定何时刷新 | 临时 `qDebug()` 通常在完整表达式结束时提交 |

还有一个容易忽略的行为：析构恢复格式后，`QDebugStateSaver` 会根据**创建 saver 时**的自动空格设置调用 `maybeSpace()`。这使一个自定义对象输出结束后，正常的后续 `<<` 项仍能以空格分隔。

因此不要在 `return debug;` 前手工补“为了调用方准备”的空格。让 saver 恢复并处理分隔即可；手工补空格可能造成重复空格或在 `nospace` 调用方中产生意外输出。

## 4. 使用场景：什么时候必须用，什么时候不必

### 4.1 应在自定义 `operator<<` 中默认使用

只要运算符调用了以下任何一种接口，基本都应放一个栈上的 saver：

```cpp
debug.nospace();
debug.noquote();
debug.setAutoInsertSpaces(false);
debug.setQuoteStrings(false);
debug.setVerbosity(...);
debug << Qt::hex << value;
debug << Qt::fixed << value;
```

原因不只是今天的实现。即使当前输出函数暂时只改了一项格式，未来维护者加上 `Qt::hex` 或 `noquote()` 时，已有 saver 能把这种修改限制在局部作用域。

### 4.2 不需要用它的简单情况

```cpp
QDebug operator<<(QDebug debug, const Version &version)
{
    return debug << version.major << version.minor << version.patch;
}
```

这段代码没有改变格式状态，saver 并非必需。不过项目通常会倾向于始终在公开自定义输出运算符里使用它：开销很小，且可以避免后续改动引入状态泄漏。

### 4.3 不要把它延长到 QDebug 之后

```cpp
QDebugStateSaver *badSaver(QDebug &debug)
{
    return new QDebugStateSaver(debug); // 不要这样做
}
```

它应是和目标 `QDebug` 同一局部作用域中的栈对象。动态分配会让恢复时机不清楚，还可能在 debug 流已经销毁后才析构 saver。类被显式禁止复制，也不应尝试把它作为普通可转移的值对象保存。

## 5. 常见误区

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 以为 saver 会撤销已写日志内容 | 它只保存格式，不保存输出缓冲区快照 | 在写入前决定输出内容，不能依赖析构回滚 | 敏感字段一旦写入就无法由 saver 抹除 |
| 在 `operator<<` 中改 `nospace()` 后不恢复 | 后续调用方输出继承紧凑格式 | 在函数开头构造 `QDebugStateSaver` | 这是自定义类型日志格式错乱的首要原因 |
| 设置 `Qt::hex` 后忘记改回十进制 | 后续整数都可能以十六进制显示 | 用 saver 管理 `QTextStream` 格式 | 不要手工“改回去”并赌所有分支都执行 |
| 将 saver 放在比 debug 更长的作用域 | 析构时会访问已经失效的流 | 让 saver 在 debug 参数的当前栈帧内析构 | 两者必须有清楚的销毁顺序 |
| 手工在 return 前追加分隔空格 | saver 已按原自动空格策略处理分隔 | 直接返回 debug | 调用方若本来是 `nospace()`，不应强加空格 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDebugStateSaver(QDebug &debug)` | 保存传入 debug 流当前的 QDebug 和 QTextStream 格式状态 | 立即在当前作用域构造；参数必须在 saver 析构前继续有效 |
| 析构 | `~QDebugStateSaver()` | 恢复构造时保存的格式，并按原自动空格状态调用 `maybeSpace()` | 自动执行，不要依赖手工提前析构；它不撤销已输出文本 |

## 7. 一个带十六进制字段的完整例子

```cpp
namespace protocol {

struct Header {
    quint16 opcode;
    quint32 payloadSize;
};

QDebug operator<<(QDebug debug, const Header &header)
{
    QDebugStateSaver saver(debug);
    debug.nospace()
        << "Header(opcode=0x" << Qt::hex << header.opcode
        << Qt::dec << ", payloadSize=" << header.payloadSize
        << ')';
    return debug;
}

} // namespace protocol
```

`Qt::dec` 在示例中让本函数内的 `payloadSize` 以十进制输出；即便遗漏它，saver 仍会保证调用方流的进制状态被恢复。保留 `Qt::dec` 的价值是让这一条消息本身符合读者预期，saver 的价值则是确保这一条消息不会影响下一条。
