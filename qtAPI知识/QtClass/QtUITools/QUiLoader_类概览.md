# Qt QUiLoader 深入笔记：在运行时把 .ui 文件变成控件树

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUiLoader>`  
> 所属模块：`Qt6::UiTools`  
> 继承：`QObject -> QUiLoader`  
> 对象特性：不可复制、不可移动。

`QUiLoader` 读取 Qt Widgets Designer 保存的 `.ui` XML，并在**运行时**创建其中描述的 widget、layout、action 和 action group。它解决的是“界面文件不在编译期固定下来，而是由资源、磁盘、插件或外部配置决定”的问题。

```text
.ui XML + 可能的自定义控件插件
              |
              v
          QUiLoader::load()
              |
              v
根 QWidget + 子控件树 + 布局 + QAction
```

它和 `uic` 生成的 `ui_xxx.h` 不是同一种工作方式：

- `uic`：编译期把 `.ui` 变成 C++ 代码，类型安全、成员访问直接，适合普通固定界面。
- `QUiLoader`：程序运行时再解析 `.ui`，适合插件化页面、可替换皮肤、可配置工具面板或 Designer 宿主。

若 UI 永远随程序一起编译、布局也不需要动态更换，优先用 `uic`。`QUiLoader` 换来灵活性，也意味着你必须自己处理加载失败、对象所有权和 `findChild()` 查找。

## 1. 最小可用示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS UiTools Widgets)
target_link_libraries(mytarget PRIVATE Qt6::UiTools Qt6::Widgets)
```

```cpp
#include <QFile>
#include <QPushButton>
#include <QUiLoader>
#include <QVBoxLayout>
#include <QWidget>

QFile file(":/forms/preferences.ui");
if (!file.open(QIODevice::ReadOnly)) {
    return;
}

QUiLoader loader;
QWidget *page = loader.load(&file, this);
if (!page) {
    qWarning() << loader.errorString();
    return;
}

auto *applyButton = page->findChild<QPushButton *>("applyButton");
if (applyButton) {
    connect(applyButton, &QPushButton::clicked, this, &SettingsPane::apply);
}
```

`this` 是 `load()` 的 `parentWidget`。这样返回的根控件会加入当前控件的对象树，随父控件销毁，不需要手动 `delete`。如果传 `nullptr`，调用方必须立刻安排返回根控件的所有权，例如放进某个 layout、作为窗口显示后交给窗口生命周期管理，或用明确的智能指针策略管理它。

## 2. 运行时 UI 的三件要事

### 2.1 `.ui` 文件从哪里来

`load()` 接收 `QIODevice *`，所以来源不限于普通文件：

- `QFile(":/forms/page.ui")`：把 `.ui` 放进 qrc，发布最稳定。
- 磁盘上的 `QFile`：可替换主题或外部配置页面。
- `QBuffer`：从压缩包、网络或数据库取出的 XML 字节。

无论来源是什么，device 都要在调用前打开为可读状态，并且在 `load()` 返回前保持有效。

### 2.2 动态加载后如何拿到控件

编译期 `uic` 方案通常有 `ui->saveButton`；`QUiLoader` 没有这层静态成员。要给 `.ui` 内控件设置稳定的 `objectName`，再通过 `findChild()` 查找：

```cpp
auto *nameEdit = page->findChild<QLineEdit *>("nameEdit");
auto *saveButton = page->findChild<QPushButton *>("saveButton");
```

这也是动态 UI 的一个契约：改了 Designer 中的 `objectName`，C++ 查找代码就可能失效。对关键控件应在加载后立即判空并报告有意义的错误，而不是等用户点击时才崩溃。

### 2.3 失败时看哪里

`load()` 返回 `nullptr` 表示没有创建出根 widget。紧接着读取 `errorString()`，它给出最近一次加载错误的人类可读描述。

```cpp
QWidget *page = loader.load(&file, parent);
if (!page) {
    qWarning().noquote()
        << "Cannot load" << file.fileName() << ":" << loader.errorString();
}
```

