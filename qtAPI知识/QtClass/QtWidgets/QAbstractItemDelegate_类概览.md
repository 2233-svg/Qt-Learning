# Qt QAbstractItemDelegate 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractItemDelegate>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QObject -> QAbstractItemDelegate`  
> 定位：模型/视图代理的抽象基类

## 1. 先建立整体认识：它解决什么问题

在 Qt 的模型/视图体系里：

- `QAbstractItemModel` 提供数据；
- `QAbstractItemView` 决定怎么排布和交互；
- `QAbstractItemDelegate` 决定一个单元格怎么画、怎么编辑、怎么把结果写回模型。

所以代理（delegate）解决的是：

> **同一个模型数据，如何以特定的外观显示，并在用户编辑时使用合适的编辑器。**

例如：

- 普通文本单元格；
- 带复选框的布尔值；
- 进度条；
- 日期编辑器；
- 下拉选择器；
- 自定义按钮或状态图标。

`QAbstractItemDelegate` 本身是抽象基类，不能直接创建。实际开发通常继承：

- `QStyledItemDelegate`：优先推荐，能复用当前 Qt Style；
- `QItemDelegate`：老一些的绘制路线；
- `QAbstractItemDelegate`：你要完全接管绘制和编辑流程时才用。

## 2. 什么时候该用代理

| 需求 | 建议 |
| --- | --- |
| 只显示普通文本 | 使用默认 `QStyledItemDelegate` |
| 修改默认绘制样式 | 继承 `QStyledItemDelegate` 并重写 `paint()` |
| 修改单元格尺寸 | 重写 `sizeHint()` |
| 单元格双击后用自定义控件编辑 | 重写 `createEditor()` 等编辑函数 |
| 点击单元格就切换状态 | 重写 `editorEvent()` |
| 不同列使用不同编辑器 | 在 `createEditor()` 中根据 `index` 分支 |
| 需要图片、进度条、按钮 | 自定义 `paint()` 或 `editorEvent()` |

不要为了“给表格加一个输入框”就给每个单元格永久放一个 QWidget。  
代理的设计目的就是：只在需要时创建临时编辑器，平时用绘制完成展示。

## 3. 代理的两条工作路线

### 3.1 绘制路线

绘制一个单元格至少需要两个函数：

```cpp
void paint(QPainter *painter,
           const QStyleOptionViewItem &option,
           const QModelIndex &index) const override;

QSize sizeHint(const QStyleOptionViewItem &option,
               const QModelIndex &index) const override;
```

- `paint()` 决定画什么；
- `sizeHint()` 决定这个单元格需要多大。

只重写 `paint()` 不重写 `sizeHint()`，很容易出现内容被裁切或行高不够。

### 3.2 编辑路线

使用 QWidget 编辑器时，典型流程是：

```text
createEditor()
    -> setEditorData()
    -> updateEditorGeometry()
    -> 用户编辑
    -> commitData()
    -> setModelData()
    -> closeEditor()
    -> destroyEditor()
```

每个函数的职责要分开：

- `createEditor()`：创建什么控件；
- `setEditorData()`：把模型值填进控件；
- `updateEditorGeometry()`：控件放在哪里；
- `setModelData()`：把控件值写回模型；
- `destroyEditor()`：编辑结束后怎么销毁。

## 4. 最小可用代码

### 4.1 继承 `QStyledItemDelegate` 修改绘制

```cpp
class ProgressDelegate : public QStyledItemDelegate
{
public:
    using QStyledItemDelegate::QStyledItemDelegate;

    void paint(QPainter *painter,
               const QStyleOptionViewItem &option,
               const QModelIndex &index) const override
    {
        if (index.column() != 1) {
            QStyledItemDelegate::paint(painter, option, index);
            return;
        }

        QStyleOptionProgressBar progress;
        progress.rect = option.rect;
        progress.minimum = 0;
        progress.maximum = 100;
        progress.progress = index.data().toInt();
        progress.textVisible = true;
        progress.text = QString::number(progress.progress) + "%";

        QApplication::style()->drawControl(
            QStyle::CE_ProgressBar, &progress, painter);
    }
};
```

### 4.2 给某一列使用自定义编辑器

