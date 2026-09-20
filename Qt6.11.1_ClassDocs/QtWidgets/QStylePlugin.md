# QStylePlugin

> Qt 6.11.1 · Qt Widgets · 来自 `QStylePlugin`

## 1. 先建立直觉

`QStylePlugin` 是给 Qt 提供自定义 widget style 的插件基类。它让你的 style 可以被 `QStyleFactory` 按 key 发现并创建，而不是直接链接进应用。

它适合框架、组件库或需要独立部署主题的产品；普通应用内部自定义一个 style，通常不需要插件化。

## 2. 类说明

`QStylePlugin` 继承自 `QObject`。你继承它并实现 `create(const QString &key)`，根据 key 返回对应 `QStyle` 实例。

插件还需要 Qt 插件元数据和正确部署路径。style 插件属于 Widgets 样式插件体系，能否被发现取决于插件目录、IID、metadata 和平台加载规则。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStylePlugin(QObject *)` | 创建 style 插件对象。 |
| `create(const QString &key)` | 根据 style key 创建 `QStyle`。子类必须实现。 |
| `QStyleFactory::keys()` | 查看插件 style 是否被发现。 |
| `QStyleFactory::create(key)` | 通过工厂创建插件提供的 style。 |
| `Q_PLUGIN_METADATA` | 声明插件元数据。 |
| `Q_INTERFACES` | 声明实现的插件接口。 |

## 4. 关键用法

```cpp
class MyStylePlugin : public QStylePlugin {
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QStyleFactoryInterface")

public:
    QStyle *create(const QString &key) override
    {
        if (key.compare("MyStyle", Qt::CaseInsensitive) == 0)
            return new MyStyle;
        return nullptr;
    }
};
```

应用侧：

```cpp
auto *style = QStyleFactory::create("MyStyle");
if (style)
    qApp->setStyle(style);
```

## 5. 使用场景

适合主题插件、企业统一控件风格、可选皮肤包、第三方 style 分发、无需重新编译主程序即可添加外观。

如果 style 只给当前应用使用，直接编译进程序更简单，调试和部署也更省心。

## 6. 常见坑与经验

插件没出现在 `QStyleFactory::keys()` 时，先查部署路径和 metadata，不要先怀疑绘制代码。

`create()` 应只对自己支持的 key 返回 style，不支持就返回 `nullptr`。

插件式 style 仍要处理所有普通 style 的责任：绘制、尺寸、状态、RTL、高 DPI 和平台差异。
