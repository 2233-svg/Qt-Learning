# Qt QStyleHintReturnVariant 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleHintReturnVariant>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleHintReturn -> QStyleHintReturnVariant`  
> 定位：样式提示的 QVariant 返回数据

## 1. QStyleHintReturnVariant 解决什么问题

`QStyleHintReturnVariant` 让 `QStyle::styleHint()` 可以通过附加参数返回一个 `QVariant`。当某个样式提示需要传递的值不适合固定成整数或 `QRegion` 时，它提供了一个更通用的返回槽位。

```text
QStyle::styleHint(...)
        │
        └─ QStyleHintReturnVariant::variant
```

它解决的是“样式实现需要返回一个可携带多种 Qt 元类型的数据”的问题，但它仍然属于样式系统内部协议，不应该被当成业务层的通用数据交换对象。

## 2. 最小可用代码

```cpp
int MyStyle::styleHint(StyleHint hint,
                       const QStyleOption *option,
                       const QWidget *widget,
                       QStyleHintReturn *returnData) const
{
    if (hint == SH_TextControl_FocusIndicatorTextCharFormat && returnData) {
        if (auto *result = qstyleoption_cast<QStyleHintReturnVariant *>(returnData)) {
            QTextCharFormat format;
            format.setUnderlineStyle(QTextCharFormat::SingleUnderline);
            result->variant = QVariant::fromValue(format);
        }
    }

    return QCommonStyle::styleHint(hint, option, widget, returnData);
}
```

具体可返回什么类型，取决于对应的 `StyleHint` 约定。读取方必须知道预期元类型，不能只拿到 `QVariant` 就盲目转换。

## 3. 核心使用模型

### 3.1 `variant` 是唯一数据字段

```cpp
QStyleHintReturnVariant result;
result.variant = QStringLiteral("style data");
```

它可以承载 Qt 支持的多种值类型，也可以通过 `QVariant::fromValue()` 携带注册过的自定义类型。

### 3.2 读写双方必须约定类型

写入方和读取方必须对 variant 的实际类型有共同约定：

```cpp
if (result.variant.canConvert<QTextCharFormat>()) {
    const auto format = result.variant.value<QTextCharFormat>();
}
```

否则就会出现转换失败或把值解释错的问题。

### 3.3 仍然要做安全类型转换

`styleHint()` 的参数是 `QStyleHintReturn *`。应通过 `qstyleoption_cast<QStyleHintReturnVariant *>` 验证 type/version，而不是直接强转。

## 4. 适合用在哪里

- 样式提示需要返回 `QTextCharFormat` 等复杂 Qt 值；
- 自定义样式与控件之间传递额外配置；
- 样式插件需要扩展标准整数返回之外的信息。

## 5. 常见误区

### 5.1 把它当成任意业务数据通道

它只服务于 style hint 协议，生命周期和读取方都由样式系统决定。

### 5.2 忽略元类型注册

自定义类型放进 `QVariant` 前，要确保 Qt 元对象系统知道该类型。

### 5.3 只检查 `isValid()` 不检查类型

variant 有值不代表类型正确，还要用 `canConvert()` 或比较 `metaType()`。

### 5.4 直接 static_cast

必须先用 `qstyleoption_cast()` 检查返回对象实际类型。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `StyleOptionType` | 标识这是 `SH_Variant` 类型的返回数据。 | 用于 `qstyleoption_cast()` 识别。 |
| 类型 | `StyleOptionVersion` | 标识当前 variant 返回结构的版本。 | 当前版本为 `1`。 |
| 构造 | `QStyleHintReturnVariant()` | 创建一个 variant 返回数据对象。 | 会初始化正确的 type/version。 |
| 析构 | `~QStyleHintReturnVariant()` | 销毁 variant 返回数据对象。 | `QVariant` 成员随对象释放。 |
| 数据 | `variant` | 保存样式要返回的 Qt 变体值。 | 写入方和读取方必须约定实际类型。 |
| 转换 | `qstyleoption_cast<QStyleHintReturnVariant *>(...)` | 将基类返回指针安全转换为 variant 返回类型。 | 转换失败时返回 `nullptr`。 |

## 7. 一句话总结

`QStyleHintReturnVariant` 是样式系统传递复杂附加值的返回数据包，核心是 `QVariant variant`，使用时必须同时确认 type/version 和实际元类型。
