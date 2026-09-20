# Qt QFormBuilder 深入笔记：给 Designer 宿主构建运行时表单

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFormBuilder>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QAbstractFormBuilder -> QFormBuilder`

`QFormBuilder` 根据 Qt Widgets Designer 产生的 `.ui` 文件，在运行时构造一棵 widget 树。它的重点不只是“加载 UI”，而是为**嵌入 Qt Designer 的应用、自定义组件容器和自定义控件插件**提供表单构建与插件发现能力。

Qt 文档给出的选择建议很明确：

- 普通独立应用需要运行时加载 `.ui`：使用 `QtUiTools` 模块的 `QUiLoader`。
- 应用本身在做 Designer 宿主、表单编辑器或自定义 Designer 组件：使用 `QFormBuilder`。

两者都会读取 `.ui`，但所在模块、面向的扩展场景和插件接口不同。不要因为 API 相似就随手互换。

## 1. 它在表单构建链路中的位置

```text
Designer .ui 文件
      |
      v
QFormBuilder / QAbstractFormBuilder
      |
      +-- 内置 Qt Widgets
      +-- QDesignerCustomWidgetInterface 插件
      |
      v
根 QWidget 与其子控件、布局、动作对象
```

`load()`、`save()` 等表单读写能力来自基类 `QAbstractFormBuilder`。`QFormBuilder` 在此基础上增加的 API 主要围绕**自定义 widget 插件路径和插件接口**展开。本页速查表列出 `QFormBuilder` 自己声明的成员；真正读取、保存 `.ui` 的继承 API 需要结合 `QAbstractFormBuilder` 一起使用。

## 2. 最小加载示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Designer Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Designer Qt6::Widgets)
```

```cpp
#include <QFile>
#include <QFormBuilder>
#include <QVBoxLayout>
#include <QWidget>

QFile file(":/forms/property-editor.ui");
if (!file.open(QIODevice::ReadOnly)) {
    return;
}

QFormBuilder builder;
QWidget *form = builder.load(&file, this); // load() 继承自 QAbstractFormBuilder
if (!form) {
    return;
}

auto *layout = new QVBoxLayout(this);
layout->addWidget(form);
```

`parentWidget` 决定返回根 widget 的对象树归属。上例传入 `this`，所以 `form` 由当前界面管理。传入空指针时，调用方必须马上安排它的所有权，不能把裸指针遗留在某个临时变量里。

## 3. 自定义控件插件是它的核心价值

普通控件如 `QPushButton`、`QLineEdit` 不需要额外插件；`.ui` 中出现自定义控件时，`QFormBuilder` 需要从插件路径发现实现 `QDesignerCustomWidgetInterface` 的插件。

```cpp
QFormBuilder builder;
builder.addPluginPath(QCoreApplication::applicationDirPath() + "/designer");

for (QDesignerCustomWidgetInterface *plugin : builder.customWidgets()) {
    qDebug() << plugin->name() << plugin->group();
}
```

`customWidgets()` 返回当前可用的自定义控件接口列表。列表中的接口由插件加载机制维持，不应把它当成“由调用者负责 delete 的对象数组”。最实用的用途是加载前诊断：确认期望的 widget 类是否已经被发现。

插件是动态库，会执行代码。不要把来自下载目录、可写临时目录或不可信网络位置的路径加入 `pluginPaths`。

## 4. 三种插件路径操作

```text
已有路径列表 -- addPluginPath() --> 追加一个目录
已有路径列表 -- setPluginPath() --> 整体替换为新列表
已有路径列表 -- clearPluginPaths() --> 清空
```

- 临时额外发现一个插件目录时，用 `addPluginPath()`。
- 从配置文件或应用策略完全接管搜索目录时，用 `setPluginPath()`。
- 想构造一个不搜索外部自定义控件的受控环境时，用 `clearPluginPaths()`。

注意 `setPluginPath()` 名称是单数 `Path`，但参数是 `QStringList`，它不是“设置一个目录”，而是**替换整个目录列表**。

## 5. 典型使用场景

### 5.1 Designer 嵌入式工具

例如 IDE、内部表单编辑器或可视化页面搭建器，需要读取用户编辑的 `.ui`，同时支持公司自定义的属性编辑器、曲线控件和业务控件插件。这里既需要构造表单，也需要列举、管理和调试自定义 widget 插件，`QFormBuilder` 正是为此准备的。

### 5.2 验证 UI 与插件环境

工具在真正 `load()` 前，可以通过 `pluginPaths()` 记录搜索路径，通过 `customWidgets()` 输出已发现控件。若某个 `.ui` 在开发机可加载、在发布环境失败，最先比较的往往就是这两项，而不是盲目重装 Qt。

### 5.3 不适合用它的场景

业务程序只想把资源中的一个 `.ui` 当作可换页面加载，没有 Designer 宿主和自定义 Designer 插件需求时，`QUiLoader` 的依赖更小、语义也更直接。

## 6. 生命周期和线程边界

`QFormBuilder` 不是 QObject，不使用 parent 对象树。它通常是局部对象；它构建出来的 widget 才需要加入 QObject/Widget 对象树。

创建和修改 widget 必须在 GUI 线程完成。磁盘或网络读取可以在工作线程做，但把 XML 交给 `QFormBuilder::load()`、创建控件并嵌入界面必须回到 GUI 线程。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFormBuilder()` | 创建表单构建器 | `load()`、`save()` 等核心表单读写能力继承自 `QAbstractFormBuilder` |
| 析构 | `~QFormBuilder()` | 销毁构建器与其插件发现状态 | 已经返回的根 widget 仍需由其 parent 或调用方管理 |
| 插件路径 | `pluginPaths() const` | 返回搜索自定义 widget 插件的目录列表 | 用于诊断发布环境与开发环境的插件发现差异 |
| 插件路径 | `addPluginPath(const QString &pluginPath)` | 在现有搜索列表末尾增加一个插件目录 | 仅加入受信任目录；插件是可执行代码 |
| 插件路径 | `setPluginPath(const QStringList &pluginPaths)` | 用新目录列表整体替换现有插件搜索路径 | 名称虽是单数，参数是整个列表；会丢失先前未包含的目录 |
| 插件路径 | `clearPluginPaths()` | 清空全部自定义 widget 插件搜索目录 | 适合受控环境；之后依赖外部自定义控件的 `.ui` 可能无法构建 |
| 自定义控件 | `customWidgets() const` | 返回已发现插件提供的 `QDesignerCustomWidgetInterface` 列表 | 用于检查可用控件；不要擅自释放返回的接口指针 |

---

### 一句话总结

`QFormBuilder` 是偏向 Qt Widgets Designer 宿主的运行时表单构建器。它的关键不是简单读取 `.ui`，而是让自定义 Designer 控件插件可以被发现、审查和用于构建表单；独立应用的动态 UI 通常选 `QUiLoader` 更合适。
