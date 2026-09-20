# Qt QStyle 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QStyle>`
> 所属模块：`Qt6::Widgets`
> 继承：`QObject -> QStyle`
> 常见搭档：`QWidget`、`QStyleOption`、`QProxyStyle`

## 1. QStyle 解决什么问题

`QStyle` 定义的是“控件该怎么画、间距该怎么算、标准图标该长什么样、控件的子区域在哪里”。

它不是某一个控件，而是一整套 UI 规则接口。Qt 的各种按钮、菜单、滚动条、标题栏、标签页，都会向 style 问这些问题：

- 这个控件怎么画；
- 这个子控件在哪；
- 这个控件有多大合适；
- 这个标准图标该返回什么；
- 这个布局间距该是多少。

`QStyle` 通常不直接实例化，而是由 `QCommonStyle` 或 `QProxyStyle` 这类派生类实现。

## 2. 你真正会用到的是什么

大多数普通项目不会直接写一个完整 `QStyle`，而是：

```cpp
QWidget *w = ...;
QStyle *s = w->style();
```

然后调用它的查询或绘制辅助函数。

```cpp
style()->drawPrimitive(QStyle::PE_FrameFocusRect, &opt, &painter, widget);
```

这类调用通常出现在自定义控件和 delegate 绘制里。

## 3. 纯虚接口是骨架

```cpp
drawPrimitive(...)
drawControl(...)
drawComplexControl(...)
generatedIconPixmap(...)
hitTestComplexControl(...)
layoutSpacing(...)
pixelMetric(...)
sizeFromContents(...)
standardIcon(...)
standardPixmap(...)
styleHint(...)
subControlRect(...)
subElementRect(...)
```

如果你在做自定义 style，最关键的是这些函数。

它们分别回答：

- `drawPrimitive`：画最基础的部件；
- `drawControl`：画复合控件中的标准部分；
- `drawComplexControl`：画有多个子区域的复杂控件；
- `subControlRect`：某个子控件矩形在哪；
- `hitTestComplexControl`：点到了哪个子控件；
- `sizeFromContents`：控件内容决定多大；
- `pixelMetric`：某个像素参数是多少；
- `styleHint`：某个行为提示是什么；
- `standardIcon` / `standardPixmap`：标准图标/像素图是什么。

## 4. 静态辅助函数

```cpp
QStyle::visualRect(direction, boundingRect, logicalRect);
QStyle::alignedRect(direction, alignment, size, rect);
QStyle::sliderPositionFromValue(...);
QStyle::sliderValueFromPosition(...);
```

这些是样式实现和右到左布局处理里很常用的工具函数。

`proxy()` 也很关键：它说明当前 style 背后是否还有代理风格。

## 5. 什么时候会接触它

你会在这些地方碰到 `QStyle`：

