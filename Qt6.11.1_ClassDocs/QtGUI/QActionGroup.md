# QActionGroup

> Qt 6.11.1 · Qt GUI · 来自 `QActionGroup`

## 1. 先建立直觉

`QActionGroup` 是 action 的逻辑分组器。它让一组菜单/工具栏命令共享启用、可见和互斥规则，例如“选择工具/移动工具/缩放工具”只能同时选一个。

它不负责显示，也不是菜单。显示仍由 `QMenu`、`QToolBar` 或按钮完成；group 负责行为关系。

## 2. 类说明

`QActionGroup` 继承自 `QObject`。加入组的 action 可以按 `ExclusionPolicy` 互斥、可选互斥或完全不互斥。

Qt 6 的 `ExclusionPolicy` 比旧的 `exclusive` 更明确：`Exclusive` 必须有一个选中项，`ExclusiveOptional` 允许没有选中项，`None` 则不做互斥。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QActionGroup(QObject *)` | 创建 action 组。 |
| `addAction(QAction *)` | 把已有 action 加入组。 |
| `addAction(text/icon, text)` | 创建并加入 action。 |
| `removeAction(QAction *)` | 从组中移除 action，不删除 action 本身。 |
| `actions()` | 返回组内所有 action。 |
| `checkedAction()` | 返回当前选中的 action。 |
| `setExclusionPolicy()` / `exclusionPolicy()` | 设置或读取互斥策略。 |
| `setExclusive(bool)` / `isExclusive()` | 旧式互斥属性接口。 |
| `setEnabled()` / `isEnabled()` | 统一控制组内 action 启用状态。 |
| `setVisible()` / `isVisible()` | 统一控制组内 action 可见性。 |
| `triggered(QAction *)` | 组内任一 action 触发时发出。 |
| `hovered(QAction *)` | 组内任一 action 悬停时发出。 |

## 4. 关键用法

```cpp
auto *tools = new QActionGroup(this);
tools->setExclusionPolicy(QActionGroup::ExclusionPolicy::Exclusive);

auto *select = tools->addAction(tr("Select"));
select->setCheckable(true);

auto *pan = tools->addAction(tr("Pan"));
pan->setCheckable(true);

connect(tools, &QActionGroup::triggered, this, &MainWindow::setToolFromAction);
```

可取消的单选：

```cpp
group->setExclusionPolicy(QActionGroup::ExclusionPolicy::ExclusiveOptional);
```

## 5. 使用场景

适合互斥工具模式、视图模式选择、排序方式、颜色/线型选项、菜单中的单选命令、工具栏 toggle 组。

如果只是视觉分组，用菜单分隔线或工具栏分组即可；行为互斥才需要 action group。

## 6. 常见坑与经验

组不会自动让 action checkable。互斥选择通常仍要给每个 action 设置 `setCheckable(true)`。

`removeAction()` 不销毁 action。生命周期由 parent 或持有者决定。

组的 enabled/visible 会影响成员整体，但单个 action 自身状态也要考虑；调试时要同时看 group 和 action。
