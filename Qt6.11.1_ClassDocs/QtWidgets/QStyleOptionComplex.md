# QStyleOptionComplex

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionComplex`

## 1. 先建立直觉

`QStyleOptionComplex` 是复杂控件的 style option 基类。复杂控件由多个子控件组成，例如滚动条有箭头、滑槽、滑块；组合框有框体、箭头、编辑区域。

它在普通 `QStyleOption` 的基础上增加了“哪些子控件要画”和“当前活动的是哪个子控件”。

## 2. 类说明

`QStyleOptionComplex` 继承自 `QStyleOption`。派生类包括 `QStyleOptionSlider`、`QStyleOptionSpinBox`、`QStyleOptionComboBox` 等。

`subControls` 表示参与绘制/布局的子控件集合，`activeSubControls` 表示鼠标悬停或正在操作的子控件集合。style 据此绘制 hover、pressed 等状态。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `subControls` | 要绘制或考虑的子控件集合。 |
| `activeSubControls` | 当前活动/命中的子控件集合。 |
| `QStyle::drawComplexControl()` | 使用 complex option 绘制复杂控件。 |
| `QStyle::subControlRect()` | 查询复杂控件子控件区域。 |
| `QStyle::hitTestComplexControl()` | 判断坐标命中哪个子控件。 |
| `QStyleOptionSlider` | 滑块/滚动条 option。 |
| `QStyleOptionSpinBox` | spin box option。 |
| `QStyleOptionComboBox` | combo box option。 |

## 4. 关键用法

```cpp
QStyleOptionSlider opt;
opt.initFrom(this);
opt.subControls = QStyle::SC_SliderGroove | QStyle::SC_SliderHandle;
opt.activeSubControls = hoveredHandle ? QStyle::SC_SliderHandle : QStyle::SC_None;

QStylePainter p(this);
p.drawComplexControl(QStyle::CC_Slider, opt);
```

命中测试：

```cpp
const auto sc = style()->hitTestComplexControl(QStyle::CC_Slider, &opt, pos, this);
```

## 5. 使用场景

适合实现复杂自定义控件、style 绘制、需要按子区域处理 hover/press 的控件。

普通单一区域控件用 `QStyleOption` 或具体 control option 即可。

## 6. 常见坑与经验

`subControls` 是“有哪些部分”，`activeSubControls` 是“当前哪部分活跃”。混淆后 hover/pressed 会错位。

绘制、命中、子区域计算应使用同一份 option，否则看到的区域和点击区域会不一致。

复杂控件的状态很多。禁用、只读、RTL、倒置外观、键盘焦点都应进入 option。
