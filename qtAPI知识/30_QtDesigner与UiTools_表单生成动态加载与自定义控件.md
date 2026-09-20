# Qt Designer 与 UiTools：表单生成、动态加载与自定义控件

> Qt Widgets Designer 负责编辑 `.ui` 表单，`uic` 把表单转换为 C++ 代码，`QUiLoader` 在运行时从 XML 创建控件。三者解决的是不同问题：编译期生成更快、更安全；运行时加载更灵活，但类型、资源和生命周期需要额外管理。

## 1. `.ui` 与 uic

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
qt_standard_project_setup()

qt_add_executable(editor
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
)
target_link_libraries(editor PRIVATE Qt6::Widgets)
```

启用 `AUTOUIC` 后，CMake 自动调用 `uic` 生成 `ui_mainwindow.h`。典型窗口类：

```cpp
class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit MainWindow(QWidget *parent = nullptr)
        : QMainWindow(parent), ui(new Ui::MainWindow)
    {
        ui->setupUi(this);
        connect(ui->saveButton, &QPushButton::clicked,
                this, &MainWindow::save);
    }
    ~MainWindow() override { delete ui; }
private:
    void save();
    std::unique_ptr<Ui::MainWindow> ui;
};
```

`setupUi()` 创建控件、应用属性、布局和 Designer 中配置的信号槽连接。业务逻辑不要写入生成的头文件；重新运行 uic 会覆盖它。

## 2. objectName 与运行时查找

Designer 中设置的 `objectName` 会写入 UI 文件，可用于 `findChild<T*>()`：

```cpp
auto *label = window.findChild<QLabel *>(QStringLiteral("statusLabel"));
if (label)
    label->setText(tr("就绪"));
```

频繁依赖字符串查找会削弱类型安全。固定界面优先使用 `ui->member`；动态插件或通用工具才使用 `findChild`，并在找不到时输出明确错误。

## 3. Designer 中的布局和尺寸策略

表单应使用布局而不是固定坐标。常用属性：

- `sizePolicy`：控件在水平/垂直方向的伸缩意愿；
- `minimumSize`/`maximumSize`：硬约束；
- `baseSize`/`sizeIncrement`：窗口调整步长；
- `stretch`：布局空间分配权重；
- `buddy`：标签与输入控件的快捷键关系。

自定义控件应实现合理的 `sizeHint()` 和 `minimumSizeHint()`，否则 Designer 预览和运行时布局可能不一致。

## 4. QUiLoader：运行时加载表单

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets UiTools)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::UiTools)
```

```cpp
#include <QFile>
#include <QUiLoader>

QFile file(QStringLiteral(":/forms/settings.ui"));
if (!file.open(QIODevice::ReadOnly))
    return;

QUiLoader loader;
QWidget *form = loader.load(&file, parentWidget);
file.close();
if (!form) {
    qWarning() << loader.errorString();
    return;
}
form->show();
```

`load()` 从 `QIODevice` 读取 XML 并创建控件，返回的顶层 widget 通常应设置父对象。动态加载适合插件、主题或用户可替换表单，但错误要在加载阶段处理。

## 5. 自定义 QUiLoader

QUiLoader 默认只能创建已知 Qt 类型。自定义控件可以重载 `createWidget()`：

```cpp
class Loader : public QUiLoader
{
public:
    using QUiLoader::QUiLoader;

    QWidget *createWidget(const QString &className,
                          QWidget *parent = nullptr,
                          const QString &name = {}) override
    {
        if (className == QStringLiteral("ColorPreview")) {
            auto *widget = new ColorPreview(parent);
            widget->setObjectName(name);
            return widget;
        }
        return QUiLoader::createWidget(className, parent, name);
    }
};
```

自定义控件的构造函数必须接受 `QWidget *parent`，并在返回前设置 objectName。不要在 `createWidget()` 中执行依赖尚未加载属性的初始化；UI 属性会在加载过程中继续设置。

## 6. QFormBuilder 与表单保存

