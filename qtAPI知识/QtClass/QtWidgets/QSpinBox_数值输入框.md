# Qt QSpinBox 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QSpinBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSpinBox -> QSpinBox`  
> 定位：编辑和步进整数值，也可把整数映射为离散文本的控件

## 1. QSpinBox 解决什么问题

`QSpinBox` 用于有限范围的整数：端口号、数量、百分比、行数、图标尺寸、月份序号、枚举型选项索引等。用户既能键入，也能用按钮、滚轮和键盘步进。

```text
数量： [  12 ][▲]
              [▼]
```

它比 `QSlider` 更适合精确输入，比 `QLineEdit` 更适合强制范围与步长。小数应使用 `QDoubleSpinBox`；日期时间应使用 `QDateTimeEdit`。

## 2. 值、显示文本和 cleanText

同一个 integer 会有三种相关表达：

```cpp
spin->setPrefix("宽度：");
spin->setSuffix(" px");
spin->setValue(32);
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 数值 | `value()` | 返回已经校验并提交的整数值 | 业务计算、模型同步和保存设置应读它，不要从显示文本反解析 |
| 显示文本 | `text()` | 返回当前完整显示文本，包含 prefix、suffix 和本地化格式 | 适合展示或日志；文本不一定能直接作为整数解析 |
| 显示文本 | `cleanText()` | 返回去掉前后缀和首尾空白后的显示文本 | 仍然是文本；用户正在编辑时最终提交值还受校验和 keyboard tracking 影响 |

`cleanText()` 适合显示或日志，不应替代 `value()` 做业务计算。当前用户可能正在编辑未提交文本，最终值提交、校验和 keyboard tracking 的规则由 `QAbstractSpinBox` 决定。

## 3. 范围、步长与自适应十进制步进

```cpp
spin->setRange(1, 65535);
spin->setSingleStep(1);
spin->setValue(443);
```

`setRange()` 是 `setMinimum()` 加 `setMaximum()` 的便捷写法。设置任一端点时 Qt 会维护合法范围并夹紧 value。默认范围是 0 到 99，默认 step 是 1。

`singleStep` 必须非负；设置负数不会生效。普通 `DefaultStepType` 下，箭头每次按 `singleStep` 改变值。

```cpp
spin->setStepType(QAbstractSpinBox::AdaptiveDecimalStepType);
```

自适应十进制步进会忽略当前 `singleStep`，根据数值量级选择约低一位的 10 的幂：

```text
1100 向上 -> 1200   （步长约 100）
1200 向上 -> 1300
100 向下  -> 99     （方向被特别处理，保证反向能回到起点）
99 向上   -> 100
```

它适合大范围数量的“按量级粗调”，例如缓存大小、采样数或图像尺寸；端口、月份、枚举索引等离散业务值应保持默认步进。

## 4. prefix、suffix、specialValueText 的边界

```cpp
spin->setRange(0, 1000);
spin->setPrefix("$");
spin->setSuffix(" ms");
spin->setSpecialValueText("自动");
```

- prefix 在数值前显示，例如 `$25`；
- suffix 在数值后显示，例如 `25 ms`；
- 当 value 等于 minimum 且设置了 `specialValueText` 时，只显示 `"自动"`，不显示 prefix 或 suffix。

特殊文本只是最小值的展示替代，不是额外的枚举值。上例中业务层仍需把 `value()==0` 解释为“自动”。要关闭特殊文本，设置空字符串。

## 5. 进制显示和离散文本

```cpp
spin->setDisplayIntegerBase(16);
spin->setRange(0, 255);
```

`displayIntegerBase` 默认是 10。它影响默认的整数文本转换，适合十六进制颜色通道、位掩码或调试工具。用户看到的表示法改变了，`value()` 仍是十进制整数语义。

若 prefix/suffix/进制仍不够，例如希望输入并显示 `"32 x 32"`、月份名称或离散模式文本，应同时重写：

```cpp
class IconSizeSpinBox : public QSpinBox
{
protected:
    QString textFromValue(int value) const override
    {
        return QString("%1 x %1").arg(value);
    }

