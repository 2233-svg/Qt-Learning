# QPageRanges

> Qt 6.11.1 · Qt GUI · 来自 `QPageRanges`

## 1. 先建立直觉

`QPageRanges` 是“用户想打印哪些页”的值对象。它不关心文档内容、页数统计、打印机能力，也不把页码转换成数组；它只负责保存若干个 **从 1 开始的页码区间**，并能在字符串、区间列表和二进制流之间转换。

最常见的输入来自打印对话框或命令行：用户输入 `1-3,6-7`，程序用 `QPageRanges::fromString()` 转成对象，再交给 `QPrinter`、`QPagedPaintDevice` 或自己的分页导出逻辑。它的价值在于把“离散页”和“连续范围”统一起来，避免到处手写解析和合并逻辑。

## 2. 类说明

- 头文件：`#include <QPageRanges>`
- CMake：`Qt6::Gui`
- 类型性质：轻量值类型，可复制、可移动、可清空
- 页码规则：页码从 `1` 开始；`0` 和负数不是有效页码
- 空范围语义：`isEmpty()` 为 `true`，`firstPage()` / `lastPage()` 返回 `0`

`QPageRanges` 不验证“文档是否真的有这些页”。例如文档只有 5 页，范围里仍然可以保存 `1-10`。真正执行打印或导出时，调用方需要用文档页数再做一次裁剪。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPageRanges()` | 创建空页码范围，适合先构造再逐步添加页码。 |
| `addPage(int pageNumber)` | 添加单页，会与已有相邻区间合并；页码必须大于等于 `1`。 |
| `addRange(int from, int to)` | 添加闭区间 `[from, to]`；常用于用户输入、打印选择和批量导出。 |
| `clear()` | 清空全部页码选择。 |
| `contains(int pageNumber)` | 判断某一页是否被选中，适合分页循环时过滤。 |
| `firstPage()` | 返回所有范围中的第一页；空对象返回 `0`。 |
| `lastPage()` | 返回所有范围中的最后一页；空对象返回 `0`。 |
| `isEmpty()` | 判断是否没有任何页码范围。 |
| `toRangeList()` | 返回 `Range { from, to }` 列表，便于自己循环处理连续段。 |
| `toString()` | 转成紧凑字符串，例如 `1-3,6-7`，适合保存配置或显示摘要。 |
| `fromString(const QString &ranges)` | 从字符串解析页码范围；解析失败返回空对象。 |
| `operator<<` / `operator>>` | 通过 `QDataStream` 序列化，内部以范围字符串表达。 |

## 4. 关键用法

### 从用户输入转成打印范围

```cpp
const QPageRanges ranges = QPageRanges::fromString("1-3,6-7");

if (!ranges.isEmpty())
    printer.setPageRanges(ranges);
```

`fromString()` 适合处理标准范围字符串，但不要把“空对象”简单等同于“用户没选”。输入为空、输入非法、或者用户确实选择了空范围，最终都可能得到空对象。界面层最好保留原始输入，用于提示“格式错误”。

### 在分页循环中使用

```cpp
for (int page = 1; page <= pageCount; ++page) {
    if (!ranges.isEmpty() && !ranges.contains(page))
        continue;

    renderPage(page);
}
```

这里故意把空范围解释为“全部页”，这是很多打印界面的习惯；但 `QPageRanges` 本身不定义这个业务语义，是否“空代表全部”要由你的调用逻辑决定。

### 分段处理比逐页展开更高效

```cpp
for (const QPageRanges::Range &range : ranges.toRangeList()) {
    for (int page = range.from; page <= range.to; ++page)
        exportPage(page);
}
```

当范围很大时，不要先生成一个包含所有页码的列表。`QPageRanges` 保存的是区间，直接按区间循环更贴近它的设计。

## 5. 使用场景

- 打印对话框：保存用户选择的页码、范围和多段选择。
- PDF 导出：只导出特定页，例如导出第 `1` 页和附录页。
- 报表系统：把“预览页码”和“实际输出页码”分离。
- 命令行工具：解析 `--pages 1-3,8,10-12` 这类参数。
- 批处理任务：对大文档按页段拆分，而不是一次性展开成所有页。

## 6. 常见坑与经验

- **页码是 1 基。** 这是打印领域习惯，不是 C++ 容器索引。把页面数组下标传进去会整体偏移一页。
- **小于 1 的页码会被忽略并产生警告。** 如果输入来自用户，最好在界面层提前校验，不要依赖 Qt 的运行期警告。
- **空范围没有统一业务含义。** 对 `QPageRanges` 来说空就是空；“空代表全部页”是打印界面或导出逻辑的约定。
- **它不校验文档页数。** `contains(999)` 只回答范围中是否包含 999，不回答文档有没有第 999 页。
- **解析失败会返回空对象。** 因此当你需要区分“输入为空”和“输入非法”时，应自行做格式提示。
- **序列化格式适合 Qt 内部持久化。** 如果要写入公开配置文件，`toString()` 更直观，也更便于用户编辑。

## 7. 知识点覆盖

- 1 基页码与 0 基索引的转换边界
- 离散页和连续页段的统一表达
- 字符串解析、配置持久化和 `QDataStream` 序列化
- 与 `QPrinter`、`QPagedPaintDevice`、PDF 导出流程的配合
- 空范围、非法输入、超出文档页数三种情况的区别
- 分段循环与逐页展开之间的性能和语义差异
