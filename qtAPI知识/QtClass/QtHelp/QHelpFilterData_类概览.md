# QHelpFilterData：定义组件和版本过滤条件

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpFilterData>`
> 所属模块：`Qt6::Help`
> 类型：值类型

## 它解决什么问题

`QHelpFilterData` 保存一个帮助 filter 的约束：允许哪些 component，以及允许哪些 version。`QHelpFilterEngine` 使用这些条件从所有已注册 qch 中筛出目录、索引和搜索结果。

它把“过滤器名称”和“过滤器内容”分开：名称由 `QHelpFilterEngine` 管理，组件/版本条件由这个值类型描述。这样同一组条件可以被读取、修改、比较和传递给 `setFilterData()`。

## 实际使用场景

- 创建“只显示 Qt Widgets 文档”或“只显示某版本 SDK 文档”的 filter。
- 从设置界面读取用户选中的组件和版本，再写回 engine。
- 用 `filterData(filterName)` 读取现有配置并显示在编辑控件中。
- 在测试中构造不同条件，验证目录和搜索结果是否正确收敛。

## 空列表与值语义

默认构造得到空 filter。空组件列表表示不按 component 约束，空版本列表表示不按 version 约束；两者都为空时通常相当于不限制这两个维度，而不是“返回零条结果”。

`setComponents()` 和 `setVersions()` 会复制传入容器，调用者之后修改原列表不会影响 filter。getter 也按值返回，适合在设置界面中编辑临时副本，再一次性提交给 `QHelpFilterEngine`。

这是隐式共享值类型。拷贝便宜，修改时由 Qt 处理数据分离。它没有线程亲和性，但把它提交给 QObject 过滤器引擎的操作仍应在引擎所属线程完成。

## 过滤语义

组件和版本条件分别约束文档的 metadata：只返回 component 在列表中的文档，只返回 version 在列表中的文档。列表中的多个值表示允许集合，而不是字符串前缀或版本范围表达式；需要范围逻辑时，应先把具体版本整理成明确列表。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QHelpFilterData()` | 构造没有 component/version 约束的空 filter。 | 空列表通常表示该维度不限制。 |
| `QHelpFilterData(const QHelpFilterData &other)` | 拷贝 filter 条件。 | 值语义；不会复制或创建 engine 中的 filter 名称。 |
| `QHelpFilterData(QHelpFilterData &&other)` | 移动构造 filter 条件。 | 适合接收临时设置结果。 |
| `~QHelpFilterData()` | 释放 filter 值对象。 | 不会从 `QHelpFilterEngine` 删除同名 filter。 |
| `operator=(const QHelpFilterData &other)` | 拷贝赋值。 | 只改变当前值。 |
| `operator=(QHelpFilterData &&other)` | 移动赋值。 | 移动后源对象只保证可析构和重新赋值。 |
| `bool operator==(const QHelpFilterData &other) const` | 比较 component 和 version 条件是否相同。 | 相同条件不代表在 engine 中使用了相同 filter 名称。 |
| `void swap(QHelpFilterData &other)` | 交换两个 filter 条件。 | `noexcept` 且不会触及 engine 或 collection。 |
| `void setComponents(const QStringList &components)` | 指定允许的 component 集合。 | 列表是允许集合；空列表通常取消 component 限制。 |
| `QStringList components() const` | 返回当前 component 条件。 | 返回副本；可直接交给设置界面编辑。 |
| `void setVersions(const QList<QVersionNumber> &versions)` | 指定允许的版本集合。 | 使用明确版本值，不是自动解析的范围表达式。 |
| `QList<QVersionNumber> versions() const` | 返回当前 version 条件。 | 空列表通常取消版本限制。 |

## 一句话总结

`QHelpFilterData` 只描述过滤条件，不管理 filter 名称；用空列表表示不限制，用明确 component/version 集合表达允许文档。