    int valueFromText(const QString &text) const override
    {
        return text.section(' ', 0, 0).toInt();
    }
};
```

`textFromValue()` 只返回“裸值文本”，不要包含 prefix/suffix，也不会用于 `specialValueText`。自定义 `valueFromText()` 后通常还应一并重写 `validate()` 和必要时的 `fixup()`，否则输入过程可能接受了不该接受的中间文本。

## 6. 信号怎么选

| 信号 | 提供什么 | 使用场景 |
| --- | --- | --- |
| `valueChanged(int)` | 已提交的纯整数。 | 更新模型、配置、计算参数。 |
| `textChanged(const QString &)` | 当前显示文本，包含 prefix/suffix。 | 同步文字预览、显示层联动。 |

键盘 tracking 开启时，用户从 `6` 键入到 `600` 可能依次提交 6、60、600。昂贵操作不要直接绑定到默认 tracking 下的 `valueChanged()`；可关闭 keyboard tracking，配合 `editingFinished()` 在最终提交时处理。

## API 速查表
### 7.1 构造、整数属性和显示文本

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSpinBox(QWidget *parent = nullptr)` | 创建整数 spin box | 默认范围 `0..99`、步长 `1`、值 `0`；创建后通常设置 range、单位和初值 |
| 生命周期 | `~QSpinBox()` | 销毁整数输入控件 | 生命周期通常交给父 widget |
| 值 | `value() const` | 读取已提交整数值 | 业务计算优先用它，不要解析 `text()` 或 `cleanText()` |
| 值 | `setValue(int value)` | 设置当前整数值并夹到合法范围内 | 新值实际改变才发 `valueChanged(int)`；初始化联动可配合 `QSignalBlocker` |
| 范围 | `minimum() const` / `maximum() const` | 读取整数范围两端 | `specialValueText` 绑定的是 `minimum()`，不是额外枚举值 |
| 范围 | `setMinimum(int min)` / `setMaximum(int max)` | 分别设置最小值或最大值 | Qt 会维护合法 range，并可能调整当前 value |
| 范围 | `setRange(int minimum, int maximum)` | 一次设置整数范围 | 初始化范围时首选；端口号、数量、百分比都应先确定业务边界 |
| 步进 | `singleStep() const` / `setSingleStep(int step)` | 读取或设置普通步长 | 负数 step 无效；自适应步进时暂不生效但会被保留 |
| 步进 | `stepType() const` / `setStepType(StepType type)` | 选择默认步进或自适应十进制步进 | `AdaptiveDecimalStepType` 会按数量级步进，适合大范围粗调，不适合端口/月号等离散值 |
| 进制 | `displayIntegerBase() const` / `setDisplayIntegerBase(int base)` | 查询或设置整数的显示进制 | 默认 `10`；十六进制工具界面常用，`value()` 的整数语义不变 |
| 文本 | `prefix() const` / `setPrefix(const QString &prefix)` | 查询或设置数值前缀 | `specialValueText` 生效时不会显示 prefix |
| 文本 | `suffix() const` / `setSuffix(const QString &suffix)` | 查询或设置数值后缀 | 单位前通常自己带空格，如 `" ms"` |
| 文本 | `cleanText() const` | 返回去掉前后缀和首尾空白后的显示文本 | 适合日志或显示，不是可靠的业务整数来源 |

### 7.2 信号与自定义文本转换

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `valueChanged(int value)` | 已提交整数变化时发出 | 更新模型、配置、计算参数的首选信号 |
| 信号 | `textChanged(const QString &text)` | 显示文本变化时发出 | 参数包含 prefix/suffix，适合显示层联动，不适合业务计算 |
| 文本转换 | `textFromValue(int value) const` | 把整数转换成显示用的裸值文本 | 不要包含 prefix/suffix；`specialValueText` 生效时不走这个函数 |
| 文本转换 | `valueFromText(const QString &text) const` | 把用户输入文本转换成整数 | 自定义月份名、档位名、`32 x 32` 这类格式时重写 |
| 校验 | `validate(QString &text, int &pos) const` | 判断当前编辑文本是否合法或是否处于中间态 | 自定义 text/value 映射时通常也要重写，避免输入过程和最终解析不一致 |
| 校正 | `fixup(QString &input) const` | 在提交前尝试修正无效文本 | 应和 `validate()`、`valueFromText()` 保持同一套语义 |
| 事件 | `event(QEvent *event)` | 处理通用事件入口 | 普通使用不直接调用，派生类重写时要保留父类输入法、快捷键等行为 |

### 7.3 常用继承 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 特殊文本 | `specialValueText() const` / `setSpecialValueText(const QString &text)` | 把最小值显示成一段特殊文字 | 业务层仍通过 `value()==minimum()` 判断含义；它不是额外值 |
| 提交策略 | `keyboardTracking() const` / `setKeyboardTracking(bool enable)` | 控制键入过程中是否持续提交 value | 昂贵计算或需要整段数字输入完成后再提交时设为 `false` |
| 循环 | `wrapping() const` / `setWrapping(bool enable)` | 控制步进到端点后是否循环到另一端 | 月份、循环索引适合；数量、端口号通常不适合 |
| 按钮 | `buttonSymbols() const` / `setButtonSymbols(ButtonSymbols bs)` | 设置显示箭头、加减号或隐藏按钮 | 只影响按钮外观，不禁用键盘、滚轮和文本输入 |
| 分组 | `isGroupSeparatorShown() const` / `setGroupSeparatorShown(bool shown)` | 控制是否显示千位分隔符 | 大数更易读；解析和显示要符合当前 locale |
| 步进 | `stepUp()` / `stepDown()` | 按当前规则向上或向下步进一步 | 自定义外部按钮、快捷键或测试自动化可直接触发 |
| 步进 | `stepBy(int steps)` | 按指定步数执行步进 | 继承自 `QAbstractSpinBox`；自定义复杂步进时可在派生类重写 |
| 可步进性 | `stepEnabled() const` | 查询当前向上/向下是否可继续步进 | 派生类可重写以表达领域里的可达状态 |
| 提交信号 | `editingFinished()` | 用户按 Enter 或控件失焦完成编辑时发出 | `keyboardTracking=false` 时常在这里读取最终 `value()` |
