# QQuickStyle
> Qt 6.11.1 · Qt Quick Controls · 来自 `QQuickStyle`

## 1. 先建立直觉

`QQuickStyle` 控制 Qt Quick Controls 使用哪套控件样式。它影响的是 `Button`、`TextField`、`ComboBox`、`Slider` 这类 Controls 的外观和部分行为，不是给所有 QML Item 套皮肤的全局魔法。

最重要的规则只有一条：样式要在加载任何导入 Qt Quick Controls 的 QML 之前设置。Controls 类型一旦注册和实例化，样式选择就基本定型了。

## 2. 类说明

`QQuickStyle` 是静态工具类，没有实例生命周期。它的 API 用于设置主样式、备用样式，以及查询最终采用的样式名称。

保留类说明：这些 API 来自 `QQuickStyle`，它属于 Qt Quick Controls 模块，作用范围集中在 Quick Controls 样式解析。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `setStyle(const QString &style)` | 设置主样式名称，例如 Material、Fusion、Imagine、Universal、Basic。 |
| `setFallbackStyle(const QString &style)` | 设置自定义样式缺少控件实现时回退到哪套内置样式。 |
| `name()` | 返回当前解析出的样式名称。 |

## 4. 典型流程

```cpp
int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQuickStyle::setStyle("Material");
    QQuickStyle::setFallbackStyle("Fusion");

    QQmlApplicationEngine engine;
    engine.loadFromModule("Demo", "Main");
    return app.exec();
}
```

如果项目允许命令行或环境变量配置样式，需要明确优先级。工程里常见做法是：开发/测试通过命令行切换，产品发布时在 C++ 或配置文件里固定默认样式。

## 5. 使用场景

| 场景 | 建议 |
| --- | --- |
| 桌面工具想接近 QWidget/Fusion 质感 | 使用 `Fusion`，便于跨平台保持稳定。 |
| 移动或嵌入式触控界面 | 选择 Material、Universal 或自定义 style，注意控件尺寸和触摸热区。 |
| 品牌化 Quick Controls | 自定义 style 加 `setFallbackStyle()`，只重写真正需要品牌表达的控件。 |
| 测试不同平台表现 | 在启动参数或环境变量中切换样式，避免频繁改代码。 |

## 6. 常见坑与经验

不要在 QML 已经加载后再调用 `setStyle()` 期待现有控件重绘成另一套样式。运行时主题色可以用 palette、附加属性或自定义样式属性处理；“换整套 style”通常是启动时决策。

`setFallbackStyle()` 主要服务自定义样式：当你的 style 目录里没有实现某个 Control 时，Qt 可以从备用样式拿默认实现。备用样式最好选择 Qt 自带样式，避免 fallback 链条复杂到难以定位。

`name()` 查询的是当前样式解析结果。太早调用时，命令行参数、环境变量、配置文件和 C++ 设置之间的最终结果可能还没完全体现；调试时最好在应用和 QML 初始化路径固定后观察。

样式不负责你的自定义 `Rectangle`、`Item`、`Canvas` 外观。那些元素没有 Controls 的 style 查找机制，需要你自己用主题对象、palette 或设计 token 维护一致性。

## 7. 知识点覆盖

- Qt Quick Controls 样式选择时机。
- 内置样式、自定义样式、fallback style 的职责。
- C++ API、环境变量、命令行参数之间的配置边界。
- Controls 样式与普通 QML Item 外观的区别。
- 启动期决策和运行时主题切换的不同设计。
