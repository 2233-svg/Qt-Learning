# QHelpContentModel
> Qt 6.11.1 · Qt Help · 来自 `QHelpContentModel`

## 1. 先建立直觉

`QHelpContentModel` 是帮助目录树的 model。它把已注册文档包里的 table of contents 暴露给 `QTreeView`，每个索引对应一个 `QHelpContentItem`。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpContentModel`，属于 Qt Help 模块，用于提供帮助内容树的 Model/View 数据。

应用通常通过 `QHelpEngine::contentModel()` 获取它。现成视图是 `QHelpContentWidget`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `createContents(customFilterName)` | 按过滤器创建/刷新目录树。 |
| `contentItemAt(index)` | 从模型索引取得 `QHelpContentItem`。 |
| `index(row, column, parent)`、`parent(index)` | 树模型索引关系。 |
| `rowCount()`、`columnCount()` | 行列数。 |
| `data(index, role)` | 返回标题等显示数据。 |
| `isCreatingContents()` | 判断目录树是否正在生成。 |
| `contentsCreated()` | 目录树创建完成信号。 |
| `contentsCreationStarted()` | 创建开始信号。 |

## 4. 典型流程

```cpp
auto *model = engine->contentModel();
connect(model, &QHelpContentModel::contentsCreated, this, &HelpWindow::expandRoot);
model->createContents(engine->filterEngine()->activeFilter());
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 自定义帮助目录树 | 绑定到自己的 QTreeView。 |
| 根据过滤器刷新目录 | 调用 `createContents(filter)`。 |
| URL 与目录同步 | index -> content item -> url。 |

## 6. 常见坑与经验

内容创建可能不是瞬时完成。依赖目录树的 UI 操作应等 `contentsCreated()`。

filter 改变后要重新创建内容树，否则目录仍可能显示旧范围。

## 7. 知识点覆盖

- 帮助 TOC 的模型表示。
- Model/View 树索引与 content item。
- 过滤器驱动的目录刷新。
