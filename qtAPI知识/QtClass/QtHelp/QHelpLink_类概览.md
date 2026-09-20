# QHelpLink：帮助文档链接的数据结构

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpLink>`  
> 所属模块：`Qt6::Help`  
> 类型：`struct`，无基类

## 它解决什么问题

`QHelpLink` 用两个字段描述一条帮助文档链接：

- `title`：文档标题。
- `url`：文档目标 URL。

它不是可点击控件，也不负责打开页面。它只是 Qt Help 在“关键词、标识符对应哪些文档”这类查询结果中使用的值类型，让调用者可以同时拿到用户可读的标题和真正的导航地址。

## 实际使用场景

- 读取 `QHelpEngineCore::documentsForKeyword()` 或 `documentsForIdentifier()` 的结果。
- 接收 `QHelpIndexWidget::documentActivated()` 和 `documentsActivated()` 信号。
- 在“同一关键词命中多个文档”的选择对话框中显示 `title`，用 `url` 打开最终文档。
- 将帮助链接放入 `QList<QHelpLink>`、缓存到业务对象，或转换为自定义导航项。

## 值语义与生命周期

`QHelpLink` 是 `struct`，没有 QObject 身份、父对象、信号槽或独立线程归属。它可以直接复制、放进 Qt 容器并按值传递。字段本身是公开的，允许直接读取和修改：

```cpp
QHelpLink link;
link.title = QStringLiteral("QHelpEngine");
link.url = QUrl(QStringLiteral("qthelp://my.manual/doc/qhelpengine.html"));

QList<QHelpLink> links = helpEngine.documentsForKeyword(QStringLiteral("QHelpEngine"));
for (const QHelpLink &item : links) {
    qDebug() << item.title << item.url;
}
```

从帮助引擎得到的对象是查询结果的副本。修改本地变量的字段不会修改 collection 中的注册文档，也不会改变引擎的索引。

## 字段的边界

`url` 通常是 `qthelp://` URL，但结构本身不限制 URL scheme。是否能由 `QHelpEngineCore::fileData()` 读取、是否应交给外部浏览器打开，由 URL 类型和应用策略决定。调用者应检查 URL 是否有效，并避免把不可信 URL 直接交给外部程序。

`title` 是显示文本，不是唯一标识。多个文档可能有相同标题，应用需要使用 `url` 区分目标。空标题或无效 URL 也可以存在于一个手工构造的 `QHelpLink` 中，Qt 不会替应用补全或校验字段。

## 常见误区

- 把 `QHelpLink` 当成 `QUrl`：它同时包含标题和 URL，导航时通常使用 `link.url`。
- 认为修改 `title` 或 `url` 会回写帮助数据库：它只是一个值对象。
- 用标题判断文档唯一性：应优先使用规范化后的 URL。
- 忽略 `documentsActivated()`：一个关键词可能关联多个 `QHelpLink`。
- 把无效 URL 当作已经定位到正文：使用前应检查 `QUrl::isValid()` 和 scheme。

## 与相关类型的分工

- `QHelpEngineCore`：产生和查询 `QHelpLink` 列表。
- `QHelpIndexWidget`：在索引项激活时通过信号传出一个或多个 `QHelpLink`。
- `QUrl`：表示目标地址，但不保存文档标题。
- `QString`：保存用户可读的标题。

## 逐项 API 说明

### `QString QHelpLink::title`

公开成员变量，保存链接对应文档的标题。适合用于列表、菜单或候选文档对话框的显示。它不是稳定的文档 ID，也不保证非空。

### `QUrl QHelpLink::url`

公开成员变量，保存链接的目标 URL。帮助系统中通常指向 `qthelp://` 虚拟地址；是否有效、是否能读取以及如何打开由调用者负责判断。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 公共字段 | `QString title` | 保存帮助文档的显示标题。 | 标题不保证唯一，也可能为空。 |
| 公共字段 | `QUrl url` | 保存帮助文档的目标 URL。 | 常见为 `qthelp://`；导航前检查有效性和 scheme。 |
| 值语义 | `QHelpLink` | 可默认构造、复制并放入 Qt 容器的链接值对象。 | 没有 QObject 生命周期和所有权；修改只影响本地值。 |

---

### 一句话总结

`QHelpLink` 只是“文档标题 + 文档 URL”的值类型；它承载查询结果，不负责索引、渲染或导航。
