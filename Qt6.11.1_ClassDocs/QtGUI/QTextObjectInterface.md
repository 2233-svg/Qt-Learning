# QTextObjectInterface
> Qt 6.11.1 · Qt GUI · 来自 `QTextObjectInterface`

## 1. 先建立直觉

`QTextObjectInterface` 是自定义 inline object 的绘制接口。你实现它，告诉 `QTextDocument` 某种 object type 的内联对象需要多大，以及如何绘制。

## 2. 类说明

- 头文件：`#include <QTextObjectInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：接口类
- 协作类：`QTextDocument::documentLayout()`、`QTextCharFormat`、`QTextInlineObject`

实现类通常同时继承 `QObject`，再用 `QTextDocumentLayout::registerHandler(objectType, handler)` 注册。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `intrinsicSize(doc, pos, format)` | 返回自定义对象天然尺寸 |
| `drawObject(painter, rect, doc, pos, format)` | 在给定矩形中绘制对象 |

## 4. 关键用法

```cpp
class BadgeObject : public QObject, public QTextObjectInterface {
    Q_OBJECT
    Q_INTERFACES(QTextObjectInterface)
public:
    QSizeF intrinsicSize(QTextDocument *, int, const QTextFormat &) override;
    void drawObject(QPainter *, const QRectF &, QTextDocument *, int,
                    const QTextFormat &) override;
};
```

插入时使用 `QChar::ObjectReplacementCharacter` 和带 object type 的 `QTextCharFormat`。

## 5. 使用场景

公式、mention、tag、状态徽章、富文本中的自定义图形对象、编辑器里的不可拆分 token。

## 6. 常见坑与经验

- handler 对象必须在文档使用期间保持存活。
- `intrinsicSize()` 要快且稳定，频繁变化会导致布局抖动。
- 它负责绘制，不是嵌入 QWidget。
- format 属性是传参渠道，设计好自定义 property id。

## 7. 知识点覆盖

自定义文本对象、尺寸回调、绘制回调、handler 注册、object replacement character。
