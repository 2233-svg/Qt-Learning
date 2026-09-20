# Qt QStyleHintReturnMask 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleHintReturnMask>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleHintReturn -> QStyleHintReturnMask`  
> 定位：样式掩码返回数据

## 1. QStyleHintReturnMask 解决什么问题

`QStyleHintReturnMask` 用于让样式通过 `QStyle::styleHint()` 返回一个 `QRegion`。这个区域通常表示控件或装饰元素的有效形状、遮罩或需要保留的绘制区域。

它最典型的用途是配合：

- `SH_RubberBand_Mask`：返回橡皮筋选择框的遮罩；
- `SH_FocusFrame_Mask`：返回焦点框的遮罩；
- `SH_WindowFrame_Mask`：返回窗口边框的遮罩。

```text
QStyle::styleHint(...)
        │
        └─ QStyleHintReturnMask::region
```

它不是一个普通的“矩形返回值”，而是允许样式返回任意形状的区域。

## 2. 最小可用代码

```cpp
int MyStyle::styleHint(StyleHint hint,
                       const QStyleOption *option,
                       const QWidget *widget,
                       QStyleHintReturn *returnData) const
{
    if (hint == SH_RubberBand_Mask && returnData) {
        if (auto *mask = qstyleoption_cast<QStyleHintReturnMask *>(returnData)) {
            mask->region = QRegion(QRect(0, 0, 120, 30));
            return 1;
        }
    }

    return QCommonStyle::styleHint(hint, option, widget, returnData);
}
```

真正使用时，返回的 `region` 应该和对应控件的绘制坐标、尺寸及 style hint 语义保持一致。

## 3. 核心使用模型

### 3.1 `region` 是核心数据

```cpp
QStyleHintReturnMask result;
result.region = QRegion(QRect(0, 0, 100, 20));
```

`QRegion` 可以由矩形组合、复杂剪切形状或区域运算得到，比单个 `QRect` 更灵活。

### 3.2 必须通过类型转换确认返回类型

样式函数收到的是 `QStyleHintReturn *`，不能假设它一定是 `QStyleHintReturnMask *`。推荐使用：

```cpp
auto *mask = qstyleoption_cast<QStyleHintReturnMask *>(returnData);
```

### 3.3 region 的坐标系要和调用方约定一致

样式返回区域时，最容易出错的是把窗口坐标、控件坐标和设备坐标混在一起。应以具体 style hint 和对应控件的文档语义为准。

## 4. 适合用在哪里

- 自定义 `QRubberBand` 的非矩形遮罩；
- 自定义焦点框的可见区域；
- 自定义窗口或菜单的形状；
- 需要让样式支持不规则边界的控件。

## 5. 常见误区

### 5.1 直接把基类指针强转

应使用 `qstyleoption_cast()` 检查 type/version。

### 5.2 只改 region，不考虑绘制

遮罩区域和实际绘制区域不一致时，会出现点击、重绘或透明区域错位。

### 5.3 用屏幕坐标写 region

样式返回值通常不是屏幕坐标，必须确认当前 style hint 的坐标约定。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `StyleOptionType` | 标识这是 `SH_Mask` 类型的返回数据。 | 用于 `qstyleoption_cast()` 识别。 |
| 类型 | `StyleOptionVersion` | 标识当前掩码返回结构的版本。 | 当前版本为 `1`。 |
| 构造 | `QStyleHintReturnMask()` | 创建一个掩码返回数据对象。 | 会初始化正确的 type/version。 |
| 析构 | `~QStyleHintReturnMask()` | 销毁掩码返回数据对象。 | `QRegion` 成员随对象一起释放。 |
| 数据 | `region` | 保存样式要返回的区域掩码。 | 应和对应控件的坐标系、绘制区域一致。 |
| 转换 | `qstyleoption_cast<QStyleHintReturnMask *>(...)` | 将基类返回指针安全转换为掩码返回类型。 | 转换失败时返回 `nullptr`。 |

## 7. 一句话总结

`QStyleHintReturnMask` 是样式系统返回不规则区域的专用数据包，核心字段是 `QRegion region`，使用重点是类型检查和坐标系一致。
