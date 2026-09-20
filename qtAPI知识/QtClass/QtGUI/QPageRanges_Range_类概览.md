# QPageRanges::Range：一个连续页码的闭区间

> 头文件：`#include <QPageRanges>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QPageRanges`

## 它解决什么问题

`QPageRanges::Range` 是 `QPageRanges` 内部使用和公开返回的轻量结构，表示一段连续的页码闭区间 `[from, to]`。`QPageRanges::toRangeList()` 返回它的列表，便于分页器按连续片段而不是逐页扫描处理选择结果。

它没有复杂状态、所有权或线程语义，只保存两个 `int`。因此它不负责校验页码、修正端点，也不关心文档实际有多少页；这些规则由构造它的代码和 `QPageRanges` 的高层 API 保证。

## 基本用法

```cpp
QPageRanges::Range range;
range.from = 4;
range.to = 8;

if (range.contains(6)) {
    // 6 位于闭区间 [4, 8]。
}
```

`contains(pageNumber)` 等价于 `from <= pageNumber && pageNumber <= to`，两端都包含在内。

## 数据有效性边界

成员默认值均为 `-1`，因此默认构造的 `Range` 不表示一个可打印页区间。直接手写 `Range` 时应至少满足：

- `from >= 1`；
- `to >= from`；
- 页码不超过目标文档的逻辑总页数。

`Range` 本身不会强制这些条件。若页面选择来源于用户文本，应优先用 `QPageRanges::fromString()`；若需要单页或范围添加，使用 `QPageRanges::addPage()` / `addRange()`，再通过 `toRangeList()` 读取。

## 与 QPageRanges 的关系

`Range` 是范围表示，不是容器。不要只修改 `toRangeList()` 返回列表中的 `Range` 期待原 `QPageRanges` 被修改；该列表是值拷贝。要修改选择集合，回到 `QPageRanges` 的添加/清空 API。

对于 `QPageRanges` 返回的范围，仍不能假设它们等于实际可输出页面。页范围只描述选择意图，分页器还要结合文档页数、打印设置和业务规则执行。

## 常见错误

### 认为端点是开区间

`contains()` 是闭区间判断，`from` 与 `to` 都包含。

### 直接使用默认 Range

默认 `from = -1`、`to = -1` 只表示未初始化端点。它不符合 Qt 打印页从 1 开始的约定。

### 修改 toRangeList() 的元素以更新原对象

返回列表是拷贝。要改变原选择范围，使用 `QPageRanges` 的修改 API。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 数据成员 | `int from` | 闭区间的下端点。 | 默认 `-1`；有效打印页通常应从 `1` 开始。 |
| 数据成员 | `int to` | 闭区间的上端点。 | 默认 `-1`；调用方应保证 `to >= from`。 |
| 查询 | `bool contains(int pageNumber) const noexcept` | 判断页号是否位于 `[from, to]`。 | 两端包含；不验证端点是否为有效打印页。 |
| 比较 | `operator==`, `operator!=` | 比较两个范围的端点是否相同。 | 比较的是原始数值，不做规范化。 |
| 排序 | `operator<` | 按 `from`、再按 `to` 的字典序排序。 | 适合排列范围值，不自动合并重叠或相邻区间。 |

## 一句话总结

`QPageRanges::Range` 只是连续页码的闭区间值；它足够轻量，因此有效性、页号下界和范围合并都应由使用它的 `QPageRanges` 或业务代码负责。
