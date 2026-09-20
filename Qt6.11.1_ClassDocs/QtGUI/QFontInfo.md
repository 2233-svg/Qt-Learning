# QFontInfo

> Qt 6.11.1 · Qt GUI · 来自 `QFontInfo`

## 1. 先建立直觉

`QFont` 是“我希望使用什么字体”的请求；`QFontInfo` 是 Qt 结合当前绘制设备和系统字体库以后，“实际选中了什么字体”的结果快照。

这一区分在跨平台程序里很重要：请求 `Inter, 13pt, Bold` 不代表机器真的安装了 Inter，也不代表打印机和屏幕会选到同一张字体。`QFontInfo` 用来诊断回退、确认字号和样式是否被满足，而不是用来配置字体。

## 2. 类说明

- 头文件：`#include <QFontInfo>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：轻量值类型；构造时保存匹配结果，之后原 `QFont` 改动不会同步过来。
- 更准确的来源：在绘制中优先用 `QPainter::fontInfo()`，它反映该 painter 当前设备上的真实匹配结果。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFontInfo(font)` | 为屏幕兼容的字体请求创建匹配结果快照 |
| `QPainter::fontInfo()` | 查询当前 painter、当前设备实际使用的字体 |
| `family()` / `styleName()` | 查看最终选中的字族和样式名 |
| `exactMatch()` | 判断系统是否完全满足请求，而非发生回退或近似匹配 |
| `pointSize()` / `pointSizeF()` / `pixelSize()` | 读取最终字号表示 |
| `weight()` / `bold()` / `italic()` / `style()` | 检查最终粗细和倾斜样式 |
| `fixedPitch()` | 判断最终字体是否为等宽字体 |
| `styleHint()` | 查看匹配时采用的风格提示 |
| `variableAxes()` | Qt 6.9 起，取得最终可变字体提供的轴描述 |
| `swap()` | 常数时间交换两个结果对象 |

## 4. 关键用法

### 查清字体是否发生了回退

```cpp
QFont requested("JetBrains Mono", 11);
requested.setStyleHint(QFont::Monospace);

QFontInfo actual(requested);
qDebug() << "requested:" << requested.families();
qDebug() << "matched:" << actual.family()
         << actual.styleName()
         << actual.pointSizeF()
         << "exact:" << actual.exactMatch()
         << "fixed:" << actual.fixedPitch();
```

`exactMatch()` 为 `false` 不等于失败。它常常只表示系统选了替代字族、替代字重，或应用了字体合成；对普通 UI 这是正常现象。只有品牌字体、代码编辑器的列对齐、排版验收等场景，才应把它当作需要处理的信号。

### 查询打印或高 DPI 设备上的实际字体

```cpp
void ReportWidget::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setFont(reportFont);
    const QFontInfo info = p.fontInfo();
    p.drawText(rect(), Qt::AlignCenter, info.family());
}
```

不要用先前根据屏幕构造的 `QFontInfo` 推断打印机结果。字体匹配和点到像素的换算都依赖绘制设备；`QPainter::fontInfo()` 才与当前输出介质一致。

### 用可变轴信息建立字体选择器

```cpp
QFontInfo info(font);
for (const QFontVariableAxis &axis : info.variableAxes()) {
    qDebug() << axis.tag() << axis.name()
             << axis.minimumValue() << axis.defaultValue()
             << axis.maximumValue();
}
```

这只是“已匹配字体支持哪些轴”的查询。要设置轴值，应对 `QFont` 调用 `setVariableAxis()`。

## 5. 使用场景

- 启动时记录“指定品牌字体是否安装、实际回退到什么”。
- 在等宽编辑器、终端模拟器中验证 `fixedPitch()`，并仍用 `QFontMetrics` 验证实际列宽。
- 生成问题报告时采集系统真实使用的字族、样式与字号。
- 将字体请求交给 `QPainter` 后，检查打印预览或高 DPI 输出的匹配结果。

## 6. 常见坑与经验

- **它不是实时观察器。** `QFontInfo(font)` 建立后，`font.setBold()` 不会更新已有的 `QFontInfo`。
- **`family()` 是结果，不是偏好列表。** 多族回退由 `QFont::families()` 表达；这里返回最终被选中的那一个。
- **屏幕与打印机不一定一致。** 构造函数面向屏幕兼容字体；设备相关查询请从 painter 取。
- **“精确”不等于“视觉相同”。** `exactMatch()` 比较请求与窗口系统匹配，不能替代截图或排版测试。
- **不要据此计算文本尺寸。** 宽度、基线、裁剪范围应交给 `QFontMetrics`、`QFontMetricsF` 或 `QTextLayout`。

## 7. 知识点覆盖

字体回退、字体匹配、绘制设备差异、点与像素、等宽字体、可变字体轴、值类型快照、跨平台排版诊断。
