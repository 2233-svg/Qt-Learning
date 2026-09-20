# QStyleHintReturnVariant

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleHintReturnVariant`

## 1. 先建立直觉

`QStyleHintReturnVariant` 是 `QStyleHintReturn` 的派生类，用 `QVariant` 承载 style hint 的额外返回值。

当某些 style hint 无法只用一个整数表达时，可以用它返回字符串、尺寸、颜色或其他 QVariant 支持的数据。

## 2. 类说明

`QStyleHintReturnVariant` 有一个公开成员 `variant`。调用方把对象传给 `QStyle::styleHint()`，style 按约定填充它。

它是扩展通道，不是所有 style hint 都支持。读它之前要知道目标 hint 的语义。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStyleHintReturnVariant()` | 创建 variant 返回对象。 |
| `variant` | 保存 style 返回的 `QVariant`。 |
| `QStyleHintReturn::type` | 标识这是 variant 类型返回。 |
| `QStyle::styleHint()` | 填充该对象的入口。 |

## 4. 关键用法

```cpp
QStyleHintReturnVariant ret;
style()->styleHint(hint, option, widget, &ret);

if (ret.variant.isValid())
    useStyleValue(ret.variant);
```

自定义 style 中：

```cpp
if (auto *v = qstyleoption_cast<QStyleHintReturnVariant *>(returnData))
    v->variant = QColor(Qt::red);
```

## 5. 使用场景

适合自定义 style 和高级控件通信，让 style hint 携带比 int 更丰富的数据。

普通应用设置颜色、尺寸、图标时，通常有更直接的 API，不需要绕 style hint。

## 6. 常见坑与经验

`QVariant` 灵活，但也容易让协议不清楚。自定义 hint 要明确返回类型和默认值。

使用前检查 `isValid()`，并按预期类型转换。

不要把大量业务配置塞进 style hint。style 负责外观和行为提示，不应变成业务参数仓库。
