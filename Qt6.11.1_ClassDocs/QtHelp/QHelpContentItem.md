# QHelpContentItem
> Qt 6.11.1 · Qt Help · 来自 `QHelpContentItem`

## 1. 先建立直觉

`QHelpContentItem` 是帮助目录树中的一个节点。它有标题、URL、父节点、子节点，通常对应文档目录里的某一章或某个页面。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpContentItem`，属于 Qt Help 模块，用于表示帮助内容树条目。

它由 `QHelpContentModel` 管理，应用通常只读取它，不自己 new/delete。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `title()` | 返回目录项标题。 |
| `url()` | 返回点击后应打开的帮助链接。 |
| `parent()` | 返回父目录项。 |
| `child(row)` | 返回指定子项。 |
| `childCount()` | 子项数量。 |
| `childPosition(child)` | 查询某个子项的位置。 |
| `row()` | 当前项在父项中的行号。 |

## 4. 典型流程

```cpp
QHelpContentItem *item = model->contentItemAt(index);
if (item)
    openHelpUrl(item->url());
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 自定义目录树视图 | 从 item 读取 title/url。 |
| 面包屑导航 | 用 parent() 向上回溯。 |
| 同步当前页面 | 根据 URL 找 item，再展开到该节点。 |

## 6. 常见坑与经验

不要保存裸指针很久。内容模型重建或 filter 切换后，旧 item 指针可能不再适合使用。

title 只是显示文本，真正打开文档应使用 url。

## 7. 知识点覆盖

- 帮助目录树节点。
- 标题、链接、父子关系。
- 与 content model/widget 的关系。
