# QAction

> Qt 6.11.1 · Qt GUI · 来自 `QAction`

## 1. 先建立直觉

`QAction` 是 Qt 里的“命令对象”。同一个保存命令可以同时出现在菜单、工具栏、快捷键、上下文菜单里；你只维护一个 `QAction`，所有入口共享文本、图标、启用状态、勾选状态和触发信号。

它不是按钮，也不是菜单项。按钮和菜单只是 action 的不同展示方式。这个分层能避免“菜单能用、工具栏忘了禁用”这种状态分裂。

## 2. 类说明

`QAction` 继承自 `QObject`。它保存命令的元数据：`text`、`icon`、`shortcut`、`statusTip`、`toolTip`、`whatsThis`、`checkable`、`checked`、`enabled`、`visible` 等。

当用户通过任意展示入口激活它时，会发出 `triggered()`；鼠标悬停或菜单高亮时会发出 `hovered()`。可勾选 action 还能表示模式或开关状态。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QAction(text/icon, text, parent)` | 创建命令对象。 |
| `setText()` / `text()` | 设置菜单/按钮显示文本。 |
| `setIcon()` / `icon()` | 设置命令图标。 |
| `setShortcut()` / `shortcut()` | 设置主快捷键。 |
| `setShortcuts()` / `shortcuts()` | 设置多个快捷键。 |
| `setShortcutContext()` | 设置快捷键生效范围。 |
| `setCheckable()` / `isCheckable()` | 让 action 成为可勾选命令。 |
| `setChecked()` / `isChecked()` | 设置或读取勾选状态。 |
| `setEnabled()` / `isEnabled()` | 控制所有关联入口是否可用。 |
| `setVisible()` / `isVisible()` | 控制所有关联入口是否可见。 |
| `setData()` / `data()` | 附加业务数据，如命令 id。 |
| `associatedObjects()` | 查看 action 已被哪些对象使用。 |
| `trigger()` / `activate()` | 程序化触发命令。 |
| `triggered(bool)` | 命令被触发时发出。 |
| `toggled(bool)` | 勾选状态变化时发出。 |
| `hovered()` | 用户悬停/高亮该命令时发出。 |

## 4. 关键用法

```cpp
auto *save = new QAction(QIcon(":/icons/save.svg"), tr("&Save"), this);
save->setShortcut(QKeySequence::Save);
save->setStatusTip(tr("Save the current document"));

connect(save, &QAction::triggered, this, &MainWindow::saveDocument);

fileMenu->addAction(save);
toolBar->addAction(save);
```

可勾选模式：

```cpp
gridAction->setCheckable(true);
connect(gridAction, &QAction::toggled, canvas, &Canvas::setGridVisible);
```

## 5. 使用场景

适合菜单命令、工具栏按钮、上下文菜单项、快捷键命令、可开关模式、最近文件项、统一启用/禁用的业务动作。

如果只是一个临时按钮且不会出现在其他入口，可以直接用按钮信号；一旦命令有多个入口，就应抽成 `QAction`。

## 6. 常见坑与经验

命令状态应绑定业务状态。文档只读时禁用 save action，比逐个禁用菜单项和按钮更可靠。

`triggered(bool)` 的 bool 只对 checkable action 有明显意义；普通 action 不要过度依赖它。

快捷键冲突不会替你做业务仲裁。大型应用要集中管理 action 和 shortcut。
