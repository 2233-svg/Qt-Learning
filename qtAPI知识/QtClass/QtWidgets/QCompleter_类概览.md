# QCompleter 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCompleter>`  
> 模块：`Qt6::Widgets`  
> 继承：`QObject -> QCompleter`

`QCompleter` 是 Qt Widgets 的输入补全协调器。它不拥有输入框，也不负责保存业务数据；它把“用户当前输入”“候选模型”“候选展示视图”和“用户选中的结果”接在一起。

最常见的搭配是 `QLineEdit` 与 `QComboBox`。例如用户输入部门名、命令、标签、文件路径时，补全器从模型找出匹配项，再用下拉列表或行内文本让用户少打几个字。

## 1. 它解决什么问题

补全不是简单的 `QStringList::filter()`。实际输入控件里还要处理：

- 输入框什么时候开始匹配，候选框显示在哪；
- 键盘上下键、回车、Esc 应该由输入框还是候选框处理；
- 当前前缀应如何映射到模型的一列和一个角色；
- 用户选中树模型的某个节点后，应当回填节点文本还是完整路径；
- 大型、已排序模型怎样避免每次输入都线性扫描。

`QCompleter` 把这套交互收敛为一个稳定流程：

```text
编辑控件中的文本
       |
       v
completionPrefix
       |
       v
model + completionColumn + completionRole
       |
       v
completionModel（当前匹配结果，只读）
       |
       v
popup / inline completion
       |
       v
activated / highlighted
```

它适合“已有候选集合，用户通过一小段前缀定位”的问题。它不擅长模糊搜索、拼音首字母、权重排序、网络请求流式建议或语义推荐；这些需求应先在外部筛选/排序得到模型，再让 `QCompleter` 负责最终的控件交互。

## 2. 最小可用例子

### 2.1 给 `QLineEdit` 安装列表补全

```cpp
#include <QApplication>
#include <QCompleter>
#include <QLineEdit>
#include <QStringListModel>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QStringList commands {
        "build",
        "clean",
        "configure",
        "deploy",
        "test"
    };

    QLineEdit edit;
    auto *completer = new QCompleter(commands, &edit);
    completer->setCaseSensitivity(Qt::CaseInsensitive);
    completer->setCompletionMode(QCompleter::PopupCompletion);

    edit.setCompleter(completer);
    edit.resize(360, 32);
    edit.show();
    return app.exec();
}
```

`QLineEdit::setCompleter()` 会把补全器绑定到这个输入框，因此这里不需要再手动 `setWidget(&edit)`。补全器以 `edit` 为父对象，输入框销毁时补全器也会销毁。

### 2.2 不要把补全器结果再手工筛一遍

```cpp
connect(completer,
        qOverload<const QModelIndex &>(&QCompleter::activated),
        this,
        [this](const QModelIndex &index) {
            openCommand(index.data(Qt::UserRole).toString());
        });
```

模型行中常常同时有“给人看的标题”和“给程序用的 ID”。`activated(const QModelIndex &)` 能保留完整索引和所有角色数据；只有确实只需要文本时，再连接 `activated(const QString &)`。

## 3. 四个对象，四种职责

| 对象 | 职责 | 最容易混淆的点 |
| --- | --- | --- |
| `widget()` | 补全器当前服务的输入控件 | 补全器不创建这个控件，也不拥有它 |
| `model()` | 原始候选数据源 | 不是“当前匹配结果”；通常由外部模型所有者管理 |
| `completionModel()` | 根据当前前缀导出的只读匹配模型 | 不要把它当作原始模型去修改 |
| `popup()` | 候选的弹出项视图 | 只有 popup 模式才是主要展示出口 |

`setWidget()` 会在目标控件上安装事件过滤器，以便把按键、焦点和输入变化协调到补全流程。一个补全器在某一时刻服务一个 widget；切换 widget 时，旧绑定会被解除。

`setModel()` 不会让 `QCompleter` 取得你传入模型的所有权。因此，当模型是独立业务模型时，应让窗口、控制器或模型层拥有它；若模型直接 `new` 出来且只服务此补全器，可以把补全器设为它的 QObject 父对象。

## 4. 匹配到底匹配什么

补全器不是默认读取“第一列的所有显示文本”这么简单，它有四个决定匹配目标的参数：

```cpp
completer->setCompletionColumn(0);       // 哪一列
completer->setCompletionRole(Qt::DisplayRole); // 哪个角色
completer->setCaseSensitivity(Qt::CaseInsensitive);
completer->setFilterMode(Qt::MatchStartsWith);
```

### 4.1 列与角色

假设模型有三列：显示名、命令 ID、描述。用户看到的候选要按显示名匹配，就使用 `DisplayRole` 的第 0 列；如果希望用户输入内部命令 ID，则把补全列改为对应列，或把 ID 放进某个自定义 role 后设置 `completionRole`。