不要继续把空指针加入 layout，也不要把错误只归结为“文件不存在”：非法 XML、未知 widget 类、缺失自定义 widget 插件都可能导致失败。

## 3. 自定义控件：插件路径和创建钩子

### 3.1 通过 Designer 自定义控件插件加载

`pluginPaths()` 是 loader 搜索自定义控件插件的目录列表。`addPluginPath()` 加入一个目录，`clearPluginPaths()` 清空当前列表；`availableWidgets()` 和 `availableLayouts()` 可以在实际加载前查看当前能创建什么类。

```cpp
loader.addPluginPath(QCoreApplication::applicationDirPath() + "/designer");

if (!loader.availableWidgets().contains("ColorRampEditor")) {
    qWarning() << "ColorRampEditor plugin is unavailable";
}
```

插件是可执行代码，不是普通资源文件。不要把不受信任目录、用户随手下载的目录或网络共享目录直接加入 `pluginPaths()`。

### 3.2 子类化，拦截对象创建

`createWidget()`、`createLayout()`、`createAction()` 与 `createActionGroup()` 是 `QUiLoader` 在解析 `.ui` 时内部调用的虚函数。覆写它们可以替换类、记录创建对象，或为创建过程附加业务初始化。

```cpp
class TrackingLoader : public QUiLoader
{
public:
    using QUiLoader::QUiLoader;

    QWidget *createWidget(const QString &className,
                          QWidget *parent,
                          const QString &name) override
    {
        QWidget *widget = QUiLoader::createWidget(className, parent, name);
        if (widget) {
            createdWidgets.append(widget);
        }
        return widget;
    }

    QList<QWidget *> createdWidgets;
};
```

覆写时先调用基类版本很重要：基类负责处理内置控件和已发现的插件。只有基类返回空指针、并且你明确认识该 `className` 时，再创建自己的替代控件。

## 4. 相对路径资源与语言切换

### 4.1 `workingDirectory`

`.ui` 中的图标、图片等相对路径资源，会以 `workingDirectory` 为基准解析。若 UI 文件和资源从磁盘目录一起发布，加载前设置它：

```cpp
loader.setWorkingDirectory(QDir("C:/app/themes/dark"));
```

如果资源走 qrc 路径，如 `:/icons/save.svg`，通常不依赖这个目录。磁盘 UI 显示了空图标时，除了检查路径，也要检查 `workingDirectory()`。

### 4.2 `LanguageChange`

`setLanguageChangeEnabled(true)` 后，由这个 loader 加载的 UI 收到 `LanguageChange` 事件时会自动重新翻译。它适用于应用在运行期间安装新的 `QTranslator` 并向顶层控件发送语言切换事件的场景。

这不是自动安装翻译器的 API，也不会替你维护业务代码里的字符串。它只影响 QUiLoader 创建的 UI 的自动重译行为。

当前 Qt 6.11.1 安装头文件还声明了 `setTranslationEnabled()` 和 `isTranslationEnabled()`；本机同版本 C++ 类页没有给出这两个接口的详细行为说明。将它们视为与 loader 翻译处理相关的版本特性即可，不要把它们和 `LanguageChange` 自动重译混为一谈；若项目依赖该开关，先在目标 Qt 版本上编写最小测试确认实际效果。

## 5. QObject 生命周期与线程边界

`QUiLoader` 自身是 QObject，可以给它 parent，但它通常只是一次性加载工具，局部变量就足够。真正重要的是 `load()` 返回的根 `QWidget` 的归属。

