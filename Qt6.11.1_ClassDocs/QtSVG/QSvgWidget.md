# QSvgWidget
> Qt 6.11.1 · Qt SVG · 来自 `QSvgWidget`

## 1. 先建立直觉

`QSvgWidget` 是“拿来显示 SVG 的 QWidget”。它内部持有一个 `QSvgRenderer`，在 `paintEvent()` 里把当前 SVG 画到 widget 区域。你想在传统 QWidget 界面里快速放一个 SVG 图标、插画或动画，不想自己写绘制代码时，用它最省事。

如果你要在同一个文件中只画某个元素、做复杂缓存、或者把 SVG 画到图片/打印机/自定义画布，直接使用 `QSvgRenderer` 会更灵活。

## 2. 类说明

保留类说明：这些 API 来自 `QSvgWidget`，属于 Qt SVG 模块，用于在 QWidget 层级中显示 SVG。

`QSvgWidget` 是显示控件，不是编辑器。它关心加载和绘制；交互、选择、拖拽、元素级命中测试需要你在外层 widget 或场景里另做。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSvgWidget(QWidget *parent = nullptr)` | 创建空 SVG 控件。 |
| `QSvgWidget(const QString &file, QWidget *parent = nullptr)` | 创建控件并加载文件。 |
| `load(const QString &file)` | 从文件加载 SVG 并更新显示。 |
| `load(const QByteArray &contents)` | 从内存字节加载 SVG 并更新显示。 |
| `renderer() const` | 访问内部 `QSvgRenderer`，可连接动画信号或查询文档信息。 |
| `setOptions(QtSvg::Options)` | 设置 SVG 解析/渲染选项，需在加载前设置。 |
| `options() const` | 查询当前 SVG 选项。 |
| `sizeHint() const` | 返回建议尺寸，通常来自 SVG 默认尺寸。 |
| `paintEvent(QPaintEvent *)` | QWidget 绘制入口，由框架调用。 |

## 4. 典型流程

```cpp
auto *logo = new QSvgWidget(this);
logo->setOptions(QtSvg::Options{});
logo->load(QStringLiteral(":/art/logo.svg"));
layout->addWidget(logo);
```

如果 SVG 有动画，内部 renderer 会发出重绘请求；通常控件自身已经处理显示，但你也可以访问 renderer 做诊断：

```cpp
connect(logo->renderer(), &QSvgRenderer::repaintNeeded,
        logo, qOverload<>(&QWidget::update));
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| QWidget 界面里的 logo、空状态插画 | 一行控件即可显示矢量资源。 |
| 固定 SVG 图标面板 | 缩放时保持清晰，不需要多套位图。 |
| 轻量动画 SVG | 依靠 renderer 的动画刷新和 widget 重绘。 |
| 运行时从配置或资源加载 SVG | `load()` 可重复切换内容。 |

## 6. 常见坑与经验

`setOptions()` 必须在 `load()` 前设置。用带文件名的构造函数时，SVG 已经加载，后续设置 options 不会影响那次解析；需要 options 时请先空构造再加载。

`renderer()` 返回的是内部对象，不代表你拥有它。不要 delete，也不要在控件销毁后保存指针继续用。

`sizeHint()` 只是布局建议，不是强制尺寸。SVG 是否保持比例，最终还取决于 widget 实际大小、renderer 的比例模式和你的布局策略。

SVG 文件越复杂，重绘成本越高。大量 `QSvgWidget` 同时显示同一个复杂文件时，考虑共享 `QSvgRenderer` 的 `QGraphicsSvgItem`，或预渲染成 `QPixmap` 缓存。

## 7. 知识点覆盖

- QWidget 中显示 SVG 的最短路径。
- `QSvgWidget` 与内部 `QSvgRenderer` 的关系。
- `load()`、`sizeHint()`、`paintEvent()` 的职责。
- SVG options 的加载前设置规则。
- 布局尺寸、动画重绘和性能缓存。