不要把“显示文本”和“业务标识”强行混在同一个字符串中。匹配用什么、弹出层显示什么、激活后执行什么，可以分别通过模型列、角色和 `activated(QModelIndex)` 来表达。

### 4.2 `completionPrefix` 是当前查询，不一定等于控件全文

`setCompletionPrefix()` 直接设置补全器当前查询前缀。它常用于自定义编辑控件，例如只补全光标前最后一个单词：

```cpp
const QString prefix = wordBeforeCursor();
completer->setCompletionPrefix(prefix);
completer->complete(cursorRectangle());
```

对于树模型，前缀可能是一段路径而不只是一个词。此时 `splitPath()` 将路径拆成模型层级片段，`pathFromIndex()` 再把激活的模型索引变成最终应回填的路径。

### 4.3 `filterMode` 的边界

`Qt::MatchStartsWith` 是最符合“补全”直觉的模式：输入 `con` 时优先找 `configure`。`MatchContains` 和 `MatchEndsWith` 可以满足更宽松的查找，但候选会更多，并且很难利用排序优化。

传给 `setFilterMode()` 的是 `Qt::MatchFlags`，但不应把任意 `Qt::MatchFlag` 组合都当作有意义的补全规则。需要复杂模糊匹配时，使用代理模型或业务层先生成更合适的候选模型。

## 5. 大模型性能：排序声明必须诚实

`QCompleter` 可以利用“模型已经按补全列排序”这一事实加速前缀查找。配置方式是：

```cpp
completer->setFilterMode(Qt::MatchStartsWith);
completer->setCaseSensitivity(Qt::CaseInsensitive);
completer->setModelSorting(QCompleter::CaseInsensitivelySortedModel);
```

只有以下前提都满足时，这个声明才有价值：

1. 模型确实按 `completionColumn()` 和 `completionRole()` 所读的值排序；
2. 排序规则与 `caseSensitivity()` 一致；
3. 使用前缀匹配，即 `Qt::MatchStartsWith`。

此时补全器可以用二分查找缩小候选范围。若模型实际未排序、大小写规则不一致，结果可能漏项或顺序异常。拿不准时用 `UnsortedModel`，先保证正确。

`completionCount()` 看起来无害，但要得到完整候选数，补全器可能需要访问全部结果。输入每改一个字符就调用它，容易把本可延迟的工作变成热点；弹出列表本身通常不需要你先计算总数。

## 6. 三种展示模式

| `CompletionMode` | 行为 | 适合什么 |
| --- | --- | --- |
| `PopupCompletion` | 显示经过过滤的候选弹出列表 | 大多数普通文本、命令、标签输入 |
| `UnfilteredPopupCompletion` | 弹出完整候选列表，当前输入主要用于定位当前项 | 希望用户浏览有限选项集的输入 |
| `InlineCompletion` | 把候选剩余部分直接放入编辑控件中 | 候选短、歧义低、用户希望快速确认的命令输入 |

`complete(rect)` 用于明确要求补全器显示或更新补全。`rect` 是绑定 widget 的局部矩形，通常传光标矩形，使弹出列表贴近插入点；默认空矩形时由补全器自行决定位置。

`setPopup()` 允许替换候选视图，比如自定义 `QTreeView` 来显示多列信息。传入后，补全器接管这个视图的所有权；因此不要同时给它设置一个会独立删除它的 QObject 父对象。

## 7. 树模型和文件路径：为什么要重写两个函数

普通列表模型中，一个候选通常就是一个字符串。文件系统、分类树、命令分组模型不同：用户输入 `src/widgets/qco`，补全器需要知道斜杠代表层级，而不是一整个候选字符串。

`QCompleter` 默认实现适合常见路径场景；自定义分隔符或自定义树模型时，重写这两个函数：

```cpp
class DotPathCompleter final : public QCompleter
{
public:
    using QCompleter::QCompleter;

    QStringList splitPath(const QString &path) const override
    {
        return path.split('.', Qt::SkipEmptyParts);
    }

    QString pathFromIndex(const QModelIndex &index) const override
    {
        QStringList parts;
        for (QModelIndex current = index; current.isValid(); current = current.parent())
            parts.prepend(current.data(completionRole()).toString());
        return parts.join('.');
    }
};
```

`splitPath()` 与 `pathFromIndex()` 要使用同一套语法。前者按 `.` 拆层，后者也应使用 `.` 拼回；两者若不对称，激活候选后会得到无法再次匹配的文本。

## 8. 信号：高亮不是确认

