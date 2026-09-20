# QDesignerCustomWidgetInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerCustomWidgetInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerCustomWidgetInterface` 是把一个普通 `QWidget` 子类暴露给 Qt Widgets Designer 的插件接口。你的控件即使能在代码里正常构造，也不会自动出现在 Designer 的 Widget Box；实现这个接口并导出插件后，Designer 才知道：

- 控件在 Widget Box 中叫什么、属于哪个分组、显示什么图标；
- `.ui` 代码生成时要包含哪个头文件；
- 拖到窗体时怎样创建控件实例；
- 初始属性如何用 `domXml()` 描述；
- 它是否是能容纳子 widget 的容器；
- 插件加载后是否还要注册 Designer 扩展。

它不是控件本体。通常插件类同时继承 `QObject` 和这个接口，真正的 UI 类仍然是 `MyWidget : public QWidget`。

## 最小插件骨架

```cpp
class MyWidgetPlugin : public QObject, public QDesignerCustomWidgetInterface
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QDesignerCustomWidgetInterface")
    Q_INTERFACES(QDesignerCustomWidgetInterface)

public:
    bool isContainer() const override { return false; }
    bool isInitialized() const override { return initialized; }
    QIcon icon() const override { return QIcon(":/designer/mywidget.png"); }
    QString domXml() const override;
    QString group() const override { return "My Widgets"; }
    QString includeFile() const override { return "mywidget.h"; }
    QString name() const override { return "MyWidget"; }
    QString toolTip() const override { return "A custom widget"; }
    QString whatsThis() const override { return "Shows application-specific data."; }
    QWidget *createWidget(QWidget *parent) override { return new MyWidget(parent); }

    void initialize(QDesignerFormEditorInterface *formEditor) override
    {
        if (initialized)
            return;

        // 在此注册 QExtensionFactory 等 Designer 扩展。
        initialized = true;
    }

private:
    bool initialized = false;
};
```

`Q_INTERFACES` 让 Qt 元对象系统知道插件实现了该接口，Designer 才能通过 `qobject_cast` 发现它。`Q_PLUGIN_METADATA` 用于把插件导出给 Qt 的插件系统。二者漏掉任何一个，控件通常都不会被 Designer 正确加载。

## `createWidget()` 和 `domXml()` 各做什么

`createWidget(parent)` 返回 Designer 编辑窗体上实际放置的控件实例。必须把传入的 `parent` 传给 widget 构造函数，保持 QWidget 父子关系和布局管理正确。

`domXml()` 返回描述控件初始状态的 XML。它不负责替代控件运行时的序列化，而是帮助 Designer 在拖放新控件时设置默认属性，例如对象名、默认 geometry、初始文本。控件所有可设计属性仍应通过 `Q_PROPERTY` 和元对象系统正确公开。

```cpp
QString MyWidgetPlugin::domXml() const
{
    return R"(
        <ui language="c++">
            <widget class="MyWidget" name="myWidget"/>
        </ui>
    )";
}
```

## 容器控件不要只返回 `true`

如果 `isContainer()` 返回 `true`，Designer 会把该控件视为可容纳其它 widget 的容器。但要让添加、删除、切换页面等编辑操作真正可用，还常需要实现并注册 `QDesignerContainerExtension`。只改这个布尔值并不会自动让你的自定义堆叠控件获得完整的页面编辑行为。

普通控件应返回 `false`。错误地标为容器会让 Designer 的拖放和层级编辑行为变得混乱。

## `initialize()` 的真实用途

Designer 在加载插件后调用 `initialize(formEditor)`。这里适合做一次性接入工作，例如：

- 取得 `formEditor->extensionManager()`；
- 注册 `QExtensionFactory`；
- 初始化插件级资源或状态。

它可能被重复调用，因此 `isInitialized()` 和内部标志应配套使用，避免重复注册同一个 factory。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QDesignerCustomWidgetInterface()` | 销毁自定义控件插件接口。 | 通过接口指针管理派生插件时依赖虚析构。 |
| 预留接口 | `codeTemplate() const` | 返回代码模板字符串。 | Qt Widgets Designer 当前为未来用途保留，通常无需重写。 |
| 创建控件 | `createWidget(QWidget *parent)` | 创建并返回一个实际放到 Designer 窗体上的控件实例。 | 必须使用传入的 `parent`；每次调用应创建新的 widget。 |
| 初始 XML | `domXml() const` | 返回 Designer 用于描述新控件初始属性的 XML。 | 只描述 Designer 初始状态；不要把它当作运行时配置存储。 |
| Widget Box 分组 | `group() const` | 返回控件在 Widget Box 中所属分组名。 | 纯展示分类；保持同一插件的分组命名一致。 |
| Widget Box 图标 | `icon() const` | 返回 Widget Box 中显示的图标。 | 使用插件可访问的资源路径，避免依赖开发机绝对路径。 |
| 代码生成头文件 | `includeFile() const` | 返回 `uic` 生成代码时需要包含的头文件名。 | 必须与使用该控件的项目可见头文件一致，例如 `mywidget.h`。 |
| 插件初始化 | `initialize(QDesignerFormEditorInterface *formEditor)` | 在 Designer 加载插件后进行一次性设置。 | 用它注册扩展 factory；应防止重复初始化。 |
| 容器声明 | `isContainer() const` | 告诉 Designer 该控件是否用于容纳其它 widget。 | 返回 `true` 的控件通常还应实现容器扩展。 |
| 初始化状态 | `isInitialized() const` | 返回插件是否已完成初始化。 | 与 `initialize()` 内部标志保持一致，防止重复注册扩展。 |
| 控件类名 | `name() const` | 返回自定义 widget 的 C++ 类名。 | 必须与真实 widget 类名完全一致。 |
| 简短说明 | `toolTip() const` | 返回 Widget Box 等位置可显示的短提示。 | 面向控件使用者描述用途，不是运行时 tooltip 属性。 |
| 详细说明 | `whatsThis() const` | 返回 Designer “这是什么”帮助文字。 | 提供比 `toolTip()` 更完整的使用说明。 |
| 导出宏 | `QDESIGNER_WIDGET_EXPORT` | 确保自定义 widget 的必要符号能从 Designer 插件导出。 | 平台或构建系统可能裁剪符号时尤其重要；用于 widget 类声明。 |

## 易错点

1. 插件接口类和 widget 类不是同一个类。插件负责向 Designer 描述和创建控件，widget 负责实际界面行为。
2. `name()` 必须是控件真实 C++ 类名，不能随意写显示标题。
3. `includeFile()` 错误会让 `.ui` 的 `uic` 代码生成后编译失败。
4. `isContainer()` 返回 `true` 不会自动补齐页面管理能力；复杂容器还要提供 `QDesignerContainerExtension`。
5. `initialize()` 里的扩展注册必须只做一次。

### 一句话总结

`QDesignerCustomWidgetInterface` 是自定义 widget 进入 Qt Designer 的身份证和构造入口：它描述控件、创建控件、声明代码生成依赖，并在加载时接入 Designer 扩展系统。