控件和 layout 的创建、加载、修改都应在 GUI 线程进行。不要在工作线程 `load()` 完一棵 QWidget 树后再搬到 GUI 线程使用；文件读取或下载可以放在工作线程，拿到完整内容后再在 GUI 线程把它放进 `QBuffer` 或打开文件并调用 `load()`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QUiLoader(QObject *parent = nullptr)` | 创建运行时 UI 加载器 | loader 可作为局部对象；真正要管理的是 `load()` 返回的根控件 |
| 析构 | `~QUiLoader()` | 销毁加载器及其内部状态 | 它不替代对已返回根 `QWidget` 的所有权安排 |
| 插件路径 | `pluginPaths() const` | 返回搜索自定义 widget 插件的目录列表 | 用它诊断插件发现路径，不代表每个插件都已成功加载 |
| 插件路径 | `clearPluginPaths()` | 清空自定义控件插件搜索目录 | 之后原目录内的自定义控件将不可发现；内置 widget 不受此操作影响 |
| 插件路径 | `addPluginPath(const QString &path)` | 增加一个自定义 widget 插件搜索目录 | 只加入受信任路径；插件加载意味着执行第三方代码 |
| 可用类型 | `availableWidgets() const` | 返回当前 `createWidget()` 可创建的 widget 类名 | 加载前用它检查自定义控件是否可用 |
| 可用类型 | `availableLayouts() const` | 返回当前 `createLayout()` 可创建的 layout 类名 | 适合诊断 UI 文件依赖的布局类是否已提供 |
| 加载 | `load(QIODevice *device, QWidget *parentWidget = nullptr)` | 读取 `.ui` 并创建根 widget 及其对象树 | device 必须已打开可读；失败返回 `nullptr`，随后读取 `errorString()`；立即安排根控件所有权 |
| 创建钩子 | `createWidget(const QString &className, QWidget *parent, const QString &name)` | 按类名创建 widget，解析 `.ui` 时内部调用 | 可覆写以处理自定义类；先调用基类版本，`parent` 和 `name` 不能丢 |
| 创建钩子 | `createLayout(const QString &className, QObject *parent, const QString &name)` | 按类名创建 layout，解析 `.ui` 时内部调用 | 覆写时先交给基类处理内置布局和已发现插件 |
| 创建钩子 | `createActionGroup(QObject *parent, const QString &name)` | 创建 `.ui` 中的 `QActionGroup` | 覆写可收集或替换动作组；保留 parent 维持对象树 |
| 创建钩子 | `createAction(QObject *parent, const QString &name)` | 创建 `.ui` 中的 `QAction` | 常用于记录菜单、工具栏动作；先调用基类版本 |
| 错误诊断 | `errorString() const` | 返回最近一次 `load()` 失败的人类可读错误 | 只在失败后立即读取最有价值；日志同时保留 UI 文件来源 |
| 语言切换 | `isLanguageChangeEnabled() const` | 查询加载 UI 是否启用 LanguageChange 自动重译 | 只描述自动重译开关，不表示应用已安装翻译器 |
| 语言切换 | `setLanguageChangeEnabled(bool enabled)` | 启用或关闭加载 UI 在语言切换事件上的自动重译 | 应配合 `QTranslator` 安装和正确派发 `LanguageChange` |
| 翻译处理 | `isTranslationEnabled() const` | 查询 header 声明的 loader 翻译处理开关 | Qt 6.11.1 本机 C++ 类页未给出详细语义；依赖前在目标版本做最小验证 |
| 翻译处理 | `setTranslationEnabled(bool enabled)` | 设置 header 声明的 loader 翻译处理开关 | 不要假定它等价于 `setLanguageChangeEnabled()`；需以目标版本实测为准 |
| 资源基准 | `workingDirectory() const` | 读取相对图片、图标等资源的解析目录 | 磁盘 `.ui` 资源找不到时先检查它 |
| 资源基准 | `setWorkingDirectory(const QDir &dir)` | 设置加载器解析相对资源的基准目录 | 在 `load()` 前设置；qrc 的 `:/` 资源通常不依赖它 |

---

### 一句话总结

`QUiLoader` 是运行时 UI 装配器：它把 `.ui` 变成控件树，也把所有权、控件查找、自定义插件和资源路径的责任交给调用方。加载成功不是终点，给根控件确定归属、验证关键 `objectName` 和报告 `errorString()` 才是可靠的动态 UI 流程。
