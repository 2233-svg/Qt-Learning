# Qt QCommonStyle 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCommonStyle>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyle -> QCommonStyle`  
> 定位：样式实现底座

## 1. 先建立整体认识：它解决什么问题

`QCommonStyle` 是 Qt Widgets 的通用样式实现层。控件本身并不决定按钮边距、菜单高度、滚动条命中区、标准图标和绘制细节，这些都由 `QStyle` 体系回答。`QCommonStyle` 提供的是一套通用的默认实现，很多平台风格或自定义风格都会以它为基础。

它更像样式系统里的“公共答案模板”，而不是一个单独拿来做业务的控件类。你如果想做局部风格调整，它常常是比完全重写 `QStyle` 更现实的起点。

```text
QStyle
  └─ QCommonStyle
       └─ QProxyStyle
```

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 查询一个样式度量

```cpp
#include <QApplication>
#include <QCommonStyle>
#include <QStyle>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QCommonStyle style;
    qDebug() << style.pixelMetric(QStyle::PM_ButtonMargin);
    return 0;
}
```

### 2.3 作为派生样式的基础

```cpp
class TightStyle : public QCommonStyle
{
public:
    int pixelMetric(PixelMetric metric, const QStyleOption *opt = nullptr,
                    const QWidget *widget = nullptr) const override
    {
        if (metric == PM_ButtonMargin)
            return 4;
        return QCommonStyle::pixelMetric(metric, opt, widget);
    }
};
```

这才是它最常见的真实用途：保留大部分默认行为，只改少量规则。

## 3. 核心使用模型

### 3.1 样式是“询问-回答”系统

控件会不断向样式问：

- 这里该留多大边距；
- 这段文本应该多高；
- 这个按钮应该怎么画；
- 这个复杂控件的子区域在哪里。

`QCommonStyle` 就是这些问题的默认回答者。你重写其中某几个函数，就能改变大量控件的外观和行为。

### 3.2 先改最小粒度的函数

样式定制时通常按这个顺序：

1. 先改 `pixelMetric()`、`layoutSpacing()`，微调尺寸和间距；
2. 再改 `sizeFromContents()`，让推荐尺寸和视觉一致；
3. 再改 `drawPrimitive()`、`drawControl()`、`drawComplexControl()`；
4. 必要时补 `subElementRect()`、`subControlRect()`、`hitTestComplexControl()`。

不要一上来就把整套样式全部重写。

### 3.3 polish 和 unpolish 是安装/回收阶段

- `polish(QApplication *)`：样式安装到应用时做全局初始化；
- `polish(QWidget *)`：样式应用到控件时做局部初始化；
- `polish(QPalette &)`：顺手调整调色板；
- `unpolish(...)`：撤销之前的附加设置。

这组函数适合做样式相关初始化，不适合塞业务逻辑。

## 4. 适合用在哪里

- 给现有风格做小幅定制；
- 写企业内控软件的统一样式；
- 研究控件到底是怎么被绘制和度量的；
- 给 `QProxyStyle` 提供基础实现。

如果只想改少数控件的外观，优先考虑样式表或 `QProxyStyle`。如果要控制整套样式语义，`QCommonStyle` 才是更合适的底层入口。

## 5. 常见误区

### 5.1 把样式当布局

样式管视觉规则，不管控件层级和布局关系。

### 5.2 只改绘制，不改几何

如果改了绘制，却没同步 `pixelMetric()` 和 `sizeFromContents()`，很容易裁切或错位。

### 5.3 把样式表和样式实现混为一谈

样式表是另一套机制，和 `QStyle` 的重写不是一回事。

### 5.4 重写太多函数

越接近全量重写，越容易在 DPI、平台和控件差异上出问题。

### 5.5 忘记回调基类实现

很多函数应该“在基类结果上微调”，而不是完全替换。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCommonStyle()` | 创建一个通用样式对象。 | 常用于直接安装样式或作为派生类基础。 |
| 析构 | `~QCommonStyle()` | 销毁样式对象。 | 要理清样式对象的生命周期。 |
| 受保护构造 | `QCommonStyle(QCommonStylePrivate &dd)` | 给内部派生实现用的构造入口。 | 一般业务代码不会直接调用。 |
| 绘制 | `drawPrimitive(...)` | 画基础界面元素，如边框、箭头、面板。 | 最细粒度的绘制入口之一。 |
| 绘制 | `drawControl(...)` | 画较完整的控件部件，如按钮文本、菜单项。 | 控件级外观常改这里。 |
| 绘制 | `drawComplexControl(...)` | 画复杂控件，如滑块、组合框、滚动条。 | 常要配合子控件矩形一起改。 |
| 绘制 | `generatedIconPixmap(...)` | 根据状态生成图标变体。 | 常用于禁用态或特殊模式图标。 |
| 命中 | `hitTestComplexControl(...)` | 判断复杂控件的子区域命中结果。 | 和子控件绘制必须一致。 |
| 几何 | `subElementRect(...)` | 返回控件内部子元素矩形。 | 影响文本区、图标区等布局。 |
| 几何 | `subControlRect(...)` | 返回复杂控件某个子控件矩形。 | 影响命中和定位。 |
| 尺寸 | `sizeFromContents(...)` | 根据内容尺寸推导控件推荐尺寸。 | 改外观时很常需要同步。 |
| 度量 | `pixelMetric(...)` | 返回标准像素度量值。 | 边距、厚度、间距都可能走这里。 |
| 间距 | `layoutSpacing(...)` | 返回不同控件类型之间的推荐间距。 | 影响布局观感和平台一致性。 |
| 标准图标 | `standardIcon(...)` | 返回标准图标。 | 常用于消息框、导航和文件相关 UI。 |
| 标准像素图 | `standardPixmap(...)` | 返回标准像素图。 | 更偏底层资源接口，和 `standardIcon()` 语义相近。 |
| 样式提示 | `styleHint(...)` | 返回样式行为建议或平台偏好。 | 很多平台差异都在这里体现。 |
| 全局安装 | `polish(QApplication *)` | 样式安装到应用时初始化全局状态。 | 适合做全局调色板修正。 |
| 调色板 | `polish(QPalette &)` | 让样式调整调色板。 | 影响一批控件的基础配色。 |
| 控件安装 | `polish(QWidget *)` | 样式应用到某个控件时初始化它。 | 适合做局部修饰。 |
| 解除安装 | `unpolish(QApplication *)` | 撤销应用级初始化。 | 与 `polish(QApplication *)` 对应。 |
| 解除安装 | `unpolish(QWidget *)` | 撤销控件级初始化。 | 与 `polish(QWidget *)` 对应。 |

## 7. 一句话总结

`QCommonStyle` 是 Qt Widgets 样式系统的通用实现底座，真正要改样式的人，通常都会先从它理解起。
