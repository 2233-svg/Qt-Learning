# QTextFragment 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextBlock>`（相关声明位于 Qt 文本对象头文件）  
> 所属模块：`Qt6::Gui`  
> 继承：无（轻量值类型）

## 1. 它解决什么问题

`QTextFragment` 表示一个块内连续、共享同一字符格式的文本运行（text run）。它是 `QTextDocument` 内部格式化文本的观察视图，适合在不逐字符读取的情况下遍历一段文本及其格式。

实际场景：

- 代码编辑器按格式运行统计关键字、注释和普通文本；
- 导出器遍历块中的格式片段；
- 调试富文本格式合并是否生效；
- 从文档中取得某个运行的 `QGlyphRun` 做底层绘制或测量。

它不是可编辑对象。需要修改内容或格式时使用 `QTextCursor`；需要生成一段可插入内容时使用 `QTextDocumentFragment`。

## 2. 从块迭代器取得

```cpp
for (QTextBlock block = document->begin();
     block.isValid();
     block = block.next()) {
    for (QTextBlock::iterator it = block.begin();
         !it.atEnd();
         ++it) {
        QTextFragment fragment = it.fragment();
        if (!fragment.isValid())
            continue;

        qDebug() << fragment.position()
                 << fragment.length()
                 << fragment.text()
                 << fragment.charFormat().font();
    }
}
```

空块通常没有有效 fragment。一个字符格式发生变化，或遇到图像等对象边界，块就可能被拆成多个 fragment；不要把一个块误认为一个 fragment。

## 3. 位置、长度和格式

`position()` 是 fragment 在文档中的起始位置，`length()` 是其内部文本范围长度，`contains(position)` 判断一个文档位置是否落在该范围内。位置是文档坐标，不是块内下标；需要块内偏移时用 `position - block.position()`。

`text()` 返回该运行的字符串。它可能包含段落分隔或对象替代字符，不能保证只包含用户可见的普通字母。

`charFormat()` 返回运行的字符格式，`charFormatIndex()` 返回文档格式表中的索引。格式索引是文档内部实现编号，不是稳定的业务 ID，不应写入持久化协议。

## 4. 有效性和生命周期

默认构造的 fragment 无效。fragment 由块迭代器产生，关联来源文档的内部数据，但不拥有文档。文档被修改后，尤其是删除或重排相应文本时，旧 fragment 不应继续作为长期缓存使用；重新遍历文档取得新的 fragment 更稳妥。

它是轻量可复制值，不提供公开构造函数让应用指定任意位置。这样可以避免应用构造出不符合文档格式运行边界的对象。

## 5. 字形运行

`glyphRuns()` 把文本运行转换为字形级数据，返回 `QGlyphRun` 列表，适合自定义绘制、命中测试或字形调试。它依赖 Qt 的 raw font / glyph 支持配置；默认参数表示请求整个 fragment。字形位置和字符串索引涉及排版结果，不能用简单的字符下标替代。

如果只需要文本和字符格式，不要为了普通遍历调用 `glyphRuns()`，因为字形提取的成本和数据量都更高。

## API 速查表
| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextFragment()` | 创建无效 fragment。 | `isValid()` 为 `false`。 |
| `QTextFragment(const QTextFragment &other)` | 复制 fragment 观察值。 | 不复制文档；文档生命周期仍必须覆盖使用期。 |
| `operator=(const QTextFragment &other)` | 赋值 fragment。 | 只替换观察状态，不修改文档。 |
| `isValid()` | 判断 fragment 是否对应有效文档运行。 | 空块、默认对象或已失效状态不能读取有效文本。 |
| `operator==` | 比较两个 fragment 是否表示同一内部运行。 | 不等同于文本内容相同。 |
| `operator!=` | 判断两个 fragment 是否不同。 | 内部运行不同，即使文本相同也可能不等。 |
| `operator<` | 按起始文档位置排序。 | 适合同一文档中的 fragment；不同文档的位置没有业务可比性。 |
| `position()` | 返回 fragment 的文档起点。 | 不是块内偏移，也不是像素坐标。 |
| `length()` | 返回 fragment 的文档位置长度。 | 结构对象和段落边界可能影响长度理解。 |
| `contains(int position)` | 判断文档位置是否在 fragment 范围内。 | 位置应使用同一文档的坐标体系。 |
| `charFormat()` | 返回该运行的字符格式。 | 返回值是格式副本；修改它不会回写文档。 |
| `charFormatIndex()` | 返回内部格式表索引。 | 仅适合调试或与文档内部查询配合，不是稳定持久化 ID。 |
| `text()` | 返回 fragment 文本。 | 不包含可编辑接口；可能含对象替代字符或段落边界。 |
| `glyphRuns(int from = -1, int length = -1)` | 获取范围对应的字形运行。 | 依赖 raw font 配置；默认请求整个 fragment，适合底层绘制和测量。 |

## 7. 记忆重点

`QTextFragment` 是“同格式文本运行的只读视图”。用它做高效遍历和排版观察，用 `QTextCursor` 做修改；fragment 的位置和格式索引属于文档内部坐标，文档发生结构性变化后应重新获取。
