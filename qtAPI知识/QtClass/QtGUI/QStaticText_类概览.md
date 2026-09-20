# Qt QStaticText：重复绘制文本的布局缓存值类型

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStaticText>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 类型定位：供 `QPainter::drawStaticText()` 使用的隐式共享文本缓存

## 1. 它解决什么问题

`QStaticText` 用于“文本内容和排版参数重复不变，但需要频繁绘制”的场景。它可以缓存文本布局和绘制准备结果，减少每一帧重复解析、排版和计算的成本。

典型场景：

- 自定义控件每帧绘制固定标签；
- 图表轴标题、刻度说明或水印；
- 游戏/动画界面中的静态 UI 文本；
- 绘制大量相同格式的说明文字。

它不是普通的 `QString` 替代品，也不是通用文本编辑器模型。文本、格式、宽度、文本选项或变换发生变化后，缓存可能失效，需要重新准备。

## 2. 构建与最小用法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QPainter>
#include <QStaticText>

class LabelWidget : public QWidget
{
public:
    LabelWidget(QWidget *parent = nullptr)
        : QWidget(parent),
          text(QStringLiteral("固定提示"))
    {
        text.prepare(QTransform(), font());
    }

protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter painter(this);
        painter.drawStaticText(QPointF(12, 12), text);
    }

private:
    QStaticText text;
};
```

`QStaticText` 只保存文本及其缓存状态，实际绘制仍由 `QPainter::drawStaticText()` 完成。

## 3. 核心工作模型

```text
设置 text / format / width / option
    -> 可选：prepare(matrix, font)
    -> QPainter::drawStaticText(position, staticText)
    -> 内容或绘制条件改变时重新 prepare
```

缓存是否真正带来收益取决于文本复杂度、绘制次数、字体、变换和后端。短文本只画一次时，使用 `QStaticText` 不一定比直接 `drawText()` 更快。

## 4. 文本格式和文本宽度

### 4.1 `setTextFormat()` / `textFormat()`

`Qt::TextFormat` 决定字符串按纯文本、富文本或自动识别处理。纯文本适合不需要 HTML 解释的内容；富文本会引入解析和布局成本，文本来源不可信时还要避免把用户输入误当成 markup。

`Qt::AutoText` 会根据内容推断格式。若业务需要稳定语义，应显式设置 `Qt::PlainText` 或 `Qt::RichText`。

### 4.2 `setTextWidth()` / `textWidth()`

文本宽度影响换行和最终 `size()`：

- 负值通常表示不限制宽度；
- 非负宽度会参与布局和换行；
- 改变宽度会使已有布局缓存失效；
- 宽度是逻辑绘制坐标中的浮点值。

如果需要固定区域内换行，应同时设置宽度和适当的 `QTextOption`。

## 5. `QTextOption` 和尺寸

### `setTextOption(const QTextOption &)`

设置换行、对齐、制表位和其他排版选项。改变 option 后应重新考虑缓存准备。

### `textOption() const`

返回当前文本选项值副本。

### `size() const`

返回按当前文本、格式、宽度和文本选项计算出的布局尺寸。它不是 widget 的 sizeHint，也不包含绘制位置、外部 margin 或 painter transform 造成的屏幕包围盒变化。

如果字体或变换影响布局，应用应在对应参数确定后再读取 size。

## 6. `prepare()` 的语义

```cpp
void prepare(const QTransform &matrix = QTransform(),
             const QFont &font = QFont());
```

`prepare()` 预先为给定变换和字体准备绘制缓存：

```cpp
staticText.prepare(widget->deviceTransform(widget->windowHandle()),
                   widget->font());
