# QQuickView
> Qt 6.11.1 · Qt Quick · 来自 `QQuickView`

## 作用定位
`QQuickView` 是一个独立原生窗口，负责加载 QML 根对象并显示 Qt Quick 场景。它同时拥有 `QQuickWindow` 的渲染能力和 `QQmlEngine` 的加载能力，适合 C++ 主程序以 QML 作为整个窗口界面的桌面应用。

## 类说明
它不是嵌入 QWidget 的容器；需要把 QML 放到已有 `QMainWindow`、表单或 dock 中时，应使用 `QQuickWidget` 或 `QQuickRenderControl`。

## API 速查
| API | 是做什么的 |
|---|---|
| `setSource(url)` | 加载一个 QML 文件并实例化根对象。|
| `loadFromModule(uri, typeName)` | 从已注册 QML 模块加载类型，适合模块化部署。|
| `status()` / `statusChanged()` | 观察 `Null`、`Loading`、`Ready`、`Error` 加载状态。|
| `errors()` | 取得导入、语法或实例化失败的详细错误。|
| `rootObject()` | 获取创建后的根 `QQuickItem`。|
| `rootContext()` | 设置根上下文属性或访问 QML 上下文。|
| `engine()` | 取得该视图使用的 QML 引擎。|
| `setInitialProperties()` | 在根对象完成创建前赋初始属性。|
| `setResizeMode()` | 决定窗口跟随根项，还是根项跟随窗口。|
| `initialSize()` | 读取 QML 根项给出的初始大小。|

## 使用场景
```cpp
QQuickView view;
view.setResizeMode(QQuickView::SizeRootObjectToView);
view.setInitialProperties({{"documentId", 42}});
view.setSource(QUrl(u"qrc:/qml/Main.qml"_qs));
if (view.status() == QQuickView::Error)
    qFatal("Cannot load main QML");
view.resize(1100, 720);
view.show();
```

`setInitialProperties()` 比加载完成后 `rootObject()->setProperty()` 更适合不可变启动参数：QML 的 `Component.onCompleted` 能看到正确值，且避免先以默认值执行一次绑定。

## 常见坑与经验
- `setSource()` 后先检查 `status()` 和 `errors()`；QML 加载失败常表现为一片空窗口，真正原因在错误列表中。
- `SizeViewToRootObject` 更适用于由 QML 决定自然尺寸的小工具窗口；响应式主窗口通常选 `SizeRootObjectToView`。
- Context property 便捷但隐式依赖强。对长期维护的业务对象，优先注册 QML 类型、单例或使用明确属性传递。
- 根对象是 `QQuickItem` 才能显示；非视觉 `QObject` 可以被创建，却不会成为窗口内容。

## 知识点覆盖
QML 文件与模块加载、QML 错误诊断、根对象、上下文、初始属性、窗口与根项的尺寸协商、资源路径。
