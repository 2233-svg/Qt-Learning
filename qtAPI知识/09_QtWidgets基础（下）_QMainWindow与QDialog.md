# Qt Widgets 基础（下）：QMainWindow 与 QDialog

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Widgets  
> 核心类型：`QMainWindow`、`QMenuBar`、`QToolBar`、`QDockWidget`、`QStatusBar`、`QAction`、`QDialog`、`QDialogButtonBox`

## 1. 两类应用级窗口

Qt Widgets 中最常见的顶层窗口：

- `QMainWindow`：长期存在的主工作窗口，有固定的菜单、工具栏、Dock、状态栏和中心区框架；
- `QDialog`：围绕一次短任务、设置或确认的窗口，可模态或非模态，并可返回结果。

它们都继承 QWidget，但不能当作普通空白 QWidget 使用。

## 2. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

常用头文件：

```cpp
#include <QMainWindow>
#include <QMenuBar>
#include <QToolBar>
#include <QDockWidget>
#include <QStatusBar>
#include <QAction>
#include <QDialog>
#include <QDialogButtonBox>
```

## 3. QMainWindow 的固定结构

```text
┌──────────────── 菜单栏 ────────────────┐
├──────────────── 工具栏 ────────────────┤
│ Dock 区 │                           │ Dock 区 │
│         │        中心控件           │         │
│         │     centralWidget         │         │
├──────────────── 状态栏 ────────────────┤
```

主窗口有自己的内部布局。不要直接对 QMainWindow 调用 `setLayout()`。

正确方式：

```cpp
auto *central = new QWidget;
auto *layout = new QVBoxLayout(central);
layout->addWidget(editor);
setCentralWidget(central);
```

## 4. 最小可用主窗口

```cpp
#include <QApplication>
#include <QMainWindow>
#include <QMenuBar>
#include <QPlainTextEdit>
#include <QStatusBar>
#include <QToolBar>

class MainWindow : public QMainWindow
{
public:
    MainWindow()
    {
        auto *editor = new QPlainTextEdit;
        setCentralWidget(editor);//在 Qt 应用程序中，主窗口通常具有一个中心窗口部件。中心窗口部件是指 QMainWindow 类中的一个 QWidget 对象，它被放置在主窗口的中心区域，占据主要的显示区域，用于显示应用程序的主要内容。setCentralWidget 是QMainWindow 类的一个成员函数，用于设置窗口的中心部件。通过调用 setCentralWidget 方法，可以将一个 QWidget 对象设置为主窗口的中心部件。

        auto *clearAction = new QAction(tr("清空"), this);//tr是用来实现翻译的
        clearAction->setShortcut(QKeySequence::Delete);//QAction类提供了setShortcut()方法，可以为动作设置快捷键
        connect(clearAction, &QAction::triggered,
                editor, &QPlainTextEdit::clear);

        menuBar()->addMenu(tr("编辑"))->addAction(clearAction);
        addToolBar(tr("编辑"))->addAction(clearAction);

        statusBar()->showMessage(tr("就绪"));
        resize(720, 480);
    }
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    MainWindow window;
    window.show();
    return app.exec();
}
```

菜单和工具栏复用同一个 QAction，因此文本、图标、快捷键、启用状态和触发逻辑只有一个来源。

## 5. 中心控件

```cpp
setCentralWidget(new QPlainTextEdit);
```

`setCentralWidget()` 把控件交给主窗口管理。再次设置会替换原中心控件；需要保留旧控件时先用 `takeCentralWidget()` 取回所有权。

多页面中心区常用：

- `QStackedWidget`：一次显示一页；
- `QTabWidget`：标签页；
- `QSplitter`：可拖动分割；
- 普通 QWidget + Layout：组合多个控件。

## 6. QAction：命令的单一来源

一个“保存”命令可能同时出现在菜单、工具栏和快捷键中。不要为三个入口分别写三套槽。

```cpp
saveAction_ = new QAction(QIcon::fromTheme("document-save"),
                          tr("保存"), this);
saveAction_->setShortcut(QKeySequence::Save);
saveAction_->setStatusTip(tr("保存当前文档"));
connect(saveAction_, &QAction::triggered,
        this, &MainWindow::saveDocument);

fileMenu->addAction(saveAction_);
fileToolBar->addAction(saveAction_);
```

