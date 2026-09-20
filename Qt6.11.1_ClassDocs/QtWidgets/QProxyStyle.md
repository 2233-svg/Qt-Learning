# QProxyStyle

> Qt 6.11.1 · Qt Widgets · 来自 `QProxyStyle`

## 1. 先建立直觉

`QProxyStyle` 是包在另一个 style 外面的代理。它让你只改少量指标、绘制或行为，其余全部转发给原来的平台 style。

这是自定义 Widgets 外观时最常用、也最稳的方式：保留系统风格大部分细节，只在必要处动刀。

## 2. 类说明

`QProxyStyle` 继承自 `QCommonStyle`，内部持有 base style。你可以重写 `pixelMetric()`、`styleHint()`、`drawControl()` 等函数，未处理的部分交给基类/基础 style。

它适合做“更紧凑的间距”“统一图标尺寸”“某个控件特殊绘制”“禁用某种平台行为”。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QProxyStyle()` | 创建使用默认基础 style 的代理。 |
| `QProxyStyle(QStyle *)` | 包装指定基础 style。 |
| `QProxyStyle(QString key)` | 按 style key 创建并包装基础 style。 |
| `setBaseStyle(QStyle *)` / `baseStyle()` | 设置或读取被代理的 style。 |
| `drawPrimitive/drawControl/drawComplexControl` | 可按需覆盖局部绘制。 |
| `pixelMetric()` | 常用于调整边距、图标尺寸、框宽。 |
| `styleHint()` | 常用于调整行为提示。 |
| `sizeFromContents()` | 调整控件尺寸计算。 |
| `standardIcon()` | 替换标准图标。 |
| `polish()` / `unpolish()` | 应用或撤销代理时处理初始化。 |

## 4. 关键用法

```cpp
class CompactProxyStyle : public QProxyStyle {
public:
    int pixelMetric(PixelMetric metric, const QStyleOption *option,
                    const QWidget *widget) const override
    {
        if (metric == PM_ButtonMargin)
            return 4;
        return QProxyStyle::pixelMetric(metric, option, widget);
    }
};

qApp->setStyle(new CompactProxyStyle);
```

包装指定平台 style：

```cpp
qApp->setStyle(new CompactProxyStyle(QStyleFactory::create("Fusion")));
```

## 5. 使用场景

适合局部微调系统风格、统一应用密度、替换标准图标、修正某个平台控件细节、给现有 style 加一点产品特征。

如果要彻底重画所有控件，`QCommonStyle` 或完整自定义 style 更合适，但成本也高得多。

## 6. 常见坑与经验

重写函数时要回退到 `QProxyStyle::...`，不要直接跳到某个固定 style，否则代理链可能被破坏。

代理 style 影响范围可能是全应用。只想影响某个控件时，可以给局部 widget 设置 style，但要注意所有权和一致性。

样式表会和 proxy style 交互。出现“我重写了但没生效”时，先检查 stylesheet 是否接管了相关控件。
