# QStyleHintReturn

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleHintReturn`

## 1. 先建立直觉

`QStyleHintReturn` 是 `QStyle::styleHint()` 的扩展返回数据容器。普通 style hint 返回一个 `int`，但有些 hint 需要额外结构化信息，就通过这个对象带回来。

它是 style 系统内部协作对象，普通应用代码很少直接使用。自定义 style 时才会关心它。

## 2. 类说明

`QStyleHintReturn` 是基类，保存 `version` 和 `type`。具体扩展由子类表达，例如 `QStyleHintReturnMask` 返回区域 mask，`QStyleHintReturnVariant` 返回 `QVariant`。

调用方把派生对象指针传给 `styleHint()`，style 根据 hint 类型填充它。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStyleHintReturn(int version, int type)` | 创建指定版本和类型的返回对象。 |
| `version` | 结构版本，用于兼容。 |
| `type` | 返回对象类型，用于区分派生数据。 |
| `HintReturnType` | 枚举不同返回对象类别。 |
| `QStyleHintReturnMask` | 用于返回 `QRegion` mask。 |
| `QStyleHintReturnVariant` | 用于返回 `QVariant` 数据。 |
| `QStyle::styleHint()` | 使用该对象的入口。 |

## 4. 关键用法

```cpp
QStyleHintReturnVariant ret;
style()->styleHint(QStyle::SH_SomeStyleHint, &option, widget, &ret);
const QVariant value = ret.variant;
```

实际代码中要确认目标 hint 是否会填充对应返回类型，否则对象可能没有业务意义。

## 5. 使用场景

适合自定义 style、查询高级 style hint、实现平台相关控件行为。

普通控件开发更多使用 `QStyleOption` 和 `QStyle` 绘制函数，不需要直接操作它。

## 6. 常见坑与经验

不要把它当万能返回值。只有特定 style hint 才会使用扩展返回对象。

传入对象类型要和 hint 期望匹配。类型不对时，style 可能忽略它。

自定义 style 中填充扩展返回值时，要保持 version/type 正确，避免调用方误读。