业务状态改变时统一更新：

```cpp
saveAction_->setEnabled(document_->isModified());
```

### 6.1 可选中动作

```cpp
wrapAction_->setCheckable(true);
connect(wrapAction_, &QAction::toggled,
        editor, [editor](bool enabled) {
    editor->setLineWrapMode(
        enabled ? QPlainTextEdit::WidgetWidth
                : QPlainTextEdit::NoWrap);
});
```

这里不能把 `toggled(bool)` 直接连接到 `setLineWrapMode(LineWrapMode)`：虽然 bool 和枚举底层都可表示为整数，但信号槽的类型签名不匹配。lambda 明确完成了状态到枚举的转换。

学习 API 时不要只看名字推断参数类型。

### 6.2 QActionGroup

互斥模式选择可使用 QActionGroup：

```cpp
auto *group = new QActionGroup(this);
group->setExclusive(true);

for (QAction *action : {lightAction, darkAction, systemAction}) {
    action->setCheckable(true);
    group->addAction(action);
}
```

## 7. 菜单栏与菜单

```cpp
QMenu *fileMenu = menuBar()->addMenu(tr("文件"));
fileMenu->addAction(newAction_);
fileMenu->addAction(openAction_);
fileMenu->addSeparator();
fileMenu->addAction(exitAction_);
```

动态菜单可在 `aboutToShow` 时刷新：

```cpp
connect(recentMenu, &QMenu::aboutToShow,
        this, &MainWindow::rebuildRecentMenu);
```

不要让失效动作留在菜单中。命令暂时不可用时禁用；永远不适用于当前模式时再隐藏。

## 8. 工具栏

```cpp
auto *toolbar = new QToolBar(tr("文件"), this);
toolbar->setObjectName("fileToolBar");
toolbar->addAction(openAction_);
toolbar->addAction(saveAction_);
addToolBar(Qt::TopToolBarArea, toolbar);
```

可限制停靠区域：

```cpp
toolbar->setAllowedAreas(Qt::TopToolBarArea |
                         Qt::BottomToolBarArea);
toolbar->setMovable(true);
```

工具栏中的普通命令使用 QAction。只有搜索框、缩放框等持续交互控件才用 `addWidget()`。

`addWidget()` 返回一个 QAction，工具栏拥有的是这个包装动作；控件的可见性和生命周期应按文档语义管理。

## 9. Dock Widget

Dock 是可停靠、浮动、关闭的面板：

```cpp
auto *dock = new QDockWidget(tr("属性"), this);
dock->setObjectName("propertiesDock");
dock->setWidget(new PropertyEditor(dock));
dock->setAllowedAreas(Qt::LeftDockWidgetArea |
                      Qt::RightDockWidgetArea);
addDockWidget(Qt::RightDockWidgetArea, dock);
```

`QDockWidget` 自身是外壳，实际内容必须通过 `setWidget()` 放入。

### 9.1 分割和标签化

```cpp
splitDockWidget(firstDock, secondDock, Qt::Vertical);
tabifyDockWidget(propertiesDock, historyDock);
propertiesDock->raise();
```

四个角落属于哪个 Dock 区可通过 `setCorner()` 调整。复杂布局应先建立所有 Dock，再恢复状态。

### 9.2 显示/隐藏 Dock 的标准动作

```cpp
viewMenu->addAction(dock->toggleViewAction());
```

这个 QAction 已与 Dock 可见性同步，不必自己维护勾选状态。

## 10. 状态栏

临时消息：

```cpp
statusBar()->showMessage(tr("已保存"), 3000);
```

永久区域：

```cpp
auto *positionLabel = new QLabel;
statusBar()->addPermanentWidget(positionLabel);
```

状态栏适合短状态，不应塞入长篇说明或关键错误。需要用户明确处理的错误使用内联提示或对话框。

## 11. 保存主窗口布局

`QWidget::saveGeometry()` 保存窗口几何；`QMainWindow::saveState()` 保存工具栏和 Dock 布局。

