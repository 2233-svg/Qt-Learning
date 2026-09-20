# QHelpSearchQueryWidget：生成标准化的帮助搜索表达式

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpSearchQueryWidget>`  
> 所属模块：`Qt6::Help`  
> 继承：`QWidget`  
> 定位：搜索输入控件

## 它解决什么问题

`QHelpSearchQueryWidget` 为 Qt Help 提供搜索输入界面。它可以只显示一个普通搜索框，也可以展开扩展搜索字段，让用户通过控件生成搜索引擎能够理解的标准化查询字符串。

它只负责收集和规范化输入，不负责建立索引，也不执行全文搜索。真正的搜索由 `QHelpSearchEngine::search(const QString &)` 完成。

## 实际使用场景

- 直接作为 `QHelpSearchEngine::queryWidget()` 返回的搜索框使用。
- 在自定义搜索页面中放置输入控件，并把 `searchInput()` 传给 `QHelpSearchEngine`。
- 普通模式只需要一个输入框，扩展模式需要让用户表达更复杂的查询条件。
- 在窄侧栏或工具栏中启用紧凑模式，减少额外控件占用的空间。

## 基本用法

使用 `QHelpSearchEngine` 时，优先取得引擎管理的查询控件：

```cpp
auto *queryWidget = searchEngine->queryWidget();
layout->addWidget(queryWidget);

connect(queryWidget, &QHelpSearchQueryWidget::search,
        this, [this, queryWidget] {
            searchEngine->search(queryWidget->searchInput());
        });
```

也可以直接创建一个 `QHelpSearchQueryWidget`，但它不会自动连接任何搜索引擎：

```cpp
auto *query = new QHelpSearchQueryWidget(this);
query->setSearchInput(QStringLiteral("QHelpEngine AND setup"));

