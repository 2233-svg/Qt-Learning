# QFontVariableAxis

> Qt 6.11.1 · Qt GUI · 来自 `QFontVariableAxis`

## 1. 先建立直觉

可变字体把“常规、半粗、粗体、窄体、斜体”等多个实例收进同一个字体文件，并以连续数值的轴来描述变化。`QFontVariableAxis` 是其中一根轴的**说明卡**：它有四字符 tag、可读名称、最小值、默认值和最大值。

它不会改变字体。真正选择 `wght=550` 或 `wdth=85` 的操作在 `QFont::setVariableAxis()`；`QFontVariableAxis` 的价值是让程序知道某个匹配字体有哪些可用控制项，以及滑块可以安全取到哪里。

## 2. 类说明

- 头文件：`#include <QFontVariableAxis>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：值类型，通常由 `QFontInfo::variableAxes()` 获得。
- tag 类型为 `QFont::Tag`，表示恰好四个 Latin-1 字符；标准 tag 常见为 `wght`、`wdth`、`ital`、`opsz`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `tag()` / `setTag()` | 读取或设置四字符轴标识 |
| `name()` / `setName()` | 读取或设置人类可读的轴名称 |
| `minimumValue()` / `setMinimumValue()` | 读取或设置描述中的最小值 |
| `defaultValue()` / `setDefaultValue()` | 读取或设置字体未指定该轴时的默认值 |
| `maximumValue()` / `setMaximumValue()` | 读取或设置描述中的最大值 |
| 拷贝、赋值、`swap()` | 复制或交换轴描述；不影响任何 `QFont` |
| `QFontInfo::variableAxes()` | 查询已匹配字体实际公开的轴列表 |
| `QFont::setVariableAxis(tag, value)` | 依据轴描述把一个值应用到字体请求 |

## 4. 关键用法

### 根据字体能力动态生成控制项

```cpp
QFontInfo info(currentFont);
for (const QFontVariableAxis &axis : info.variableAxes()) {
    qDebug() << axis.tag()
             << axis.name()
             << axis.minimumValue()
             << axis.defaultValue()
             << axis.maximumValue();
}
```

不要假定所有可变字体都有 `wght`。有的只提供光学尺寸，有的有厂商自定义轴；界面应根据查询结果生成，而非硬编码一套滑块。

### 将滑块值安全地应用到 QFont

```cpp
const QFontVariableAxis weightAxis = findAxis("wght");
const float value = std::clamp<float>(sliderValue,
                                      weightAxis.minimumValue(),
                                      weightAxis.maximumValue());

QFont font = baseFont;
font.setVariableAxis(weightAxis.tag(), value);
label->setFont(font);
```

`setVariableAxis()` 是请求，不承诺系统一定能提供该效果。应用后若需确认实际匹配字体，重新通过 `QFontInfo` 检查。

### 标准 tag 的语义不是统一的值域

```cpp
font.setVariableAxis("wght", 550.0f); // 常见是 100..900，但必须查询
font.setVariableAxis("wdth", 87.5f);  // 常见以百分比表达，但仍必须查询
font.setVariableAxis("ital", 1.0f);   // 常见为 0..1，不应凭猜测使用
```

tag 的语义有行业约定，不代表所有字体都采用同一范围、同一插值方式或同一视觉结果。范围永远以该字体返回的轴描述为准。

## 5. 使用场景

- 排版工具、海报工具、字体预览器中的粗细、宽度和光学尺寸调节。
- 代码或设计系统中介于“Regular”和“Bold”之间的连续字重。
- 自适应字号时，让 `opsz` 随视觉尺寸变化的高级排版。
- 诊断某台机器的字体后端是否暴露了可变轴能力。

## 6. 常见坑与经验

- **描述对象不会修改字体。** `setMinimumValue()`、`setName()` 等只改当前 `QFontVariableAxis` 值对象，通常仅适合保存或测试自定义描述。
- **不要把 tag 当任意字符串。** 它严格是四字符标识；Qt 的 `QFont::Tag` 设计就是为了避免 `"weight"` 这类拼写在运行时悄悄失效。
- **不要把范围写死。** 即便标准 `wght` 通常接近 100 到 900，实际字体范围仍可能不同。
- **变量轴与 `setWeight()` 的优先级要设计清楚。** 若显式设置了 `wght`，它比离散 `QFont::Weight` 更适合表达连续值；不要让两个控件互相覆盖却不更新 UI。
- **平台支持会影响结果。** 字体后端、已安装的字体版本和 Windows 可选 GDI 后端都可能限制可变轴支持。
- **轴名称不是稳定标识。** `name()` 可本地化、缺失或由字体提供；持久化时用 tag，展示时用 name。

## 7. 知识点覆盖

OpenType 可变字体、四字符 tag、标准与自定义轴、字体能力发现、范围校验、连续字重、设备/平台差异、字体请求与实际匹配。