```

注意：

- `matrix` 和 `font` 会影响缓存的适用条件；
- 之后用不同字体、不同变换或不同设备条件绘制，可能重新准备或不能复用原缓存；
- 改变 text、text format、text width 或 text option 后，应重新调用；
- `prepare()` 不是强制“编译”，只是提前准备，最终绘制仍由 painter 完成；
- 没有重复绘制收益时，不必为了调用而调用。

不同设备像素比、缩放和 painter transform 可能导致同一逻辑文本需要不同缓存。

## 7. `PerformanceHint`

```cpp
enum PerformanceHint {
    ModerateCaching,
    AggressiveCaching
};
```

- `ModerateCaching`：适度缓存，平衡内存和准备成本；
- `AggressiveCaching`：更积极地缓存，适合反复绘制且缓存占用可接受的文本。

这是性能提示，不是功能开关，也不是“必然更快”的保证。应根据绘制频率、文本数量、字体变化和内存预算选择。

## 8. 成员函数语义

### `QStaticText()`

创建空 static text。空对象没有有意义的绘制内容。

### `QStaticText(const QString &text)`

用文本创建对象。格式、宽度和文本选项仍使用默认设置。

### `QStaticText(const QStaticText &other)`

复制 static text。它是值类型并使用共享数据，复制通常成本较低；修改副本时按值语义分离。

### `operator=(const QStaticText &other)`

复制赋值，目标对象获得源对象的文本和缓存逻辑状态。

### `~QStaticText()`

销毁值对象和共享缓存引用，不涉及任何 painter 或 widget。

### `swap(QStaticText &other)`

交换两个对象的数据，适合高效更新缓存对象。不会进行重新排版或绘制。

### `setText(const QString &text)` / `text() const`

设置或读取文本。设置文本会让依赖旧文本的布局缓存失效。`text()` 返回值副本。

### `setPerformanceHint(PerformanceHint)` / `performanceHint() const`

设置或读取缓存策略提示。它不改变文本内容，也不保证立即分配或释放全部缓存。

### `operator==` / `operator!=`

比较对象值是否相等。相等判断适合缓存键或测试，不应拿来判断两个对象在任意 painter transform 下是否有完全相同的 GPU 资源。

## 9. 生命周期、线程和绘制边界

`QStaticText` 不继承 `QObject`，可以作为成员或按值传递。它不拥有 `QPainter`、字体引擎上下文或 widget。

同一个值对象的读取和绘制应遵循 Qt GUI 线程约定。若工作线程准备文本，完成后传递不可变副本给 GUI 线程更稳妥；不要让一个线程修改文本，同时另一个线程绘制同一个实例。

## 10. 常见误区与排查顺序

### 10.1 内容变化后仍假设旧缓存有效

调用 `setText()`、`setTextFormat()`、`setTextWidth()` 或 `setTextOption()` 后，重新考虑 `prepare()`。

### 10.2 把 `QStaticText` 当作文本编辑模型

它没有光标、选区、编辑操作和文档结构。需要编辑、复杂段落或动态排版时使用 `QTextDocument`、`QTextLayout` 等类型。

### 10.3 把 `size()` 当成最终屏幕像素尺寸

`size()` 是当前布局坐标中的尺寸，painter 的变换、DPR 和设备会影响最终像素覆盖范围。

### 10.4 对只绘制一次的文本强行缓存

缓存有准备成本和内存成本。只有在重复绘制、文本和格式相对稳定时才更可能收益。

### 10.5 用不同字体或 transform 绘制已准备文本

准备条件与绘制条件不一致时，缓存可能失效或需要重新准备。高 DPI、缩放窗口和多屏幕场景尤其要注意。

### 10.6 把 `AggressiveCaching` 当成质量选项

它只提示缓存策略，不会提高字体质量，也不替代正确的 antialiasing、字体和 painter 设置。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 枚举 | `ModerateCaching` | 适度缓存提示 | 平衡内存和准备开销 |
| 枚举 | `AggressiveCaching` | 积极缓存提示 | 不是必然更快或质量选项 |
| 构造 | `QStaticText()` | 创建空对象 | 没有可绘制文本 |
| 构造 | `QStaticText(const QString &)` | 用文本创建 | 其他排版属性仍为默认值 |
| 构造 | `QStaticText(const QStaticText &)` | 复制对象 | 值语义，共享数据可能分离 |
| 赋值 | `operator=(const QStaticText &)` | 复制赋值 | 不涉及 painter 或 widget |
| 析构 | `~QStaticText()` | 销毁对象 | 不销毁外部绘图资源 |
| 工具 | `swap(QStaticText &)` | 交换数据 | 不重新排版、不绘制 |
| 设置 | `setText(const QString &)` | 设置文本 | 可能使缓存失效 |
| 查询 | `text() const` | 读取文本 | 返回值副本 |
| 设置 | `setTextFormat(Qt::TextFormat)` | 设置纯文本/富文本语义 | AutoText 可能推断格式 |
| 查询 | `textFormat() const` | 读取文本格式 | 影响解析和布局 |
| 设置 | `setTextWidth(qreal)` | 设置布局宽度 | 影响换行；负值通常不限制 |
| 查询 | `textWidth() const` | 读取布局宽度 | 是逻辑坐标宽度 |
| 设置 | `setTextOption(const QTextOption &)` | 设置排版选项 | 改变后需重新考虑缓存 |
| 查询 | `textOption() const` | 读取排版选项 | 返回值副本 |
| 查询 | `size() const` | 获取布局尺寸 | 不是最终屏幕像素包围盒 |
| 准备 | `prepare(const QTransform &, const QFont &)` | 预先准备绘制缓存 | transform/font 要与绘制条件匹配 |
| 设置 | `setPerformanceHint(PerformanceHint)` | 设置缓存提示 | 不是功能或质量开关 |
| 查询 | `performanceHint() const` | 读取缓存提示 | 不表示缓存一定已分配 |
| 绘制 | `QPainter::drawStaticText()` | 实际绘制 static text | `QStaticText` 本身不绘制 |
| 比较 | `operator==` | 比较值内容 | 不是任意设备上的资源等价 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`QStaticText` 是面向重复绘制的文本布局缓存：用 `QPainter::drawStaticText()` 绘制，用 text、format、width、option、font 和 transform 决定缓存条件；内容或绘制条件变化时要重新准备，短文本只画一次时不必强行使用。