```cpp
settings.setValue("main/geometry", saveGeometry());
settings.setValue("main/state", saveState(1));
```

恢复：

```cpp
restoreGeometry(settings.value("main/geometry").toByteArray());
restoreState(settings.value("main/state").toByteArray(), 1);
```

### 11.1 objectName 为什么关键

保存状态通过 `objectName` 识别工具栏和 Dock：

```cpp
dock->setObjectName("propertiesDock");
toolbar->setObjectName("fileToolBar");
```

名称应稳定且唯一，不要使用会随翻译变化的窗口标题。

### 11.2 恢复顺序

1. 构造主窗口；
2. 创建所有需要恢复的工具栏和 Dock；
3. 为它们设置稳定 objectName；
4. 调用 `restoreGeometry()`；
5. 调用 `restoreState()`；
6. 恢复失败时使用默认布局。

版本参数可在布局结构不兼容时升级，避免旧数据强行套用。

## 12. QDialog 的用途

对话框适合：

- 获取少量输入；
- 编辑设置；
- 显示属性；
- 确认危险操作；
- 展示短期任务进度。

不适合把整个长期工作流塞进多层模态窗口。复杂编辑更适合主窗口页面或 Dock。

## 13. 模态与非模态

### 13.1 应用模态

阻止用户操作应用中的其他窗口：

```cpp
dialog->setWindowModality(Qt::ApplicationModal);
dialog->open();
```

### 13.2 窗口模态

只阻止关联的父窗口，其他顶层窗口仍可使用：

```cpp
dialog->setWindowModality(Qt::WindowModal);
dialog->open();
```

多窗口应用中通常优先窗口模态，减少不必要的全应用阻塞。

### 13.3 非模态

```cpp
dialog->show();
```

用户可同时操作其他窗口。查找、工具属性等持续面板适合非模态，但必须管理“重复打开”和对象生命周期。

## 14. 优先使用 open，而不是 exec

推荐的异步模态流程：

```cpp
auto *dialog = new SettingsDialog(this);
dialog->setAttribute(Qt::WA_DeleteOnClose);

connect(dialog, &QDialog::finished,
        this, [this](int result) {
    if (result == QDialog::Accepted)
        reloadSettings();
});

dialog->open();
```

`open()` 立即返回，不创建额外事件循环。通过 `finished(int)`、`accepted()` 或 `rejected()` 获取结果。

`exec()` 会同步等待并启动嵌套事件循环：

```cpp
if (dialog.exec() == QDialog::Accepted)
    apply();
```

虽然旧代码常见，但 Qt 6 文档明确建议避免，部分平台并不完整支持嵌套事件循环。嵌套循环还会让原本以为“当前函数未返回就不会发生”的删除、重入和状态变化提前发生。

## 15. open 的生命周期陷阱

错误：

```cpp
void Window::showSettings()
{
    SettingsDialog dialog(this);
    dialog.open();
} // 立即析构，对话框消失
```

`open()` 和 `show()` 立即返回，局部栈对象随函数结束而销毁。

正确选择：

- 在堆上创建并设置 parent；
- 使用 `WA_DeleteOnClose`；
- 把长期非模态对话框保存为成员；
- 或在确实采用同步 `exec()` 时才使用局部栈对象。

## 16. 对话框返回值

标准结果：

```cpp
QDialog::Accepted
QDialog::Rejected
```

结束方法：

```cpp
accept();       // Accepted
reject();       // Rejected
done(custom);   // 自定义 int
```

对应信号：

- `finished(int)`：所有 done/accept/reject 结果；
- `accepted()`：Accepted；
- `rejected()`：Rejected。

自定义业务数据应通过明确 getter、信号或数据对象传出，不要把大量业务状态塞进 int result code。

## 17. QDialogButtonBox

按钮盒按平台规范排列按钮：

```cpp
auto *buttons = new QDialogButtonBox(
    QDialogButtonBox::Ok |
    QDialogButtonBox::Cancel,
    this);

connect(buttons, &QDialogButtonBox::accepted,
        this, &QDialog::accept);
connect(buttons, &QDialogButtonBox::rejected,
        this, &QDialog::reject);
```