| 信号 | 何时发出 | 常见用途 |
| --- | --- | --- |
| `highlighted(const QString &)` | 当前候选高亮变化时 | 状态栏预览、临时说明 |
| `highlighted(const QModelIndex &)` | 当前候选高亮变化时 | 需要读取图标、ID 或其他角色时 |
| `activated(const QString &)` | 用户确认选择候选时 | 只需最终显示文本 |
| `activated(const QModelIndex &)` | 用户确认选择候选时 | 执行业务动作、读取完整模型数据 |

高亮会随着键盘上下移动和鼠标悬停反复发出，不能直接触发不可逆业务操作。真正执行命令、打开文件、提交选择，应放在 `activated`。

## 9. 常见问题

| 现象 | 原因 | 处理方式 |
| --- | --- | --- |
| 绑定了补全器却没出现候选 | 输入框没有触发或当前前缀为空、模型没有匹配值 | 检查 `widget()`、`model()`、`completionPrefix()`；必要时调用 `complete()` |
| 候选显示了但回填文本不对 | 模型列、role 或树路径回填策略不一致 | 检查 `completionColumn()`、`completionRole()` 和 `pathFromIndex()` |
| 大数据量下输入卡顿 | 每次输入线性匹配、频繁读取 `completionCount()` | 正确声明已排序模型，或先在代理模型中缩小候选 |
| 候选漏掉了本应匹配的条目 | `Case...SortedModel` 声明与真实排序不一致 | 改回 `UnsortedModel` 或修正排序 |
| 自定义 popup 显示后崩溃 | 同一视图被补全器和其他对象重复管理 | 让补全器独占 popup 的生命周期 |
| 自定义编辑器的 popup 位置不对 | `complete()` 的矩形不是 widget 局部坐标 | 传入编辑器光标的局部 `QRect` |
| 树路径补全越用越奇怪 | `splitPath()` 和 `pathFromIndex()` 使用不同分隔规则 | 把拆分和拼接写成对称逻辑 |

## API 速查表
下表按 Qt 6.11.1 的 `qcompleter.h` 直接声明整理。表中的“模型”特指传给 `setModel()` 的原始模型，“补全模型”特指 `completionModel()` 返回的只读结果模型。

### 10.1 构造、目标控件与数据模型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCompleter(QObject *parent = nullptr)` | 创建尚未指定候选源的补全器 | 后续必须设置模型或使用字符串列表构造 |
| 构造 | `QCompleter(QAbstractItemModel *model, QObject *parent = nullptr)` | 创建并绑定已有模型 | 补全器不拥有传入模型 |
| 构造 | `QCompleter(const QStringList &completions, QObject *parent = nullptr)` | 用字符串列表创建补全器 | 适合小型静态候选；动态数据应使用模型 |
| 生命周期 | `~QCompleter()` | 销毁补全器和其内部资源 | QObject 父对象可负责销毁它 |
| 目标控件 | `setWidget(QWidget *widget)` | 绑定补全器服务的 widget | 会安装事件过滤器；一个补全器一次服务一个 widget |
| 目标控件 | `widget() const` | 返回当前绑定 widget | 未绑定时返回空指针 |
| 原始模型 | `setModel(QAbstractItemModel *model)` | 设置候选数据模型 | 不接管模型所有权；切换模型会让当前补全结果失效 |
| 原始模型 | `model() const` | 返回候选数据模型 | 不等于 `completionModel()` |
| 补全模型 | `completionModel() const` | 返回当前匹配结果的只读模型 | 不要修改或把它当作长期业务模型保存 |

### 10.2 匹配规则与展示配置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 展示模式 | `setCompletionMode(CompletionMode mode)` | 设置 popup、未过滤 popup 或行内补全 | 改模式会改变键盘交互预期 |
| 展示模式 | `completionMode() const` | 读取当前展示模式 | |
| 过滤 | `setFilterMode(Qt::MatchFlags filterMode)` | 设置候选匹配规则 | 排序加速只适合 `MatchStartsWith` |
| 过滤 | `filterMode() const` | 读取匹配规则 | |
| 弹出视图 | `popup() const` | 返回候选 popup 视图 | 主要用于调整列宽、委托或选择行为 |
| 弹出视图 | `setPopup(QAbstractItemView *popup)` | 替换候选 popup 视图 | 补全器接管 view 所有权 |
| 大小写 | `setCaseSensitivity(Qt::CaseSensitivity caseSensitivity)` | 设置匹配是否区分大小写 | 必须与已排序模型的声明一致 |
| 大小写 | `caseSensitivity() const` | 读取大小写匹配规则 | |
| 排序 | `setModelSorting(ModelSorting sorting)` | 声明模型是否按补全数据排序 | 声明错误会伤害正确性，不只是性能 |
| 排序 | `modelSorting() const` | 读取排序声明 | |
| 字段 | `setCompletionColumn(int column)` | 设置读取补全文本的模型列 | 需要是模型中有效列 |
| 字段 | `completionColumn() const` | 读取补全列 | |
| 字段 | `setCompletionRole(int role)` | 设置读取补全文本的 item data role | 默认通常使用显示角色；自定义模型可使用自定义 role |
| 字段 | `completionRole() const` | 读取补全 role | |
| 弹层 | `maxVisibleItems() const` | 读取 popup 最大可见候选数 | 不会限制模型中的真实匹配数 |
| 弹层 | `setMaxVisibleItems(int maxItems)` | 设置 popup 最大可见候选数 | 控制视觉高度，过大列表仍应保持可扫描 |
| 导航 | `wrapAround() const` | 是否允许候选导航从尾循环到头 | 影响键盘上下键体验 |
| 导航 | `setWrapAround(bool wrap)` | 设置候选导航循环 | 这是公共槽，也可用于信号槽连接 |

