# Qt QLCDNumber 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLCDNumber>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QFrame -> QLCDNumber`  
> 定位：数字显示控件

## 1. QLCDNumber 解决什么问题

`QLCDNumber` 是一个七段式数字显示控件。它把数字或字符串以“LCD 数码管”的风格显示出来，常用于计数器、仪表盘、状态面板、实验数据读数和调试界面。

它解决的不是“随便显示一段文本”，而是“把数值以很醒目的数字面板形式呈现”。

```text
QFrame
  └─ QLCDNumber
```

它适合：

- 计数器；
- 电子仪表风格显示；
- 数值状态面板；
- 需要突出读数的场合。

它不适合长文本，也不适合复杂排版。它本质上是一个数字显示器，不是标签控件。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 显示一个整数

```cpp
#include <QApplication>
#include <QLCDNumber>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QLCDNumber lcd;
    lcd.display(12345);
    lcd.resize(180, 80);
    lcd.show();

    return app.exec();
}
```

### 2.3 连接信号显示数值

```cpp
connect(sensor, &Sensor::valueChanged,
        lcd, qOverload<int>(&QLCDNumber::display));
```

`display()` 有多个重载，连接信号时要明确你要的是 `int`、`double` 还是 `QString` 版本。

## 3. 核心使用模型

### 3.1 它显示的是“数字面板”，不是普通字符串

`QLCDNumber` 负责把值映射成数码管视觉效果。你传入的值会根据当前模式、位数和小数点设置进行显示。

### 3.2 模式决定显示进制

`mode` 决定如何解释整数：

- `Hex`：十六进制；
- `Dec`：十进制；
- `Oct`：八进制；
- `Bin`：二进制。

这让它很适合显示调试值、寄存器值或编码状态。

### 3.3 位数决定显示上限

`digitCount` 决定最多显示多少位。位数不够时，就会发生溢出判断；因此它不是“想显示多少就多少”的自由文本控件。

### 3.4 溢出是显式可检查的

`checkOverflow()` 可以在显示前检查某个数是否超出当前显示能力。`overflow()` 信号则会在显示溢出时发出，方便你做提示或回退处理。

### 3.5 外观由 segmentStyle 控制

`segmentStyle` 决定数码管外观：

- `Outline`：轮廓风格；
- `Filled`：填充风格；
- `Flat`：扁平风格。

这会显著影响整体视觉感受。

## 4. 适合用在哪里

- 数字仪表盘；
- 计数器；
- 电压、电流、温度等读数面板；
- 调试界面里的寄存器显示；
- 需要数字感很强的状态展示。

如果你想展示一段普通文本，直接用 `QLabel` 更合适。

## 5. 常见误区

### 5.1 把它当成通用文本控件

它只适合数字面板风格，不适合复杂文字。

### 5.2 不检查溢出

位数不够时，显示结果可能和预期不同，尤其是二进制和十六进制模式。

### 5.3 忘记 `display()` 的重载差异

传 `int`、`double` 和 `QString`，显示结果不是同一套规则。连接信号时要选对版本。

### 5.4 以为 `smallDecimalPoint` 只是小数点样式的小修小补

它会影响小数点在数码管上的显示方式，和位数、模式一起看才准确。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QLCDNumber(QWidget *parent = nullptr)` | 创建一个默认数字显示控件。 | 适合后续手动 `display()`。 |
| 构造 | `QLCDNumber(uint numDigits, QWidget *parent = nullptr)` | 创建并指定初始显示位数。 | `numDigits` 会影响能显示多少位。 |
| 析构 | `~QLCDNumber()` | 销毁数字显示控件。 | 由父对象和对象树管理生命周期。 |
| 属性 | `digitCount : int` | 控制可显示的数字位数。 | 位数不够时要检查溢出。 |
| 属性 | `intValue : int` | 读取当前显示值的整数形式。 | 适合显示整数模式。 |
| 属性 | `mode : Mode` | 控制显示进制。 | 影响 `display(int)` 的解释方式。 |
| 属性 | `segmentStyle : SegmentStyle` | 控制数码管外观风格。 | 直接影响视觉样式。 |
| 属性 | `smallDecimalPoint : bool` | 控制小数点显示样式。 | 常用于节省空间。 |
| 属性 | `value : double` | 读取当前显示值的浮点形式。 | 适合数值显示。 |
| 类型 | `Mode` | 定义显示进制枚举。 | `Hex`、`Dec`、`Oct`、`Bin`。 |
| 类型 | `SegmentStyle` | 定义数码管样式枚举。 | `Outline`、`Filled`、`Flat`。 |
| 查询 | `digitCount() const` | 返回当前位数设置。 | 和 `setDigitCount()` 配对。 |
| 修改 | `setDigitCount(int nDigits)` | 设置可显示的数字位数。 | 位数变化会影响显示能力。 |
| 查询 | `checkOverflow(double num) const` | 检查浮点数是否超出当前可显示范围。 | 显示前预判很有用。 |
| 查询 | `checkOverflow(int num) const` | 检查整数是否超出当前可显示范围。 | 二进制/十六进制下更要注意。 |
| 查询 | `mode() const` | 返回当前显示模式。 | 与 `setMode()` 配对。 |
| 修改 | `setMode(Mode)` | 设置当前显示模式。 | 决定值按什么进制显示。 |
| 查询 | `segmentStyle() const` | 返回当前数码管样式。 | 与 `setSegmentStyle()` 配对。 |
| 修改 | `setSegmentStyle(SegmentStyle)` | 设置数码管样式。 | 控制外观风格。 |
| 查询 | `value() const` | 返回当前值的浮点形式。 | 适合数值显示。 |
| 查询 | `intValue() const` | 返回当前值的整数形式。 | 适合整数显示。 |
| 尺寸 | `sizeHint() const` | 返回推荐尺寸。 | 会受位数和样式影响。 |
| 槽 | `display(const QString &str)` | 用字符串更新显示内容。 | 适合自定义文本格式。 |
| 槽 | `display(int num)` | 用整数更新显示内容。 | 会按当前模式显示。 |
| 槽 | `display(double num)` | 用浮点数更新显示内容。 | 会按当前格式规则显示。 |
| 槽 | `setHexMode()` | 切换到十六进制模式。 | 便捷槽。 |
| 槽 | `setDecMode()` | 切换到十进制模式。 | 便捷槽。 |
| 槽 | `setOctMode()` | 切换到八进制模式。 | 便捷槽。 |
| 槽 | `setBinMode()` | 切换到二进制模式。 | 便捷槽。 |
| 槽 | `setSmallDecimalPoint(bool)` | 设置是否使用小数点节省显示空间。 | 与显示宽度有关。 |
| 信号 | `overflow()` | 当显示内容溢出时发出。 | 可用于报警或 UI 提示。 |
| 事件 | `event(QEvent *e)` | 处理控件级通用事件。 | 控件行为入口。 |
| 绘制 | `paintEvent(QPaintEvent *)` | 绘制数码管面板。 | 由框架调用。 |

## 7. 一句话总结

`QLCDNumber` 是七段式数字显示控件，最适合做仪表盘、计数器和数值面板，关键在于位数、模式、样式和溢出检查。
