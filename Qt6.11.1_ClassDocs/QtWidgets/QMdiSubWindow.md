# QMdiSubWindow

> Qt 6.11.1 · Qt Widgets · 来自 `QMdiSubWindow`

## 1. 先建立直觉

`QMdiSubWindow` 是 `QMdiArea` 里的单个子窗口外壳。它给普通内容控件加上 MDI 场景需要的标题、边框、系统菜单、最小化/最大化/关闭、移动和缩放能力。

可以把它理解为“主窗口内部的小窗口”。里面真正承载业务的是 `setWidget()` 放进去的控件；`QMdiSubWindow` 负责窗口壳、状态和与 `QMdiArea` 的协作。

## 2. 类说明

`QMdiSubWindow` 继承自 `QWidget`。它通常由 `QMdiArea::addSubWindow()` 创建，也可以手动构造后加入 MDI 区域。

它提供 `RubberBandResize`、`RubberBandMove` 选项，允许移动/缩放时只显示预览框，从而降低复杂内容实时重排成本。键盘移动步长、系统菜单、shade 状态也都在这个类上控制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QMdiSubWindow(QWidget *, Qt::WindowFlags)` | 创建 MDI 子窗口壳。 |
| `setWidget(QWidget *)` / `widget()` | 设置或读取内部内容控件。 |
| `mdiArea()` | 返回所属 `QMdiArea`。 |
| `setSystemMenu(QMenu *)` / `systemMenu()` | 定制子窗口系统菜单。 |
| `showSystemMenu()` | 在当前位置显示系统菜单。 |
| `showShaded()` | 折叠成只显示标题栏的 shade 状态。 |
| `isShaded()` | 判断是否处于 shade 状态。 |
| `setOption(RubberBandResize/Move, bool)` | 控制移动或缩放时是否使用橡皮筋预览。 |
| `testOption(SubWindowOption)` | 查询子窗口选项是否启用。 |
| `setKeyboardSingleStep(int)` / `keyboardSingleStep()` | 设置键盘移动/调整的单步步长。 |
| `setKeyboardPageStep(int)` / `keyboardPageStep()` | 设置键盘 page 步长。 |
| `aboutToActivate()` | 子窗口即将激活时发出，适合同步工具栏和菜单。 |
| `windowStateChanged(old, now)` | 最小化、最大化、还原等状态变化时发出。 |

## 4. 关键用法

通常不手动 new 子窗口，而是让 `QMdiArea` 包装内容：

```cpp
auto *editor = new DocumentEditor;
auto *sub = mdiArea->addSubWindow(editor);
sub->setWindowTitle(editor->fileName());
sub->show();
```

需要定制窗口壳时，可以手动创建：

```cpp
auto *sub = new QMdiSubWindow;
sub->setWidget(new PreviewPanel);
sub->setOption(QMdiSubWindow::RubberBandResize, true);
mdiArea->addSubWindow(sub);
sub->show();
```

响应激活：

```cpp
connect(sub, &QMdiSubWindow::aboutToActivate, this, [=] {
    setCurrentDocument(qobject_cast<DocumentEditor *>(sub->widget()));
});
```

## 5. 使用场景

适合每个文档需要独立窗口状态的 MDI 应用：例如图纸窗口、数据表窗口、多个查询结果、多个图像视图、工程中的多个编辑器。

如果界面只需要简单标签页，不需要窗口壳、平铺、层叠、最小化等概念，就不必直接使用 `QMdiSubWindow`。

## 6. 常见坑与经验

`setWidget()` 后，内容控件生命周期通常由子窗口接管。不要同时在别处手动删除同一个 widget。

业务状态应放在内部 widget 或文档对象里，不要塞进子窗口壳。子窗口会被关闭、重建或模式切换，壳不应该变成文档模型。

`RubberBandResize` 对重型控件有帮助，但用户释放鼠标前看不到实时内容变化。性能和即时反馈要按场景取舍。