```cpp
QWidget *createEditor(QWidget *parent,
                      const QStyleOptionViewItem &option,
                      const QModelIndex &index) const override
{
    if (index.column() == 0)
        return new QLineEdit(parent);

    return QStyledItemDelegate::createEditor(parent, option, index);
}
```

真正可用时，还要配套实现 `setEditorData()` 和 `setModelData()`。

## 5. `EndEditHint`：编辑结束后下一步做什么

`closeEditor()` 的第二个参数不是“关闭原因”，而是给 view 的建议：

| 取值 | 含义 |
| --- | --- |
| `NoHint` | 不建议额外动作。 |
| `EditNextItem` | 继续编辑下一个单元格。 |
| `EditPreviousItem` | 继续编辑上一个单元格。 |
| `SubmitModelCache` | 建议模型提交缓存。 |
| `RevertModelCache` | 建议模型回滚缓存。 |

例如表格里按 Tab 连续录入时，可以发出：

```cpp
emit closeEditor(editor, QAbstractItemDelegate::EditNextItem);
```

## 6. 两种编辑事件方式

### 6.1 QWidget 编辑器：`createEditor()` 路线

适合需要完整输入控件的场景：

- `QLineEdit`
- `QSpinBox`
- `QComboBox`
- 自定义 QWidget

优点是交互完整，缺点是编辑期间会创建控件。

### 6.2 直接处理事件：`editorEvent()` 路线

适合简单状态切换：

- 点击复选框；
- 点击单元格里的按钮；
- 鼠标按下时切换一个标志；
- 不需要弹出真正编辑器的操作。

基类默认返回 `false`，表示没有处理事件。  
你处理成功后应返回 `true`，否则事件可能继续传给其他对象。

### 6.3 `handleEditorEvent()`：Qt 6.10+

这个函数用于统一处理活动编辑器的常见按键事件，典型包括：

- Tab
- Backtab
- Enter
- Escape

它通常在编辑器的事件过滤器中调用。调用后不要再重复调用父类 `eventFilter()`，否则可能产生重复处理。

## 7. `paintingRoles()` 的用途

`paintingRoles()` 返回绘制时会用到的模型角色列表。

如果自定义 delegate 只关心某几个角色，可以通过它告诉 view：

- 哪些角色变化会影响绘制；
- 哪些数据变化需要触发重绘。

这对减少不必要的刷新有帮助。  
如果你的代理依赖 `DisplayRole`、`DecorationRole`、`CheckStateRole` 等数据，应让返回值和实际绘制逻辑一致。

## 8. 常见误区

### 8.1 把 `paint()` 当成普通 QWidget 绘制

delegate 画的是 view 的一个单元格，不拥有独立窗口。  
绘制区域、状态、选中颜色等都应该优先从 `QStyleOptionViewItem` 读取。

### 8.2 在 `paint()` 里创建 QWidget

这样会带来大量对象和性能问题。  
需要临时编辑器时走 `createEditor()`。

### 8.3 `setEditorData()` 和 `setModelData()` 方向写反

- `setEditorData()`：模型 -> 编辑器
- `setModelData()`：编辑器 -> 模型

这是代理最常见的逻辑错误。

### 8.4 忘记发 `commitData()` 和 `closeEditor()`

自定义编辑器如果不发这两个信号，view 可能不知道：

- 什么时候该把数据写回模型；
- 什么时候该销毁编辑器；
- 是否应该跳到下一个单元格。

## API 速查表
下表按 Qt 6.11.1 的 `qabstractitemdelegate.h` 直接声明整理。delegate 的 API 要按两条路线读：绘制路线只需要 `paint()` / `sizeHint()`；编辑路线才进入 editor 创建、数据搬运、提交和关闭。

