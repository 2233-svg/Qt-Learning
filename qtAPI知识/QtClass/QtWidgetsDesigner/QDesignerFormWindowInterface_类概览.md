# QDesignerFormWindowInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerFormWindowInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QWidget`

## 它解决什么问题

`QDesignerFormWindowInterface` 代表 Qt Widgets Designer 工作区中一份正在编辑的 `.ui` 窗体。它不是运行时普通窗口的替代品，而是 Designer 用来承载窗体内容、选择状态、资源文件、保存状态和 UI 元数据的编辑会话对象。

插件或 IDE 集成通过它可以：

- 找到某个 widget 或 action 所属的 `.ui` 窗体；
- 控制 Designer 是否把一个 widget 当作可编辑设计对象；
- 改变 Designer 画布的选择，并通过 cursor 执行可追踪的属性修改；
- 读写 `.ui` XML 内容、文件名、作者、注释、资源和代码生成设置；
- 响应文件、选区、资源、几何和 widget 管理状态的变化。

它不应直接实例化。常见取得方式是从对象反查，或从窗体管理器取得：

```cpp
auto *formWindow = QDesignerFormWindowInterface::findFormWindow(widget);

auto *manager = core->formWindowManager();
auto *activeFormWindow = manager->activeFormWindow();
```

## Designer 管理与 QObject 所有权不是一回事

`manageWidget()` 和 `unmanageWidget()` 解决的是“Designer 要不要编辑这个 widget”。普通自定义 widget 插件默认往往只有插件的顶层 widget 受 Designer 管理；如果内部 child 也需要被设计器选中、移动或调整，才考虑把它纳入管理。

这不改变 `QWidget` 的 parent-child 关系，也不等于销毁或创建对象。调用 `unmanageWidget()` 后对象仍存在，只是不再由 Designer 当作设计对象处理。相关信号的顺序是：

```text
aboutToUnmanageWidget(widget)  // 此时仍处于 managed 状态
widgetUnmanaged(widget)        // 此时已不再受 Designer 管理
```

## 选择、cursor 与撤销栈

`selectWidget()`、`clearSelection()` 和 `selectionChanged()` 管的是 Designer 画布选区。批量读取选区、移动选中位置或修改 widget 属性时，应从 `cursor()` 取得 `QDesignerFormWindowCursorInterface`。

```cpp
if (formWindow && formWindow->isManaged(widget)) {
    formWindow->selectWidget(widget);
    formWindow->cursor()->setWidgetProperty(widget, "text", "Run");
}
```

不要只调用 `widget->setProperty()` 再 `setDirty(true)` 来模拟 Designer 编辑。前者会绕开 Designer 的命令和撤销系统；需要用户可撤销的改动应通过 form window cursor。

`emitSelectionChanged()` 是实现方在内部选择模型已经改变后补发通知的接口。普通插件通常调用 `selectWidget()` 或 `clearSelection()`，不应无意义地手工发射选择信号。

## 资源文件的两个层次

- `resourceFiles()`：这份 `.ui` 关联和保存的 `.qrc` 文件列表；
- `activeResourceFilePaths()`：Designer 当前实际通过 `QResource` 激活、可供资源选择器使用的 `.qrc` 路径。

IDE 集成可用 `activateResourceFilePaths()` 将项目资源传给 Designer。它的错误数量和错误信息由输出参数返回。这个全局激活集合和当前 `.ui` 需要写入的 `resourceFiles()` 不是同一个概念。

## `.ui` 序列化和代码生成设置

`contents()` 返回当前 UI 内容，`setContents()` 可从字符串或任意 `QIODevice` 载入 UI。设备版本在失败时会把原因写到 `errorMessage`，很适合 IDE 打开和重新载入 `.ui` 时报告 XML 错误。

字符串版 `setContents()` 是重载槽，连接信号时要显式消歧：

```cpp
connect(source, &Source::uiTextReady,
        formWindow,
        qOverload<const QString &>(
            &QDesignerFormWindowInterface::setContents));
```

`includeHints()`、`exportMacro()`、`pixmapFunction()` 和布局设置会影响 `.ui` 元数据或 `uic` 的生成代码。`layoutDefault()` 使用具体数值，而 `layoutFunction()` 使用函数名；一旦设置布局函数，生成代码会调用这些函数来替代默认 margin 和 spacing。

## 功能、网格、检查和保存状态

`Feature` 是 `QFlags<FeatureFlag>`。`setFeatures()` 接收的是一整个 flags 组合，不是“追加一个功能”的命令；保留已有标志时，先读 `features()`，修改后再写回。