`QFormBuilder` 可把 QWidget 层次写回 `.ui` 描述，适合设计器工具和运行时表单编辑器。生产应用不应把用户输入直接覆盖原始模板，保存前应使用临时文件、校验 XML，并保留版本信息。

## 7. 自定义控件集成 Designer

要让自定义控件出现在 Designer 工具箱，通常实现 `QDesignerCustomWidgetInterface`，提供：

- `name()`、`group()`、`toolTip()`、`whatsThis()`；
- `includeFile()`；
- `icon()`；
- `domXml()`；
- `createWidget()`；
- `isContainer()`。

插件使用 `Q_PLUGIN_METADATA` 导出，控件类通常使用 `QDESIGNER_WIDGET_EXPORT`。如果只需要在表单中占位，可在 Designer 中使用“提升为”指定自定义类，而不必开发完整插件。

## 8. 自定义容器与扩展

多页容器可以实现 `QDesignerContainerExtension`，任务菜单可以实现 `QDesignerTaskMenuExtension`，属性面板可以实现 `QDesignerPropertySheetExtension`。这些接口只影响 Designer 编辑体验，不会自动改变运行时控件逻辑。

## 9. Designer 信号槽编辑器

Designer 可以配置信号到槽的连接，生成代码会调用 `QObject::connectSlotsByName()`，并识别 `on_objectName_signal` 命名的槽：

```cpp
void MainWindow::on_saveButton_clicked()
{
    save();
}
```

现代代码也可以在构造函数中使用函数指针连接，类型更安全。不要同时配置 Designer 自动连接和手写连接，否则一次点击可能执行两遍。

## 10. 资源和翻译

`.ui` 中的图标和图片可以来自 Qt Resource System。动态加载时，资源路径必须在加载器可见的资源系统中；部署到文件系统后不能假设 `:/` 路径会自动存在。

界面文本应使用 `tr()`/`QT_TR_NOOP` 体系并通过 Linguist 生成翻译。动态加载表单的翻译上下文取决于 UI 文件和控件类名，切换语言时需要重新翻译已创建控件。

## 11. 运行时加载与安全

不可信 `.ui` 文件可以创建大量控件、触发资源加载或占用内存。不要从用户目录无条件加载表单；限制来源、大小和允许的控件类型，必要时使用自定义 QUiLoader 白名单。

## 12. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 找不到 ui_xxx.h | AUTOUIC 未启用或 `.ui` 未列入目标 | 使用 qt_standard_project_setup 并加入源列表 |
| QUiLoader 返回 null | XML 损坏或类型未知 | 检查 errorString 和自定义 createWidget |
| Designer 预览正常，运行错位 | 缺少布局或 sizeHint 不合理 | 使用布局并实现尺寸提示 |
| 点击执行两次 | 自动连接和手写连接重复 | 保留一种连接方式 |
| 自定义控件不在工具箱 | 插件元数据或导出宏缺失 | 检查接口实现、插件路径和 ABI |
| 动态表单找不到图片 | 资源未嵌入或路径错误 | 使用 `:/` 资源并确认 qrc 配置 |

## 13. 自测题

1. `.ui`、uic 和 QUiLoader 的主要区别是什么？
2. 为什么不能直接修改 `ui_xxx.h`？
3. 自定义 QUiLoader 的 createWidget 需要注意什么？
4. Designer 自动连接可能带来什么问题？
5. 自定义控件如何快速放入现有表单而不开发插件？

### 参考答案

1. `.ui` 是描述文件，uic 在编译期生成 C++，QUiLoader 在运行时解析创建。
2. 它是生成文件，下次 uic 会覆盖修改。
3. 识别白名单类型、传入 parent、设置 objectName，并让属性在加载阶段继续生效。
4. 若又手写连接，会造成槽重复执行。
5. 使用 Designer 的“提升为”功能指定自定义类。

## 14. 小结

固定界面优先用 `.ui + uic`，获得编译期检查和更快启动；需要插件化或用户可替换表单时使用 `QUiLoader`，并通过自定义加载器控制类型和生命周期。Designer 插件解决的是编辑体验，运行时控件仍要保持独立、可测试和有合理尺寸策略。