connect(query, &QHelpSearchQueryWidget::search, this, [this, query] {
    searchEngine->search(query->searchInput());
});
```

## 输入与执行是两个步骤

`setSearchInput()` 只把字符串写入控件，`searchInput()` 只读取控件当前生成的查询表达式。两者都不会触发搜索。用户点击搜索按钮或按下相应操作键时，控件才发出无参数的 `search()` 信号；接收方需要读取 `searchInput()`，再显式调用搜索引擎。

这一区分很重要：如果程序在 `setSearchInput()` 后需要立即搜索，必须自己调用 `QHelpSearchEngine::search()`，不能等待控件自动完成。

## 普通模式、扩展模式与紧凑模式

- `expandExtendedSearch()`：显示扩展搜索字段。
- `collapseExtendedSearch()`：收起扩展字段，只保留默认搜索字段。
- `isCompactMode()`：读取当前是否处于紧凑展示模式。
- `setCompactMode(bool)`：切换紧凑展示模式。

扩展模式和紧凑模式是界面状态，不等于搜索引擎的索引状态。改变它们不会自动重建索引，也不应被当成一次搜索提交。具体子控件的布局和平台风格由 Qt 实现管理，应用应把控件放入布局，而不是依赖固定坐标。

## 生命周期、线程和事件循环

这是 QWidget，必须在 GUI 线程创建和访问。构造函数的 `parent` 只管理 QWidget 生命周期；它不代表控件已经连接到某个帮助引擎。

用户点击搜索按钮、键盘回车等交互依赖事件循环。若在没有运行 GUI 事件循环的测试中调用 `setSearchInput()`，可以验证文本状态，但不会自然产生用户触发的 `search()` 信号。

## 常见误区

- 调用 `setSearchInput()` 后期待自动搜索。
- 直接把用户原始文本当作最终查询，而不读取 `searchInput()` 生成的标准表达式。
- 将 `search()` 信号当作带查询参数的信号；它没有参数。
- 通过固定坐标摆放扩展字段，导致字体、翻译或紧凑模式变化后布局错位。
- 把 `setCompactMode()` 当成“限制搜索结果”的设置；它只影响控件显示方式。
- 连接到搜索引擎旧的 `QList<QHelpSearchQuery>` 重载时没有显式选择目标槽。

## 逐项 API 说明

### `[explicit] QHelpSearchQueryWidget::QHelpSearchQueryWidget(QWidget *parent = nullptr)`

创建搜索查询控件，并按 QWidget 规则设置父对象。它不会接收搜索引擎指针，也不会自动开始索引或搜索。

### `[override virtual noexcept] QHelpSearchQueryWidget::~QHelpSearchQueryWidget()`

销毁查询控件及其内部界面子控件。若控件有 parent，通常由父对象负责销毁；不要在父对象销毁后继续保存并使用指针。

### `void QHelpSearchQueryWidget::expandExtendedSearch()`

展开扩展搜索界面，使额外搜索字段可见。它只改变展示状态，不会自动调用搜索引擎。

### `void QHelpSearchQueryWidget::collapseExtendedSearch()`

收起扩展搜索界面，只保留默认搜索字段。收起不会自动清空搜索条件，具体已生成表达式应通过 `searchInput()` 验证。

### `QString QHelpSearchQueryWidget::searchInput() const`

返回可传给 `QHelpSearchEngine::search(const QString &)` 的搜索表达式。它是控件对当前输入状态的标准化输出，适合在 `search()` 信号处理函数中读取。

### `void QHelpSearchQueryWidget::setSearchInput(const QString &searchInput)`

把指定字符串填入控件。它只更新输入字段，不执行实际搜索；需要搜索时显式调用引擎的 `search()`。

### `bool QHelpSearchQueryWidget::isCompactMode() const`

返回当前是否启用紧凑展示模式。该状态用于读取界面配置，不表示索引或搜索是否正在进行。

### `[slot] void QHelpSearchQueryWidget::setCompactMode(bool on)`

启用或关闭紧凑展示模式。应让布局系统重新计算尺寸，不要假设切换后控件的固定宽高保持不变。

### `[signal] void QHelpSearchQueryWidget::search()`

用户触发搜索按钮时发出。信号没有查询参数；接收后调用 `searchInput()` 取得表达式，再传给搜索引擎。

## 过时接口

旧版的 `query()` 和 `setQuery(const QList<QHelpSearchQuery> &)` 已废弃。新代码使用 `searchInput()` 和 `setSearchInput(const QString &)`；旧的结构化查询类型也应迁移为字符串查询表达式。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QHelpSearchQueryWidget(QWidget *parent = nullptr)` | 创建搜索输入控件。 | 不自动连接搜索引擎；必须在 GUI 线程创建。 |
| 析构 | `~QHelpSearchQueryWidget()` | 销毁控件。 | 遵守 QWidget 父子所有权。 |
| 展示 | `void expandExtendedSearch()` | 显示扩展搜索字段。 | 只改变界面，不执行搜索。 |
| 展示 | `void collapseExtendedSearch()` | 收起扩展字段。 | 不等于清空查询；用 `searchInput()`确认实际表达式。 |
| 输入 | `QString searchInput() const` | 返回标准化搜索表达式。 | 适合传给 `QHelpSearchEngine::search()`。 |
| 输入 | `void setSearchInput(const QString &searchInput)` | 填写搜索输入。 | 不会执行实际搜索。 |
| 展示状态 | `bool isCompactMode() const` | 读取紧凑模式状态。 | 只反映布局状态。 |
| 展示状态槽 | `void setCompactMode(bool on)` | 切换紧凑展示模式。 | 切换后让布局重新计算尺寸。 |
| 信号 | `void search()` | 用户触发搜索时通知应用。 | 无参数；槽中读取 `searchInput()`。 |
| 已废弃 | `query()`、`setQuery(const QList<QHelpSearchQuery> &)` | 旧版结构化查询接口。 | 用 `searchInput()` 和 `setSearchInput()` 替代。 |

---

### 一句话总结

`QHelpSearchQueryWidget` 是 Qt Help 的查询表达式编辑器：它负责输入和规范化，搜索引擎负责真正执行，二者通过 `search()` 信号和 `searchInput()` 返回值连接。
