# Qt QWhatsThis 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWhatsThis>`  
> 所属模块：`Qt6::Widgets`  
> 继承：无  
> 定位：交互式上下文帮助

## 1. 先建立整体认识：它解决什么问题

`QWhatsThis` 提供的是“用户主动点一下某个控件，再看这块具体是干什么”的帮助机制。  
它和悬停即出现的 `QToolTip` 不一样：

- `QToolTip`：鼠标停留时给短提示；
- `QWhatsThis`：进入帮助模式后，用户点目标控件查看更完整的说明。

这很适合功能密度高、控件名称无法写得很长的桌面软件。

## 2. 日常用法：先给对象放帮助文本

通常并不直接调用 `QWhatsThis::showText()`，而是给控件或 action 设置说明：

```cpp
auto *exportButton = new QPushButton(tr("导出"), this);
exportButton->setWhatsThis(
    tr("将当前表格导出为 CSV 文件。导出不会修改原始数据。"));

auto *exportAction = new QAction(tr("导出"), this);
exportAction->setWhatsThis(
    tr("将当前表格导出为 CSV 文件。"));
```

用户按下帮助快捷键或点击“这是什么？” action 后，Qt 进入 What’s This 模式；下一次点击带帮助文本的对象时，Qt 显示该文本。

## 3. 怎么给用户一个进入帮助模式的入口

`createAction()` 创建一个标准的“这是什么？” action，可以放到菜单、工具栏或帮助按钮上：

```cpp
QAction *whatsThisAction = QWhatsThis::createAction(this);
helpMenu->addAction(whatsThisAction);
```

也可以在代码中直接进入或离开帮助模式：

```cpp
QWhatsThis::enterWhatsThisMode();
// 用户选择一个控件后，Qt 通常会自动结束该模式
```

## 4. `showText()` 适合什么

`showText()` 用于你自己决定何时、何处显示帮助泡泡，例如自定义帮助按钮或无标准 widget 的画布区域：

```cpp
QWhatsThis::showText(
    QCursor::pos(),
    tr("拖动节点可以改变流程顺序。"),
    this);
```

`pos` 是屏幕坐标。可选的 `w` 用来把帮助文本和某个 widget 上下文关联起来；它不是文本内容的所有者。

## 5. 常见误区

- 只给控件设置 `toolTip`，不会自动得到 What’s This 内容；
- 不要把 What’s This 当成长篇帮助中心，它更适合解释当前控件、当前操作；
- `enterWhatsThisMode()` 后要考虑用户取消操作的路径，可用 `inWhatsThisMode()` 检查状态；
- `showText()` 的位置是全局坐标，不是 widget 内部坐标；
- 静态类不能实例化，所有 API 都是静态函数。

## 6. API 逐项说明

### `createAction(QObject *parent)`

创建一个触发 What’s This 模式的标准 `QAction`。返回的 action 由传入 parent 管理。

### `enterWhatsThisMode()`

让应用进入“下一次点击用于查询帮助”的交互状态。

### `inWhatsThisMode()`

查询当前是否仍处于 What’s This 模式。

### `leaveWhatsThisMode()`

主动退出帮助模式。适合用户按下取消键、关闭自定义帮助面板等场景。

### `showText(const QPoint &pos, const QString &text, QWidget *w)`

在屏幕坐标 `pos` 显示一段帮助文本。用于手动展示上下文帮助。

### `hideText()`

隐藏当前正在显示的 What’s This 帮助文本。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 静态工厂 | `QAction *QWhatsThis::createAction(QObject *parent = nullptr)` | 创建进入 What’s This 模式的标准 action。 | 将 action 放进菜单或工具栏；parent 管理其生命周期。 |
| 模式控制 | `void QWhatsThis::enterWhatsThisMode()` | 进入交互式上下文帮助模式。 | 用户下一次点击通常用于选取帮助目标。 |
| 模式查询 | `bool QWhatsThis::inWhatsThisMode()` | 查询是否处于帮助选择模式。 | 适合在取消操作或自定义帮助 UI 中判断状态。 |
| 模式控制 | `void QWhatsThis::leaveWhatsThisMode()` | 主动离开帮助选择模式。 | 用户取消或模式切换时调用。 |
| 手动显示 | `void QWhatsThis::showText(const QPoint &pos, const QString &text, QWidget *w = nullptr)` | 在指定屏幕位置显示帮助泡泡。 | `pos` 是全局坐标，不是 widget 局部坐标。 |
| 手动隐藏 | `void QWhatsThis::hideText()` | 隐藏当前 What’s This 文本。 | 只影响帮助泡泡，不改变对象设置的帮助内容。 |

## 8. 一句话总结

`QWhatsThis` 是 Qt 的点击式上下文帮助机制：先给控件设置 `whatsThis` 文本，再让用户在帮助模式里点到需要解释的地方。