不要手动假定 Windows、macOS 和 Linux 的确定/取消按钮顺序相同。

### 17.1 校验后再 accept

```cpp
connect(buttons, &QDialogButtonBox::accepted,
        this, [this] {
    if (!validateInput()) {
        showValidationError();
        return;
    }
    accept();
});
```

把 accepted 信号无条件连接到 accept 会绕过输入校验。

## 18. 默认按钮与 Escape

`QPushButton::setDefault(true)` 指定按 Enter 触发的默认按钮。默认按钮应代表当前对话框最合理且安全的主要动作。

Esc 通常调用 `reject()`，而且 `QDialog` 的关闭行为有专门语义。需要保存确认时可重写 `reject()` 或关闭处理，但不要让用户完全无法关闭窗口。

破坏性动作不应成为默认按钮。

## 19. modeless 对话框单实例

```cpp
void MainWindow::showFindDialog()
{
    if (!findDialog_) {
        findDialog_ = new FindDialog(this);
        findDialog_->setAttribute(Qt::WA_DeleteOnClose);
        connect(findDialog_, &QObject::destroyed,
                this, [this] { findDialog_ = nullptr; });
    }

    findDialog_->show();
    findDialog_->raise();
    findDialog_->activateWindow();
}
```

也可把成员声明为 `QPointer<FindDialog>`，对象删除后自动清空。

`activateWindow()` 受平台防抢焦点策略限制，不保证强制把窗口带到前台。

## 20. 长任务不能放在模态槽中

模态只限制用户输入，不会让 GUI 线程获得额外执行能力：

```cpp
void ProgressDialog::start()
{
    doTenSecondTask(); // 界面仍冻结
}
```

耗时任务放到异步 API 或工作线程，对话框只显示进度、取消请求和最终状态。取消按钮应发出协作式取消请求，而不是强制终止线程。

## 21. 对话框 parent 的含义

```cpp
auto *dialog = new SettingsDialog(this);
```

parent 提供对象所有权，并让窗口系统知道瞬态父窗口；但仅设置 parent 不保证始终置顶。需要阻止父窗口交互时设置适当模态级别。

不要使用 `WindowStaysOnTopHint` 模拟模态，这会造成焦点、键盘和多窗口行为混乱。

## 22. 关闭、隐藏和删除

非模态工具窗口如果频繁打开，可选择隐藏并复用：

```cpp
dialog_->hide();
```

若每次都应重建，则：

```cpp
dialog->setAttribute(Qt::WA_DeleteOnClose);
dialog->show();
```

两种策略都可行，但成员指针、连接和状态恢复必须与策略一致。

对于异步 `open()`，finished 信号发出时若设置 DeleteOnClose，对象可能随后被删除。回调中不要把 dialog 裸指针保存到更晚执行的任务。

## 23. 窗口标题与修改标记

```cpp
setWindowFilePath(documentPath);
setWindowModified(document_->isModified());
setWindowTitle(tr("编辑器[*]"));
```

标题中的 `[*]` 会根据 modified 状态显示平台适当的修改标记。这样比手动拼接星号更符合平台风格。

## 24. 菜单、工具栏和快捷键的一致性

命令状态应从业务模型统一推导：

```cpp
void MainWindow::updateActions()
{
    const bool hasDocument = document_ != nullptr;
    saveAction_->setEnabled(hasDocument && document_->isModified());
    closeAction_->setEnabled(hasDocument);
    undoAction_->setEnabled(hasDocument && document_->canUndo());
}
```

不要分别禁用菜单项和工具栏按钮；它们应共享 QAction。快捷键也会同步禁用，避免界面显示不可用但快捷键仍执行。

## 25. 常见错误

### 25.1 给 QMainWindow 设置普通布局

主窗口已有专用布局。把普通布局放到 central widget，再 `setCentralWidget()`。

### 25.2 Dock 没有 objectName

`saveState()` 无法稳定识别，恢复布局失败或错位。使用唯一且不翻译的名称。

### 25.3 每个入口各建一个 QAction

状态和快捷键会分叉。一个业务命令只创建一个 QAction，多个视图复用。