### 9.1 构造、绘制与尺寸

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAbstractItemDelegate(QObject *parent = nullptr)` | 创建 item delegate 抽象基类 | 不能直接实例化；通常继承 `QStyledItemDelegate` 更省力 |
| 生命周期 | `virtual ~QAbstractItemDelegate()` | 销毁代理对象 | 不要在多个 view 之间共享同一个 delegate 实例 |
| 绘制 | `paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const` | 绘制一个 index 对应的单元格 | 纯虚函数；绘制状态、区域和选中外观应从 `option` 读取 |
| 尺寸 | `sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const` | 返回一个 index 的建议尺寸 | 纯虚函数；绘制内容变高/变宽时必须同步考虑它 |
| 绘制角色 | `paintingRoles() const` | 返回绘制依赖的模型 role 列表 | 返回值应和 `paint()` 实际读取的数据一致，避免不必要或缺失刷新 |

### 9.2 QWidget 编辑器流程

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 创建编辑器 | `createEditor(QWidget *parent, const QStyleOptionViewItem &option, const QModelIndex &index) const` | 为单元格创建临时 QWidget 编辑器 | 基类默认不创建；editor 应以传入 parent 为父对象 |
| 销毁编辑器 | `destroyEditor(QWidget *editor, const QModelIndex &index) const` | 编辑结束后销毁 editor | 默认通常走延迟删除；特殊复用策略需保证生命周期清楚 |
| 模型到编辑器 | `setEditorData(QWidget *editor, const QModelIndex &index) const` | 把模型数据填入 editor | 方向是 model -> editor，不要写回模型 |
| 编辑器到模型 | `setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const` | 把 editor 中的数据写回模型 | 方向是 editor -> model；通常调用 `model->setData()` |
| 编辑器几何 | `updateEditorGeometry(QWidget *editor, const QStyleOptionViewItem &option, const QModelIndex &index) const` | 把 editor 放到单元格合适位置 | 常用 `option.rect`；滚动和 resize 后会再次调用 |
| 编辑器事件 | `handleEditorEvent(QObject *object, QEvent *event)` | 统一处理活动编辑器的 Tab、Enter、Escape 等事件 | Qt 6.10 起；在事件过滤器中调用后不要再重复交给父类处理同一事件 |

### 9.3 非 QWidget 编辑、帮助事件与信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 直接编辑事件 | `editorEvent(QEvent *event, QAbstractItemModel *model, const QStyleOptionViewItem &option, const QModelIndex &index)` | 不创建 QWidget，直接处理单元格事件 | 复选框、按钮区域、点击切换状态常用；处理成功返回 `true` |
| 帮助事件 | `helpEvent(QHelpEvent *event, QAbstractItemView *view, const QStyleOptionViewItem &option, const QModelIndex &index)` | 处理 tooltip、What's This 等帮助事件 | 文案通常来自模型 role 或 delegate 逻辑 |
| 信号 | `commitData(QWidget *editor)` | 通知 view 从 editor 提交数据 | 自定义 editor 完成编辑时发出，否则模型可能得不到新值 |
| 信号 | `closeEditor(QWidget *editor, EndEditHint hint = NoHint)` | 通知 view 关闭 editor，并给出后续编辑建议 | 常和 `commitData()` 连用；hint 可引导编辑下一个单元格 |
| 信号 | `sizeHintChanged(const QModelIndex &index)` | 通知 view 某项尺寸建议改变 | 动态内容高度变化后发出，促使视图重新布局 |

### 9.4 `EndEditHint` 与受保护构造

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结束建议 | `NoHint` | 关闭编辑器后不建议额外动作 | 默认选择 |
| 结束建议 | `EditNextItem` | 建议 view 继续编辑下一个项目 | 表格连续录入常用 |
| 结束建议 | `EditPreviousItem` | 建议 view 继续编辑上一个项目 | Shift+Tab 或反向录入 |
| 结束建议 | `SubmitModelCache` | 建议模型提交缓存 | 仅对支持缓存提交的模型有意义 |
| 结束建议 | `RevertModelCache` | 建议模型回滚缓存 | 取消批量编辑或数据库缓存时使用 |
| 派生构造 | `QAbstractItemDelegate(QObjectPrivate &, QObject *parent = nullptr)` | Qt 内部或特殊派生类传入私有实现 | 普通业务派生类不使用 |

## 10. 一句话总结

`QAbstractItemDelegate` 是模型数据和视图单元格之间的“显示与编辑契约”：`paint()` 负责画，`sizeHint()` 负责尺寸，`createEditor()` 到 `setModelData()` 负责编辑闭环。
