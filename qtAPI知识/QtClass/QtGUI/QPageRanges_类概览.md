# QPageRanges：保存和解析要输出的页码范围

> 适用版本：Qt 6.0 起  
> 头文件：`#include <QPageRanges>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QPageRanges::Range`、`QPagedPaintDevice`、`QPageLayout`

## 它解决什么问题

`QPageRanges` 是一个隐式共享值类型，用来表示“要处理哪些逻辑页”。它适合承接打印对话框、导出 UI 或命令行中的范围输入，例如 `1-3,6-7`，并将结果交给 `QPrinter`、`QPdfWriter` 或自己的分页循环。

它只描述页码集合，不会自动：

- 生成页面；
- 调用 `QPagedPaintDevice::newPage()`；
- 验证文档是否真的拥有这些页；
- 将物理打印机副本、双面顺序或 booklet 排版映射成逻辑页。

也就是说，`QPageRanges` 是选择条件，不是分页执行器。

## 最小用法

```cpp
QPageRanges ranges = QPageRanges::fromString("1-3,6-7");
if (ranges.isEmpty())
    return; // 输入为空或解析失败时都可能到这里。

for (int page = 1; page <= document.pageCount(); ++page) {
    if (!ranges.contains(page))
        continue;

    renderLogicalPage(page);
}
```

页码从 **1** 开始。`addPage(0)`、`addRange(-2, 4)` 等小于 1 的页码会被忽略，并产生警告；不要把 `0` 当作“全部页面”的特殊值。

## 构造、拷贝与范围添加

默认构造得到空集合。它是隐式共享类型，拷贝和按值传递成本通常较低；首次修改某份副本时才会分离底层数据。因此可自然用于配置对象、信号参数或临时解析结果，不需要 QObject 生命周期管理。

```cpp
QPageRanges selected;
selected.addPage(1);
selected.addRange(4, 8);

if (selected.contains(6)) {
    // 渲染逻辑页 6。
}
```

`addPage()` 表示一个页号，`addRange(from, to)` 表示闭区间。若范围来自外部文本，优先使用 `fromString()`，并在业务层额外决定空范围是否允许；因为空字符串、用户未选页和解析失败都可能表现为 `isEmpty()`。

## 字符串与序列化

`fromString()` 解析 Qt 的范围文本表示，例如：

```cpp
QPageRanges ranges = QPageRanges::fromString("1-3,6-7");
QString text = ranges.toString();
```

解析错误时，`fromString()` 返回空 `QPageRanges`，不会抛异常，也没有错误对象。因此需要给用户展示“格式错误”与“确实未选页”不同提示时，应在调用前保存原始文本、自己进行格式校验，或要求空输入有明确语义。

`QDataStream <<` 将范围写成范围字符串，`>>` 再读取并解析。它适合 Qt 内部配置/IPC 场景；持久化协议若需要可诊断的错误信息或长久兼容性，建议同时保存版本和原始文本。

## 边界与常见错误

### 把 firstPage()/lastPage() 当作已选择页数

它们只给出覆盖范围两端；中间可以存在未选页面。要判断单页用 `contains()`，要遍历连续块用 `toRangeList()`。

### 空集合一定意味着“没有页可打印”

`fromString()` 出错也返回空。若用户输入可见，业务代码应区分空值和非法格式。

### 让页范围替代实际输出循环

将 `ranges` 设置到 `QPagedPaintDevice` 只是关联选择信息。是否跳过、怎样编号以及何时调用 `newPage()` 仍取决于输出后端和应用的文档模型。

### 传入 0 或负页号

Qt 页号约定从 1 开始。先在 UI 和解析层拦截非法值，不依赖运行时警告作为控制流。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 构造 | `QPageRanges()` | 创建空页范围集合。 | 空集合既可表示未选择，也可能来自解析失败。 |
| 构造 | `QPageRanges(const QPageRanges &other)` | 复制范围集合。 | 隐式共享，首次写入可能分离数据。 |
| 构造 | `QPageRanges(QPageRanges &&other)` | 移动构造范围集合。 | 移后对象仅保持有效但未指定内容。 |
| 生命周期 | `~QPageRanges()` | 销毁范围值。 | 不持有打印设备或页面对象。 |
| 修改 | `void addPage(int pageNumber)` | 添加单个逻辑页号。 | 页号从 1 开始；小于 1 会被忽略并警告。 |
| 修改 | `void addRange(int from, int to)` | 添加闭区间页范围。 | 使用正的逻辑页号；范围含义不验证是否存在于文档。 |
| 修改 | `void clear()` | 移除所有范围。 | 之后 `isEmpty()` 为真，`firstPage()`/`lastPage()` 为 0。 |
| 查询 | `bool contains(int pageNumber) const` | 判断指定逻辑页是否被选中。 | 用于分页循环的逐页筛选。 |
| 查询 | `bool isEmpty() const` | 判断范围集合是否为空。 | 解析失败也会得到空集合，必要时保留原始输入辅助诊断。 |
| 查询 | `int firstPage() const` | 返回覆盖到的最小页号。 | 空集合返回 `0`；不表示范围连续。 |
| 查询 | `int lastPage() const` | 返回覆盖到的最大页号。 | 空集合返回 `0`；不表示范围连续。 |
| 查询 | `QList<Range> toRangeList() const` | 返回范围值列表。 | 用于按连续区间迭代；列表是值拷贝。 |
| 文本 | `static QPageRanges fromString(const QString &ranges)` | 从范围文本解析集合。 | 例如 `1-3,6-7`；解析失败返回空集合。 |
| 文本 | `QString toString() const` | 返回范围的字符串表示。 | 可用于显示和持久化；不要把它当作带错误码的解析协议。 |
| 赋值 | `operator=(const QPageRanges &other)` | 复制赋值。 | 值语义；适合替换配置。 |
| 赋值 | `operator=(QPageRanges &&other)` | 移动赋值。 | 移后源对象内容不应再依赖。 |
| 流 | `QDataStream &operator<<(QDataStream &, const QPageRanges &)` | 将范围以范围字符串写入数据流。 | 读取端依赖文本解析成功。 |
| 流 | `QDataStream &operator>>(QDataStream &, QPageRanges &)` | 从数据流读出范围字符串并解析。 | 解析异常的语义仍表现为空范围；持久化时可增加版本/校验。 |

## 一句话总结

`QPageRanges` 将用户或配置给出的页码选择保存为可查询的值对象；页号从 1 开始，范围选择与实际分页输出是两件事，解析失败则需在业务层主动区分。