### 10.3 当前补全状态与公共槽

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 统计 | `completionCount() const` | 返回当前前缀匹配到的候选数量 | 可能触发完整结果访问，别在高频输入路径滥用 |
| 当前项 | `setCurrentRow(int row)` | 把当前候选设为指定结果行 | 行号基于当前补全模型；无效行返回 `false` |
| 当前项 | `currentRow() const` | 返回当前候选行 | 没有当前项时结果不应当作有效索引 |
| 当前项 | `currentIndex() const` | 返回当前候选的模型索引 | 用它读取同一行的其他列和 role |
| 当前项 | `currentCompletion() const` | 返回当前候选回填文本 | 树模型时结果受 `pathFromIndex()` 影响 |
| 查询 | `completionPrefix() const` | 返回当前匹配前缀 | 不一定等于整个输入控件文本 |
| 查询槽 | `setCompletionPrefix(const QString &prefix)` | 设置当前匹配前缀并更新结果 | 自定义编辑器通常在文本变化时调用 |
| 显示槽 | `complete(const QRect &rect = QRect())` | 显示或更新补全 | `rect` 是绑定 widget 的局部坐标；默认矩形让补全器决定位置 |

### 10.4 树路径与可重写入口

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 路径 | `pathFromIndex(const QModelIndex &index) const` | 将候选索引转为要回填或显示的路径 | 树模型、自定义分隔符场景重写它 |
| 路径 | `splitPath(const QString &path) const` | 将用户路径拆成模型层级片段 | 必须与 `pathFromIndex()` 的拼接规则对称 |
| 事件 | `eventFilter(QObject *object, QEvent *event)` | 处理绑定 widget 的事件流 | 框架连接点；普通代码不要手动调用 |
| 事件 | `event(QEvent *event)` | 处理补全器自身事件 | 通常只有扩展补全器行为时才重写 |

### 10.5 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 确认 | `activated(const QString &text)` | 用户确认候选后发出回填文本 | 只需文本时连接它 |
| 确认 | `activated(const QModelIndex &index)` | 用户确认候选后发出模型索引 | 业务逻辑通常优先连接它，信息更完整 |
| 预览 | `highlighted(const QString &text)` | 当前高亮候选变化时发出文本 | 会高频触发，不做不可逆操作 |
| 预览 | `highlighted(const QModelIndex &index)` | 当前高亮候选变化时发出索引 | 用于显示说明、图标或预览数据 |

### 10.6 枚举速查

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 展示枚举 | `PopupCompletion` | 过滤后以 popup 显示候选 | 最常用模式 |
| 展示枚举 | `UnfilteredPopupCompletion` | 不先过滤，直接弹出候选集合 | 候选较少且用户需要浏览时使用 |
| 展示枚举 | `InlineCompletion` | 在编辑控件内显示补全剩余文本 | 歧义大的候选会让体验变差 |
| 排序枚举 | `UnsortedModel` | 声明模型未排序 | 默认且最稳妥 |
| 排序枚举 | `CaseSensitivelySortedModel` | 声明按区分大小写顺序排序 | 需配合 `Qt::CaseSensitive` 与前缀匹配 |
| 排序枚举 | `CaseInsensitivelySortedModel` | 声明按忽略大小写顺序排序 | 需配合 `Qt::CaseInsensitive` 与前缀匹配 |

## 11. 什么时候不该用 QCompleter

当候选来自远端接口时，不要让每个按键直接把网络结果塞入补全器。应在业务层做去抖、取消过期请求和错误处理，结果返回后再更新模型。

当你需要“任意字符散落匹配、拼音、权重、最近使用优先、同义词”等规则时，也不要把规则硬塞进 `filterMode`。用 `QSortFilterProxyModel` 或专门搜索模型产生排序后的候选，再把 `QCompleter` 作为输入和选择层。这样补全器仍然简单，搜索逻辑也有独立的测试位置。
