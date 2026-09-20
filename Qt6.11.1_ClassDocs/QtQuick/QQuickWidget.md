# QQuickWidget
> Qt 6.11.1 · Qt Quick · 来自 `QQuickWidget`

## 作用定位
`QQuickWidget` 把一个 Qt Quick 场景显示为 `QWidget`。它让老的 Widgets 应用能在表单、布局、dock 或 `QMainWindow` 中局部使用 QML，而不必把整个应用改成独立 `QQuickWindow`。

## 类说明
它通过离屏渲染后再交给 Widgets 合成，因此集成成本低，却不适合把每一帧性能都压到极限的场景。全屏动画、复杂 3D 或大量实时特效应优先采用独立 `QQuickView`/`QQuickWindow`。

```cmake
find_package(Qt6 REQUIRED COMPONENTS QuickWidgets)
target_link_libraries(app PRIVATE Qt6::QuickWidgets)
```

## API 速查
| API | 是做什么的 |
|---|---|
| `setSource()` | 加载 QML 文件。|
| `loadFromModule()` | 从 QML 模块加载根类型。|
| `status()` / `errors()` | 检查加载进度与失败原因。|
| `rootObject()` | 取得 QML 根项。|
| `quickWindow()` | 取得内部 `QQuickWindow`，用于观察场景图状态。|
| `setResizeMode()` | 选择由 QML 根项或 QWidget 自身控制尺寸。|
| `setInitialProperties()` | 在根对象创建前注入属性。|
| `setClearColor()` | 设置离屏缓冲清屏色。|
| `setFormat()` | 请求图形表面格式；应在加载内容前设置。|
| `grabFramebuffer()` | 读取当前离屏帧为 `QImage`。|
| `sceneGraphError()` | 报告图形初始化、上下文等 Scene Graph 错误。|

## 使用场景
```cpp
auto *quick = new QQuickWidget(this);
quick->setResizeMode(QQuickWidget::SizeRootObjectToView);
quick->setInitialProperties({{"themeName", "dark"}});
quick->setSource(QUrl(u"qrc:/qml/Inspector.qml"_qs));
layout()->addWidget(quick);
```

它尤其适合“Widgets 负责主框架和成熟控件，QML 负责某块动态可视化或动画面板”的渐进式迁移。

## 常见坑与经验
- `QQuickWidget` 会引入额外离屏目标和合成步骤；频繁 `grabFramebuffer()` 还会增加读回开销。
- 不要同时让 QWidget layout 和 QML 根项互相抢尺寸。通常选 `SizeRootObjectToView`，由 layout 决定外层尺寸。
- `quickWindow()` 是内部窗口，不应调用 `show()` 或按独立窗口方式管理它。
- `setFormat()`、图形后端和共享上下文问题应在创建/加载 QML 前处理；运行中切换不可依赖。

## 知识点覆盖
Widgets 与 Qt Quick 混合、离屏渲染、布局尺寸协商、QML 装载、图形表面格式、性能取舍、渐进式界面迁移。
