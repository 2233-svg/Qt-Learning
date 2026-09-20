# QQuickView：加载一个 QML 根对象的独立 Qt Quick 窗口

> Qt 6.11.1 | `#include <QQuickView>` | CMake: `Qt6::Quick`

`QQuickView` 是 `QQuickWindow` 的便捷子类：给它一个 QML URL 或模块内类型，它会创建 QML engine、实例化根 item，并负责将根 item 显示在自己的原生窗口中。它适合纯 Qt Quick 桌面窗口、工具窗口和小型独立 QML 程序。

它并非把 QML 嵌入 QWidget 的通用方案；需要嵌入 Widgets 布局时应评估 `QQuickWidget`，需要完整控制 QML 对象创建或图形资源时则从 `QQuickWindow`、`QQmlEngine` 和 `QQmlComponent` 组合开始。

## 常用的加载与错误处理

```cpp
QQuickView view;
view.setResizeMode(QQuickView::SizeRootObjectToView);

QObject::connect(&view, &QQuickView::statusChanged, [&view](QQuickView::Status status) {
    if (status == QQuickView::Error)
        qWarning() << view.errors();
});

view.setSource(QUrl::fromLocalFile("C:/app/qml/Main.qml"));
view.show();
```

`setSource()` 会加载并实例化 QML；即使 URL 与当前值相同，也会再次实例化组件。对于本地文件必须传入正确的完整 URL，通常使用 `QUrl::fromLocalFile()`。网络加载期间状态为 `Loading`，完成后检查 `Ready` 或 `Error`，错误细节从 `errors()` 获得。

Qt 6.7 起也可用 `loadFromModule(uri, typeName)` 或对应构造函数加载已注册 QML 模块中的类型。若该类型来自 QML 文件，`source` 会随之设置；若是 C++ 注册类型，`source` 为空。此调用会清除原 `source`，并且每次调用都会重新实例化组件。

## 窗口尺寸与根 item 尺寸

`resizeMode` 是使用中最容易反着记的地方：

- `SizeViewToRootObject` 是默认值：根 item 的尺寸驱动窗口尺寸。适合固定内容大小的对话框或工具。
- `SizeRootObjectToView`：窗口尺寸驱动根 item 尺寸。适合用户可以自由拉伸的主窗口或根 item 使用 anchors 填满视图的程序。

`initialSize()` 返回根 item 的初始尺寸；在 `SizeRootObjectToView` 下它仍保留根 item 被窗口调整前的大小。不要将它误作窗口此刻的实时大小。

## 初始属性与 C++ 入口

需要在 QML 创建前注入参数时，先 `setInitialProperties()`，再 `setSource()`：

```cpp
QQuickView view;
view.setInitialProperties({ { "projectPath", "C:/work/demo" } });
view.setSource(QUrl(u"qrc:/qt/qml/App/Main.qml"_s));
```

组件变为 `Ready` 后再设初始属性不会产生效果。加载成功后用 `rootObject()` 访问根 item，用 `rootContext()` 设置或查询 context 体系，用 `engine()` 访问所属 `QQmlEngine`。若构造时传入外部 engine，view 不拥有它；提前销毁 engine 会让 view 进入 `Error`。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickView()` | 创建自带 QML engine 的独立 Quick 窗口 | 显示前需加载内容；不等同于 Widgets 内嵌控件 |
| `QQuickView(QQmlEngine *engine, ...)` | 使用外部 QML engine | view 不拥有 engine；engine 必须晚于 view 销毁 |
| `QQuickView(source, ...)` | 创建并立刻以 URL 加载 QML | URL 必须完整正确；本地路径用 `QUrl::fromLocalFile()` |
| `QQuickView(uri, typeName, ...)` | 从注册的 QML 模块类型创建窗口内容 | Qt 6.7 起；对应 C++ 类型时 `source` 为空 |
| `setSource(url)` / `source()` | 以 URL 加载并实例化根组件 | 即便 URL 未变也会重新实例化 |
| `loadFromModule(uri, typeName)` | 从 QML 模块加载根组件 | Qt 6.7 起；清空之前的 `source`，重复调用会重建组件 |
| `status` / `statusChanged(status)` | 观察 `Null`、`Loading`、`Ready`、`Error` | `Error` 后用 `errors()` 取得诊断；不要只检查 `source` |
| `errors()` | 返回最近一次编译或创建错误 | 非 `Error` 状态时为空列表 |
| `ResizeMode::SizeViewToRootObject` | 让窗口跟随根 item 尺寸 | 默认；适合内容决定窗口大小 |
| `ResizeMode::SizeRootObjectToView` | 让根 item 跟随窗口尺寸 | 适合可拉伸窗口；根 item 应有合理布局或 anchors |
| `setInitialProperties(map)` | 设定组件构造时的初始 QML 属性 | 必须在 `setSource()` 前调用，`Ready` 后无效 |
| `rootObject()` | 取得已实例化的根 `QQuickItem` | 加载成功后才可使用；不要假定错误状态下非空 |
| `rootContext()` / `engine()` | 访问 QML context 与 engine | context 属性应在组件实例化前设置才最可预测 |
| `initialSize()` | 返回根 item 初始尺寸 | 不是窗口的实时尺寸 |
| `setContent(url, component, item)` | 直接指定已创建组件和根对象 | 高级路径；调用方需确保对象、engine 与窗口的生命期和归属一致 |
