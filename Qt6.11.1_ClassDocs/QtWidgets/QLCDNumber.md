# QLCDNumber

> Qt 6.11.1 · Qt Widgets · 来自 `QLCDNumber`

## 1. 先建立直觉

`QLCDNumber` 是一个“数码管风格”的只读数字显示控件。它适合显示计数、计时、测量值、仪表盘数值、状态编号这类需要强视觉识别的数字，不适合承担普通文本标签的职责。

它的核心不是输入，而是显示：你给它一个数字或字符串，它按 LCD 段码风格绘制。和 `QLabel` 相比，它更像仪表；和 `QSpinBox` 相比，它没有编辑能力；和图表相比，它只强调当前值，不表达趋势。

## 2. 类说明

`QLCDNumber` 继承自 `QFrame`，因此可以拥有边框外观，同时提供不同进制和段码样式。它支持十进制、十六进制、八进制、二进制显示，也能显示小数点和少量字符。

设计时要先想清楚：这个数值是否需要“像设备读数一样被看见”。如果只是表单里的普通数值，用 `QLabel` 更自然；如果用户要修改数值，用 `QSpinBox` / `QDoubleSpinBox`；如果是实时读数、倒计时、分数板，`QLCDNumber` 的识别度会更好。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QLCDNumber(QWidget *)` | 创建默认位数的 LCD 显示控件。 |
| `QLCDNumber(uint, QWidget *)` | 创建指定显示位数的 LCD 控件，适合固定宽度读数。 |
| `display(int)` | 显示整数，是计数器和状态码最常用入口。 |
| `display(double)` | 显示浮点数；注意位数不足时可能溢出。 |
| `display(const QString &)` | 显示可被段码表达的字符串，例如简单编号。 |
| `value()` | 返回当前显示值的浮点形式。 |
| `intValue()` | 返回当前显示值的整数形式。 |
| `setDigitCount(int)` / `digitCount()` | 设置或读取显示位数。位数太少会触发溢出。 |
| `setMode(Mode)` / `mode()` | 设置数字进制：`Dec`、`Hex`、`Oct`、`Bin`。 |
| `setSegmentStyle(SegmentStyle)` / `segmentStyle()` | 设置段码外观：`Outline`、`Filled`、`Flat`。 |
| `setSmallDecimalPoint(bool)` | 使用较小的小数点，减少小数点占用的视觉空间。 |
| `checkOverflow(int)` / `checkOverflow(double)` | 在显示前判断位数是否足够，避免读数被截断或显示异常。 |
| `overflow()` | 当显示值超出可显示范围时发出，适合提示用户或自动扩展位数。 |

## 4. 关键用法

固定读数位数时，优先先设置 `digitCount`，再显示数值：

```cpp
auto *lcd = new QLCDNumber(6, this);
lcd->setMode(QLCDNumber::Dec);
lcd->setSegmentStyle(QLCDNumber::Filled);
lcd->display(1250);
```

如果显示值可能增长，要在更新前做溢出判断：

```cpp
if (lcd->checkOverflow(total)) {
    lcd->setDigitCount(lcd->digitCount() + 1);
}
lcd->display(total);
```

进制显示常用于调试工具、嵌入式配置面板或协议观察器：

```cpp
lcd->setMode(QLCDNumber::Hex);
lcd->display(registerValue);
```

这里的 `display(int)` 会按当前 `mode()` 解释为对应进制的可视结果，而不是把数字转成普通文本标签。

## 5. 使用场景

`QLCDNumber` 适合倒计时、秒表、计数器、仪器读数、串口/传感器面板、考试计时器、分数牌、生产线状态看板，以及需要让数字在界面上被快速扫到的地方。

不建议把它用于大段文本、带单位的复杂数值、需要复制的结果、金融金额录入或精确格式化报表。那些场景里 `QLabel` 加明确格式化字符串更可控。

## 6. 常见坑与经验

`digitCount` 是 `QLCDNumber` 的关键约束。读数显示不完整时，首先检查位数，而不是怀疑布局或字体。

LCD 段码不是通用字体。有些字符不适合显示，字符串模式只适合短标识或数字混合片段。

实时刷新时不要过度追求毫秒级重绘。对于人眼读数，合理节流通常比疯狂 `display()` 更好，也能避免界面事件循环被无意义更新占满。