### 25.4 open 局部栈对话框

函数返回后对象立即销毁。异步显示的对话框必须有足够生命周期。

### 25.5 无条件使用 exec

嵌套事件循环带来重入和平台兼容风险。优先 `open()` + finished。

### 25.6 accept 前不校验

连接 ButtonBox 时先运行输入校验，成功后才 accept。

### 25.7 用模态窗口执行耗时任务

GUI 线程仍会冻结。使用异步任务，并通过信号更新进度。

### 25.8 restoreState 调用过早

Dock 和 Toolbar 尚未创建时无法匹配。先完整搭建窗口结构，再恢复。

## 26. API 速查表

| API                          | 用途                 | 注意点                 |
| ---------------------------- | ------------------ | ------------------- |
| `setCentralWidget()`         | 设置中心区              | 主窗口管理所有权            |
| `menuBar()`                  | 获取菜单栏              | 菜单复用 QAction        |
| `addToolBar()`               | 添加工具栏              | 设置稳定 objectName     |
| `addDockWidget()`            | 添加 Dock            | 内容用 dock->setWidget |
| `tabifyDockWidget()`         | 标签化两个 Dock         | 可用 raise 选择当前页      |
| `toggleViewAction()`         | 标准显隐动作             | 自动同步勾选状态            |
| `statusBar()->showMessage()` | 临时状态消息             | 可设置超时               |
| `QMainWindow::saveState()`   | 保存 Dock/Toolbar 布局 | 与 objectName 和版本有关  |
| `restoreState()`             | 恢复布局               | 先创建所有组件             |
| `QDialog::open()`            | 异步模态显示             | 优先使用                |
| `QDialog::show()`            | 非模态显示              | 管理重复实例              |
| `QDialog::exec()`            | 同步模态显示             | 嵌套事件循环，不推荐          |
| `accept()` / `reject()`      | 标准结束结果             | 发出对应信号              |
| `done(int)`                  | 自定义结果结束            | 业务数据不要全塞 int        |
| `QDialogButtonBox`           | 平台化按钮排列            | 校验后再 accept         |

## 27. 自测题

### 题 1：QMainWindow 为什么不能直接 setLayout

<details>
<summary>答案</summary>

它已有管理菜单、工具栏、Dock、中心区和状态栏的内部布局。普通内容布局应放在中心 QWidget 上，再设为 central widget。

</details>

### 题 2：为什么菜单和工具栏共用 QAction

<details>
<summary>答案</summary>

命令文本、图标、快捷键、可用性、勾选状态和触发逻辑保持单一来源，任何入口都不会状态分叉。

</details>

### 题 3：saveState 恢复依赖什么

<details>
<summary>答案</summary>

工具栏和 Dock 必须先创建，并具有稳定唯一的 objectName；保存和恢复的版本号也要匹配。

</details>

### 题 4：open 为什么不能使用局部栈对话框

<details>
<summary>答案</summary>

open 立即返回，函数结束后局部对象析构，对话框来不及交互。应在堆上创建并由 parent/DeleteOnClose 管理，或保存长期成员。

</details>

### 题 5：open 相比 exec 的主要优势

<details>
<summary>答案</summary>

open 不启动嵌套事件循环，调用立即返回，通过信号报告结果，减少重入、意外删除和平台兼容问题。

</details>

## 28. 本篇总结

1. QMainWindow 是应用窗口框架，普通内容必须放进 central widget。
2. QAction 是命令模型，菜单、工具栏和快捷键应共享它。
3. Dock 和 Toolbar 使用稳定 objectName 后才能可靠保存恢复布局。
4. QDialog 的模态性描述输入范围，不代表可以在 GUI 线程执行慢任务。
5. 现代流程优先 `open()` + 完成信号，避免 `exec()` 的嵌套事件循环。
6. 异步显示的对话框不能是即将离开作用域的栈对象。
7. 用 QDialogButtonBox 遵守平台按钮顺序，并在校验成功后才 accept。

至此，QWidget 与应用级窗口的基础结构已经完整。下一章将系统讲解标签、按钮、输入框、选择控件、列表、进度和反馈等常用 Widgets。
