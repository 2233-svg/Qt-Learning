<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QAbstractGraphicsShapeItem 深入笔记

> 头文件：`#include <QAbstractGraphicsShapeItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QAbstractGraphicsShapeItem`  
> 性质：抽象的“描边 + 填充”形状图元基类

## 1. 它解决什么问题

`QAbstractGraphicsShapeItem` 将形状图元都会遇到的两种视觉状态统一起来：

- `QPen`：轮廓怎样画，包括颜色、宽度、线型、端点和连接方式。
- `QBrush`：形状内部怎样填充，包括纯色、纹理、渐变或不填充。

它不定义轮廓本身。矩形、椭圆、路径、多边形各自决定自己的几何，而这个基类负责让它们以一致方式配置和保存 pen/brush。

```text
QGraphicsItem
  └─ QAbstractGraphicsShapeItem
       ├─ QGraphicsPathItem
       ├─ QGraphicsRectItem
       ├─ QGraphicsEllipseItem
       └─ QGraphicsPolygonItem
```

注意：`QGraphicsSimpleTextItem` 直接继承 `QGraphicsItem`，不属于这条“填充几何形状”继承链。

## 2. 为什么不能只把它理解成两个 setter

对形状图元而言，pen 和 brush 不只改变颜色：

```text
pen 宽度、连接方式、端点
        ↓
可能扩展可见轮廓、包围范围和命中形状
        ↓
影响 scene 重绘区域、点击命中与遮挡优化
```

例如一个矩形设置 12 像素宽的描边后，肉眼能看到的边缘不再等于原始 `rect()`；标准 `QGraphicsRectItem` 等派生类会把 pen 的影响纳入自身 `boundingRect()` 与 `shape()` 计算。

因此，“图元明明画出来了却点击不到”或“粗边被裁掉”时，不能只查画笔颜色，还要检查具体派生类的 `shape()`、`boundingRect()` 与 pen 是否一致。

## 3. 直接使用应选具体形状项

这个类仍然是抽象类，不能直接创建。平常选择具体图元：

```cpp
#include <QGraphicsRectItem>
#include <QPen>
#include <QBrush>

auto *card = new QGraphicsRectItem(0, 0, 160, 72);
card->setPen(QPen(QColor("#4d6a85"), 2.0));
card->setBrush(QBrush(QColor("#eaf4ff")));
scene->addItem(card);
```

要实现新的形状，例如六边形、流程图节点、可编辑贝塞尔区域，才从 `QAbstractGraphicsShapeItem` 派生。此时除了复用 pen/brush，还必须实现 `QGraphicsItem` 的 `boundingRect()`、`shape()` 与 `paint()`，并保证三者描述的是同一个几何事实。

## 4. `QPen`：描边的边界和交互影响

```cpp
QPen pen(QColor("#2266aa"));
pen.setWidthF(2.5);
pen.setStyle(Qt::DashLine);
pen.setJoinStyle(Qt::RoundJoin);
shape->setPen(pen);
```

未显式设置 pen 时，`pen()` 返回默认的黑色、宽度 `1` 实线画笔。若不想绘制轮廓，应明确写：

```cpp
shape->setPen(Qt::NoPen);
```

不要把透明 pen 当作 `Qt::NoPen` 的等价物：透明 pen 仍可能参与几何和样式计算，而 `NoPen` 明确表示没有轮廓。

自定义子类的 `boundingRect()` 应预留描边厚度，特别是粗笔、尖角连接（`MiterJoin`）或可变宽度画笔。改变形状几何、或 pen 会使有效范围变化时，要遵守 `prepareGeometryChange()` 的规则；标准 Qt 形状项已为自己的 setter 处理这一点。

## 5. `QBrush`：填充不只是单色

```cpp
shape->setBrush(QBrush(QColor("#d9f2e6")));
shape->setBrush(Qt::NoBrush);
```

未显式设置 brush 时，`brush()` 返回 `Qt::NoBrush`，即只画轮廓、不填内部。

brush 还可承载渐变和纹理：

```cpp
QLinearGradient gradient(0, 0, 160, 72);
gradient.setColorAt(0.0, QColor("#eaf4ff"));
gradient.setColorAt(1.0, QColor("#8dc5ff"));
shape->setBrush(gradient);
```

