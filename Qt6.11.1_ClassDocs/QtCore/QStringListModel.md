# QStringListModel
> Qt 6.11.1 · Qt Core · 来自 `QStringListModel`

## 作用定位
`QStringListModel` 将 `QStringList` 暴露为一列模型，适合列表控件、补全器、简单可编辑文本列表。复杂多列或多角色数据应写自定义模型。

## API 速查
| API | 是做什么的 |
|---|---|
| `setStringList()` | 用列表替换模型内容。 |
| `stringList()` | 取回当前字符串列表。 |
| `data()` / `setData()` | 读写显示/编辑角色文本。 |
| `insertRows()` / `removeRows()` | 改变行结构。 |
| `rowCount()` | 查询项目数。 |
| `flags()` | 声明项目是否可编辑。 |

## 使用场景
```cpp
auto *model = new QStringListModel(words, this);
auto *completer = new QCompleter(model, this);
lineEdit->setCompleter(completer);
```

## 常见坑与经验
- 它是一列模型；需要 id、图标、状态等多角色时不要硬塞进字符串。
- 修改底层列表应通过模型 API 或 `setStringList()`，保持视图通知。
- 大量增删时考虑批量替换或自定义模型优化。

## 知识点覆盖
模型/视图、一列数据、编辑角色、补全器、结构通知。
