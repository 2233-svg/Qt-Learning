# QHelpSearchResultWidget
> Qt 6.11.1 · Qt Help · 来自 `QHelpSearchResultWidget`

## 1. 先建立直觉

`QHelpSearchResultWidget` 是搜索结果显示控件。它展示标题和摘要，用户点击结果时发出要打开的帮助链接。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpSearchResultWidget`，属于 Qt Help 模块，用于显示帮助搜索结果并通知链接激活。

通常通过 `QHelpSearchEngine::resultWidget()` 获取。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `linkAt(point)` | 查询某个坐标位置对应的结果链接。 |
| `requestShowLink(link)` | 用户请求打开某条结果时发出。 |

## 4. 典型流程

```cpp
connect(search->resultWidget(), &QHelpSearchResultWidget::requestShowLink,
        this, &HelpWindow::showHelpUrl);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 搜索结果页 | 直接显示搜索结果。 |
| 鼠标悬停预览 | 用 `linkAt()` 判断当前位置链接。 |
| 点击打开文档 | 连接 `requestShowLink()`。 |

## 6. 常见坑与经验

结果控件不负责加载 HTML。它只告诉你用户想打开哪个 URL。

坐标是控件局部坐标，和屏幕全局坐标不同。

## 7. 知识点覆盖

- 搜索结果 UI。
- 坐标到链接查询。
- 结果激活和文档显示分离。
