# QHelpSearchResult：一条全文搜索结果的值对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpSearchResult>`  
> 所属模块：`Qt6::Help`  
> 类型：值类型，无基类

## 它解决什么问题

`QHelpSearchResult` 描述一次 Qt Help 全文搜索命中的单个文档。它包含：

- 文档标题 `title()`。
- 文档目标 `url()`。
- 包含最佳匹配位置的摘要 `snippet()`。

搜索引擎通过 `QList<QHelpSearchResult>` 返回结果。这个类型把“用于展示的文字”和“用于导航的地址”放在一起，适合交给列表、表格或自定义结果卡片。

## 实际使用场景

- 在 `QHelpSearchEngine::searchingFinished()` 后读取一页结果。
- 自己实现搜索结果列表，而不使用 `QHelpSearchResultWidget`。
- 将标题和摘要显示给用户，点击时使用 URL 打开 qthelp 文档。
- 在测试中构造预期结果，验证自定义排序或过滤逻辑。

## 值语义与隐式共享

它不是 QObject，没有 parent、信号槽或线程归属。头文件使用 `QSharedDataPointer` 保存内部数据，因此复制对象的成本很低，适合在 `QList` 中按值传递。类型没有 setter；如果需要另一组字段，创建新的结果对象。

```cpp
const auto results = searchEngine->searchResults(0, pageSize);
for (const QHelpSearchResult &result : results) {
    qDebug() << result.title()
             << result.url()
             << result.snippet();
}
```

默认构造得到空结果。空结果的 `title()`、`url()` 和 `snippet()` 不应被当成有效文档；使用前应检查标题或 URL，并根据应用需求检查 `QUrl::isValid()`。

## 字段语义

`title()` 是文档标题，适合显示，但不一定唯一。`url()` 是文档 URL，通常是 `qthelp://` 地址，是后续读取正文或发出导航请求的关键。`snippet()` 是包含最佳匹配的文档内容片段，适合预览；它不是完整正文，也不应被当成完整 HTML 页面直接嵌入而不经过应用策略处理。

结果对象本身不保证永久有效：新的搜索会更新搜索引擎内部结果，但已经复制出来的 `QHelpSearchResult` 值仍可独立保存。若保存的是引擎返回的列表，应在新搜索开始后明确区分旧查询和新查询。

## 常见误区

- 把 `snippet()` 当成完整文档正文。
- 只显示标题而丢弃 URL，导致点击时无法导航。
- 修改搜索结果对象期待回写搜索引擎；该类型没有 setter，也没有回写关系。
- 用标题判断结果唯一性；应使用 URL 或业务定义的稳定标识。
- 把默认构造结果当作有效命中。
- 误以为该类型需要 QObject 父对象或必须在特定线程操作。

## 与相关类型的分工

- `QHelpSearchEngine` / `QHelpSearchEngineCore`：执行查询并返回结果列表。
- `QHelpSearchResultWidget`：把结果显示出来，并在链接激活时发出请求。
- `QUrl`：承载目标地址。
- `QString`：承载标题和摘要文本。

## 逐项 API 说明

### `QHelpSearchResult::QHelpSearchResult()`

构造空搜索结果。它适合先声明值对象或作为容器的默认元素，但不代表存在命中的文档。

### `QHelpSearchResult::QHelpSearchResult(const QUrl &url, const QString &title, const QString &snippet)`

构造包含 URL、标题和摘要的结果对象。构造函数不替调用者校验 URL，也不限制摘要格式。

### `QHelpSearchResult::QHelpSearchResult(const QHelpSearchResult &other)`

复制另一个结果对象。由于内部采用隐式共享，复制适合用于 Qt 容器和信号参数；修改接口不存在，因此不会出现常见的写时修改场景。

### `[noexcept] QHelpSearchResult::~QHelpSearchResult()`

销毁结果值对象并释放其共享数据引用。它不负责删除 URL、字符串之外的外部资源。

### `QHelpSearchResult &QHelpSearchResult::operator=(const QHelpSearchResult &other)`

将 `other` 的结果数据赋给当前对象并返回当前对象引用。赋值后当前对象代表同一组标题、URL 和摘要值。

### `QString QHelpSearchResult::title() const`

返回命中文档的标题。它是显示文本，不是唯一 ID。

### `QUrl QHelpSearchResult::url() const`

返回命中文档的 URL。通常用于传给帮助内容读取逻辑、结果控件或自定义导航器。

### `QString QHelpSearchResult::snippet() const`

返回包含搜索短语最佳匹配的文档片段。适合结果预览，不等价于完整文件数据。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QHelpSearchResult()` | 构造空结果。 | 不代表存在有效命中。 |
| 构造 | `QHelpSearchResult(const QUrl &url, const QString &title, const QString &snippet)` | 构造带 URL、标题和摘要的结果。 | 不自动校验 URL 或摘要格式。 |
| 构造 | `QHelpSearchResult(const QHelpSearchResult &other)` | 复制结果对象。 | 隐式共享，复制成本低。 |
| 析构 | `~QHelpSearchResult()` | 销毁结果值对象。 | 无 QObject 所有权关系。 |
| 赋值 | `QHelpSearchResult &operator=(const QHelpSearchResult &other)` | 覆盖当前结果数据。 | 返回当前对象引用。 |
| 读取 | `QString title() const` | 返回文档标题。 | 不保证唯一，不应替代文档 ID。 |
| 读取 | `QUrl url() const` | 返回文档 URL。 | 导航前检查有效性和 scheme。 |
| 读取 | `QString snippet() const` | 返回最佳匹配摘要。 | 不是完整正文。 |

---

### 一句话总结

`QHelpSearchResult` 是全文搜索的一条结果记录：按值传递标题、URL 和摘要，适合分页、缓存和自定义结果视图。