渐变的坐标相对于图元本地坐标。图元移动到 scene 的其它位置时，渐变随图元一起移动；若想实现跨多个图元保持连续的背景渐变，需要自行用 scene 坐标或 painter 变换设计，而不能期待默认 brush 自动对齐。

## 6. 绘制、命中和遮挡不是同一个问题

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 绘制 | `paint()` | 使用 pen、brush 和具体形状把图元画出来 | 只负责绘制，不自动定义点击区域或碰撞区域 |
| 命中与碰撞 | `shape()` | 返回精确命中和碰撞使用的路径 | 它影响选择、碰撞和鼠标命中；不决定重绘索引范围 |
| 重绘范围 | `boundingRect()` | 给 scene 一个保守的重绘和索引范围 | 必须包含实际绘制区域；不必像 `shape()` 那样精确 |
| 遮挡优化 | `opaqueArea()` | 告诉 scene 哪些区域完全不透明 | 用于遮挡优化，不是鼠标命中 API |
| 遮挡判断 | `isObscuredBy()` | 判断另一个 item 是否足以遮住当前 item | 不等同于几何相交；它服务于可见性和绘制优化 |

基类重写的 `opaqueArea()` 和 `isObscuredBy()` 使用形状项的 pen/brush 信息帮助 scene 做遮挡优化。自定义派生类若改变了“哪些区域真正不透明”的含义，应重写对应逻辑；否则不要为了“碰撞更准确”去乱改 `opaqueArea()`，那是不同的问题。

## 7. 什么时候继承它，什么时候直接继承 `QGraphicsItem`

选择 `QAbstractGraphicsShapeItem`：

- 图元确实是一个可填充的几何形状。
- 希望对外提供标准 `pen()` / `brush()` 接口。
- 轮廓、填充、命中形状大体围绕同一条路径。

直接继承 `QGraphicsItem`：

- 图元是文本、图片、句柄、容器或完全自定义绘制。
- 没有统一的“边框 + 填充”语义。
- 绘制由多层素材、子图元或动态 painter 状态组成。

不要为了少写两个成员就强行使用本类。合适的基类应反映外部 API 语义，而不是只看实现复用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QAbstractGraphicsShapeItem(QGraphicsItem *parent = nullptr)` | 初始化形状图元基类并可指定图元父项。 | 抽象类，只供具体形状类或自定义派生类使用。 |
| 析构 | `~QAbstractGraphicsShapeItem()` | 销毁形状图元基类部分。 | 由图元父子树或 scene 生命周期统一管理。 |
| 描边读取 | `QPen pen() const` | 返回当前轮廓画笔。 | 默认是黑色、宽度 `1` 的实线画笔。 |
| 描边设置 | `void setPen(const QPen &pen)` | 设置轮廓画笔。 | 宽笔和连接方式会影响可见边界；无轮廓用 `Qt::NoPen`。 |
| 填充读取 | `QBrush brush() const` | 返回当前内部填充画刷。 | 默认 `Qt::NoBrush`，表示不填充。 |
| 填充设置 | `void setBrush(const QBrush &brush)` | 设置形状内部的填充方式。 | 渐变坐标是图元本地坐标；无填充用 `Qt::NoBrush`。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断给定图元是否足以遮住本形状项。 | 用于 scene 绘制优化，不是通用碰撞检测。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回已知完全不透明的区域。 | 用于遮挡/重绘优化，不是鼠标命中路径。 |
| 受保护构造 | `QAbstractGraphicsShapeItem(QAbstractGraphicsShapeItemPrivate &, QGraphicsItem *parent)` | Qt 私有实现的构造入口。 | 私有参数类型，普通派生类不应调用。 |

## 9. 排查清单

1. 粗描边被裁掉：检查派生类 `boundingRect()` 是否包含 pen 宽度和连接样式。
2. 图元可见却点不到：检查 `shape()`，不要把 `opaqueArea()` 当命中范围。
3. 改了 pen/brush 画面未刷新：标准图元使用 setter 即可；自定义缓存绘制时检查是否正确调用更新。
4. 渐变在多个图元间不连续：默认 brush 使用本地坐标，需要自定义坐标策略。
5. 想画“无边框”：使用 `Qt::NoPen`，不要仅把颜色设为透明。

### 一句话总结

`QAbstractGraphicsShapeItem` 为几何形状图元提供统一的描边和填充语义；真正的关键不在两个 setter，而在 pen/brush 如何影响具体派生类的可见边界、命中形状和遮挡优化。