`grid()` 的 `QPoint` 表示网格单元宽和高，不是画布坐标。`checkContents()` 返回富文本警告，例如未放进布局的顶层 spacer；它适合保存前提示，不会修复问题，也不替代保存操作。

`isDirty()` 表示修改尚未保存。只有真正保存成功或成功载入新内容后才应 `setDirty(false)`，不能用它掩盖保存失败。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum FeatureFlag` | 定义 form window 可用的 Designer 功能。 | 与 `Feature` 组合使用；设置时传入完整 flags 组合。 |
| 标志 | `EditFeature` | 表示窗体支持编辑。 | 禁用后不要假设仍能进行普通画布编辑。 |
| 标志 | `GridFeature` | 表示窗体提供设计网格。 | 与实际 `grid()` 间距设置配合使用。 |
| 标志 | `TabOrderFeature` | 表示窗体支持 tab 顺序编辑。 | 只影响 Designer 的编辑能力，不直接修改运行时焦点逻辑。 |
| 标志 | `DefaultFeature` | 默认组合，由 `EditFeature` 和 `GridFeature` 组成。 | 它是组合值，不是独立的第四种功能。 |
| 类型 | `Feature` | `QFlags<FeatureFlag>`，可组合多个功能标志。 | 查询单项优先用 `hasFeature()`。 |
| 类型 | `enum ResourceFileSaveMode` | 指定保存窗体时如何处理资源文件。 | 会影响 `.qrc` 文件写入，宿主项目应明确负责方。 |
| 枚举值 | `SaveAllResourceFiles` | 保存全部关联资源文件。 | 可能改写当前窗体未直接使用的资源文件。 |
| 枚举值 | `SaveOnlyUsedResourceFiles` | 只保存当前 form 实际使用的资源文件。 | 使用前确认不会漏掉项目层面的资源维护。 |
| 枚举值 | `DontSaveResourceFiles` | 保存 form 时不保存资源文件。 | 资源由 IDE 或项目的其它流程维护时使用。 |
| 构造 | `QDesignerFormWindowInterface(QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 构造 form window 接口 widget。 | 正常由 Designer 创建，插件不应自己构造替代对象。 |
| 析构 | `~QDesignerFormWindowInterface()` | 销毁 form window 接口。 | 窗体关闭或被管理器移除后，插件缓存的非拥有指针必须作废。 |
| 管理前通知 | `aboutToUnmanageWidget(QWidget *widget)` | widget 即将变为非受管状态时发出。 | 此时仍受管；需要收尾 Designer 状态时在这里处理。 |
| 窗体目录 | `absoluteDir() const` | 返回当前 `.ui` 所在目录的绝对路径。 | 只读；解析相对资源或头文件时可作基准。 |
| 激活资源 | `activateResourceFilePaths(const QStringList &paths, int *errorCount = nullptr, QString *errorMessages = nullptr)` | 激活 `.qrc` 路径，使其资源可在 Designer 中使用。 | 检查错误输出；它不同于修改当前 form 的 `resourceFiles()`。 |
| 激活通知 | `activated(QWidget *widget)` | form 中某 widget 被激活时发出。 | 用来同步 Designer 面板上下文，不等同于普通 focus 事件。 |
| 活跃资源 | `activeResourceFilePaths() const` | 返回当前已被 Designer 激活的 `.qrc` 路径。 | 这是编辑器资源集合，不等价于 form 关联资源。 |
| 添加资源 | `addResourceFile(const QString &path)` | 将 `.qrc` 加入当前 form 使用的资源列表。 | 会改变 form 元数据；随后可监听 `resourceFilesChanged()`。 |
| 作者 | `author() const` | 返回 form 作者或创建者元数据。 | 不代表版本控制提交作者。 |
| 修改通知 | `changed()` | form 内容发生变化时发出。 | 可用来更新保存提示，不表示内容已经写入磁盘。 |
| 保存前检查 | `checkContents() const` | 检查当前 form 并返回潜在问题的富文本警告。 | 适合保存前提示；不自动修复，也不阻止保存。 |
| 清空选择 | `clearSelection(bool update = true)` | 清除当前 Designer 选区。 | `update = true` 会发出选择变化通知；批量更新时谨慎延迟。 |
| 注释 | `comment() const` | 返回 form 的人类可读注释。 | 不要把它作为程序必须解析的结构化数据。 |
| UI 内容 | `contents() const` | 返回当前 form 的 UI 内容。 | 内容可能很大，适用于导出、保存或差异比较。 |
| 所属核心 | `core() const` | 返回当前 `QDesignerFormEditorInterface`。 | 返回指针由 Designer 持有。 |
| 编辑 cursor | `cursor() const` | 返回本窗体的 `QDesignerFormWindowCursorInterface`。 | 用于可撤销的属性修改；不要和 `QTextCursor` 混淆。 |
| 发射选择通知 | `emitSelectionChanged()` | 主动发出 `selectionChanged()`。 | 通常仅供 form window 实现方在内部状态更新后调用。 |
| 导出宏 | `exportMacro() const` | 返回 form 的导出宏，用于把 form 编译为 widget 插件。 | 普通应用 UI 通常不需要设置。 |
| 功能变化通知 | `featureChanged(Feature feature)` | 功能 flags 改变时发出，并携带新组合。 | 参数是 flags 组合，不应当作单个枚举值。 |
| 功能集合 | `features() const` | 返回当前支持的功能 flags。 | 用 `hasFeature()` 检查单项更清晰。 |
| UI 文件名 | `fileName() const` | 返回描述当前 form 的 `.ui` 文件名。 | 文件名变化时监听 `fileNameChanged()`。 |
| 文件名通知 | `fileNameChanged(const QString &fileName)` | form 文件名改变时发出。 | 更新宿主标签、保存目标或最近文件列表。 |
| 查找所属窗体 | `findFormWindow(QObject *object)` | 返回给定 QObject 所属的 form window。 | 找不到会返回空；适合 action、button group 等非 widget 对象。 |
| 查找所属窗体 | `findFormWindow(QWidget *widget)` | 返回给定 widget 所属的 form window。 | 只对 Designer 工作区对象有意义，使用前检查空指针。 |
| 窗体容器 | `formContainer() const` | 返回包含主容器 widget 的 form 容器。 | 它不一定等于主容器本身，注意层级区别。 |
| 几何通知 | `geometryChanged()` | form 几何变化时发出。 | 用于刷新设计视图相关信息，不是每个 child 的通用 geometry 通知。 |
| 网格间距 | `grid() const` | 返回 form 使用的网格间距。 | `QPoint` 的 x、y 表示单元宽高，不是一个网格位置。 |
| 功能查询 | `hasFeature(Feature feature) const` | 判断 form 是否提供指定功能 flags。 | 可以传组合，单项判断最直观。 |
| include 提示 | `includeHints() const` | 返回会写进关联 UI 的头文件列表。 | 可含相对头或 `<QtGui/QWidget>` 形式的系统头。 |
| 未保存状态 | `isDirty() const` | 判断 form 是否已修改但未保存。 | 保存成功后才应清除 dirty 状态。 |
| 受管查询 | `isManaged(QWidget *widget) const` | 判断 widget 是否受 Designer 管理。 | 受管状态不等于对象所有权，也不等于可见性。 |
| 默认布局数值 | `layoutDefault(int *margin, int *spacing)` | 通过输出参数返回默认布局 margin 与 spacing。 | 传入有效指针；这是数值默认值。 |
| 布局函数名 | `layoutFunction(QString *margin, QString *spacing)` | 通过输出参数返回生成代码使用的 margin、spacing 函数名。 | 这是代码生成配置，不是当前实际像素值。 |
| 主容器通知 | `mainContainerChanged(QWidget *mainContainer)` | form 主容器改变时发出。 | 更新依赖根 widget 的插件逻辑，注意指针生命周期。 |
| 纳入管理 | `manageWidget(QWidget *widget)` | 将 widget 纳入 Designer 管理。 | 适合插件内部需要在设计态编辑的 child；不改变 QObject 所有权。 |
| 对象移除通知 | `objectRemoved(QObject *object)` | action、`QButtonGroup` 等对象从 form 移除时发出。 | 清理对象缓存，不能只监听 `widgetRemoved()`。 |
| 图片加载函数 | `pixmapFunction() const` | 返回 form 中用于加载 pixmap 的函数名。 | 它影响生成代码策略，不是立即加载图片的调用。 |
| 移除资源 | `removeResourceFile(const QString &path)` | 从当前 form 的关联资源列表中移除 `.qrc`。 | 不会删除磁盘文件；操作后会产生资源列表变化。 |
| 资源保存策略 | `resourceFileSaveMode() const` | 返回当前资源文件保存策略。 | 保存前确认策略符合宿主项目的资源管理责任。 |
| 关联资源 | `resourceFiles() const` | 返回当前 form 使用的资源文件路径。 | 与 `activeResourceFilePaths()` 的全局激活集合不同。 |
| 资源变化通知 | `resourceFilesChanged()` | form 关联资源列表变化时发出。 | 用于同步项目资源面板或保存流程。 |
| 设置选择 | `selectWidget(QWidget *widget, bool select = true)` | 选中或取消选中指定 widget。 | widget 应属于当前 form；批量操作后注意选择通知。 |
| 选择通知 | `selectionChanged()` | 当前 Designer 选区改变时发出。 | 需要具体选区时用 `cursor()` 查询。 |
| 设置作者 | `setAuthor(const QString &author)` | 设置 form 作者或创建者元数据。 | 修改后属于 form 内容变化，应进入保存流程。 |
| 设置注释 | `setComment(const QString &comment)` | 设置 form 的人类可读注释。 | 适合说明，不要承载机器可读配置。 |
| 载入字符串内容 | `setContents(const QString &contents)` | 从 UI 字符串加载 form，返回是否成功。 | 是重载槽；函数指针连接时用 `qOverload<const QString &>` 消歧。 |
| 载入设备内容 | `setContents(QIODevice *device, QString *errorMessage = 0)` | 从设备读取 UI 内容并加载 form，返回是否成功。 | 失败时读取 `errorMessage`；设备应处于可读状态。 |
| 设置 dirty | `setDirty(bool dirty)` | 设置 form 是否为“已修改未保存”。 | 保存失败时不能设为 `false`，否则可能造成数据丢失。 |
| 设置导出宏 | `setExportMacro(const QString &exportMacro)` | 设置 form 编译为 widget 插件时使用的导出宏。 | 主要服务插件生成，普通 `.ui` 不一定需要。 |
| 设置功能 | `setFeatures(Feature features)` | 启用指定功能 flags 组合。 | 是整体替换；保留旧值时先取 `features()` 再修改。 |
| 设置文件名 | `setFileName(const QString &fileName)` | 设置 form 对应的 UI 文件名。 | 只改目标名，实际写文件仍由保存流程负责。 |
| 设置网格 | `setGrid(const QPoint &grid)` | 设置 Designer 网格单元宽高。 | `x`、`y` 都是尺寸，取值应合理且非负。 |
| 设置 include 提示 | `setIncludeHints(const QStringList &includeHints)` | 设置会写入 UI 的头文件列表。 | 区分项目相对头与系统头的写法。 |
| 设置默认布局数值 | `setLayoutDefault(int margin, int spacing)` | 设置 form 默认布局的数值 margin 和 spacing。 | 与布局函数替代设置是不同层次。 |
| 设置布局函数 | `setLayoutFunction(const QString &margin, const QString &spacing)` | 设置 `uic` 生成代码时取 margin、spacing 的函数名。 | 设置后替代默认布局属性，函数必须在目标代码环境有效。 |
| 设置主容器 | `setMainContainer(QWidget *mainContainer)` | 设置 form 的主容器 widget。 | 会改变根设计对象上下文，传入 widget 必须与 form 相容。 |
| 设置图片函数 | `setPixmapFunction(const QString &pixmapFunction)` | 设置生成 form 时用于加载 pixmap 的函数名。 | 是代码生成钩子，函数名应在生成代码环境中有效。 |
| 设置资源保存策略 | `setResourceFileSaveMode(ResourceFileSaveMode behavior)` | 设置保存 form 时处理资源文件的策略。 | 可能影响项目 `.qrc` 写入，普通插件不应随意覆盖。 |
| 解除管理 | `unmanageWidget(QWidget *widget)` | 让 Designer 不再管理指定 widget。 | 不会销毁 widget；会依次关联管理前和解除管理通知。 |
| 受管通知 | `widgetManaged(QWidget *widget)` | widget 成为受管设计对象时发出。 | 可建立只在设计态需要的关联。 |
| widget 移除通知 | `widgetRemoved(QWidget *widget)` | widget 从 form 移除时发出。 | 清理指针缓存；这不等于仅解除 Designer 管理。 |
| 解除管理通知 | `widgetUnmanaged(QWidget *widget)` | widget 已变为非受管状态时发出。 | 此时不再能假定 Designer 会选择或编辑该 widget。 |

## 易错点

1. `resourceFiles()` 与 `activeResourceFilePaths()` 分别代表 form 元数据和 Designer 已加载资源，不能混用。
2. `manageWidget()`、`unmanageWidget()` 管的是 Designer 编辑资格，不管理对象生命周期。
3. 用户可撤销的属性改动应走 `cursor()`，不要直接设属性后只标记 dirty。
4. `setFeatures()` 会整体替换 flags，不是只追加一项。
5. `setContents()` 有重载，连接字符串槽时必须消除歧义。
6. `setDirty(false)` 不是保存函数，只有保存或载入成功后才应调用。

### 一句话总结

`QDesignerFormWindowInterface` 是 Designer 中一份 `.ui` 编辑会话的总入口，统一管理窗体选择、可编辑 widget、资源、UI 序列化和代码生成元数据。
