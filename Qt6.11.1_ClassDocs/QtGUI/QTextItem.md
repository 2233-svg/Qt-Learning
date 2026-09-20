# QTextItem

> Qt 6.11.1 · Qt GUI · 来自 `QTextItem`

## 1. 先建立直觉

`QTextItem` 是 `QPainter` 在执行文字绘制时交给某些低层回调的一小段“已经布局好的文本”。它不是可自由构造的文本模型，也不是日常 UI 代码应保存的对象；它暴露这段文字、字体、宽度、基线度量与装饰标记，方便你在绘制引擎或代理逻辑中检查实际输出。

通常你不会主动创建 `QTextItem`。它主要出现在重载 `QPaintEngine::drawTextItem()` 等绘制管线扩展点；普通程序请使用 `drawText()`、`QTextLayout` 或 `QStaticText`。

## 2. 类说明

- 头文件：`#include <QTextItem>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：绘制期间的只读视图，构造与生命周期由 Qt 绘制系统控制。
- 没有公开构造、修改或持久化接口；不要跨越绘制回调保存引用或指针。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `text()` | 读取当前待绘制的文本片段 |
| `font()` | 读取该片段实际使用的 `QFont` 请求 |
| `width()` | 读取该片段已经布局好的逻辑宽度 |
| `ascent()` | 读取基线以上高度 |
| `descent()` | 读取基线以下高度 |
| `renderFlags()` | 查询文字方向与装饰线标志 |
| `RenderFlag::RightToLeft` | 片段按右到左视觉方向绘制 |
| `RenderFlag::Overline` | 片段带上划线 |
| `RenderFlag::Underline` | 片段带下划线 |
| `RenderFlag::StrikeOut` | 片段带删除线 |

## 4. 关键用法

### 在自定义绘制引擎中观察文本片段

```cpp
void MyPaintEngine::drawTextItem(const QPointF &pos,
                                 const QTextItem &item)
{
    qDebug() << item.text()
             << item.width()
             << item.ascent()
             << item.descent()
             << item.renderFlags();

    // 将 item 交给你的后端，或按后端协议转换。
}
```

`pos` 通常与基线相关，而 `ascent()`、`descent()` 给出上下范围。若你把它误当作左上角坐标，会造成垂直偏移。

### 正确处理方向和装饰

```cpp
const auto flags = item.renderFlags();
if (flags.testFlag(QTextItem::RightToLeft)) {
    // 保持布局提供的视觉方向，不要仅靠 reverse(text())。
}
if (flags.testFlag(QTextItem::Underline)) {
    // 由后端绘制与字体度量匹配的下划线。
}
```

对 RTL 文本不能简单翻转 `item.text()`；双向算法、数字和中性字符的视觉顺序远比字符串反转复杂。后端应把 `RightToLeft` 当作渲染语义，而不是文本变换指令。

## 5. 使用场景

- 自定义 `QPaintEngine`、打印后端或录制型绘制后端。
- 调试 Qt 文字绘制管线，检查每次下发的片段与装饰。
- 在低层后端中把 Qt 的文本参数映射到第三方渲染 API。

## 6. 常见坑与经验

- **不是通用文本布局类。** 它没有换行、光标、选区或字形列表；复杂需求回到 `QTextLayout`。
- **生命周期短。** 只在 Qt 传入它的当前回调内读取；不要存储其引用。
- **`width()` 是布局宽度，不必等于像素墨迹边界。** 背景与裁剪仍需正确的字体/字形测量。
- **`font()` 仍是字体请求。** 真正物理匹配和 glyph 回退可能由后端/设备决定。
- **装饰线不是可忽略的装饰。** 忽略 `Underline`、`StrikeOut` 会让富文本和无障碍语义在自定义后端中丢失。

## 7. 知识点覆盖

QPainter 绘制管线、绘制回调生命周期、基线、RTL 语义、文本装饰、布局宽度与墨迹范围、低层渲染后端。
