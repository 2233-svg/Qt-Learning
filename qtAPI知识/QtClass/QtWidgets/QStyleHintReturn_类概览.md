# Qt QStyleHintReturn 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleHintReturn>`  
> 所属模块：`Qt6::Widgets`  
> 继承：无  
> 定位：QStyle::styleHint() 的扩展返回数据

## 1. QStyleHintReturn 解决什么问题

`QStyle::styleHint()` 通常返回一个整数，但有些样式提示不止需要一个整数。例如，样式可能需要返回一个区域掩码，或者返回一个 `QVariant` 承载的额外值。这时就需要通过 `QStyleHintReturn` 传出附加数据。

`QStyleHintReturn` 是这个附加数据的基类，`QStyleHintReturnMask` 和 `QStyleHintReturnVariant` 是两个常用派生类型。

```text
QStyle::styleHint(..., QStyleHintReturn *returnData)
                                  ▲
                                  │
                    QStyleHintReturn
                       ├─ QStyleHintReturnMask
                       └─ QStyleHintReturnVariant
```

它不是业务层的结果对象，而是样式实现和 Qt 控件之间约定好的“小型数据包”。

## 2. 最小可用代码

### 2.1 样式实现里读取专用返回类型

```cpp
int MyStyle::styleHint(StyleHint hint,
                       const QStyleOption *option,
                       const QWidget *widget,
                       QStyleHintReturn *returnData) const
{
    if (hint == SH_RubberBand_Mask && returnData) {
        if (auto *mask = qstyleoption_cast<QStyleHintReturnMask *>(returnData))
            mask->region = QRegion(QRect(0, 0, 100, 20));
    }

    return QCommonStyle::styleHint(hint, option, widget, returnData);
}
```

### 2.2 通过版本和类型安全转换

```cpp
QStyleHintReturnMask mask;
QStyleHintReturn *base = &mask;

if (auto *typed = qstyleoption_cast<QStyleHintReturnMask *>(base)) {
    // typed->region 可安全使用
}
```

不要直接把基类指针强转成某个派生类；`qstyleoption_cast()` 会同时检查 `version` 和 `type`。

## 3. 核心使用模型

### 3.1 `version` 和 `type` 是运行时识别信息

基类包含两个公开字段：

- `version`：返回结构的版本；
- `type`：返回结构的种类。

Qt 用它们判断当前指针是否真的指向可兼容的派生返回类型。

### 3.2 `SH_Default` 允许默认类型

基类默认构造时的 type 是 `SH_Default`。派生返回类会使用自己的类型编号：

- `SH_Mask`；
- `SH_Variant`。

这套设计让样式可以识别传入的数据包，而不用依赖 C++ RTTI。

### 3.3 `qstyleoption_cast()` 是推荐入口

`qstyleoption_cast()` 和 `QStyleOption` 的转换辅助函数采用同一套思路：先检查版本和类型，成功后再返回目标指针；不匹配则返回 `nullptr`。

## 4. 适合用在哪里

- 自定义 `QStyle` 的 `styleHint()`；
- 为 `QRubberBand`、`QFocusFrame` 等控件返回特殊 mask；
- 样式插件需要向 Qt 传递额外的 QVariant 数据；
- 编写兼容不同 Qt 样式版本的返回结构。

普通业务控件一般不需要直接创建它。只有做样式扩展或研究 Qt 样式系统时才会经常接触。

## 5. 常见误区

### 5.1 把它当成 styleHint 的普通返回值

`styleHint()` 的整数返回值和 `QStyleHintReturn` 指针是两条并行通道，后者只承载附加数据。

### 5.2 直接 static_cast

传入的指针类型可能不是你以为的派生类，应使用 `qstyleoption_cast()` 检查。

### 5.3 忽略 nullptr

`returnData` 本来就可能为空，样式实现不能无条件解引用。

### 5.4 修改 version/type

这两个字段是类型识别契约的一部分，通常应使用 Qt 派生类构造函数设置的值，不要随意改动。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `HintReturnType` | 定义附加返回数据的类型编号。 | `SH_Default`、`SH_Mask`、`SH_Variant`。 |
| 类型 | `StyleOptionType` | 定义当前基类返回结构的类型编号。 | 基类默认为 `SH_Default`。 |
| 类型 | `StyleOptionVersion` | 定义当前返回结构的版本号。 | 用于 `qstyleoption_cast()` 兼容性检查。 |
| 构造 | `QStyleHintReturn(int version = QStyleOption::Version, int type = SH_Default)` | 创建一个样式提示返回数据基类对象。 | 一般由派生返回类或样式代码使用。 |
| 析构 | `~QStyleHintReturn()` | 销毁返回数据对象。 | 不负责释放外部样式资源。 |
| 字段 | `version` | 保存返回数据结构的版本号。 | 不要随意改动。 |
| 字段 | `type` | 保存返回数据结构的类型编号。 | 用于识别具体返回类型。 |
| 非成员 | `qstyleoption_cast<T>(const QStyleHintReturn *)` | 把基类返回指针安全转换成兼容的派生类型。 | 类型或版本不匹配时返回 `nullptr`。 |
| 非成员 | `qstyleoption_cast<T>(QStyleHintReturn *)` | 对可修改的返回数据执行安全类型转换。 | 转换成功后才能写入派生字段。 |

## 7. 一句话总结

`QStyleHintReturn` 是 `QStyle::styleHint()` 的扩展返回数据基类，真正的关键不是构造它，而是用 version/type 和 `qstyleoption_cast()` 安全识别它。
