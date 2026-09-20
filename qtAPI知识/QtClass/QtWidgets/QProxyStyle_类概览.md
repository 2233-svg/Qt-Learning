# Qt QProxyStyle 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QProxyStyle>`
> 所属模块：`Qt6::Widgets`
> 继承：`QCommonStyle -> QProxyStyle`
> 常见搭档：`QStyle`、`QApplication`

## 1. QProxyStyle 解决什么问题

`QProxyStyle` 是“包一层现有 style，再改其中少数规则”的工具。  
它最适合的不是从零写一套风格，而是：

- 轻微修改平台风格；
- 只改某几个 `pixelMetric` 或 `styleHint`；
- 针对某类控件修补外观；
- 给特定 widget 单独挂一个样式代理。

你可以把它看成 `QStyle` 的中间层：

```text
原始 style -> QProxyStyle -> widget
```

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QProxyStyle>
#include <QPushButton>

class MyProxyStyle : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    int pixelMetric(PixelMetric metric, const QStyleOption *option,
                    const QWidget *widget) const override
    {
        if (metric == PM_ButtonDefaultIndicator)
            return 0;
        return QProxyStyle::pixelMetric(metric, option, widget);
    }
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setStyle(new MyProxyStyle);

    QPushButton button("Button");
    button.show();
    return app.exec();
}
```

## 3. baseStyle 和代理链

```cpp
QStyle *base = proxy->baseStyle();
proxy->setBaseStyle(baseStyle);
```

`baseStyle()` 返回底层样式；如果没手动设，Qt 会用应用当前 style。

这意味着 `QProxyStyle` 不是替代品，而是一个“转发 + 改写”的层。

## 4. 最常改的接口

```cpp
drawControl(...)
drawPrimitive(...)
drawComplexControl(...)
pixelMetric(...)
styleHint(...)
sizeFromContents(...)
subControlRect(...)
subElementRect(...)
standardIcon(...)
standardPixmap(...)
generatedIconPixmap(...)
layoutSpacing(...)
```

这和 `QStyle` 一样，但 `QProxyStyle` 的写法通常是：

1. 先判断自己要不要改；
2. 不改就调用 `QProxyStyle::xxx(...)` 继续走基类；
3. 改的时候只动少量规则。

## 5. 什么时候用它

适合：

- 只想调一两个风格参数；
- 想在不重写整套 style 的前提下做局部替换；
- 想让某个 widget 用独立 style。

不适合：

- 你要重构整个 UI 规范；
- 你要完全自定义所有控件绘制。那就不是 proxy 了。

## 6. 单控件代理样式

```cpp
auto *proxy = new MyProxyStyle(QApplication::style()->name());
proxy->setParent(widget);
widget->setStyle(proxy);
```

这个模式很重要：  
如果只想让某个 widget 用代理 style，就不要把它挂到全局应用 style 上。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QProxyStyle(QStyle *style = nullptr)` | 用一个已有 `QStyle` 作为底层风格创建代理层。 | 没有显式设置时，通常会使用应用当前风格；代理不应和底层 style 形成循环。 |
| 构造 | `QProxyStyle(const QString &key)` | 按 style key 创建底层风格，再包成代理。 | key 必须是当前平台可用的风格名称；不要把显示名称和 key 混用。 |
| 析构 | `~QProxyStyle()` | 销毁代理风格。 | 代理挂到应用或 widget 后，所有权通常由 Qt 对象树处理；不要重复删除。 |
| 代理链 | `baseStyle()` / `setBaseStyle(QStyle *)` | 读取或替换实际负责绘制大部分内容的底层风格。 | 重写接口中不需要修改的分支应继续调用代理基类，让请求沿代理链转发。 |
| 绘制 | `drawPrimitive(...)` | 代理基础图元的绘制，例如面板、边框、箭头和焦点框。 | 只在目标 `PrimitiveElement` 上改写，其他元素调用 `QProxyStyle::drawPrimitive()`。 |
| 绘制 | `drawControl(...)` | 代理标准控件元素的绘制，例如按钮标签、菜单项和 tab。 | `QStyleOption` 的具体派生类型要与 element 匹配，读取时使用 `qstyleoption_cast()`。 |
| 绘制 | `drawComplexControl(...)` | 代理由多个子区域组成的复杂控件绘制。 | combo box、slider、spin box 等要同时考虑 `subControls` 和 `activeSubControls`。 |
| 绘制 | `drawItemText(...)` | 代理文本绘制，统一处理对齐、调色板、启用状态和文本角色。 | 修改文字颜色时优先尊重 palette 和 `textRole`，不要无条件写死颜色。 |
| 绘制 | `drawItemPixmap(...)` | 代理像素图在指定矩形中的对齐绘制。 | 适合统一图标对齐或缩放策略；不要破坏高 DPI pixmap 的设备像素比。 |
| 图标 | `generatedIconPixmap(...)` | 根据图标状态生成禁用、激活或选中等状态的像素图。 | 如果只想替换一个标准图标，优先重写 `standardIcon()`，不要全局改所有状态。 |
| 命中 | `hitTestComplexControl(...)` | 代理复杂控件的子控件命中测试。 | 返回的 `SubControl` 必须和对应复杂控件的 option、坐标系一致。 |
| 几何 | `itemTextRect(...)` / `itemPixmapRect(...)` | 计算文本或像素图在给定矩形中的实际绘制区域。 | 用于让绘制和尺寸计算保持一致，不要一边改绘制一边另写不一致的坐标算法。 |
| 间距 | `layoutSpacing(...)` | 代理不同控件类型之间的推荐布局间距。 | 返回负值通常表示交给 style 的默认策略；只改确实需要的控件组合。 |
| 尺寸 | `pixelMetric(...)` | 代理像素级指标，例如边框宽度、按钮默认指示器和滚动条尺寸。 | 这是最常用的局部修补入口；修改后可能影响大量控件的布局。 |
| 行为提示 | `styleHint(...)` | 代理样式行为提示，例如是否自动隐藏、是否使用动画或拖动习惯。 | 这是行为层配置，不是像素尺寸；先确认目标 hint 的平台差异。 |
| 尺寸 | `sizeFromContents(...)` | 根据内容尺寸和 style option 计算控件推荐尺寸。 | 只改变绘制外观不够时才改它，否则容易出现文字被裁切或布局跳动。 |
| 标准图标 | `standardIcon(...)` | 返回当前平台风格的标准 `QIcon`。 | 适合替换关闭、文件夹、箭头等标准图标；尽量保持禁用态和高 DPI 支持。 |
| 标准像素图 | `standardPixmap(...)` | 返回当前平台风格的标准 `QPixmap`。 | 低层接口；普通业务代码通常优先使用 `standardIcon()`。 |
| 调色板 | `standardPalette()` | 返回代理风格建议使用的标准调色板。 | 全局改变颜色影响面很大，局部 widget 主题通常更适合用 palette 或单独 style。 |
| 几何 | `subControlRect(...)` | 代理复杂控件内部某个子控件的矩形。 | 与 `drawComplexControl()` 和 `hitTestComplexControl()` 必须使用同一套几何规则。 |
| 几何 | `subElementRect(...)` | 代理普通控件内部标准子元素的矩形。 | 适合调整按钮标签、进度条内容区等，不要把 complex control 的子区混进来。 |
| 应用样式 | `polish(QWidget *)` / `unpolish(QWidget *)` | 在 widget 应用或移除该 style 时进行初始化和清理。 | 需要处理动态属性或事件过滤时使用；退出时不要访问已经销毁的 widget。 |
| 应用样式 | `polish(QApplication *)` / `unpolish(QApplication *)` | 在应用级 style 安装或卸载时进行全局初始化和清理。 | 只适合全局代理；单控件代理不要在这里改全局状态。 |
| 调色板样式 | `polish(QPalette &)` | 对传入 palette 做风格层面的调整。 | 它会修改引用对象，必须明确是否会影响应用或控件共享的 palette。 |
| 事件 | `event(QEvent *)` | 接收代理 style 自身的事件。 | 只有代理需要处理定时器、动态状态或内部事件时才重写，通常返回基类结果。 |

### 一句话总结

`QProxyStyle` 是“样式补丁层”：不重写整套 UI，只在你想改的地方插一刀，其余全交回底层 style。
