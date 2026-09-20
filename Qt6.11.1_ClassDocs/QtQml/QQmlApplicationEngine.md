# QQmlApplicationEngine
> Qt 6.11.1 · Qt QML · 来自 `QQmlApplicationEngine`

## 作用定位

`QQmlApplicationEngine` 是最常用的 QML 应用入口。它继承 `QQmlEngine`，封装了“加载一个主 QML 文件或模块类型、创建根对象、发出创建成功/失败信号”的流程。

它适合应用级启动；如果你要在运行期反复创建某个组件实例，更适合用 `QQmlComponent`。

## 类说明

- 头文件：`#include <QQmlApplicationEngine>`
- CMake：链接 `Qt6::Qml`
- 继承：`QQmlEngine`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 可空构造，也可直接用文件路径、URL 或模块 URI/typeName 加载入口。 |
| `load(filePath)` / `load(url)` | 加载主 QML 文件并创建根对象。 |
| `loadFromModule(uri, typeName)` | Qt 6.5 起从 QML 模块加载类型作为入口。 |
| `loadData(data, url)` | 从内存数据加载 QML，`url` 用于相对路径和错误定位。 |
| `setInitialProperties()` | 创建根对象前设置初始属性。 |
| `setExtraFileSelectors()` | Qt 6.0 起增加文件选择器，配合平台/主题等变体资源。 |
| `rootObjects()` | 返回已创建的根对象列表。 |
| `objectCreated(object, url)` | 根对象创建完成时发出；失败时 object 为 null。 |
| `objectCreationFailed(url)` | Qt 6.4 起根对象创建失败时发出。 |

## 典型启动

```cpp
QQmlApplicationEngine engine;
engine.setInitialProperties({{"backend", QVariant::fromValue(backend)}});

QObject::connect(&engine, &QQmlApplicationEngine::objectCreationFailed,
                 &app, [] { QCoreApplication::exit(-1); },
                 Qt::QueuedConnection);

engine.loadFromModule("MyApp", "Main");
```

## 使用场景

- Qt Quick/QML 应用主入口。
- 从资源文件或模块类型加载 `Main.qml`。
- 启动时给根对象注入少量初始属性。
- 监听 QML 创建失败并决定应用退出。

## 常见坑与经验

- `setInitialProperties()` 必须在 `load()` 前调用；加载后它不会 retroactively 改根对象。
- `rootObjects()` 可能为空，要连接 `objectCreationFailed()` 或检查 `objectCreated(nullptr, url)`。
- 注入大型全局对象时，优先考虑注册单例或 context property，初始属性更适合根对象自己的必需属性。
- `loadData()` 的 URL 不只是装饰；没有正确 URL，相对 import 和错误行列定位会变差。
- `QQmlApplicationEngine` 不负责创建 `QGuiApplication`，应用对象仍要自己先建好。

## 知识点覆盖

- QML 应用入口加载
- 根对象创建与失败处理
- 模块化入口 `loadFromModule`
- 初始属性和文件选择器
- 与 `QQmlComponent` 的边界