- 自定义控件绘制；
- delegate 绘制；
- 想适配平台原生外观；
- 想拿标准间距、图标、像素参数；
- 想理解为什么同一个按钮在不同平台长得不一样。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `PrimitiveElement` / `ControlElement` / `ComplexControl` | 标识基础图元、标准控件元素和复杂控件的绘制目标。 | 传给绘制接口时必须与 `QStyleOption` 的具体类型匹配。 |
| 类型 | `SubElement` / `SubControl` | 标识普通控件内部子元素和复杂控件内部子控件。 | `SubControls` 是 flags；不要用 `==` 代替 `testFlag()` 判断包含关系。 |
| 类型 | `PixelMetric` / `StyleHint` / `ContentsType` | 分别标识像素指标、行为提示和内容尺寸计算类别。 | 这些枚举值决定 style 接口正在回答哪一个平台相关问题。 |
| 构造 | `QStyle()` | 创建样式基类对象。 | `QStyle` 是抽象接口，实际使用通常是 `QCommonStyle`、平台 style 或自定义派生类。 |
| 析构 | `~QStyle()` | 销毁样式对象。 | style 常被应用或 widget 托管；不要删除仍被使用的共享 style。 |
| 基础绘制 | `drawPrimitive(...)` | 绘制最基础的视觉元素，例如边框、箭头、焦点框和面板。 | `PrimitiveElement`、option 和 rect 的语义必须一致；通常由自定义 style 或控件调用。 |
| 标准绘制 | `drawControl(...)` | 绘制标准控件的一部分，例如按钮、菜单项、tab 或进度条。 | 传入的 option 往往是具体派生类，不能无条件强转。 |
| 复杂绘制 | `drawComplexControl(...)` | 绘制由多个子控件组成的 combo box、slider、spin box、title bar 等。 | 子控件集合由 `QStyleOptionComplex::subControls` 描述，几何应交给 style 计算。 |
| 命中测试 | `hitTestComplexControl(...)` | 判断一个位置命中了复杂控件的哪个子控件。 | position 的坐标语义按接口约定处理，必须与 `subControlRect()` 使用同一套布局规则。 |
| 子控件几何 | `subControlRect(...)` | 计算复杂控件某个子控件的矩形。 | 不要手工假设箭头、按钮或滑块固定占据最后若干像素，要考虑 style、DPI 和 RTL。 |
| 子元素几何 | `subElementRect(...)` | 计算普通控件内部标准元素的矩形。 | 用于按钮标签、编辑框内容区、tab frame 等非 complex control 区域。 |
| 内容尺寸 | `sizeFromContents(...)` | 根据内容大小、option 和 style 规则计算控件推荐尺寸。 | 返回值会影响布局；修改 style 时要避免文字、图标被裁切。 |
| 像素指标 | `pixelMetric(...)` | 查询边框宽度、滚动条宽度、按钮间距等像素级参数。 | 跨平台 style 可能返回不同值，业务代码不要把它们硬编码成常数。 |
| 行为提示 | `styleHint(...)` | 查询双击间隔、动画、拖动、快捷键等风格行为偏好。 | 它描述的是行为而不是几何尺寸，通常还要读取 `QStyleHintReturn` 扩展结果。 |
| 标准图标 | `standardIcon(...)` | 获取平台风格提供的标准 `QIcon`。 | 适合关闭、文件夹、箭头等通用语义；不要把它当成业务图标资源库。 |
| 标准像素图 | `standardPixmap(...)` | 获取平台风格提供的标准 `QPixmap`。 | 是更低层的像素图接口；高 DPI 场景要注意设备像素比。 |
| 状态图标 | `generatedIconPixmap(...)` | 根据图标模式生成禁用、激活或选中状态的像素图。 | 自定义 style 时要保留透明度、设备像素比和状态语义。 |
| 文本区域 | `itemTextRect(...)` | 计算一段文字在给定矩形和对齐方式下的实际区域。 | 使用传入的 `QFontMetrics`，不要另用应用默认字体猜尺寸。 |
| 图片区域 | `itemPixmapRect(...)` | 计算像素图在给定矩形中的对齐区域。 | 适合和 `drawItemPixmap()` 的绘制结果保持一致。 |
| 布局间距 | `layoutSpacing(...)` | 查询两种控件类型之间在指定方向上的推荐间距。 | 负值可能表示没有特定建议；实际布局还会结合 layout、style 和平台规则。 |
| 组合间距 | `combinedLayoutSpacing(...)` | 计算两组控件类型之间的综合间距。 | 适合布局系统在两侧存在多个候选控件类型时使用。 |
| 样式代理 | `proxy()` | 返回当前 style 链中应当被调用的代理 style。 | 自定义 style 中优先通过 `proxy()` 保持代理链，而不是直接强转某个具体实现。 |

### 6.1 静态辅助函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| RTL 几何 | `visualRect(Qt::LayoutDirection, const QRect &, const QRect &)` | 把逻辑矩形转换成当前布局方向下的视觉矩形。 | 自定义绘制时不要固定把逻辑左当成屏幕左，RTL 下必须经过它转换。 |
| RTL 坐标 | `visualPos(Qt::LayoutDirection, const QRect &, const QPoint &)` | 把逻辑坐标转换为视觉坐标。 | 适合处理按钮、图标和文字的方向镜像。 |
| 对齐 | `alignedRect(Qt::LayoutDirection, Qt::Alignment, const QSize &, const QRect &)` | 在给定矩形中按对齐方式放置指定尺寸。 | 同时考虑布局方向和对齐 flags；比手工算 x/y 更可靠。 |
| 滑块换算 | `sliderPositionFromValue(int min, int max, int val, int space, bool upsideDown)` | 把滑块值换算成可绘制空间中的位置。 | `space` 是可用轨道空间，不是整个控件宽度；反向方向要正确传 `upsideDown`。 |
| 滑块换算 | `sliderValueFromPosition(int min, int max, int pos, int space, bool upsideDown)` | 把滑块位置换算回逻辑值。 | 与前一个函数成对使用，注意整数舍入和方向反转。 |

### 一句话总结

`QStyle` 就是 Qt UI 外观规则的接口层：控件怎么画、怎么摆、用多大、间距多少，都要问它。
