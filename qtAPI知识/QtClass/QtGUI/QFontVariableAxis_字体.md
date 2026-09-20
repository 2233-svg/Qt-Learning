# QFontVariableAxis

`QFontVariableAxis` 描述可变字体中的一个连续变化维度：它携带四字节标签、可选名称、最小值、最大值和默认值。它是“字体提供什么轴”的元数据，不是给字体施加样式的对象；真正设置实例化值的是 `QFont::setVariableAxis()`。

- 头文件：`#include <QFontVariableAxis>`
- 模块：`Qt6::Gui`
- 起始版本：Qt 6.9
- 类型特性：隐式共享、可复制、可重入值类型；带 `Q_GADGET` 只读属性

## 它解决的问题

传统字体把 Regular、Bold、Condensed、Italic 等变体放在多个独立 face 中。可变字体把这些变化放进同一个字体文件的一个或多个轴，轴值是浮点数。例如 `"wght"` 可能从 100 到 900，`"wdth"` 可能从 75 到 125。`QFontVariableAxis` 让程序发现每个轴的合法范围，而不是把数字猜测或写死。

```cpp
QFont font(u"Inter Variable"_s);
QFontInfo info(font);

for (const QFontVariableAxis &axis : info.variableAxes()) {
    if (axis.tag() == QFont::Tag("wght")) {
        const float weight = std::clamp(650.0f,
                                        float(axis.minimumValue()),
                                        float(axis.maximumValue()));
        font.setVariableAxis(axis.tag(), weight);
    }
}
```

## 实际场景

**字体设置面板。** 由 `QFontInfo::variableAxes()` 动态生成滑块：显示 `name()`，使用 `minimumValue()` / `maximumValue()` 约束范围，初始值取 `defaultValue()`，提交时调用 `QFont::setVariableAxis(axis.tag(), value)`。

**保存可变字体选择。** 持久化标签和用户设定值，而不是保存轴在列表中的索引；不同字体、版本或平台可能以不同顺序报告轴。

**验证输入。** 先匹配标签，再把用户值限制到该轴公布的范围。文档明确指出高于 `maximumValue()` 或低于 `minimumValue()` 的设置不受支持。

## 语义与边界

`defaultValue()` 是当 `QFont` 查询没有显式提供该轴时字体使用的默认值。它不是当前 `QFont` 的值；当前请求值由 `QFont::variableAxisValue()` 和 `isVariableAxisSet()` 查询。

`name()` 可为空，因为字体未必提供人类可读名称。`tag()` 是稳定的机器键：标准轴常见 `"wght"`、`"wdth"`、`"ital"`、`"opsz"`；自定义轴按惯例用全大写四字符标签，但标签“有效”不代表含义标准化。

本类的 setter 只修改当前这个元数据副本，**不会改变字体文件，也不会影响 `QFont` 的渲染**。从 `QFontInfo` 得到的轴通常用于读取；手动构造/编辑 `QFontVariableAxis` 更适合测试、模型或自定义元数据。

Windows 上若应用使用可选 GDI 字体后端，变量轴不受支持。即使 API 可调用，也应在目标平台和真实字体上测试实际视觉结果。

## API 速查表

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `QFontVariableAxis()` | 创建空的轴描述。 | 适合容器/后续赋值；其初始标签不应当作真实字体轴。 |
| 复制构造、移动构造、`operator=`、移动赋值、`swap()` | 复制、移动或交换轴描述。 | 值语义；不会影响对应字体或其他副本。 |
| `tag()` | 返回 `QFont::Tag` 机器标识。 | 用它传给 `QFont::setVariableAxis()`；不要依赖列表位置。 |
| `setTag(tag)` | 设置该描述的标签。 | 只改元数据副本，不改变字体。 |
| `name()` | 返回字体提供的轴名称。 | 可能为空；显示时应为标签准备备用文本。 |
| `setName(name)` | 设置轴名称。 | 只改元数据副本。 |
| `minimumValue()` | 返回轴受支持的最小值。 | 设置更小值不受支持；UI 下界以它为准。 |
| `setMinimumValue(value)` | 修改描述的最小值。 | 不会改变字体能力或裁剪实际 `QFont` 值。 |
| `maximumValue()` | 返回轴受支持的最大值。 | 设置更大值不受支持；UI 上界以它为准。 |
| `setMaximumValue(value)` | 修改描述的最大值。 | 同样只改副本。 |
| `defaultValue()` | 返回未显式设置该轴时的默认值。 | 不是当前 `QFont` 的显式设置值。 |
| `setDefaultValue(value)` | 修改描述的默认值。 | 通常无需调用，不会改变字体。 |
| `tag` 属性 | 以 `QByteArray` 暴露四字节标签。 | 属性读到的是 `tag().toString()`，C++ 设置应使用 `setTag(QFont::Tag)`。 |
| `name`、`minimumValue`、`maximumValue`、`defaultValue` 属性 | 暴露轴元数据。 | 都是 `CONSTANT` 只读属性，没有变更通知。 |

## 易错点

1. 对 `QFontVariableAxis` 调用 setter 后期待文字改变。渲染要用 `QFont::setVariableAxis()`。
2. 以 `defaultValue()` 当作当前实例的值。先看 `QFont::isVariableAxisSet()`。
3. 不查询轴范围就把 100-900 当作所有 `"wght"` 的范围。范围由字体定义。
4. 将自定义轴按标准语义解释。四字节标签合法不等于 Qt 或应用认识其含义。
